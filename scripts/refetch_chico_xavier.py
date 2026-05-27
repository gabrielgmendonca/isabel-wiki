#!/usr/bin/env python3
"""Re-baixa o corpus Chico Xavier de bibliadocaminho.com aplicando o seletor
corrigido do bookcrawler (captura texto em <strong>/<em>/<a>; iteração
por <p>, não por fragmento). Produz `books_with_links.json` no formato
que `compile_book.py` consome.

Bypass do spider scrapy: o índice do site reestruturou
(TXavieriano/ → TX/) e a varredura via spider precisa de rewrite
(roadmap §1.3). A lista de URLs vem do JSON gerado pela última crawl
bem-sucedida (backup), que aponta para URLs ainda válidas.

Uso:
  uv run python scripts/refetch_chico_xavier.py \\
      --source ~/supersim-bkp/Personal/isabel-wiki/books_with_links.json \\
      [--book "Missionários da Luz"] \\
      [--output books_with_links.json] \\
      [--workers 4] [--delay 0.2]
"""

import argparse
import concurrent.futures
import json
import sys
import time
from pathlib import Path

import requests
from parsel import Selector

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = ROOT / "books_with_links.json"


def _normalize_ws(s: str) -> str:
    return " ".join(s.split())


def fetch_chapter(url: str, session: requests.Session) -> dict:
    """Espelha BooksSpider.parse_chapter com o fix do bold + iteração por <p>.
    Retorna um dict no formato de entrada do compile_book.py."""
    r = session.get(url, timeout=30)
    r.raise_for_status()
    r.encoding = "utf-8"
    sel = Selector(text=r.text)

    heading = sel.css("h1 i::text").get("").strip().split("—")
    book_title = heading[0].strip()
    book_author = heading[1].strip() if len(heading) > 1 else ""

    chapter_number = sel.css("h4::text").get("").strip()
    chapter_name = sel.css("h2::text").get("").strip()

    epigraph = sel.css("blockquote p.BT")
    chapter_epigraph_text = ""
    chapter_epigraph_author = ""
    chapter_epigraph_ref = ""
    if epigraph:
        chapter_epigraph_text = (
            epigraph.css("::text").get("").replace("—", "").strip()
        )
        chapter_epigraph_author = (
            epigraph.css("i::text").get("").replace(".", "").strip()
        )
        chapter_epigraph_ref = epigraph.css("a::text").get("")

    paragraphs_sel = sel.css(
        'blockquote p:not([class="BT"]):not([class="Sgn"]):not([class="FnT"])'
    )
    parts: list[str] = []
    for p in paragraphs_sel:
        text = _normalize_ws("".join(p.xpath(".//text()").getall()).strip())
        if text:
            parts.append(text)
    chapter_text = "\n".join(parts)

    return {
        "book_title": _normalize_ws(book_title),
        "book_author": _normalize_ws(book_author),
        "book_medium": "Chico Xavier",
        "chapter_number": chapter_number,
        "chapter_name": chapter_name,
        "chapter_epigraph_text": chapter_epigraph_text,
        "chapter_epigraph_author": chapter_epigraph_author,
        "chapter_epigraph_ref": chapter_epigraph_ref,
        "chapter_text": chapter_text,
        "chapter_url": url,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        required=True,
        help="JSON antigo de onde extrair a lista de chapter_url",
    )
    parser.add_argument(
        "--book",
        help='Filtrar por book_title exato (ex.: "Missionários da Luz"). Sem isso, processa todos.',
    )
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument(
        "--delay",
        type=float,
        default=0.2,
        help="Delay (s) entre o início de fetches por worker. Polidez com o site.",
    )
    args = parser.parse_args()

    source = json.loads(Path(args.source).read_text(encoding="utf-8"))
    if args.book:
        urls = sorted({e["chapter_url"] for e in source if e["book_title"] == args.book})
    else:
        urls = sorted({e["chapter_url"] for e in source})
    if not urls:
        print("Nenhum chapter_url encontrado.", file=sys.stderr)
        sys.exit(1)
    print(f"refetching {len(urls)} URLs...", file=sys.stderr)

    results: list[dict] = []
    failures: list[tuple[str, str]] = []
    session = requests.Session()
    session.headers.update({
        "User-Agent": "bookcrawler-refetch (+https://github.com/gabrielgmendonca/bookcrawler)"
    })

    lock_state = {"last_start": 0.0}

    def worker(url: str) -> dict | None:
        # crude rate limit: ensure at least `delay` seconds between fetch starts
        now = time.monotonic()
        wait = lock_state["last_start"] + args.delay - now
        if wait > 0:
            time.sleep(wait)
        lock_state["last_start"] = time.monotonic()
        try:
            return fetch_chapter(url, session)
        except Exception as e:
            failures.append((url, repr(e)))
            return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as ex:
        for i, ch in enumerate(ex.map(worker, urls), 1):
            if ch is not None:
                results.append(ch)
            if i % 50 == 0 or i == len(urls):
                print(f"  {i}/{len(urls)}", file=sys.stderr)

    results.sort(key=lambda c: (c["book_title"], c["chapter_url"]))
    Path(args.output).write_text(
        json.dumps(results, ensure_ascii=False), encoding="utf-8"
    )
    print(f"escrito: {args.output} ({len(results)} capítulos)", file=sys.stderr)
    if failures:
        print(f"falhas: {len(failures)}", file=sys.stderr)
        for u, err in failures[:10]:
            print(f"  {u}\n    {err}", file=sys.stderr)


if __name__ == "__main__":
    main()
