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
import unicodedata
from datetime import date, datetime
from functools import lru_cache
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

# Permitir `from _slug import ...` (top-level scripts/ do repo)
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "scripts"))
from _slug import (  # noqa: E402
    RAW_TOP_LEVEL_DIRS,
    canonical_for,
    has_artifact_marker,
    is_canonical_slug,
)
from kardec_structure import (  # noqa: E402
    SIGLA_NORM,
    load_structures,
    resolve_locus,
)
from link_citations import KARDEC_RE  # noqa: E402
from cite import literal_text  # noqa: E402
from reverse_locus import (  # noqa: E402
    _ELISION_RE,
    classify,
    normalize as _normalize_quote,
    word_coverage as _word_coverage,
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
        if not target.startswith("wiki/"):
            continue
        # Normalizar [[wiki/conceitos/leis-morais]] para a key real do index.md
        # quando o link aponta para uma pasta com index.md.
        resolved = resolve_wikilink(target)
        if resolved.exists() and resolved.name == "index.md" and not target.endswith("/index"):
            targets.add(str(resolved.with_suffix("")))
        else:
            targets.add(target)
    return targets


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

# Corpus de fonte publicado verbatim (Bíblia NT + Pentateuco): o próprio texto é
# a fonte, sem ## Fontes, sem tags tema/*, fora do catálogo curado, e não auditado
# por links/órfãos como as páginas curadas. Espelha o tratamento da Bíblia.
_CORPUS_TIPOS = {
    "capitulo-biblico", "livro-biblico",
    "capitulo-pentateuco", "obra-pentateuco",
}


def check_broken_links(pages: list[Path]) -> dict:
    """Check 4 — wikilinks apontando para arquivos inexistentes."""
    items = []
    sources = list(pages)
    if INDEX_PATH.exists():
        sources.append(INDEX_PATH)
    for page in sources:
        fm, _ = parse_frontmatter(page)
        # Capítulos do Pentateuco são texto verbatim do raw, que traz marcadores
        # de nota de rodapé `[[1]](#_ftnref1)` — wikilinks aparentes que não são
        # cross-links curados. Não auditar (alterá-los mexeria no texto do Kardec).
        if fm.get("tipo") == "capitulo-pentateuco":
            continue
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
    """Check 2 — páginas sem nenhum link de entrada (excluindo index.md como fonte).

    Páginas com `index: false` no frontmatter são excluídas — landings/meta-índices
    cuja função é receber visitas via Explorer/breadcrumb, não via wikilink.
    """
    excluded_keys: set[str] = set()
    for p in pages:
        fm, _ = parse_frontmatter(p)
        if str(fm.get("index", "")).lower() == "false":
            excluded_keys.add(page_key(p))
        if fm.get("tipo") in _CORPUS_TIPOS:
            excluded_keys.add(page_key(p))

    all_keys = {page_key(p) for p in pages} - excluded_keys
    incoming: dict[str, list[str]] = {k: [] for k in all_keys}

    for page in pages:
        text = page.read_text(encoding="utf-8")
        src = page_key(page)
        for _, target in find_wikilinks(text):
            key = target.rstrip("/")
            if key not in incoming:
                # Pasta com index.md: [[wiki/conceitos/leis-morais]] resolve para
                # wiki/conceitos/leis-morais/index.
                folder_key = key + "/index"
                if folder_key in incoming:
                    key = folder_key
            if key in incoming and key != src:
                incoming[key].append(str(page))

    orphans = [k for k, sources in incoming.items() if not sources]
    items = [{"path": k + ".md"} for k in sorted(orphans)]
    return {"severity": "warning", "count": len(items), "items": items}


def check_fontes_section(pages: list[Path]) -> dict:
    """Check 5 — ## Fontes ausente ou vazia.

    Skip: `capitulo-biblico` e `livro-biblico` — o próprio texto é a fonte.
    """
    items = []
    for page in pages:
        fm, _ = parse_frontmatter(page)
        if fm.get("tipo") in _CORPUS_TIPOS:
            continue
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
        if fm.get("tipo") in _CORPUS_TIPOS:
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


def _collect_missing_concepts(pages: list[Path]) -> dict[str, list[dict]]:
    """Agrega wikilinks para wiki/conceitos/X onde X.md não existe.

    Retorna dict[target, list[{source, line}]] preservando todas as ocorrências
    (sem deduplicar por source) para que `frequent_missing_concepts` possa
    contar páginas distintas que referenciam o mesmo conceito.
    """
    refs: dict[str, list[dict]] = {}
    all_sources = list(pages) + [INDEX_PATH]
    for page in all_sources:
        if not page.exists():
            continue
        text = page.read_text(encoding="utf-8")
        for lineno, target in find_wikilinks(text):
            if not target.startswith("wiki/conceitos/"):
                continue
            if resolve_wikilink(target).exists():
                continue
            refs.setdefault(target, []).append({"source": str(page), "line": lineno})
    return refs


def check_missing_concept_pages(pages: list[Path]) -> dict:
    """Check 3 — links para wiki/conceitos/X onde X.md não existe.

    Agrupado por target com contagem de páginas distintas que o referenciam.
    `frequent_missing_concepts` filtra esta lista por count >= 5.
    """
    refs = _collect_missing_concepts(pages)
    items = []
    for target in sorted(refs):
        sources = refs[target]
        unique_sources = sorted({s["source"] for s in sources})
        items.append({
            "target": target,
            "count": len(unique_sources),
            "sources": unique_sources[:3],
            "first_seen_in": sources[0]["source"],
            "line": sources[0]["line"],
        })
    return {"severity": "info", "count": len(items), "items": items}


FREQUENT_MISSING_THRESHOLD = 5


def check_frequent_missing_concepts(pages: list[Path]) -> dict:
    """Check — conceitos referenciados em FREQUENT_MISSING_THRESHOLD+ páginas mas sem página própria.

    Subconjunto warning-level de `missing_concept_pages`: indica conceitos que
    já circulam pelo corpo da wiki como wikilink mas continuam sem página, e
    portanto têm prioridade alta para virar página própria.
    """
    refs = _collect_missing_concepts(pages)
    items = []
    for target in sorted(refs):
        unique_sources = sorted({s["source"] for s in refs[target]})
        if len(unique_sources) >= FREQUENT_MISSING_THRESHOLD:
            items.append({
                "target": target,
                "count": len(unique_sources),
                "sources": unique_sources,
            })
    return {"severity": "warning", "count": len(items), "items": items}


# Tipos doutrinários onde citação é esperada. obras/personalidades/sinteses/divergencias
# têm estrutura própria (descritivos, comparativos, meta) e são excluídos do check.
LOW_CITATION_TIPOS = {"conceito", "aprofundamento", "questao"}
LOW_CITATION_MIN_WORDS = 200
LOW_CITATION_MIN_CITATIONS = 2

# Citações reconhecidas para `low_citations`: parentéticas com sigla do Pentateuco /
# complementares Kardec (`cf.` opcional), livros bíblicos canônicos por nome ou
# abreviação ACF (com prefixo opcional `S.`/`São`), ou autor/médium + obra em itálico.
# Para RE/LM/ESE/Gênese, aceita também sigla seguida de espaço + marcador estrutural
# (ex.: `(RE dez/1868)`, `(LM cap. XXIX)`) — forma curta de uso editorial.
_CITATION_COUNT_RE = re.compile(
    r"\((?:cf\.\s+)?(?:LE|LM|ESE|C&I|Gênese|RE|OPE|OQE)"
    r"(?:\s*[,)]"
    r"|\s+(?:caps?\.|q\.|item|p\.|\d|jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez))"
    r"|\((?:cf\.\s+)?(?:S\.\s+|São\s+|Sta\.\s+|Santa\s+)?"
    r"(?:Mateus|Marcos|Lucas|João|Atos|Romanos|Tiago|Hebreus|Apocalipse"
    r"|1?-?\s*Coríntios|2-?\s*Coríntios|Gálatas|Efésios|Filipenses|Colossenses"
    r"|1?-?\s*Tessalonicenses|2-?\s*Tessalonicenses|1?-?\s*Timóteo|2-?\s*Timóteo"
    r"|Tito|Filemom|1?-?\s*Pedro|2-?\s*Pedro|1?-?\s*João|2-?\s*João|3-?\s*João|Judas"
    # Abreviações ACF: Mt, Mc, Lc, Jo, At, Rm, 1Co, 2Co, Gl, Ef, Fp, Cl,
    # 1Ts, 2Ts, 1Tm, 2Tm, Tt, Fm, Hb, Tg, 1Pe, 2Pe, 1Jo, 2Jo, 3Jo, Jd, Ap.
    r"|Mt|Mc|Lc|Jo|At|Rm|[123]?Co|Gl|Ef|Fp|Cl|[12]?Ts|[12]?Tm"
    r"|Tt|Fm|Hb|Tg|[12]?Pe|[123]?Jo|Jd|Ap)"
    r"[,\s]+\d"
    r"|\([A-ZÀ-Ú][^)]*?,\s*\*[^*]+\*"
)


def _body_for_metrics(text: str) -> str:
    """Retorna o corpo da página sem frontmatter, ## Fontes e inline code."""
    body = re.sub(r"^---.*?^---", "", text, count=1, flags=re.DOTALL | re.MULTILINE)
    body = strip_inline_code(body)
    fontes = re.search(r"^## Fontes\s*$", body, re.MULTILINE)
    if fontes:
        body = body[: fontes.start()]
    return body


def check_low_citations(pages: list[Path]) -> dict:
    """Check — páginas doutrinárias com corpo substantivo mas poucas citações.

    Aplica-se a `tipo: conceito | aprofundamento | questao`. Páginas com
    body >= LOW_CITATION_MIN_WORDS palavras e menos de
    LOW_CITATION_MIN_CITATIONS citações reconhecidas são candidatas a
    enriquecimento. Tipos descritivos (`obra`, `personalidade`) e meta
    (`sintese`, `divergencia`) são excluídos.
    """
    items = []
    for page in pages:
        fm, _ = parse_frontmatter(page)
        if fm.get("tipo") not in LOW_CITATION_TIPOS:
            continue
        if str(fm.get("index", "")).lower() == "false":
            continue
        body = _body_for_metrics(page.read_text(encoding="utf-8"))
        n_words = len(re.findall(r"\b\w+\b", body))
        if n_words < LOW_CITATION_MIN_WORDS:
            continue
        n_cit = len(_CITATION_COUNT_RE.findall(body))
        if n_cit < LOW_CITATION_MIN_CITATIONS:
            items.append({
                "path": str(page),
                "tipo": fm.get("tipo"),
                "words": n_words,
                "citations": n_cit,
            })
    return {"severity": "warning", "count": len(items), "items": items}


def _normalize_tag(tag: str) -> str:
    """Lowercase + sem diacríticos, para detectar variantes de mesma raiz."""
    import unicodedata
    s = unicodedata.normalize("NFKD", tag)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.lower()


def _stem_tag(tag: str) -> str:
    """Stem ingênuo: remove plural pt-br trivial (-s, -es) para detectar par singular/plural."""
    n = _normalize_tag(tag)
    if len(n) > 4 and n.endswith("es"):
        return n[:-2]
    if len(n) > 3 and n.endswith("s"):
        return n[:-1]
    return n


# Pares plural/singular intencionais — a wiki usa ambos como conceitos distintos:
# singular tagga páginas de instância (uma parábola, um apóstolo); plural tagga
# índices/coletivos/comparativos. Exemplo: "evangelho" (método) vs "evangelhos"
# (os 4 textos), "parabola" (uma parábola) vs "parabolas" (índice e trilhas).
NAMING_STEM_ALLOWLIST: set[tuple[str, str]] = {
    ("evangelho", "evangelhos"),
    ("apostolo", "apostolos"),
    ("espirito", "espiritos"),
    ("parabola", "parabolas"),
}


def check_naming_consistency(pages: list[Path]) -> dict:
    """Check — tags equivalentes registradas com nomenclaturas inconsistentes.

    Detecta dois padrões em frontmatter `tags`:
    a) variantes que normalizam para a mesma forma (lowercase + sem diacríticos)
       — ex.: `perispirito` vs `perispírito`;
    b) pares singular/plural com mesmo stem que aparecem em pelo menos 2 páginas
       cada — ex.: `parabola` vs `parabolas` (e ambos circulam) sugerem
       indecisão sobre qual é a tag canônica. Pares declarados em
       NAMING_STEM_ALLOWLIST são intencionais (significados distintos).
    """
    from collections import defaultdict

    tag_pages: dict[str, set[str]] = defaultdict(set)
    for page in pages:
        fm, _ = parse_frontmatter(page)
        tags = fm.get("tags", [])
        if isinstance(tags, str):
            tags = [tags]
        for t in tags:
            tag_pages[t].add(str(page))

    items: list[dict] = []

    # (a) variantes case/diacrítico
    norm_groups: dict[str, set[str]] = defaultdict(set)
    for t in tag_pages:
        norm_groups[_normalize_tag(t)].add(t)
    for norm, variants in sorted(norm_groups.items()):
        if len(variants) > 1:
            items.append({
                "kind": "case_or_accent",
                "normalized": norm,
                "variants": sorted(variants),
                "counts": {v: len(tag_pages[v]) for v in sorted(variants)},
            })

    # (b) pares singular/plural com ambos circulando
    stem_groups: dict[str, set[str]] = defaultdict(set)
    for t in tag_pages:
        stem_groups[_stem_tag(t)].add(_normalize_tag(t))
    seen_pairs: set[tuple[str, str]] = set()
    for stem, variants in sorted(stem_groups.items()):
        if len(variants) < 2:
            continue
        ordered = sorted(variants, key=len)
        for i in range(len(ordered)):
            for j in range(i + 1, len(ordered)):
                a, b = ordered[i], ordered[j]
                pair = (a, b) if a < b else (b, a)
                if pair in NAMING_STEM_ALLOWLIST or pair in seen_pairs:
                    continue
                seen_pairs.add(pair)
                count_a = sum(len(tag_pages[t]) for t in tag_pages if _normalize_tag(t) == a)
                count_b = sum(len(tag_pages[t]) for t in tag_pages if _normalize_tag(t) == b)
                if count_a >= 2 and count_b >= 2:
                    items.append({
                        "kind": "plural_singular",
                        "stem": stem,
                        "variants": [a, b],
                        "counts": {a: count_a, b: count_b},
                    })

    return {"severity": "warning", "count": len(items), "items": items}


# Padrões válidos de citação (seção 4 do CLAUDE.md + variantes reais)
_CITATION_VALID = [
    # LE
    r"\(LE,\s*q\.\s*\d+",
    r"\(LE,\s*Introdução",
    r"\(LE,\s*Conclusão",
    r"\(LE,\s*Prolegômenos",
    r"\(LE,\s*Nota\s",
    r"\(LE,\s*Parte\s*\d",
    r"\(LE,\s*[12][ªa]\s*parte",
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
        fm, _ = parse_frontmatter(page)
        # Texto verbatim do raw: citações bíblicas inline ("(Gênese, 1:28)") não
        # são citações Kardec malformadas — são o próprio Kardec citando a Bíblia.
        if fm.get("tipo") in _CORPUS_TIPOS:
            continue
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


def check_citation_resolves(pages: list[Path]) -> dict:
    """Check — citações (sigla, ref) cujo locus não existe na obra-fonte.

    Camada baixa da verificação de fidelidade: bate cada citação ao Pentateuco
    contra a estrutura real da obra (parts, chapters, intro_items, range de
    questão). Captura typo de número, sigla com parte que não existe e cap.
    fora do range. **Não** verifica se o trecho citado sustenta a afirmação —
    essa é a versão estrita, que exige granularidade questão/item em `raw/`
    (§4 do ROADMAP).

    Skip por design (mesma política de `check_canonical_names`):
    - Citações em blockquote (transcrição literal de outra fonte).
    - Citações em inline/fenced code (exemplo/placeholder).
    - Siglas sem estrutura carregada (RE, OPE, OQE, complementares).

    **Wikilinks não são strippados**: citações dentro de `[[obras/X|(LE q. N)]]`
    são reais e devem ser validadas; mais importante, encadear a próxima sigla
    via wikilink-com-alias (`…; [[wiki/obras/ceu-e-inferno|C&I]] 1ª parte cap. IX`)
    é padrão idiomático na wiki — NEXT_SIGLA_RE precisa ver `|<sigla>` para
    truncar corretamente.
    """
    structures = load_structures()
    items: list[dict] = []
    for page in pages:
        text = page.read_text(encoding="utf-8")
        # Frontmatter pode ter `fontes: [LE, ...]` sem parêntese — não casa
        # KARDEC_RE — então skip-frontmatter explícito é desnecessário.
        body = strip_inline_code(text)
        body = _strip_blockquotes(body)
        for i, line in enumerate(body.splitlines(), 1):
            for m in KARDEC_RE.finditer(line):
                sigla = SIGLA_NORM.get(m.group("sigla"), m.group("sigla"))
                structure = structures.get(sigla)
                if structure is None:
                    continue
                ok, reason = resolve_locus(m.group("sigla"), m.group("rest"), structure)
                if not ok:
                    items.append({
                        "path": str(page),
                        "line": i,
                        "citation": m.group(0),
                        "reason": reason,
                    })
    # severity "error": locus do Pentateuco que não resolve é citação falsa de
    # Kardec — bloqueia o deploy e reprova o PR (lint-pr.yml / deploy-wiki.yml),
    # não só registra aviso. Captura typo de número, parte inexistente e cap.
    # fora do range; NÃO captura deturpação semântica (ROADMAP §4).
    return {"severity": "error", "count": len(items), "items": items}


# ─── check_literal_quote_exists ────────────────────────────────────────────────
# Aspa literal (reta "…" ou curva “…”) imediatamente seguida de uma citação Kardec.
# Captura o conteúdo da aspa (grupo 1) e o parêntese candidato (grupo 2); o
# parêntese é revalidado por KARDEC_RE para confirmar que é citação ao Pentateuco.
_QUOTE_BEFORE_CITE_RE = re.compile(
    r'["“]([^"”\n]{12,}?)["”]'      # aspa com ≥12 chars (pré-filtro bruto)
    r'[\s,.:;…–—-]*'                # liga até a citação (só pontuação/espaço — sem letras)
    r'(\([^)\n]*\))'                # parêntese seguinte (citação candidata)
)

# Pisos contra ruído de aspas curtas/triviais.
_MIN_WORDS = 5
# Abaixo desta fração de cobertura CONTÍGUA (ver reverse_locus.word_coverage) a
# aspa não bate verbatim com o locus citado — candidata a fabricação / locus
# errado / paráfrase. A classificação fina (e a sugestão do locus correto) vem de
# reverse_locus.classify. Conservador: 0.5 = metade da aspa ausente como trecho
# contíguo. _normalize_quote / _word_coverage / _ELISION_RE vêm de reverse_locus
# (fonte única — check e índice reverso usam matemática idêntica de cobertura).
_COVERAGE_MIN = 0.5


def _safe_mtime(p: Path) -> int:
    try:
        return p.stat().st_mtime_ns
    except OSError:
        return 0


def _scan_literal_quotes(pages: list[Path]) -> list[dict]:
    """Núcleo compartilhado por `check_literal_quote_exists` (info) e
    `check_quote_misattributed` (warning): varre `pages` por aspa literal de Kardec
    e classifica cada candidata pelo índice reverso. A varredura `difflib` sobre a
    obra inteira é cara — memoizada por (path, mtime) para que os dois checks rodem
    no mesmo lint sem dobrar o custo. Cada check filtra a fatia que lhe interessa.
    """
    key = tuple((str(p), _safe_mtime(p)) for p in pages)
    return list(_scan_literal_quotes_cached(key))


@lru_cache(maxsize=8)
def _scan_literal_quotes_cached(key: tuple[tuple[str, int], ...]) -> tuple[dict, ...]:
    """Para cada candidato (cobertura contígua < _COVERAGE_MIN no locus citado),
    `reverse_locus.classify` varre a obra inteira e anexa um veredicto:

    - **misattributed**: a aspa é verbatim em OUTRO locus → `suggested_locus` traz o
      `ref` correto (auto-corrigível: trocar o locus). Classe 2 do §12 — o erro
      mais comum dos itens diferidos do `/critica`, detectado sem LLM.
    - **fabricated**: a aspa não aparece contígua em locus nenhum da obra. Classe 1.
    - **paraphrase**: o melhor locus É o citado, mas a aspa o parafraseia (não é
      verbatim) → conserto é de-quote ou usar o texto literal.
    - **uncertain**: zona cinzenta → revisão humana.
    - **supported** é SUPRIMIDO (não vira item): o índice achou a aspa no próprio
      locus citado — o flag foi artefato de extração do `cite.py` em capítulo
      irregular (ESE cap. XXVIII, C&I 2ª parte). Elimina a maior fonte de FP.

    Conservador: só double-quotes adjacentes a citação Kardec **resolvível**;
    cobertura contígua (tolera acento/caixa/pontuação/elisão); piso de ≥5 palavras;
    skip em blockquote/code; locus inválido → skip (coberto por
    `check_citation_resolves`).
    """
    items: list[dict] = []
    for path_str, _mtime in key:
        page = Path(path_str)
        text = page.read_text(encoding="utf-8")
        body = strip_inline_code(text)
        body = _strip_blockquotes(body)
        for i, line in enumerate(body.splitlines(), 1):
            for m in _QUOTE_BEFORE_CITE_RE.finditer(line):
                quote, citation = m.group(1), m.group(2)
                km = KARDEC_RE.search(citation)
                if not km:
                    continue
                locus = literal_text(km.group("sigla"), km.group("rest"))
                if locus is None:
                    continue  # locus inválido → responsabilidade do citation_resolves
                if len(_normalize_quote(_ELISION_RE.sub(" ", quote)).split()) < _MIN_WORDS:
                    continue  # aspa curta demais para afirmar fabricação
                coverage = _word_coverage(quote, locus)
                if coverage >= _COVERAGE_MIN:
                    continue
                verdict = classify(km.group("sigla"), km.group("rest"), quote, coverage)
                if verdict.label == "supported":
                    continue  # FP de extração: a aspa está no locus citado
                item = {
                    "path": str(page),
                    "line": i,
                    "quote": quote if len(quote) <= 120 else quote[:117] + "...",
                    "citation": citation,
                    "coverage": round(coverage, 2),
                    "classification": verdict.label,
                }
                if verdict.label == "misattributed" and verdict.suggested_ref:
                    suggested = f"({km.group('sigla')}, {verdict.suggested_ref})"
                    item["suggested_locus"] = suggested
                    item["suggested_coverage"] = round(verdict.suggested_coverage, 2)
                    # `detail` é o que o hook PostToolUse surfa na edição — torna a
                    # sugestão acionável sem abrir o JSON: locus citado → sugerido.
                    item["detail"] = (
                        f"{citation} → trocar por {suggested} "
                        f"(cob. {round(coverage, 2)}→{round(verdict.suggested_coverage, 2)})"
                    )
                items.append(item)
    return tuple(items)


def check_literal_quote_exists(pages: list[Path]) -> dict:
    """Check (info) — aspa literal de Kardec que não bate verbatim com o locus
    citado e **não** é mal-atribuída (`fabricated`/`paraphrase`/`uncertain`).
    As mal-atribuídas (classe 2, sinal limpo) saíram para `check_quote_misattributed`
    (warning + hook). Esta fatia segue `info`/aid de auditoria: a cobertura é
    tolerante e o de-quote/reancoragem exige conferência humana — não promover a
    warning/error sem calibrar o threshold contra as 97 fabricadas (ROADMAP §12).
    Alimenta `reports/citacao/triagem-aspas.md`.
    """
    items = [
        it for it in _scan_literal_quotes(pages)
        if it["classification"] in ("fabricated", "paraphrase", "uncertain")
    ]
    return {"severity": "info", "count": len(items), "items": items}


# Allowlist data-driven (não hardcoded) de aspas mal-atribuídas que foram
# verificadas À MÃO como corretas no locus citado — FPs do índice reverso. Cada
# entrada suprime um item de check_quote_misattributed. Adicionar/remover é edição
# de JSON. Ver ROADMAP §12 e memória feedback-checks-data-driven.
ASPAS_ACEITAS_PATH = Path(__file__).resolve().parents[4] / "data" / "citacao-aspas-aceitas.json"


def _load_aspas_aceitas() -> list[dict]:
    """Lista de aspas aceitas (FPs confirmados). Vazia se o arquivo sumir/quebrar
    — o check então não suprime nada (fail-open: prefere ruído a esconder erro)."""
    try:
        data = json.loads(ASPAS_ACEITAS_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    return data.get("aceitas", [])


_ASPAS_ACEITAS = _load_aspas_aceitas()


def _is_accepted_quote(item: dict) -> bool:
    """True se a aspa mal-atribuída consta da allowlist (path por sufixo + citação
    idêntica + trecho contido, tudo normalizado)."""
    path = item["path"].replace("\\", "/")
    quote_norm = _normalize_quote(item["quote"])
    for entry in _ASPAS_ACEITAS:
        entry_path = entry.get("path", "")
        if not entry_path or not path.endswith(entry_path):
            continue
        if entry.get("citation") != item["citation"]:
            continue
        needle = _normalize_quote(entry.get("quote_contem", ""))
        if needle and needle in quote_norm:
            return True
    return False


def check_quote_misattributed(pages: list[Path]) -> dict:
    """Check (warning) — aspa literal de Kardec que é verbatim em OUTRO locus que
    não o citado (classe 2 do ROADMAP §12). Sinal limpo do índice reverso: o
    conserto é trocar o `ref` pelo `suggested_locus` (verificável por `cite.py`).

    Promovido a **warning + hook** (edit-time) em 2026-06-17 para barrar a
    reincidência — a varredura wiki-wide das 25 mal-atribuições foi zerada antes da
    promoção, então qualquer mal-atribuição nova surge no PostToolUse já na edição.
    FPs verificados à mão ficam na allowlist data-driven (`_is_accepted_quote`).

    Ainda **não** é `error`/CI gate: a promoção a error vem quando a confiança
    consolidar (e `fabricated` exige calibrar o threshold contra as 97 da triagem).
    """
    items = [
        it for it in _scan_literal_quotes(pages)
        if it["classification"] == "misattributed" and not _is_accepted_quote(it)
    ]
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

VALID_GRAU_TAGS = {
    "grau/introdutorio", "grau/intermediario", "grau/avancado",
}

VALID_TEMA_TAGS = {
    "tema/deus", "tema/espiritos", "tema/encarnacao", "tema/mediunidade",
    "tema/moral", "tema/jesus", "tema/vida-futura", "tema/sociedade",
    "tema/livre-arbitrio", "tema/prece-caridade", "tema/sofrimento",
    "tema/historia-doutrina",
}

VALID_AUTOR_TAGS = {
    "autor/kardec", "autor/leon-denis", "autor/chico-xavier",
    "autor/emmanuel", "autor/andre-luiz", "autor/humberto-de-campos",
    "autor/joanna-de-angelis", "autor/divaldo-franco",
    "autor/bezerra-de-menezes", "autor/cairbar-schutel", "autor/hammed",
    "autor/paulo", "autor/joao", "autor/pedro", "autor/tiago",
    "autor/waldo-vieira", "autor/flammarion",
}

FONTES_TO_OBRA = {
    "LE": "obra/le", "LM": "obra/lm", "ESE": "obra/ese",
    "C&I": "obra/ci", "Gênese": "obra/genese",
    "OPE": "obra/ope", "OQE": "obra/oqe", "RE": "obra/re",
}

# Tipos de página que NÃO recebem grau/* (obras não têm grau próprio).
GRAU_EXEMPT_TIPOS = {"obra", "capitulo-biblico", "livro-biblico", "capitulo-pentateuco", "obra-pentateuco"}


def _is_trilha(page: Path, tags: list[str]) -> bool:
    """Trilhas (em wiki/trilhas/ ou marcadas com tag livre 'trilha') não recebem grau/*."""
    return "wiki/trilhas/" in str(page) or "trilha" in tags


def check_tag_taxonomy(pages: list[Path]) -> dict:
    """Check — tags lei/, obra/, grau/, tema/, autor/ devem pertencer a conjuntos canônicos."""
    items = []
    for page in pages:
        fm, _ = parse_frontmatter(page)
        # Corpus verbatim (Bíblia/Pentateuco): fontes: [LE] etc. é correto, mas
        # não recebe tag obra/ (não é página curada) — não cobrar a correspondência.
        if fm.get("tipo") in _CORPUS_TIPOS:
            continue
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
            if tag.startswith("grau/") and tag not in VALID_GRAU_TAGS:
                items.append({
                    "path": str(page),
                    "detail": f"tag grau/ inválida: {tag} (valores válidos: {', '.join(sorted(VALID_GRAU_TAGS))})",
                })
            if tag.startswith("tema/") and tag not in VALID_TEMA_TAGS:
                items.append({
                    "path": str(page),
                    "detail": f"tag tema/ inválida: {tag} (valores válidos: {', '.join(sorted(VALID_TEMA_TAGS))})",
                })
            if tag.startswith("autor/") and tag not in VALID_AUTOR_TAGS:
                items.append({
                    "path": str(page),
                    "detail": f"tag autor/ inválida: {tag} (valores válidos: {', '.join(sorted(VALID_AUTOR_TAGS))})",
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

        # grau/* não é permitido em obras nem em trilhas
        tipo = fm.get("tipo", "")
        if tipo in GRAU_EXEMPT_TIPOS or _is_trilha(page, tags):
            for t in sorted(t for t in tags if t.startswith("grau/")):
                items.append({
                    "path": str(page),
                    "detail": f"tag {t} não se aplica (obras/trilhas não têm grau próprio)",
                })

    return {"severity": "warning", "count": len(items), "items": items}


def _is_meta_tagged(fm: dict) -> bool:
    """Meta-páginas (tipo: sintese + tag 'meta') ficam fora de checks de cobertura."""
    tags = fm.get("tags", []) or []
    if isinstance(tags, str):
        tags = [tags]
    return fm.get("tipo") == "sintese" and "meta" in tags


def check_tag_coverage(pages: list[Path]) -> dict:
    """Check — páginas elegíveis devem ter ao menos 1 tag tema/* (info-level).

    Eleva sinal sobre páginas ainda sem eixo doutrinário marcado, alimentando
    passes incrementais de tagueamento. Skip explícito: trilhas (estruturais),
    meta-páginas (tipo: sintese + tag meta) e capítulos/livros bíblicos
    publicados (texto literal, taguear por capítulo seria ruído).
    """
    items = []
    for page in pages:
        fm, _ = parse_frontmatter(page)
        tags = fm.get("tags", []) or []
        if isinstance(tags, str):
            tags = [tags]
        if _is_trilha(page, tags) or _is_meta_tagged(fm):
            continue
        if fm.get("tipo") in _CORPUS_TIPOS:
            continue
        if not any(t.startswith("tema/") for t in tags):
            items.append({
                "path": str(page),
                "tipo": fm.get("tipo", ""),
                "detail": "página sem nenhuma tag tema/*",
            })
    return {"severity": "info", "count": len(items), "items": items}


PENTATEUCO_SLUGS = {
    "livro-dos-espiritos",
    "livro-dos-mediuns",
    "evangelho-segundo-o-espiritismo",
    "genese",
    "ceu-e-inferno",
}

EVANGELHOS_SLUGS = {
    "evangelho-segundo-mateus",
    "evangelho-segundo-marcos",
    "evangelho-segundo-lucas",
    "evangelho-segundo-joao",
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
        1 for o in obras_pages
        if o.stem not in PENTATEUCO_SLUGS and o.stem not in EVANGELHOS_SLUGS
    )
    # Páginas curadas = tudo sob wiki/ exceto o corpus bíblico (wiki/biblia/**) e a
    # landing page wiki/index.md. Os index.md de seção (wiki/<dir>/index.md) CONTAM —
    # só a landing page (parent == WIKI_DIR) sai. Mesma definição do gerador canônico
    # update_status.py (skill stats) — manter as duas em sincronia.
    total_paginas = sum(
        1 for p in pages
        if "biblia" not in p.parts
        and "pentateuco" not in p.parts
        and not (p.name == "index.md" and p.parent == WIKI_DIR)
    )
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


SKILLS_DIR = Path(".claude/skills")
RULES_DIR = Path(".claude/rules")
CLAUDE_MD_PATH = Path("CLAUDE.md")
QUARTZ_CONFIG_PATH = Path("quartz.config.ts")


def check_raw_excluded(pages: list[Path]) -> dict:
    """Check — `raw/` deve estar em `ignorePatterns` do quartz.config.ts.

    `raw/` contém transcrições integrais de obras protegidas (Chico Xavier,
    Hammed, Divaldo etc.) usadas só na pipeline local. Vazamento para o build
    público é o pior caso: o GitHub Pages republicaria texto de terceiros
    integralmente. Trava regressão.
    """
    if not QUARTZ_CONFIG_PATH.exists():
        return {
            "severity": "error",
            "count": 1,
            "items": [{"detail": "quartz.config.ts não encontrado"}],
        }
    text = QUARTZ_CONFIG_PATH.read_text(encoding="utf-8")
    match = re.search(r"ignorePatterns\s*:\s*\[([^\]]*)\]", text)
    if not match:
        return {
            "severity": "error",
            "count": 1,
            "items": [{"detail": "ignorePatterns não encontrado em quartz.config.ts"}],
        }
    patterns = match.group(1)
    if not re.search(r"""['"]raw['"]""", patterns):
        return {
            "severity": "error",
            "count": 1,
            "items": [{
                "detail": "raw/ ausente de ignorePatterns — obras protegidas vazariam para o build público",
                "ignorePatterns": patterns.strip(),
            }],
        }
    return {"severity": "error", "count": 0, "items": []}


RAW_DIR = Path("raw")

# Em raw/mediuns/<medium>/, a próxima camada deve ser <autor-espiritual>/.
# Não há .pdf/.md soltos no nível do médium.
_MEDIUNS_REQUIRES_AUTHOR_LAYER = True


def check_raw_layout(pages: list[Path]) -> dict:
    """Check — raw/ deve seguir o esquema canônico de slugs e hierarquia.

    Regras (warnings — legado em migração):
    1. Subpasta direta de raw/ está em RAW_TOP_LEVEL_DIRS.
    2. Cada nome de pasta/arquivo (sem extensão) é kebab-case ASCII puro.
    3. Em raw/mediuns/<medium>/: o próximo nível é <autor-espiritual>/, não
       arquivo solto (CLAUDE.md §3 — "o médium não é o autor").
    4. Para cada <slug>.pdf, existe diretório <slug>/ com <slug>.md dentro.
    5. Imagens _page_*.jpeg ficam em assets/, não soltas no diretório <slug>/.
    6. Sem sufixos artefato (_compress, -min, c3a[0-9a-f]) em nomes.

    Nota: pares <TÍTULO>.md + summary-<TÍTULO>.md em palestras/ ficam lado
    a lado por convenção (.claude/rules/convencoes-palestras.md).
    """
    items: list[dict] = []

    if not RAW_DIR.exists():
        return {"severity": "warning", "count": 0, "items": []}

    # Regra 1: top-level allowlist
    for entry in sorted(RAW_DIR.iterdir()):
        if entry.name.startswith(".") or entry.is_file():
            continue
        if entry.name not in RAW_TOP_LEVEL_DIRS:
            items.append({
                "path": str(entry),
                "rule": "top_level_unknown",
                "detail": f"subpasta '{entry.name}' fora da allowlist {sorted(RAW_TOP_LEVEL_DIRS)}",
            })

    # Coletor genérico — visita tudo dentro das pastas conhecidas
    def _walk(base: Path):
        if not base.exists():
            return
        for p in base.rglob("*"):
            # ignora dot-files de sistema
            if any(part.startswith(".") for part in p.relative_to(RAW_DIR).parts):
                continue
            yield p

    # Regras 2 e 7: slug canônico + sem artefato (toda pasta/arquivo dentro de raw/)
    # Skip biblia-acf/ (slugs de livros e capítulos numerados são especiais) e kardec/
    # (estrutura própria validada manualmente).
    for top in RAW_TOP_LEVEL_DIRS - {"biblia-acf", "kardec", "assets"}:
        base = RAW_DIR / top
        for p in _walk(base):
            rel = p.relative_to(RAW_DIR)
            # Para arquivos: stem; para pastas: nome.
            name = p.stem if p.is_file() else p.name
            # Allowlist de nomes especiais (não-slug por desenho)
            if name in {"_meta", "_summaries", "assets", "_page_*"}:
                continue
            if name.startswith("_page_"):  # _page_0_Picture_0.jpeg etc.
                continue
            # Metadados de extração: `<slug>_meta.json` é a forma produzida pelo
            # extrator (marker-pdf etc.). Validar o slug sem o sufixo `_meta`.
            if p.is_file() and name.endswith("_meta"):
                name = name[: -len("_meta")]
            if has_artifact_marker(name):
                items.append({
                    "path": str(p),
                    "rule": "artifact_suffix",
                    "detail": f"nome contém marcador artefato (compress/min/c3a*): '{name}'",
                    "suggested": str(p.parent / canonical_for(p.name)),
                })
                continue
            if not is_canonical_slug(name):
                items.append({
                    "path": str(p),
                    "rule": "non_canonical_slug",
                    "detail": f"slug fora do padrão kebab-case ASCII: '{name}'",
                    "suggested": str(p.parent / canonical_for(p.name)),
                })

    # Regra 3: mediuns/<medium>/<autor-espiritual>/<obra>
    mediuns_dir = RAW_DIR / "mediuns"
    if mediuns_dir.exists() and _MEDIUNS_REQUIRES_AUTHOR_LAYER:
        for medium_dir in sorted(mediuns_dir.iterdir()):
            if not medium_dir.is_dir() or medium_dir.name.startswith("."):
                continue
            for child in sorted(medium_dir.iterdir()):
                if child.name.startswith("."):
                    continue
                # No nível do médium só pode haver pastas (autor espiritual).
                if child.is_file():
                    items.append({
                        "path": str(child),
                        "rule": "missing_author_layer",
                        "detail": (
                            f"arquivo direto em mediuns/{medium_dir.name}/ — "
                            f"deve estar dentro de <autor-espiritual>/"
                        ),
                    })

    # Regra 4: PDF ↔ diretório homônimo + Regra 5: imagens em assets/
    # Aplicamos em autores/ e mediuns/.
    for top in ("autores", "mediuns"):
        base = RAW_DIR / top
        if not base.exists():
            continue
        # Considera pares pdf/diretório no mesmo nível
        for parent in base.rglob("*"):
            if not parent.is_dir():
                continue
            stems_with_pdf: set[str] = set()
            stems_with_dir: set[str] = set()
            for child in parent.iterdir():
                if child.name.startswith("."):
                    continue
                if child.is_file() and child.suffix.lower() == ".pdf":
                    stems_with_pdf.add(child.stem)
                elif child.is_dir():
                    stems_with_dir.add(child.name)
            # PDF sem diretório de extrato (warning brando — pode ser intencional)
            for stem in stems_with_pdf - stems_with_dir:
                # ignora se há .md irmão com mesmo stem (extração single-file)
                if (parent / f"{stem}.md").exists():
                    continue
                items.append({
                    "path": str(parent / f"{stem}.pdf"),
                    "rule": "pdf_without_extract",
                    "detail": f"{stem}.pdf sem diretório homônimo {stem}/ (extrato ausente)",
                })
            # Diretório com .md mas sem PDF (apenas info — extrato órfão)
            for name in stems_with_dir - stems_with_pdf:
                d = parent / name
                if (d / f"{name}.md").exists() and not (parent / f"{name}.pdf").exists():
                    # info, não warning — ingest pode chegar como .md direto
                    pass

        # Regra 5: imagens _page_*.jpeg dentro de <slug>/ devem estar em assets/.
        # Skip o próprio `assets/` (é o destino canônico das imagens; flagga-lo
        # geraria detail "mover para assets/assets/", falso positivo).
        for slug_dir in base.rglob("*"):
            if not slug_dir.is_dir() or slug_dir.name == "assets":
                continue
            loose_images = [
                p for p in slug_dir.iterdir()
                if p.is_file() and p.name.startswith("_page_")
                and p.suffix.lower() in (".jpeg", ".jpg", ".png")
            ]
            if loose_images:
                items.append({
                    "path": str(slug_dir),
                    "rule": "images_not_in_assets",
                    "detail": f"{len(loose_images)} imagem(ns) _page_*.* solta(s) — mover para {slug_dir.name}/assets/",
                    "count_images": len(loose_images),
                })

    # Nota: pares <TÍTULO>.md + summary-<TÍTULO>.md em palestras/ são uma
    # convenção documentada (.claude/rules/convencoes-palestras.md). Os summaries
    # ficam lado a lado com a transcrição — só a slugificação se aplica
    # (já coberta pela Regra 2).

    return {"severity": "warning", "count": len(items), "items": items}


def check_skills_consistency(pages: list[Path]) -> dict:
    """Check — coerência interna entre CLAUDE.md, .claude/skills/ e .claude/rules/.

    Detecta três classes de drift entre as instruções de base e a realidade do repo:
    - referência a `wiki/<dir>/` inexistente (ex.: `wiki/parabolas/` fantasma);
    - skill em `.claude/skills/<name>/SKILL.md` sem menção em CLAUDE.md;
    - caminho de script (`uv run python ...` ou `python3 ...`) inexistente no disco.

    Não strippa inline code: paths em backticks (`wiki/x/`) são referências reais
    que precisam ser validadas, não exemplos a ignorar.
    """
    items = []

    meta_files: list[Path] = []
    if CLAUDE_MD_PATH.exists():
        meta_files.append(CLAUDE_MD_PATH)
    if SKILLS_DIR.exists():
        meta_files.extend(sorted(SKILLS_DIR.glob("*/SKILL.md")))
    if RULES_DIR.exists():
        meta_files.extend(sorted(RULES_DIR.glob("*.md")))

    # (a) referências wiki/<dir>/ a diretórios inexistentes
    wiki_dir_re = re.compile(r"\bwiki/([a-z0-9_-]+)/")
    seen_dir_refs: set[tuple[str, str]] = set()
    for f in meta_files:
        text = f.read_text(encoding="utf-8")
        for lineno, line in enumerate(text.splitlines(), 1):
            for m in wiki_dir_re.finditer(line):
                dir_name = m.group(1)
                key = (str(f), dir_name)
                if key in seen_dir_refs:
                    continue
                seen_dir_refs.add(key)
                if not (WIKI_DIR / dir_name).is_dir():
                    items.append({
                        "source": str(f),
                        "line": lineno,
                        "detail": f"referência a wiki/{dir_name}/ — diretório não existe",
                    })

    # (b) skills sem menção em CLAUDE.md
    if CLAUDE_MD_PATH.exists() and SKILLS_DIR.exists():
        claude_text = CLAUDE_MD_PATH.read_text(encoding="utf-8")
        for skill_md in sorted(SKILLS_DIR.glob("*/SKILL.md")):
            skill_name = skill_md.parent.name
            if skill_name.startswith("_"):
                continue
            if f"/{skill_name}" not in claude_text:
                items.append({
                    "source": str(CLAUDE_MD_PATH),
                    "detail": f"skill /{skill_name} sem menção em CLAUDE.md",
                })

    # (c) caminhos `uv run python <path>` ou `python3 <path>` inexistentes
    script_path_re = re.compile(r"(?:uv run python|python3)\s+(\.claude/[\w/.-]+\.py)")
    seen_scripts: set[tuple[str, str]] = set()
    for f in meta_files:
        text = f.read_text(encoding="utf-8")
        for lineno, line in enumerate(text.splitlines(), 1):
            for m in script_path_re.finditer(line):
                script = m.group(1)
                key = (str(f), script)
                if key in seen_scripts:
                    continue
                seen_scripts.add(key)
                if not Path(script).is_file():
                    items.append({
                        "source": str(f),
                        "line": lineno,
                        "detail": f"script {script} referenciado mas não existe",
                    })

    return {"severity": "warning", "count": len(items), "items": items}


VALID_DETENTORES = {"dominio-publico", "FEB", "Boa-Nova", "LEAL", "IDE", "desconhecido"}

QUOTE_MAX_WORDS = 400
QUOTE_MAX_PROPORTION = 0.25


def _count_words(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def _extract_blockquotes(body: str) -> list[str]:
    """Retorna o texto de cada blockquote contíguo (linhas começando com `>`).

    Callouts (`> [!note]`, `> [!tip]` etc.) são excluídos — são UI/aviso, não citação
    de obra protegida.
    """
    blocks: list[str] = []
    current: list[str] = []
    is_callout = False
    for line in body.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(">"):
            content = stripped[1:].lstrip()
            if not current and content.startswith("[!"):
                is_callout = True
            current.append(content)
        else:
            if current and not is_callout:
                blocks.append("\n".join(current))
            current = []
            is_callout = False
    if current and not is_callout:
        blocks.append("\n".join(current))
    return blocks


def check_quote_proportion(pages: list[Path]) -> dict:
    """Check — proporção/tamanho de citações em obras protegidas (CLAUDE.md §3).

    Aplica-se a `tipo: obra` com `direitos.detentor` diferente de `dominio-publico`
    e `desconhecido`. Reporta como `info` (orienta revisão manual; severidade
    sobe para `warning` após calibração contra páginas existentes).
    """
    items: list[dict] = []
    for page in pages:
        fm, _ = parse_frontmatter(page)
        if fm.get("tipo") != "obra":
            continue
        direitos = fm.get("direitos")
        if not isinstance(direitos, dict):
            continue
        detentor = direitos.get("detentor")
        if detentor in {"dominio-publico", "desconhecido", None}:
            continue
        body = _body_for_metrics(page.read_text(encoding="utf-8"))
        body_words = _count_words(body)
        if body_words == 0:
            continue
        quotes = _extract_blockquotes(body)
        quote_words = sum(_count_words(q) for q in quotes)
        max_single = max((_count_words(q) for q in quotes), default=0)
        proportion = quote_words / body_words if body_words else 0
        violations = []
        if max_single > QUOTE_MAX_WORDS:
            violations.append(f"trecho único com {max_single} palavras (limite {QUOTE_MAX_WORDS})")
        if proportion > QUOTE_MAX_PROPORTION:
            violations.append(
                f"citação representa {proportion:.0%} do corpo (limite {QUOTE_MAX_PROPORTION:.0%})"
            )
        if violations:
            items.append({
                "path": str(page),
                "detentor": detentor,
                "body_words": body_words,
                "quote_words": quote_words,
                "max_single_quote": max_single,
                "violations": violations,
            })
    return {"severity": "info", "count": len(items), "items": items}


def check_direitos_obras(pages: list[Path]) -> dict:
    """Check — frontmatter `direitos:` em páginas tipo: obra.

    Severity `info` enquanto o backfill de massa está em andamento; será
    promovido a `warning` quando todas as obras tiverem o campo populado.
    Detentor fora do conjunto canônico é `error` desde já — é typo, não gap.
    """
    items_info: list[dict] = []
    items_error: list[dict] = []
    items_warning: list[dict] = []
    for page in pages:
        fm, _ = parse_frontmatter(page)
        if fm.get("tipo") != "obra":
            continue
        direitos = fm.get("direitos")
        if direitos is None:
            items_info.append({"path": str(page), "detail": "campo direitos: ausente"})
            continue
        if not isinstance(direitos, dict):
            items_error.append({
                "path": str(page),
                "detail": f"direitos: deve ser um mapa YAML, recebido {type(direitos).__name__}",
            })
            continue
        detentor = direitos.get("detentor")
        if detentor is None:
            items_error.append({"path": str(page), "detail": "direitos.detentor ausente"})
            continue
        if detentor not in VALID_DETENTORES:
            items_error.append({
                "path": str(page),
                "detail": f"direitos.detentor inválido: {detentor} "
                          f"(válidos: {', '.join(sorted(VALID_DETENTORES))})",
            })
            continue
        if detentor == "dominio-publico" and direitos.get("ano_dp_estimado"):
            items_warning.append({
                "path": str(page),
                "detail": "ano_dp_estimado presente mas detentor é dominio-publico (incoerente)",
            })
        if detentor not in {"dominio-publico", "desconhecido"} and not direitos.get("url_aquisicao"):
            items_info.append({
                "path": str(page),
                "detail": f"obra protegida ({detentor}) sem url_aquisicao",
            })

    # Erros tomam precedência: se há detentor inválido, severity = error.
    if items_error:
        return {"severity": "error", "count": len(items_error), "items": items_error}
    if items_warning:
        return {"severity": "warning", "count": len(items_warning), "items": items_warning}
    return {"severity": "info", "count": len(items_info), "items": items_info}


def _strip_blockquotes(body: str) -> str:
    """Substitui linhas começando com `>` por espaços, preservando offsets.

    Citações em blockquote (transcrições literais de fonte) podem usar a forma
    histórica de uma personalidade (ex.: "Rivail" em jornal de 1857) e devem
    ser preservadas. O canonical-name check ignora esse conteúdo.
    """
    out = []
    for line in body.splitlines(keepends=True):
        stripped = line.lstrip()
        if stripped.startswith(">"):
            out.append("".join(c if c == "\n" else " " for c in line))
        else:
            out.append(line)
    return "".join(out)


def _strip_wikilinks(body: str) -> str:
    """Substitui o conteúdo de cada `[[...]]` por espaços, preservando offsets.

    Necessário para o canonical-name check: aliases já citados via wikilink
    com label (`[[wiki/personalidades/allan-kardec|Rivail]]`) são uso correto
    e não devem ser sinalizados.
    """
    return re.sub(r"\[\[[^\]]*\]\]", lambda m: " " * len(m.group(0)), body)


_FONTES_HEADING_RE = re.compile(r"^#{1,2}\s+Fontes\b", re.IGNORECASE)
_H1_H2_RE = re.compile(r"^#{1,2}\s")


def _strip_fontes_section(body: str) -> str:
    """Blanqueia a seção `## Fontes` (até a próxima H1/H2 ou EOF), preservando offsets.

    Em `## Fontes` as referências bibliográficas citam o título da obra em itálico
    como forma canônica de citação (acompanhado de `Ver [[wiki/obras/...]]` em
    separado) e o nome do autor na forma bibliográfica (`SOBRENOME, Nome`). Esse
    título/nome plano é convenção de citação, não prosa onde se esperaria wikilink.
    O canonical-name check ignora esse trecho.
    """
    out = []
    in_fontes = False
    for line in body.splitlines(keepends=True):
        if in_fontes:
            if _H1_H2_RE.match(line) and not _FONTES_HEADING_RE.match(line):
                in_fontes = False
                out.append(line)
            else:
                out.append("".join(c if c == "\n" else " " for c in line))
        elif _FONTES_HEADING_RE.match(line):
            in_fontes = True
            out.append("".join(c if c == "\n" else " " for c in line))
        else:
            out.append(line)
    return "".join(out)


# Páginas de Escritura — os nomes próprios pertencem ao texto sagrado (tradução
# ACF) e não recebem wikilink inline; cross-references a personalidades se fazem
# por página dedicada/seção, não no versículo.
_SCRIPTURE_TIPOS = {"capitulo-biblico", "livro-biblico", "capitulo-pentateuco", "obra-pentateuco"}


def check_canonical_names(pages: list[Path]) -> dict:
    """Check — uso de alias registrado fora de wikilink/blockquote/inline code.

    Constrói o mapa alias → canonical a partir do campo `aliases:` no frontmatter
    de páginas em `wiki/personalidades/` e `wiki/obras/`. Para cada página da
    wiki, varre o corpo (sem frontmatter, sem blockquotes, sem inline code, sem
    wikilinks, sem a seção `## Fontes`) e sinaliza ocorrências de alias como
    whole-word. Skip explícito:

    - Página canônica da própria entidade (ela introduz seus próprios aliases
      em "Identificação", "Dados bibliográficos", etc.).
    - Aliases com menos de 4 caracteres (regra editorial em
      `convencoes-aliases.md`) — defesa profunda contra cadastro errado.
    - Páginas de Escritura (`tipo` em `_SCRIPTURE_TIPOS`): o nome próprio é texto
      sagrado, não prosa editorial a linkar.
    - Seção `## Fontes`: título/autor em forma bibliográfica é citação canônica
      (ver `_strip_fontes_section`).
    - Entidade já referenciada por wikilink em algum ponto da página: a cobertura
      de cross-reference já existe; menções planas subsequentes (2ª ocorrência,
      título original entre parênteses) são estilo correto, não omissão.

    Severity `info`: orienta passes incrementais; promover a `warning` após
    calibração contra falsos positivos.
    """
    aliases_map: dict[str, dict] = {}
    canonical_dirs = ("personalidades", "obras")
    for page in pages:
        if not any(f"/{d}/" in str(page) for d in canonical_dirs):
            continue
        fm, _ = parse_frontmatter(page)
        aliases = fm.get("aliases") or []
        if isinstance(aliases, str):
            aliases = [aliases]
        for alias in aliases:
            alias_str = alias.strip()
            if len(alias_str) < 4:
                continue
            # Em caso de colisão (alias registrado em duas páginas), preserva o
            # primeiro e ignora subsequentes — o cadastro deveria ser único.
            if alias_str in aliases_map:
                continue
            aliases_map[alias_str] = {
                "canonical_path": str(page),
                "canonical_link": page_key(page),
            }

    if not aliases_map:
        return {"severity": "info", "count": 0, "items": []}

    # Compila um regex por alias com word-boundary unicode-aware. \b padrão do
    # Python já trata letras acentuadas como parte da palavra na flag default,
    # mas a borda em "Rivail." casa porque "." não é \w — bom assim.
    alias_patterns = {
        alias: re.compile(rf"\b{re.escape(alias)}\b")
        for alias in aliases_map
    }

    items: list[dict] = []
    for page in pages:
        page_str = str(page)
        text = page.read_text(encoding="utf-8")
        fm, _ = parse_frontmatter(page)
        if fm.get("tipo") in _SCRIPTURE_TIPOS:
            continue  # nome próprio em versículo é texto sagrado, não prosa a linkar
        body = re.sub(r"^---.*?^---", "", text, count=1, flags=re.DOTALL | re.MULTILINE)
        body = strip_inline_code(body)
        body = _strip_blockquotes(body)
        body = _strip_wikilinks(body)
        body = _strip_fontes_section(body)
        for alias, info in aliases_map.items():
            if info["canonical_path"] == page_str:
                continue  # página canônica introduz seus próprios aliases
            if f"[[{info['canonical_link']}" in text:
                continue  # entidade já cross-referenciada por wikilink na página
            pat = alias_patterns[alias]
            for i, line in enumerate(body.splitlines(), 1):
                if pat.search(line):
                    items.append({
                        "path": page_str,
                        "line": i,
                        "alias": alias,
                        "canonical": info["canonical_link"],
                    })
                    break  # uma ocorrência por (página, alias) basta
    return {"severity": "info", "count": len(items), "items": items}


_MUNDOS_HABITADOS_CANONICAL_SLUGS = (
    "mundos-primitivos",
    "mundos-de-expiacao-e-provas",
    "mundos-regeneradores",
    "mundos-felizes",
    "mundos-celestes-ou-divinos",
    "pluralidade-dos-mundos-habitados",
)

# (descrição amigável, regex) — cada padrão captura UM tipo de drift.
_MUNDOS_HABITADOS_DRIFT_PATTERNS = (
    ("mundo regenerado (particípio)", re.compile(r"\bmundos?\s+regenerados?\b", re.IGNORECASE)),
    ("mundos ditosos (variante)", re.compile(r"\bmundos?\s+ditosos?\b", re.IGNORECASE)),
    ("ordem invertida 'provas e expiações'", re.compile(r"\bmundos?\s+de\s+provas\s+e\s+expia[cç][õo]es?\b", re.IGNORECASE)),
)

# "mundo de provas" sem "expiação" próximo na mesma linha — flagged separado
# porque exige verificação de contexto.
_MUNDOS_PROVAS_PATTERN = re.compile(r"\bmundos?\s+de\s+provas?\b", re.IGNORECASE)


def check_mundos_habitados_naming(pages: list[Path]) -> dict:
    """Check — variantes não-canônicas da escala dos mundos habitados.

    Kardec fixa em ESE cap. III, item 4 cinco categorias canônicas (mundos
    primitivos / de expiação e provas / de regeneração / felizes / celestes
    ou divinos). Em prosa, a wiki acaba usando variantes drift: "mundo de
    provas" (sem expiação), "mundo regenerado" (particípio), "mundos ditosos",
    "mundo de provas e expiações" (ordem invertida). Ver
    `.claude/rules/convencoes-mundos-habitados.md`.

    Skip: as 6 páginas-conceito da escala (introduzem suas próprias variantes
    em "Definição"/"Ensino de Kardec"), frontmatter, blockquotes, inline code,
    wikilinks. Severity `info` — orienta passes incrementais; promover a
    `warning` após calibração contra falsos positivos.
    """
    items: list[dict] = []
    for page in pages:
        page_str = str(page)
        slug = page.stem
        if slug in _MUNDOS_HABITADOS_CANONICAL_SLUGS:
            continue
        fm, _ = parse_frontmatter(page)
        if fm.get("tipo") in _CORPUS_TIPOS:
            continue  # texto verbatim — Kardec usa "mundos ditosos" etc., não normalizar
        text = page.read_text(encoding="utf-8")
        body = re.sub(r"^---.*?^---", "", text, count=1, flags=re.DOTALL | re.MULTILINE)
        body = strip_inline_code(body)
        body = _strip_blockquotes(body)
        body = _strip_wikilinks(body)
        seen_for_page: set[str] = set()
        for i, line in enumerate(body.splitlines(), 1):
            for label, pat in _MUNDOS_HABITADOS_DRIFT_PATTERNS:
                if label in seen_for_page:
                    continue
                if pat.search(line):
                    items.append({"path": page_str, "line": i, "variante": label})
                    seen_for_page.add(label)
            # "mundo de provas" sem "expiação" na mesma linha — drift.
            if "provas" in seen_for_page:
                continue
            if _MUNDOS_PROVAS_PATTERN.search(line) and "expia" not in line.lower():
                items.append({"path": page_str, "line": i, "variante": "mundo de provas (sem expiação)"})
                seen_for_page.add("provas")
    return {"severity": "info", "count": len(items), "items": items}


# ─── check_kardequiano ──────────────────────────────────────────────────────
# Formas adjetivais proibidas derivadas de "Kardec" (§13 do ROADMAP). Lidas do
# registro data-driven data/terminologia.json (vocabulário 'derivados-de-kardec'
# → mapa 'evitar'), não hardcoded: adicionar/remover uma forma é edição de JSON.
TERMINOLOGIA_PATH = Path(__file__).resolve().parents[4] / "data" / "terminologia.json"


def _load_kardequiano_forms() -> dict[str, str]:
    """{forma_proibida_lower: forma_canônica} do vocabulário 'derivados-de-kardec'.

    Vazio se o arquivo sumir/quebrar — o check então se abstém (count 0).
    """
    try:
        data = json.loads(TERMINOLOGIA_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    vocab = data.get("vocabularios", {}).get("derivados-de-kardec", {})
    forms: dict[str, str] = {}
    for termo in vocab.get("termos", []):
        for bad, good in termo.get("evitar", {}).items():
            forms[bad.lower()] = good
    return forms


_KARDEQUIANO_FORMS = _load_kardequiano_forms()
_KARDEQUIANO_RE = (
    re.compile(
        r"\b(" + "|".join(re.escape(f) for f in sorted(_KARDEQUIANO_FORMS, key=len, reverse=True)) + r")\b",
        re.IGNORECASE,
    )
    if _KARDEQUIANO_FORMS
    else None
)


def check_kardequiano(pages: list[Path]) -> dict:
    """Check — formas adjetivais proibidas derivadas de "Kardec" (§13 do ROADMAP).

    Regra dura do usuário (memória `feedback-kardequiano-vs-de-kardec`): nunca
    "kardequiano/a" (nem "kardeciano/a"); a forma correta é "de Kardec",
    reescrita conforme o contexto. "kardecista" é VÁLIDO e reservado ao
    movimento espírita — não sinalizado. As formas proibidas vêm do registro
    data-driven `data/terminologia.json` ('derivados-de-kardec').

    Skip: corpus verbatim (Bíblia/Pentateuco), frontmatter, blockquotes (citação
    literal de fonte secundária — não reescrever aspas), inline code, wikilinks
    (alias já correto). Severity `error` (CI gate): a varredura wiki-wide do §13
    zerou em 2026-06-07, então qualquer reintrodução em prosa reprova o PR.
    Nota: páginas de corpus (`livro-biblico` index) são puladas; o template
    editorial delas vive em `scripts/publish_biblia_nt.py` (corrigido na fonte).
    """
    if _KARDEQUIANO_RE is None:
        return {"severity": "error", "count": 0, "items": []}
    items: list[dict] = []
    for page in pages:
        fm, _ = parse_frontmatter(page)
        if fm.get("tipo") in _CORPUS_TIPOS:
            continue
        text = page.read_text(encoding="utf-8")
        body = re.sub(r"^---.*?^---", "", text, count=1, flags=re.DOTALL | re.MULTILINE)
        body = strip_inline_code(body)
        body = _strip_blockquotes(body)
        body = _strip_wikilinks(body)
        for i, line in enumerate(body.splitlines(), 1):
            for m in _KARDEQUIANO_RE.finditer(line):
                forma = m.group(0)
                items.append({
                    "path": str(page),
                    "line": i,
                    "forma": forma,
                    "sugestao": _KARDEQUIANO_FORMS.get(forma.lower(), "de Kardec"),
                })
    return {"severity": "error", "count": len(items), "items": items}


def check_frontmatter(pages: list[Path]) -> dict:
    """Check extra — frontmatter com campos obrigatórios ausentes."""
    required = {"tipo", "fontes", "tags", "atualizado_em", "status"}
    valid_tipos = {"conceito", "obra", "personalidade", "questao", "aprofundamento", "sintese", "divergencia", "capitulo-biblico", "livro-biblico", "capitulo-pentateuco", "obra-pentateuco"}
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
    "citation_resolves": check_citation_resolves,
    "literal_quote_exists": check_literal_quote_exists,
    "quote_misattributed": check_quote_misattributed,
    "low_citations": check_low_citations,
    "rascunho_stale": check_rascunho_stale,
    "divergencias_aberta": check_divergencias_aberta,
    "missing_concept_pages": check_missing_concept_pages,
    "frequent_missing_concepts": check_frequent_missing_concepts,
    "pentateuco_completo": check_pentateuco_completo,
    "status_projeto": check_status_projeto,
    "broken_urls": check_broken_urls,
    "tag_taxonomy": check_tag_taxonomy,
    "tag_coverage": check_tag_coverage,
    "naming_consistency": check_naming_consistency,
    "canonical_names": check_canonical_names,
    "mundos_habitados_naming": check_mundos_habitados_naming,
    "kardequiano": check_kardequiano,
    "skills_consistency": check_skills_consistency,
    "raw_excluded": check_raw_excluded,
    "raw_layout": check_raw_layout,
    "direitos_obras": check_direitos_obras,
    "quote_proportion": check_quote_proportion,
}

# Checks rodados por padrão. broken_urls é opt-in via --check-urls (I/O externo).
DEFAULT_SKIP = {"broken_urls"}

# Checks isoláveis: operam sobre uma única página sem precisar de estado global
# (incoming links, agregação de tags entre páginas, índice/catálogo, config do
# Quartz). Usados pelo modo --file e pelo hook PostToolUse para feedback rápido
# pós-edit. Os checks de fora deste conjunto continuam exclusivos do `/lint` global.
SINGLE_FILE_CHECKS = (
    "frontmatter",
    "fontes_missing",
    "citation_format",
    "citation_resolves",
    "quote_misattributed",
    "broken_links",
    "low_citations",
    "rascunho_stale",
    "divergencias_aberta",
    "tag_taxonomy",
    "tag_coverage",
    "direitos_obras",
    "quote_proportion",
    "mundos_habitados_naming",
    "kardequiano",
)


def _filter_items_to_target(check_result: dict, target_str: str) -> dict:
    """Mantém apenas items cujo `source` ou `path` aponta para `target_str`.

    Necessário porque alguns checks (notadamente `broken_links`) lêem fontes
    auxiliares como `index.md` mesmo quando rodam sobre uma única página —
    no modo single-file queremos só o ruído do arquivo recém-editado.
    """
    filtered = [
        item for item in check_result.get("items", [])
        if (item.get("source") or item.get("path")) == target_str
    ]
    return {
        "severity": check_result["severity"],
        "count": len(filtered),
        "items": filtered,
    }


def lint_single_file(target: Path) -> dict:
    """Roda os checks isoláveis sobre uma única página e devolve resultado filtrado.

    Estrutura espelha `main()` para que callers (CLI `--file`, hook PostToolUse)
    consumam o mesmo schema. Inclui apenas items cujo source/path bate com
    `target` — INDEX_PATH e similares são descartados.
    """
    if not target.exists():
        return {"error": f"arquivo não existe: {target}"}

    pages = [target]
    target_str = str(target)
    checks: dict[str, dict] = {}
    for name in SINGLE_FILE_CHECKS:
        result = CHECK_REGISTRY[name](pages)
        checks[name] = _filter_items_to_target(result, target_str)

    errors = sum(1 for c in checks.values() if c["severity"] == "error" and c["count"] > 0)
    warnings = sum(1 for c in checks.values() if c["severity"] == "warning" and c["count"] > 0)
    infos = sum(1 for c in checks.values() if c["severity"] == "info" and c["count"] > 0)
    total_items = sum(c["count"] for c in checks.values())

    return {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "file": target_str,
        "checks": checks,
        "summary": (
            f"{total_items} achados em {target_str}: "
            f"{errors} erro(s), {warnings} aviso(s), {infos} info"
        ),
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Lint determinístico da wiki IsAbel")
    p.add_argument("--check", action="append", default=[], metavar="NAME",
                   help="Rodar apenas os checks listados (repetível).")
    p.add_argument("--skip", action="append", default=[], metavar="NAME",
                   help="Pular os checks listados (repetível).")
    p.add_argument("--check-urls", action="store_true",
                   help="Habilita check broken_urls (I/O externo, opt-in).")
    p.add_argument("--file", metavar="PATH",
                   help="Modo single-file: roda apenas checks isoláveis sobre PATH "
                        "(consumido pelo hook PostToolUse). Incompatível com --check/--skip.")
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

    if args.file:
        if args.check or args.skip or args.check_urls:
            print(json.dumps({"error": "--file é incompatível com --check/--skip/--check-urls"}),
                  file=sys.stdout)
            sys.exit(2)
        target = Path(args.file)
        result = lint_single_file(target)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if "error" in result:
            sys.exit(1)
        errors = sum(
            1 for c in result["checks"].values()
            if c["severity"] == "error" and c["count"] > 0
        )
        if errors > 0:
            sys.exit(1)
        return

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
