#!/usr/bin/env python3
"""
Estatísticas da wiki IsAbel.

Gera `wiki/sinteses/estatisticas-da-wiki.md` com:
- Totais e cobertura por tipo.
- Métricas de grafo (grau in/out, PageRank, componentes, órfãos) via networkx.
- Vocabulário (top palavras e bigramas) com stopwords PT-BR via nltk.
- Atividade temporal a partir de log.md.
- Tamanho das páginas.

Rodar: `uv run python .claude/skills/stats/scripts/stats_wiki.py`
"""

import re
import sys
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path

import networkx as nx
import nltk

# Acessar módulo compartilhado em .claude/skills/_lib/
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _lib.wiki_utils import (  # noqa: E402
    INDEX_PATH,
    LOG_PATH,
    WIKI_DIR,
    collect_pages,
    find_wikilinks,
    page_key,
    parse_frontmatter,
    resolve_wikilink,
)

OUTPUT_PATH = WIKI_DIR / "sinteses" / "estatisticas-da-wiki.md"
RAW_DIR = Path("raw")

TIPOS_DIR = ["obras", "conceitos", "entidades", "personalidades", "questoes", "aprofundamentos", "sinteses", "divergencias"]

# Tokens/padrões a remover antes de contar palavras
FRONTMATTER_RE = re.compile(r"^---\n.*?\n---\n", re.DOTALL)
CODE_RE = re.compile(r"```.*?```", re.DOTALL)
WIKILINK_RE = re.compile(r"\[\[[^\]]+\]\]")
MDLINK_RE = re.compile(r"\[([^\]]+)\]\([^\)]+\)")
URL_RE = re.compile(r"https?://\S+")
CITATION_RE = re.compile(r"\((?:LE|LM|ESE|C&I|Gênese|RE|OPE|OQE)[^)]*\)")
TOKEN_RE = re.compile(r"[a-záéíóúâêôãõàçA-ZÁÉÍÓÚÂÊÔÃÕÀÇ]{4,}")

# Seções-template/aparato bibliográfico — removidas antes de tokenizar para
# não inflar vocabulário com bigramas tipo "páginas relacionadas" ou
# "trad guillon ribeiro".
TEMPLATE_SECTION_RE = re.compile(
    r"^##\s+(?:Fontes|Páginas relacionadas|Páginas referenciadas|Conceitos relacionados)\s*$.*?(?=^##\s|\Z)",
    re.MULTILINE | re.DOTALL | re.IGNORECASE,
)

SPARK = "▁▂▃▄▅▆▇█"

# Denominadores canônicos do Pentateuco, usados para % de cobertura.
# LM tem 3 caps na 1ª parte (teórica) e 33 na 2ª (prática); contabilizamos a 2ª,
# que concentra o grosso do ensino sobre médiuns.
# C&I soma 11 caps da 1ª parte (doutrina) + 7 da 2ª (exemplos) = 18.
PENTATEUCO_TOTAIS: dict[str, tuple[str, int]] = {
    "LE": ("questões", 1019),
    "LM": ("capítulos da 2ª parte", 33),
    "ESE": ("capítulos", 28),
    "C&I": ("capítulos", 18),
    "Gênese": ("capítulos", 18),
}

LE_CITATION_RE = re.compile(r"\(LE,\s*q\.\s*(\d+)")
ESE_CITATION_RE = re.compile(r"\(ESE,\s*cap\.\s*([IVXLCDM]+)(?:\s*,\s*item\s*(\d+))?")
GENESE_CITATION_RE = re.compile(r"\(Gênese,\s*cap\.\s*([IVXLCDM]+)(?:\s*,\s*item\s*(\d+))?")
LM_CITATION_RE = re.compile(r"\(LM(?:,\s*(\d+)ª?\s*parte)?,\s*cap\.\s*([IVXLCDM]+)")
CI_CITATION_RE = re.compile(r"\(C&I(?:,\s*(\d+)ª?\s*parte)?,\s*cap\.\s*([IVXLCDM]+)")


