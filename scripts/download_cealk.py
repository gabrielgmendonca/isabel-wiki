#!/usr/bin/env python3
"""Baixa o acervo PDF do CEAK (Centro Espírita Allan Kardec) para `raw/`.

Fonte: https://extras.ceallankardec.org.br/livros.html (356 PDFs catalogados).
Consome `data/cealk-catalogo.json` (gerado pelo scrape inicial) — cada entrada
traz titulo, url, autor_slug, scope, slug e dest_pdf canônico.

Layout resultante (exemplos):
  raw/kardec/pentateuco/livro-dos-espiritos.pdf
  raw/kardec/complementares/o-que-e-o-espiritismo.pdf
  raw/autores/leon-denis/depois-da-morte.pdf
  raw/mediuns/chico-xavier/emmanuel/paulo-e-estevao.pdf
  raw/mediuns/divaldo-franco/manoel-philomeno-de-miranda/<obra>.pdf

CLI:
  uv run python scripts/download_cealk.py               # baixa tier 1-4 faltantes
  uv run python scripts/download_cealk.py --dry-run     # só lista
  uv run python scripts/download_cealk.py --tier 1 2 3  # filtra por tier
  uv run python scripts/download_cealk.py --only cairbar # filtra autor_slug
  uv run python scripts/download_cealk.py --force       # re-baixa existentes

Idempotência:
  - Pula se o arquivo destino existe (a menos que --force).
  - Pula entradas marcadas `exists: true` no JSON (match heurístico contra
    raw/ feito no scrape) — exceto se --include-matched.

Exit: 0 se todos baixaram ou foram pulados; 1 se houve falhas.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
UA = "isabel-wiki/download-cealk"

# Mesma classificação usada na geração de OBRAS-PENDENTES-CEALK.md.
TIER: dict[str, int] = {
    # tier 1 (Pentateuco)
    "allan-kardec/kardec-pentateuco": 1,
    # tier 2 (Kardec complementar)
    "allan-kardec/kardec-complementares": 2,
    "allan-kardec/kardec-biografias": 2,
    "allan-kardec/kardec-revista": 2,
    # tier 3 (consagrados)
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
    # tier 4 (secundários)
    "herculano-pires/autor": 4,
    "ernesto-bozzano/autor": 4,
    "herminio-correa-de-miranda/autor": 4,
    "canuto-abreu/autor": 4,
    "inacio-ferreira/autor": 4,
    "carlos-alberto-baccelli/medium:inacio-ferreira": 4,
    "feb/estudos-feb": 4,
    # tier 9 (ambíguo — fora da hierarquia oficial; opt-in via --tier 9)
    "pietro-ubaldi/autor": 9,
    "edgard-armond/autor": 9,
    "eduardo-penna/autor": 9,
    "hernani-guimaraes-de-andrade/autor": 9,
}


def tier_for(rec: dict) -> int:
    key = f"{rec['autor_slug']}/{rec['scope']}"
    return TIER.get(key, 5)


def download(url: str, dest: Path, *, delay: float, ua: str) -> int:
    """Stream-download. Retorna bytes escritos. Cria pais."""
    if delay:
        time.sleep(delay)
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    with requests.get(url, stream=True, timeout=120, headers={"User-Agent": ua}) as r:
        r.raise_for_status()
        written = 0
        with tmp.open("wb") as fh:
            for chunk in r.iter_content(chunk_size=64 * 1024):
                if chunk:
                    fh.write(chunk)
                    written += len(chunk)
    tmp.replace(dest)
    return written


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--catalog",
        type=Path,
        default=ROOT / "data" / "cealk-catalogo.json",
        help="JSON do catálogo (default: data/cealk-catalogo.json)",
    )
    ap.add_argument(
        "--tier",
        nargs="+",
        type=int,
        default=[1, 2, 3, 4],
        help="tiers a baixar (default: 1 2 3 4; tier 9 = ambíguo, opt-in)",
    )
    ap.add_argument(
        "--only", help="substring (case-insensitive) p/ filtrar autor_slug ou titulo"
    )
    ap.add_argument(
        "--include-matched",
        action="store_true",
        help="inclui entradas marcadas exists:true (re-checa por path)",
    )
    ap.add_argument(
        "--force", action="store_true", help="re-baixa mesmo se path destino existe"
    )
    ap.add_argument(
        "--dry-run", action="store_true", help="só lista; não baixa nada"
    )
    ap.add_argument(
        "--delay", type=float, default=0.3, help="delay entre requisições (s)"
    )
    args = ap.parse_args(argv)

    if not args.catalog.exists():
        print(f"erro: catálogo não encontrado: {args.catalog}", file=sys.stderr)
        return 2

    records = json.loads(args.catalog.read_text(encoding="utf-8"))
    print(f"[catalog] {len(records)} entradas em {args.catalog.relative_to(ROOT)}",
          file=sys.stderr)

    # Filtros
    tier_set = set(args.tier)
    selected: list[dict] = []
    for r in records:
        t = tier_for(r)
        if t not in tier_set:
            continue
        if not args.include_matched and r.get("exists"):
            continue
        if args.only:
            needle = args.only.lower()
            if (
                needle not in r["autor_slug"].lower()
                and needle not in r["titulo"].lower()
                and needle not in r["scope"].lower()
            ):
                continue
        selected.append(r)

    print(
        f"[filter] tiers={sorted(tier_set)} only={args.only!r} "
        f"→ {len(selected)} candidato(s)",
        file=sys.stderr,
    )

    new_bytes = 0
    skipped_exists = 0
    failed: list[tuple[str, str]] = []
    downloaded = 0

    for i, r in enumerate(selected, 1):
        dest = ROOT / r["dest_pdf"]
        rel = dest.relative_to(ROOT)
        if dest.exists() and not args.force:
            print(f"  [{i}/{len(selected)}] já existe: {rel}", file=sys.stderr)
            skipped_exists += 1
            continue
        if args.dry_run:
            print(f"  [{i}/{len(selected)}] DRY → {r['url']} → {rel}", file=sys.stderr)
            continue
        print(
            f"  [{i}/{len(selected)}] {r['autor_slug']}/{r['slug']}.pdf "
            f"← {r['url']}",
            file=sys.stderr,
        )
        try:
            written = download(r["url"], dest, delay=args.delay, ua=UA)
            new_bytes += written
            downloaded += 1
            print(f"    {written:,} B", file=sys.stderr)
        except requests.RequestException as exc:
            print(f"    ! falha: {exc}", file=sys.stderr)
            failed.append((r["titulo"], r["url"]))

    print(
        f"\nresumo: {downloaded} baixado(s) · {skipped_exists} já presente(s) · "
        f"{len(failed)} falha(s) · {new_bytes:,} B novos",
        file=sys.stderr,
    )
    if failed:
        print("falhas:", file=sys.stderr)
        for t, u in failed:
            print(f"  - {t} ({u})", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
