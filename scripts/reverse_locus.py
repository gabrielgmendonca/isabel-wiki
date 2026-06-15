#!/usr/bin/env python3
"""Índice reverso de locus do Pentateuco — dada uma aspa, acha onde ela mora.

`cite.py` vai locus→texto (`(LE, q. 918)` → o texto da q. 918). Este módulo faz
o inverso: texto→locus. Dada uma frase atribuída "entre aspas" a Kardec, varre
a obra inteira e devolve o(s) locus de **cobertura máxima** — a questão/item cujo
texto mais se parece com a aspa.

Para que serve: distinguir, deterministicamente, as duas classes graves de erro
de citação do Pentateuco (ROADMAP §12):

- **aspa fabricada** (classe 1 do §12): a frase não aparece em locus nenhum da
  obra → nenhum candidato tem cobertura alta.
- **aspa mal-atribuída** (classe 2 do §12): a frase existe, mas o `(SIGLA, ref)` citado
  aponta para a questão errada → outro locus cobre muito melhor que o citado.
  Esse é o erro mais comum nos itens diferidos do `/critica`, e fica
  **auto-corrigível**: basta trocar o `ref` pelo sugerido.

A premissa que torna isto determinístico (a mesma do §12): a wiki e o corpus
`raw/kardec/pentateuco/` usam a mesma edição (Guillon Ribeiro/FEB), então aspa
genuína bate ~verbatim e aspa fabricada diverge muito — a separação de sinal
sustenta um threshold de fuzzy match (cobertura de palavras em ordem, via
`difflib`, tolerante a acento/caixa/pontuação/rewording leve).

Reusa a maquinaria de segmentação de `cite.py` (`_ITEM_RE`, `_find_block`,
`_HEADING_RE`, ranges de capítulo do `.index.md`) — sem reimplementar o parser.

Uso (CLI, para conferência humana ao corrigir uma citação):

    uv run python scripts/reverse_locus.py LE "A perfeição moral consiste em..."
    uv run python scripts/reverse_locus.py ESE "Atire-lhe a primeira pedra" --top 5
"""
from __future__ import annotations

import argparse
import difflib
import re
import sys
import unicodedata
from dataclasses import dataclass
from functools import lru_cache

from cite import (
    SIGLA_TO_SLUG,
    _CAP_ITEM_RE,
    _HEADING_RE,
    _INDEX_LINE_RE,
    _INDEX_PART_RE,
    _ITEM_RE,
    _PART_ORDINAL,
    _find_block,
    _read_lines,
)
from kardec_structure import (
    PENTATEUCO_DIR,
    _CAP_RE,
    _PART_NUM_RE,
    _Q_RE,
)

# ─── normalização e cobertura (fonte única; o lint importa daqui) ───────────────
# Marcadores de elisão colapsados antes do match: "...", "…", "[...]", "[…]".
_ELISION_RE = re.compile(r"\[\s*(?:\.\.\.|…)\s*\]|\.\.\.|…")


def normalize(s: str) -> str:
    """Casefold + sem acento + só alfanumérico colapsado em espaço único.
    Absorve diferenças de pontuação, caixa e diacrítico entre aspa e fonte."""
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


# Tamanho mínimo de bloco contíguo contado na cobertura. CRÍTICO para a busca
# reversa: somar TODOS os matching blocks (inclusive de 1 palavra) infla a
# cobertura contra alvos longos — `difflib` alinha palavras funcionais soltas
# ("a", "de", "que") espalhadas por uma questão extensa, e a questão mais COMPRIDA
# vence por acaso, não por conter a aspa. Empiricamente (fórmula da perfeição
# moral, q.918): com min_block=1 o índice apontava q.222 (questão longa sobre
# Pitágoras, FP); exigindo runs contíguos ≥3 palavras, q.918 — o locus real —
# passa a vencer. Aspa verbatim tem um bloco longo único → fica ~1.0 de qualquer
# forma; o min_block só corta o ruído de scatter.
_MIN_CONTIG_BLOCK = 3