def ensure_stopwords() -> set[str]:
    """Garante corpus de stopwords do nltk disponível; retorna set PT-BR."""
    try:
        from nltk.corpus import stopwords
        stopwords.words("portuguese")
    except LookupError:
        nltk.download("stopwords", quiet=True)
        from nltk.corpus import stopwords
    extra = {
        "ser", "ter", "haver", "fazer", "pode", "podem", "podemos",
        "assim", "ainda", "quando", "porque", "porém", "sobre", "entre",
        "cada", "todos", "todas", "outro", "outra", "outros", "outras",
        "mesmo", "mesma", "mesmos", "mesmas", "isto", "isso", "aquilo",
        "sendo", "sido", "estar", "está", "estão", "sejam", "seja",
        "parte", "partes", "apenas", "também",
    }
    return set(stopwords.words("portuguese")) | extra


def clean_body(text: str) -> str:
    text = FRONTMATTER_RE.sub("", text)
    text = CODE_RE.sub(" ", text)
    text = TEMPLATE_SECTION_RE.sub("", text)
    text = WIKILINK_RE.sub(" ", text)
    text = MDLINK_RE.sub(r"\1", text)
    text = URL_RE.sub(" ", text)
    text = CITATION_RE.sub(" ", text)
    return text


def is_meta_page(fm: dict) -> bool:
    """Meta-páginas (`tipo: sintese` + tag `meta`) são excluídas de grafo,
    vocabulário e estatísticas de tamanho — são painéis gerados sobre a própria
    wiki e seus links/termos não refletem sinal doutrinário."""
    if fm.get("tipo") != "sintese":
        return False
    tags = fm.get("tags", [])
    if isinstance(tags, list):
        return "meta" in tags
    return "meta" in str(tags)


def tokenize(text: str, stop: set[str]) -> list[str]:
    return [t.lower() for t in TOKEN_RE.findall(text) if t.lower() not in stop]


# ---------------------------------------------------------------------------
# Coletas
# ---------------------------------------------------------------------------

def counts_by_type(pages: list[Path]) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for p in pages:
        parts = p.parts
        if len(parts) >= 2 and parts[0] == "wiki":
            counts[parts[1]] += 1
    return dict(counts)


def counts_by_status(pages: list[Path]) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for p in pages:
        fm, _ = parse_frontmatter(p)
        counts[str(fm.get("status", "desconhecido"))] += 1
    return dict(counts)


def build_graph(pages: list[Path]) -> nx.DiGraph:
    g = nx.DiGraph()
    non_meta = [p for p in pages if not is_meta_page(parse_frontmatter(p)[0])]
    page_keys = {page_key(p) for p in non_meta}
    for p in non_meta:
        g.add_node(page_key(p))
    for p in non_meta:
        text = p.read_text(encoding="utf-8")
        src = page_key(p)
        for _, target in find_wikilinks(text):
            resolved = resolve_wikilink(target)
            tgt = page_key(resolved)
            if tgt in page_keys and tgt != src:
                g.add_edge(src, tgt)
    return g


def word_stats(pages: list[Path], stop: set[str]) -> tuple[Counter, Counter, dict[Path, int]]:
    word_counter: Counter = Counter()
    bigram_counter: Counter = Counter()
    size_by_page: dict[Path, int] = {}
    for p in pages:
        fm, _ = parse_frontmatter(p)
        if is_meta_page(fm):
            continue
        text = p.read_text(encoding="utf-8")
        body = clean_body(text)
        tokens = tokenize(body, stop)
        size_by_page[p] = len(tokens)
        word_counter.update(tokens)
        for a, b in zip(tokens, tokens[1:]):
            bigram_counter[f"{a} {b}"] += 1
    return word_counter, bigram_counter, size_by_page


LOG_ENTRY_RE = re.compile(r"^## \[(\d{4}-\d{2}-\d{2})\] (\w+) \| (.+)$", re.MULTILINE)


def parse_log() -> list[tuple[date, str, str]]:
    if not LOG_PATH.exists():
        return []
    text = LOG_PATH.read_text(encoding="utf-8")
    entries = []
    for m in LOG_ENTRY_RE.finditer(text):
        try:
            d = datetime.strptime(m.group(1), "%Y-%m-%d").date()
        except ValueError:
            continue
        entries.append((d, m.group(2), m.group(3)))
    return entries


def sparkline(values: list[int]) -> str:
    if not values:
        return ""
    mx = max(values)
    if mx == 0:
        return SPARK[0] * len(values)
    return "".join(SPARK[min(len(SPARK) - 1, int((v / mx) * (len(SPARK) - 1)))] for v in values)


