#!/usr/bin/env python3
"""Compila um livro do books_with_links.json em uma página Markdown em raw/mediuns/."""

import argparse
import difflib
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).parent
JSON_PATH = ROOT / "books_with_links.json"
OUTPUT_DIR = ROOT / "raw" / "mediuns"


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


_SUFFIX_NAMES = re.compile(
    r"(?i)^(conclus|ep[ií]logo|posf[aá]cio|nota.?final|agradecimento|ap[eê]ndice)"
)


def sort_chapters(indexed_chapters: list[tuple[int, dict]]) -> list[dict]:
    """Ordena: prefácios, numerados por número, posfácios."""
    numbered = []
    prefix = []
    suffix = []
    for orig_idx, ch in indexed_chapters:
        num_match = re.search(r"\d+", ch.get("chapter_number", ""))
        if num_match:
            numbered.append((int(num_match.group()), orig_idx, ch))
        elif _SUFFIX_NAMES.search(ch.get("chapter_name", "")):
            suffix.append((orig_idx, ch))
        else:
            prefix.append((orig_idx, ch))

    numbered.sort(key=lambda x: x[0])
    prefix.sort(key=lambda x: x[0])
    suffix.sort(key=lambda x: x[0])

    return (
        [ch for _, ch in prefix]
        + [ch for _, _, ch in numbered]
        + [ch for _, ch in suffix]
    )


def build_markdown(chapters: list[dict]) -> str:
    first = chapters[0]
    lines = [
        f"# {first['book_title']}",
        "",
        f"**Autor espiritual:** {first['book_author']}  ",
        f"**Médium:** {first['book_medium']}  ",
    ]
    if first.get("chapter_url"):
        lines.append(f"**Fonte:** {first['chapter_url']}")
    lines.append("")

    for ch in chapters:
        lines.append("---")
        lines.append("")
        header = f"## {ch['chapter_number']}"
        if ch.get("chapter_name"):
            header += f" — {ch['chapter_name']}"
        lines.append(header)
        lines.append("")

        if ch.get("chapter_epigraph_text"):
            for epigraph_line in ch["chapter_epigraph_text"].splitlines():
                lines.append(f"> {epigraph_line}")
            attribution = ""
            if ch.get("chapter_epigraph_author"):
                attribution = ch["chapter_epigraph_author"]
            if ch.get("chapter_epigraph_ref"):
                attribution += f", {ch['chapter_epigraph_ref']}" if attribution else ch["chapter_epigraph_ref"]
            if attribution:
                lines.append(f"> — {attribution}")
            lines.append("")

        lines.append(ch.get("chapter_text", ""))
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Compila livro do JSON em Markdown.")
    parser.add_argument("title", help="Título do livro (book_title)")
    args = parser.parse_args()

    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))

    title_map: dict[str, str] = {}
    for entry in data:
        t = entry.get("book_title", "")
        if t:
            title_map[t.lower()] = t

    key = args.title.lower()
    if key not in title_map:
        suggestions = difflib.get_close_matches(key, title_map.keys(), n=5, cutoff=0.4)
        print(f"Livro não encontrado: \"{args.title}\"")
        if suggestions:
            print("Você quis dizer:")
            for s in suggestions:
                print(f"  - {title_map[s]}")
        raise SystemExit(1)

    canonical_title = title_map[key]
    indexed = [
        (i, e) for i, e in enumerate(data) if e.get("book_title") == canonical_title
    ]
    chapters = sort_chapters(indexed)

    md = build_markdown(chapters)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / f"{slugify(canonical_title)}.md"
    out_path.write_text(md, encoding="utf-8")
    print(f"Criado: {out_path}")


if __name__ == "__main__":
    main()
