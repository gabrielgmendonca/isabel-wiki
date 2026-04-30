#!/usr/bin/env python3
"""Adiciona tag grau/* ao frontmatter das páginas wiki por default heurístico.

Mapeamento por `tipo:` documentado em .claude/rules/convencoes-paginas.md
(seção Taxonomia de tags / `grau/`):

    questao        → grau/introdutorio
    parabola       → grau/intermediario
    personalidade  → grau/intermediario
    conceito       → grau/intermediario
    aprofundamento → grau/avancado
    sintese        → grau/avancado
    divergencia    → grau/avancado
    obra, trilha   → não recebem grau/*

Skip se a página já tiver qualquer tag grau/*. Não tenta refinar sub-categorias
(ex.: "questão sobre tema avançado" continua introdutorio); promoção é manual.

Uso:
    uv run python scripts/enrich_tags_grau.py --dry-run
    uv run python scripts/enrich_tags_grau.py
"""

import re
import sys
from pathlib import Path

WIKI_DIR = Path("wiki")

TIPO_TO_GRAU: dict[str, str] = {
    "questao": "grau/introdutorio",
    "parabola": "grau/intermediario",
    "personalidade": "grau/intermediario",
    "conceito": "grau/intermediario",
    "aprofundamento": "grau/avancado",
    "sintese": "grau/avancado",
    "divergencia": "grau/avancado",
}

TAGS_RE = re.compile(r"^(tags:\s*\[)(.*?)(\]\s*)$")
TIPO_RE = re.compile(r"^tipo:\s*(.+?)\s*$")


def _split_csv(value: str) -> list[str]:
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


def extract_tipo_and_tags(lines: list[str]) -> tuple[str, list[str]]:
    in_fm = False
    tipo = ""
    tags: list[str] = []
    for line in lines:
        if line.strip() == "---":
            if in_fm:
                break
            in_fm = True
            continue
        if in_fm:
            m_tipo = TIPO_RE.match(line)
            if m_tipo:
                tipo = m_tipo.group(1).strip()
                continue
            m_tags = TAGS_RE.match(line)
            if m_tags:
                tags = _split_csv(m_tags.group(2))
    return tipo, tags


def is_meta_sintese(tipo: str, tags: list[str]) -> bool:
    """Meta-páginas de síntese (estatísticas, catálogo) não recebem grau/*."""
    return tipo == "sintese" and "meta" in tags


def is_trilha(path: Path, tags: list[str]) -> bool:
    """Trilhas (estruturais) não recebem grau/* — a trilha agrupa páginas de vários graus."""
    return "wiki/trilhas/" in str(path) or "trilha" in tags


def apply_tag(path: Path, new_tag: str) -> bool:
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
                if new_tag in existing:
                    return False
                all_tags = existing + [new_tag]
                lines[i] = f"tags: [{', '.join(all_tags)}]"
                path.write_text("\n".join(lines), encoding="utf-8")
                return True
    return False


def main() -> None:
    dry_run = "--dry-run" in sys.argv

    plans: list[tuple[Path, str]] = []
    skipped_tipo: dict[str, int] = {}
    for path in sorted(WIKI_DIR.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        lines = text.split("\n")
        tipo, tags = extract_tipo_and_tags(lines)

        if any(t.startswith("grau/") for t in tags):
            continue
        if is_meta_sintese(tipo, tags) or is_trilha(path, tags):
            continue

        grau = TIPO_TO_GRAU.get(tipo)
        if not grau:
            skipped_tipo[tipo or "(vazio)"] = skipped_tipo.get(tipo or "(vazio)", 0) + 1
            continue
        plans.append((path, grau))

    if not plans:
        print("Nenhuma tag grau/ a adicionar.")
        return

    if dry_run:
        print(f"## Sugestões de tags grau/ ({len(plans)} páginas)\n")
        by_grau: dict[str, int] = {}
        for path, grau in plans:
            print(f"  {path}: {grau}")
            by_grau[grau] = by_grau.get(grau, 0) + 1
        print(f"\nResumo: {by_grau}")
        if skipped_tipo:
            print(f"Tipos sem mapeamento (skip): {skipped_tipo}")
        print(f"\nPara aplicar: uv run python scripts/enrich_tags_grau.py")
        return

    modified = 0
    for path, grau in plans:
        if apply_tag(path, grau):
            modified += 1
    print(f"Modificados: {modified} | Sem mudança: {len(plans) - modified}")
    if skipped_tipo:
        print(f"Tipos sem mapeamento (skip): {skipped_tipo}")


if __name__ == "__main__":
    main()
