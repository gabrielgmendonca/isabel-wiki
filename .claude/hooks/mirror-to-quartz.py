#!/usr/bin/env python3
"""PostToolUse hook: espelha wiki/**/*.md (e index.md raiz) editado para o mirror
do Quartz em /tmp/quartz/content/, destravando hot-rebuild do `npx quartz build --serve`.

Sem este hook, edições no repo não aparecem no preview local até refazer `cp` manual
ou re-rodar `scripts/serve-local.sh` (rebuild completo ~10-15s). Com ele, o Quartz
detecta o mtime atualizado e hot-rebuilda (~6s). Roadmap §5.

Trava de segurança: só atua se `/tmp/quartz/content/wiki/` existir — em máquina/
sessão que não rodou `serve-local.sh`, é noop silencioso.

Limitação consciente: pre-processadores de CI (link_citations.py, wrap_glossary_terms.py,
inject_copyright.py) NÃO rodam aqui — preview de dev fica "raw" comparado ao deploy
(sem auto-link Kardecpedia, sem <abbr>, sem callout de direitos). Aceitável para
inspeção visual de estrutura, tipografia, Mermaid e wikilinks internos.
"""
from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path

MIRROR_ROOT = Path("/tmp/quartz/content")


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    if event.get("tool_name") not in ("Edit", "Write", "MultiEdit"):
        return 0

    target_raw = (event.get("tool_input") or {}).get("file_path")
    if not target_raw:
        return 0

    if not (MIRROR_ROOT / "wiki").is_dir():
        return 0

    cwd = event.get("cwd") or os.getcwd()
    try:
        rel = os.path.relpath(target_raw, cwd).replace(os.sep, "/")
    except ValueError:
        return 0
    if rel.startswith("../") or not rel.endswith(".md"):
        return 0
    if not (rel.startswith("wiki/") or rel == "index.md"):
        return 0

    src = Path(cwd) / rel
    if not src.is_file():
        return 0

    dst = MIRROR_ROOT / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        shutil.copy2(src, dst)
    except OSError as exc:
        print(f"mirror-to-quartz: copy falhou ({rel}): {exc}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
