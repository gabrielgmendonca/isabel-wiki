#!/usr/bin/env python3
"""Sugere e aplica tags lei/ ao frontmatter de páginas wiki.

Modo padrão (sem --apply): gera relatório de sugestões.
Com --apply: aplica as tags ao frontmatter.
"""

import re
import sys
from pathlib import Path

WIKI_DIR = Path("wiki")

# Mapeamento: slug da página → tag lei/
SLUG_TO_LEI = {
    "lei-de-adoracao": "lei/adoracao",
    "lei-do-trabalho": "lei/trabalho",
    "lei-de-reproducao": "lei/reproducao",
    "lei-de-conservacao": "lei/conservacao",
    "lei-de-destruicao": "lei/destruicao",
    "lei-de-sociedade": "lei/sociedade",
    "lei-do-progresso": "lei/progresso",
    "lei-de-igualdade": "lei/igualdade",
    "lei-de-liberdade": "lei/liberdade",
    "lei-de-justica-amor-e-caridade": "lei/justica-amor-caridade",
}

# Faixas de questões LE para cada lei moral
LEI_RANGES = {
    "lei/adoracao": (649, 673),
    "lei/trabalho": (674, 685),
    "lei/reproducao": (686, 701),
    "lei/conservacao": (702, 727),
    "lei/destruicao": (728, 765),
    "lei/sociedade": (766, 775),
    "lei/progresso": (776, 800),
    "lei/igualdade": (803, 824),
    "lei/liberdade": (825, 872),
    "lei/justica-amor-caridade": (873, 919),
}

# Termos-chave associados a cada lei (para matching por conteúdo)
LEI_KEYWORDS = {
    "lei/adoracao": ["adoração", "adorar a deus", "culto exterior", "contemplação", "vida contemplativa"],
    "lei/trabalho": ["lei do trabalho", "necessidade do trabalho", "limite do trabalho", "ociosidade"],
    "lei/reproducao": ["reprodução", "celibato", "casamento", "virgindade", "obstáculos à reprodução"],
    "lei/conservacao": ["conservação", "instinto de conservação", "gozo dos bens terrenos", "necessário e supérfluo", "privações voluntárias"],
    "lei/destruicao": ["destruição", "flagelos destrutores", "guerras", "assassínio", "crueldade", "duelo", "pena de morte", "suicídio"],
    "lei/sociedade": ["lei de sociedade", "vida social", "vida de insulamento", "laço de família"],
    "lei/progresso": ["lei do progresso", "estado de natureza", "marcha do progresso", "progresso da legislação", "influência do espiritismo"],
    "lei/igualdade": ["lei de igualdade", "igualdade natural", "desigualdade das aptidões", "desigualdades sociais", "igualdade de direitos", "igualdade perante a morte"],
    "lei/liberdade": ["lei de liberdade", "liberdade natural", "escravidão", "liberdade de pensar", "liberdade de consciência", "livre-arbítrio", "fatalismo", "fatalidade"],
    "lei/justica-amor-caridade": ["lei de justiça", "justiça natural", "direito de propriedade", "lei de amor", "lei de caridade", "amor ao próximo", "benevolência"],
}

TAGS_RE = re.compile(r"^(tags:\s*\[)(.*?)(\]\s*)$")
# Match questões LE no formato: q. 123, q.123, questão 123, questões 123
Q_RE = re.compile(r"(?:q\.\s*|questão\s+|questões\s+)(\d+)", re.IGNORECASE)


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
                return [t.strip() for t in m.group(2).split(",") if t.strip()]
    return []


def find_lei_by_slug(path: Path) -> list[str]:
    slug = path.stem
    tag = SLUG_TO_LEI.get(slug)
    return [tag] if tag else []


def find_lei_by_questions(text: str) -> list[str]:
    matches = Q_RE.findall(text)
    if not matches:
        return []
    questions = {int(q) for q in matches}
    found = set()
    for lei, (lo, hi) in LEI_RANGES.items():
        if any(lo <= q <= hi for q in questions):
            found.add(lei)
    return sorted(found)


def find_lei_by_keywords(text: str) -> list[str]:
    text_lower = text.lower()
    found = set()
    for lei, keywords in LEI_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                found.add(lei)
                break
    return sorted(found)


def find_lei_by_wikilinks(text: str) -> list[str]:
    """Encontra tags lei/ baseado em wikilinks para páginas de leis morais."""
    found = set()
    for slug, tag in SLUG_TO_LEI.items():
        if f"[[wiki/conceitos/{slug}]]" in text or f"[[wiki/conceitos/{slug}|" in text:
            found.add(tag)
    return sorted(found)


def suggest_tags(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
    existing = set(extract_tags(lines))

    slug = path.stem
    candidates = set()

    # Para páginas lei-de-*, aplicar APENAS a tag do próprio slug
    # (evita ruído de cross-references para leis vizinhas)
    slug_tags = find_lei_by_slug(path)
    if slug_tags:
        candidates.update(slug_tags)
    else:
        # Para demais páginas, usar todas as heurísticas
        candidates.update(find_lei_by_questions(text))
        candidates.update(find_lei_by_wikilinks(text))

    # Remover já existentes
    new_tags = sorted(candidates - existing)
    return new_tags


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
    do_apply = "--apply" in sys.argv

    suggestions: list[tuple[Path, list[str]]] = []
    for path in sorted(WIKI_DIR.rglob("*.md")):
        new_tags = suggest_tags(path)
        if new_tags:
            suggestions.append((path, new_tags))

    if not suggestions:
        print("Nenhuma sugestão de tag lei/ encontrada.")
        return

    if do_apply:
        modified = 0
        for path, tags in suggestions:
            if apply_tags(path, tags):
                modified += 1
                print(f"  + {path}: {', '.join(tags)}")
        print(f"\nModificados: {modified}")
    else:
        print(f"## Sugestões de tags lei/ ({len(suggestions)} páginas)\n")
        print(f"| Página | Tags sugeridas | Método |")
        print(f"|--------|---------------|--------|")
        for path, tags in suggestions:
            # Determinar método
            methods = []
            if find_lei_by_slug(path):
                methods.append("slug")
            text = path.read_text(encoding="utf-8")
            if find_lei_by_questions(text):
                methods.append("questões LE")
            if find_lei_by_wikilinks(text):
                methods.append("wikilinks")
            print(f"| `{path}` | {', '.join(tags)} | {', '.join(methods)} |")
        print(f"\nPara aplicar: `uv run python scripts/enrich_tags_lei.py --apply`")


if __name__ == "__main__":
    main()
