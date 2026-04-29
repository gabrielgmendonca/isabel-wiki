#!/usr/bin/env python3
"""Pré-processa páginas da wiki transformando citações inline em links.

- Citações Kardec (LE, LM, ESE, C&I, Gênese) → link Markdown para Kardecpedia
  no nível do capítulo (LE também resolve via questão).
- Citações da *Revista Espírita* `(RE, mês/ano, …)` → link para o primeiro
  artigo do mês na Kardecpédia (ou para o índice do ano, se o mês não casar).
- Citações de complementares no formato `(Autor, *Obra*, ref)` → wikilink para
  `wiki/obras/<slug-da-obra>` quando a página existir.

Não toca citações dentro de [[wikilinks]] existentes, [texto](url) já linkado,
`código inline` ou ``` blocos cercados ```.

Uso:
  uv run python scripts/link_citations.py --check wiki/aprofundamentos/expiacao-e-arrependimento.md
  uv run python scripts/link_citations.py --apply /tmp/quartz/content
"""

import argparse
import difflib
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MAPPING = ROOT / "data" / "kardec-mapping.json"
DEFAULT_REVISTA = ROOT / "data" / "revista-espirita-mapping.json"
DEFAULT_OBRAS = ROOT / "wiki" / "obras"

# ─── safe zones ───────────────────────────────────────────────────────────────
# Match (in order): fenced code, inline code, wikilinks, existing markdown links.
# These are returned untouched.
SAFE_RE = re.compile(
    r"```.*?```"                  # fenced code (DOTALL)
    r"|`[^`\n]+`"                 # inline code
    r"|\[\[[^\]\n]+\]\]"          # [[wikilink]] or [[wikilink|alias]]
    r"|\[[^\]\n]+\]\([^)\n]+\)",  # [text](url)
    re.DOTALL,
)

# ─── Kardec citations ─────────────────────────────────────────────────────────
# Captura a citação inteira para passar a um parser específico.
KARDEC_RE = re.compile(
    r"\(\s*(?P<sigla>LE|LM|ESE|C&I|Gênese|Genese)\b(?P<rest>[^)]*)\)"
)

PART_NUM_RE = re.compile(r"(?P<n>[1-5])\s*[ªa°]?\s*parte", re.IGNORECASE)
CAP_RE      = re.compile(r"cap\.\s*(?P<r>[ivxlcdm]+)\b", re.IGNORECASE)
Q_RE        = re.compile(r"q\.\s*(?P<n>\d+)")
INTRO_RE    = re.compile(r"introdu[çc][ãa]o", re.IGNORECASE)
INTRO_IT_RE = re.compile(r"introdu[çc][ãa]o[^,]*,\s*item\s+(?P<r>[ivxlcdm]+)", re.IGNORECASE)

SIGLA_NORM = {"Gênese": "Genese"}

# ─── Revista Espírita ─────────────────────────────────────────────────────────
# (RE, jan/1858, p. 12) | (RE, janeiro/1858) | (RE, fev. de 1860, p. 45)
RE_CITE_RE = re.compile(
    r"\(\s*RE\s*,\s*"
    r"(?P<mes>[A-Za-zçÇãÃáéíóúÁÉÍÓÚâêôÂÊÔ]+)\.?"
    r"(?:\s*/\s*|\s+(?:de\s+)?)"
    r"(?P<ano>1[89]\d{2})"
    r"\b[^)]*\)"
)

MONTHS_NORM = {
    "janeiro": "janeiro", "jan": "janeiro",
    "fevereiro": "fevereiro", "fev": "fevereiro",
    "março": "marco", "marco": "marco", "mar": "marco",
    "abril": "abril", "abr": "abril",
    "maio": "maio", "mai": "maio",
    "junho": "junho", "jun": "junho",
    "julho": "julho", "jul": "julho",
    "agosto": "agosto", "ago": "agosto",
    "setembro": "setembro", "set": "setembro", "sept": "setembro",
    "outubro": "outubro", "out": "outubro",
    "novembro": "novembro", "nov": "novembro",
    "dezembro": "dezembro", "dez": "dezembro",
}

