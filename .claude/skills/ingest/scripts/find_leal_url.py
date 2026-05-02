#!/usr/bin/env python3
"""
Helper para a skill /ingest preencher `direitos.url_aquisicao` em páginas de
obras com livros publicados pela Livraria Espírita Alvorada (LEAL) — sobretudo
Divaldo Franco / Joanna de Ângelis.

A Leal não expõe URL de busca por query string, mas publica
`sitemap_produtos.xml` com todas as URLs canônicas. Padrões observados:

  - Série Psicológica de Joanna de Ângelis:
      /series-e-colecoes/serie-psicologica-joanna-de-angelis/<slug>.html
  - Demais livros por espírito:
      /livros-por-espirito/<espirito>/<slug>.html
  - Outras categorias:
      /series-e-colecoes/<colecao>/<slug>.html
      /outros/<categoria>/<slug>.html

O slug do produto é o título normalizado (lowercase, sem acentos, hífens no
lugar de espaços/pontuação). Filtrar o sitemap por slug resolve o caso da
Série Psicológica sem precisar de regra especial.

Fluxo:

  1) `find_leal_url.py wiki/obras/<slug>.md`
     → baixa o sitemap, imprime URLs cujo slug do produto bate com o título
       da página (match exato + parciais, em blocos separados).

  2) `find_leal_url.py wiki/obras/<slug>.md --set <url-do-produto>`
     → grava a URL escolhida em `direitos.url_aquisicao` na frontmatter,
       criando o campo se não existir e sobrescrevendo se já existir.

Rodar:
  uv run python .claude/skills/ingest/scripts/find_leal_url.py <obra.md> [--set URL]
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

LEAL_BASE = "https://www.livrarialeal.com.br"
SITEMAP_URL = f"{LEAL_BASE}/sitemap_produtos.xml"
PRODUCT_RE = re.compile(r"^https://www\.livrarialeal\.com\.br/[a-z0-9\-/]+\.html$")
SITEMAP_NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def slugify(text: str) -> str:
    """Aproxima o slug usado pela Leal: lowercase, sem acentos, hífens.

    Não é exato byte-a-byte com o que a Leal gera, mas é suficiente para
    ranquear matches contra os slugs do sitemap.
    """
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def read_title(obra_path: Path) -> str:
    """Título da obra: primeiro `# heading` do corpo. Fallback: nome do arquivo."""
    text = obra_path.read_text(encoding="utf-8")
    m = re.search(r"^#\s+(.+?)\s*$", text, flags=re.MULTILINE)
    if m:
        return m.group(1).strip()
    return obra_path.stem.replace("-", " ")


def fetch_sitemap_urls() -> list[str]:
    req = urllib.request.Request(
        SITEMAP_URL,
        headers={"User-Agent": "isabel-wiki/find_leal_url"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read()
    root = ET.fromstring(data)
    seen: dict[str, None] = {}
    for loc in root.iterfind(".//sm:url/sm:loc", SITEMAP_NS):
        if loc.text:
            seen.setdefault(loc.text.strip(), None)
    return list(seen.keys())


def url_slug(url: str) -> str:
    """Extrai o slug do produto: parte final da URL antes de `.html`."""
    m = re.match(r".*/([^/]+)\.html$", url)
    return m.group(1) if m else ""


def rank_candidates(title: str, urls: list[str]) -> tuple[list[str], list[str]]:
    """Retorna (matches_exatos, matches_parciais) ordenados por proximidade."""
    target = slugify(title)
    if not target:
        return [], []

    exact: list[str] = []
    partial: list[tuple[int, str]] = []

    for url in urls:
        slug = url_slug(url)
        if not slug:
            continue
        if slug == target:
            exact.append(url)
        elif target in slug or slug in target:
            # menor diferença de comprimento = mais próximo
            partial.append((abs(len(slug) - len(target)), url))

    partial.sort(key=lambda p: p[0])
    return exact, [u for _, u in partial]


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        sys.exit("erro: arquivo sem frontmatter YAML (precisa começar com `---`)")
    end = text.find("\n---\n", 4)
    if end == -1:
        sys.exit("erro: frontmatter sem delimitador de fim (`---`)")
    return text[4:end], text[end + 5 :]


def patch_direitos(front: str, url: str) -> str:
    """Insere/atualiza `url_aquisicao` dentro do bloco `direitos:`.

    Mantém a indentação de 2 espaços usada no resto da wiki. Se já houver
    `url_aquisicao`, sobrescreve. Se não, insere logo após `detentor:` quando
    presente, senão no fim do bloco.
    """
    lines = front.splitlines()
    start = next(
        (i for i, line in enumerate(lines) if line.rstrip() == "direitos:"),
        None,
    )
    if start is None:
        sys.exit(
            "erro: bloco `direitos:` ausente na frontmatter. "
            "Preencha-o primeiro (ver passo 4.5 do /ingest e "
            ".claude/rules/convencoes-direitos.md)."
        )

    # Fim do bloco: primeira linha não indentada e não vazia depois do start.
    end = start + 1
    while end < len(lines):
        line = lines[end]
        if line == "" or line.startswith("  "):
            end += 1
            continue
        break
    block = lines[start:end]

    new_line = f"  url_aquisicao: {url}"
    for i, line in enumerate(block):
        if line.lstrip().startswith("url_aquisicao:"):
            if line.rstrip() == new_line:
                return front  # já está correto
            block[i] = new_line
            return "\n".join(lines[:start] + block + lines[end:])

    # Não existe ainda: inserir após `detentor:` se houver.
    detentor_idx = next(
        (i for i, line in enumerate(block) if line.lstrip().startswith("detentor:")),
        None,
    )
    insert_at = (detentor_idx + 1) if detentor_idx is not None else len(block)
    block.insert(insert_at, new_line)
    return "\n".join(lines[:start] + block + lines[end:])


def cmd_set(obra_path: Path, url: str) -> None:
    if not PRODUCT_RE.match(url):
        sys.exit(
            f"erro: URL não parece um produto da Livraria Leal: {url!r}\n"
            f"  esperado: {LEAL_BASE}/<categoria>/<slug>.html"
        )
    text = obra_path.read_text(encoding="utf-8")
    front, body = split_frontmatter(text)
    new_front = patch_direitos(front, url)
    if new_front == front:
        print(f"= direitos.url_aquisicao já está como {url}")
        return
    obra_path.write_text(f"---\n{new_front}\n---\n{body}", encoding="utf-8")
    print(f"✓ {obra_path}: direitos.url_aquisicao = {url}")


def cmd_search(obra_path: Path) -> None:
    title = read_title(obra_path)
    print(f"Título detectado: {title}")
    print(f"Slug alvo:        {slugify(title)}")
    print(f"Sitemap:          {SITEMAP_URL}")
    print()

    try:
        urls = fetch_sitemap_urls()
    except Exception as e:
        sys.exit(f"erro: falha ao baixar sitemap ({e})")

    exact, partial = rank_candidates(title, urls)

    if exact:
        print(f"Match exato ({len(exact)}):")
        for u in exact:
            print(f"  {u}")
        print()
    else:
        print("Match exato: nenhum.")
        print()

    if partial:
        print(f"Parciais (top {min(10, len(partial))} por proximidade de slug):")
        for u in partial[:10]:
            print(f"  {u}")
        print()

    if not exact and not partial:
        print("Nenhum candidato. Possíveis causas:")
        print("  - Título da página difere do título comercial (ed. especial, capa dura, ISBN)")
        print("  - Obra não publicada pela Leal (verificar `direitos.detentor`)")
        print("  - Sitemap incompleto")
        return

    script = (
        Path(__file__).relative_to(Path.cwd())
        if Path(__file__).is_relative_to(Path.cwd())
        else __file__
    )
    print("Próximo passo:")
    print(f"  uv run python {script} \\")
    print(f"    {obra_path} --set <url-escolhida>")


def resolve_obra(arg: str) -> Path:
    """Aceita caminho completo, caminho sem extensão, ou apenas o slug."""
    candidates = [
        Path(arg),
        Path(arg).with_suffix(".md"),
        Path("wiki/obras") / f"{arg}.md",
        Path("wiki/obras") / Path(arg).name,
    ]
    for c in candidates:
        if c.is_file():
            return c
    sys.exit(f"erro: página da obra não encontrada (tentei: {[str(c) for c in candidates]})")


def main() -> None:
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument(
        "obra",
        help="Caminho para wiki/obras/<slug>.md (ou apenas o slug)",
    )
    p.add_argument(
        "--set",
        dest="url",
        metavar="URL",
        help="Grava a URL em direitos.url_aquisicao em vez de buscar candidatos",
    )
    args = p.parse_args()

    obra_path = resolve_obra(args.obra)
    if args.url:
        cmd_set(obra_path, args.url)
    else:
        cmd_search(obra_path)


if __name__ == "__main__":
    main()
