#!/usr/bin/env python3
"""Baixa a Revista Espírita (1858–1869) da Kardecpédia.

Gera:
  - data/revista-espirita-mapping.json — catálogo {ano → [artigos]}
  - raw/kardec/revista-espirita/revista-espirita-YYYY.md (12 arquivos)

Uso:
  uv run python scripts/download_revista_espirita.py                     # tudo
  uv run python scripts/download_revista_espirita.py --year 1858         # só 1858
  uv run python scripts/download_revista_espirita.py --discover-only     # só catálogo
  uv run python scripts/download_revista_espirita.py --year 1858 --dry-run

Idempotente: respostas HTTP ficam em /tmp/revista-espirita-cache/.
"""

import argparse
import hashlib
import json
import re
import sys
import time
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup, Tag
from html_to_markdown import convert

BASE = "https://kardecpedia.com"
UA = "isabel-wiki/download-revista-espirita"
CACHE_DIR = Path("/tmp/revista-espirita-cache")

# Year → publication ID (descobertos em https://kardecpedia.com/).
YEARS: dict[int, int] = {
    1858: 20,
    1859: 893,
    1860: 894,
    1861: 895,
    1862: 896,
    1863: 897,
    1864: 898,
    1865: 899,
    1866: 900,
    1867: 901,
    1868: 902,
    1869: 903,
}

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


def cache_path(url: str) -> Path:
    slug = re.sub(r"[^a-z0-9]+", "_", url.lower()).strip("_")
    # macOS / ext4 limitam nomes a 255 bytes; trunca e desambigua com hash.
    if len(slug) > 200:
        digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:10]
        slug = f"{slug[:180]}_{digest}"
    return CACHE_DIR / f"{slug}.html"


def fetch(url: str, *, delay: float = 0.0) -> str:
    cp = cache_path(url)
    if cp.exists():
        return cp.read_text(encoding="utf-8")
    if delay:
        time.sleep(delay)
    r = requests.get(url, timeout=30, headers={"User-Agent": UA})
    r.raise_for_status()
    cp.parent.mkdir(parents=True, exist_ok=True)
    cp.write_text(r.text, encoding="utf-8")
    return r.text


def url_segments(path: str) -> list[str]:
    """Segmentos depois do slug do volume (ano).

    Ex.: /roteiro-de-estudos/20/revista-…-1858/25/janeiro/introducao
         → ['25', 'janeiro', 'introducao']
    """
    parts = [s for s in urlparse(path).path.split("/") if s]
    return parts[3:] if len(parts) >= 4 else []


def discover_articles(year: int, pub_id: int, *, delay: float) -> list[dict]:
    """Lista artigos de um ano (na ordem do índice)."""
    toc_url = f"{BASE}/roteiro-de-estudos/{pub_id}/revista-espirita-jornal-de-estudos-psicologicos-{year}"
    soup = BeautifulSoup(fetch(toc_url, delay=delay), "html.parser")
    prefix = f"/roteiro-de-estudos/{pub_id}/"
    seen: set[str] = set()
    articles: list[dict] = []
    for a in soup.find_all("a", href=True):
        href: str = a["href"]
        if href.startswith(BASE):
            href = href[len(BASE):]
        if not href.startswith(prefix) or href in seen:
            continue
        segs = url_segments(href)
        if len(segs) < 3:  # precisa ter ao menos: article_id / mes / slug
            continue
        article_id = segs[0]
        mes = segs[1]
        if mes not in MONTHS:
            continue
        if not article_id.isdigit():
            continue
        seen.add(href)
        path_segments = segs[2:]  # tudo depois do mes (1+ slugs)
        articles.append({
            "id": int(article_id),
            "mes": mes,
            "path": path_segments,
            "titulo": a.get_text(strip=True),
            "url": f"{BASE}{href}",
        })
    return articles


_HEADER_RE = re.compile(r"^(#+)(\s+.*)$", re.MULTILINE)


def demote_headers(md: str, article_level: int) -> str:
    """Rebaixa headers do corpo para ficarem abaixo do header do artigo.

    Se o artigo é `###` (level=3) e o body tem `## Foo`, vira `#### Foo`.
    """
    shift = article_level - 1
    if shift <= 0:
        return md
    def repl(m: re.Match[str]) -> str:
        return "#" * (len(m.group(1)) + shift) + m.group(2)
    return _HEADER_RE.sub(repl, md)


def extract_body(html: str, *, article_level: int = 3) -> str:
    """Extrai o corpo do artigo (`<div class="js-texts">`) já como Markdown."""
    soup = BeautifulSoup(html, "html.parser")
    container = soup.find("div", class_="js-texts")
    if not isinstance(container, Tag):
        raise ValueError("div.js-texts ausente")
    for tag in container.find_all(["script", "style", "form", "button"]):
        tag.decompose()
    result = convert(str(container))
    return demote_headers(result.content.strip(), article_level)


