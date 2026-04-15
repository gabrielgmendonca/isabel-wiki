#!/usr/bin/env python3
"""Scaffold de deck Marp a partir de uma página da wiki.

Extrai título, fontes, blockquotes com citação e seção `## Fontes`, e emite
um esqueleto Marp seguindo o padrão socrático Q&A (ver
.claude/rules/convencoes-slides.md). O esqueleto é refinado depois pela skill
/slides: marcadores `<!-- skill: ... -->` sinalizam onde a skill deve
preencher conteúdo não-determinístico (pergunta literal do LE via qmd,
parábola, síntese, etc.).
"""

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _lib.wiki_utils import parse_frontmatter  # noqa: E402

SIGLAS = r"LE|LM|ESE|C&I|Gênese|Genese|OPE|OQE|RE"
CITATION_RE = re.compile(rf"\(({SIGLAS})([^)]*)\)")

OBRA_NOME = {
    "LE": "O Livro dos Espíritos",
    "LM": "O Livro dos Médiuns",
    "ESE": "O Evangelho Segundo o Espiritismo",
    "C&I": "O Céu e o Inferno",
    "Gênese": "A Gênese",
    "Genese": "A Gênese",
    "OPE": "Obras Póstumas",
    "OQE": "O Que é o Espiritismo",
    "RE": "Revista Espírita",
}

SKIP_SECTIONS = {
    "fontes", "páginas relacionadas", "paginas relacionadas",
    "divergências", "divergencias", "ver também", "ver tambem",
}


