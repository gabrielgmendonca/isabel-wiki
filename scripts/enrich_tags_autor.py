#!/usr/bin/env python3
"""Adiciona tags autor/ ao frontmatter de cada página wiki.

Deriva de duas fontes:
  1. Campo `fontes:` (LE/LM/ESE/... → autor/kardec; "Léon Denis" → autor/leon-denis;
     "Emmanuel/Chico Xavier" → autor/emmanuel + autor/chico-xavier; etc.).
  2. Tags livres canônicas já em uso (`paulo`, `andre-luiz`, `chico-xavier` etc.)
     promovidas para `autor/<slug>` correspondente.

Uso:
    uv run python scripts/enrich_tags_autor.py --dry-run
    uv run python scripts/enrich_tags_autor.py
"""

import re
import sys
from pathlib import Path

WIKI_DIR = Path("wiki")

# Fontes canônicas → autor/* (uma ou mais)
FONTE_TO_AUTORES: dict[str, tuple[str, ...]] = {
    # Pentateuco e complementares Kardec
    "LE": ("autor/kardec",),
    "LM": ("autor/kardec",),
    "ESE": ("autor/kardec",),
    "C&I": ("autor/kardec",),
    "Gênese": ("autor/kardec",),
    "OPE": ("autor/kardec",),
    "OQE": ("autor/kardec",),
    "RE": ("autor/kardec",),
    # Léon Denis (autor encarnado)
    "Léon Denis": ("autor/leon-denis",),
    # Cairbar Schutel
    "Cairbar Schutel": ("autor/cairbar-schutel",),
    # Psicografias canônicas — espírito + médium
    "Emmanuel/Chico Xavier": ("autor/emmanuel", "autor/chico-xavier"),
    "André Luiz/Chico Xavier": ("autor/andre-luiz", "autor/chico-xavier"),
    "Humberto de Campos/Chico Xavier": ("autor/humberto-de-campos", "autor/chico-xavier"),
    "Joanna de Ângelis/Divaldo Franco": ("autor/joanna-de-angelis", "autor/divaldo-franco"),
    "Bezerra de Menezes/Divaldo Franco": ("autor/bezerra-de-menezes", "autor/divaldo-franco"),
    "Hammed/Francisco do Espírito Santo Neto": ("autor/hammed",),
}

# Tags livres canônicas → autor/* (promoção)
FREE_TAG_TO_AUTOR: dict[str, str] = {
    "kardec": "autor/kardec",
    "leon-denis": "autor/leon-denis",
    "chico-xavier": "autor/chico-xavier",
    "emmanuel": "autor/emmanuel",
    "andre-luiz": "autor/andre-luiz",
    "humberto-de-campos": "autor/humberto-de-campos",
    "joanna-de-angelis": "autor/joanna-de-angelis",
    "divaldo": "autor/divaldo-franco",
    "divaldo-franco": "autor/divaldo-franco",
    "bezerra-de-menezes": "autor/bezerra-de-menezes",
    "cairbar": "autor/cairbar-schutel",
    "cairbar-schutel": "autor/cairbar-schutel",
    "hammed": "autor/hammed",
    "paulo": "autor/paulo",
    "joao": "autor/joao",
    "pedro": "autor/pedro",
    "tiago": "autor/tiago",
}

TAGS_RE = re.compile(r"^(tags:\s*\[)(.*?)(\]\s*)$")
FONTES_RE = re.compile(r"^fontes:\s*\[(.*?)\]\s*$")


def _split_csv(value: str) -> list[str]:
    """Divide lista CSV de YAML inline, removendo aspas opcionais e espaços."""
    out: list[str] = []
    for raw in value.split(","):
        item = raw.strip()
        if (item.startswith('"') and item.endswith('"')) or (
            item.startswith("'") and item.endswith("'")
        ):
            item = item[1:-1]
        if item:
            out.append(item)
    return out


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
                return _split_csv(m.group(1))
    return []


def extract_tags(lines: list[str]) -> list[str]:
    in_fm = False
    for line in lines:
        if line.strip() == "---":
            if in_fm:
                break
            in_fm = True
            continue
        if in_fm:
            m = TAGS_RE.match(line)
            if m:
                return _split_csv(m.group(2))
    return []


def derive_autor_tags(fontes: list[str], tags: list[str]) -> list[str]:
    """Retorna a lista ordenada de tags autor/* derivadas, sem duplicar com as existentes."""
    derived: set[str] = set()
    for f in fontes:
        for autor in FONTE_TO_AUTORES.get(f, ()):
            derived.add(autor)
    for t in tags:
        if t in FREE_TAG_TO_AUTOR:
            derived.add(FREE_TAG_TO_AUTOR[t])
    existing = {t for t in tags if t.startswith("autor/")}
    return sorted(derived - existing)


def apply_tags(path: Path, new_tags: list[str]) -> bool:
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
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
                existing = _split_csv(m.group(2))
                to_add = [t for t in new_tags if t not in existing]
                if not to_add:
                    return False
                all_tags = existing + to_add
                lines[i] = f"tags: [{', '.join(all_tags)}]"
                path.write_text("\n".join(lines), encoding="utf-8")
                return True
    return False


def main() -> None:
    dry_run = "--dry-run" in sys.argv

    plans: list[tuple[Path, list[str]]] = []
    for path in sorted(WIKI_DIR.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        lines = text.split("\n")
        fontes = extract_fontes(lines)
        tags = extract_tags(lines)
        new_tags = derive_autor_tags(fontes, tags)
        if new_tags:
            plans.append((path, new_tags))

    if not plans:
        print("Nenhuma tag autor/ a adicionar.")
        return

    if dry_run:
        print(f"## Sugestões de tags autor/ ({len(plans)} páginas)\n")
        for path, tags in plans:
            print(f"  {path}: {', '.join(tags)}")
        print(f"\nPara aplicar: uv run python scripts/enrich_tags_autor.py")
        return

    modified = 0
    for path, tags in plans:
        if apply_tags(path, tags):
            modified += 1
            print(f"  + {path}: {', '.join(tags)}")
    print(f"\nModificados: {modified} | Sem mudança: {len(plans) - modified}")


if __name__ == "__main__":
    main()
