"""Utilitários compartilhados para scripts da wiki IsAbel.

Funções puras de leitura/parse usadas pelos skills `lint` e `stats`.
"""

import re
from pathlib import Path

WIKI_DIR = Path("wiki")
INDEX_PATH = Path("index.md")
LOG_PATH = Path("log.md")


def _strip_quotes(val: str) -> str:
    if len(val) >= 2 and val[0] == val[-1] and val[0] in {'"', "'"}:
        return val[1:-1]
    return val


def parse_frontmatter(path: Path) -> tuple[dict, list[str]]:
    """Extrai frontmatter YAML simples.

    Suporta: scalars, valores quoted, listas inline `[a, b]` e listas multilinha
    (`-` em linhas indentadas após chave com valor vazio).

    Retorna (fm_dict, lista_de_chaves_duplicadas).
    """
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, []
    fm: dict = {}
    duplicates: list[str] = []
    pending_key: str | None = None
    pending_list: list[str] | None = None

    def flush_pending():
        nonlocal pending_key, pending_list
        if pending_key is not None:
            if pending_key in fm:
                duplicates.append(pending_key)
            fm[pending_key] = pending_list if pending_list is not None else ""
        pending_key = None
        pending_list = None

    for line in lines[1:]:
        stripped = line.strip()
        if stripped == "---":
            break
        if pending_key is not None and stripped.startswith("- "):
            if pending_list is None:
                pending_list = []
            pending_list.append(_strip_quotes(stripped[2:].strip()))
            continue
        if not stripped:
            flush_pending()
            continue
        if ":" not in line:
            continue
        flush_pending()
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()
        if val.startswith("[") and val.endswith("]"):
            parsed = [_strip_quotes(v.strip()) for v in val[1:-1].split(",") if v.strip()]
            if key in fm:
                duplicates.append(key)
            fm[key] = parsed
        elif val == "":
            pending_key = key
            pending_list = None
        else:
            if key in fm:
                duplicates.append(key)
            fm[key] = _strip_quotes(val)
    flush_pending()
    return fm, duplicates


def strip_inline_code(text: str) -> str:
    """Substitui conteúdo de blocos ``` ``` e inline `...` por espaços.

    Preserva quebras de linha (para manter numeração) e comprimento (para manter
    offsets). Usado por parsers (wikilinks, citações) que devem ignorar trechos
    em backticks — p.ex. `[[...]]` dentro de inline code é exemplo, não link real.
    """
    def _blank(m: re.Match) -> str:
        return "".join(c if c == "\n" else " " for c in m.group(0))

    text = re.sub(r"```.*?```", _blank, text, flags=re.DOTALL)
    text = re.sub(r"`[^`\n]+`", _blank, text)
    return text


def find_wikilinks(text: str) -> list[tuple[int, str]]:
    """Retorna lista de (linha, target) para cada wikilink no texto.

    Conteúdo dentro de backticks (inline code ou blocos cercados) é ignorado.
    """
    results = []
    stripped = strip_inline_code(text)
    for i, line in enumerate(stripped.splitlines(), 1):
        for m in re.finditer(r"\[\[([^\]|#]+)", line):
            results.append((i, m.group(1).strip()))
    return results


def resolve_wikilink(link: str) -> Path:
    """Converte wikilink target em caminho de arquivo."""
    p = Path(link)
    if p.suffix != ".md":
        p = p.with_suffix(".md")
    return p


def collect_pages() -> list[Path]:
    """Retorna todos os .md dentro de wiki/."""
    return sorted(WIKI_DIR.rglob("*.md"))


def page_key(path: Path) -> str:
    """Converte Path em formato de wikilink (sem .md)."""
    return str(path.with_suffix(""))
