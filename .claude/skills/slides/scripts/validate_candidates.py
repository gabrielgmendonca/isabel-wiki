#!/usr/bin/env python3
"""Refutação mecânica dos candidatos a título e a pergunta socrática.

Roda no Passo 4 de `/slides`, **antes** do `AskUserQuestion`: a skill gera os
candidatos, este script reprova os que caem em antipadrão decidível por código,
e a skill regenera só os reprovados. O usuário vê apenas os sobreviventes.

Por que script e não prompt (CLAUDE.md §4, princípio das 3 camadas): "este
título é igual ao heading da wiki?", "esta pergunta tem quantas palavras?",
"ela recicla as palavras do section header?" são perguntas fechadas. Gastar
token de Opus derivando isso — e ainda por cima de forma não-reprodutível — é
desperdício. O que **não** é decidível aqui (rótulo vs. afirmação, se a pergunta
é intercambiável entre citações) fica na auto-refutação do SKILL.md.

Regras aplicadas: `.claude/rules/convencoes-titulos-slides.md` e
`.claude/rules/convencoes-perguntas-socraticas.md`.

## Limites conhecidos (medidos contra o corpus)

O heurístico de `rotulo_nominal` só alcança títulos **curtos** (≤6 palavras).
Nominalização abstrata mais longa **passa**:

    "A causa que escapa ao olhar terreno"        (7 palavras) → aprovado
    "A justiça das aflições e a fé que consola"  (9 palavras) → aprovado

Ambos são títulos ruins reais do deck `justica-aflicoes-fe-consola`, e ambos
foram **escritos assim**, não herdados — não há página wiki com esses headings,
então nem o teste de origem os pega. Detectar "isto é rótulo nominal ou
afirmação?" em 7+ palavras exige análise sintática que não cabe num regex.

É exatamente esse resíduo que a auto-refutação do `SKILL.md` cobre. Este script
não substitui esse passo: ele tira do caminho do Opus o que é fechado, para que
o julgamento semântico chegue com menos ruído. **Aprovado aqui não significa bom
— significa "sem defeito mecânico".**

Uso:
    uv run python .claude/skills/slides/scripts/validate_candidates.py \\
      --tipo titulo --wiki-page wiki/aprofundamentos/dor-rigidez.md \\
      --candidato "Ninguém é irrecuperável:afirmacao" \\
      --candidato "Bem-aventurados os misericordiosos:verbatim"

    uv run python .claude/skills/slides/scripts/validate_candidates.py \\
      --tipo pergunta --contexto-secao "A causa que escapa ao olhar terreno" \\
      --candidato "Se a causa é anterior, por que esquecemos?"

Saída: JSON com `aprovados`, `reprovados` e, por candidato, as falhas.
Exit 1 se algum candidato foi reprovado (para a skill saber que precisa regerar).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

# Orçamentos — espelham lint_wiki.py (check `slide_titulos`). Se divergirem, o
# lint no CI contradiz este script e a skill fica sem norte.
TITULO_MAX_PALAVRAS = 12
SECAO_MAX_PALAVRAS = 8
PERGUNTA_MAX_PALAVRAS = 15
PERGUNTA_MAX_DURO = 22

PADROES = ("verbatim", "cena-tese", "afirmacao")

# Marcadores de predicação: um título que não tem nenhum deles e é curto tende a
# ser rótulo nominal ("Expiação e arrependimento", "A tríade", "Dor: Rigidez").
# Heurística deliberadamente grosseira — vale só para reprovar, nunca aprovar,
# e `verbatim` fica isento (uma bem-aventurança é nominal e é o melhor título).
PREDICACAO = {
    "é", "são", "era", "eram", "foi", "foram", "será", "serão", "seja",
    "tem", "têm", "há", "não", "nunca", "jamais", "ainda", "já", "só",
    "quando", "porque", "porquanto", "como", "quem", "que", "onde", "quanto",
    "sem", "contra", "antes", "depois", "sempre",
}

# Antipadrão "teaser": as três ✗ da rule socrática abrem todas com "E ".
TEASER_RE = re.compile(r"^e\s+(se|a|o|as|os|quando|quem|que)\b", re.IGNORECASE)
# "Dor: Rigidez" — telegráfico de duas palavras ligadas por dois-pontos.
TELEGRAFICO_RE = re.compile(r"^\s*[\wÀ-ÿ]+\s*:\s*[\wÀ-ÿ]+\s*$")
# Coordenação nominal de conceitos: "Expiação e arrependimento".
COORDENACAO_RE = re.compile(r"^[^,;:?!\"“]+\s+e\s+[^,;:?!\"“]+$", re.IGNORECASE)
ABREV = (r"(?<!\bcap)(?<!\bitem)(?<!\bq)(?<!\bp)(?<!\bn)(?<!\bart)(?<!\bsr)"
         r"(?<!\bsra)(?<!\bséc)(?<!\bed)(?<!\bvol)")
FRASE_BREAK_RE = re.compile(ABREV + r"[.!?]\s+(?=[A-ZÀ-ÞÁÉÍÓÚÂÊÔÃÕÇ\"“'])")

STOPWORDS = {
    "a", "o", "as", "os", "um", "uma", "de", "do", "da", "dos", "das", "em",
    "no", "na", "nos", "nas", "ao", "à", "aos", "às", "e", "ou", "que", "se",
    "por", "para", "com", "sem", "sobre", "como", "mais", "menos", "seu",
    "sua", "seus", "suas", "este", "esta", "esse", "essa", "isso", "ele",
    "ela", "nosso", "nossa",
}


def norm(s: str) -> str:
    """Normaliza para comparação: sem markdown, aspas, caixa ou pontuação final."""
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", s)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"\*\*|\*|`|~~", "", s)
    for ch in "“”\"'":
        s = s.replace(ch, "")
    s = re.sub(r"[.:;,!?—–-]+$", "", s.strip())
    return " ".join(s.lower().split())


def content_words(s: str) -> set[str]:
    """Palavras de conteúdo, sem acento e sem stopword — para medir reciclagem."""
    base = unicodedata.normalize("NFKD", norm(s))
    base = "".join(c for c in base if not unicodedata.combining(c))
    return {w for w in re.findall(r"[a-z]{4,}", base) if w not in STOPWORDS}


def strip_frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return text
    end = text.find("\n---", 3)
    return text if end < 0 else text[end + 4:].lstrip("\n")


def wiki_headings(page: Path | None) -> tuple[str, set[str]]:
    """(H1 normalizado, conjunto de `##` normalizados) da página wiki de origem."""
    if page is None or not page.exists():
        return "", set()
    body = strip_frontmatter(page.read_text(encoding="utf-8"))
    m = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    h1 = norm(m.group(1)) if m else ""
    hs = {norm(h) for h in re.findall(r"^##\s+(.+)$", body, re.MULTILINE)}
    return h1, hs


def check_titulo(texto: str, padrao: str, h1: str, hs: set[str],
                 is_secao: bool) -> tuple[list[dict], list[dict]]:
    """→ (falhas bloqueantes, avisos não-bloqueantes)."""
    falhas: list[dict] = []
    avisos: list[dict] = []
    n = norm(texto)
    palavras = len(n.split())
    teto = SECAO_MAX_PALAVRAS if is_secao else TITULO_MAX_PALAVRAS

    if not n:
        return [{"regra": "vazio", "detalhe": "candidato vazio"}], []

    if h1 and n == h1:
        falhas.append({"regra": "titulo_herdado",
                       "detalhe": "idêntico ao H1 da página wiki (verbete de "
                                  "índice, não título de palestra)"})
    if n in hs:
        falhas.append({"regra": "secao_herdada",
                       "detalhe": "idêntico a um heading `##` da página wiki"})
    if palavras > teto:
        falhas.append({"regra": "longo",
                       "detalhe": f"{palavras} palavras (máx. {teto})"})
    if TELEGRAFICO_RE.match(texto):
        falhas.append({"regra": "telegrafico",
                       "detalhe": "forma 'X: Y' — rótulo de sumário"})
    if re.match(r"^\s*(parte\s+)?(\d+|[ivxlc]+)\s*[—–-]?\s*$", texto,
                re.IGNORECASE):
        falhas.append({"regra": "parte_sem_nome",
                       "detalhe": "numeração sem nome"})
    # Rótulo nominal: sem marcador de predicação e curto. `verbatim` é isento —
    # "Bem-aventurados os misericordiosos" é nominal e é o padrão preferido.
    if padrao != "verbatim" and palavras <= 6:
        if not (set(n.split()) & PREDICACAO):
            falhas.append({"regra": "rotulo_nominal",
                           "detalhe": "curto e sem predicação — parece rótulo "
                                      "de tópico, não afirmação nem cena"})
    if padrao != "verbatim" and COORDENACAO_RE.match(texto) and palavras <= 6:
        if not (set(n.split()) & PREDICACAO):
            falhas.append({"regra": "coordenacao_de_conceitos",
                           "detalhe": "forma '<conceito> e <conceito>' — "
                                      "assinatura de título de wiki"})
    return falhas, avisos


def check_pergunta(texto: str, contexto: str | None) -> tuple[list[dict], list[dict]]:
    """→ (falhas bloqueantes, avisos não-bloqueantes).

    O teto de 15 palavras é **aviso**, não bloqueio: o ✓ exemplar da própria
    rule socrática ("Como uma mãe que perdeu a filha de seis anos pode, ainda
    assim, agradecer a Deus?") tem 16. Bloquear em 16 seria o validador
    reprovando o padrão que ele existe para defender. Bloqueia em 22, o ponto
    onde a pergunta vira parágrafo a 64px — mesma divisão do lint.
    """
    falhas: list[dict] = []
    avisos: list[dict] = []
    n = norm(texto)
    palavras = len(n.split())

    if not texto.strip().endswith("?"):
        falhas.append({"regra": "nao_e_pergunta",
                       "detalhe": "não termina com '?'"})
    if palavras > PERGUNTA_MAX_DURO:
        falhas.append({"regra": "pergunta_longa",
                       "detalhe": f"{palavras} palavras a 64px "
                                  f"(máx. duro {PERGUNTA_MAX_DURO}) — âncora "
                                  f"deve ir para o subtítulo"})
    elif palavras > PERGUNTA_MAX_PALAVRAS:
        avisos.append({"regra": "pergunta_acima_do_orcamento",
                       "detalhe": f"{palavras} palavras (orçamento "
                                  f"{PERGUNTA_MAX_PALAVRAS}) — aceitável se a "
                                  f"âncora estiver na própria frase e for curta"})
    if FRASE_BREAK_RE.search(texto):
        falhas.append({"regra": "pergunta_duas_frases",
                       "detalhe": "setup + pergunta no mesmo h2 — o setup vai "
                                  "para o subtítulo de 24px"})
    if TEASER_RE.match(texto.strip()):
        falhas.append({"regra": "teaser",
                       "detalhe": "abre com 'E se/E a/E quando' — pergunta "
                                  "aditiva, antipadrão da rule socrática"})
    if contexto:
        recicla = content_words(texto) & content_words(contexto)
        base = content_words(contexto)
        if base and len(recicla) / len(base) >= 0.6:
            falhas.append({"regra": "reformulacao_do_section_header",
                           "detalhe": f"recicla {len(recicla)}/{len(base)} "
                                      f"palavras do section header "
                                      f"('{contexto[:40]}')"})
    return falhas, avisos


def parse_candidato(raw: str, tipo: str) -> tuple[str, str]:
    """'texto:padrao' → (texto, padrao). Padrão só se aplica a título."""
    if tipo == "pergunta":
        return raw, ""
    if ":" in raw:
        head, _, tail = raw.rpartition(":")
        if tail.strip() in PADROES and head.strip():
            return head.strip(), tail.strip()
    return raw, ""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tipo", required=True,
                    choices=["titulo", "secao", "pergunta"],
                    help="titulo = capa; secao = section header; pergunta = "
                         "pergunta-ponte/abertura")
    ap.add_argument("--wiki-page", type=Path, default=None,
                    help="Página wiki de origem (titulo/secao): habilita o "
                         "teste de origem contra o H1 e os `##`")
    ap.add_argument("--contexto-secao", default=None,
                    help="Section header que precede a pergunta: habilita o "
                         "teste de reformulação vazia")
    ap.add_argument("--candidato", action="append", required=True,
                    help="Repetir por candidato. Para titulo/secao, sufixar "
                         "com ':verbatim', ':cena-tese' ou ':afirmacao'")
    ap.add_argument("--exigir-padroes-distintos", action="store_true",
                    help="Reprova o lote se os candidatos repetirem padrão "
                         "(convencoes-titulos-slides.md pede 3 padrões)")
    args = ap.parse_args()

    h1, hs = wiki_headings(args.wiki_page)
    is_secao = args.tipo == "secao"

    resultados = []
    padroes_vistos: list[str] = []
    for raw in args.candidato:
        texto, padrao = parse_candidato(raw, args.tipo)
        if args.tipo == "pergunta":
            falhas, avisos = check_pergunta(texto, args.contexto_secao)
        else:
            falhas, avisos = check_titulo(texto, padrao, h1, hs, is_secao)
            if padrao:
                padroes_vistos.append(padrao)
            elif args.exigir_padroes_distintos:
                falhas.append({"regra": "padrao_nao_declarado",
                               "detalhe": "sufixar com ':verbatim', "
                                          "':cena-tese' ou ':afirmacao'"})
        resultados.append({
            "texto": texto,
            "padrao": padrao or None,
            "palavras": len(norm(texto).split()),
            "aprovado": not falhas,
            "falhas": falhas,
            "avisos": avisos,
        })

    lote_falhas = []
    if args.exigir_padroes_distintos and padroes_vistos:
        if len(set(padroes_vistos)) < len(padroes_vistos):
            lote_falhas.append({
                "regra": "padroes_repetidos",
                "detalhe": f"padrões usados: {padroes_vistos} — a rule pede um "
                           f"candidato por padrão distinto",
            })

    aprovados = [r for r in resultados if r["aprovado"]]
    reprovados = [r for r in resultados if not r["aprovado"]]
    print(json.dumps({
        "tipo": args.tipo,
        "total": len(resultados),
        "aprovados": len(aprovados),
        "reprovados": len(reprovados),
        "lote_falhas": lote_falhas,
        "candidatos": resultados,
        "acao": ("regerar os reprovados e rodar de novo"
                 if reprovados or lote_falhas
                 else "seguir para o AskUserQuestion"),
    }, ensure_ascii=False, indent=2))

    return 1 if (reprovados or lote_falhas) else 0


if __name__ == "__main__":
    sys.exit(main())
