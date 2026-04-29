#!/usr/bin/env python3
"""Sugere candidatos a termos do dicionário de glossário (data/dicionario.json).

Heurística: varre `wiki/` por substantivos comuns (não nomes próprios) que:
  - não estão no dicionário,
  - aparecem ≥ 2 vezes,
  - têm pelo menos 1 ocorrência em contexto bíblico/histórico
    (linha com citação evangélica, marcadores tipo "parábola/Jesus/Israel/
    Jerusalém/romano/judaic-/templo/antig-/hebrai-", ou em página com tipo
    `obra` cujo frontmatter referencia Evangelhos).

Saída: JSON em stdout. Ranking primário por `biblical_count` desc, depois
`count` desc.

Uso:
  uv run python .claude/skills/glossario/scripts/sugerir_termos.py
  uv run python .claude/skills/glossario/scripts/sugerir_termos.py --top 50
  uv run python .claude/skills/glossario/scripts/sugerir_termos.py --min-count 3
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

SKILLS_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILLS_DIR))

from _lib.wiki_utils import WIKI_DIR, collect_pages, parse_frontmatter  # noqa: E402

import nltk  # noqa: E402

DEFAULT_DICT = Path("data") / "dicionario.json"

FRONTMATTER_RE = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)
CODE_RE = re.compile(r"```.*?```|`[^`\n]+`", re.DOTALL)
WIKILINK_RE = re.compile(r"\[\[[^\]\n]+\]\]")
MDLINK_RE = re.compile(r"\[([^\]\n]+)\]\([^)\n]+\)")
URL_RE = re.compile(r"https?://\S+")
ABBR_RE = re.compile(r"<abbr\b[^>]*>(.*?)</abbr>", re.DOTALL)
HEADING_RE = re.compile(r"^#{1,6}\s.*$", re.MULTILINE)
CITATION_RE = re.compile(r"\((?:LE|LM|ESE|C&I|Gênese|RE|OPE|OQE)[^)]*\)")

# Tokens de tamanho ≥ 5 com letras (PT-BR + acentos).
TOKEN_RE = re.compile(r"[A-Za-zÁÉÍÓÚÂÊÔÃÕÀÇáéíóúâêôãõàç]{5,}")

# Citação bíblica abreviada: "Mt 9:9", "Lc 15:11", "Jo 4:7", "Mc 12:42",
# "Gn 18:27", etc. Aceita ranges (Mt 9:9-13).
BIBLICAL_REF_RE = re.compile(
    r"\b(?:Mt|Mc|Lc|Jo|Gn|Êx|Ex|Lv|Nm|Dt|Sl|Pv|Is|Jr|Ez|Dn|Os|Jn|At|Rm|"
    r"1Co|2Co|Gl|Ef|Fp|Cl|1Ts|2Ts|1Tm|2Tm|Tt|Fm|Hb|Tg|1Pe|2Pe|1Jo|2Jo|3Jo|Jd|Ap)"
    r"\s+\d+(?::\d+(?:[-–]\d+)?)?",
    re.IGNORECASE,
)

# Marcadores de contexto bíblico/histórico em prosa.
CONTEXT_KEYWORDS_RE = re.compile(
    r"\b(?:par[áa]bola|evangelho|jesus|israel|jerusal[ée]m|"
    r"jud(?:eu|aica|aico|aicos|aicas|aicos|aismo)|"
    r"romano|romana|romanos|romanas|"
    r"templo|antig(?:o|a|os|as|uidade)|"
    r"hebrai(?:co|ca|cos|cas|smo)|samari(?:tan[oa]s?|a)|"
    r"profeta|messi[âa])\b",
    re.IGNORECASE,
)

# Vocabulário doutrinário/meta-wiki que NUNCA é candidato — não é cultural-
# arcaico, é a língua da própria wiki. Mantido hard-coded; expandir conforme
# o ranking acumular ruído.
DOCTRINAL_STOPLIST = {
    # núcleo espírita
    "espírito", "espíritos", "espírita", "espíritas", "espiritismo",
    "espirituais", "espiritual", "espiritualidade",
    "doutrina", "doutrinária", "doutrinário", "doutrinárias", "doutrinários",
    "evangelho", "evangelhos", "evangélica", "evangélico", "evangélicos",
    "parábola", "parábolas",
    "caridade", "caridoso", "caridosa",
    "médium", "médiuns", "mediúnico", "mediúnica", "mediúnicas", "mediúnicos",
    "mediunidade", "mediunidades",
    "perispírito", "perispiritual",
    "reencarnação", "reencarnações", "reencarnar", "reencarnado", "reencarnada",
    "encarnação", "encarnações", "encarnar", "encarnado", "encarnada",
    "desencarnado", "desencarnada", "desencarnação",
    "fluido", "fluidos", "fluídico", "fluídica",
    "kardec", "allan", "pentateuco", "codificação",
    "comunicação", "comunicações", "comunicante", "comunicantes",
    "obsessão", "obsessões", "obsessor", "obsessores", "obsessado",
    # meta-wiki / léxico geral recorrente
    "moral", "morais",
    "leitura", "leituras", "estudo", "estudos",
    "questão", "questões", "capítulo", "capítulos", "item", "itens",
    "página", "páginas", "obra", "obras", "trecho", "trechos",
    "aprofundamento", "aprofundamentos", "síntese", "sínteses",
    "seção", "seções", "tema", "temas", "subseção", "subseções",
    "história", "histórica", "histórico", "históricas", "históricos",
    "exemplo", "exemplos", "termo", "termos",
    "segundo", "primeiro", "terceiro", "quarto", "quinto",
    "também", "ainda", "porém", "contudo", "todavia",
    "natureza", "presença", "existência", "verdade", "vida",
    "homem", "homens", "humano", "humana", "humanos", "humanas",
    "mundo", "mundos", "terra", "alma", "almas",
    # kardecismo recorrente
    "criação", "lei", "leis", "justiça", "amor",
    "deus", "jesus", "cristo", "cristã", "cristão",
    "sentido", "sentidos", "forma", "formas", "noção", "ideia", "ideias",
    "ponto", "pontos", "caso", "casos", "tipo", "tipos",
    "modo", "modos", "fato", "fatos", "ato", "atos",
    "objeto", "sujeito", "presente", "atual", "atuais",
    "geral", "comum", "comuns", "próprio", "própria", "próprios", "próprias",
}


def load_dict_terms(path: Path) -> set[str]:
    if not path.is_file():
        return set()
    raw = json.loads(path.read_text(encoding="utf-8"))
    termos = raw.get("termos", raw)
    return {k.lower() for k in termos if not k.startswith("_")}


def ensure_stopwords() -> set[str]:
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
        "parte", "partes", "apenas", "também", "muito", "muitos", "muitas",
        "pouco", "poucos", "poucas", "qualquer", "quais", "depois",
        "antes", "ent", "como", "onde", "porém",
    }
    return set(stopwords.words("portuguese")) | extra


def clean_text(text: str) -> str:
    text = FRONTMATTER_RE.sub("", text)
    text = CODE_RE.sub(" ", text)
    text = ABBR_RE.sub(r"\1", text)  # preserva o termo, descarta a tag
    text = WIKILINK_RE.sub(" ", text)
    text = MDLINK_RE.sub(r"\1", text)
    text = URL_RE.sub(" ", text)
    text = CITATION_RE.sub(" ", text)
    return text


def is_evangelho_page(fm: dict) -> bool:
    if fm.get("tipo") != "obra":
        return False
    fontes = fm.get("fontes", [])
    if isinstance(fontes, str):
        fontes = [fontes]
    return any("evangelho" in str(f).lower() for f in fontes)


def extract_snippet(line: str, term_lower: str, max_len: int = 140) -> str:
    """Recorta a linha em volta da palavra-alvo, com elipse."""
    line_clean = re.sub(r"\s+", " ", line).strip()
    lower = line_clean.lower()
    idx = lower.find(term_lower)
    if idx < 0:
        return line_clean[:max_len]
    half = max_len // 2
    start = max(0, idx - half)
    end = min(len(line_clean), idx + len(term_lower) + half)
    snippet = line_clean[start:end]
    if start > 0:
        snippet = "…" + snippet
    if end < len(line_clean):
        snippet = snippet + "…"
    return snippet


def scan_pages(stopwords_pt: set[str], dict_terms: set[str]):
    """Acumula stats por palavra (lowercase).

    Retorna dict[term_lower] = {
        "count": int,
        "biblical_count": int,
        "always_capitalized": bool,  # filtra nomes próprios
        "pages": set[str],
        "contexts": list[str],  # até 3 snippets, priorizando os bíblicos
    }
    """
    stats: dict[str, dict] = defaultdict(lambda: {
        "count": 0,
        "biblical_count": 0,
        "always_capitalized": True,
        "pages": set(),
        "contexts": [],
    })
    total_tokens = 0

    for path in collect_pages():
        text = path.read_text(encoding="utf-8")
        fm, _ = parse_frontmatter(path)
        body = clean_text(text)
        # Remove headings da varredura para não contar palavras de título.
        body = HEADING_RE.sub("", body)
        page_is_evangelho = is_evangelho_page(fm)

        for line in body.splitlines():
            if not line.strip():
                continue
            line_is_biblical = (
                page_is_evangelho
                or bool(BIBLICAL_REF_RE.search(line))
                or bool(CONTEXT_KEYWORDS_RE.search(line))
            )
            for m in TOKEN_RE.finditer(line):
                token = m.group(0)
                lower = token.lower()
                total_tokens += 1
                if lower in stopwords_pt:
                    continue
                if lower in dict_terms:
                    continue
                entry = stats[lower]
                entry["count"] += 1
                if line_is_biblical:
                    entry["biblical_count"] += 1
                if not (token[0].isupper() and token[1:] == token[1:].lower()):
                    # forma não-Title: tem minúscula em posição de início.
                    # Se é toda-minúscula ou misto, definitivamente não é
                    # nome próprio "puro".
                    if not token[0].isupper():
                        entry["always_capitalized"] = False
                entry["pages"].add(str(path))
                if len(entry["contexts"]) < 3 and line_is_biblical:
                    entry["contexts"].append(extract_snippet(line, lower))
        # Segunda passada: completa contextos não-bíblicos só se faltarem.
        for line in body.splitlines():
            if not line.strip():
                continue
            for m in TOKEN_RE.finditer(line):
                lower = m.group(0).lower()
                if lower in stats and len(stats[lower]["contexts"]) < 2:
                    snippet = extract_snippet(line, lower)
                    if snippet not in stats[lower]["contexts"]:
                        stats[lower]["contexts"].append(snippet)

    return stats, total_tokens


def filter_and_rank(
    stats: dict, min_count: int, top: int,
    max_pages: int, min_ratio: float,
):
    """Aplica heurísticas que separam termo cultural-arcaico de doutrinário.

    - count >= min_count (recorrência mínima);
    - biblical_count / count >= min_ratio (concentração em contexto bíblico);
    - pages_distinct <= max_pages (termo nicho, não onipresente);
    - sem ocorrência sempre-capitalizada (filtra nomes próprios);
    - fora de DOCTRINAL_STOPLIST.
    """
    candidates = []
    for term, e in stats.items():
        if e["count"] < min_count:
            continue
        if e["biblical_count"] == 0:
            continue
        if e["always_capitalized"]:
            continue
        if term in DOCTRINAL_STOPLIST:
            continue
        if len(e["pages"]) > max_pages:
            continue
        ratio = e["biblical_count"] / e["count"]
        if ratio < min_ratio:
            continue
        candidates.append({
            "term": term,
            "count": e["count"],
            "biblical_count": e["biblical_count"],
            "biblical_ratio": round(ratio, 2),
            "pages_distinct": len(e["pages"]),
            "pages_sample": sorted(e["pages"])[:3],
            "contexts": e["contexts"][:3],
        })
    candidates.sort(
        key=lambda c: (-c["biblical_ratio"], -c["count"], c["term"])
    )
    return candidates[:top]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--top", type=int, default=30)
    ap.add_argument("--min-count", type=int, default=2)
    ap.add_argument("--max-pages", type=int, default=15,
                    help="termo é candidato apenas se aparece em ≤ N páginas distintas")
    ap.add_argument("--min-ratio", type=float, default=0.7,
                    help="biblical_count/count mínimo (0.0–1.0)")
    ap.add_argument("--dicionario", type=Path, default=DEFAULT_DICT)
    args = ap.parse_args(argv)

    if not WIKI_DIR.is_dir():
        print(f"Diretório {WIKI_DIR} não encontrado — rodar da raiz do repo.",
              file=sys.stderr)
        return 2

    stopwords_pt = ensure_stopwords()
    dict_terms = load_dict_terms(args.dicionario)
    stats, total_tokens = scan_pages(stopwords_pt, dict_terms)
    candidates = filter_and_rank(
        stats, args.min_count, args.top,
        max_pages=args.max_pages, min_ratio=args.min_ratio,
    )

    output = {
        "candidates": candidates,
        "stats": {
            "total_tokens_scanned": total_tokens,
            "unique_lemmas": len(stats),
            "candidates_returned": len(candidates),
            "dict_terms_loaded": len(dict_terms),
        },
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