def collect_citations(pages: list[Path]) -> dict[str, set]:
    """Coleta conjuntos de referências únicas por obra do Pentateuco."""
    le_q: set[int] = set()
    ese_caps: set[str] = set()
    ese_refs: set[str] = set()
    genese_caps: set[str] = set()
    genese_refs: set[str] = set()
    lm_refs: set[str] = set()
    lm_caps_p2: set[str] = set()
    ci_refs: set[str] = set()
    ci_caps: set[str] = set()
    for p in pages:
        fm, _ = parse_frontmatter(p)
        if is_meta_page(fm):
            continue
        text = p.read_text(encoding="utf-8")
        for m in LE_CITATION_RE.finditer(text):
            le_q.add(int(m.group(1)))
        for m in ESE_CITATION_RE.finditer(text):
            cap = m.group(1)
            ese_caps.add(cap)
            ese_refs.add(f"{cap}/{m.group(2) or '-'}")
        for m in GENESE_CITATION_RE.finditer(text):
            cap = m.group(1)
            genese_caps.add(cap)
            genese_refs.add(f"{cap}/{m.group(2) or '-'}")
        for m in LM_CITATION_RE.finditer(text):
            parte, cap = m.group(1), m.group(2)
            lm_refs.add(f"P{parte or '?'}/{cap}")
            if parte == "2":
                lm_caps_p2.add(cap)
        for m in CI_CITATION_RE.finditer(text):
            parte, cap = m.group(1), m.group(2)
            key = f"P{parte or '?'}/{cap}"
            ci_refs.add(key)
            ci_caps.add(key)
    return {
        "LE_questions": le_q,
        "ESE_chapters": ese_caps,
        "ESE_refs": ese_refs,
        "Genese_chapters": genese_caps,
        "Genese_refs": genese_refs,
        "LM_chapters_p2": lm_caps_p2,
        "LM_refs": lm_refs,
        "CI_chapters": ci_caps,
        "CI_refs": ci_refs,
    }


def broken_wikilinks(pages: list[Path]) -> Counter:
    """Conta wikilinks cujo target não resolve para um arquivo existente."""
    broken: Counter = Counter()
    for p in pages:
        fm, _ = parse_frontmatter(p)
        if is_meta_page(fm):
            continue
        text = p.read_text(encoding="utf-8")
        for _, target in find_wikilinks(text):
            resolved = resolve_wikilink(target)
            if not resolved.exists():
                broken[target] += 1
    return broken


def le_coverage_buckets(questions: set[int], bucket: int = 100, total: int = 1019) -> list[tuple[str, int, int]]:
    """Agrupa questões do LE em blocos e retorna (intervalo, cobertas, tamanho)."""
    results: list[tuple[str, int, int]] = []
    for start in range(1, total + 1, bucket):
        end = min(start + bucket - 1, total)
        count = sum(1 for q in questions if start <= q <= end)
        results.append((f"{start:>4}–{end:>4}", count, end - start + 1))
    return results


# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------

def wikilink_for(node: str) -> str:
    return f"[[{node}]]"