def word_coverage(quote: str, target: str, min_block: int = _MIN_CONTIG_BLOCK) -> float:
    """Fração das palavras da aspa cobertas por runs CONTÍGUOS (≥ `min_block`
    palavras) presentes no `target`, via `difflib` a nível de palavra. 1.0 = aspa
    verbatim; baixo = a aspa não aparece como trecho contíguo no alvo. Tolera
    acento/caixa/pontuação/elisão; descarta alinhamento disperso de palavras
    funcionais (a fonte de falso-positivo contra questões longas)."""
    qw = normalize(_ELISION_RE.sub(" ", quote)).split()
    tw = normalize(target).split()
    if not qw:
        return 1.0
    sm = difflib.SequenceMatcher(None, qw, tw, autojunk=False)
    return sum(b.size for b in sm.get_matching_blocks() if b.size >= min_block) / len(qw)


# ─── índice de segmentos por obra ───────────────────────────────────────────────
@dataclass(frozen=True)
class Segment:
    """Um locus indexado: o `ref` canônico (no formato que `cite.py` aceita),
    o texto-fonte normalizado (para cobertura) e o range de linhas no raw."""

    ref: str
    norm_text: str
    line_start: int
    line_end: int


def _fmt_ref(sigla: str, part: int | None, roman: str | None, n: int) -> str:
    """Ref canônico do índice, no formato que `cite.py` aceita — para que a
    comparação best vs. citado (em `cited_covers`) seja textual e exata."""
    if sigla == "LE":
        return f"q. {n}"
    if sigla == "LM":
        return f"item {n}"
    base = f"cap. {roman}, item {n}"
    if part:
        return f"{part}ª parte, {base}"
    return base


def _segments_from_range(
    sigla: str, lines: list[str], lo: int, hi: int,
    part: int | None, roman: str | None,
) -> list[Segment]:
    """Fatia [lo, hi) (0-based) em segmentos por marcador de item `_ITEM_RE`,
    cada bloco terminando no próximo item ou heading — mesma segmentação que o
    `_find_block` de `cite.py`, garantindo consistência com a extração forward.

    **Filtro monotônico**: só aceita um marcador cujo número SUPERE o último aceito.
    Sem isto, o scan capturava ordinais internos das respostas ("2.º que…", que o
    `_ITEM_RE` casa por desenho — ver cite.py) como itens espúrios: em LM o item
    223 gerava 27 segmentos falsos "item 2". A numeração canônica é estritamente
    crescente (LE 1..1019 global; LM 1..350 global; itens 1..N por capítulo em
    ESE/C&I/Gênese), então o monotônico mantém só o item real (1ª ocorrência) e
    descarta enumerações e sub-perguntas embutidas — espelhando o "primeiro match"
    do `extract_capitulo` de cite.py. `lo` reinicia a cada capítulo (chamada),
    logo a contagem por-capítulo recomeça naturalmente."""
    segs: list[Segment] = []
    last_n = 0
    for i in range(lo, min(hi, len(lines))):
        m = _ITEM_RE.match(lines[i])
        if not m:
            continue
        n = int(m.group(1))
        if n <= last_n:
            continue
        last_n = n
        end = _find_block(lines, i, [_ITEM_RE, _HEADING_RE])
        end = min(end, hi)
        text = "\n".join(lines[i:end])
        segs.append(Segment(_fmt_ref(sigla, part, roman, n), normalize(text), i + 1, end))
    return segs


def _iter_chapters(index_path):
    """Gera (part, roman, line_start, line_end) lendo o `.index.md`. `part` é
    None em obras sem partes (ESE, Gênese). Espelha `_find_chapter_range`."""
    cur_part: int | None = None
    for line in index_path.read_text(encoding="utf-8").splitlines():
        m_part = _INDEX_PART_RE.match(line)
        if m_part:
            cur_part = _PART_ORDINAL.get(m_part.group(1).lower())
            continue
        m = _INDEX_LINE_RE.search(line)
        if m:
            yield cur_part, m.group(1).upper(), int(m.group(2)), int(m.group(3))


