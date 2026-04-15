#!/usr/bin/env python3
"""
Crawler da Bíblia Almeida Corrigida Fiel (ACF) — bibliaestudos.com

Extrai todos os capítulos em Markdown para raw/biblia-acf/{slug}/{cap}.md

Uso:
    uv run python scripts/crawl_biblia_acf.py                  # tudo
    uv run python scripts/crawl_biblia_acf.py --livro genesis   # só um livro
    uv run python scripts/crawl_biblia_acf.py --skip-existing   # pula já baixados
"""

import argparse
import html
import re
import sys
import time
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://bibliaestudos.com/acf/"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "raw" / "biblia-acf"
DELAY = 3  # segundos entre requests

session = requests.Session()
session.headers.update({
    "User-Agent": "IsAbel-Wiki-Crawler/1.0 (estudo pessoal)"
})


def fetch(url: str, retries: int = 5) -> str:
    for attempt in range(retries):
        try:
            resp = session.get(url, timeout=30)
            resp.raise_for_status()
            resp.encoding = "utf-8"
            return resp.text
        except requests.RequestException as e:
            if attempt < retries - 1:
                is_429 = hasattr(e, "response") and e.response is not None and e.response.status_code == 429
                wait = 30 * (attempt + 1) if is_429 else 2 ** (attempt + 1)
                print(f"  ⚠ {e} — retry em {wait}s")
                time.sleep(wait)
            else:
                raise


def get_books() -> list[dict]:
    """Retorna lista de {nome, slug, url} dos 66 livros."""
    page = fetch(BASE_URL)
    soup = BeautifulSoup(page, "html.parser")

    books = []
    seen = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        # Match /acf/{slug}/ mas não /acf/{slug}/{num}/ nem /acf/feed/
        if not href.startswith(BASE_URL):
            continue
        path = href[len(BASE_URL):].strip("/")
        if not path or "/" in path or path == "feed":
            continue
        if path in seen:
            continue
        seen.add(path)

        # Extrair nome do livro do texto do link
        nome = a.get_text(strip=True)
        if not nome:
            continue

        books.append({"nome": nome, "slug": path, "url": href})

    return books


def get_chapters(book_url: str, slug: str) -> list[int]:
    """Retorna lista de números de capítulos para um livro."""
    page = fetch(book_url)
    soup = BeautifulSoup(page, "html.parser")

    chapters = []
    prefix = f"{BASE_URL}{slug}/"
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith(prefix):
            rest = href[len(prefix):].strip("/")
            if rest.isdigit():
                chapters.append(int(rest))

    return sorted(set(chapters))


def extract_book_name(page_html: str) -> str:
    """Extrai nome do livro do <title>, ex: 'Gênesis 1 – Bíblia Online ACF' → 'Gênesis'."""
    soup = BeautifulSoup(page_html, "html.parser")
    title = soup.find("title")
    if title:
        text = html.unescape(title.get_text())
        # "Gênesis 1 – Bíblia Online ACF" → "Gênesis 1"
        parts = text.split("–")
        book_chapter = parts[0].strip()
        # Remover número do capítulo no final
        return re.sub(r"\s+\d+$", "", book_chapter).strip()
    return ""


def parse_verses(page_html: str) -> list[tuple[int, str]]:
    """Extrai versículos da página. Retorna [(num, texto), ...]."""
    soup = BeautifulSoup(page_html, "html.parser")
    verses = []

    for p in soup.find_all("p", class_="v"):
        num_str = p.get("data-v", "")
        if not num_str:
            sup = p.find("sup")
            if sup:
                num_str = sup.get_text(strip=True)

        # Remover o <sup> do número antes de extrair texto
        sup = p.find("sup")
        if sup:
            sup.decompose()

        # get_text com separator=" " para evitar palavras grudadas de <a> tags
        text = p.get_text(separator=" ", strip=True)
        # Normalizar espaços múltiplos e espaços antes de pontuação
        text = re.sub(r" {2,}", " ", text)
        text = re.sub(r" ([,;:.!?])", r"\1", text)

        try:
            num = int(num_str)
        except (ValueError, TypeError):
            continue

        verses.append((num, text))

    return sorted(verses, key=lambda v: v[0])


