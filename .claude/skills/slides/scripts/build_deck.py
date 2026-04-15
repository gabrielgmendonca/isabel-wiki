#!/usr/bin/env python3
"""Build de deck Marp em PPTX e PDF via npx @marp-team/marp-cli.

Requer Node disponível no PATH. Não instala nada globalmente — usa `npx -y`.
"""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

THEME = Path("slides/themes/isabel.css")


def run_marp(deck: Path, out: Path, fmt: str) -> tuple[int, str]:
    cmd = [
        "npx", "-y", "@marp-team/marp-cli@latest",
        str(deck),
        f"--{fmt}",
        "--allow-local-files",
        "-o", str(out),
    ]
    if THEME.exists():
        cmd.extend(["--theme", str(THEME)])
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode, (proc.stderr or proc.stdout).strip()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("deck", type=Path, help="Caminho para deck.md")
    ap.add_argument("--formats", nargs="+", default=["pptx", "pdf"], choices=["pptx", "pdf", "html"])
    args = ap.parse_args()

    if not args.deck.exists():
        print(json.dumps({"error": f"deck not found: {args.deck}"}))
        return 1
    if shutil.which("npx") is None:
        print(json.dumps({"error": "npx not found in PATH; install Node.js to build slides"}))
        return 1

    build_dir = args.deck.parent / "build"
    build_dir.mkdir(parents=True, exist_ok=True)

    results = {}
    failed = False
    for fmt in args.formats:
        out = build_dir / f"{args.deck.stem}.{fmt}"
        code, msg = run_marp(args.deck, out, fmt)
        results[fmt] = {"path": str(out), "ok": code == 0, "message": msg}
        if code != 0:
            failed = True

    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
