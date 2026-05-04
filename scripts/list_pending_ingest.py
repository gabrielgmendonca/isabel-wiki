#!/usr/bin/env python3
"""Lista obras em raw/ que ainda não têm página correspondente em wiki/obras/.

Estratégia: compara slugs (basename sem .md) entre raw/{autores,mediuns} e
wiki/obras/. Heurística simples — não cobre obras renomeadas/fundidas, mas
serve de ponto de partida.

Exclui:
- raw/biblia-acf/ (corpus bíblico, ingerido por outro fluxo)
- raw/assets/, raw/artigos/, raw/palestras/ (não viram página em wiki/obras/)
- raw/kardec/ (já tem estrutura própria; tratado à parte se necessário)
- arquivos auxiliares (.index.md, .resumo.md, README.md, .gitkeep)
"""

from pathlib import Path
import re
import sys
import unicodedata

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"
OBRAS = ROOT / "wiki" / "obras"

INCLUDE_DIRS = ["autores", "mediuns"]
SKIP_SUFFIXES = (".index.md", ".resumo.md")
SKIP_NAMES = {"README.md", ".gitkeep"}

STOPWORDS = {"de", "da", "do", "das", "dos", "e", "o", "a", "as", "os", "para", "min"}


def normalize(slug: str) -> str:
    s = unicodedata.normalize("NFKD", slug).encode("ascii", "ignore").decode("ascii")
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    tokens = [t for t in s.split("-") if t and t not in STOPWORDS]
    return "-".join(tokens)


def tokenset(slug: str) -> set:
    return set(t for t in normalize(slug).split("-") if len(t) > 2)


def collect_raw():
    out = {}
    for sub in INCLUDE_DIRS:
        base = RAW / sub
        if not base.exists():
            continue
        for p in base.rglob("*.md"):
            name = p.name
            if name in SKIP_NAMES or name.endswith(SKIP_SUFFIXES):
                continue
            slug = p.stem
            out.setdefault(slug, []).append(p.relative_to(ROOT))
    return out


def collect_obras():
    return [p.stem for p in OBRAS.glob("*.md")]


def match(raw_slug: str, obras_norm: dict) -> str | None:
    """Tenta achar uma obra existente que cubra o slug do raw.

    1. Igualdade após normalização.
    2. Slug normalizado do raw contém o da obra (ou vice-versa).
    3. Interseção forte de tokens (>= 3 tokens em comum, e cobre >= 60% do menor).
    """
    n = normalize(raw_slug)
    if n in obras_norm:
        return obras_norm[n]

    raw_tokens = tokenset(raw_slug)
    if not raw_tokens:
        return None

    best = None
    for o_norm, o_orig in obras_norm.items():
        if n and (n in o_norm or o_norm in n):
            return o_orig
        o_tokens = set(t for t in o_norm.split("-") if len(t) > 2)
        if not o_tokens:
            continue
        common = raw_tokens & o_tokens
        smaller = min(len(raw_tokens), len(o_tokens))
        if len(common) >= 3 and len(common) / smaller >= 0.6:
            best = o_orig
    return best


def main():
    raw_map = collect_raw()
    obras = collect_obras()
    obras_norm = {normalize(o): o for o in obras}

    pending = []
    matched = []
    for slug, paths in raw_map.items():
        m = match(slug, obras_norm)
        if m:
            matched.append((slug, m, paths))
        else:
            pending.append((slug, paths))

    by_author = {}
    for slug, paths in pending:
        for p in paths:
            author = p.parts[2] if len(p.parts) > 2 else "?"
            by_author.setdefault(author, []).append((slug, p))

    print(f"raw/ obras únicas (autores+mediuns): {len(raw_map)}")
    print(f"wiki/obras/ páginas: {len(obras)}")
    print(f"Já cobertas (match heurístico): {len(matched)}")
    print(f"Pendentes de ingestão: {len(pending)}")
    print()

    print("# Pendentes")
    for author in sorted(by_author):
        items = sorted(by_author[author])
        print(f"\n## {author} ({len(items)})")
        for slug, path in items:
            print(f"- {slug}  ←  {path}")

    if "--show-matched" in sys.argv:
        print("\n# Já cobertas (revisar se o match está correto)")
        for slug, obra, _paths in sorted(matched):
            print(f"- raw `{slug}` → wiki/obras/{obra}.md")

    return 0 if not pending else 1


if __name__ == "__main__":
    sys.exit(main())