def save_chapter(slug: str, chapter: int, nome_livro: str,
                 verses: list[tuple[int, str]]) -> Path:
    """Salva capítulo como Markdown."""
    outdir = OUTPUT_DIR / slug
    outdir.mkdir(parents=True, exist_ok=True)
    outpath = outdir / f"{chapter}.md"

    url = f"{BASE_URL}{slug}/{chapter}/"

    lines = [
        "---",
        f"livro: {nome_livro}",
        f"capitulo: {chapter}",
        f"slug: {slug}",
        f"url: {url}",
        "---",
        "",
        f"# {nome_livro} {chapter}",
        "",
    ]

    for num, text in verses:
        lines.append(f"**{num}.** {text}")
        lines.append("")

    outpath.write_text("\n".join(lines), encoding="utf-8")
    return outpath


def generate_index(books_data: list[dict]) -> Path:
    """Gera raw/biblia-acf/index.md com índice completo."""
    lines = [
        "# Bíblia Almeida Corrigida Fiel (ACF)",
        "",
        f"Fonte: [{BASE_URL}]({BASE_URL})",
        "",
    ]

    for book in books_data:
        nome = book["nome"]
        slug = book["slug"]
        caps = book.get("chapters", [])
        if caps:
            cap_links = ", ".join(f"[{c}]({slug}/{c}.md)" for c in caps)
            lines.append(f"## {nome}")
            lines.append("")
            lines.append(f"Capítulos: {cap_links}")
            lines.append("")

    outpath = OUTPUT_DIR / "index.md"
    outpath.write_text("\n".join(lines), encoding="utf-8")
    return outpath


def main():
    parser = argparse.ArgumentParser(description="Crawler Bíblia ACF")
    parser.add_argument("--livro", help="Slug de um livro específico (ex: genesis, judas)")
    parser.add_argument("--skip-existing", action="store_true",
                        help="Pular capítulos já baixados")
    args = parser.parse_args()

    print("Buscando lista de livros...")
    books = get_books()
    print(f"  {len(books)} livros encontrados")

    if args.livro:
        books = [b for b in books if b["slug"] == args.livro]
        if not books:
            print(f"Livro '{args.livro}' não encontrado.")
            sys.exit(1)

    total_saved = 0
    total_skipped = 0

    for i, book in enumerate(books, 1):
        slug = book["slug"]
        nome = book["nome"]

        print(f"\n[{i}/{len(books)}] {nome} ({slug})")

        time.sleep(DELAY)
        chapters = get_chapters(book["url"], slug)
        book["chapters"] = chapters
        print(f"  {len(chapters)} capítulos")

        for cap in chapters:
            outpath = OUTPUT_DIR / slug / f"{cap}.md"
            if args.skip_existing and outpath.exists():
                total_skipped += 1
                continue

            time.sleep(DELAY)
            url = f"{BASE_URL}{slug}/{cap}/"
            page_html = fetch(url)

            # Extrair nome completo com acentos do título da página
            nome_completo = extract_book_name(page_html) or nome

            verses = parse_verses(page_html)
            if not verses:
                print(f"  ⚠ {nome} {cap}: nenhum versículo encontrado!")
                continue

            save_chapter(slug, cap, nome_completo, verses)
            total_saved += 1
            print(f"  {nome} {cap}/{chapters[-1]} ✓ ({len(verses)} versículos)")

    # Gerar índice
    print("\nGerando índice...")
    idx_path = generate_index(books)
    print(f"  {idx_path}")

    print(f"\nConcluído: {total_saved} capítulos salvos, {total_skipped} pulados")


if __name__ == "__main__":
    main()