def heading_for(article: dict) -> str:
    """### + extras conforme profundidade do path da URL."""
    depth = len(article["path"])
    level = "#" * (2 + depth)  # ## mês, ### artigo top, #### sub, …
    return level


def render_year(year: int, articles: list[dict], pub_id: int) -> str:
    pieces: list[str] = []
    pieces.append("Allan Kardec  ")
    pieces.append("**Revista Espírita — Jornal de Estudos Psicológicos**  ")
    pieces.append(f"**Ano {year}**\n")
    pieces.append(
        f"Fonte: Kardecpédia "
        f"(<{BASE}/roteiro-de-estudos/{pub_id}/revista-espirita-jornal-de-estudos-psicologicos-{year}>)  "
    )
    pieces.append(f"Baixado em: {time.strftime('%Y-%m-%d')}\n")

    current_month: str | None = None
    for art in articles:
        if art["mes"] != current_month:
            current_month = art["mes"]
            pieces.append(f"\n## {MONTH_DISPLAY[current_month]}\n")
        level = heading_for(art)
        pieces.append(f"<!-- url: {art['url']} | id: {art['id']} -->")
        pieces.append(f"{level} {art['titulo']}\n")
        body = art.get("body", "").strip()
        if body:
            pieces.append(body)
        else:
            pieces.append("_(corpo não baixado — ver URL acima)_")
        pieces.append("")  # linha em branco
    return "\n".join(pieces).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--year", type=int, help="processa apenas este ano")
    ap.add_argument("--discover-only", action="store_true",
                    help="apenas descoberta (não baixa corpos)")
    ap.add_argument("--dry-run", action="store_true",
                    help="descobre + imprime sumário; não escreve arquivos")
    ap.add_argument("--delay", type=float, default=0.5,
                    help="delay entre requests novos (cache nunca atrasa)")
    ap.add_argument("--mapping", type=Path,
                    default=Path("data/revista-espirita-mapping.json"))
    ap.add_argument("--out-dir", type=Path,
                    default=Path("raw/kardec/revista-espirita"))
    args = ap.parse_args(argv)

    years_to_process: Iterable[int]
    if args.year:
        if args.year not in YEARS:
            print(f"erro: ano {args.year} não conhecido (1858–1869)", file=sys.stderr)
            return 2
        years_to_process = [args.year]
    else:
        years_to_process = sorted(YEARS)

    mapping: dict = {"_base": BASE, "anos": {}}
    if args.mapping.exists() and not args.year:
        # preserva entradas de outros anos quando rodando ano único
        try:
            mapping = json.loads(args.mapping.read_text(encoding="utf-8"))
        except Exception:
            pass
    elif args.mapping.exists() and args.year:
        try:
            mapping = json.loads(args.mapping.read_text(encoding="utf-8"))
        except Exception:
            pass

    args.out_dir.mkdir(parents=True, exist_ok=True)

    total_articles = 0
    for year in years_to_process:
        pub_id = YEARS[year]
        print(f"[{year}] descobrindo artigos (id={pub_id})…", file=sys.stderr)
        articles = discover_articles(year, pub_id, delay=args.delay)
        print(f"[{year}] {len(articles)} artigos", file=sys.stderr)
        total_articles += len(articles)

        mapping.setdefault("anos", {})[str(year)] = {
            "id": pub_id,
            "url": f"{BASE}/roteiro-de-estudos/{pub_id}/revista-espirita-jornal-de-estudos-psicologicos-{year}",
            "artigos": [
                {"id": a["id"], "mes": a["mes"], "path": a["path"],
                 "titulo": a["titulo"], "url": a["url"]}
                for a in articles
            ],
        }

        if args.discover_only:
            continue

        if not args.dry_run:
            for i, art in enumerate(articles, 1):
                if i % 25 == 0 or i == len(articles):
                    print(f"[{year}] baixando {i}/{len(articles)}…", file=sys.stderr)
                try:
                    html = fetch(art["url"], delay=args.delay)
                    art["body"] = extract_body(html, article_level=2 + len(art["path"]))
                except Exception as exc:  # noqa: BLE001
                    print(f"  ! falha em {art['url']}: {exc}", file=sys.stderr)
                    art["body"] = f"_(falha ao baixar: {exc})_"

            out_path = args.out_dir / f"revista-espirita-{year}.md"
            out_path.write_text(render_year(year, articles, pub_id), encoding="utf-8")
            print(f"[{year}] gravado {out_path} ({out_path.stat().st_size:,} bytes)",
                  file=sys.stderr)
        else:
            # dry-run: imprime resumo por mês
            from collections import Counter
            por_mes = Counter(a["mes"] for a in articles)
            for mes in MONTHS:
                if mes in por_mes:
                    print(f"  {MONTH_DISPLAY[mes]:12s}: {por_mes[mes]}", file=sys.stderr)

    args.mapping.parent.mkdir(parents=True, exist_ok=True)
    args.mapping.write_text(
        json.dumps(mapping, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"mapping: {args.mapping} ({total_articles} artigos no batch)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