def render(pages: list[Path]) -> str:
    today = date.today().isoformat()
    stop = ensure_stopwords()

    tcounts = counts_by_type(pages)
    scounts = counts_by_status(pages)
    graph = build_graph(pages)
    words, bigrams, sizes = word_stats(pages, stop)
    log_entries = parse_log()
    citations = collect_citations(pages)
    broken = broken_wikilinks(pages)

    n_conceitos = tcounts.get("conceitos", 0)
    n_questoes = tcounts.get("questoes", 0)
    ratio_cq = f"{n_conceitos / n_questoes:.1f}" if n_questoes else "—"

    raw_total = sum(1 for _ in RAW_DIR.rglob("*.md")) if RAW_DIR.exists() else 0

    # --- Grafo ---
    in_deg = sorted(graph.in_degree(), key=lambda x: -x[1])[:15]
    out_deg = sorted(graph.out_degree(), key=lambda x: -x[1])[:15]
    pr = sorted(nx.pagerank(graph).items(), key=lambda x: -x[1])[:15] if graph.number_of_edges() else []

    components = list(nx.weakly_connected_components(graph))
    components.sort(key=len, reverse=True)
    largest = len(components[0]) if components else 0
    small_components = [c for c in components if len(c) <= 2]
    small_component_nodes = sorted({n for c in small_components for n in c})

    orphans = sorted([n for n, d in graph.in_degree() if d == 0])

    # --- Atividade ---
    by_month_type: dict[tuple[str, str], int] = defaultdict(int)
    for d, tipo, _ in log_entries:
        by_month_type[(d.strftime("%Y-%m"), tipo)] += 1
    months = sorted({m for m, _ in by_month_type.keys()})
    types = sorted({t for _, t in by_month_type.keys()})

    day_counter = Counter(d.isoformat() for d, _, _ in log_entries)

    # --- Tamanho ---
    buckets = [("<200", 0), ("200-500", 0), ("500-1000", 0), ("1000-2000", 0), (">2000", 0)]
    bucket_counts = {k: 0 for k, _ in buckets}
    for n in sizes.values():
        if n < 200:
            bucket_counts["<200"] += 1
        elif n < 500:
            bucket_counts["200-500"] += 1
        elif n < 1000:
            bucket_counts["500-1000"] += 1
        elif n < 2000:
            bucket_counts["1000-2000"] += 1
        else:
            bucket_counts[">2000"] += 1
    largest_pages = sorted(sizes.items(), key=lambda x: -x[1])[:10]
    smallest_pages = sorted(sizes.items(), key=lambda x: x[1])[:10]

    # --- Sugestões ---
    suggestions = []
    if orphans:
        suggestions.append(f"**{len(orphans)} páginas órfãs** (grau de entrada = 0) — considerar adicionar backlinks a partir de conceitos/obras relacionados.")
    candidates_for_page = [(w, c) for w, c in words.most_common(200) if c >= 20]
    page_slugs = {Path(page_key(p)).name for p in pages}
    missing_word_pages = [(w, c) for w, c in candidates_for_page if w not in page_slugs][:15]
    if missing_word_pages:
        termos = ", ".join(f"`{w}` ({c})" for w, c in missing_word_pages[:8])
        suggestions.append(f"**Termos frequentes sem página própria**: {termos} — candidatos a novos conceitos ou sinônimos a padronizar.")
    if small_component_nodes:
        suggestions.append(f"**{len(small_component_nodes)} páginas em componentes isolados** (≤2 nós) — candidatas a integração no grafo principal.")

    broken_top = sorted(((t, c) for t, c in broken.items() if c >= 5), key=lambda x: -x[1])
    if broken_top:
        amostra = ", ".join(f"`{t}` ({c})" for t, c in broken_top[:8])
        suggestions.append(
            f"**{len(broken_top)} targets de wikilink referenciados 5+ vezes sem página**: {amostra} — "
            "candidatos diretos a novas páginas (conceitos/personalidades/obras)."
        )

    uncovered_le_blocks = [(label, count, size) for label, count, size in le_coverage_buckets(citations["LE_questions"]) if count / size < 0.20]
    if uncovered_le_blocks:
        blocos = ", ".join(f"{l.replace(' ', '')} ({c}/{s})" for l, c, s in uncovered_le_blocks[:6])
        suggestions.append(
            f"**{len(uncovered_le_blocks)} blocos de 100 questões do LE com <20% de cobertura**: {blocos}. "
            "Priorizar extração de questões-chave desses intervalos para `wiki/questoes/`."
        )

    if n_questoes and n_conceitos / n_questoes > 20:
        suggestions.append(
            f"**Razão conceitos/questões muito alta** ({n_conceitos}:{n_questoes} = {ratio_cq}). "
            "`wiki/questoes/` está sub-representada; ver item §3 do ROADMAP."
        )

    # ---------------------------------------------------------------- Markdown
    lines: list[str] = []

    lines.append("---")
    lines.append("tipo: sintese")
    lines.append("fontes: [meta]")
    lines.append("tags: [estatisticas, meta, grafo, vocabulario]")
    lines.append(f"atualizado_em: {today}")
    lines.append("status: ativo")
    lines.append("---")
    lines.append("")
    lines.append("# Estatísticas da wiki")
    lines.append("")
    lines.append("## Pergunta motivadora")
    lines.append("")
    lines.append(
        "Como a wiki IsAbel está distribuída entre obras, conceitos e entidades? "
        "Quais são os nós centrais do grafo, quais páginas estão isoladas, que "
        "termos dominam o vocabulário, e como é o ritmo de ingestão ao longo do "
        "tempo? Esta página é **regenerada automaticamente** — serve como painel "
        "para orientar expansões, backlinks faltantes e possíveis novos conceitos."
    )
    lines.append("")
    lines.append(f"> Gerado em **{today}** por `.claude/skills/stats/scripts/stats_wiki.py`.")
    lines.append("")

    # --- Resumo ---
    lines.append("## Resumo executivo")
    lines.append("")
    lines.append(f"- Páginas na wiki: **{len(pages)}**")
    lines.append(f"- Arquivos em `raw/`: **{raw_total}**")
    lines.append(f"- Nós no grafo: **{graph.number_of_nodes()}** · Arestas: **{graph.number_of_edges()}**")
    lines.append(f"- Componentes fracamente conexos: **{len(components)}** (maior: {largest} nós)")
    lines.append(f"- Páginas órfãs (sem backlinks): **{len(orphans)}**")
    lines.append(f"- Vocabulário único (após stopwords): **{len(words)}** termos")
    lines.append(f"- Entradas em `log.md`: **{len(log_entries)}**")
    lines.append(f"- Razão conceitos/questões: **{n_conceitos}:{n_questoes}** ({ratio_cq})")
    le_pct = 100 * len(citations["LE_questions"]) / PENTATEUCO_TOTAIS["LE"][1]
    lines.append(f"- Questões únicas do LE citadas: **{len(citations['LE_questions'])}/1019** ({le_pct:.1f}%)")
    broken_5 = [t for t, c in broken.items() if c >= 5]
    lines.append(f"- Wikilinks não resolvidos (freq ≥ 5): **{len(broken_5)}** targets")
    lines.append("")

    # --- Cobertura ---
    lines.append("## Cobertura por tipo")
    lines.append("")
    lines.append("| Diretório | Páginas |")
    lines.append("|-----------|---------|")
    for t in TIPOS_DIR:
        if t in tcounts:
            lines.append(f"| `wiki/{t}/` | {tcounts[t]} |")
    for t in sorted(tcounts):
        if t not in TIPOS_DIR:
            lines.append(f"| `wiki/{t}/` | {tcounts[t]} |")
    lines.append("")
    lines.append("### Status")
    lines.append("")
    lines.append("| Status | Páginas |")
    lines.append("|--------|---------|")
    for k in sorted(scounts, key=lambda k: -scounts[k]):
        lines.append(f"| `{k}` | {scounts[k]} |")
    lines.append("")

    # --- Cobertura doutrinária ---
    lines.append("## Cobertura doutrinária")
    lines.append("")
    lines.append(
        "Referências únicas do Pentateuco efetivamente citadas pela wiki "
        "(`(LE, q. N)`, `(ESE, cap. X, item Y)`, etc.). Mede o quanto da "
        "codificação já foi ancorado em páginas próprias."
    )
    lines.append("")
    lines.append("| Obra | Unidade | Citadas | Total | Cobertura |")
    lines.append("|------|---------|--------:|------:|----------:|")
    le_n = len(citations["LE_questions"])
    lines.append(f"| LE | questões | {le_n} | 1019 | {100 * le_n / 1019:.1f}% |")
    ese_n = len(citations["ESE_chapters"])
    lines.append(f"| ESE | capítulos | {ese_n} | 28 | {100 * ese_n / 28:.1f}% |")
    gen_n = len(citations["Genese_chapters"])
    lines.append(f"| Gênese | capítulos | {gen_n} | 18 | {100 * gen_n / 18:.1f}% |")
    lm_n = len(citations["LM_chapters_p2"])
    lines.append(f"| LM | capítulos da 2ª parte | {lm_n} | 33 | {100 * lm_n / 33:.1f}% |")
    ci_n = len(citations["CI_chapters"])
    lines.append(f"| C&I | capítulos | {ci_n} | 18 | {100 * ci_n / 18:.1f}% |")
    lines.append("")
    lines.append(
        f"Referências `cap./item` únicas: ESE **{len(citations['ESE_refs'])}**, "
        f"Gênese **{len(citations['Genese_refs'])}**, LM **{len(citations['LM_refs'])}**, "
        f"C&I **{len(citations['CI_refs'])}**."
    )
    lines.append("")
    lines.append("### Cobertura do LE por bloco de 100 questões")
    lines.append("")
    lines.append("```")
    for label, count, size in le_coverage_buckets(citations["LE_questions"]):
        bar = "█" * int(30 * count / size) + "·" * int(30 * (1 - count / size))
        pct = 100 * count / size
        lines.append(f"{label}  {bar}  {count:>3}/{size} ({pct:.0f}%)")
    lines.append("```")
    lines.append("")

    # --- Grafo ---
    lines.append("## Grafo de conhecimento")
    lines.append("")
    lines.append("### Mais referenciados (grau de entrada)")
    lines.append("")
    lines.append("| # | Página | In |")
    lines.append("|---|--------|----|")
    for i, (n, d) in enumerate(in_deg, 1):
        lines.append(f"| {i} | {wikilink_for(n)} | {d} |")
    lines.append("")
    lines.append("### Mais conectores (grau de saída)")
    lines.append("")
    lines.append("| # | Página | Out |")
    lines.append("|---|--------|-----|")
    for i, (n, d) in enumerate(out_deg, 1):
        lines.append(f"| {i} | {wikilink_for(n)} | {d} |")
    lines.append("")
    if pr:
        lines.append("### Centralidade (PageRank)")
        lines.append("")
        lines.append("| # | Página | PR |")
        lines.append("|---|--------|-----|")
        for i, (n, score) in enumerate(pr, 1):
            lines.append(f"| {i} | {wikilink_for(n)} | {score:.4f} |")
        lines.append("")

    lines.append("### Páginas órfãs (sem backlinks)")
    lines.append("")
    if orphans:
        for n in orphans[:30]:
            lines.append(f"- {wikilink_for(n)}")
        if len(orphans) > 30:
            lines.append(f"- … e mais {len(orphans) - 30} páginas.")
    else:
        lines.append("_Nenhuma página órfã._")
    lines.append("")

    lines.append("### Componentes isolados (≤ 2 nós)")
    lines.append("")
    if small_component_nodes:
        for n in small_component_nodes[:30]:
            lines.append(f"- {wikilink_for(n)}")
    else:
        lines.append("_Nenhum._")
    lines.append("")

    # --- Vocabulário ---
    lines.append("## Vocabulário")
    lines.append("")
    lines.append("### Top 50 termos")
    lines.append("")
    lines.append("| # | Termo | Ocorrências |")
    lines.append("|---|-------|-------------|")
    for i, (w, c) in enumerate(words.most_common(50), 1):
        lines.append(f"| {i} | `{w}` | {c} |")
    lines.append("")
    lines.append("### Top 20 bigramas")
    lines.append("")
    lines.append("| # | Bigrama | Ocorrências |")
    lines.append("|---|---------|-------------|")
    for i, (w, c) in enumerate(bigrams.most_common(20), 1):
        lines.append(f"| {i} | `{w}` | {c} |")
    lines.append("")

    # --- Atividade ---
    lines.append("## Atividade no tempo")
    lines.append("")
    if months:
        lines.append(f"Período coberto: **{months[0]}** → **{months[-1]}** ({len(months)} meses).")
        lines.append("")
        lines.append("### Sparkline por tipo")
        lines.append("")
        lines.append("```")
        for t in types:
            series = [by_month_type.get((m, t), 0) for m in months]
            lines.append(f"{t:<10} {sparkline(series)}  total={sum(series)}")
        lines.append("```")
        lines.append("")
        lines.append("### Tabela mensal")
        lines.append("")
        header = "| Mês | " + " | ".join(types) + " | Total |"
        sep = "|-----|" + "|".join(["---"] * len(types)) + "|-------|"
        lines.append(header)
        lines.append(sep)
        for m in months:
            row_vals = [by_month_type.get((m, t), 0) for t in types]
            lines.append(f"| {m} | " + " | ".join(str(v) for v in row_vals) + f" | {sum(row_vals)} |")
        lines.append("")
        lines.append("### Dias mais ativos")
        lines.append("")
        lines.append("| Data | Entradas |")
        lines.append("|------|----------|")
        for d, c in day_counter.most_common(10):
            lines.append(f"| {d} | {c} |")
        lines.append("")
    else:
        lines.append("_Sem entradas em `log.md`._")
        lines.append("")

    # --- Tamanho ---
    lines.append("## Tamanho das páginas")
    lines.append("")
    max_bucket = max(bucket_counts.values()) if bucket_counts else 1
    lines.append("```")
    for label, _ in buckets:
        n = bucket_counts[label]
        bar = "█" * int(30 * n / max_bucket) if max_bucket else ""
        lines.append(f"{label:<10} {n:>4}  {bar}")
    lines.append("```")
    lines.append("")
    lines.append("### Maiores")
    lines.append("")
    for p, n in largest_pages:
        lines.append(f"- {wikilink_for(page_key(p))} — {n} palavras")
    lines.append("")
    lines.append("### Menores (candidatas a expansão)")
    lines.append("")
    for p, n in smallest_pages:
        lines.append(f"- {wikilink_for(page_key(p))} — {n} palavras")
    lines.append("")

    # --- Wikilinks não resolvidos ---
    lines.append("## Referências não resolvidas")
    lines.append("")
    lines.append(
        "Wikilinks `[[...]]` cujo target não existe na árvore — candidatos a "
        "páginas novas (quando frequentes) ou erros de digitação (quando raros)."
    )
    lines.append("")
    if broken:
        top_broken = sorted(broken.items(), key=lambda x: -x[1])
        freq_broken = [(t, c) for t, c in top_broken if c >= 5]
        lines.append(f"Total: **{len(broken)}** targets distintos, **{sum(broken.values())}** ocorrências. Freq ≥ 5: **{len(freq_broken)}**.")
        lines.append("")
        lines.append("### Mais referenciados (freq ≥ 3)")
        lines.append("")
        lines.append("| # | Target | Ocorrências |")
        lines.append("|---|--------|------------:|")
        rows = [(t, c) for t, c in top_broken if c >= 3][:30]
        for i, (t, c) in enumerate(rows, 1):
            lines.append(f"| {i} | `{t}` | {c} |")
        if not rows:
            lines.append("| — | _nenhum com freq ≥ 3_ | — |")
        lines.append("")
    else:
        lines.append("_Nenhum wikilink quebrado._")
        lines.append("")

    # --- Sugestões ---
    lines.append("## Sugestões automáticas")
    lines.append("")
    if suggestions:
        for s in suggestions:
            lines.append(f"- {s}")
    else:
        lines.append("_Nada a sugerir._")
    lines.append("")

    # --- Páginas referenciadas ---
    lines.append("## Páginas referenciadas")
    lines.append("")
    lines.append(f"- [[{page_key(INDEX_PATH)}]]")
    lines.append(f"- `{LOG_PATH}`")
    lines.append("")

    # --- Fontes ---
    lines.append("## Fontes")
    lines.append("")
    lines.append(f"- Script gerador: `.claude/skills/stats/scripts/stats_wiki.py` (execução em {today}).")
    lines.append("- Corpus analisado: `wiki/**/*.md`, `log.md`, `raw/**/*.md`.")
    lines.append("- Dependências: `networkx` (grafo, PageRank), `nltk` (stopwords PT-BR).")
    lines.append("- Filtros: meta-páginas (`tipo: sintese` + tag `meta`) são excluídas de grafo, vocabulário, tamanho, cobertura doutrinária e wikilinks quebrados; seções-template (`## Fontes`, `## Páginas relacionadas`, `## Páginas referenciadas`, `## Conceitos relacionados`) são removidas antes da tokenização.")
    lines.append("- Cobertura doutrinária: regex sobre citações inline `(LE, q. N)`, `(ESE, cap. X, item Y)`, `(Gênese, cap. X, item Y)`, `(LM, Nª parte, cap. X)`, `(C&I, Nª parte, cap. X)`. Totais canônicos: LE=1019q; ESE=28c; Gênese=18c; LM=33c (2ª parte); C&I=18c (11 + 7).")
    lines.append("")

    return "\n".join(lines)


def main():
    if not WIKI_DIR.exists():
        print("Diretório wiki/ não encontrado.", file=sys.stderr)
        sys.exit(1)
    pages = collect_pages()
    content = render(pages)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(content, encoding="utf-8")
    print(f"Escrito: {OUTPUT_PATH} ({len(content)} bytes, {len(pages)} páginas analisadas)")


if __name__ == "__main__":
    main()
