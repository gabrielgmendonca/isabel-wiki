#!/usr/bin/env python3
"""Converte arquivos .doc legados para .md via markitdown.

Pipeline: .doc → .docx (LibreOffice headless) → .md (markitdown).
markitdown não suporta o formato binário .doc legado, então passamos por
.docx intermediário gerado pelo soffice.

Uso:
    uv run python scripts/convert_doc_to_md.py raw/autores/camille-flammarion/
    uv run python scripts/convert_doc_to_md.py raw/autores/camille-flammarion/ --force
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from markitdown import MarkItDown

SOFFICE_CANDIDATES = [
    "/Applications/LibreOffice.app/Contents/MacOS/soffice",
    "soffice",
    "libreoffice",
]

# Match Markdown image whose src is a data: URI (often base64-encoded image
# extracted from the docx). Replace with empty image placeholder so the layout
# beat survives but we don't carry hundreds of KB of base64 per obra.
DATA_URI_IMAGE_RE = re.compile(r"!\[[^\]]*\]\(data:[^)]+\)")


def find_soffice() -> str:
    for candidate in SOFFICE_CANDIDATES:
        resolved = shutil.which(candidate) if "/" not in candidate else (
            candidate if Path(candidate).exists() else None
        )
        if resolved:
            return resolved
    sys.exit(
        "ERRO: LibreOffice (soffice) não encontrado. Instale o LibreOffice "
        "ou ajuste SOFFICE_CANDIDATES."
    )


def doc_to_docx(doc_path: Path, out_dir: Path, soffice: str) -> Path:
    """Converte .doc → .docx via LibreOffice headless."""
    result = subprocess.run(
        [
            soffice,
            "--headless",
            "--convert-to",
            "docx",
            "--outdir",
            str(out_dir),
            str(doc_path),
        ],
        capture_output=True,
        text=True,
        timeout=300,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"soffice falhou em {doc_path.name}:\n"
            f"stdout: {result.stdout}\nstderr: {result.stderr}"
        )
    docx_path = out_dir / f"{doc_path.stem}.docx"
    if not docx_path.exists():
        raise RuntimeError(
            f"soffice não produziu {docx_path} (stdout: {result.stdout})"
        )
    return docx_path


def docx_to_md(docx_path: Path, md_converter: MarkItDown) -> str:
    result = md_converter.convert(str(docx_path))
    text = result.text_content
    # Remove imagens em data: URI (markitdown inlina como base64).
    cleaned = DATA_URI_IMAGE_RE.sub("![](image)", text)
    # Compacta runs de linhas vazias resultantes da remoção.
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip() + "\n"


def convert_directory(
    input_dir: Path,
    output_dir: Path | None,
    force: bool,
) -> None:
    output_dir = output_dir or input_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    soffice = find_soffice()
    md_converter = MarkItDown()

    doc_files = sorted(input_dir.glob("*.doc"))
    if not doc_files:
        print(f"Nenhum .doc encontrado em {input_dir}")
        return

    print(f"Encontrados {len(doc_files)} .doc em {input_dir}")
    print(f"Saída: {output_dir}\n")

    converted = 0
    skipped = 0
    failed = 0

    with tempfile.TemporaryDirectory(prefix="doc2md-") as tmpdir:
        tmp_path = Path(tmpdir)
        for doc in doc_files:
            md_out = output_dir / f"{doc.stem}.md"
            if md_out.exists() and not force:
                print(f"  [skip] {doc.name} (já existe {md_out.name})")
                skipped += 1
                continue
            try:
                print(f"  [conv] {doc.name} ...", end=" ", flush=True)
                docx = doc_to_docx(doc, tmp_path, soffice)
                md_text = docx_to_md(docx, md_converter)
                md_out.write_text(md_text, encoding="utf-8")
                size_kb = md_out.stat().st_size / 1024
                print(f"OK ({size_kb:.1f} KB)")
                converted += 1
            except Exception as exc:  # noqa: BLE001
                print(f"FALHOU: {exc}")
                failed += 1

    print(
        f"\nResultado: {converted} convertido(s), "
        f"{skipped} pulado(s), {failed} falha(s)."
    )
    if failed:
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "input_dir",
        type=Path,
        help="Diretório com arquivos .doc para converter.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Diretório de saída (default: mesmo do input).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Sobrescreve .md existente.",
    )
    args = parser.parse_args()

    if not args.input_dir.is_dir():
        sys.exit(f"ERRO: {args.input_dir} não é diretório.")

    convert_directory(args.input_dir, args.output_dir, args.force)


if __name__ == "__main__":
    main()
