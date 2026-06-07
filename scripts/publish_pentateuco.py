#!/usr/bin/env python3
"""Publica uma cópia derivada do Pentateuco em wiki/pentateuco/ com headings
granulares por questão/item, para habilitar link interno preferencial (§4 do
ROADMAP, "Fase 2 do híbrido").

Espelha a arquitetura de `publish_biblia_nt.py`: NÃO edita os `.md` de
`raw/kardec/pentateuco/` — só os LÊ. Cada capítulo de cada obra vira
`wiki/pentateuco/<obra>/<arquivo>.md` (tipo: capitulo-pentateuco), com o texto
do capítulo VERBATIM e uma âncora `## q. N` (LE) ou `## item N` (demais)
injetada antes de cada questão/item. Cada obra recebe um `index.md`
(tipo: obra-pentateuco) com a lista de capítulos e cross-link para
`wiki/obras/<slug>`.

Garantias (é o ponto da Fase 2 — não perder informação nem alterar o Kardec):

1. **`raw/` intocado** — o script nunca abre `raw/` para escrita. O guard de CI
   (`git diff --quiet raw/`) prova isso deterministicamente.
2. **Texto fiel por construção** — o corpo publicado é o slice de linhas do raw,
   inalterado; as únicas linhas novas são os headings de âncora (`## q. N` /
   `## item N`) e o frontmatter/H1. Nenhuma linha do Kardec é modificada.
3. **Round-trip vs cite.py** — cada âncora candidata só entra no manifest se o
   bloco sob ela for byte-a-byte igual ao que `cite.py:literal_text` extrai do
   raw (a mesma verdade-fonte que o `/critica` usa). Loci onde o `cite.py` não
   resolve limpo (C&I 2ª parte nominal, ESE cap. XXVIII coletânea de preces)
   simplesmente não recebem âncora — a citação cai no link externo (Kardecpedia),
   cobertura idêntica à de hoje, zero regressão.

Saída adicional: `data/pentateuco-anchors.json` — mapa (sigla → questão/item →
caminho#âncora) consumido por `link_citations.py` para preferir o link interno.

Idempotente: re-rodar reconstrói o derivado a partir do raw.

Uso:
    uv run python scripts/publish_pentateuco.py            # gera + verifica
    uv run python scripts/publish_pentateuco.py --check    # só verifica, não escreve
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Reuso integral do parsing auditado — não duplicar regex de bloco.
from cite import _ITEM_RE, _HEADING_RE, _find_block, literal_text
from kardec_structure import (
    INDEX_PART_RE,
    PART_ORDINAL,
    _roman_to_int,
)

ROOT = Path(__file__).resolve().parents[1]
PENTATEUCO_DIR = ROOT / "raw" / "kardec" / "pentateuco"
WIKI_PENTATEUCO = ROOT / "wiki" / "pentateuco"
ANCHORS_PATH = ROOT / "data" / "pentateuco-anchors.json"
WIKI_PREFIX = "wiki/pentateuco"

TODAY = "2026-06-05"

# (slug do raw / .index.md, sigla de citação, nome canônico, unidade citável)
# unidade "q" → heading "## q. N" e chave de manifest "questions"; "item" →
# "## item N" e chave "items".
OBRAS: list[tuple[str, str, str, str]] = [
    ("livro-dos-espiritos", "LE", "O Livro dos Espíritos", "q"),
    ("livro-dos-mediuns", "LM", "O Livro dos Médiuns", "item"),
    ("evangelho-segundo-o-espiritismo", "ESE", "O Evangelho segundo o Espiritismo", "item"),
    ("ceu-e-inferno", "C&I", "O Céu e o Inferno", "item"),
    ("genese", "Genese", "A Gênese", "item"),
]

# Linha de capítulo no .index.md, com título e range de linhas:
#   "- **Capítulo I — De Deus** (linhas 178–226) — 1. Que é Deus?..."
_IDX_CHAP_RE = re.compile(
    r"^-\s+\*\*Cap[íi]tulo\s+(?P<roman>[IVXLCDM]+)\s*[—–-]\s*(?P<title>.+?)\*\*"
    r"\s*\(linhas\s+(?P<start>\d+)\s*[–\-—]\s*(?P<end>\d+)\)"
)

# Heading de capítulo no corpo do raw ("## Capítulo I — De Deus") — descartado
# do corpo publicado (vira H1/frontmatter).
_BODY_CHAP_RE = re.compile(r"^##\s+Cap[íi]tulo\b", re.IGNORECASE)


class Chapter:
    __slots__ = ("part", "roman", "title", "start", "end")

    def __init__(self, part: int | None, roman: str, title: str, start: int, end: int):
        self.part = part
        self.roman = roman
        self.title = title
        self.start = start  # 1-based, inclusivo (linha do "## Capítulo …")
        self.end = end      # 1-based, inclusivo (última linha do capítulo)

    @property
    def has_part(self) -> bool:
        return self.part is not None

    def filename(self) -> str:
        rl = self.roman.lower()
        return f"parte-{self.part}-cap-{rl}.md" if self.has_part else f"cap-{rl}.md"


def parse_chapters(index_path: Path) -> list[Chapter]:
    """Lê o `<obra>.index.md` e devolve a lista ordenada de capítulos, com a
    parte corrente rastreada a partir das linhas `### … parte`."""
    chapters: list[Chapter] = []
    current_part: int | None = None
    for line in index_path.read_text(encoding="utf-8").splitlines():
        m_part = INDEX_PART_RE.match(line)
        if m_part:
            title = m_part.group("title").strip().lower()
            if title.startswith("introdu"):
                current_part = None
                continue
            roman = m_part.group("roman")
            ordinal = m_part.group("ordinal")
            if roman:
                current_part = _roman_to_int(roman.upper())
            elif ordinal:
                current_part = PART_ORDINAL.get(ordinal.lower())
            else:
                current_part = PART_ORDINAL.get(title.split()[0])
            continue
        m_chap = _IDX_CHAP_RE.match(line)
        if m_chap:
            chapters.append(
                Chapter(
                    current_part,
                    m_chap.group("roman").upper(),
                    m_chap.group("title").strip(),
                    int(m_chap.group("start")),
                    int(m_chap.group("end")),
                )
            )
    return chapters


def _anchor(unidade: str, n: int) -> str:
    """Âncora github-slugger do heading de formato fixo.

    github-slugger de "q. N" → "q-N" e "item N" → "item-N" (minúsculo, pontuação
    removida, espaço → hífen). Formato fixo ⇒ mapeamento determinístico, sem
    depender da slugificação genérica do Quartz. Verificado pelo caso da Bíblia
    (heading "## 1" → âncora "#1") já em produção."""
    return f"q-{n}" if unidade == "q" else f"item-{n}"


def _heading(unidade: str, n: int) -> str:
    return f"## q. {n}" if unidade == "q" else f"## item {n}"


def _manifest_key(sigla: str, chap: Chapter, n: int) -> str:
    """Chave do manifest, alinhada com a construção de chave de
    `link_citations.kardec_url` (item_urls):

    - LE: questão global → str(n) (em "questions").
    - LM: item contínuo 1–350 → str(n) flat (em "items").
    - ESE/Gênese (sem parte): "ROMAN:n".
    - C&I (com parte): "PARTE:ROMAN:n".
    """
    if sigla == "LE" or sigla == "LM":
        return str(n)
    if chap.has_part:
        return f"{chap.part}:{chap.roman}:{n}"
    return f"{chap.roman}:{n}"


def _cite_ref(sigla: str, chap: Chapter, n: int) -> str:
    """Referência no formato que o cite.py entende, para o round-trip."""
    if sigla == "LE":
        return f"q. {n}"
    if sigla == "LM":
        return f"item {n}"
    return f"cap. {chap.roman}, item {n}"


def build_chapter_page(
    sigla: str,
    obra_nome: str,
    unidade: str,
    obra_slug: str,
    chap: Chapter,
    all_lines: list[str],
) -> tuple[str, dict[str, str]]:
    """Devolve (conteúdo markdown da página, {chave_manifest: caminho#âncora}).

    Injeta uma âncora antes de cada questão/item; registra no manifest apenas a
    PRIMEIRA ocorrência de cada número (semântica do cite.py) cujo bloco passa o
    round-trip contra `cite.literal_text`."""
    # Slice 1-based inclusivo → 0-based [start-1:end].
    body_lines = all_lines[chap.start - 1 : chap.end]
    # Descarta a linha "## Capítulo …" inicial (vira H1).
    if body_lines and _BODY_CHAP_RE.match(body_lines[0]):
        body_lines = body_lines[1:]

    rel = f"{obra_slug}/{chap.filename()[:-3]}"  # sem ".md"

    # Corpo: âncora `## q./item N` antes de cada item (mantém o page-block
    # alinhado com a terminação por _ITEM_RE/_HEADING_RE que o cite.py usa).
    out: list[str] = []
    for line in body_lines:
        m = _ITEM_RE.match(line)
        if m:
            out += ["", _heading(unidade, int(m.group(1))), ""]
        out.append(line)

    # Manifest: registro determinístico sobre o raw absoluto, validado por
    # round-trip contra cite.literal_text (independente do drop do H1).
    registered = _register_anchors(sigla, unidade, chap, rel, all_lines)

    content = _frontmatter(sigla, obra_nome, chap) + _h1(obra_nome, chap) + "\n".join(out).strip() + "\n"
    return content, registered


def _register_anchors(
    sigla: str,
    unidade: str,
    chap: Chapter,
    rel: str,
    all_lines: list[str],
) -> dict[str, str]:
    """Para cada primeira ocorrência de item no range do capítulo, valida o bloco
    contra cite.literal_text e registra a âncora se baterem exatamente."""
    registered: dict[str, str] = {}
    seen: set[int] = set()
    lo = chap.start - 1
    hi = chap.end  # exclusivo em 0-based
    for i in range(lo, min(hi, len(all_lines))):
        m = _ITEM_RE.match(all_lines[i])
        if not m:
            continue
        n = int(m.group(1))
        if n in seen:
            continue
        seen.add(n)
        end = _find_block(all_lines, i, [_ITEM_RE, _HEADING_RE])
        end = min(end, hi)
        my_block = "\n".join(all_lines[i:end]).strip()
        truth = literal_text(sigla, _cite_ref(sigla, chap, n))
        if truth is None or truth.strip() != my_block:
            continue  # locus irregular → sem âncora interna (fallback externo)
        registered[_manifest_key(sigla, chap, n)] = f"{rel}#{_anchor(unidade, n)}"
    return registered


def _frontmatter(sigla: str, obra_nome: str, chap: Chapter) -> str:
    lines = [
        "---",
        "tipo: capitulo-pentateuco",
        f"obra: {obra_nome}",
        f"sigla: {sigla}",
    ]
    if chap.has_part:
        lines.append(f"parte: {chap.part}")
    lines += [
        f"capitulo: {chap.roman}",
        f"fontes: [{sigla}]",
        "tags: []",
        f"atualizado_em: {TODAY}",
        "status: ativo",
        "---",
        "",
        "",
    ]
    return "\n".join(lines)


def _h1(obra_nome: str, chap: Chapter) -> str:
    parte = f" — {chap.part}ª parte" if chap.has_part else ""
    return f"# {obra_nome}{parte} — Cap. {chap.roman} — {chap.title}\n\n"


def _obra_index(sigla: str, obra_nome: str, obra_slug: str, chapters: list[Chapter]) -> str:
    fm = "\n".join(
        [
            "---",
            "tipo: obra-pentateuco",
            f"obra: {obra_nome}",
            f"sigla: {sigla}",
            f"fontes: [{sigla}]",
            "tags: []",
            f"atualizado_em: {TODAY}",
            "status: ativo",
            "---",
            "",
            "",
        ]
    )
    links = [
        f"- [[{WIKI_PREFIX}/{obra_slug}/{c.filename()[:-3]}|Cap. {c.roman} — {c.title}]]"
        for c in chapters
    ]
    body = [
        f"# {obra_nome}",
        "",
        f"Texto integral de **{obra_nome}** ({sigla}) com âncora por questão/item, "
        "para citação e link interno. Análise e leitura kardecista da obra em "
        f"[[wiki/obras/{obra_slug}]].",
        "",
        "## Capítulos",
        "",
        *links,
        "",
    ]
    return fm + "\n".join(body)


def _top_index() -> str:
    fm = "\n".join(
        [
            "---",
            "tipo: obra-pentateuco",
            "obra: Pentateuco",
            "fontes: []",
            "tags: []",
            f"atualizado_em: {TODAY}",
            "status: ativo",
            "---",
            "",
            "",
        ]
    )
    links = [f"- [[{WIKI_PREFIX}/{slug}/index|{nome}]]" for slug, _, nome, _ in OBRAS]
    body = [
        "# Pentateuco — texto integral",
        "",
        "Cópia derivada das cinco obras da Codificação, com âncora por questão/item "
        "para link interno. Fonte: `raw/kardec/pentateuco/` (intocada).",
        "",
        *links,
        "",
    ]
    return fm + "\n".join(body)


def publish(check_only: bool) -> int:
    if not PENTATEUCO_DIR.is_dir():
        print(f"ERRO: {PENTATEUCO_DIR} não existe", file=sys.stderr)
        return 1

    manifest: dict[str, dict[str, dict[str, str]]] = {"_prefix": WIKI_PREFIX}
    written = 0
    total_anchors = 0

    for obra_slug, sigla, obra_nome, unidade in OBRAS:
        index_path = PENTATEUCO_DIR / f"{obra_slug}.index.md"
        md_path = PENTATEUCO_DIR / f"{obra_slug}.md"
        if not index_path.exists() or not md_path.exists():
            print(f"AVISO: faltando index/md para {obra_slug}", file=sys.stderr)
            continue
        all_lines = md_path.read_text(encoding="utf-8").splitlines()
        chapters = parse_chapters(index_path)

        unit_key = "questions" if unidade == "q" else "items"
        book_anchors: dict[str, str] = {}

        for chap in chapters:
            content, registered = build_chapter_page(
                sigla, obra_nome, unidade, obra_slug, chap, all_lines
            )
            book_anchors.update(registered)
            if not check_only:
                out = WIKI_PENTATEUCO / obra_slug / chap.filename()
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_text(content, encoding="utf-8")
                written += 1

        manifest[sigla] = {unit_key: book_anchors}
        total_anchors += len(book_anchors)

        if not check_only:
            idx = WIKI_PENTATEUCO / obra_slug / "index.md"
            idx.parent.mkdir(parents=True, exist_ok=True)
            idx.write_text(_obra_index(sigla, obra_nome, obra_slug, chapters), encoding="utf-8")
        print(f"  {sigla}: {len(chapters)} capítulos, {len(book_anchors)} âncoras")

    if not check_only:
        (WIKI_PENTATEUCO / "index.md").write_text(_top_index(), encoding="utf-8")
        ANCHORS_PATH.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    print(
        f"\nTotal: {written} páginas, {total_anchors} âncoras verificadas (round-trip cite.py)."
        + ("" if check_only else f"\nManifest: {ANCHORS_PATH.relative_to(ROOT)}")
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="só verifica âncoras (round-trip), não escreve")
    args = ap.parse_args(argv)
    return publish(check_only=args.check)


if __name__ == "__main__":
    raise SystemExit(main())
