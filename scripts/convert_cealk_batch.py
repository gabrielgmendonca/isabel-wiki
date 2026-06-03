#!/usr/bin/env python3
"""Converte todos os PDFs do catálogo CEAK para Markdown em lote.

Consome `data/cealk-catalogo.json` e, para cada entrada cujo PDF está
presente em raw/ e cujo .md correspondente NÃO existe, invoca
`scripts/convert_pdf_to_md.sh` (marker via uv).

Checkpoint natural: a próxima execução pula o que já virou .md. Se o
processo for interrompido no meio de um arquivo, o .part residual do
marker é descartado (script `convert_pdf_to_md.sh` usa mktemp).

CLI:
  uv run python scripts/convert_cealk_batch.py            # processa tudo pendente
  uv run python scripts/convert_cealk_batch.py --dry-run  # só lista
  uv run python scripts/convert_cealk_batch.py --tier 1 2 3
  uv run python scripts/convert_cealk_batch.py --only cairbar
  uv run python scripts/convert_cealk_batch.py --max-pages 400  # pula PDFs > N páginas

Progresso: linhas em /tmp/cealk-convert.log (passar tee externamente se
quiser também no stdout).
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONVERT_SH = ROOT / "scripts" / "convert_pdf_to_md.sh"

# Espelho da classificação usada em download_cealk.py
TIER: dict[str, int] = {
    "allan-kardec/kardec-pentateuco": 1,
    "allan-kardec/kardec-complementares": 2,
    "allan-kardec/kardec-biografias": 2,
    "allan-kardec/kardec-revista": 2,
    "leon-denis/autor": 3,
    "gabriel-delanne/autor": 3,
    "cairbar-schutel/autor": 3,
    "bezerra-de-menezes/autor": 3,
    "pedro-de-camargo/autor": 3,
    "chico-xavier/medium:andre-luiz": 3,
    "chico-xavier/medium:emmanuel": 3,
    "chico-xavier/medium:humberto-de-campos": 3,
    "chico-xavier/medium:irmao-x": 3,
    "divaldo-franco/medium:joanna-de-angelis": 3,
    "divaldo-franco/medium:manoel-philomeno-de-miranda": 3,
    "camille-flammarion/autor": 3,
    "arthur-conan-doyle/autor": 3,
    "herculano-pires/autor": 4,
    "ernesto-bozzano/autor": 4,
    "herminio-correa-de-miranda/autor": 4,
    "canuto-abreu/autor": 4,
    "inacio-ferreira/autor": 4,
    "carlos-alberto-baccelli/medium:inacio-ferreira": 4,
    "feb/estudos-feb": 4,
    "pietro-ubaldi/autor": 9,
    "edgard-armond/autor": 9,
    "eduardo-penna/autor": 9,
    "hernani-guimaraes-de-andrade/autor": 9,
}


def pdf_page_count(pdf: Path) -> int | None:
    try:
        out = subprocess.check_output(
            ["pdfinfo", str(pdf)], stderr=subprocess.DEVNULL, text=True
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
    for line in out.splitlines():
        if line.startswith("Pages:"):
            try:
                return int(line.split(":", 1)[1].strip())
            except ValueError:
                return None
    return None


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--catalog",
        type=Path,
        default=ROOT / "data" / "cealk-catalogo.json",
    )
    ap.add_argument(
        "--tier", nargs="+", type=int, default=[1, 2, 3, 4],
    )
    ap.add_argument("--only", help="substring p/ filtrar autor_slug/scope/titulo")
    ap.add_argument(
        "--max-pages", type=int, default=None,
        help="pula PDFs maiores que N páginas (default: sem limite)",
    )
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    if not args.catalog.exists():
        print(f"erro: catálogo {args.catalog} ausente", file=sys.stderr)
        return 2
    if not CONVERT_SH.exists():
        print(f"erro: {CONVERT_SH} ausente", file=sys.stderr)
        return 2

    records = json.loads(args.catalog.read_text(encoding="utf-8"))
    tier_set = set(args.tier)

    pending: list[tuple[Path, Path, int | None, dict]] = []
    skipped_no_pdf = 0
    skipped_done = 0
    skipped_oversize = 0
    skipped_filter = 0
    for r in records:
        key = f"{r['autor_slug']}/{r['scope']}"
        t = TIER.get(key, 5)
        if t not in tier_set:
            skipped_filter += 1
            continue
        if args.only:
            needle = args.only.lower()
            if (
                needle not in r["autor_slug"].lower()
                and needle not in r["scope"].lower()
                and needle not in r["titulo"].lower()
            ):
                skipped_filter += 1
                continue
        pdf = ROOT / r["dest_pdf"]
        md = pdf.with_suffix(".md")
        if not pdf.exists():
            skipped_no_pdf += 1
            continue
        if md.exists() and md.stat().st_size > 0:
            skipped_done += 1
            continue
        pages = pdf_page_count(pdf)
        if args.max_pages is not None and pages is not None and pages > args.max_pages:
            skipped_oversize += 1
            continue
        pending.append((pdf, md, pages, r))

    total_pages = sum(p[2] or 0 for p in pending)
    print(
        f"[plan] tiers={sorted(tier_set)} only={args.only!r} "
        f"max_pages={args.max_pages}",
        file=sys.stderr,
    )
    print(
        f"[plan] pendentes: {len(pending)} PDFs · {total_pages:,} páginas total · "
        f"~{total_pages * 6 // 60} min @6s/pág",
        file=sys.stderr,
    )
    print(
        f"[plan] pulados: {skipped_done} já-convertidos · "
        f"{skipped_no_pdf} sem-PDF · {skipped_oversize} >max-pages · "
        f"{skipped_filter} filtro",
        file=sys.stderr,
    )

    if args.dry_run:
        for pdf, md, pages, r in pending:
            print(
                f"  DRY [{pages or '?':>4}p] {pdf.relative_to(ROOT)} → "
                f"{md.relative_to(ROOT)}",
                file=sys.stderr,
            )
        return 0

    ok = 0
    failed: list[tuple[Path, str]] = []
    t_start = time.time()
    for i, (pdf, md, pages, r) in enumerate(pending, 1):
        elapsed = time.time() - t_start
        rate = (sum(p[2] or 0 for p in pending[:i-1])) / max(elapsed, 1)
        print(
            f"\n[{i}/{len(pending)}] {pdf.relative_to(ROOT)} ({pages or '?'}p) "
            f"— elapsed {elapsed/60:.1f}min",
            file=sys.stderr,
        )
        # Invoca o conversor canônico. Captura stdout/stderr para o log.
        try:
            res = subprocess.run(
                [str(CONVERT_SH), str(pdf)],
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
            if res.returncode != 0:
                tail = "\n".join(res.stdout.strip().splitlines()[-10:])
                print(f"  ✗ falha (rc={res.returncode})\n{tail}", file=sys.stderr)
                failed.append((pdf, f"rc={res.returncode}"))
                continue
            if not md.exists() or md.stat().st_size == 0:
                print(f"  ✗ marker não produziu {md.name}", file=sys.stderr)
                failed.append((pdf, "no output"))
                continue
            print(
                f"  ✓ {md.stat().st_size:,} B → {md.relative_to(ROOT)}",
                file=sys.stderr,
            )
            ok += 1
        except KeyboardInterrupt:
            print("\n[abort] interrompido — checkpoint salvo, retomar com mesmo cmd",
                  file=sys.stderr)
            return 130
        except Exception as exc:
            print(f"  ✗ exceção: {exc}", file=sys.stderr)
            failed.append((pdf, str(exc)))

    elapsed = time.time() - t_start
    print(
        f"\n=== resumo ===\n"
        f"  convertidos: {ok}/{len(pending)}\n"
        f"  falhas:      {len(failed)}\n"
        f"  tempo total: {elapsed/60:.1f} min\n",
        file=sys.stderr,
    )
    if failed:
        print("falhas:", file=sys.stderr)
        for pdf, why in failed:
            print(f"  - {pdf.relative_to(ROOT)}: {why}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