# ─── Complementares ───────────────────────────────────────────────────────────
# `(Autor, *Obra*, qualquer-coisa)` — pega o primeiro *itálico* dentro do paren.
COMPL_RE = re.compile(
    r"\((?P<head>[^()*]*?),\s*\*(?P<obra>[^*\n]+)\*(?P<tail>[^)]*)\)"
)

# Stop-words removidas do início do título antes do slug match (artigos PT-BR).
STOP_PREFIXES = ("o ", "a ", "os ", "as ", "um ", "uma ")


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    text = re.sub(r"[-\s]+", "-", text)
    return text


def load_obras_index(obras_dir: Path) -> set[str]:
    if not obras_dir.is_dir():
        return set()
    return {p.stem for p in obras_dir.glob("*.md") if p.stem != "index"}


def resolve_obra_slug(obra_title: str, obras_index: set[str]) -> str | None:
    """Tenta casar o título da obra com um slug em wiki/obras/.

    Estratégias, em ordem:
      1. Slug exato do título.
      2. Slug sem artigo inicial (ex.: "O Consolador" → "consolador").
      3. Slug exato sem prefixo `o-`/`a-` candidato (ambiguidade resolvida só
         se houver match único).
    """
    s = slugify(obra_title)
    if s in obras_index:
        return s

    lowered = obra_title.lower().strip()
    for prefix in STOP_PREFIXES:
        if lowered.startswith(prefix):
            stripped = slugify(obra_title[len(prefix):])
            if stripped in obras_index:
                return stripped
            break

    candidates = [name for name in obras_index if name.endswith("-" + s) or name == s]
    if len(candidates) == 1:
        return candidates[0]
    return None


def kardec_url(mapping: dict, sigla_raw: str, rest: str) -> str | None:
    sigla = SIGLA_NORM.get(sigla_raw, sigla_raw)
    book = mapping["books"].get(sigla)
    if not book:
        return None
    base = mapping["_base"]

    # Introdução com item: (LE, Introdução, item IV)
    m = INTRO_IT_RE.search(rest)
    if m:
        path = book.get("intro_items", {}).get(m.group("r").upper())
        return base + path if path else None

    # Introdução sem item
    if INTRO_RE.search(rest):
        path = book.get("intro")
        return base + path if path else None

    # Capítulo (com ou sem parte): (ESE, cap. III, ...) | (C&I, 1ª parte, cap. VII, ...)
    cap_m = CAP_RE.search(rest)
    if cap_m:
        cap = cap_m.group("r").upper()
        part_m = PART_NUM_RE.search(rest)
        key = f"{part_m.group('n')}:{cap}" if part_m else cap
        path = book.get("chapters", {}).get(key)
        return base + path if path else None

    # Questão (LE): (LE, q. 990) | (LE, q. 149–164) — usa primeira do range.
    q_m = Q_RE.search(rest)
    if q_m:
        chap_key = book.get("questions", {}).get(q_m.group("n"))
        if chap_key:
            path = book.get("chapters", {}).get(chap_key)
            return base + path if path else None
    return None


def link_kardec(mapping: dict) -> callable:
    def repl(m: re.Match) -> str:
        original = m.group(0)
        url = kardec_url(mapping, m.group("sigla"), m.group("rest"))
        return f"[{original}]({url})" if url else original
    return repl


def revista_url(mapping: dict, mes_raw: str, ano_raw: str) -> str | None:
    """Resolve (RE, mês/ano) → URL.

    Estratégia:
      1. Se o mês casa com algum artigo daquele ano, retorna a URL do
         **primeiro artigo do mês** (proximidade máxima dentro do que a
         Kardecpédia expõe — não há âncora por página da revista).
      2. Caso contrário, retorna a URL do índice do ano.
    """
    ano = mapping.get("anos", {}).get(ano_raw)
    if not ano:
        return None
    mes = MONTHS_NORM.get(mes_raw.lower())
    if mes:
        for art in ano.get("artigos", []):
            if art.get("mes") == mes:
                return art.get("url") or ano.get("url")
    return ano.get("url")


