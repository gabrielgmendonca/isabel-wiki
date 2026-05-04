#!/usr/bin/env python3
"""PostToolUse hook: lint leve por arquivo após Edit/Write/MultiEdit em wiki/**/*.md.

Roda os checks isoláveis de `lint_wiki.py` sobre o arquivo recém-editado e devolve
findings de severity error/warning via `hookSpecificOutput.additionalContext`.
Não bloqueia: Claude vê o aviso no próximo turno, sem trancar o edit.

Frontmatter inválido, tag fora dos namespaces canônicos e wikilink quebrado são
detectados no momento da edição em vez de no fim do `/ingest`. Roadmap §5.

Importa `lint_single_file` direto (em vez de spawnar subprocesso) para evitar
um segundo `uv run` — o hook já roda dentro de `uv run --project`, então o
import só paga o custo de compilar regex.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "lint" / "scripts"))
sys.path.insert(0, str(ROOT / ".claude" / "skills"))

from lint_wiki import lint_single_file  # noqa: E402


def _format_findings(result: dict) -> str:
    """Renderiza findings de error/warning como bullets curtos para additionalContext.

    Info-level fica fora — é ruído no edit-time; vai pelo `/lint` global.
    """
    lines = [f"Lint pós-edit em `{result['file']}`:"]
    for name, check in result["checks"].items():
        if check["count"] == 0 or check["severity"] == "info":
            continue
        for item in check["items"]:
            detail = (
                item.get("detail")
                or item.get("citation")
                or item.get("target")
                or ""
            )
            lineno = item.get("line")
            loc = f"L{lineno}: " if lineno else ""
            lines.append(f"- [{check['severity']}] {name}: {loc}{detail}".rstrip())
    return "\n".join(lines)


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        print(f"lint-on-edit: invalid event JSON on stdin: {exc}", file=sys.stderr)
        return 0

    if event.get("tool_name") not in ("Edit", "Write", "MultiEdit"):
        return 0

    target_raw = (event.get("tool_input") or {}).get("file_path")
    if not target_raw:
        return 0

    cwd = event.get("cwd") or os.getcwd()
    try:
        rel = os.path.relpath(target_raw, cwd).replace(os.sep, "/")
    except ValueError:
        return 0
    if rel.startswith("../") or not rel.startswith("wiki/") or not rel.endswith(".md"):
        return 0

    # rodar a partir da raiz para que paths relativos batam com o que os checks emitem
    os.chdir(cwd)
    target = Path(rel)
    if not target.exists():
        return 0

    try:
        result = lint_single_file(target)
    except Exception as exc:  # noqa: BLE001
        print(f"lint-on-edit: falha em lint_single_file: {exc}", file=sys.stderr)
        return 0

    if "error" in result:
        return 0

    has_findings = any(
        c["count"] > 0 and c["severity"] in ("error", "warning")
        for c in result["checks"].values()
    )
    if not has_findings:
        return 0

    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": _format_findings(result),
            }
        },
        sys.stdout,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
