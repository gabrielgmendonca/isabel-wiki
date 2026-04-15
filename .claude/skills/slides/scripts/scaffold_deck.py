#!/usr/bin/env python3
"""Scaffold de deck Marp a partir de uma página da wiki.

Extrai título, fontes, blockquotes com citação e seção `## Fontes`, e emite
um esqueleto Marp seguindo o padrão socrático Q&A (ver
.claude/rules/convencoes-slides.md). O esqueleto é refinado depois pela skill
/slides (perguntas reescritas, parábola adicionada, slides em branco
intercalados).
"""

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _lib.wiki_utils import parse_frontmatter  # noqa: E402

CITATION_RE = re.compile(
    r"\((LE|LM|ESE|C&I|Gênese|Genese|OPE|OQE|RE)[^)]*\)"
)


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
    """Separa frontmatter do corpo."""
    if not text.startswith("---"):
        return "", text
    end = text.find("\n---", 3)
    if end < 0:
        return "", text
    return text[: end + 4], text[end + 4 :].lstrip("\n")


def extract_title(body: str, fallback: str) -> str:
    m = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    return m.group(1).strip() if m else fallback


def extract_sections(body: str) -> list[tuple[str, str]]:
    """Retorna lista de (heading, conteúdo) das seções `##`."""
    parts = re.split(r"^##\s+(.+)$", body, flags=re.MULTILINE)
    sections = []
    # parts[0] é o conteúdo antes do primeiro ##, ignoramos
    for i in range(1, len(parts), 2):
        heading = parts[i].strip()
        content = parts[i + 1].strip() if i + 1 < len(parts) else ""
        sections.append((heading, content))
    return sections


def extract_quote_with_citation(content: str) -> list[tuple[str, str]]:
    """Encontra blockquotes que contêm citação. Retorna [(quote_text, citation)]."""
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
                    quote = CITATION_RE.sub("", joined).strip().rstrip('"').strip()
                    found.append((quote, m.group(0)))
                current = []
    if current:
        joined = " ".join(l for l in current if l).strip()
        m = CITATION_RE.search(joined)
        if m:
            quote = CITATION_RE.sub("", joined).strip().rstrip('"').strip()
            found.append((quote, m.group(0)))
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


def heading_to_question(heading: str, title: str) -> str:
    """Converte heading de seção em pergunta retórica curta."""
    h = heading.strip().rstrip(".?!:")
    lower = h.lower()
    if lower.startswith(("o que", "por que", "como", "quando", "onde", "haverá", "é ", "qual")):
        return h + "?"
    if lower in {"definição", "definicao"}:
        return f"O que é {title.lower()}?"
    return f"E quanto a: {h}?"


def render_deck(
    title: str,
    fontes: list[str],
    qa_pairs: list[tuple[str, str, str]],
    fontes_bib: list[str],
    source_page: Path,
) -> str:
    today = date.today().isoformat()
    fonte_str = ", ".join(fontes) if fontes else "Doutrina Espírita"
    header = (
        "---\n"
        "marp: true\n"
        "paginate: true\n"
        f"header: '{title}'\n"
        f"footer: 'Gabriel Mendonça · {today}'\n"
        "---\n\n"
    )
    cap = (
        f"# {title}\n\n"
        f"**{fonte_str}**\n\n"
        f"Gabriel Mendonça · {today}\n\n"
        "---\n\n"
    )
    abertura = (
        "<!-- _class: blank -->\n\n"
        "---\n\n"
        f"## E afinal — {title.lower()}?\n\n"
        "*<!-- TODO: reescrever como pergunta socrática que ancora o tema -->*\n\n"
        "---\n\n"
    )
    body_parts = []
    for q, a, cite in qa_pairs:
        body_parts.append(f"## {q}\n\n---\n\n")
        body_parts.append(
            f"<!-- _class: quote -->\n\n"
            f"> {a}\n\n"
            f"**{cite}**\n\n"
            "---\n\n"
        )
        body_parts.append("<!-- _class: blank -->\n\n---\n\n")

    parabola = (
        "## Uma parábola\n\n"
        "*<!-- TODO: inserir parábola ou caso ilustrativo (2-4 slides). "
        "Sugestões via qmd query em wiki/parabolas/ ou wiki/personalidades/ -->*\n\n"
        "---\n\n"
        "<!-- _class: blank -->\n\n---\n\n"
    )
    sintese = (
        f"## Voltando à pergunta — {title.lower()}\n\n"
        "*<!-- TODO: síntese que retoma a pergunta de abertura com a resposta consolidada -->*\n\n"
        "---\n\n"
    )
    fontes_slide = "<!-- _class: source -->\n\n## Fontes\n\n"
    if fontes_bib:
        fontes_slide += "\n".join(f"- {f}" for f in fontes_bib) + "\n"
    else:
        fontes_slide += f"- Página wiki: `{source_page}`\n"

    return header + cap + abertura + "".join(body_parts) + parabola + sintese + fontes_slide


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("page", type=Path, help="Caminho para página da wiki (ex: wiki/conceitos/lei-do-trabalho.md)")
    ap.add_argument("--out", type=Path, help="Caminho de saída (default: slides/<slug>/deck.md)")
    args = ap.parse_args()

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

    sections = extract_sections(body)
    qa: list[tuple[str, str, str]] = []
    for heading, content in sections:
        if heading.lower() in {"fontes", "páginas relacionadas", "paginas relacionadas", "divergências", "divergencias"}:
            continue
        for quote, cite in extract_quote_with_citation(content):
            q = heading_to_question(heading, title)
            qa.append((q, quote, cite))

    fontes_bib = extract_fontes(body)

    out = args.out or Path("slides") / slugify(title) / "deck.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    deck = render_deck(title, fontes_fm, qa, fontes_bib, page)
    out.write_text(deck, encoding="utf-8")

    print(json.dumps({
        "deck": str(out),
        "title": title,
        "fontes": fontes_fm,
        "qa_pairs": len(qa),
        "fontes_bib": len(fontes_bib),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
