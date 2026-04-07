#!/usr/bin/env python3
# Executar sempre com python3
"""
Lint determinístico da wiki IsAbel.

Roda todos os checks mecânicos definidos na seção 8 do CLAUDE.md e imprime
um JSON estruturado em stdout para consumo pela skill /lint.

Sem dependências externas — apenas stdlib.
"""

import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

WIKI_DIR = Path("wiki")
INDEX_PATH = Path("index.md")
STALE_DAYS = 14

# ---------------------------------------------------------------------------
# Utilitários
# ---------------------------------------------------------------------------

def parse_frontmatter(path: Path) -> tuple[dict, list[str]]:
    """Extrai frontmatter YAML simples (scalars e listas [a, b]).

    Retorna (fm_dict, lista_de_chaves_duplicadas).
    """
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, []
    fm: dict = {}
    duplicates: list[str] = []
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()
        if val.startswith("[") and val.endswith("]"):
            val = [v.strip() for v in val[1:-1].split(",") if v.strip()]
        if key in fm:
            duplicates.append(key)
        fm[key] = val
    return fm, duplicates


def find_wikilinks(text: str) -> list[tuple[int, str]]:
    """Retorna lista de (linha, target) para cada wikilink no texto."""
    results = []
    for i, line in enumerate(text.splitlines(), 1):
        for m in re.finditer(r"\[\[([^\]|#]+)", line):
            results.append((i, m.group(1).strip()))
    return results


def resolve_wikilink(link: str) -> Path:
    """Converte wikilink target em caminho de arquivo."""
    p = Path(link)
    if p.suffix != ".md":
        p = p.with_suffix(".md")
    return p


def collect_pages() -> list[Path]:
    """Retorna todos os .md dentro de wiki/."""
    return sorted(WIKI_DIR.rglob("*.md"))


def page_key(path: Path) -> str:
    """Converte Path em formato de wikilink (sem .md)."""
    return str(path.with_suffix(""))


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def check_broken_links(pages: list[Path]) -> dict:
    """Check 4 — wikilinks apontando para arquivos inexistentes."""
    items = []
    for page in pages:
        text = page.read_text(encoding="utf-8")
        for lineno, target in find_wikilinks(text):
            resolved = resolve_wikilink(target)
            if not resolved.exists():
                items.append({
                    "source": str(page),
                    "line": lineno,
                    "target": target,
                })
    # Também checar index.md
    text = INDEX_PATH.read_text(encoding="utf-8")
    for lineno, target in find_wikilinks(text):
        resolved = resolve_wikilink(target)
        if not resolved.exists():
            items.append({
                "source": str(INDEX_PATH),
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


def check_index_sync(pages: list[Path]) -> dict:
    """Check 7 — index.md desatualizado vs arquivos reais."""
    # Links no index
    text = INDEX_PATH.read_text(encoding="utf-8")
    index_targets = set()
    for _, target in find_wikilinks(text):
        if target.startswith("wiki/"):
            index_targets.add(target)

    # Arquivos reais
    disk_keys = {page_key(p) for p in pages}

    on_disk_not_in_index = sorted(disk_keys - index_targets)
    in_index_not_on_disk = sorted(index_targets - disk_keys)

    items = []
    for p in in_index_not_on_disk:
        items.append({"detail": f"no index mas arquivo não existe: {p}"})
    for p in on_disk_not_in_index:
        items.append({"detail": f"arquivo existe mas falta no index: {p}"})

    return {
        "severity": "error",
        "count": len(items),
        "items": items,
    }


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
    """Check 1 — divergências com status: aberta e pouco conteúdo."""
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
        items.append({
            "path": str(page),
            "body_lines": body_lines,
            "possibly_incomplete": body_lines < 20,
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
]
_VALID_RE = re.compile("|".join(_CITATION_VALID))

# Siglas que indicam citação doutrinária
_BOOK_SIGLAS = re.compile(
    r"\((LE|LM|ESE|C&I|Gênese|RE|OPE|OQE)\s*,"
)


def check_citation_format(pages: list[Path]) -> dict:
    """Check 6 — citações com sigla conhecida mas formato não reconhecido."""
    items = []
    for page in pages:
        text = page.read_text(encoding="utf-8")
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


def check_frontmatter(pages: list[Path]) -> dict:
    """Check extra — frontmatter com campos obrigatórios ausentes."""
    required = {"tipo", "fontes", "tags", "atualizado_em", "status"}
    valid_tipos = {"conceito", "obra", "entidade", "questao", "sintese", "divergencia"}
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


def main():
    if not WIKI_DIR.exists():
        print(json.dumps({"error": "Diretório wiki/ não encontrado"}), file=sys.stdout)
        sys.exit(1)

    pages = collect_pages()

    checks = {
        "broken_links": check_broken_links(pages),
        "index_desync": check_index_sync(pages),
        "frontmatter": check_frontmatter(pages),
        "orphan_pages": check_orphan_pages(pages),
        "fontes_missing": check_fontes_section(pages),
        "citation_format": check_citation_format(pages),
        "rascunho_stale": check_rascunho_stale(pages),
        "divergencias_aberta": check_divergencias_aberta(pages),
        "missing_concept_pages": check_missing_concept_pages(pages),
    }

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
