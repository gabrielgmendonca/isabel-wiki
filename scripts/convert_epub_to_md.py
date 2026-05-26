#!/usr/bin/env python3
"""Converte arquivos .epub para .md via markitdown.

markitdown >=0.1.5 lê EPUB nativamente (usa beautifulsoup4 + markdownify
da base, sem extra próprio). Suporta arquivo único ou diretório.

O .md é salvo ao lado do .epub. Para impor o layout canônico de raw/
(raw/autores/<autor-slug>/<obra-slug>/<obra-slug>.md), rodar
`scripts/normalize_raw_layout.py` depois.

Uso:
    uv run python scripts/convert_epub_to_md.py raw/autores/leon-denis/o-problema-do-ser.epub
    uv run python scripts/convert_epub_to_md.py raw/autores/leon-denis/
    uv run python scripts/convert_epub_to_md.py raw/autores/leon-denis/ --force
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from markitdown import MarkItDown

# Match Markdown image whose src is a data: URI (often base64-encoded image
# embutida no EPUB). Substitui por placeholder vazio para preservar o ritmo
# do layout sem carregar centenas de KB de base64 por obra.
DATA_URI_IMAGE_RE = re.compile(r"!\[[^\]]*\]\(data:[^)]+\)")


def epub_to_md(epub_path: Path, md_converter: MarkItDown) -> str:
    result = md_converter.convert(str(epub_path))
    text = result.text_content
    # Remove imagens em data: URI (markitdown inlina como base64).
    cleaned = DATA_URI_IMAGE_RE.sub("![](image)", text)
    # Compacta runs de linhas vazias resultantes da remoção.
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip() + "\n"


def convert_one(
    epub: Path,
    output_dir: Path,
    force: bool,
    converter: MarkItDown,
) -> str:
    md_out = output_dir / f"{epub.stem}.md"
    if md_out.exists() and not force:
        return f"  [skip] {epub.name} (já existe {md_out.name})"
    md_text = epub_to_md(epub, converter)
    md_out.write_text(md_text, encoding="utf-8")
    size_kb = md_out.stat().st_size / 1024
    return f"  [conv] {epub.name} → {md_out.name} ({size_kb:.1f} KB)"


def collect_epubs(input_path: Path) -> list[Path]:
    if input_path.is_file():
        if input_path.suffix.lower() != ".epub":
            sys.exit(f"ERRO: {input_path} não é .epub.")
        return [input_path]
    if input_path.is_dir():
        return sorted(input_path.glob("*.epub"))
    sys.exit(f"ERRO: {input_path} não existe.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "input",
        type=Path,
        help="Arquivo .epub ou diretório com .epub para converter.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Diretório de saída (default: mesmo do arquivo de entrada).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Sobrescreve .md existente.",
    )
    args = parser.parse_args()

    epubs = collect_epubs(args.input)
    if not epubs:
        print(f"Nenhum .epub encontrado em {args.input}")
        return

    base_out = args.output_dir
    if base_out:
        base_out.mkdir(parents=True, exist_ok=True)

    converter = MarkItDown()
    converted = skipped = failed = 0

    for epub in epubs:
        out_dir = base_out or epub.parent
        try:
            line = convert_one(epub, out_dir, args.force, converter)
            print(line)
            if line.startswith("  [conv]"):
                converted += 1
            else:
                skipped += 1
        except Exception as exc:  # noqa: BLE001
            print(f"  [fail] {epub.name}: {exc}")
            failed += 1

    print(
        f"\nResultado: {converted} convertido(s), "
        f"{skipped} pulado(s), {failed} falha(s)."
    )
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
