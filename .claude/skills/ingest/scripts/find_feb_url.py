#!/usr/bin/env python3
"""
Helper para a skill /ingest preencher `direitos.url_aquisicao` em páginas de
obras com livros publicados pela FEB Editora.

A FEB Editora bloqueia acesso programático direto (firewall com reCAPTCHA),
então este script não tenta scraping — ele orquestra o fluxo:

  1) `find_feb_url.py wiki/obras/<slug>.md`
     → lê o título da página e imprime a URL de busca da FEB Editora.
       Claude usa `WebFetch` nessa URL para ver os candidatos.

  2) `find_feb_url.py wiki/obras/<slug>.md --set <url-do-produto>`
     → grava a URL escolhida em `direitos.url_aquisicao` na frontmatter,
       criando o campo se não existir e sobrescrevendo se já existir.

Heurística: produto canônico costuma ter o slug mais curto (ex.: `/nosso-lar`)
em vez de variantes como `/nosso-lar--novo-projeto2`, `/nosso-lar--ingles-`,
`/nosso-lar-para-criancas`. O ranqueamento fica com Claude, que vê o resultado
do WebFetch — este script só exibe a URL de busca e escreve a escolha.

Rodar:
  uv run python .claude/skills/ingest/scripts/find_feb_url.py <obra.md> [--set URL]
"""

from __future__ import annotations

import argparse
import re
import sys
import urllib.parse
from pathlib import Path

FEB_BASE = "https://www.febeditora.com.br"
SEARCH_PATH = "/product-list.ehc?typed=true&text="
PRODUCT_RE = re.compile(r"^https://www\.febeditora\.com\.br/[a-z0-9\-]+/?$")


def search_url(title: str) -> str:
    return FEB_BASE + SEARCH_PATH + urllib.parse.quote_plus(title.strip())


def read_title(obra_path: Path) -> str:
    """Título da obra: primeiro `# heading` do corpo. Fallback: nome do arquivo."""
    text = obra_path.read_text(encoding="utf-8")
    m = re.search(r"^#\s+(.+?)\s*$", text, flags=re.MULTILINE)
    if m:
        return m.group(1).strip()
    return obra_path.stem.replace("-", " ")


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
            ".claude/rules/convencoes-paginas.md)."
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
            f"erro: URL não parece um produto da FEB Editora: {url!r}\n"
            f"  esperado: {FEB_BASE}/<slug-do-produto>"
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
    url = search_url(title)
    print(f"Título detectado: {title}")
    print(f"Busca FEB Editora: {url}")
    print()
    print("Próximos passos:")
    print(f"  1. WebFetch({url!r}, prompt='Liste produtos: título exato + URL completa.')")
    print("  2. Escolha o slug canônico (geralmente o mais curto, sem `--ingles-`,")
    print("     `--novo-projeto2`, `-para-criancas` etc.).")
    print(f"  3. uv run python {Path(__file__).relative_to(Path.cwd()) if Path(__file__).is_relative_to(Path.cwd()) else __file__} \\")
    print(f"       {obra_path} --set https://www.febeditora.com.br/<slug>")


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
        help="Grava a URL em direitos.url_aquisicao em vez de imprimir busca",
    )
    args = p.parse_args()

    obra_path = resolve_obra(args.obra)
    if args.url:
        cmd_set(obra_path, args.url)
    else:
        cmd_search(obra_path)


if __name__ == "__main__":
    main()
