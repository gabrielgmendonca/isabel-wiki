#!/usr/bin/env python3
"""Autofix de canonical_names — envolve aliases plain-text em wikilinks.

Reusa o mapa alias→canonical de `check_canonical_names`. Para cada ocorrência de
alias registrado fora de wikilink/blockquote/inline-code/frontmatter, substitui
`alias` por `[[canonical|alias]]`. Skip por allowlist quando a linha sinaliza
listagem intencional de variantes (pseudônimo, nome civil, catálogo).

Default é dry-run com diff resumido; `--apply` materializa as mudanças.
"""

import argparse
import difflib
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _lib.wiki_utils import (  # noqa: E402
    WIKI_DIR,
    collect_pages,
    page_key,
    parse_frontmatter,
)

CANONICAL_DIRS = ("personalidades", "obras")

# Padrões de linha onde aliases são listados intencionalmente — não envolver.
ALLOWLIST_LINE_PATTERNS = [
    re.compile(r"pseud[oô]nimo", re.IGNORECASE),
    re.compile(r"também\s+conhecid[oa]", re.IGNORECASE),
    re.compile(r"nome\s+(civil|de\s+batismo|completo|original)", re.IGNORECASE),
    re.compile(r"outras\s+formas", re.IGNORECASE),
    re.compile(r"^aliases\s*:", re.IGNORECASE),
    # catálogo lista variantes adjacentes ("Yvonne A. Pereira / Yvonne do Amaral")
    re.compile(r"\s/\s"),
]


def build_alias_map(pages: list[Path]) -> dict[str, str]:
    """alias → caminho-canônico (page_key sem .md)."""
    amap: dict[str, str] = {}
    for page in pages:
        if not any(f"/{d}/" in str(page) for d in CANONICAL_DIRS):
            continue
        fm, _ = parse_frontmatter(page)
        aliases = fm.get("aliases") or []
        if isinstance(aliases, str):
            aliases = [aliases]
        for alias in aliases:
            a = alias.strip()
            if len(a) < 4:
                continue
            if a in amap:
                continue
            amap[a] = page_key(page)
    return amap


def excluded_ranges(line: str) -> list[tuple[int, int]]:
    """Ranges [start, end) na linha que devem ser ignorados: wikilink ou backticks."""
    ranges: list[tuple[int, int]] = []
    for m in re.finditer(r"\[\[[^\]]*\]\]", line):
        ranges.append((m.start(), m.end()))
    for m in re.finditer(r"`[^`\n]+`", line):
        ranges.append((m.start(), m.end()))
    return ranges


def in_excluded(pos: int, ranges: list[tuple[int, int]]) -> bool:
    return any(s <= pos < e for s, e in ranges)


def is_allowlisted_line(line: str) -> bool:
    return any(p.search(line) for p in ALLOWLIST_LINE_PATTERNS)


def split_frontmatter(text: str) -> tuple[str, str]:
    """Retorna (frontmatter_inclusive, body). Se não houver, ('', text)."""
    if not text.startswith("---\n"):
        return "", text
    m = re.search(r"^---\n", text[4:], re.MULTILINE)
    if not m:
        return "", text
    end = 4 + m.end()
    return text[:end], text[end:]


def _fold(s: str) -> str:
    """Remove acentos e lowercase — para comparar 'Pôncio' com slug 'poncio'."""
    return "".join(
        c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c)
    ).lower()


def _slug_words(canon: str) -> list[str]:
    return [_fold(w) for w in canon.split("/")[-1].split("-")]


def alias_is_canonical_tail(canon: str, alias: str) -> tuple[bool, list[str]]:
    """True se alias-words formam o sufixo estrito do slug. Retorna (bool, head_missing)."""
    slug_words = _slug_words(canon)
    alias_words = [_fold(w) for w in alias.split()]
    if len(alias_words) >= len(slug_words):
        return False, []
    if slug_words[-len(alias_words):] != alias_words:
        return False, []
    return True, slug_words[: -len(alias_words)]


def alias_is_canonical_head(canon: str, alias: str) -> tuple[bool, list[str]]:
    """True se alias-words formam o prefixo estrito do slug. Retorna (bool, tail_missing)."""
    slug_words = _slug_words(canon)
    alias_words = [_fold(w) for w in re.findall(r"\w+", alias)]
    if len(alias_words) >= len(slug_words):
        return False, []
    if slug_words[: len(alias_words)] != alias_words:
        return False, []
    return True, slug_words[len(alias_words):]


def preceded_by_head(line: str, match_start: int, head: list[str]) -> bool:
    """Verifica se as palavras imediatamente antes de `match_start` na linha
    casam (accent/case-insensitive) com `head`.
    """
    if not head:
        return False
    prefix = line[:match_start]
    tokens = re.findall(r"\S+", prefix)
    if len(tokens) < len(head):
        return False
    tail_tokens = [_fold(t.strip(".,;:()[]{}\"'*")) for t in tokens[-len(head):]]
    return tail_tokens == head


