#!/usr/bin/env python3
"""Converte embeds do YouTube com tempo em <iframe> que começa no trecho certo.

O embed nativo do Quartz (`![](https://www.youtube.com/watch?v=ID)`) descarta o
parâmetro `t=` e sempre abre o vídeo no início. Para as páginas que citam uma
fala pelo tempo (Pinga-Fogo), o markdown-fonte usa

    ![Pinga-Fogo I, 0:37:13](https://www.youtube.com/watch?v=v5waIS1qedA&t=2233s)

e este script, no CI e sobre a cópia, troca esse embed por um <iframe> com
`start=` (e `end=`, se a URL trouxer `&end=N`). Embeds sem `t=` ficam para o
Quartz. O markdown-fonte não é alterado; no Obsidian o embed continua valendo.

Uso:
  uv run python scripts/embed_youtube_clips.py --check wiki/
  python3 scripts/embed_youtube_clips.py --apply /tmp/quartz/content/wiki
"""
from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

EMBED_RE = re.compile(
    r"!\[(?P<alt>[^\]]*)\]\((?P<url>https?://(?:www\.)?youtube\.com/watch\?v=(?P<id>[\w-]{11})(?P<params>[^)\s]*))\)"
)
T_RE = re.compile(r"[?&]t=(\d+)s?\b")
END_RE = re.compile(r"[?&]end=(\d+)\b")
FENCE_RE = re.compile(r"```.*?```", re.S)


def iframe(alt: str, video: str, start: int, end: int | None) -> str:
    query = f"start={start}" + (f"&amp;end={end}" if end else "")
    titulo = html.escape(alt or "Vídeo", quote=True)
    return (
        f'<iframe class="external-embed youtube clip" loading="lazy" '
        f'src="https://www.youtube-nocookie.com/embed/{video}?{query}&amp;rel=0" '
        f'title="{titulo}" allow="fullscreen; picture-in-picture" frameborder="0"></iframe>'
    )


def converter(texto: str) -> tuple[str, int]:
    n = 0

    def troca(m: re.Match) -> str:
        nonlocal n
        t = T_RE.search(m.group("params"))
        if not t:
            return m.group(0)
        end = END_RE.search(m.group("params"))
        n += 1
        return iframe(m.group("alt"), m.group("id"), int(t.group(1)), int(end.group(1)) if end else None)

    partes, ultimo = [], 0
    for f in FENCE_RE.finditer(texto):
        partes.append(EMBED_RE.sub(troca, texto[ultimo:f.start()]))
        partes.append(f.group(0))
        ultimo = f.end()
    partes.append(EMBED_RE.sub(troca, texto[ultimo:]))
    return "".join(partes), n


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    modo = ap.add_mutually_exclusive_group(required=True)
    modo.add_argument("--check", action="store_true", help="só conta os embeds com tempo")
    modo.add_argument("--apply", action="store_true", help="reescreve os arquivos (usar só na cópia do CI)")
    ap.add_argument("alvo", type=Path)
    args = ap.parse_args()
    arquivos = [args.alvo] if args.alvo.is_file() else sorted(args.alvo.rglob("*.md"))
    total = 0
    for p in arquivos:
        texto = p.read_text(encoding="utf-8")
        novo, n = converter(texto)
        if n:
            total += n
            if args.apply:
                p.write_text(novo, encoding="utf-8")
    print(f"{total} embed(s) com tempo em {len(arquivos)} arquivo(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
