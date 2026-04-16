#!/usr/bin/env python3
"""Crawl Kardecpedia para gerar data/kardec-mapping.json.

Roda uma vez (ou quando Kardecpedia mudar). Resultado é commitado.
Coleta URLs de capítulo do Pentateuco e, para LE, índice questão→capítulo.

Uso:
  uv run python scripts/build_kardec_mapping.py --output data/kardec-mapping.json
"""

import argparse
import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

BASE = "https://kardecpedia.com"

BOOKS = {
    "LE":     {"id": 2,   "slug": "o-livro-dos-espiritos",                                       "wrapper": None},
    "LM":     {"id": 884, "slug": "o-livro-dos-mediuns-ou-guia-dos-mediuns-e-dos-evocadores",    "wrapper": None},
    "ESE":    {"id": 887, "slug": "o-evangelho-segundooespiritismo",                             "wrapper": None},
    "C&I":    {"id": 886, "slug": "o-ceu-e-o-inferno-ou-a-justica-divina-segundo-o-espiritismo", "wrapper": None},
    "Genese": {"id": 888, "slug": "a-genese-os-milagres-e-as-predicoes-segundo-o-espiritismo",   "wrapper": "a-genese"},
}

# LE: "parte-primeira-...", "parte-segunda-...". LM/C&I: "primeira-parte-...", "segunda-parte-...".
PART_ORDINALS = {
    "primeira": "1", "segunda": "2", "terceira": "3", "quarta": "4", "quinta": "5",
}
PART_RE_A = re.compile(r"^parte-([a-zçãéíó]+)(?:-|$)", re.IGNORECASE)   # LE
PART_RE_B = re.compile(r"^([a-zçãéíó]+)-parte(?:-|$)", re.IGNORECASE)   # LM, C&I
CAP_RE    = re.compile(r"^capitulo-([ivx]+)(?:-|$)", re.IGNORECASE)
INTRO_RE  = re.compile(r"^introducao(?:-|$)", re.IGNORECASE)
ROMAN_RE  = re.compile(r"^[ivxlcdm]+$", re.IGNORECASE)


def fetch(url: str) -> BeautifulSoup:
    r = requests.get(url, timeout=20, headers={"User-Agent": "isabel-wiki/build_kardec_mapping"})
    r.raise_for_status()
    return BeautifulSoup(r.text, "html.parser")


def book_links(book_id: int, book_slug: str) -> list[tuple[str, str]]:
    """Retorna [(text, path)] para todos os links internos do livro."""
    soup = fetch(f"{BASE}/roteiro-de-estudos/{book_id}/{book_slug}")
    out, seen = [], set()
    prefix = f"/roteiro-de-estudos/{book_id}/"
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith(BASE):
            href = href[len(BASE):]
        if not href.startswith(prefix) or href in seen:
            continue
        seen.add(href)
        out.append((a.get_text(strip=True), href))
    return out


def url_segments(path: str) -> list[str]:
    """Segmentos depois do book_slug + section_id."""
    parts = [s for s in urlparse(path).path.split("/") if s]
    # ["roteiro-de-estudos", str(book_id), book_slug, section_id, *rest]
    return parts[4:] if len(parts) >= 5 else []


def parse_part(seg: str) -> str | None:
    m = PART_RE_A.match(seg) or PART_RE_B.match(seg)
    if not m:
        return None
    return PART_ORDINALS.get(m.group(1).lower())


def crawl_book(sigla: str, meta: dict) -> dict:
    pairs = book_links(meta["id"], meta["slug"])
    print(f"[{sigla}] {len(pairs)} links", file=sys.stderr)

    chapters: dict[str, str] = {}     # "1:VII" or "VII" → URL
    questions: dict[str, str] = {}    # "990" → "4:II" (LE) or "990" → "1:VII" (C&I, LM)
    intro_url: str | None = None
    intro_items: dict[str, str] = {}

    for _text, path in pairs:
        segs = url_segments(path)
        if not segs:
            continue

        # Wrapper (Gênese): strip leading "a-genese"
        if meta.get("wrapper") and segs and segs[0] == meta["wrapper"]:
            segs = segs[1:]
            if not segs:
                continue

        # Introdução
        if len(segs) == 1 and INTRO_RE.match(segs[0]):
            intro_url = path
            continue
        if len(segs) == 2 and INTRO_RE.match(segs[0]) and ROMAN_RE.match(segs[1]):
            intro_items[segs[1].upper()] = path
            continue

        # Try part prefix
        part_id = parse_part(segs[0])
        if part_id is not None:
            rest = segs[1:]
        else:
            rest = segs

        # Now look for capitulo-X in rest[0]
        if not rest:
            continue
        cap_m = CAP_RE.match(rest[0])
        if not cap_m:
            continue
        cap_roman = cap_m.group(1).upper()
        key = f"{part_id}:{cap_roman}" if part_id else cap_roman

        # Chapter URL: rest is just [capitulo-X-...]
        if len(rest) == 1:
            chapters.setdefault(key, path)
            continue

        # Item/question: bare digit at the end (depth varies due to optional sub-section)
        last = rest[-1]
        if last.isdigit():
            questions[last] = key

    entry: dict = {"chapters": chapters}
    # Só LE é citado por questão isolada (`q. 990`); demais sempre incluem o capítulo.
    # Para outros livros, "items" colidem entre capítulos (per-chapter, não globais).
    if sigla == "LE" and questions:
        entry["questions"] = questions
    if intro_url:
        entry["intro"] = intro_url
    if intro_items:
        entry["intro_items"] = intro_items
    return entry


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output", type=Path, default=Path("data/kardec-mapping.json"))
    ap.add_argument("--delay", type=float, default=0.5, help="segundos entre requests")
    args = ap.parse_args(argv)

    result = {"_base": BASE, "books": {}}
    for sigla, meta in BOOKS.items():
        print(f"[{sigla}] crawling…", file=sys.stderr)
        entry = crawl_book(sigla, meta)
        chs = len(entry["chapters"])
        qs = len(entry.get("questions", {}))
        print(f"[{sigla}] {chs} chapters, {qs} items", file=sys.stderr)
        result["books"][sigla] = entry
        time.sleep(args.delay)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {args.output}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
