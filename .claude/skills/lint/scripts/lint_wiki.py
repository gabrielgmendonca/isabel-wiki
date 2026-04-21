#!/usr/bin/env python3
# Executar sempre com python3
"""
Lint determinístico da wiki IsAbel.

Roda todos os checks mecânicos definidos na seção 8 do CLAUDE.md e imprime
um JSON estruturado em stdout para consumo pela skill /lint.

Sem dependências externas — apenas stdlib.
"""

import argparse
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

# Permitir `from _lib.wiki_utils import ...` (raiz em .claude/skills/)
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _lib.wiki_utils import (  # noqa: E402
    INDEX_PATH,
    WIKI_DIR,
    collect_pages,
    find_wikilinks,
    page_key,
    parse_frontmatter,
    resolve_wikilink,
    strip_inline_code,
)

STALE_DAYS = 14

# A listagem linear da wiki vive em wiki/sinteses/catalogo.md. A home (index.md)
# virou landing minimalista de trilhas e não é mais fonte de catálogo.
CATALOG_PATH = WIKI_DIR / "sinteses" / "catalogo.md"


def _collect_catalog_targets() -> set[str]:
    targets: set[str] = set()
    if not CATALOG_PATH.exists():
        return targets
    text = CATALOG_PATH.read_text(encoding="utf-8")
    for _, target in find_wikilinks(text):
        if target.startswith("wiki/"):
            targets.add(target)
    return targets


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def check_broken_links(pages: list[Path]) -> dict:
    """Check 4 — wikilinks apontando para arquivos inexistentes."""
    items = []
    sources = list(pages)
    if INDEX_PATH.exists():
        sources.append(INDEX_PATH)
    for page in sources:
        text = page.read_text(encoding="utf-8")
        for lineno, target in find_wikilinks(text):
            resolved = resolve_wikilink(target)
            if not resolved.exists():
                items.append({
                    "source": str(page),
                    "line": lineno,
                    "target": target,
                })
    return {"severity": "error", "count": len(items), "items": items}


def check_orphan_pages(pages: list[Path]) -> dict:
    """Check 2 — páginas sem nenhum link de entrada (excluindo index.md como fonte)."""
    all_keys = {page_key(p) for p in pages}
    incoming: dict[str, list[str]] = {k: [] for k in all_keys}

    for page in pages:
        text = page.read_text(encoding="utf-8")
        src = page_key(page)
        for _, target in find_wikilinks(text):
            key = target.rstrip("/")
            if key in incoming and key != src:
                incoming[key].append(str(page))

    orphans = [k for k, sources in incoming.items() if not sources]
    items = [{"path": k + ".md"} for k in sorted(orphans)]
    return {"severity": "warning", "count": len(items), "items": items}


def check_fontes_section(pages: list[Path]) -> dict:
    """Check 5 — ## Fontes ausente ou vazia."""
    items = []
    for page in pages:
        text = page.read_text(encoding="utf-8")
        match = re.search(r"^## Fontes\s*$", text, re.MULTILINE)
        if not match:
            items.append({"path": str(page), "detail": "seção ## Fontes ausente"})
            continue
        # Conteúdo entre ## Fontes e próximo ## (ou EOF)
        after = text[match.end():]
        next_section = re.search(r"^## ", after, re.MULTILINE)
        content = after[:next_section.start()] if next_section else after
        non_blank = [l for l in content.strip().splitlines() if l.strip()]
        if not non_blank:
            items.append({"path": str(page), "detail": "seção ## Fontes vazia"})
    return {"severity": "warning", "count": len(items), "items": items}


def check_catalogo_broken(pages: list[Path]) -> dict:
    """Check 7a — catalogo.md aponta para arquivos inexistentes (erro)."""
    catalog_targets = _collect_catalog_targets()
    disk_keys = {page_key(p) for p in pages}
    in_catalog_not_on_disk = sorted(catalog_targets - disk_keys)
    items = [{"detail": f"no catálogo mas arquivo não existe: {p}"} for p in in_catalog_not_on_disk]
    return {"severity": "error", "count": len(items), "items": items}


