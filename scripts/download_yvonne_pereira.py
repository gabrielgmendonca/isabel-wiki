#!/usr/bin/env python3
"""Baixa o catálogo de Yvonne do Amaral Pereira de Portal do Espírito.

Fonte: https://files.comunidades.net/portaldoespirito/ — repositório PHP
sem listagem de diretório. As URLs foram descobertas pesquisa-a-pesquisa
(maio/2026) e validadas com Range GET. 14 dos 17 títulos do catálogo FEB
estão presentes ali; 3 ficam fora (ver MISSING_TITLES).

Por que script próprio (não usar `download_espiritualidades_autor.py`):
  espiritualidades.com.br lista Yvonne Pereira só sob o espírito autor
  (`BOTELHO_Camilo_..._et_PEREIRA_Yvonne_tit_Memorias_de_um_suicida`), e
  com apenas 1 obra. O repositório dela está em outro host (Portal do
  Espírito), sem índice — daí a tabela hard-coded abaixo.

Destino: raw/autores/yvonne-pereira/<slug>.pdf

CLI:
  uv run python scripts/download_yvonne_pereira.py            # baixa tudo
  uv run python scripts/download_yvonne_pereira.py --dry-run  # só lista
  uv run python scripts/download_yvonne_pereira.py --force    # re-baixa
  uv run python scripts/download_yvonne_pereira.py --only memorias  # filtra
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from _slug import slugify  # noqa: E402

UA = "isabel-wiki/download-yvonne-pereira"

# (titulo, url) — titulo vira o slug do arquivo (.pdf), url é o que baixa.
# Ordenado por ano de publicação para casar com a lista em
# wiki/personalidades/yvonne-pereira.md.
WORKS: list[tuple[str, str]] = [
    ("Memórias de um Suicida",
     "https://files.comunidades.net/portaldoespirito/Memorias_de_um_Suicida_1954.pdf"),
    ("Amor e Ódio",
     "https://files.comunidades.net/portaldoespirito/Amor_e_Odio_1956.pdf"),
    ("A Tragédia de Santa Maria",
     "https://files.comunidades.net/portaldoespirito/A_Tragedia_de_Santa_Maria_1957.pdf"),
    ("Nas Voragens do Pecado",
     "https://files.comunidades.net/portaldoespirito/Nas_Voragens_do_Pecado_1960.pdf"),
    ("Ressurreição e Vida",
     "https://files.comunidades.net/portaldoespirito/Ressurreicao_e_Vida_(1963).pdf"),
    ("Devassando o Invisível",
     "https://files.comunidades.net/portaldoespirito/Devassando_o_Invisivel_1964.pdf"),
    ("Dramas da Obsessão",
     "https://files.comunidades.net/portaldoespirito/Dramas_da_Obsessao_1964.pdf"),
    ("Recordações da Mediunidade",
     "https://files.comunidades.net/portaldoespirito/Recordacoes_da_Mediunidade_1968.pdf"),
    ("A Família Espírita",
     "https://files.comunidades.net/portaldoespirito/A_Familia_Espirita_(1973).pdf"),
    ("O Cavaleiro de Numiers",
     "https://files.comunidades.net/portaldoespirito/O_Cavaleiro_de_Numiers_1973.pdf"),
    ("O Drama da Bretanha",
     "https://files.comunidades.net/portaldoespirito/O_Drama_da_Bretanha_1973.pdf"),
    ("Sublimação",
     "https://files.comunidades.net/portaldoespirito/Sublimacao_1973.pdf"),
    ("À Luz do Consolador",
     "https://files.comunidades.net/portaldoespirito/A_Luz_do_Consolador_(1979).pdf"),
    ("As Três Revelações",
     "https://files.comunidades.net/portaldoespirito/As_Tres_Revelacoes_(1979).pdf"),
    # Biografia (não é obra dela, mas é o índice do catálogo no portal)
    ("Biografia - Vidas Passadas",
     "https://files.comunidades.net/portaldoespirito/0_-_BIOGRAFIA_-_Vidas_Passadas_por_Yvonne_do_Amaral_Pereira.pdf"),
]

# Títulos do catálogo FEB que NÃO estão em portaldoespirito (probed em maio/2026
# com várias variantes de ano e capitalização — todos 404). Buscar manualmente
# se for ingerir; provavelmente em scribd/lelivros/pdfcoffee.
MISSING_TITLES: list[str] = [
    "Nas Telas do Infinito",
    "Contos Amigos",
    "Evangelho aos Simples",
]


def download(url: str, dest: Path, *, delay: float) -> int:
    if delay:
        time.sleep(delay)
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    with requests.get(url, stream=True, timeout=60, headers={"User-Agent": UA}) as r:
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
    ap.add_argument("--out-dir", type=Path,
                    help="default: raw/autores/yvonne-pereira/")
    ap.add_argument("--only",
                    help="substring (case-insensitive) para filtrar títulos")
    ap.add_argument("--dry-run", action="store_true",
                    help="lista o que seria baixado; não baixa nada")
    ap.add_argument("--force", action="store_true",
                    help="re-baixa mesmo se o arquivo já existir")
    ap.add_argument("--delay", type=float, default=0.5,
                    help="delay entre downloads (default: 0.5s)")
    args = ap.parse_args(argv)

    out_dir = args.out_dir or (ROOT / "raw" / "autores" / "yvonne-pereira")

    works = WORKS
    if args.only:
        needle = args.only.lower()
        # Match contra título E slug — `--only memorias` casa com "Memórias…".
        works = [(t, u) for (t, u) in WORKS
                 if needle in t.lower() or needle in slugify(t)]
        if not works:
            print(f"erro: --only {args.only!r} não casou com nenhum título",
                  file=sys.stderr)
            return 2

    print(f"[catálogo] {len(works)} obra(s) — destino: "
          f"{out_dir.relative_to(ROOT) if ROOT in out_dir.parents else out_dir}",
          file=sys.stderr)

    new_bytes = 0
    skipped = 0
    failed: list[tuple[str, str]] = []

    for i, (titulo, url) in enumerate(works, 1):
        slug = slugify(titulo)
        dest = out_dir / f"{slug}.pdf"
        rel = dest.relative_to(ROOT) if ROOT in dest.parents else dest
        print(f"[{i}/{len(works)}] {titulo}", file=sys.stderr)

        if args.dry_run:
            print(f"  → {url}", file=sys.stderr)
            print(f"  → {rel}", file=sys.stderr)
            continue
        if dest.exists() and not args.force:
            print(f"  já existe: {rel} ({dest.stat().st_size:,} B)",
                  file=sys.stderr)
            skipped += 1
            continue

        try:
            written = download(url, dest, delay=args.delay)
            new_bytes += written
            print(f"  baixado: {rel} ({written:,} B)", file=sys.stderr)
        except Exception as exc:  # noqa: BLE001
            print(f"  ! falha: {exc}", file=sys.stderr)
            failed.append((titulo, url))

    print("", file=sys.stderr)
    print(
        f"resumo: {len(works)} descoberta(s); {skipped} já presente(s); "
        f"{len(failed)} falha(s); {new_bytes:,} B novos",
        file=sys.stderr,
    )
    if MISSING_TITLES and not args.only:
        print("", file=sys.stderr)
        print(f"NÃO encontrados em portaldoespirito ({len(MISSING_TITLES)} obra(s) — "
              f"buscar manualmente):", file=sys.stderr)
        for t in MISSING_TITLES:
            print(f"  - {t}", file=sys.stderr)
    if failed:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