def followed_by_tail(line: str, match_end: int, tail: list[str]) -> bool:
    """Verifica se as palavras logo após `match_end` casam com `tail`."""
    if not tail:
        return False
    suffix = line[match_end:]
    tokens = re.findall(r"\S+", suffix)
    if len(tokens) < len(tail):
        return False
    head_tokens = [_fold(t.strip(".,;:()[]{}\"'*")) for t in tokens[: len(tail)]]
    return head_tokens == tail


def line_has_canonical_link(line: str, canonical: str) -> bool:
    """True se a linha já contém [[<canonical>...]] (com ou sem display alias).

    Catch para entradas de catálogo (`[[wiki/personalidades/X]] — X (...)`) e
    bibliografias bilíngues (`[[wiki/obras/estela|*Estela*]] (*Stella*...)`) —
    casos onde o alias listado é descritivo, não link adicional.
    """
    return bool(re.search(rf"\[\[{re.escape(canonical)}(?:[|\]#])", line))


def wrap_in_body(
    body: str,
    aliases_sorted: list[str],
    amap: dict[str, str],
    canonical_page_key: str,
) -> tuple[str, int]:
    """Aplica wraps no body. Retorna (novo_body, n_substituicoes)."""
    lines = body.splitlines(keepends=True)
    in_fence = False
    n_subs = 0
    for i, raw_line in enumerate(lines):
        stripped = raw_line.lstrip()
        # Fenced code blocks (```)
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        # Blockquotes
        if stripped.startswith(">"):
            continue
        if is_allowlisted_line(raw_line):
            continue

        line = raw_line
        # Aplica aliases na ordem (longest-first); recalcula ranges após cada wrap
        for alias in aliases_sorted:
            canon = amap[alias]
            if canon == canonical_page_key:
                continue  # página da própria entidade
            # Skip se canonical já aparece como link na linha (catálogo/biblio)
            if line_has_canonical_link(line, canon):
                continue
            is_tail, head = alias_is_canonical_tail(canon, alias)
            is_head, tail = alias_is_canonical_head(canon, alias)
            pat = re.compile(rf"\b{re.escape(alias)}\b")
            # Loop até não restar match fora de exclusão
            offset = 0
            while True:
                ranges = excluded_ranges(line)
                m = pat.search(line, offset)
                if not m:
                    break
                if in_excluded(m.start(), ranges):
                    offset = m.end()
                    continue
                # Skip se alias é tail do slug e está precedido pelo head
                if is_tail and preceded_by_head(line, m.start(), head):
                    offset = m.end()
                    continue
                # Skip se alias é head do slug e está seguido pelo tail
                if is_head and followed_by_tail(line, m.end(), tail):
                    offset = m.end()
                    continue
                replacement = f"[[{canon}|{alias}]]"
                line = line[: m.start()] + replacement + line[m.end():]
                offset = m.start() + len(replacement)
                n_subs += 1
        lines[i] = line
    return "".join(lines), n_subs


def process_page(
    page: Path,
    amap: dict[str, str],
    aliases_sorted: list[str],
) -> tuple[str, int]:
    """Retorna (novo_conteudo, n_substituicoes) para a página."""
    original = page.read_text(encoding="utf-8")
    fm, body = split_frontmatter(original)
    canonical = page_key(page)
    new_body, n = wrap_in_body(body, aliases_sorted, amap, canonical)
    return fm + new_body, n


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="materializa as mudanças")
    parser.add_argument(
        "--path",
        action="append",
        default=[],
        help="restringe a páginas cujo caminho contém este substring (repetível)",
    )
    parser.add_argument(
        "--diff",
        action="store_true",
        help="imprime diff unificado por página (default: só resumo)",
    )
    args = parser.parse_args()

    pages = collect_pages()
    amap = build_alias_map(pages)
    if not amap:
        print("Nenhum alias registrado.", file=sys.stderr)
        return 0

    # longest-first evita que "Pilatos" coma "Pôncio Pilatos"
    aliases_sorted = sorted(amap.keys(), key=len, reverse=True)

    if args.path:
        pages = [p for p in pages if any(s in str(p) for s in args.path)]

    total_subs = 0
    changed = 0
    for page in pages:
        try:
            new_content, n = process_page(page, amap, aliases_sorted)
        except Exception as e:
            print(f"# erro em {page}: {e}", file=sys.stderr)
            continue
        if n == 0:
            continue
        changed += 1
        total_subs += n
        if args.diff:
            original = page.read_text(encoding="utf-8")
            diff = difflib.unified_diff(
                original.splitlines(keepends=True),
                new_content.splitlines(keepends=True),
                fromfile=str(page),
                tofile=str(page),
                n=1,
            )
            sys.stdout.writelines(diff)
        else:
            print(f"{page}: {n} substituição(ões)")
        if args.apply:
            page.write_text(new_content, encoding="utf-8")

    mode = "aplicado" if args.apply else "dry-run"
    print(
        f"\n# wrap_aliases — {mode}: {total_subs} substituição(ões) em "
        f"{changed} arquivo(s). Aliases ativos: {len(amap)}.",
        file=sys.stderr,
    )
    if not args.apply and total_subs > 0:
        print("# use --apply para materializar; --diff para ver hunks.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
