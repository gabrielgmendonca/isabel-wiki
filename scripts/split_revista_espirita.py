#!/usr/bin/env python3
"""Particiona raw/kardec/revista-espirita/revista-espirita-YYYY.md em
arquivos mensais sob raw/kardec/revista-espirita/YYYY/MM-mes.md.

Cada arquivo mensal recebe o header do ano com o sufixo do mês, ficando
auto-contido — `Allan Kardec / **Revista Espírita…** / **Ano YYYY — Mês**`.

Default: NÃO remove o YYYY.md original. Use `--delete-yearly` para deletar
após split bem-sucedido (operação destrutiva).

Uso:
  uv run python scripts/split_revista_espirita.py             # todos os anos
  uv run python scripts/split_revista_espirita.py --year 1858 # só 1858
  uv run python scripts/split_revista_espirita.py --dry-run   # mostra plano
  uv run python scripts/split_revista_espirita.py --delete-yearly  # remove YYYY.md
"""

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RE_DIR = ROOT / "raw" / "kardec" / "revista-espirita"

MONTHS = (
    "janeiro", "fevereiro", "marco", "abril", "maio", "junho",
    "julho", "agosto", "setembro", "outubro", "novembro", "dezembro",
)
MONTH_DISPLAY = {
    "janeiro": "Janeiro", "fevereiro": "Fevereiro", "marco": "Março",
    "abril": "Abril", "maio": "Maio", "junho": "Junho",
    "julho": "Julho", "agosto": "Agosto", "setembro": "Setembro",
    "outubro": "Outubro", "novembro": "Novembro", "dezembro": "Dezembro",
}
DISPLAY_TO_SLUG = {v: k for k, v in MONTH_DISPLAY.items()}
MONTH_NUM = {m: f"{i+1:02d}" for i, m in enumerate(MONTHS)}

HEADER_END_RE = re.compile(r"^Baixado em:.*$", re.MULTILINE)
MONTH_HEAD_RE = re.compile(
    r"^## (Janeiro|Fevereiro|Março|Abril|Maio|Junho|"
    r"Julho|Agosto|Setembro|Outubro|Novembro|Dezembro)\s*$",
    re.MULTILINE,
)
YEAR_FROM_NAME_RE = re.compile(r"revista-espirita-(\d{4})\.md$")


def split_year(path: Path, *, dry_run: bool = False) -> list[Path]:
    text = path.read_text(encoding="utf-8")
    year_match = YEAR_FROM_NAME_RE.search(path.name)
    if not year_match:
        raise ValueError(f"não consegui extrair ano de {path.name}")
    year = int(year_match.group(1))

    header_match = HEADER_END_RE.search(text)
    if not header_match:
        raise ValueError(f"{path.name}: linha 'Baixado em:' não encontrada")
    blank = text.find("\n\n", header_match.end())
    if blank == -1:
        raise ValueError(f"{path.name}: linha em branco após 'Baixado em:' não encontrada")
    year_header = text[: blank + 2]

    matches = list(MONTH_HEAD_RE.finditer(text, pos=blank + 2))
    if not matches:
        raise ValueError(f"{path.name}: nenhum '## <Mês>' encontrado")

    written: list[Path] = []
    for i, m in enumerate(matches):
        mes_display = m.group(1)
        mes_slug = DISPLAY_TO_SLUG[mes_display]
        mm = MONTH_NUM[mes_slug]

        body_start = m.end()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[body_start:body_end].strip("\n")

        out_dir = RE_DIR / str(year)
        out_path = out_dir / f"{mm}-{mes_slug}.md"

        month_header = year_header.replace(
            f"**Ano {year}**",
            f"**Ano {year} — {mes_display}**",
            1,
        )
        content = f"{month_header}{body}\n"

        if not dry_run:
            out_dir.mkdir(parents=True, exist_ok=True)
            out_path.write_text(content, encoding="utf-8")
        written.append(out_path)
    return written


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--year", type=int, help="processa apenas um ano (1858–1869)")
    ap.add_argument("--dry-run", action="store_true",
                    help="mostra arquivos que seriam criados, sem escrever")
    ap.add_argument("--delete-yearly", action="store_true",
                    help="remove revista-espirita-YYYY.md após split (destrutivo)")
    args = ap.parse_args()

    years = [args.year] if args.year else list(range(1858, 1870))
    total = 0
    for y in years:
        path = RE_DIR / f"revista-espirita-{y}.md"
        if not path.exists():
            print(f"skip {y}: {path} não existe", file=sys.stderr)
            continue
        try:
            outputs = split_year(path, dry_run=args.dry_run)
        except ValueError as exc:
            print(f"erro em {y}: {exc}", file=sys.stderr)
            return 1
        suffix = " (dry-run)" if args.dry_run else ""
        print(f"{y}: {len(outputs)} arquivos{suffix}")
        total += len(outputs)
        if not args.dry_run and args.delete_yearly:
            path.unlink()
            print(f"  removido {path.name}")
    print(f"total: {total} arquivos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
