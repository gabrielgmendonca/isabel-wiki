#!/usr/bin/env python3
"""Compila todos os livros do books_with_links.json, pulando os que já existem em raw/.

Reaproveita slugify/sort_chapters/build_markdown de compile_book.py para garantir
path idêntico ao do compilador individual. Não regenera obra já presente em raw/:
pula se o arquivo-alvo existe ou se o mesmo slug já existe em qualquer subpasta de raw/.
"""

import argparse
import json
from pathlib import Path

from compile_book import (
    OUTPUT_DIR,
    ROOT,
    build_markdown,
    slugify,
    sort_chapters,
)

RAW_DIR = ROOT / "raw"


def resolve_json_path() -> Path:
    """books_with_links.json pode estar na raiz do worktree ou do repo
    principal (worktree → ../../.. ). Procura subindo a partir de ROOT."""
    for base in (ROOT, *ROOT.parents):
        candidate = base / "books_with_links.json"
        if candidate.is_file():
            return candidate
    raise SystemExit("books_with_links.json não encontrado a partir de " + str(ROOT))


def existing_raw_slugs() -> set[str]:
    """Slugs (stem do arquivo) de todo .md sob raw/, para evitar duplicar obra
    que já vive em outra subpasta (raw/kardec, raw/autores, ...)."""
    return {p.stem for p in RAW_DIR.rglob("*.md")}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Mostra o que seria criado/pulado sem escrever nada.",
    )
    args = parser.parse_args()

    data = json.loads(resolve_json_path().read_text(encoding="utf-8"))

    # Agrupa por título exato preservando a ordem de aparição (como compile_book.main).
    by_title: dict[str, list[tuple[int, dict]]] = {}
    for i, entry in enumerate(data):
        title = entry.get("book_title", "")
        if title:
            by_title.setdefault(title, []).append((i, entry))

    raw_slugs = existing_raw_slugs()

    created = skipped_target = skipped_elsewhere = 0
    for title, indexed in sorted(by_title.items()):
        chapters = sort_chapters(indexed)
        medium = chapters[0].get("book_medium", "")
        out_dir = OUTPUT_DIR / slugify(medium) if medium else OUTPUT_DIR
        slug = slugify(title)
        out_path = out_dir / f"{slug}.md"

        if out_path.exists():
            skipped_target += 1
            continue
        if slug in raw_slugs:
            print(f"Pulado (já existe em raw/ com slug '{slug}'): {title}")
            skipped_elsewhere += 1
            continue

        rel = out_path.relative_to(ROOT)
        if args.dry_run:
            print(f"[dry-run] Criaria: {rel}")
        else:
            md = build_markdown(chapters)
            out_dir.mkdir(parents=True, exist_ok=True)
            out_path.write_text(md, encoding="utf-8")
            raw_slugs.add(slug)
            print(f"Criado: {rel}")
        created += 1

    verbo = "Criaria" if args.dry_run else "Criado(s)"
    print(
        f"\n{verbo}: {created} | "
        f"já no destino: {skipped_target} | "
        f"já em raw/ (outra pasta): {skipped_elsewhere} | "
        f"total de livros: {len(by_title)}"
    )


if __name__ == "__main__":
    main()
