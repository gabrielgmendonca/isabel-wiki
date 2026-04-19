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
    lines.append("- Filtros: meta-páginas (`tipo: sintese` + tag `meta`) são excluídas de grafo, vocabulário e tamanho; seções-template (`## Fontes`, `## Páginas relacionadas`, `## Páginas referenciadas`, `## Conceitos relacionados`) são removidas antes da tokenização.")
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
