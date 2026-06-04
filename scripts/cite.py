#!/usr/bin/env python3
"""Extrai o texto literal de uma passagem do Pentateuco a partir da citação canônica.

Uso:
    uv run python scripts/cite.py LE "q. 150"
    uv run python scripts/cite.py LE "q. 150b"            # só subitem b
    uv run python scripts/cite.py LE "Introdução, item IV"
    uv run python scripts/cite.py LE "Conclusão, IX"
    uv run python scripts/cite.py LM "item 230"
    uv run python scripts/cite.py ESE "cap. XVII, item 4"
    uv run python scripts/cite.py "C&I" "1ª parte, cap. VI"
    uv run python scripts/cite.py "Gênese" "cap. XI, item 13"

Saída (stdout): cabeçalho com locus + path:linhas + texto literal pronto pra
colar como citação. Em locus inválido, aborta com exit code 2 (motivo na
stderr) reusando `resolve_locus` de `kardec_structure`.

Cobertura v1: LE, LM, ESE, C&I (1ª parte), Gênese. C&I 2ª parte (Exemplos —
relatos nominais sem numeração) faz dump do capítulo inteiro com aviso.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Reuso integral do parsing — não duplicar regex.
from kardec_structure import (
    OBRA_SIGLA,
    PENTATEUCO_DIR,
    MAPPING_PATH,
    _CAP_RE,
    _Q_RE,
    _INTRO_RE,
    _INTRO_IT_RE,
    _PART_NUM_RE,
    _roman_to_int,
    load_structures,
    resolve_locus,
)

SIGLA_TO_SLUG = {v: k for k, v in OBRA_SIGLA.items()}
ROOT = Path(__file__).resolve().parent.parent

# Normalização da sigla aceita pela CLI: "Genese" ↔ "Gênese".
SIGLA_INPUT_NORM = {
    "GENESE": "Genese",
    "GÊNESE": "Genese",
    "C&I": "C&I",
    "LE": "LE",
    "LM": "LM",
    "ESE": "ESE",
}

# Item dentro de capítulo / questão dentro do LE: linha começa com "N." (com
# ou sem texto depois — algumas edições quebram a linha após o número).
# As questões finais do LE (q. 1012–1019) vêm em numeração dupla
# "<nº Kardec> [<nº sequencial>]." (ex.: "1019 [1018].") porque Kardec saltou
# o nº 1011 (ver Nota dos Revisores no raw, após a q. 1012). Capturamos o
# PRIMEIRO número — o de Kardec, que é o usado nas citações canônicas.
_ITEM_RE = re.compile(r"^(\d+)(?:\s*\[\d+\])?\.\s*")

# Subitem do LE: "a) –", tolera travessões variados ou ausência.
_SUBITEM_RE = re.compile(r"^([a-z])\)\s*[–—-]?")

# Marcador de Introdução / Conclusão do LE: "**I**", "****I****", "**IX**" etc.
_BOLD_ROMAN_RE = re.compile(r"^\*+\s*([IVXLCDM]+)\s*\*+\s*$")

# Heading qualquer (`## ` ou `### `): limite natural de um bloco.
_HEADING_RE = re.compile(r"^#{2,}\s+")

# Subref "q. 150b" — captura letra do subitem se houver.
_Q_SUBITEM_RE = re.compile(r"q\.\s*(\d+)\s*([a-z])", re.IGNORECASE)

# "Conclusão, IX" / "Conclusão IX".
_CONCLUSAO_RE = re.compile(r"conclus[ãa]o[^a-z]*([IVX]+)", re.IGNORECASE)

# Item dentro de capítulo: "cap. X, item Y" / "cap. X item Y".
_CAP_ITEM_RE = re.compile(
    r"cap\.\s*[ivxlcdm]+[^,]*,?\s*item\s+(\d+)", re.IGNORECASE
)

# Para ESE/C&I/Gênese: extrair line_start/line_end de uma linha do .index.md.
# Casa "- **Capítulo XVII — ...** (linhas 2665–3049)".
_INDEX_LINE_RE = re.compile(
    r"-\s+\*\*Cap[íi]tulo\s+([IVXLCDM]+)[^\*]*\*\*\s*\(linhas\s+(\d+)[–\-](\d+)\)",
    re.IGNORECASE,
)

# Nome bonito de parte (LE).
_PART_PRETTY = {1: "Parte primeira", 2: "Parte segunda", 3: "Parte terceira", 4: "Parte quarta"}


def _read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def _rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def _le_pretty_locus(n: int) -> str:
    """'Parte segunda, Capítulo III' para `q. N`, via kardec-mapping.json."""
    data = json.loads(MAPPING_PATH.read_text(encoding="utf-8"))
    le = data.get("books", {}).get("LE", {})
    questions = le.get("questions", {})
    loc = questions.get(str(n))
    if not loc or ":" not in loc:
        return ""
    parte, cap = loc.split(":", 1)
    try:
        parte_pretty = _PART_PRETTY[int(parte)]
    except (ValueError, KeyError):
        return ""
    return f"{parte_pretty}, Capítulo {cap}"


def _find_block(lines: list[str], start_idx: int, terminators: list[re.Pattern]) -> int:
    """Acha o índice (0-based, exclusivo) onde o bloco que começa em `start_idx`
    termina. Termina ao encontrar uma linha que case qualquer dos terminators."""
    for i in range(start_idx + 1, len(lines)):
        for pat in terminators:
            if pat.match(lines[i]):
                return i
    return len(lines)


def _format(header: str, body: str) -> str:
    return f"{header}\n\n{body.rstrip()}\n"


def extract_le(ref: str) -> tuple[str, str]:
    """LE: questão, subitem, intro_item, ou conclusão."""
    md_path = PENTATEUCO_DIR / "livro-dos-espiritos.md"
    lines = _read_lines(md_path)

    # 1. Introdução, item X
    m_intro = _INTRO_IT_RE.search(ref)
    if m_intro:
        item = m_intro.group("r").upper()
        intro_start = next(
            (i for i, ln in enumerate(lines) if ln.startswith("## Introdução")), None
        )
        intro_end = next(
            (i for i, ln in enumerate(lines) if i > (intro_start or 0) and ln.startswith("## Parte ")),
            len(lines),
        )
        if intro_start is None:
            return _err_unexpected(ref)
        for i in range(intro_start + 1, intro_end):
            m = _BOLD_ROMAN_RE.match(lines[i])
            if m and m.group(1).upper() == item:
                end = _find_block(lines, i, [_BOLD_ROMAN_RE, _HEADING_RE])
                end = min(end, intro_end)
                header = f"(LE, Introdução, item {item}) — linhas {i + 1}-{end}\n{_rel(md_path)}:{i + 1}-{end}"
                body = "\n".join(lines[i:end])
                return header, body
        return _err_unexpected(ref)

    # 2. Conclusão, X
    m_conc = _CONCLUSAO_RE.search(ref)
    if m_conc:
        roman = m_conc.group(1).upper()
        # Conclusão fica depois do último "## Parte quarta" → no fim do arquivo.
        # No LE não há heading "## Conclusão" — os romanos **I**…**IX** aparecem
        # diretamente como linhas isoladas. Procurar a partir do último ~10% do arquivo.
        scan_start = int(len(lines) * 0.85)
        for i in range(scan_start, len(lines)):
            m = _BOLD_ROMAN_RE.match(lines[i])
            if m and m.group(1).upper() == roman:
                end = _find_block(lines, i, [_BOLD_ROMAN_RE, _HEADING_RE])
                header = f"(LE, Conclusão, {roman}) — linhas {i + 1}-{end}\n{_rel(md_path)}:{i + 1}-{end}"
                body = "\n".join(lines[i:end])
                return header, body
        return _err_unexpected(ref)

    # 3. q. N ou q. Nx
    m_qsub = _Q_SUBITEM_RE.search(ref)
    if m_qsub:
        n = int(m_qsub.group(1))
        subitem = m_qsub.group(2).lower()
    else:
        m_q = _Q_RE.search(ref)
        if not m_q:
            return _err_unexpected(ref)
        n = int(m_q.group("n"))
        subitem = None

    for i, ln in enumerate(lines):
        m = _ITEM_RE.match(ln)
        if m and int(m.group(1)) == n:
            end = _find_block(lines, i, [_ITEM_RE, _HEADING_RE])
            if subitem is None:
                pretty = _le_pretty_locus(n)
                loc_str = f"{pretty} — " if pretty else ""
                header = f"(LE, q. {n}) — {loc_str}linhas {i + 1}-{end}\n{_rel(md_path)}:{i + 1}-{end}"
                body = "\n".join(lines[i:end])
                return header, body
            # Subitem dentro do bloco.
            for j in range(i + 1, end):
                m_sub = _SUBITEM_RE.match(lines[j])
                if m_sub and m_sub.group(1).lower() == subitem:
                    sub_end = _find_block(lines, j, [_SUBITEM_RE, _ITEM_RE, _HEADING_RE])
                    sub_end = min(sub_end, end)
                    pretty = _le_pretty_locus(n)
                    loc_str = f"{pretty} — " if pretty else ""
                    header = f"(LE, q. {n}{subitem}) — {loc_str}linhas {j + 1}-{sub_end}\n{_rel(md_path)}:{j + 1}-{sub_end}"
                    body = "\n".join(lines[j:sub_end])
                    return header, body
            return _err(f"subitem {subitem}) não encontrado em q. {n} (linhas {i + 1}-{end})")

    if n == 1011:
        return _err(
            "q. 1011 não existe no LE: Kardec saltou esse número na numeração "
            "(Nota dos Revisores, após a q. 1012). A sequência vai q. 1010 → q. 1012; "
            "as questões finais usam numeração dupla 'Kardec [sequencial]' até q. 1019."
        )
    return _err(f"q. {n} não encontrada em {_rel(md_path)}")


def extract_lm(ref: str) -> tuple[str, str]:
    """LM: item N (numeração contínua 1–350)."""
    md_path = PENTATEUCO_DIR / "livro-dos-mediuns.md"
    lines = _read_lines(md_path)

    m_q = _Q_RE.search(ref)
    m_item = re.search(r"item\s+(\d+)", ref, re.IGNORECASE)
    n = None
    if m_q:
        n = int(m_q.group("n"))
    elif m_item:
        n = int(m_item.group(1))
    if n is None:
        return _err_unexpected(ref)

    for i, ln in enumerate(lines):
        m = _ITEM_RE.match(ln)
        if m and int(m.group(1)) == n:
            end = _find_block(lines, i, [_ITEM_RE, _HEADING_RE])
            header = f"(LM, item {n}) — linhas {i + 1}-{end}\n{_rel(md_path)}:{i + 1}-{end}"
            body = "\n".join(lines[i:end])
            return header, body
    return _err(f"item {n} não encontrado em {_rel(md_path)}")


def _find_chapter_range(index_path: Path, cap_roman: str) -> tuple[int, int] | None:
    """Lê o .index.md e devolve (line_start, line_end) do capítulo dado."""
    for line in index_path.read_text(encoding="utf-8").splitlines():
        m = _INDEX_LINE_RE.search(line)
        if m and m.group(1).upper() == cap_roman.upper():
            return int(m.group(2)), int(m.group(3))
    return None


def extract_capitulo(sigla: str, ref: str) -> tuple[str, str]:
    """ESE / C&I / Gênese: cap. X (com ou sem item Y)."""
    slug = SIGLA_TO_SLUG[sigla]
    md_path = PENTATEUCO_DIR / f"{slug}.md"
    index_path = PENTATEUCO_DIR / f"{slug}.index.md"

    m_cap = _CAP_RE.search(ref)
    if not m_cap:
        return _err_unexpected(ref)
    cap_roman = m_cap.group("r").upper()

    rng = _find_chapter_range(index_path, cap_roman)
    if rng is None:
        return _err(f"cap. {cap_roman} não localizado em {_rel(index_path)}")
    line_start, line_end = rng
    lines = _read_lines(md_path)

    m_item = _CAP_ITEM_RE.search(ref)
    if m_item:
        target = int(m_item.group(1))
        # Buscar dentro do range [line_start-1, line_end) em 0-indexed.
        for i in range(line_start - 1, min(line_end, len(lines))):
            m = _ITEM_RE.match(lines[i])
            if m and int(m.group(1)) == target:
                end_idx = _find_block(lines, i, [_ITEM_RE, _HEADING_RE])
                end_idx = min(end_idx, line_end)
                # Aviso especial para C&I 2ª parte (relatos nominais).
                warn = ""
                if sigla == "C&I" and _is_ci_segunda_parte(line_start):
                    warn = (
                        "AVISO: C&I 2ª parte usa relatos nominais; cobertura "
                        "limitada de itens numerados.\n"
                    )
                header = (
                    f"({sigla}, cap. {cap_roman}, item {target}) — "
                    f"linhas {i + 1}-{end_idx}\n{_rel(md_path)}:{i + 1}-{end_idx}"
                )
                body = warn + "\n".join(lines[i:end_idx])
                return header, body
        return _err(f"item {target} não encontrado em cap. {cap_roman} (linhas {line_start}-{line_end})")

    # Sem item: dump do capítulo inteiro.
    if sigla == "C&I" and _is_ci_segunda_parte(line_start):
        sys.stderr.write(
            "aviso: C&I 2ª parte (Exemplos) — relatos nominais sem numeração.\n"
        )
    header = (
        f"({sigla}, cap. {cap_roman}) — linhas {line_start}-{line_end}\n"
        f"{_rel(md_path)}:{line_start}-{line_end}"
    )
    body = "\n".join(lines[line_start - 1:line_end])
    return header, body


def _is_ci_segunda_parte(line_start: int) -> bool:
    """Heurística: C&I 2ª parte começa por volta da linha ~1900 (de ~3500).
    Conferir em runtime lendo o .index.md seria mais robusto mas adiciona IO."""
    return line_start > 1800


def _err(msg: str) -> tuple[str, str]:
    raise SystemExit(f"erro: {msg}")


def _err_unexpected(ref: str) -> tuple[str, str]:
    raise SystemExit(f"erro: referência não reconhecida: {ref!r}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Extrai texto literal de uma passagem do Pentateuco.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("sigla", help="LE | LM | ESE | C&I | Gênese")
    parser.add_argument("ref", help='Ex.: "q. 150", "cap. XVII, item 4", "1ª parte, cap. VI"')
    args = parser.parse_args(argv)

    sigla = SIGLA_INPUT_NORM.get(args.sigla.upper(), args.sigla)
    if sigla not in SIGLA_TO_SLUG:
        print(
            f"erro: sigla desconhecida {args.sigla!r}. Use uma de: "
            f"{', '.join(sorted(SIGLA_TO_SLUG))}",
            file=sys.stderr,
        )
        return 2

    # Validação semântica: o locus existe na obra?
    structures = load_structures()
    ok, motivo = resolve_locus(sigla, args.ref, structures[sigla])
    if not ok:
        print(
            f"erro: locus inválido em ({sigla}, {args.ref}): {motivo}. "
            f"cf. raw/kardec/pentateuco/{SIGLA_TO_SLUG[sigla]}.index.md",
            file=sys.stderr,
        )
        return 2

    try:
        if sigla == "LE":
            header, body = extract_le(args.ref)
        elif sigla == "LM":
            header, body = extract_lm(args.ref)
        else:
            header, body = extract_capitulo(sigla, args.ref)
    except SystemExit as e:
        print(str(e), file=sys.stderr)
        return 2

    sys.stdout.write(_format(header, body))
    return 0


if __name__ == "__main__":
    sys.exit(main())
