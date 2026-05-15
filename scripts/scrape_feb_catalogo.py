#!/usr/bin/env python3
"""Faz scrape do catálogo da loja FEB Editora para um conjunto de autores.

Fonte: https://www.febeditora.com.br/listaprodutos.asp (plataforma
Fastcommerce). A listagem multi-autor não expõe o autor por produto — só o
filtro `fil=<id>` sabe a quem o produto pertence. Por isso o scrape é feito
**um autor por vez** (`fil=<id_único>`), e todo produto retornado pertence
àquele autor. Cada produto vem com um bloco `<script type="application/ld+json">`
(Schema.org/Product) de onde extraímos título, SKU, preço e URL canônica.

Paginação: a plataforma usa lazy-load AJAX com o parâmetro `&pag=N`
(20 produtos/página). Iteramos até a página não trazer productID novo.

Os 14 autores e seus IDs de filtro foram derivados da URL multi-autor passada
pelo usuário (ordem `fil=` ↔ ordem dos nomes em `tfil=`, validada
empiricamente em 2026-05-15: 293768→Bezerra 5 obras, 293784→Conan Doyle
2 obras, 293870→Simonetti 7 obras).

CLI:
  uv run python scripts/scrape_feb_catalogo.py                 # scrape + JSON + MD
  uv run python scripts/scrape_feb_catalogo.py --dry-run       # só conta, não grava
  uv run python scripts/scrape_feb_catalogo.py --only simonetti # filtra autor
  uv run python scripts/scrape_feb_catalogo.py --json-out PATH --md-out PATH

Saídas:
  data/feb-catalogo-autores.json  — dados estruturados (re-runs determinísticos)
  OBRAS-PENDENTES-FEB.md          — tracker de download por autor (raiz do repo)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import date
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from _slug import slugify  # noqa: E402

UA = "isabel-wiki/scrape-feb-catalogo"
BASE = "https://www.febeditora.com.br/listaprodutos.asp"

# (fil_id, nome de exibição, slug da página em wiki/personalidades/).
# IDs vêm da URL multi-autor do usuário. ATENÇÃO: a ordem posicional
# `fil=` ↔ `tfil=` da URL combinada NÃO é confiável — a loja reordena, e o
# `tfil` é uma concatenação ambígua de nomes com `+`. Cada (fil → nome) abaixo
# foi confirmado contra o `<title>Produtos, Autor X` que a própria loja emite
# (2026-05-15). Os dois últimos (Wantuil/Gama) vinham trocados na ordem da
# URL: fil=293894 é Zilda Gama, fil=293893 é Zêus Wantuil. `verify_author()`
# revalida em todo run e aborta se a loja divergir do esperado aqui.
# Nomes/slugs canonizados conforme convencoes-aliases.md.
AUTHORS: list[tuple[str, str, str]] = [
    ("293768", "Bezerra de Menezes", "bezerra-de-menezes"),
    ("293784", "Arthur Conan Doyle", "arthur-conan-doyle"),
    ("293801", "Deolindo Amorim", "deolindo-amorim"),
    ("293824", "Geraldo Campetti Sobrinho", "geraldo-campetti-sobrinho"),
    ("293828", "Haroldo Dutra Dias", "haroldo-dutra-dias"),
    ("293830", "Hermínio Corrêa de Miranda", "herminio-correa-de-miranda"),
    ("469243", "José Raul Teixeira", "jose-raul-teixeira"),
    ("298585", "Martins Peralva", "martins-peralva"),
    ("293870", "Richard Simonetti", "richard-simonetti"),
    ("293873", "Rodolfo Calligaris", "rodolfo-calligaris"),
    ("293878", "Suely Caldas Schubert", "suely-caldas-schubert"),
    ("293881", "Vinícius (Pedro de Camargo)", "vinicius"),
    ("293894", "Zilda Gama", "zilda-gama"),
    ("293893", "Zêus Wantuil", "zeus-wantuil"),
]

# Casa o nome que a loja declara no <title> ("Produtos, Autor X :: EDITORA FEB").
STORE_AUTHOR_RE = re.compile(r"<title>\s*Produtos,\s*Autor\s+([^:<]+?)\s*(?:::|</title>)")

LDJSON_RE = re.compile(
    r'<script type="application/ld\+json"[^>]*>(.*?)</script>', re.DOTALL
)
FOUND_RE = re.compile(r"Encontrados\s*<b>(\d+)</b>")


def fetch_page(
    fil: str, tfil: str, pag: int, *, delay: float, retries: int = 4
) -> str:
    params = {"fil": fil, "avancada": "true", "tfil": tfil}
    if pag > 1:
        params["pag"] = str(pag)
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "pt-BR,pt;q=0.9",
    }
    last_exc: Exception | None = None
    for attempt in range(retries):
        if delay:
            time.sleep(delay)
        try:
            r = requests.get(BASE, params=params, headers=headers, timeout=60)
            # 424/429/5xx da Fastcommerce = throttling — backoff exponencial.
            if r.status_code in (424, 429) or r.status_code >= 500:
                wait = 3 * (2 ** attempt)
                print(
                    f"    HTTP {r.status_code} (fil={fil} pag={pag}); "
                    f"retry em {wait}s [{attempt + 1}/{retries}]",
                    file=sys.stderr,
                )
                time.sleep(wait)
                continue
            r.raise_for_status()
            r.encoding = "iso-8859-1"
            return r.text
        except requests.RequestException as exc:  # noqa: PERF203
            last_exc = exc
            wait = 3 * (2 ** attempt)
            print(
                f"    {exc.__class__.__name__} (fil={fil} pag={pag}); "
                f"retry em {wait}s [{attempt + 1}/{retries}]",
                file=sys.stderr,
            )
            time.sleep(wait)
    raise SystemExit(
        f"ABORT: fil={fil} pag={pag} falhou após {retries} tentativas"
        + (f" ({last_exc})" if last_exc else " (HTTP throttling persistente)")
    )


def parse_products(html: str) -> list[dict]:
    out = []
    for blob in LDJSON_RE.findall(html):
        try:
            d = json.loads(blob.strip())
        except json.JSONDecodeError:
            continue
        if d.get("@type") != "Product":
            continue
        offers = d.get("offers") or {}
        out.append(
            {
                "titulo": (d.get("name") or "").strip(),
                "product_id": d.get("productID"),
                "sku": str(d.get("sku") or "").strip(),
                "preco": offers.get("price"),
                "url": offers.get("url", "").strip(),
            }
        )
    return out


def verify_author(html: str, fil: str, nome_esperado: str) -> None:
    """Aborta se a loja declarar um autor diferente do esperado p/ este fil.

    Trava de segurança contra reordenação fil↔nome na loja (foi exatamente
    isso que trocou Wantuil/Gama na URL original do usuário).
    """
    m = STORE_AUTHOR_RE.search(html)
    if not m:
        return  # loja mudou o template; não dá pra verificar, segue
    loja = m.group(1).strip()
    esperado = nome_esperado.split(" (")[0]  # "Vinícius (Pedro…)" -> "Vinícius"
    if slugify(loja) != slugify(esperado):
        raise SystemExit(
            f"ABORT: fil={fil} esperava '{esperado}' mas a loja FEB declara "
            f"'{loja}'. A tabela AUTHORS está dessincronizada com a loja — "
            f"corrigir antes de prosseguir (não criar páginas com autor errado)."
        )


def scrape_author(
    fil: str, nome: str, *, delay: float, max_pages: int = 25
) -> tuple[list[dict], int | None]:
    """Retorna (lista de produtos deduplicados, total declarado pela loja)."""
    tfil = nome.split(" (")[0]  # "Vinícius (Pedro de Camargo)" -> "Vinícius"
    seen: dict = {}
    declared: int | None = None
    for pag in range(1, max_pages + 1):
        html = fetch_page(fil, tfil, pag, delay=delay)
        if declared is None:
            verify_author(html, fil, nome)
            m = FOUND_RE.search(html)
            if m:
                declared = int(m.group(1))
        prods = parse_products(html)
        new = 0
        for p in prods:
            pid = p["product_id"]
            if pid in seen:
                continue
            seen[pid] = p
            new += 1
        if new == 0:
            break
        if declared is not None and len(seen) >= declared:
            break
    return list(seen.values()), declared


def raw_slugs_for(author_slug: str) -> set[str]:
    """Slugs de arquivos já baixados em raw/autores/<slug>/ (pdf/doc/md)."""
    base = ROOT / "raw" / "autores" / author_slug
    if not base.exists():
        return set()
    return {
        p.stem.lower()
        for p in base.iterdir()
        if p.is_file() and p.suffix.lower() in {".pdf", ".doc", ".docx", ".md"}
    }


def already_downloaded(titulo: str, raw_slugs: set[str]) -> bool:
    if not raw_slugs:
        return False
    t = slugify(titulo)
    if t in raw_slugs:
        return True
    # Match tolerante: títulos longos da loja vs. slug abreviado em raw/.
    t_tokens = {x for x in t.split("-") if len(x) > 2}
    for rs in raw_slugs:
        rs_tokens = {x for x in rs.split("-") if len(x) > 2}
        if not rs_tokens:
            continue
        common = t_tokens & rs_tokens
        smaller = min(len(t_tokens), len(rs_tokens)) or 1
        if len(common) >= 3 and len(common) / smaller >= 0.6:
            return True
    return False


def render_markdown(catalogo: list[dict], gerado_em: str) -> str:
    total = sum(len(a["obras"]) for a in catalogo)
    pend = sum(
        1 for a in catalogo for o in a["obras"] if not o["em_raw"]
    )
    lines = [
        "# Obras pendentes de download — catálogo FEB Editora",
        "",
        f"Gerado por `scripts/scrape_feb_catalogo.py` em {gerado_em}. "
        f"Tracker operacional (não é página da wiki — sem frontmatter, fora "
        f"do build público). Regenerável a qualquer momento.",
        "",
        f"**{total} obras** catalogadas em {len(catalogo)} autores · "
        f"**{pend} pendentes** de download para `raw/autores/<slug>/`.",
        "",
        "Marcação `[x]` = já existe arquivo correspondente em "
        "`raw/autores/<slug>/` (match heurístico por slug — conferir antes "
        "de assumir como baixado).",
        "",
    ]
    for a in catalogo:
        if not a["obras"]:
            continue
        n_pend = sum(1 for o in a["obras"] if not o["em_raw"])
        lines.append(
            f"## {a['nome']} ({len(a['obras'])} obras · {n_pend} pendentes)"
        )
        lines.append("")
        lines.append(
            f"- Página: [[wiki/personalidades/{a['slug']}]]"
            f"{' — *stub criado por este scrape*' if a['stub_criado'] else ''}"
        )
        lines.append(
            f"- Catálogo FEB: "
            f"<{BASE}?fil={a['fil']}&avancada=true"
            f"&tfil={a['tfil_q']}>"
        )
        lines.append("")
        for o in sorted(a["obras"], key=lambda x: x["titulo"].lower()):
            box = "x" if o["em_raw"] else " "
            preco = f" — R$ {o['preco']}" if o.get("preco") else ""
            lines.append(
                f"- [{box}] *{o['titulo']}*{preco} — "
                f"[FEB]({o['url']}) (SKU {o['sku']})"
            )
        lines.append("")
    return "\n".join(lines)


def relabel_from_json(json_path: Path, md_path: Path) -> int:
    """Re-rotula um JSON já scrapeado por `fil` com a tabela AUTHORS atual.

    Os livros por `fil` são autoritativos (vieram do filtro da loja); só os
    rótulos nome/slug podem estar dessincronizados se a tabela mudou (ex.:
    correção da troca Wantuil↔Gama). Recomputa `em_raw` e regenera o MD.
    Não acessa a rede — uso quando a loja está com throttling.
    """
    by_fil = {fil: (nome, slug) for fil, nome, slug in AUTHORS}
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    gerado_em = payload.get("gerado_em", date.today().isoformat())
    ordem = {fil: i for i, (fil, _, _) in enumerate(AUTHORS)}
    for a in payload["autores"]:
        nome, slug = by_fil[a["fil"]]
        a["nome"], a["slug"] = nome, slug
        a["tfil_q"] = nome.split(" (")[0].replace(" ", "+")
        raw_slugs = raw_slugs_for(slug)
        for o in a["obras"]:
            o["em_raw"] = already_downloaded(o["titulo"], raw_slugs)
    payload["autores"].sort(key=lambda a: ordem.get(a["fil"], 99))
    json_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    md_path.write_text(
        render_markdown(payload["autores"], gerado_em) + "\n",
        encoding="utf-8",
    )
    total = sum(len(a["obras"]) for a in payload["autores"])
    print(
        f"re-rotulado (sem rede): {total} obras em "
        f"{len(payload['autores'])} autores\n"
        f"JSON: {json_path.relative_to(ROOT)}\n"
        f"MD:   {md_path.relative_to(ROOT)}",
        file=sys.stderr,
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true",
                    help="scrape e conta, mas não grava arquivos")
    ap.add_argument("--only",
                    help="substring (case-insensitive) p/ filtrar autor")
    ap.add_argument("--delay", type=float, default=0.5,
                    help="delay entre requisições (default 0.5s)")
    ap.add_argument("--from-json", action="store_true",
                    help="não acessa a rede; re-rotula o JSON existente por "
                         "fil com a tabela AUTHORS corrigida e regenera o MD "
                         "(usar quando a loja estiver com throttling)")
    ap.add_argument("--json-out", type=Path,
                    default=ROOT / "data" / "feb-catalogo-autores.json")
    ap.add_argument("--md-out", type=Path,
                    default=ROOT / "OBRAS-PENDENTES-FEB.md")
    args = ap.parse_args(argv)

    if args.from_json:
        return relabel_from_json(args.json_out, args.md_out)

    authors = AUTHORS
    if args.only:
        needle = args.only.lower()
        authors = [
            a for a in AUTHORS
            if needle in a[1].lower() or needle in a[2]
        ]
        if not authors:
            print(f"erro: --only {args.only!r} não casou", file=sys.stderr)
            return 2

    gerado_em = date.today().isoformat()
    catalogo = []
    grand_total = 0
    for i, (fil, nome, slug) in enumerate(authors, 1):
        print(f"[{i}/{len(authors)}] {nome} (fil={fil})", file=sys.stderr)
        obras, declared = scrape_author(fil, nome, delay=args.delay)
        raw_slugs = raw_slugs_for(slug)
        for o in obras:
            o["em_raw"] = already_downloaded(o["titulo"], raw_slugs)
        n_pend = sum(1 for o in obras if not o["em_raw"])
        flag = "" if declared is None or declared == len(obras) else \
            f"  (loja declara {declared}!)"
        print(
            f"    {len(obras)} obras · {n_pend} pendentes{flag}",
            file=sys.stderr,
        )
        grand_total += len(obras)
        catalogo.append(
            {
                "nome": nome,
                "slug": slug,
                "fil": fil,
                "tfil_q": nome.split(" (")[0].replace(" ", "+"),
                "declarado_loja": declared,
                "stub_criado": False,  # marcado depois pelo passo de stubs
                "obras": obras,
            }
        )

    print(f"\nTOTAL: {grand_total} obras em {len(catalogo)} autores",
          file=sys.stderr)

    if args.dry_run:
        print("(dry-run: nada gravado)", file=sys.stderr)
        return 0

    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    payload = {"gerado_em": gerado_em, "fonte": BASE, "autores": catalogo}
    args.json_out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"JSON: {args.json_out.relative_to(ROOT)}", file=sys.stderr)

    args.md_out.write_text(
        render_markdown(catalogo, gerado_em) + "\n", encoding="utf-8"
    )
    print(f"MD:   {args.md_out.relative_to(ROOT)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
