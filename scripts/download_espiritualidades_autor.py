#!/usr/bin/env python3
"""Baixa PDFs de um autor em espiritualidades.com.br.

Pipeline:
  1. Fetch  https://www.espiritualidades.com.br/Artigos/Art_Sumarios/Sumario_Autores_<L>.htm
  2. Filtra links cujo filename bate `<SURNAME>_<Firstname>_tit_*.htm`
     (matching insensível a acentos — `Léon` casa com `DENIS_Leon_tit_*`).
  3. Para cada página de obra, procura o primeiro `<a href="*.pdf">`.
  4. Baixa para `raw/autores/<author-slug>/<titulo-slug>.pdf`.

Layout resultante (espelha `raw/autores/leon-denis/*.pdf`):
  raw/autores/camille-flammarion/
    ├── as-casas-mal-assombradas.pdf
    ├── deus-na-natureza.pdf
    └── …

CLI (uso típico):
  uv run python scripts/download_espiritualidades_autor.py \
      --author "Camille Flammarion"                # baixa tudo
  uv run python scripts/download_espiritualidades_autor.py \
      --surname FLAMMARION --firstname Camille     # equivalente, forma longa
  uv run python scripts/download_espiritualidades_autor.py \
      --author "Camille Flammarion" --dry-run      # só lista (não baixa)
  uv run python scripts/download_espiritualidades_autor.py \
      --author "Camille Flammarion" --only casas   # filtra por substring
  uv run python scripts/download_espiritualidades_autor.py \
      --author "Camille Flammarion" --force        # re-baixa mesmo se existe
  uv run python scripts/download_espiritualidades_autor.py \
      --author "Camille Flammarion" --letter F     # override (se inferência falhar)
  uv run python scripts/download_espiritualidades_autor.py \
      --author "Camille Flammarion" --out-dir /tmp/test  # destino alternativo

Idempotência:
  - HTML fica cacheado em /tmp/espiritualidades-cache/ (apaga essa pasta
    para forçar re-discovery; rodar de novo é barato).
  - PDFs já presentes no destino são pulados — use --force para sobrescrever.

Exit codes:
  0 = sucesso (todas obras baixadas ou já presentes)
  1 = nenhuma obra encontrada OU houve falhas de download
  2 = erro de argumento

Limitações conhecidas:
  - Sobrenomes compostos com espaço (ex.: "Espírito Santo Neto") NÃO são
    suportados pelo atalho --author; nesse caso use --surname/--firstname
    diretamente, ou consulte a página Sumario_Autores_<L>.htm para ver
    a grafia exata do filename.
  - O site às vezes lista a obra apenas em .doc/.html (sem PDF). Essas
    aparecem em "sem PDF" no resumo, sem causar erro.
  - O site tem typos ocasionais nos filenames (ex.: Léon Denis aparece como
    `DENNIS_Leon_tit_*` com NN duplo). Quando o script não encontra obras,
    ele sugere sobrenomes parecidos do mesmo sumário — re-rode com a grafia
    que o site realmente usa: `--surname DENNIS --firstname Leon`.
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import re
import sys
import time
import unicodedata
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from _slug import slugify  # noqa: E402

BASE = "https://www.espiritualidades.com.br"
UA = "isabel-wiki/download-espiritualidades-autor"
CACHE_DIR = Path("/tmp/espiritualidades-cache")


def strip_accents(s: str) -> str:
    """Remove diacríticos preservando case e símbolos.

    Diferente de `_slug.slugify`, que também lowercase e troca não-alfanum
    por '-'. Aqui só queremos `Léon` → `Leon` para matching contra filenames
    como `DENIS_Leon_tit_*.htm`.
    """
    return "".join(
        c for c in unicodedata.normalize("NFKD", s)
        if not unicodedata.combining(c)
    )


def cache_path(url: str) -> Path:
    slug = re.sub(r"[^a-z0-9]+", "_", url.lower()).strip("_")
    if len(slug) > 200:
        digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:10]
        slug = f"{slug[:180]}_{digest}"
    return CACHE_DIR / f"{slug}.html"


def fetch_html(url: str, *, delay: float = 0.0) -> str:
    cp = cache_path(url)
    if cp.exists():
        return cp.read_text(encoding="utf-8", errors="replace")
    if delay:
        time.sleep(delay)
    r = requests.get(url, timeout=30, headers={"User-Agent": UA})
    r.raise_for_status()
    # Tentar detectar encoding; o site usa iso-8859-1 historicamente.
    if r.encoding is None or r.encoding.lower() == "iso-8859-1":
        try:
            text = r.content.decode("iso-8859-1")
        except UnicodeDecodeError:
            text = r.text
    else:
        text = r.text
    cp.parent.mkdir(parents=True, exist_ok=True)
    cp.write_text(text, encoding="utf-8")
    return text


def list_surnames_in_sumario(html: str) -> list[str]:
    """Lista sobrenomes (parte antes do `_Firstname_tit_`) que aparecem no sumário.

    Útil para sugerir grafias quando a busca volta vazia — o site às vezes
    tem typos (ex.: `DENNIS_Leon` em vez de `DENIS_Leon`).
    """
    soup = BeautifulSoup(html, "html.parser")
    rx = re.compile(r"^([A-ZÀ-Ý]+)_[A-Za-zÀ-ÿ]+_tit_", re.IGNORECASE)
    out: set[str] = set()
    for a in soup.find_all("a", href=True):
        fname = Path(unquote(urlparse(a["href"]).path)).name
        m = rx.match(fname)
        if m:
            out.add(m.group(1).upper())
    return sorted(out)


def find_author_book_pages(
    html: str, *, surname: str, firstname: str, sumario_url: str,
) -> list[tuple[str, str]]:
    """Retorna [(titulo, url_absoluta)] das obras do autor no sumário.

    Padrão observado: `../F_autores/SURNAME_Firstname_tit_<Titulo>.htm`.
    """
    soup = BeautifulSoup(html, "html.parser")
    # Matching insensível a acentos: o site grava filenames sem diacríticos
    # (`DENIS_Leon_tit_*.htm`) mesmo quando o autor é `Léon Denis`.
    prefix = strip_accents(f"{surname}_{firstname}_tit_")
    seen: set[str] = set()
    found: list[tuple[str, str]] = []
    for a in soup.find_all("a", href=True):
        href: str = a["href"]
        # filtramos pelo nome do arquivo (sem path)
        fname = Path(unquote(urlparse(href).path)).name
        fname_ascii = strip_accents(fname)
        if not fname_ascii.startswith(prefix) or not fname_ascii.endswith(".htm"):
            continue
        abs_url = urljoin(sumario_url, href)
        if abs_url in seen:
            continue
        seen.add(abs_url)
        titulo = re.sub(r"\s+", " ", a.get_text(" ", strip=True)) or fname
        found.append((titulo, abs_url))
    return found


def find_pdf_url(html: str, *, page_url: str) -> str | None:
    """Procura o link `.pdf` na página da obra. Retorna URL absoluta ou None."""
    soup = BeautifulSoup(html, "html.parser")
    for a in soup.find_all("a", href=True):
        href: str = a["href"]
        if ".pdf" not in href.lower():
            continue
        # ignora âncoras vazias e mailtos
        if href.startswith("#") or href.lower().startswith("mailto:"):
            continue
        return urljoin(page_url, href)
    return None


def download_pdf(url: str, dest: Path, *, delay: float = 0.0) -> int:
    """Baixa stream para `dest`. Retorna bytes gravados. Cria pais se preciso."""
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


def pdf_dest(out_dir: Path, pdf_url: str, *, titulo: str) -> Path:
    """Decide o nome final do PDF dentro de `out_dir`.

    Preferência: slug do título (estável, idêntico ao que `/ingest` usaria).
    Fallback: stem do filename da URL.
    """
    if titulo:
        stem = slugify(titulo)
    else:
        url_stem = Path(unquote(urlparse(pdf_url).path)).stem
        stem = slugify(url_stem)
    return out_dir / f"{stem}.pdf"


def parse_author(author: str | None, surname: str | None, firstname: str | None) -> tuple[str, str]:
    if author:
        parts = author.strip().split()
        if len(parts) < 2:
            raise SystemExit(
                "erro: --author precisa de pelo menos nome + sobrenome "
                "(ex.: 'Camille Flammarion')"
            )
        first = parts[0]
        sur = parts[-1]
        return sur.upper(), first.capitalize()
    if not (surname and firstname):
        raise SystemExit("erro: passe --author OU (--surname e --firstname)")
    return surname.upper(), firstname.capitalize()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--author", help="'Camille Flammarion' (atalho)")
    ap.add_argument("--surname", help="ex.: FLAMMARION")
    ap.add_argument("--firstname", help="ex.: Camille")
    ap.add_argument(
        "--letter",
        help="letra do sumário (default: primeira letra do sobrenome)",
    )
    ap.add_argument(
        "--out-dir",
        type=Path,
        help="default: raw/autores/<slug>/ (relativo ao root do repo)",
    )
    ap.add_argument(
        "--only",
        help="substring (case-insensitive) para filtrar títulos",
    )
    ap.add_argument(
        "--dry-run", action="store_true",
        help="lista obras e PDFs descobertos; não baixa nada",
    )
    ap.add_argument(
        "--delay", type=float, default=0.5,
        help="delay entre requests novos (cache nunca atrasa)",
    )
    ap.add_argument(
        "--force", action="store_true",
        help="re-baixa PDFs mesmo quando já existem no destino",
    )
    args = ap.parse_args(argv)

    surname, firstname = parse_author(args.author, args.surname, args.firstname)
    letter = (args.letter or surname[0]).upper()
    if not letter.isalpha() or len(letter) != 1:
        print(f"erro: letter inválida: {letter!r}", file=sys.stderr)
        return 2

    author_slug = slugify(f"{firstname} {surname}")
    out_dir = args.out_dir or (ROOT / "raw" / "autores" / author_slug)

    sumario_url = f"{BASE}/Artigos/Art_Sumarios/Sumario_Autores_{letter}.htm"
    print(f"[sumário] {sumario_url}", file=sys.stderr)
    sumario_html = fetch_html(sumario_url, delay=args.delay)

    book_pages = find_author_book_pages(
        sumario_html, surname=surname, firstname=firstname, sumario_url=sumario_url,
    )
    if args.only:
        needle = args.only.lower()
        book_pages = [
            (t, u) for (t, u) in book_pages
            if needle in t.lower() or needle in u.lower()
        ]
    print(f"[sumário] {len(book_pages)} obra(s) para {firstname} {surname}",
          file=sys.stderr)
    if not book_pages:
        print("  nada encontrado — confira --surname/--firstname/--letter",
              file=sys.stderr)
        # Sugere sobrenomes parecidos no mesmo sumário (o site às vezes
        # tem typos — ex.: DENNIS_Leon em vez de DENIS_Leon). Usamos
        # difflib (fuzzy match) porque substring exata falha aí.
        all_surnames = list_surnames_in_sumario(sumario_html)
        ascii_pool = [strip_accents(s).upper() for s in all_surnames]
        ascii_target = strip_accents(surname).upper()
        close = difflib.get_close_matches(ascii_target, ascii_pool, n=8, cutoff=0.7)
        if close:
            print(f"  sobrenomes parecidos no sumário {letter}: "
                  f"{', '.join(close)}", file=sys.stderr)
            print("  re-rode com a grafia que o site usa "
                  "(ex.: --surname DENNIS --firstname Leon)", file=sys.stderr)
        return 1

    new_bytes = 0
    skipped = 0
    failed: list[tuple[str, str]] = []
    no_pdf: list[tuple[str, str]] = []

    for i, (titulo, page_url) in enumerate(book_pages, 1):
        print(f"[{i}/{len(book_pages)}] {titulo}", file=sys.stderr)
        try:
            page_html = fetch_html(page_url, delay=args.delay)
        except Exception as exc:  # noqa: BLE001
            print(f"  ! falha ao abrir página: {exc}", file=sys.stderr)
            failed.append((titulo, page_url))
            continue

        pdf_url = find_pdf_url(page_html, page_url=page_url)
        if not pdf_url:
            print("  (sem PDF nesta página — só HTML/.doc?)", file=sys.stderr)
            no_pdf.append((titulo, page_url))
            continue

        dest = pdf_dest(out_dir, pdf_url, titulo=titulo)
        rel_dest = dest.relative_to(ROOT) if dest.is_absolute() and ROOT in dest.parents else dest
        if args.dry_run:
            print(f"  → {pdf_url}", file=sys.stderr)
            print(f"  → {rel_dest}", file=sys.stderr)
            continue
        if dest.exists() and not args.force:
            print(f"  já existe: {rel_dest} ({dest.stat().st_size:,} B)",
                  file=sys.stderr)
            skipped += 1
            continue
        try:
            written = download_pdf(pdf_url, dest, delay=args.delay)
            new_bytes += written
            print(f"  baixado: {rel_dest} ({written:,} B)", file=sys.stderr)
        except Exception as exc:  # noqa: BLE001
            print(f"  ! falha ao baixar PDF: {exc}", file=sys.stderr)
            failed.append((titulo, pdf_url))

    print("", file=sys.stderr)
    print(
        f"resumo: {len(book_pages)} obra(s) descoberta(s); "
        f"{skipped} já presente(s); {len(no_pdf)} sem PDF; "
        f"{len(failed)} falha(s); {new_bytes:,} B novos",
        file=sys.stderr,
    )
    if no_pdf:
        print("sem PDF:", file=sys.stderr)
        for t, u in no_pdf:
            print(f"  - {t} ({u})", file=sys.stderr)
    if failed:
        print("falhas:", file=sys.stderr)
        for t, u in failed:
            print(f"  - {t} ({u})", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
