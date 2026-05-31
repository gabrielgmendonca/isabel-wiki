#!/usr/bin/env python3
# Executar sempre com: uv run python .claude/skills/critica/scripts/critica_scope.py
"""Seleção de escopo e histórico do workflow /critica.

Emite a lista de páginas **devidas** para crítica profunda — nunca criticadas,
ou cujo CORPO mudou desde a última crítica, ou cujo `atualizado_em` é mais
recente que a última crítica. Mantém o estado de máquina em
`.claude/skills/critica/state/critica-state.json` (hash do corpo + data da
última crítica + veredito por página), separado do `log.md` narrativo.

Hash apenas do CORPO (sem frontmatter): a própria crítica reescreve
`atualizado_em`/tags ao auto-corrigir; se o hash incluísse o frontmatter, todo
auto-fix marcaria a página suja para sempre (loop de re-crítica).

Subcomandos:
    scope   (default) — emite JSON das páginas devidas. Read-only.
    record            — atualiza o estado após um run (recomputa hashes).

Uso:
    uv run python .claude/skills/critica/scripts/critica_scope.py
    uv run python .claude/skills/critica/scripts/critica_scope.py --limit 15
    uv run python .claude/skills/critica/scripts/critica_scope.py --path 'wiki/conceitos/*' --status ativo
    uv run python .claude/skills/critica/scripts/critica_scope.py --all
    uv run python .claude/skills/critica/scripts/critica_scope.py --format summary
    uv run python .claude/skills/critica/scripts/critica_scope.py record --from results.json
"""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import sys
from datetime import date
from pathlib import Path

# Permitir `from _lib.wiki_utils import ...` (raiz em .claude/skills/).
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _lib.wiki_utils import collect_pages, parse_frontmatter  # noqa: E402

STATE_PATH = Path(__file__).resolve().parents[1] / "state" / "critica-state.json"

# Tipos que NÃO recebem crítica doutrinária por design:
# - capítulos/índices bíblicos são texto-fonte (Escritura), não conteúdo
#   curado; divergência com o Pentateuco se trata em wiki/divergencias/, não na
#   transcrição literal.
SKIP_TIPOS = {"capitulo-biblico", "livro-biblico"}

# Peso de prioridade por tipo: menor = mais prioritário. Doutrina densa antes
# de páginas descritivas.
TIPO_WEIGHT = {
    "divergencia": 0,
    "questao": 0,
    "aprofundamento": 0,
    "conceito": 1,
    "sintese": 1,
    "parabola": 1,
    "obra": 2,
    "personalidade": 3,
}

# Ordem de exibição/limit por motivo (precedência).
REASON_ORDER = {"nunca-criticada": 0, "corpo-alterado": 1, "atualizado-apos-critica": 2}


