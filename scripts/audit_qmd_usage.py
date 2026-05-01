"""Audita uso de qmd vs grep/find/rg nos transcripts locais do Claude Code
para este projeto. Lê `.jsonl` em ~/.claude-personal/projects/<projeto>/ e
imprime relatório no stdout.

Uso:
    uv run python scripts/audit_qmd_usage.py
    uv run python scripts/audit_qmd_usage.py --since 2026-05-01
    uv run python scripts/audit_qmd_usage.py --since 2026-05-01 --top 30
"""
from __future__ import annotations

import argparse
import json
import os
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path

PROJECT_DIR = Path.home() / ".claude-personal/projects/-Users-gabrielmendonca-Documents-Personal-isabel-wiki"
SEARCH_CMD_RE = re.compile(r"\b(grep|rg|ripgrep|fgrep|egrep|find|ag)\b")
# Mesma lógica do hook .claude/hooks/inject-rules.py — exige wiki/ ou raw/
# como segmento de path, evitando falso positivo em "isabel-wiki" etc.
WIKI_RAW_PATH_RE = re.compile(r"(?:^|[\s'\"=({])(?:wiki|raw)/")


def parse_session(path: Path) -> dict:
    """Conta chamadas qmd e Bash-search numa sessão."""
    stats = {
        "qmd_calls": 0,
        "qmd_by_tool": defaultdict(int),
        "bash_search_calls": 0,
        "bash_search_in_wiki_or_raw": 0,
    }
    try:
        with path.open(encoding="utf-8") as f:
            for line in f:
                try:
                    d = json.loads(line)
                except json.JSONDecodeError:
                    continue
                content = (d.get("message") or {}).get("content") or []
                if not isinstance(content, list):
                    continue
                for c in content:
                    if not (isinstance(c, dict) and c.get("type") == "tool_use"):
                        continue
                    name = c.get("name", "")
                    if name.startswith("mcp__qmd__"):
                        stats["qmd_calls"] += 1
                        stats["qmd_by_tool"][name.replace("mcp__qmd__", "")] += 1
                    elif name == "Bash":
                        cmd = (c.get("input") or {}).get("command", "")
                        if SEARCH_CMD_RE.search(cmd):
                            stats["bash_search_calls"] += 1
                            # Normaliza paths absolutos antes de checar — espelha o hook.
                            normalized = cmd.replace(str(Path.cwd()) + "/", "")
                            if WIKI_RAW_PATH_RE.search(normalized):
                                stats["bash_search_in_wiki_or_raw"] += 1
    except OSError:
        pass
    return stats


def session_date(path: Path) -> str:
    """Data de modificação do arquivo (YYYY-MM-DD)."""
    return datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d")


def session_week(path: Path) -> str:
    return datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-W%V")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--since", help="ignorar sessões antes desta data (YYYY-MM-DD)")
    parser.add_argument("--top", type=int, default=15, help="top N sessões mais recentes (default: 15)")
    parser.add_argument("--project-dir", type=Path, default=PROJECT_DIR)
    args = parser.parse_args()

    if not args.project_dir.is_dir():
        print(f"erro: diretório não existe: {args.project_dir}")
        return 1

    sessions = sorted(args.project_dir.glob("*.jsonl"))
    if args.since:
        cutoff = datetime.strptime(args.since, "%Y-%m-%d").date()
        sessions = [s for s in sessions if datetime.fromtimestamp(s.stat().st_mtime).date() >= cutoff]

    if not sessions:
        print("sem sessões no recorte.")
        return 0

    weekly = defaultdict(lambda: {"total": 0, "with_qmd": 0, "qmd_calls": 0, "bash_search_wiki": 0})
    qmd_tool_breakdown = defaultdict(int)
    rows = []

    for s in sessions:
        st = parse_session(s)
        week = session_week(s)
        weekly[week]["total"] += 1
        weekly[week]["qmd_calls"] += st["qmd_calls"]
        weekly[week]["bash_search_wiki"] += st["bash_search_in_wiki_or_raw"]
        if st["qmd_calls"] > 0:
            weekly[week]["with_qmd"] += 1
        for tool, n in st["qmd_by_tool"].items():
            qmd_tool_breakdown[tool] += n
        rows.append((session_date(s), s.name, st))

    total_sessions = len(sessions)
    sessions_with_qmd = sum(1 for _, _, st in rows if st["qmd_calls"] > 0)
    total_qmd = sum(st["qmd_calls"] for _, _, st in rows)
    total_bash_search_wiki = sum(st["bash_search_in_wiki_or_raw"] for _, _, st in rows)
    candidate_sessions = sum(1 for _, _, st in rows if st["qmd_calls"] > 0 or st["bash_search_in_wiki_or_raw"] > 0)
    qmd_share = (sessions_with_qmd / candidate_sessions * 100) if candidate_sessions else 0

    print(f"=== Auditoria qmd — {args.project_dir.name} ===")
    if args.since:
        print(f"Recorte: desde {args.since}")
    print(f"Sessões totais: {total_sessions}")
    print(f"Sessões com busca em wiki/raw (qmd OU Bash): {candidate_sessions}")
    print(f"  → das quais usaram qmd: {sessions_with_qmd} ({qmd_share:.0f}%)")
    print(f"Chamadas qmd totais: {total_qmd}")
    print(f"Buscas Bash em wiki/raw totais: {total_bash_search_wiki}")
    print()

    print("=== Quebra por ferramenta qmd ===")
    for tool, n in sorted(qmd_tool_breakdown.items(), key=lambda x: -x[1]):
        print(f"  {tool}: {n}")
    print()

    print("=== Tendência semanal ===")
    print(f"{'semana':<12} {'total':>6} {'com_qmd':>8} {'qmd_calls':>10} {'bash_w/r':>10}")
    for week in sorted(weekly):
        w = weekly[week]
        print(f"{week:<12} {w['total']:>6} {w['with_qmd']:>8} {w['qmd_calls']:>10} {w['bash_search_wiki']:>10}")
    print()

    print(f"=== Top {args.top} sessões mais recentes ===")
    print(f"{'data':<12} {'qmd':>4} {'bash_w/r':>9}  arquivo")
    for date, name, st in sorted(rows, reverse=True)[: args.top]:
        print(f"{date:<12} {st['qmd_calls']:>4} {st['bash_search_in_wiki_or_raw']:>9}  {name}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