def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[áàâã]", "a", s)
    s = re.sub(r"[éê]", "e", s)
    s = re.sub(r"[íï]", "i", s)
    s = re.sub(r"[óôõ]", "o", s)
    s = re.sub(r"[úü]", "u", s)
    s = re.sub(r"ç", "c", s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def split_body(text: str) -> tuple[str, str]:
    if not text.startswith("---"):
        return "", text
    end = text.find("\n---", 3)
    if end < 0:
        return "", text
    return text[: end + 4], text[end + 4:].lstrip("\n")


def extract_title(body: str, fallback: str) -> str:
    m = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    return m.group(1).strip() if m else fallback


def extract_sections(body: str) -> list[tuple[str, str]]:
    parts = re.split(r"^##\s+(.+)$", body, flags=re.MULTILINE)
    sections = []
    for i in range(1, len(parts), 2):
        heading = parts[i].strip()
        content = parts[i + 1].strip() if i + 1 < len(parts) else ""
        sections.append((heading, content))
    return sections


def extract_quote_with_citation(content: str) -> list[tuple[str, str, str]]:
    """Retorna [(quote_text, sigla, detalhe)] — detalhe = tudo após a sigla."""
    found = []
    current: list[str] = []
    for line in content.splitlines():
        if line.startswith(">"):
            current.append(line.lstrip("> ").rstrip())
        else:
            if current:
                joined = " ".join(l for l in current if l).strip()
                m = CITATION_RE.search(joined)
                if m:
                    quote = CITATION_RE.sub("", joined).strip().strip('"').strip()
                    found.append((quote, m.group(1), m.group(2).strip(" ,")))
                current = []
    if current:
        joined = " ".join(l for l in current if l).strip()
        m = CITATION_RE.search(joined)
        if m:
            quote = CITATION_RE.sub("", joined).strip().strip('"').strip()
            found.append((quote, m.group(1), m.group(2).strip(" ,")))
    return found


def extract_fontes(body: str) -> list[str]:
    m = re.search(r"^##\s+Fontes\s*$(.+?)(?=^##\s|\Z)", body, re.MULTILINE | re.DOTALL)
    if not m:
        return []
    items = []
    for line in m.group(1).splitlines():
        line = line.strip()
        if line.startswith("- "):
            items.append(line[2:].strip())
    return items


def compute_range(body: str, sigla_preferida: str | None) -> str | None:
    """Agrega citações no corpo para produzir 'q. 674–685' ou 'cap. XVII, item 4'."""
    nums: list[int] = []
    detalhes: list[str] = []
    for m in CITATION_RE.finditer(body):
        if sigla_preferida and m.group(1) != sigla_preferida:
            continue
        detail = m.group(2).strip(" ,")
        detalhes.append(detail)
        for qn in re.findall(r"q\.\s*(\d+)", detail):
            nums.append(int(qn))
    if nums:
        lo, hi = min(nums), max(nums)
        return f"q. {lo}" if lo == hi else f"q. {lo}–{hi}"
    if detalhes:
        return detalhes[0]
    return None


def obra_label(sigla: str | None, range_str: str | None) -> str:
    if not sigla:
        return "Doutrina Espírita"
    nome = OBRA_NOME.get(sigla, sigla)
    if range_str:
        return f"{nome} · {range_str}"
    return nome


def citation_full(sigla: str, detalhe: str) -> str:
    """'LE' + 'q. 674' -> 'O Livro dos Espíritos, q. 674'."""
    nome = OBRA_NOME.get(sigla, sigla)
    return f"{nome}, {detalhe}" if detalhe else nome


def render_deck(
    title: str,
    sigla_principal: str | None,
    range_principal: str | None,
    sections_qa: list[tuple[str, list[tuple[str, str, str]]]],
    fontes_bib: list[str],
    source_page: Path,
    data_palestra: str,
    casa: str | None,
) -> str:
    footer_extra = f" · {casa}" if casa else ""
    header = (
        "---\n"
        "marp: true\n"
        "theme: isabel\n"
        "paginate: true\n"
        f"header: '{title}'\n"
        f"footer: 'Gabriel Mendonça · {data_palestra}{footer_extra}'\n"
        "---\n\n"
    )

    obra_str = obra_label(sigla_principal, range_principal)
    cap = (
        f"# {title}\n\n"
        f"**{obra_str}**\n\n"
        f"Gabriel Mendonça · {data_palestra}{footer_extra}\n\n"
        "---\n\n"
    )

    abertura = (
        "## Abertura\n\n"
        "*<!-- skill: escrever pergunta socrática de abertura (5-15 palavras, "
        "retórica, ancora o tema). Substituir todo este slide pela pergunta. -->*\n\n"
        "---\n\n"
    )

    body_parts: list[str] = []
    for idx, (section_heading, qa_list) in enumerate(sections_qa, start=1):
        if not qa_list:
            continue
        body_parts.append(
            "<!-- _class: section -->\n\n"
            f"## Parte {idx} — {section_heading}\n\n"
            f"*<!-- skill: opcional — reescrever título da parte em linguagem "
            f"de palestra se '{section_heading}' soar técnico demais -->*\n\n"
            "---\n\n"
        )
        for quote, sigla, detalhe in qa_list:
            cite_full = citation_full(sigla, detalhe)
            if sigla == "LE":
                # Dois passos: pergunta + resposta
                body_parts.append(
                    f"## {cite_full}\n\n"
                    f"*<!-- skill: preencher pergunta literal de {sigla}, {detalhe} "
                    f"via qmd query em collection 'raw' (Kardec). Manter o número "
                    f"da questão visível como subtítulo. -->*\n\n"
                    "---\n\n"
                )
                short = len(quote) < 200
                todo_expand = (
                    f"\n*<!-- skill: resposta curta no wiki — expandir com texto "
                    f"integral da resposta dos Espíritos de {sigla}, {detalhe} via qmd "
                    f"raw. Usar (...) para elipses em trechos não-essenciais. -->*\n"
                    if short else ""
                )
                body_parts.append(
                    "<!-- _class: quote -->\n\n"
                    f"> {quote}\n"
                    f"{todo_expand}\n"
                    f"**{cite_full}**\n\n"
                    "---\n\n"
                )
            else:
                # Obras não-LE: slide único com citação + TODO de expansão opcional
                body_parts.append(
                    "<!-- _class: quote -->\n\n"
                    f"> {quote}\n\n"
                    f"**{cite_full}**\n\n"
                    "---\n\n"
                )

    parabola = (
        "<!-- _class: section -->\n\n"
        "## Para meditar\n\n"
        "---\n\n"
        "## *<!-- skill: título -->*\n\n"
        "*<!-- skill: referência (ex: 'Mateus 25:14–30' ou 'C&I, 2ª parte, cap. V' "
        "ou 'wiki/personalidades/dimas') -->*\n\n"
        "*<!-- skill: sugerir 1 item pertinente entre: (a) parábola evangélica, "
        "(b) caso de O Céu e o Inferno, (c) personalidade/caso de André Luiz "
        "(Entre a Terra e o Céu, Nosso Lar etc.), (d) página de wiki/personalidades/ "
        "ou wiki/parabolas/. Apenas título + referência — NÃO incluir texto integral. "
        "Querier qmd em wiki/parabolas/, wiki/personalidades/, raw/. -->*\n\n"
        "---\n\n"
    )

    sintese = (
        "<!-- _class: section -->\n\n"
        "## Síntese\n\n"
        "---\n\n"
        "## Síntese\n\n"
        "*<!-- skill: 3-5 bullets consolidando a resposta à pergunta de abertura. "
        "Tom de encerramento, não de recapitulação mecânica. -->*\n\n"
        "---\n\n"
    )

    encerramento = (
        "<!-- _class: quote -->\n\n"
        "*<!-- skill: opcional — citação consolidadora (Jesus, Kardec, ou espírito "
        "do Pentateuco) que encerre a palestra. Remover este slide se não couber. -->*\n\n"
        "---\n\n"
    )

    fontes_slide = "<!-- _class: source -->\n\n## Fontes\n\n"
    if fontes_bib:
        fontes_slide += "\n".join(f"- {f}" for f in fontes_bib) + "\n"
    else:
        fontes_slide += f"- Página wiki: `{source_page}`\n"

    return (
        header + cap + abertura
        + "".join(body_parts)
        + parabola + sintese + encerramento + fontes_slide
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("page", type=Path, help="Caminho para página da wiki")
    ap.add_argument("--out", type=Path, help="Saída (default: slides/<slug>/deck.md)")
    ap.add_argument(
        "--date", dest="data", required=True,
        help="Data da palestra (YYYY-MM-DD). A skill pergunta ao usuário.",
    )
    ap.add_argument("--casa", default=None, help="Nome da casa espírita (opcional)")
    args = ap.parse_args()

    if not re.match(r"^\d{4}-\d{2}-\d{2}$", args.data):
        print(json.dumps({"error": f"--date deve ser YYYY-MM-DD, recebi: {args.data}"}))
        return 1

    page = args.page
    if not page.exists():
        print(json.dumps({"error": f"page not found: {page}"}))
        return 1

    text = page.read_text(encoding="utf-8")
    fm, _ = parse_frontmatter(page)
    _, body = split_body(text)
    title = extract_title(body, page.stem)

    fontes_fm = fm.get("fontes", [])
    if isinstance(fontes_fm, str):
        fontes_fm = [fontes_fm]
    sigla_principal = fontes_fm[0] if fontes_fm else None
    range_principal = compute_range(body, sigla_principal)

    sections = extract_sections(body)
    sections_qa: list[tuple[str, list[tuple[str, str, str]]]] = []
    for heading, content in sections:
        if heading.lower() in SKIP_SECTIONS:
            continue
        quotes = extract_quote_with_citation(content)
        if quotes:
            sections_qa.append((heading, quotes))

    fontes_bib = extract_fontes(body)

    out = args.out or Path("slides") / slugify(title) / "deck.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    deck = render_deck(
        title, sigla_principal, range_principal, sections_qa,
        fontes_bib, page, args.data, args.casa,
    )
    out.write_text(deck, encoding="utf-8")

    total_qa = sum(len(qa) for _, qa in sections_qa)
    print(json.dumps({
        "deck": str(out),
        "title": title,
        "obra": obra_label(sigla_principal, range_principal),
        "partes": len(sections_qa),
        "qa_pairs": total_qa,
        "fontes_bib": len(fontes_bib),
        "data": args.data,
        "casa": args.casa,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
