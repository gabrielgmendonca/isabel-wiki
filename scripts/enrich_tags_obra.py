#!/usr/bin/env python3
"""Adiciona tags obra/ ao frontmatter de cada página wiki, derivadas do campo fontes."""

import re
from pathlib import Path

WIKI_DIR = Path("wiki")

FONTES_TO_OBRA = {
    "LE": "obra/le",
    "LM": "obra/lm",
    "ESE": "obra/ese",
    "C&I": "obra/ci",
    "Gênese": "obra/genese",
    "OPE": "obra/ope",
    "OQE": "obra/oqe",
    "RE": "obra/re",
}

TAGS_RE = re.compile(r"^(tags:\s*\[)(.*?)(\]\s*)$")
FONTES_RE = re.compile(r"^fontes:\s*\[(.*?)\]\s*$")


def extract_fontes(lines: list[str]) -> list[str]:
    in_fm = False
    for line in lines:
        if line.strip() == "---":
            if in_fm:
                break
            in_fm = True
            continue
        if in_fm:
            m = FONTES_RE.match(line)
            if m:
                return [f.strip() for f in m.group(1).split(",") if f.strip()]
    return []


def process_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")

    fontes = extract_fontes(lines)
    new_tags = []
    for f in fontes:
        tag = FONTES_TO_OBRA.get(f)
        if tag:
            new_tags.append(tag)

    if not new_tags:
        return False

    in_fm = False
    for i, line in enumerate(lines):
        if line.strip() == "---":
            if in_fm:
                break
            in_fm = True
            continue
        if in_fm:
            m = TAGS_RE.match(line)
            if m:
                existing = [t.strip() for t in m.group(2).split(",") if t.strip()]
                to_add = [t for t in new_tags if t not in existing]
                if not to_add:
                    return False
                all_tags = existing + to_add
                lines[i] = f"tags: [{', '.join(all_tags)}]"
                path.write_text("\n".join(lines), encoding="utf-8")
                return True
    return False


def main():
    modified = 0
    skipped = 0
    for path in sorted(WIKI_DIR.rglob("*.md")):
        if process_file(path):
            modified += 1
            print(f"  + {path}")
        else:
            skipped += 1
    print(f"\nModificados: {modified} | Sem mudança: {skipped}")


if __name__ == "__main__":
    main()