def check_catalogo_missing(pages: list[Path]) -> dict:
    """Check 7b — arquivos em wiki/ ausentes do catalogo.md (aviso).

    Páginas com `index: false` no frontmatter são excluídas explicitamente.
    """
    catalog_targets = _collect_catalog_targets()

    disk_keys = set()
    for p in pages:
        fm, _ = parse_frontmatter(p)
        if str(fm.get("index", "")).lower() == "false":
            continue
        disk_keys.add(page_key(p))

    on_disk_not_in_catalog = sorted(disk_keys - catalog_targets)
    items = [{"detail": f"arquivo existe mas falta no catálogo: {p}"} for p in on_disk_not_in_catalog]
    return {"severity": "warning", "count": len(items), "items": items}


def check_rascunho_stale(pages: list[Path]) -> dict:
    """Check 8 — páginas com status: rascunho há mais de STALE_DAYS."""
    today = date.today()
    items = []
    for page in pages:
        fm, _ = parse_frontmatter(page)
        if fm.get("status") != "rascunho":
            continue
        atualizado = fm.get("atualizado_em", "")
        try:
            dt = datetime.strptime(atualizado, "%Y-%m-%d").date()
            days = (today - dt).days
        except ValueError:
            days = -1  # data inválida — reportar também
        if days > STALE_DAYS or days < 0:
            items.append({
                "path": str(page),
                "atualizado_em": atualizado,
                "dias": days,
            })
    return {"severity": "warning", "count": len(items), "items": items}


def check_divergencias_aberta(pages: list[Path]) -> dict:
    """Check 1 — divergências com status: aberta que parecem incompletas.

    Divergências com status: aberta são intencionais (o conflito teológico
    permanece em aberto). Só sinaliza aquelas com corpo < 20 linhas, que
    sugerem stub/análise pendente.
    """
    div_dir = WIKI_DIR / "divergencias"
    items = []
    if not div_dir.exists():
        return {"severity": "info", "count": 0, "items": []}
    for page in div_dir.glob("*.md"):
        fm, _ = parse_frontmatter(page)
        if fm.get("status") != "aberta":
            continue
        text = page.read_text(encoding="utf-8")
        # Contar linhas após frontmatter
        in_fm = False
        body_lines = 0
        for line in text.splitlines():
            if line.strip() == "---":
                in_fm = not in_fm
                continue
            if not in_fm:
                if line.strip():
                    body_lines += 1
        if body_lines >= 20:
            continue  # análise completa, não é issue
        items.append({
            "path": str(page),
            "body_lines": body_lines,
            "possibly_incomplete": True,
        })
    return {"severity": "info", "count": len(items), "items": items}


def check_missing_concept_pages(pages: list[Path]) -> dict:
    """Check 3 — links para wiki/conceitos/X onde X.md não existe."""
    items = []
    seen = set()
    all_sources = list(pages) + [INDEX_PATH]
    for page in all_sources:
        text = page.read_text(encoding="utf-8")
        for lineno, target in find_wikilinks(text):
            if target.startswith("wiki/conceitos/"):
                resolved = resolve_wikilink(target)
                if not resolved.exists() and target not in seen:
                    seen.add(target)
                    items.append({"target": target, "first_seen_in": str(page), "line": lineno})
    return {"severity": "info", "count": len(items), "items": items}


# Padrões válidos de citação (seção 4 do CLAUDE.md + variantes reais)
_CITATION_VALID = [
    # LE
    r"\(LE,\s*q\.\s*\d+",
    r"\(LE,\s*Introdução",
    r"\(LE,\s*Conclusão",
    r"\(LE,\s*Prolegômenos",
    r"\(LE,\s*Nota\s",
    r"\(LE,\s*Parte\s*\d",
    # LM
    r"\(LM,\s*[12][ªa]\s*parte",
    r"\(LM,\s*caps?\.\s*[IVXLC]+",
    r"\(LM,\s*Introdução",
    # ESE
    r"\(ESE,\s*caps?\.\s*[IVXLC]+",
    r"\(ESE,\s*Introdução",
    r"\(ESE,\s*Prefácio",
    # C&I
    r"\(C&I,\s*[12][ªa]\s*parte",
    r"\(C&I,\s*Prefácio",
    r"\(C&I,\s*Introdução",
    # Gênese
    r"\(Gênese,\s*caps?\.\s*[IVXLC]+",
    r"\(Gênese,\s*Introdução",
    r"\(Gênese,\s*Prefácio",
    # Complementares
    r"\(RE,\s*",
    r"\(OPE,\s*",
    r"\(OQE,\s*",
    # Referências contextuais genéricas (ano de publicação ou marcador estrutural)
    r"\((LE|LM|ESE|C&I|Gênese|RE|OPE|OQE),\s*\d{4}",
    r"\((LE|LM|ESE|C&I|Gênese|RE|OPE|OQE),\s*(epígrafe|subtítulo|Prolegômenos)",
]
_VALID_RE = re.compile("|".join(_CITATION_VALID))