def link_revista(mapping: dict | None) -> callable:
    if not mapping:
        return lambda m: m.group(0)
    def repl(m: re.Match) -> str:
        original = m.group(0)
        url = revista_url(mapping, m.group("mes"), m.group("ano"))
        return f"[{original}]({url})" if url else original
    return repl


def link_complementar(obras_index: set[str]) -> callable:
    def repl(m: re.Match) -> str:
        original = m.group(0)
        slug = resolve_obra_slug(m.group("obra"), obras_index)
        if not slug:
            return original
        # Wikilink Obsidian; o pipe preserva o texto da citação como label.
        label = original.replace("|", r"\|")
        return f"[[obras/{slug}|{label}]]"
    return repl


def transform(
    text: str,
    mapping: dict,
    obras_index: set[str],
    revista_mapping: dict | None = None,
) -> str:
    repl_kardec = link_kardec(mapping)
    repl_revista = link_revista(revista_mapping)
    repl_compl = link_complementar(obras_index)

    def dispatch(segment: str) -> str:
        # 1) Kardec Pentateuco/complementares
        segment = KARDEC_RE.sub(repl_kardec, segment)
        # 2) Revista Espírita
        segment = RE_CITE_RE.sub(repl_revista, segment)
        # 3) Complementares (após Kardec — se já virou link, está dentro de safe zone na próxima passada)
        segment = COMPL_RE.sub(repl_compl, segment)
        return segment

    out, last = [], 0
    for safe in SAFE_RE.finditer(text):
        out.append(dispatch(text[last:safe.start()]))
        out.append(safe.group(0))
        last = safe.end()
    out.append(dispatch(text[last:]))
    return "".join(out)


def process_path(
    path: Path,
    mapping: dict,
    obras_index: set[str],
    apply: bool,
    revista_mapping: dict | None = None,
) -> bool:
    """Returns True se houve mudança."""
    original = path.read_text(encoding="utf-8")
    new = transform(original, mapping, obras_index, revista_mapping)
    if new == original:
        return False
    if apply:
        path.write_text(new, encoding="utf-8")
    else:
        diff = difflib.unified_diff(
            original.splitlines(keepends=True),
            new.splitlines(keepends=True),
            fromfile=str(path), tofile=str(path) + " (linked)",
        )
        sys.stdout.writelines(diff)
    return True


def iter_md(target: Path):
    if target.is_file():
        if target.suffix == ".md":
            yield target
    else:
        yield from sorted(target.rglob("*.md"))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true", help="diff em stdout, não escreve")
    g.add_argument("--apply", action="store_true", help="escreve in-place no path")
    ap.add_argument("path", type=Path, help="arquivo .md ou diretório de conteúdo")
    ap.add_argument("--mapping", type=Path, default=DEFAULT_MAPPING)
    ap.add_argument("--revista-mapping", type=Path, default=DEFAULT_REVISTA,
                    help="mapping da Revista Espírita (json gerado por download_revista_espirita.py)")
    ap.add_argument("--obras-dir", type=Path, default=DEFAULT_OBRAS,
                    help="diretório com wiki/obras/*.md para indexar slugs")
    args = ap.parse_args(argv)

    mapping = json.loads(args.mapping.read_text(encoding="utf-8"))
    revista_mapping = (
        json.loads(args.revista_mapping.read_text(encoding="utf-8"))
        if args.revista_mapping.exists() else None
    )
    # Quando --apply em /tmp/quartz/content, obras está em <content>/wiki/obras
    obras_dir = args.obras_dir
    if not obras_dir.is_dir() and (args.path / "wiki" / "obras").is_dir():
        obras_dir = args.path / "wiki" / "obras"
    obras_index = load_obras_index(obras_dir)

    changed = 0
    total = 0
    for p in iter_md(args.path):
        total += 1
        if process_path(p, mapping, obras_index, apply=args.apply,
                        revista_mapping=revista_mapping):
            changed += 1

    verb = "modificados" if args.apply else "com mudanças pendentes"
    print(f"\n{changed}/{total} arquivos {verb}", file=sys.stderr)
    return 0 if (args.apply or changed == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