@lru_cache(maxsize=8)
def build_index(sigla: str) -> tuple[Segment, ...]:
    """Constrói (e memoiza) todos os segmentos questão/item de uma obra.

    LE/LM: itens em numeração contínua varridos no arquivo inteiro. ESE/C&I/Gênese:
    itens varridos dentro do range de cada capítulo do `.index.md` (part-aware —
    em C&I o romano se repete entre 1ª e 2ª parte, e ambos viram segmentos
    distintos rotulados pela parte)."""
    slug = SIGLA_TO_SLUG[sigla]
    md_path = PENTATEUCO_DIR / f"{slug}.md"
    lines = _read_lines(md_path)

    if sigla in ("LE", "LM"):
        return tuple(_segments_from_range(sigla, lines, 0, len(lines), None, None))

    index_path = PENTATEUCO_DIR / f"{slug}.index.md"
    segs: list[Segment] = []
    for part, roman, ls, le in _iter_chapters(index_path):
        segs.extend(_segments_from_range(sigla, lines, ls - 1, le, part, roman))
    return tuple(segs)


# Aceita a forma "Gênese"/"GENESE" do KARDEC_RE (igual a cite._HELPER_SIGLA_NORM).
_SIGLA_NORM = {"GÊNESE": "Genese", "GENESE": "Genese"}


def _norm_sigla(sigla: str) -> str:
    return _SIGLA_NORM.get(sigla.upper(), sigla)


def find_loci(sigla: str, quote: str, top: int = 3) -> list[tuple[str, float, int]]:
    """Top-N loci por cobertura da `quote`. Retorna [(ref, cobertura, linha), …]
    em ordem decrescente. Lista vazia se a sigla não for do Pentateuco."""
    sigla = _norm_sigla(sigla)
    if sigla not in SIGLA_TO_SLUG:
        return []
    scored = [
        (seg.ref, word_coverage(quote, seg.norm_text), seg.line_start)
        for seg in build_index(sigla)
    ]
    scored.sort(key=lambda t: t[1], reverse=True)
    return scored[:top]


_RANGE_RE = re.compile(r"(\d+)\s*[–\-]\s*(\d+)")


def _parse_ref(ref: str) -> tuple[int | None, str | None, int | None]:
    """(parte, romano, item) de um ref do índice. parte/romano = None em LE/LM.
    item = o ÚLTIMO número do ref (q. N / item N / cap. R, item N)."""
    pm = _PART_NUM_RE.search(ref)
    cm = _CAP_RE.search(ref)
    nums = re.findall(r"\d+", ref)
    return (
        int(pm.group("n")) if pm else None,
        cm.group("r").upper() if cm else None,
        int(nums[-1]) if nums else None,
    )


def cited_covers(sigla: str, rest: str, best_ref: str) -> bool:
    """True se `best_ref` cai DENTRO do locus citado — cobre o caso de equivalência
    exata E de citação em range (`q. 161–162`, `cap. X, itens 6-9`), onde o melhor
    locus está legitimamente contido no range citado e não é mal-atribuição."""
    sigla = _norm_sigla(sigla)
    bpart, broman, bitem = _parse_ref(best_ref)
    if bitem is None:
        return False

    if sigla in ("LE", "LM"):
        rng = _RANGE_RE.search(rest)
        if rng:
            return int(rng.group(1)) <= bitem <= int(rng.group(2))
        m = _Q_RE.search(rest) or re.search(r"item\s+(\d+)", rest, re.IGNORECASE)
        if not m:
            return False
        n = int(m.group("n") if m.re is _Q_RE else m.group(1))
        return n == bitem

    cap_m = _CAP_RE.search(rest)
    if not cap_m or cap_m.group("r").upper() != broman:
        return False
    pm = _PART_NUM_RE.search(rest)
    if (int(pm.group("n")) if pm else None) != bpart:
        return False
    tail = rest[cap_m.end():]  # só o que vem DEPOIS do capítulo (itens)
    rng = _RANGE_RE.search(tail)
    if rng:
        return int(rng.group(1)) <= bitem <= int(rng.group(2))
    im = _CAP_ITEM_RE.search(rest)
    return bool(im) and int(im.group(1)) == bitem