# Siglas que indicam citação doutrinária
_BOOK_SIGLAS = re.compile(
    r"\((LE|LM|ESE|C&I|Gênese|RE|OPE|OQE)\s*,"
)


def check_citation_format(pages: list[Path]) -> dict:
    """Check 6 — citações com sigla conhecida mas formato não reconhecido.

    Conteúdo dentro de backticks é ignorado para evitar falsos positivos em
    exemplos/placeholders como `(LE, q. N)` ou `(LM, Nª parte, cap. X)`.
    """
    items = []
    for page in pages:
        text = strip_inline_code(page.read_text(encoding="utf-8"))
        for i, line in enumerate(text.splitlines(), 1):
            for m in _BOOK_SIGLAS.finditer(line):
                # Extrair a citação completa entre parênteses
                start = m.start()
                depth = 0
                end = start
                for j in range(start, len(line)):
                    if line[j] == "(":
                        depth += 1
                    elif line[j] == ")":
                        depth -= 1
                        if depth == 0:
                            end = j + 1
                            break
                citation = line[start:end]
                if not _VALID_RE.search(citation):
                    items.append({
                        "path": str(page),
                        "line": i,
                        "citation": citation,
                    })
    return {"severity": "warning", "count": len(items), "items": items}


def find_urls(text: str) -> list[tuple[int, str]]:
    """Retorna lista de (linha, url) para cada URL http(s) no texto."""
    results = []
    url_re = re.compile(r"https?://[^\s\)\]>\"'`]+")
    for i, line in enumerate(text.splitlines(), 1):
        for m in url_re.finditer(line):
            results.append((i, m.group(0).rstrip(".,;:!?")))
    return results


def check_broken_urls(pages: list[Path]) -> dict:
    """Check — URLs externas (http/https) que retornam erro ou timeout."""
    # Coletar todas as URLs únicas com suas origens
    url_sources: dict[str, list[dict]] = {}
    all_sources = list(pages) + [INDEX_PATH]
    for page in all_sources:
        text = page.read_text(encoding="utf-8")
        for lineno, url in find_urls(text):
            if url not in url_sources:
                url_sources[url] = []
            url_sources[url].append({"source": str(page), "line": lineno})

    items = []
    for url, sources in sorted(url_sources.items()):
        try:
            req = Request(url, method="HEAD", headers={"User-Agent": "IsAbel-Wiki-Lint/1.0"})
            resp = urlopen(req, timeout=10)
            status = resp.status
            if status >= 400:
                items.append({"url": url, "status": status, "sources": sources})
        except HTTPError as e:
            items.append({"url": url, "status": e.code, "sources": sources})
        except (URLError, OSError, ValueError) as e:
            items.append({"url": url, "status": str(e), "sources": sources})

    return {"severity": "warning", "count": len(items), "items": items}


# ---------------------------------------------------------------------------
# Tags — conjuntos canônicos
# ---------------------------------------------------------------------------

VALID_LEI_TAGS = {
    "lei/adoracao", "lei/trabalho", "lei/reproducao", "lei/conservacao",
    "lei/destruicao", "lei/sociedade", "lei/progresso", "lei/igualdade",
    "lei/liberdade", "lei/justica-amor-caridade",
}

FONTES_TO_OBRA = {
    "LE": "obra/le", "LM": "obra/lm", "ESE": "obra/ese",
    "C&I": "obra/ci", "Gênese": "obra/genese",
    "OPE": "obra/ope", "OQE": "obra/oqe", "RE": "obra/re",
}


