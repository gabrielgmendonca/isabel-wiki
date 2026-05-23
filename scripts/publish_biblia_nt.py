#!/usr/bin/env python3
"""Publica os 27 livros do NT de raw/biblia-acf/ em wiki/biblia/.

Cada capítulo vira `wiki/biblia/<slug>/<N>.md` (tipo: capitulo-biblico) com
versículo em H2 (`## N`) para anchor estável `#N`. Cada livro recebe
`wiki/biblia/<slug>/index.md` (tipo: livro-biblico) com lista de capítulos e
cross-link para a página-âncora em `wiki/obras/`.

Idempotente: re-rodar sobrescreve. Não toca em raw/ nem em wiki/obras/.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw" / "biblia-acf"
WIKI_BIBLIA = ROOT / "wiki" / "biblia"

TODAY = "2026-05-22"

# (slug em raw/biblia-acf/, Nome canônico PT-BR, slug em wiki/obras/)
NT_BOOKS: list[tuple[str, str, str]] = [
    ("mateus", "Mateus", "evangelho-segundo-mateus"),
    ("marcos", "Marcos", "evangelho-segundo-marcos"),
    ("lucas", "Lucas", "evangelho-segundo-lucas"),
    ("joao", "João", "evangelho-segundo-joao"),
    ("atos", "Atos", "atos-dos-apostolos"),
    ("romanos", "Romanos", "epistola-aos-romanos"),
    ("1-corintios", "1 Coríntios", "primeira-epistola-aos-corintios"),
    ("2-corintios", "2 Coríntios", "segunda-epistola-aos-corintios"),
    ("galatas", "Gálatas", "epistola-aos-galatas"),
    ("efesios", "Efésios", "epistola-aos-efesios"),
    ("filipenses", "Filipenses", "epistola-aos-filipenses"),
    ("colossenses", "Colossenses", "epistola-aos-colossenses"),
    ("1-tessalonicenses", "1 Tessalonicenses", "primeira-epistola-aos-tessalonicenses"),
    ("2-tessalonicenses", "2 Tessalonicenses", "segunda-epistola-aos-tessalonicenses"),
    ("1-timoteo", "1 Timóteo", "primeira-epistola-a-timoteo"),
    ("2-timoteo", "2 Timóteo", "segunda-epistola-a-timoteo"),
    ("tito", "Tito", "epistola-a-tito"),
    ("filemom", "Filemom", "epistola-a-filemom"),
    ("hebreus", "Hebreus", "epistola-aos-hebreus"),
    ("tiago", "Tiago", "epistola-de-tiago"),
    ("1-pedro", "1 Pedro", "primeira-epistola-de-pedro"),
    ("2-pedro", "2 Pedro", "segunda-epistola-de-pedro"),
    ("1-joao", "1 João", "primeira-epistola-de-joao"),
    ("2-joao", "2 João", "segunda-epistola-de-joao"),
    ("3-joao", "3 João", "terceira-epistola-de-joao"),
    ("judas", "Judas", "epistola-de-judas"),
    ("apocalipse", "Apocalipse", "apocalipse"),
]

FM_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
VERSE_RE = re.compile(r"^\*\*(\d+)\.\*\*\s+(.*)$", re.MULTILINE)
H1_RE = re.compile(r"\A\s*# [^\n]+\n+")


def parse_raw_chapter(path: Path) -> tuple[dict[str, str], str]:
    """Retorna (frontmatter dict, corpo sem frontmatter)."""
    text = path.read_text(encoding="utf-8")
    m = FM_RE.match(text)
    if not m:
        return {}, text
    fm: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm, text[m.end():]


def convert_body(body: str) -> str:
    """Remove H1 do corpo (`# Livro N`) e troca cada `**N.** texto` por `## N\\n\\ntexto`."""
    body = H1_RE.sub("", body, count=1)
    body = VERSE_RE.sub(r"## \1\n\n\2", body)
    return body.strip() + "\n"


def write_chapter(raw_slug: str, book_name: str, chap_num: int, body: str) -> Path:
    out = WIKI_BIBLIA / raw_slug / f"{chap_num}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    fm = (
        "---\n"
        "tipo: capitulo-biblico\n"
        f"livro: {book_name}\n"
        f"capitulo: {chap_num}\n"
        "testamento: NT\n"
        "fontes: [NT]\n"
        "tags: []\n"
        f"atualizado_em: {TODAY}\n"
        "status: ativo\n"
        "---\n\n"
    )
    h1 = f"# {book_name} {chap_num}\n\n"
    out.write_text(fm + h1 + body, encoding="utf-8")
    return out


def write_book_index(
    raw_slug: str,
    book_name: str,
    chaps: list[int],
    obra_slug: str,
) -> Path:
    out = WIKI_BIBLIA / raw_slug / "index.md"
    fm = (
        "---\n"
        "tipo: livro-biblico\n"
        f"livro: {book_name}\n"
        "testamento: NT\n"
        "fontes: [NT]\n"
        "tags: []\n"
        f"atualizado_em: {TODAY}\n"
        "status: ativo\n"
        "---\n\n"
    )
    lines = [
        f"# {book_name}",
        "",
        f"Texto integral de **{book_name}** na tradução Almeida Corrigida e Fiel (ACF), em domínio público.",
        "",
        f"Análise temática e leitura kardequiana em [[wiki/obras/{obra_slug}]].",
        "",
        "## Capítulos",
        "",
        ", ".join(f"[[wiki/biblia/{raw_slug}/{c}|{c}]]" for c in chaps),
        "",
    ]
    out.write_text(fm + "\n".join(lines), encoding="utf-8")
    return out


def list_chapters(raw_slug: str) -> list[int]:
    book_dir = RAW / raw_slug
    return sorted(int(p.stem) for p in book_dir.glob("*.md") if p.stem.isdigit())


def main() -> int:
    if not RAW.exists():
        print(f"ERRO: {RAW} não existe", file=sys.stderr)
        return 1

    total_chaps = 0
    for raw_slug, book_name, obra_slug in NT_BOOKS:
        chaps = list_chapters(raw_slug)
        if not chaps:
            print(f"AVISO: nenhum capítulo em raw/biblia-acf/{raw_slug}/", file=sys.stderr)
            continue
        for n in chaps:
            raw_path = RAW / raw_slug / f"{n}.md"
            _, body = parse_raw_chapter(raw_path)
            write_chapter(raw_slug, book_name, n, convert_body(body))
            total_chaps += 1
        write_book_index(raw_slug, book_name, chaps, obra_slug)
        print(f"  {book_name}: {len(chaps)} capítulos + index")

    print(f"\nTotal: {total_chaps} capítulos + {len(NT_BOOKS)} índices em {WIKI_BIBLIA.relative_to(ROOT)}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
