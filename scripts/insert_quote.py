#!/usr/bin/env python3
"""Monta um blockquote de citação literal do Pentateuco a partir do locus — o
texto verbatim vem SEMPRE da fonte (via `cite.py`), nunca digitado de memória.

É o "fechar a torneira" do ROADMAP §12 Fase 2: o índice reverso (`reverse_locus`)
e o check (`check_quote_misattributed`) drenam/detectam o estoque de aspas
fabricadas; este script impede a reincidência — quem precisa citar Kardec literal
pede o locus e recebe o blockquote pronto, garantidamente verbatim.

Uso:
    uv run python scripts/insert_quote.py LE "q. 762"
    uv run python scripts/insert_quote.py ESE "cap. XVII, item 3" --sentence "consulta a sua consciência"
    uv run python scripts/insert_quote.py LE "q. 358" --italic
    uv run python scripts/insert_quote.py ESE "cap. XV, item 4" --path wiki/conceitos/caridade.md --after "## Ensino de Kardec"

Saída (stdout): o blockquote pronto para colar:
    > "<texto verbatim>" (SIGLA, ref)

`--sentence "<trecho>"` recorta só a(s) frase(s) da fonte que contêm o trecho
(o recorte continua vindo da fonte — não se digita nada). Sem match, ABORTA
(nunca fabrica). `--italic` envolve em `*...*` (estilo alternativo da casa).
`--path P --after "<âncora>"` insere o blockquote no arquivo logo após a 1ª linha
que contém a âncora (senão só imprime). Antes de emitir/inserir, o texto é
re-verificado contra a fonte (cobertura contígua ~1.0) — se não bater, aborta:
é a garantia de que o que sai é literal.

Cobertura: a mesma de `cite.py` (LE, LM, ESE, C&I, Gênese). Para loci que o
`cite.py` resolve em bloco grande (capítulo inteiro), prefira estreitar com item/
questão ou `--sentence` — um blockquote de capítulo inteiro raramente é o que se
quer (avisa na stderr se o corpo passar de ~600 chars).
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Reuso integral — não reescrever extração nem matemática de cobertura.
from cite import literal_text, SIGLA_INPUT_NORM, SIGLA_TO_SLUG
from reverse_locus import normalize as _normalize, word_coverage as _word_coverage

ROOT = Path(__file__).resolve().parent.parent

# Sigla canônica para exibição na citação (input "GENESE"/"Genese" → "Gênese").
_SIGLA_DISPLAY = {"LE": "LE", "LM": "LM", "ESE": "ESE", "C&I": "C&I", "Genese": "Gênese"}

# Marcadores estruturais no INÍCIO do corpo extraído — removidos para deixar só a
# prosa citável (o número do item/questão não faz parte da aspa). Espelham os
# marcadores que o `cite.py` reconhece; só atuam no começo do texto.
_LEAD_MARKERS = (
    re.compile(r"^AVISO:[^\n]*\n", re.IGNORECASE),       # aviso do cite.py (C&I 2ª parte)
    re.compile(r"^\s*>\s*"),                              # blockquote do raw (q. 566)
    re.compile(r"^\s*\*{0,2}\d+(?:\s*\[\d+\])?\.\*{0,2}\s*"),  # "713." / "**4.**" / "1019 [1018]."
    re.compile(r"^\s*\*+\s*[IVXLCDM]+\s*\*+\s*\n"),       # roman bold (Introdução/Conclusão)
    re.compile(r"^\s*[a-z]\)\s*[–—-]?\s*"),               # subitem "a) –"
)

_SENT_SPLIT_RE = re.compile(r"(?<=[.!?…])\s+(?=[A-ZÀ-Þ“\"—])")


def _clean_body(body: str) -> str:
    """Tira marcador estrutural inicial e markdown de heading; colapsa quebras de
    linha internas em espaço (a fonte quebra parágrafo entre linhas), preservando
    o texto palavra a palavra."""
    text = body
    # Remover headings markdown (## …) que o dump de capítulo possa carregar.
    text = re.sub(r"^#{1,6}\s+[^\n]*\n?", "", text, flags=re.MULTILINE)
    # Remover marcadores estruturais do começo (um passo de cada, em ordem).
    changed = True
    while changed:
        changed = False
        for pat in _LEAD_MARKERS:
            new = pat.sub("", text, count=1)
            if new != text:
                text, changed = new, True
    # Colapsar espaços/quebras.
    text = re.sub(r"\s*\n\s*", " ", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text.strip()


def _strip_edge_quotes(text: str) -> str:
    """Descasca aspas nas bordas do texto extraído.

    A fonte marca a resposta do Espírito com aspas curvas (“…”), e `build_quote`
    envolve o resultado em aspas retas — sem descascar, o blockquote sai com aspa
    dupla (`"“Sim, porquanto…"`). Só as bordas: aspa interna (Kardec citando
    terceiro) é parte do texto e fica. Não altera cobertura — `normalize` já
    descarta pontuação —, então a auto-verificação segue válida sobre o resultado.
    """
    return text.strip().strip("“”\"").strip()


def _select_sentence(text: str, needle: str) -> str | None:
    """Recorta a(s) frase(s) contíguas de `text` que contêm `needle` (match
    normalizado, robusto a acento/caixa/pontuação). Devolve None se não achar —
    o caller aborta (não se inventa recorte)."""
    sents = _SENT_SPLIT_RE.split(text)
    norm_needle = _normalize(needle)
    if not norm_needle:
        return None
    hits = [i for i, s in enumerate(sents) if norm_needle in _normalize(s)]
    if not hits:
        return None
    lo, hi = min(hits), max(hits)
    return " ".join(sents[lo:hi + 1]).strip()


def build_quote(sigla_in: str, ref: str, sentence: str | None, italic: bool) -> str:
    """Devolve o blockquote pronto, ou aborta (SystemExit) se o locus não resolve,
    o `--sentence` não casa, ou a auto-verificação de cobertura falha."""
    sigla = SIGLA_INPUT_NORM.get(sigla_in.upper(), sigla_in)
    if sigla not in SIGLA_TO_SLUG:
        raise SystemExit(
            f"erro: sigla desconhecida {sigla_in!r}. Use: {', '.join(sorted(SIGLA_TO_SLUG))}"
        )
    body = literal_text(sigla, ref)
    if body is None:
        raise SystemExit(
            f"erro: locus ({sigla}, {ref}) não resolvido por cite.py. Confira "
            f"raw/kardec/pentateuco/{SIGLA_TO_SLUG[sigla]}.index.md"
        )
    text = _clean_body(body)
    if sentence:
        sel = _select_sentence(text, sentence)
        if sel is None:
            raise SystemExit(
                f"erro: trecho {sentence!r} não encontrado em ({sigla}, {ref}). "
                "Não fabrico recorte — confira o trecho ou amplie o locus."
            )
        text = sel
    elif len(text) > 600:
        sys.stderr.write(
            f"aviso: corpo de ({sigla}, {ref}) tem {len(text)} chars — provável "
            "capítulo/questão longa. Estreite com item/--sentence se quer só um trecho.\n"
        )

    text = _strip_edge_quotes(text)

    # Auto-verificação: o texto emitido tem de ser verbatim da fonte (cobertura
    # contígua ~1.0). É a garantia anti-fabricação — se falhar, algo na limpeza
    # desalinhou e é melhor abortar que emitir aspa suspeita.
    cov = _word_coverage(text, body)
    if cov < 0.95:
        raise SystemExit(
            f"erro: auto-verificação falhou (cobertura {cov:.2f} < 0.95) para "
            f"({sigla}, {ref}). O texto limpo não bate verbatim com a fonte — não emito."
        )

    sigla_disp = _SIGLA_DISPLAY.get(sigla, sigla)
    quoted = f"*\"{text}\"*" if italic else f"\"{text}\""
    return f"> {quoted} ({sigla_disp}, {ref})"


def _insert_into(path: Path, anchor: str, block: str) -> bool:
    """Insere `block` (+ linha em branco) logo após a 1ª linha que contém `anchor`.
    Devolve True se inseriu; False se a âncora não foi encontrada."""
    lines = path.read_text(encoding="utf-8").splitlines()
    for i, ln in enumerate(lines):
        if anchor in ln:
            lines[i + 1:i + 1] = ["", block]
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            return True
    return False


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Monta blockquote de citação literal do Pentateuco (verbatim da fonte).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("sigla", help="LE | LM | ESE | C&I | Gênese")
    p.add_argument("ref", help='Ex.: "q. 762", "cap. XVII, item 3"')
    p.add_argument("--sentence", metavar="TRECHO",
                   help="Recorta só a(s) frase(s) da fonte que contêm TRECHO.")
    p.add_argument("--italic", action="store_true", help="Envolve em *itálico*.")
    p.add_argument("--path", metavar="PAGE", help="Inserir no arquivo (senão imprime).")
    p.add_argument("--after", metavar="ÂNCORA",
                   help="Inserir logo após a 1ª linha que contém ÂNCORA (com --path).")
    args = p.parse_args(argv)

    try:
        block = build_quote(args.sigla, args.ref, args.sentence, args.italic)
    except SystemExit as e:
        print(str(e), file=sys.stderr)
        return 2

    if args.path:
        if not args.after:
            print("erro: --path exige --after \"<âncora>\".", file=sys.stderr)
            return 2
        target = Path(args.path)
        if not target.exists():
            print(f"erro: arquivo não existe: {target}", file=sys.stderr)
            return 2
        if _insert_into(target, args.after, block):
            print(f"inserido em {args.path} após a linha com {args.after!r}:\n{block}")
            return 0
        print(f"erro: âncora {args.after!r} não encontrada em {args.path}.", file=sys.stderr)
        return 2

    print(block)
    return 0


if __name__ == "__main__":
    sys.exit(main())