# Thresholds de classificação (cobertura CONTÍGUA, _MIN_CONTIG_BLOCK=3).
# Calibrados nos candidatos do `check_literal_quote_exists` (ROADMAP §12 Fase 1).
# Três faixas, conservadoras — na dúvida, abster (uncertain → revisão humana):
#   best ≥ 0.85  → aspa verbatim achada noutro locus      → misattributed (sugere)
#   best < 0.45  → aspa não aparece contígua em lugar nenhum → fabricated
#   meio (0.45–0.85) → paráfrase/ancoragem frouxa          → uncertain (humano)
SUGGEST_MIN = 0.85   # cobertura mínima do best locus para afirmar "a aspa mora aqui"
MARGIN_MIN = 0.25    # best precisa superar o citado por esta folga p/ ser mal-atribuição
FABRICATED_MAX = 0.45  # se nem o best locus cobre isto, a aspa é candidata a fabricada


@dataclass(frozen=True)
class Verdict:
    # label ∈ supported | paraphrase | misattributed | fabricated | uncertain
    label: str
    suggested_ref: str | None
    suggested_coverage: float
    cited_coverage: float


def classify(sigla: str, cited_rest: str, quote: str, cited_coverage: float) -> Verdict:
    """Classifica uma aspa já sinalizada (cobertura baixa no locus citado).

    `cited_coverage` é a cobertura contígua da aspa no locus citado (computada
    pelo caller). Varre a obra pelo melhor locus e decide entre cinco rótulos:

    - **supported**: o melhor locus É o citado e cobre ~verbatim (≥ SUGGEST_MIN).
      A aspa está mesmo lá; o flag foi artefato de extração (capítulo irregular).
      Falso-positivo a suprimir.
    - **paraphrase**: o melhor locus é o citado, mas a cobertura é parcial — a
      aspa parafraseia o locus certo. Não é fabricação nem erro de locus; o
      conserto é de-quote (tirar as aspas) ou usar o texto verbatim.
    - **misattributed**: outro locus cobre ~verbatim (≥ SUGGEST_MIN) e supera o
      citado por MARGIN_MIN → o `ref` está errado; sugere o certo (auto-corrigível).
    - **fabricated**: nem o melhor locus cobre (< FABRICATED_MAX) → a frase não
      aparece contígua em lugar nenhum da obra.
    - **uncertain**: zona cinzenta → defere a humano (não auto-corrigir).
    """
    top = find_loci(sigla, quote, top=1)
    if not top:
        return Verdict("uncertain", None, 0.0, cited_coverage)
    best_ref, best_cov, _ = top[0]

    if cited_covers(sigla, cited_rest, best_ref):
        label = "supported" if best_cov >= SUGGEST_MIN else "paraphrase"
        return Verdict(label, best_ref, best_cov, cited_coverage)
    if best_cov < FABRICATED_MAX:
        return Verdict("fabricated", best_ref, best_cov, cited_coverage)
    if best_cov >= SUGGEST_MIN and (best_cov - cited_coverage) >= MARGIN_MIN:
        return Verdict("misattributed", best_ref, best_cov, cited_coverage)
    return Verdict("uncertain", best_ref, best_cov, cited_coverage)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Acha em que locus do Pentateuco uma aspa realmente mora.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("sigla", help="LE | LM | ESE | C&I | Gênese")
    parser.add_argument("quote", help="A frase a localizar (entre aspas no shell)")
    parser.add_argument("--top", type=int, default=3, help="Quantos loci listar (default 3)")
    args = parser.parse_args(argv)

    from cite import SIGLA_INPUT_NORM

    sigla = SIGLA_INPUT_NORM.get(args.sigla.upper(), args.sigla)
    if sigla not in SIGLA_TO_SLUG:
        print(f"erro: sigla desconhecida {args.sigla!r}", file=sys.stderr)
        return 2

    loci = find_loci(sigla, args.quote, top=args.top)
    if not loci:
        print("nenhum locus encontrado", file=sys.stderr)
        return 1
    for ref, cov, line in loci:
        print(f"{cov:.2f}  ({sigla}, {ref})  — linha {line}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