def check_tag_taxonomy(pages: list[Path]) -> dict:
    """Check — tags lei/ e obra/ devem pertencer a conjuntos canônicos e ser consistentes com fontes."""
    items = []
    for page in pages:
        fm, _ = parse_frontmatter(page)
        tags = fm.get("tags", [])
        if isinstance(tags, str):
            tags = [tags]
        fontes = fm.get("fontes", [])
        if isinstance(fontes, str):
            fontes = [fontes]

        # Validar tags lei/
        for tag in tags:
            if tag.startswith("lei/") and tag not in VALID_LEI_TAGS:
                items.append({
                    "path": str(page),
                    "detail": f"tag lei/ inválida: {tag} (valores válidos: {', '.join(sorted(VALID_LEI_TAGS))})",
                })

        # Validar que obra/ tags são consistentes com fontes
        obra_tags = {t for t in tags if t.startswith("obra/")}
        expected_obra = {FONTES_TO_OBRA[f] for f in fontes if f in FONTES_TO_OBRA}

        # Tags obra/ que não correspondem a nenhuma fonte
        extra_obra = obra_tags - expected_obra
        for t in sorted(extra_obra):
            items.append({
                "path": str(page),
                "detail": f"tag {t} sem fonte correspondente no campo fontes",
            })

        # Fontes canônicas sem tag obra/ correspondente
        missing_obra = expected_obra - obra_tags
        for t in sorted(missing_obra):
            items.append({
                "path": str(page),
                "detail": f"fonte presente mas tag {t} ausente",
            })

    return {"severity": "warning", "count": len(items), "items": items}


PENTATEUCO_SLUGS = {
    "livro-dos-espiritos",
    "livro-dos-mediuns",
    "evangelho-segundo-o-espiritismo",
    "genese",
    "ceu-e-inferno",
}


def check_pentateuco_completo(pages: list[Path]) -> dict:
    """Check — Pentateuco deve ter os 5 arquivos canônicos (erro)."""
    obras_dir = WIKI_DIR / "obras"
    pentateuco_missing = [
        s for s in sorted(PENTATEUCO_SLUGS)
        if not (obras_dir / f"{s}.md").exists()
    ]
    items = []
    if pentateuco_missing:
        items.append({
            "detail": f"Pentateuco incompleto — faltam: {', '.join(pentateuco_missing)}",
        })
    return {"severity": "error", "count": len(items), "items": items}


def check_status_projeto(pages: list[Path]) -> dict:
    """Check — contagens prosa do 'Status do projeto' em index.md (info).

    Só reporta quando uma contagem está presente e divergente. Ausência é OK:
    métricas agora vivem em `wiki/sinteses/estatisticas-da-wiki.md`.
    """
    obras_dir = WIKI_DIR / "obras"
    obras_pages = sorted(obras_dir.glob("*.md")) if obras_dir.exists() else []
    n_complementares = sum(
        1 for o in obras_pages if o.stem not in PENTATEUCO_SLUGS
    )
    total_paginas = len(pages)
    text = INDEX_PATH.read_text(encoding="utf-8")
    items = []

    m_fontes = re.search(r"(\d+)\s*fontes?\s*complementares?", text)
    if m_fontes:
        idx_fontes = int(m_fontes.group(1))
        if idx_fontes != n_complementares:
            items.append({
                "detail": f"index.md diz {idx_fontes} fontes complementares, mas há {n_complementares}",
            })

    m_paginas = re.search(r"~?(\d+)\s*páginas?", text)
    if m_paginas:
        idx_paginas = int(m_paginas.group(1))
        if idx_paginas != total_paginas:
            items.append({
                "detail": f"index.md diz ~{idx_paginas} páginas, mas há {total_paginas}",
            })

    return {"severity": "info", "count": len(items), "items": items}


