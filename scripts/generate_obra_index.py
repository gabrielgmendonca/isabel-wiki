#!/usr/bin/env python3
"""Gera _index.md para obras monolíticas em raw/.

Lê um arquivo grande (.md), identifica capítulos por padrões editoriais
(`Capítulo I`, `Primeira parte`, `Livro Primeiro`...) e escreve um índice
com título, range de linhas e primeira sentença de cada seção.

O objetivo é permitir que o agente consulte o índice (~100 linhas) antes
de decidir ler o arquivo monolítico (5K-12K linhas) por inteiro. Combina
com `mcp__qmd__get <arquivo>:<offset>` para leitura por offset.

Uso:
    uv run python scripts/generate_obra_index.py raw/kardec/pentateuco/livro-dos-mediuns.md

O destino é `<dir>/<basename>.index.md` ao lado do arquivo de entrada — múltiplas obras no mesmo diretório (ex.: pentateuco) não colidem.
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

# Padrões de capítulo: começam com `## ` seguido de um marcador estrutural.
# Ordem importa: tentamos identificar PARTES (mais grossas) e CAPÍTULOS.
PART_RE = re.compile(
    r"^##\s+("
    r"(?:Primeira|Segunda|Terceira|Quarta|Quinta|Sexta|Sétima|Oitava|Nona|Décima)"
    r"\s+parte"
    r"|Parte\s+[IVXLCDM]+"
    r"|Livro\s+(?:primeiro|segundo|terceiro|quarto|quinto)"
    r"|Prolegômenos"
    r"|Introdução"
    r")\b",
    re.IGNORECASE,
)
CHAPTER_RE = re.compile(
    r"^##\s+("
    r"Capítulo\s+[IVXLCDM]+"
    r"|Cap\.\s+[IVXLCDM]+"
    r")\b",
    re.IGNORECASE,
)


@dataclass
class Section:
    level: str  # "part" or "chapter"
    title: str
    line_start: int  # 1-indexed
    line_end: int = 0  # 1-indexed inclusive, filled later
    first_sentence: str = ""


def first_sentence(lines: list[str], start_idx: int, end_idx: int) -> str:
    """Pega a primeira sentença de conteúdo após o heading.

    Concatena linhas curtas (números de questão isolados como "82.", chamadas
    em uma palavra como "Fundada") até acumular ≥60 chars de texto, depois
    extrai a primeira sentença completa. Evita primeiras-sentenças degeneradas
    como "82." ou "I" causadas por quebras editoriais do markdown extraído.
    """
    buffer: list[str] = []
    for line in lines[start_idx:end_idx]:
        stripped = line.strip()
        if not stripped:
            if buffer:
                # Parágrafo terminou; se já temos texto suficiente, usar.
                joined = " ".join(buffer)
                if len(joined) >= 40:
                    break
            continue
        if stripped.startswith("#"):
            continue
        cleaned = re.sub(r"[*_`]", "", stripped)
        buffer.append(cleaned)
        joined = " ".join(buffer)
        if len(joined) >= 60:
            break

    if not buffer:
        return ""

    text = " ".join(buffer)
    # Primeira sentença completa: 30-200 chars, terminando em . ? ! :
    match = re.search(r"^(.{30,200}?[.?!:])(\s|$)", text)
    if match:
        return match.group(1).strip()
    # Fallback: trunca em ~150 chars.
    if len(text) > 150:
        return text[:147].rstrip() + "..."
    return text


def parse_sections(lines: list[str]) -> list[Section]:
    sections: list[Section] = []
    for i, line in enumerate(lines):
        if PART_RE.match(line):
            title = line.lstrip("#").strip()
            sections.append(Section(level="part", title=title, line_start=i + 1))
        elif CHAPTER_RE.match(line):
            title = line.lstrip("#").strip()
            sections.append(Section(level="chapter", title=title, line_start=i + 1))

    # Preencher line_end com o início da próxima seção - 1, ou fim do arquivo.
    for idx, section in enumerate(sections):
        if idx + 1 < len(sections):
            section.line_end = sections[idx + 1].line_start - 1
        else:
            section.line_end = len(lines)

    # Preencher first_sentence.
    for section in sections:
        section.first_sentence = first_sentence(lines, section.line_start, section.line_end)

    return sections


def detect_obra_title(lines: list[str]) -> str:
    """Tenta extrair o título da obra das primeiras linhas."""
    for line in lines[:20]:
        stripped = line.strip()
        if stripped.startswith("## ") and not PART_RE.match(line) and not CHAPTER_RE.match(line):
            return stripped.lstrip("#").strip()
    return "Obra"


def render_index(input_path: Path, lines: list[str], sections: list[Section]) -> str:
    title = detect_obra_title(lines)
    rel_path = input_path.relative_to(input_path.parents[3]) if len(input_path.parents) >= 4 else input_path
    total_lines = len(lines)

    out: list[str] = []
    out.append(f"# Índice — {title}")
    out.append("")
    out.append(
        "> Pré-resumo gerado por `scripts/generate_obra_index.py`. "
        "Para ler um capítulo específico sem carregar o arquivo todo, usar "
        f"`mcp__qmd__get {rel_path.as_posix()}:<linha-inicial>-<linha-final>`."
    )
    out.append("")
    out.append(f"**Arquivo**: `{rel_path.as_posix()}` ({total_lines} linhas, {len(sections)} seções)")
    out.append("")
    out.append("## Estrutura")
    out.append("")

    current_part: str | None = None
    has_parts = any(s.level == "part" for s in sections)

    for section in sections:
        if section.level == "part":
            current_part = section.title
            out.append(f"### {section.title}")
            out.append(f"_Linhas {section.line_start}–{section.line_end}_")
            if section.first_sentence:
                out.append("")
                out.append(section.first_sentence)
            out.append("")
        else:
            indent = "" if has_parts else ""
            line = (
                f"{indent}- **{section.title}** "
                f"(linhas {section.line_start}–{section.line_end})"
            )
            if section.first_sentence:
                line += f" — {section.first_sentence}"
            out.append(line)

    out.append("")
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Arquivo .md em raw/")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Imprime no stdout em vez de escrever _index.md",
    )
    args = parser.parse_args(argv)

    input_path: Path = args.input.resolve()
    if not input_path.is_file():
        print(f"erro: {input_path} não é arquivo", file=sys.stderr)
        return 1

    lines = input_path.read_text(encoding="utf-8").splitlines()
    sections = parse_sections(lines)

    if not sections:
        print(
            f"aviso: nenhuma seção identificada em {input_path}. "
            "O regex cobre 'Capítulo X', 'Primeira parte', 'Parte I', "
            "'Livro primeiro', 'Prolegômenos', 'Introdução'.",
            file=sys.stderr,
        )
        return 2

    rendered = render_index(input_path, lines, sections)

    if args.dry_run:
        sys.stdout.write(rendered)
        return 0

    output_path = input_path.with_suffix(".index.md")
    output_path.write_text(rendered, encoding="utf-8")
    print(f"escrito: {output_path} ({len(sections)} seções)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