def body_sha(path: Path) -> str:
    """sha256 do corpo da página, excluindo o bloco de frontmatter `--- … ---`."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                body = "\n".join(lines[i + 1:])
                break
        else:
            body = text
    else:
        body = text
    return "sha256:" + hashlib.sha256(body.encode("utf-8")).hexdigest()


def load_state() -> dict:
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    return {"version": 1, "last_run": None, "pages": {}}


def save_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def _due_reason(path_str: str, fm: dict, sha: str, state_pages: dict) -> str | None:
    """Retorna o motivo de a página ser devida, ou None se em dia."""
    entry = state_pages.get(path_str)
    if entry is None:
        return "nunca-criticada"
    if entry.get("content_sha") != sha:
        return "corpo-alterado"
    atualizado = str(fm.get("atualizado_em", "") or "")
    last = str(entry.get("last_critica_date", "") or "")
    if atualizado and last and atualizado > last:
        return "atualizado-apos-critica"
    return None


def compute_scope(args: argparse.Namespace) -> dict:
    state = load_state()
    state_pages = state.get("pages", {})
    due: list[dict] = []
    total = 0

    for path in collect_pages():
        path_str = str(path)
        fm, _ = parse_frontmatter(path)
        tipo = str(fm.get("tipo", "") or "")
        if tipo in SKIP_TIPOS and not args.include_biblia:
            continue
        if str(fm.get("index", "")).lower() == "false" and not args.include_meta:
            continue
        total += 1

        if args.path and not any(fnmatch.fnmatch(path_str, g) for g in args.path):
            continue
        if args.status and str(fm.get("status", "") or "") != args.status:
            continue

        sha = body_sha(path)
        atualizado = str(fm.get("atualizado_em", "") or "")
        if args.since and atualizado and atualizado < args.since:
            continue

        if args.all:
            reason = "forcado-all"
        else:
            reason = _due_reason(path_str, fm, sha, state_pages)
            if reason is None:
                continue

        entry = state_pages.get(path_str, {})
        due.append({
            "path": path_str,
            "reason": reason,
            "tipo": tipo,
            "status": str(fm.get("status", "") or ""),
            "atualizado_em": atualizado,
            "sha": sha,
            "last_critica_date": entry.get("last_critica_date"),
        })

    def sort_key(p: dict):
        return (
            REASON_ORDER.get(p["reason"], 9),
            TIPO_WEIGHT.get(p["tipo"], 2),
            # mais antigo (ou nunca) primeiro: atualizado_em ascendente
            p["atualizado_em"] or "0000-00-00",
            p["path"],
        )

    due.sort(key=sort_key)
    truncated = False
    if args.limit and len(due) > args.limit:
        due = due[: args.limit]
        truncated = True

    return {
        "generated": date.today().isoformat(),
        "total_wiki": total,
        "due_count": len(due),
        "truncated": truncated,
        "last_run": state.get("last_run"),
        "pages": due,
    }


def cmd_scope(args: argparse.Namespace) -> int:
    result = compute_scope(args)
    if args.format == "summary":
        lines = [
            f"Escopo /critica — {result['generated']}",
            f"  páginas wiki elegíveis: {result['total_wiki']}",
            f"  devidas (após filtros): {result['due_count']}"
            + (" [truncado por --limit]" if result["truncated"] else ""),
            f"  última crítica (run): {result['last_run'] or 'nunca'}",
            "",
        ]
        for p in result["pages"]:
            lines.append(f"  - {p['path']}  ({p['reason']}, {p['tipo'] or '—'})")
        sys.stdout.write("\n".join(lines) + "\n")
    else:
        sys.stdout.write(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    return 0


def cmd_record(args: argparse.Namespace) -> int:
    """Atualiza o estado após um run a partir de um JSON de resultados.

    Espera `{"pages": [{"path", "verdict", "findings_count", "deferred_count"}]}`
    (via --from <arquivo> ou stdin). Recomputa o hash do corpo ATUAL de cada
    página (já com os auto-fixes aplicados) e grava a data da crítica.
    """
    raw = Path(args.from_file).read_text(encoding="utf-8") if args.from_file else sys.stdin.read()
    payload = json.loads(raw)
    run_date = args.date or date.today().isoformat()

    state = load_state()
    state.setdefault("pages", {})
    updated = 0
    for rec in payload.get("pages", []):
        path = Path(rec["path"])
        if not path.exists():
            sys.stderr.write(f"aviso: página inexistente, pulando: {path}\n")
            continue
        fm, _ = parse_frontmatter(path)
        state["pages"][str(path)] = {
            "content_sha": body_sha(path),
            "last_critica_date": run_date,
            "atualizado_em_at_critica": str(fm.get("atualizado_em", "") or ""),
            "verdict": rec.get("verdict", "clean"),
            "findings_count": int(rec.get("findings_count", 0)),
            "deferred_count": int(rec.get("deferred_count", 0)),
        }
        updated += 1

    state["last_run"] = args.timestamp or run_date
    save_state(state)
    sys.stdout.write(json.dumps({"recorded": updated, "state": str(STATE_PATH)}, ensure_ascii=False) + "\n")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Escopo e histórico do /critica.")
    sub = parser.add_subparsers(dest="cmd")

    sc = sub.add_parser("scope", help="Emite JSON das páginas devidas (default).")
    for p in (parser, sc):  # aceitar flags tanto sem subcomando quanto em `scope`
        p.add_argument("--all", action="store_true", help="Ignora o estado; emite todas as páginas elegíveis.")
        p.add_argument("--since", metavar="YYYY-MM-DD", help="Só páginas com atualizado_em >= data.")
        p.add_argument("--path", action="append", default=[], metavar="GLOB", help="Restringe a um glob (repetível).")
        p.add_argument("--limit", type=int, default=0, metavar="N", help="Limita às N páginas mais prioritárias.")
        p.add_argument("--status", metavar="STATUS", help="Só páginas com este status (ex.: ativo).")
        p.add_argument("--include-biblia", action="store_true", help="Inclui capítulos/índices bíblicos.")
        p.add_argument("--include-meta", action="store_true", help="Inclui páginas com index: false.")
        p.add_argument("--format", choices=("json", "summary"), default="json", help="Formato de saída.")

    rec = sub.add_parser("record", help="Atualiza o estado após um run.")
    rec.add_argument("--from", dest="from_file", metavar="PATH", help="Arquivo JSON de resultados (default: stdin).")
    rec.add_argument("--date", metavar="YYYY-MM-DD", help="Data da crítica (default: hoje).")
    rec.add_argument("--timestamp", metavar="TS", help="Carimbo de last_run (default: igual a --date).")

    args = parser.parse_args(argv)
    if args.cmd == "record":
        return cmd_record(args)
    return cmd_scope(args)


if __name__ == "__main__":
    sys.exit(main())