def check_frontmatter(pages: list[Path]) -> dict:
    """Check extra — frontmatter com campos obrigatórios ausentes."""
    required = {"tipo", "fontes", "tags", "atualizado_em", "status"}
    valid_tipos = {"conceito", "obra", "personalidade", "questao", "aprofundamento", "sintese", "divergencia"}
    valid_status = {"rascunho", "ativo", "revisar"}
    valid_status_divergencia = {"aberta", "concluída"}
    items = []
    for page in pages:
        fm, duplicates = parse_frontmatter(page)
        if duplicates:
            items.append({"path": str(page), "detail": f"chaves duplicadas: {', '.join(duplicates)}"})
        missing = required - set(fm.keys())
        if missing:
            items.append({"path": str(page), "detail": f"campos ausentes: {', '.join(sorted(missing))}"})
            continue
        if fm["tipo"] not in valid_tipos:
            items.append({"path": str(page), "detail": f"tipo inválido: {fm['tipo']}"})
        allowed_status = valid_status_divergencia if fm["tipo"] == "divergencia" else valid_status
        if fm["status"] not in allowed_status:
            items.append({"path": str(page), "detail": f"status inválido: {fm['status']}"})
    return {"severity": "error", "count": len(items), "items": items}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def compute_stats(pages: list[Path]) -> dict:
    by_tipo: dict[str, int] = {}
    for page in pages:
        fm, _ = parse_frontmatter(page)
        tipo = fm.get("tipo", "desconhecido")
        by_tipo[tipo] = by_tipo.get(tipo, 0) + 1
    return {"total": len(pages), "by_tipo": by_tipo}


CHECK_REGISTRY = {
    "broken_links": check_broken_links,
    "catalogo_broken": check_catalogo_broken,
    "catalogo_missing": check_catalogo_missing,
    "frontmatter": check_frontmatter,
    "orphan_pages": check_orphan_pages,
    "fontes_missing": check_fontes_section,
    "citation_format": check_citation_format,
    "rascunho_stale": check_rascunho_stale,
    "divergencias_aberta": check_divergencias_aberta,
    "missing_concept_pages": check_missing_concept_pages,
    "pentateuco_completo": check_pentateuco_completo,
    "status_projeto": check_status_projeto,
    "broken_urls": check_broken_urls,
    "tag_taxonomy": check_tag_taxonomy,
}

# Checks rodados por padrão. broken_urls é opt-in via --check-urls (I/O externo).
DEFAULT_SKIP = {"broken_urls"}


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Lint determinístico da wiki IsAbel")
    p.add_argument("--check", action="append", default=[], metavar="NAME",
                   help="Rodar apenas os checks listados (repetível).")
    p.add_argument("--skip", action="append", default=[], metavar="NAME",
                   help="Pular os checks listados (repetível).")
    p.add_argument("--check-urls", action="store_true",
                   help="Habilita check broken_urls (I/O externo, opt-in).")
    return p.parse_args(argv)


def select_checks(args: argparse.Namespace) -> list[str]:
    all_names = list(CHECK_REGISTRY.keys())
    unknown = [n for n in (args.check + args.skip) if n not in CHECK_REGISTRY]
    if unknown:
        print(json.dumps({"error": f"Check desconhecido: {', '.join(unknown)}",
                          "valid": all_names}), file=sys.stdout)
        sys.exit(2)
    if args.check:
        selected = [n for n in all_names if n in args.check]
    else:
        selected = [n for n in all_names if n not in DEFAULT_SKIP]
        if args.check_urls and "broken_urls" not in selected:
            selected.append("broken_urls")
    selected = [n for n in selected if n not in args.skip]
    return selected


def main(argv: list[str] | None = None):
    args = parse_args(argv if argv is not None else sys.argv[1:])

    if not WIKI_DIR.exists():
        print(json.dumps({"error": "Diretório wiki/ não encontrado"}), file=sys.stdout)
        sys.exit(1)

    pages = collect_pages()
    selected = select_checks(args)
    checks = {name: CHECK_REGISTRY[name](pages) for name in selected}

    errors = sum(1 for c in checks.values() if c["severity"] == "error" and c["count"] > 0)
    warnings = sum(1 for c in checks.values() if c["severity"] == "warning" and c["count"] > 0)
    infos = sum(1 for c in checks.values() if c["severity"] == "info" and c["count"] > 0)
    total_items = sum(c["count"] for c in checks.values())

    result = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "stats": compute_stats(pages),
        "checks": checks,
        "summary": f"{total_items} achados: {errors} categorias com erro, {warnings} com aviso, {infos} info",
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))

    if errors > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
