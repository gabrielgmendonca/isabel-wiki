#!/usr/bin/env python3
"""
Atualiza a seção "Status do projeto" em `index.md`.

Recalcula a linha `**Cobertura atual:** ...` a partir dos arquivos em `wiki/`:
- Pentateuco: slugs fixos (5 obras).
- Evangelhos canônicos: slugs fixos (4 obras).
- Fontes complementares: restante de `wiki/obras/`.
- Total de páginas: soma de todos os tipos em `wiki/`.

Rodar: `uv run python .claude/skills/ingest/scripts/update_status.py`
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3].parent
WIKI = ROOT / "wiki"
INDEX = ROOT / "index.md"

PENTATEUCO = {
    "livro-dos-espiritos",
    "livro-dos-mediuns",
    "evangelho-segundo-o-espiritismo",
    "ceu-e-inferno",
    "genese",
}

EVANGELHOS = {
    "evangelho-segundo-mateus",
    "evangelho-segundo-marcos",
    "evangelho-segundo-lucas",
    "evangelho-segundo-joao",
}

EVANGELHOS_LABEL = {
    "evangelho-segundo-mateus": "Mateus",
    "evangelho-segundo-marcos": "Marcos",
    "evangelho-segundo-lucas": "Lucas",
    "evangelho-segundo-joao": "João",
}

TIPOS = ["conceitos", "obras", "personalidades", "questoes", "aprofundamentos", "sinteses", "divergencias", "trilhas"]


def slugs(dirname: str) -> set[str]:
    d = WIKI / dirname
    if not d.exists():
        return set()
    return {p.stem for p in d.glob("*.md")}


def main() -> int:
    obras = slugs("obras")
    counts = {t: len(slugs(t)) for t in TIPOS}
    total = sum(counts.values())

    pent_presentes = obras & PENTATEUCO
    evang_presentes = obras & EVANGELHOS
    complementares = obras - PENTATEUCO - EVANGELHOS

    evang_lista = ", ".join(
        EVANGELHOS_LABEL[s] for s in EVANGELHOS_LABEL if s in evang_presentes
    )
    evang_trecho = (
        f" + Evangelhos canônicos ({evang_lista})" if evang_presentes else ""
    )

    nova = (
        f"**Cobertura atual:** Pentateuco "
        f"{'completo' if len(pent_presentes) == 5 else 'parcial'} "
        f"({len(pent_presentes)}/5 obras ingeridas){evang_trecho} "
        f"+ {len(complementares)} fontes complementares. "
        f"~{total} páginas entre conceitos, obras, personalidades, questões, aprofundamentos e sínteses."
    )

    texto = INDEX.read_text(encoding="utf-8")
    padrao = re.compile(r"^\*\*Cobertura atual:\*\*.*$", re.MULTILINE)
    if not padrao.search(texto):
        print("ERRO: linha '**Cobertura atual:**' não encontrada em index.md", flush=True)
        return 1

    novo_texto = padrao.sub(nova, texto, count=1)
    if novo_texto == texto:
        print("Sem mudanças.")
        return 0

    INDEX.write_text(novo_texto, encoding="utf-8")
    print("index.md atualizado:")
    print(f"  {nova}")
    print(
        f"  obras={len(obras)} (pentateuco={len(pent_presentes)}, "
        f"evangelhos={len(evang_presentes)}, complementares={len(complementares)}), "
        f"conceitos={counts['conceitos']}, personalidades={counts['personalidades']}, "
        f"questoes={counts['questoes']}, aprofundamentos={counts['aprofundamentos']}, sinteses={counts['sinteses']}, "
        f"divergencias={counts['divergencias']}, total={total}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
