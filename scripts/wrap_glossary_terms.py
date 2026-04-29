#!/usr/bin/env python3
"""Pré-processa páginas da wiki envolvendo termos do dicionário em <abbr>.

Lê `data/dicionario.json` e, para cada termo, envolve a **primeira ocorrência
por página** em `<abbr title="definição">termo</abbr>`. Não toca:

- frontmatter YAML (entre `---` no topo);
- linhas de heading (`#`, `##`, ...);
- blocos cercados ``` ``` e código inline;
- [[wikilinks]] e [texto](url) já existentes;
- conteúdo dentro de tags HTML já abertas (heurística: não envolve se a
  ocorrência está dentro de outro `<abbr ...>...</abbr>`).

Match é case-insensitive com word boundary, mas preserva o casing original
do texto. Termos multi-palavra (ex.: "novilho cevado") toleram espaços
extras entre as palavras.

Uso:
  uv run python scripts/wrap_glossary_terms.py --check wiki/
  uv run python scripts/wrap_glossary_terms.py --apply /tmp/quartz/content/wiki
"""

import argparse
import difflib
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DICT = ROOT / "data" / "dicionario.json"

# Mesma estratégia do link_citations.py: tudo que casa SAFE_RE é devolvido
# intocado; o resto passa pela substituição.
SAFE_RE = re.compile(
    r"```.*?```"                       # fenced code
    r"|`[^`\n]+`"                      # inline code
    r"|\[\[[^\]\n]+\]\]"               # [[wikilink]]
    r"|\[[^\]\n]+\]\([^)\n]+\)"        # [text](url)
    r"|<abbr\b[^>]*>.*?</abbr>",       # já envolvido
    re.DOTALL,
)

FRONTMATTER_RE = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)
HEADING_RE = re.compile(r"^#{1,6}\s", re.MULTILINE)


def build_term_pattern(term: str) -> re.Pattern:
    """Regex case-insensitive, word-boundary, com `\\s+` entre palavras."""
    parts = [re.escape(p) for p in term.split()]
    body = r"\s+".join(parts)
    # (?<!\w) e (?!\w) funcionam corretamente com acentos em Python 3 unicode.
    return re.compile(rf"(?<!\w){body}(?!\w)", re.IGNORECASE)


def split_protected(text: str):
    """Itera (segmento_processável, segmento_protegido) preservando ordem.

    O último item pode ter `protegido = ""` se o texto não terminar em safe.
    """
    last = 0
    for m in SAFE_RE.finditer(text):
        yield text[last:m.start()], m.group(0)
        last = m.end()
    yield text[last:], ""


def wrap_first_in_segment(segment: str, term: str, definicao: str) -> tuple[str, bool]:
    """Tenta envolver a primeira ocorrência de `term` em `segment`.

    Pula matches em linhas que começam com `#` (headings).
    Retorna (novo_segmento, achou).
    """
    pattern = build_term_pattern(term)
    title = html.escape(definicao, quote=True)

    for m in pattern.finditer(segment):
        # Detecta a linha em que o match começa.
        line_start = segment.rfind("\n", 0, m.start()) + 1
        line_end = segment.find("\n", m.start())
        line_end = len(segment) if line_end == -1 else line_end
        line = segment[line_start:line_end]
        if HEADING_RE.match(line):
            continue
        original = m.group(0)
        replacement = f'<abbr title="{title}">{original}</abbr>'
        return segment[:m.start()] + replacement + segment[m.end():], True
    return segment, False


def transform(text: str, dicionario: dict[str, str]) -> str:
    # Preserva frontmatter intocado.
    fm_match = FRONTMATTER_RE.match(text)
    if fm_match:
        head = fm_match.group(0)
        body = text[fm_match.end():]
    else:
        head, body = "", text

    # Para cada termo, tenta envolver a primeira ocorrência em algum segmento
    # processável (fora de safe zones). Termos mais longos primeiro evita que
    # "novilho" seja casado antes de "novilho cevado".
    termos_ordenados = sorted(dicionario.items(), key=lambda kv: -len(kv[0]))

    # Decompõe body em lista alternada [proc, safe, proc, safe, ..., proc].
    pieces: list[str] = []
    for proc, safe in split_protected(body):
        pieces.append(proc)
        pieces.append(safe)

    for term, definicao in termos_ordenados:
        # Idempotência: se o termo já está envolto em <abbr> em algum lugar
        # da página (run anterior), considera marcado e pula. Limitar a abbrs
        # — não a todas as safe zones — preserva o caso legítimo de termo
        # citado em wikilink/link mas também solto no texto da página.
        pattern = build_term_pattern(term)
        already_wrapped = False
        for i in range(1, len(pieces), 2):
            safe = pieces[i]
            if safe.startswith("<abbr") and pattern.search(safe):
                already_wrapped = True
                break
        if already_wrapped:
            continue
        for i in range(0, len(pieces), 2):  # só índices processáveis
            new_piece, hit = wrap_first_in_segment(pieces[i], term, definicao)
            if hit:
                pieces[i] = new_piece
                break  # próximo termo

    return head + "".join(pieces)


def process_path(path: Path, dicionario: dict[str, str], apply: bool) -> bool:
    original = path.read_text(encoding="utf-8")
    new = transform(original, dicionario)
    if new == original:
        return False
    if apply:
        path.write_text(new, encoding="utf-8")
    else:
        diff = difflib.unified_diff(
            original.splitlines(keepends=True),
            new.splitlines(keepends=True),
            fromfile=str(path), tofile=str(path) + " (wrapped)",
        )
        sys.stdout.writelines(diff)
    return True


def iter_md(target: Path):
    if target.is_file():
        if target.suffix == ".md":
            yield target
    else:
        yield from sorted(target.rglob("*.md"))


def load_dicionario(path: Path) -> dict[str, str]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    termos = raw.get("termos", raw)
    return {k: v for k, v in termos.items() if not k.startswith("_")}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true", help="diff em stdout, não escreve")
    g.add_argument("--apply", action="store_true", help="escreve in-place no path")
    ap.add_argument("path", type=Path, help="arquivo .md ou diretório")
    ap.add_argument("--dicionario", type=Path, default=DEFAULT_DICT)
    args = ap.parse_args(argv)

    dicionario = load_dicionario(args.dicionario)

    changed = 0
    total = 0
    for p in iter_md(args.path):
        total += 1
        if process_path(p, dicionario, apply=args.apply):
            changed += 1

    verb = "modificados" if args.apply else "com mudanças pendentes"
    print(f"\n{changed}/{total} arquivos {verb}", file=sys.stderr)
    return 0 if (args.apply or changed == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
