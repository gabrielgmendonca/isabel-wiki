#!/usr/bin/env python3
"""Extrai o texto literal de uma passagem do Pentateuco a partir da citação canônica.

Uso:
    uv run python scripts/cite.py LE "q. 150"
    uv run python scripts/cite.py LE "q. 150b"            # só subitem b
    uv run python scripts/cite.py LE "Introdução, item IV"
    uv run python scripts/cite.py LE "Conclusão, IX"
    uv run python scripts/cite.py LM "item 230"
    uv run python scripts/cite.py ESE "cap. XVII, item 4"
    uv run python scripts/cite.py "C&I" "1ª parte, cap. VI"
    uv run python scripts/cite.py "Gênese" "cap. XI, item 13"

Saída (stdout): cabeçalho com locus + path:linhas + texto literal pronto pra
colar como citação. Em locus inválido, aborta com exit code 2 (motivo na
stderr) reusando `resolve_locus` de `kardec_structure`.

Cobertura: LE, LM, ESE, C&I (1ª e 2ª parte), Gênese. Em C&I e LM o algarismo
romano do capítulo se repete entre as partes (cap. I existe em ambas); por isso a
"parte" da citação desambigua — sem ela, devolve-se a 1ª parte (legado). A 2ª
parte de C&I (Exemplos) é resolvida no nível do capítulo, mas seus relatos são
nominais: a cobertura de `item N` é parcial e vem com aviso.

Além de questão/item/capítulo, também resolve: capítulo inteiro do LM sem item
(`LM "cap. XXIII"` → delega à maquinaria de capítulo); range de capítulos
(`Gênese "caps. XIII–XV"` → dump do span; só en-dash/hífen, não o em-dash de
glosa "cap. XXV — Mt 6:16"); Introdução marcada como `**INTRODUÇÃO**` inline
(Gênese, LM) além do heading `## Introdução`; e o Prolegômenos do LE.
Não resolve (e nem deveria): referência só ao nome da obra `(ESE)`, ano de
publicação `(LM, 1861)`, listas de capítulos `caps. I, VIII–XI`, e `(Gênese,
1:28)` — que é o livro bíblico do Gênesis, não a obra de Kardec.

ESE: o marcador de item alterna entre "N." e negrito "**N.**" no raw (às vezes
no mesmo capítulo) — ambos são reconhecidos. A Introdução é extraída inteira
(`ESE "Introdução"`); itens isolados da Introdução não, por causa do markup
irregular.

Marcadores de item robustos a ruído. O início-de-linha tolera blockquote (">566."
no LE) e asteriscos; o que vem DEPOIS do ponto decide se "N." é item ou ruído
(ver `_ITEM_RE`). Um marcador falso à frente do item verdadeiro SOMBREIA o item
(o extractor ancora nele) e TRUNCA o corpo do anterior — os quatro sombreamentos
observados no corpus: cauda de cross-ref ("219.)"), número decimal de tabela
("19.686", Gênese cap. X), enumeração ordinal com parêntese ("2.ª) Preces…", ESE
cap. XXVIII) e versículo bíblico transcrito ("6. Disse Deus também…", Gênese cap.
XII, onde Kardec cita o Gênesis e a quebra de linha expõe o nº do versículo).

Para ESE/C&I/Gênese, `_chapter_items` filtra esses falsos por continuação de
linha, política de ordinais e sequência; para LE/LM (numeração contínua),
`_ITEM_LEM_RE` rejeita ordinais de saída. O ordinal só é item legítimo em C&I 1ª
parte cap. VII, cujos 33 itens canônicos são "N.º — …".

`item_blocks(sigla, …)` é a fonte única dessa segmentação — `publish_pentateuco`
a consome para ancorar exatamente onde o `literal_text` resolve.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from functools import lru_cache
from pathlib import Path

# Reuso integral do parsing — não duplicar regex.
from kardec_structure import (
    OBRA_SIGLA,
    PENTATEUCO_DIR,
    MAPPING_PATH,
    _CAP_RE,
    _Q_RE,
    _INTRO_RE,
    _INTRO_IT_RE,
    _PART_NUM_RE,
    NEXT_SIGLA_RE,
    _roman_to_int,
    load_structures,
    resolve_locus,
)

SIGLA_TO_SLUG = {v: k for k, v in OBRA_SIGLA.items()}
ROOT = Path(__file__).resolve().parent.parent

# Normalização da sigla aceita pela CLI: "Genese" ↔ "Gênese".
SIGLA_INPUT_NORM = {
    "GENESE": "Genese",
    "GÊNESE": "Genese",
    "C&I": "C&I",
    "LE": "LE",
    "LM": "LM",
    "ESE": "ESE",
}

# Item dentro de capítulo / questão dentro do LE: linha começa com "N." (com
# ou sem texto depois — algumas edições quebram a linha após o número).
# As questões finais do LE (q. 1012–1019) vêm em numeração dupla
# "<nº Kardec> [<nº sequencial>]." (ex.: "1019 [1018].") porque Kardec saltou
# o nº 1011 (ver Nota dos Revisores no raw, após a q. 1012). Capturamos o
# PRIMEIRO número — o de Kardec, que é o usado nas citações canônicas.
# O markdown do ESE é inconsistente no marcador: a maioria dos itens vem como
# "N." simples, mas ~95 (capítulos X, XI, XIII–XVI, parte das Instruções dos
# Espíritos) vêm em negrito "**N.**" — e há casos avulsos de estrela única
# ("*N." / "N.*"). Toleramos 0–2 asteriscos antes e depois do número/ponto;
# sem isso, capítulos inteiros ficavam inacessíveis (item "não encontrado").
#
# Prefixo `>`: a q. 566 do LE vem dentro de um blockquote (">566. ..."); sem
# tolerar o marcador de citação a questão ficava inacessível. Só `>` + espaço
# opcional, não indentação arbitrária (evita casar linhas indentadas que não
# são itens).
#
# O que vem DEPOIS do ponto decide se "N." é marcador de item ou ruído. Três
# lookaheads negativos, cada um de um bug real de sombreamento (o falso marcador
# aparece ANTES do item verdadeiro e o extractor ancora nele):
#
# `(?!\d)` — "19.686" é NÚMERO DECIMAL, não item. O cap. X da Gênese traz uma
#   tabela de composição química ("Fibrina / 53.360 / 7.021 / 19.686 / 19.934");
#   a linha "19.686" sombreava o item 19 real ("19. Tomamos para termo de
#   comparação o calor…"), e `literal_text` devolvia a string "19.686".
#
# `(?![ºª]?\))` — ")" logo após o número (com ou sem ordinal) denuncia enumeração
#   ou cauda de cross-ref, nunca um item:
#     - "219.)" — cauda de "(N.º\n219.)" quebrada em duas linhas, que sombreava o
#       item 219 real do LM;
#     - "2.ª) Preces por aquele mesmo que ora;" — item de LISTA no preâmbulo do
#       ESE cap. XXVIII (Coletânea de preces), que sombreava o item 2 real
#       ("2. Prefácio. — Os Espíritos recomendaram…") e o 3.
#
# O ordinal SOZINHO ("1.º — A alma…") continua sendo item válido AQUI: em C&I 1ª
# parte cap. VII os itens canônicos do "Código penal da vida futura" SÃO ordinais,
# e rejeitá-los quebraria ~50 citações reais da wiki. É o `)` que os desqualifica,
# não o "º"/"ª". (No LE/LM, onde ordinal nunca é item, use `_ITEM_LEM_RE`.)
#
# O versículo bíblico transcrito ("6. Disse Deus também…") não dá para separar por
# regex — é o que `_chapter_items` resolve, olhando o contexto.
_ITEM_RE = re.compile(
    r"^(?:>\s*)?\*{0,2}(\d+)(?:\s*\[\d+\])?\.\*{0,2}(?!\d)(?![ºª]?\))\s*"
)

# Variante para LE e LM, que rejeita TAMBÉM o ordinal ("2.ª. Sempre se há dito…").
# O ordinal só é marcador de item legítimo em C&I 1ª parte cap. VII (obra de
# `extract_capitulo`); no LE e no LM ele é sempre enumeração DENTRO da resposta —
# e, lido como item, tanto criava um "item 2" falso lá pelo cap. XX do LM quanto
# TRUNCAVA o corpo do item que o continha (a limitação conhecida do LM item 35).
_ITEM_LEM_RE = re.compile(
    r"^(?:>\s*)?\*{0,2}(\d+)(?:\s*\[\d+\])?\.\*{0,2}(?![\dºª])(?!\))\s*"
)

# Subitem do LE: "a) –", tolera travessões variados ou ausência.
_SUBITEM_RE = re.compile(r"^([a-z])\)\s*[–—-]?")

# Marcador de Introdução / Conclusão do LE: "**I**", "****I****", "**IX**" etc.
_BOLD_ROMAN_RE = re.compile(r"^\*+\s*([IVXLCDM]+)\s*\*+\s*$")

# Heading qualquer (`## ` ou `### `): limite natural de um bloco.
_HEADING_RE = re.compile(r"^#{2,}\s+")

# Subref "q. 150b" — a letra do subitem vem GRUDADA no número (sem espaço) e
# seguida de fronteira de palavra. Sem isso, "q. 472 sobre alienação…" lia o "s"
# de "sobre" como subitem 's', não o achava e a citação inteira falhava.
_Q_SUBITEM_RE = re.compile(r"q\.\s*(\d+)([a-z])\b", re.IGNORECASE)

# "Conclusão, IX" / "Conclusão IX".
_CONCLUSAO_RE = re.compile(r"conclus[ãa]o[^a-z]*([IVX]+)", re.IGNORECASE)

# Item dentro de capítulo: "cap. X, item Y" / "cap. X item Y".
_CAP_ITEM_RE = re.compile(
    r"cap\.\s*[ivxlcdm]+[^,]*,?\s*item\s+(\d+)", re.IGNORECASE
)

# Para ESE/C&I/Gênese: extrair line_start/line_end de uma linha do .index.md.
# Casa "- **Capítulo XVII — ...** (linhas 2665–3049)".
_INDEX_LINE_RE = re.compile(
    r"-\s+\*\*Cap[íi]tulo\s+([IVXLCDM]+)[^\*]*\*\*\s*\(linhas\s+(\d+)[–\-](\d+)\)",
    re.IGNORECASE,
)

# Cabeçalho de parte no .index.md: "### Segunda parte — Exemplos". Só C&I tem
# partes entre as obras de extract_capitulo (ESE/Gênese não); por isso o
# algarismo romano de capítulo se repete (cap. I existe na 1ª E na 2ª parte) e o
# resolvedor precisa saber em qual parte está varrendo.
_INDEX_PART_RE = re.compile(
    r"^###\s+(Primeira|Segunda|Terceira|Quarta|Quinta)\s+parte",
    re.IGNORECASE,
)
_PART_ORDINAL = {
    "primeira": 1, "segunda": 2, "terceira": 3, "quarta": 4, "quinta": 5,
}

# Range de capítulos: "(Gênese, caps. XIII–XV)" ou "cap. VI–VIII". Tolera
# singular/plural ("cap."/"caps."). Separador: en-dash ou hífen — NÃO o em-dash
# `—`, reservado a glosas narrativas ("cap. XXV — Mt 6:16"). Os `\b` impedem que
# a inicial maiúscula de uma sigla bíblica ("Mt", "Lc") seja lida como romano.
_CAP_RANGE_RE = re.compile(
    r"caps?\.\s*([ivxlcdm]+)\b\s*[–\-]\s*([ivxlcdm]+)\b", re.IGNORECASE
)

# Seções avulsas (Introdução, Prolegômenos): marcadas por heading `## Introdução…`
# OU por negrito inline `**INTRODUÇÃO**` (Gênese e LM usam o inline; ESE/LE usam
# heading). Fim da seção = primeiro `## Capítulo`/`## Parte`/`## Nª parte`.
_INTRO_START_RE = re.compile(
    r"^(?:##\s+Introdu[çc][ãa]o|\*\*\s*INTRODU[ÇC][ÃA]O\s*\*\*)", re.IGNORECASE
)
_PROLEG_RE = re.compile(r"proleg[ôo]menos", re.IGNORECASE)
_PROLEG_START_RE = re.compile(r"^\*\*\s*PROLEG[ÔO]MENOS\s*\*\*", re.IGNORECASE)
_SECTION_END_RE = re.compile(
    r"^##\s+(?:Cap[íi]tulo|Parte\b|"
    r"(?:Primeira|Segunda|Terceira|Quarta|Quinta)\s+parte)",
    re.IGNORECASE,
)

# Nome bonito de parte (LE).
_PART_PRETTY = {1: "Parte primeira", 2: "Parte segunda", 3: "Parte terceira", 4: "Parte quarta"}


@lru_cache(maxsize=8)
def _read_lines_cached(path_str: str) -> tuple[str, ...]:
    """Leitura+split memoizados — obras do Pentateuco têm até ~12k linhas, e o
    check de lint chama os extractors uma vez por citação na página."""
    return tuple(Path(path_str).read_text(encoding="utf-8").splitlines())


def _read_lines(path: Path) -> list[str]:
    # Cópia fresca por chamada (os extractors só leem/fatiam, mas a cache guarda
    # uma tupla imutável — copiar isola de mutação acidental futura).
    return list(_read_lines_cached(str(path)))


def _rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def _le_pretty_locus(n: int) -> str:
    """'Parte segunda, Capítulo III' para `q. N`, via kardec-mapping.json."""
    data = json.loads(MAPPING_PATH.read_text(encoding="utf-8"))
    le = data.get("books", {}).get("LE", {})
    questions = le.get("questions", {})
    loc = questions.get(str(n))
    if not loc or ":" not in loc:
        return ""
    parte, cap = loc.split(":", 1)
    try:
        parte_pretty = _PART_PRETTY[int(parte)]
    except (ValueError, KeyError):
        return ""
    return f"{parte_pretty}, Capítulo {cap}"


def _find_block(lines: list[str], start_idx: int, terminators: list[re.Pattern]) -> int:
    """Acha o índice (0-based, exclusivo) onde o bloco que começa em `start_idx`
    termina. Termina ao encontrar uma linha que case qualquer dos terminators."""
    for i in range(start_idx + 1, len(lines)):
        for pat in terminators:
            if pat.match(lines[i]):
                return i
    return len(lines)


def _format(header: str, body: str) -> str:
    return f"{header}\n\n{body.rstrip()}\n"


# Linha que TERMINA em travessão: a seguinte é continuação do mesmo período, não
# um item novo. Kardec transcreve o Gênesis bíblico encadeando versículos com
# " — N. ", e a quebra de linha cai onde calha; quando calha logo após o
# travessão, o número do VERSÍCULO amanhece no início da linha e é indistinguível
# de um marcador de item (Gênese cap. XII: os "versículos" 2, 6, 9, 10, 13, 14,
# 15 e 20 sombreavam os itens homônimos de Kardec).
_CONT_RE = re.compile(r"[—–-]\s*$")

# Marcador com sufixo ordinal ("1.º", "2.ª"). Ver _chapter_items.
_ORDINAL_ITEM_RE = re.compile(r"^(?:>\s*)?\*{0,2}\d+(?:\s*\[\d+\])?\.\*{0,2}[ºª]")


def _chapter_items(lines: list[str], line_start: int, line_end: int) -> list[tuple[int, int]]:
    """[(índice 0-based, número)] dos marcadores REAIS de item do capítulo.

    `_ITEM_RE` sozinho é ingênuo: casa qualquer "N." no início de linha. Num
    corpus que transcreve a Bíblia, tabula números e enumera listas, isso produz
    marcadores FALSOS — e um falso à frente do item verdadeiro faz o extractor
    ancorar nele (sombreamento) e ainda TRUNCA o corpo do item anterior, porque
    `_find_block` para no primeiro marcador que encontra. Três filtros, cada um
    de um sombreamento observado:

    (a) **Continuação** — descarta marcador cuja linha anterior termina em
        travessão (`_CONT_RE`): é versículo bíblico no meio de uma transcrição
        que quebrou linha, não item.

    (b) **Política de ordinais** — se o capítulo tem QUALQUER marcador simples
        ("6."), os ordinais ("6.º") são ruído e caem. Só quando o capítulo não
        tem nenhum marcador simples é que os ordinais SÃO os itens — é o caso do
        "Código penal da vida futura" (C&I 1ª parte cap. VII), cujos 33 itens
        são todos "N.º — …". Sem isso, a tabela comparativa da Gênese cap. XII
        ("6.º DIA. — Os animais terrestres.") sombreava o item 6 de Kardec, que
        vem duas linhas depois.

    (c) **Sequencial** — os itens de um capítulo são 1, 2, 3, … n. Um marcador só
        é aceito se for o PRÓXIMO esperado; qualquer número fora de ordem é ruído
        (versículo, linha de tabela, sub-lista). Mata o resíduo que (a) e (b) não
        pegam — p.ex. o versículo "21." da transcrição do Gênesis III, que aparece
        antes do item 15 de Kardec e sombreava o item 21 real.

    Se os filtros não deixarem nada (capítulo de markup inesperado), devolve os
    candidatos crus — degradar para o comportamento antigo é melhor que perder o
    capítulo inteiro.
    """
    cands: list[tuple[int, int, bool]] = []
    for i in range(line_start - 1, min(line_end, len(lines))):
        m = _ITEM_RE.match(lines[i])
        if not m:
            continue
        if i > 0 and _CONT_RE.search(lines[i - 1]):
            continue  # (a)
        cands.append((i, int(m.group(1)), bool(_ORDINAL_ITEM_RE.match(lines[i]))))

    if any(not is_ord for _, _, is_ord in cands):  # (b)
        cands = [c for c in cands if not c[2]]

    seq: list[tuple[int, int]] = []  # (c)
    expected = 1
    for i, n, _ in cands:
        if n == expected:
            seq.append((i, n))
            expected += 1
    return seq or [(i, n) for i, n, _ in cands]


def chapter_item_blocks(
    lines: list[str], line_start: int, line_end: int
) -> list[tuple[int, int, int]]:
    """[(índice 0-based do marcador, número do item, índice 0-based do fim)].

    **Fonte única da segmentação de itens de capítulo.** `publish_pentateuco.py`
    consome esta função em vez de reimplementar a varredura — quando as duas
    tinham cópias próprias (`_ITEM_RE` cru de um lado, extractor do outro), elas
    divergiram: o publisher ancorava `## item 6` num versículo bíblico enquanto o
    `cite.py` já resolvia o item certo, e o round-trip derrubava a âncora.

    O bloco termina no próximo item REAL, no próximo heading, ou no fim do
    capítulo — o que vier primeiro.
    """
    itens = _chapter_items(lines, line_start, line_end)
    out: list[tuple[int, int, int]] = []
    for pos, (i, n) in enumerate(itens):
        proximo = itens[pos + 1][0] if pos + 1 < len(itens) else len(lines)
        end = min(_find_block(lines, i, [_HEADING_RE]), proximo, line_end)
        out.append((i, n, end))
    return out


# Obras cujos itens reiniciam em 1 a cada capítulo e são resolvidas por
# `extract_capitulo`. LE (questões) e LM (itens) têm numeração CONTÍNUA ao longo
# da obra e extractors próprios — a segmentação de capítulo não se aplica a eles.
_CAP_SIGLAS = frozenset({"ESE", "C&I", "Genese"})


def item_blocks(
    sigla: str, lines: list[str], line_start: int, line_end: int
) -> list[tuple[int, int, int]]:
    """[(índice do marcador, número, índice do fim)] no range, **espelhando o
    extractor que resolve `sigla`**.

    Quem publica âncoras (`publish_pentateuco`) tem de segmentar exatamente como
    quem resolve o locus (`literal_text`), senão o round-trip byte-a-byte falha e
    a âncora é descartada. Foi o que aconteceu ao aplicar a segmentação de
    capítulo ao LM: seus itens não reiniciam por capítulo, `extract_lm` varre com
    `_ITEM_RE` cru, e 29 âncoras legítimas evaporaram.
    """
    if sigla in _CAP_SIGLAS:
        return chapter_item_blocks(lines, line_start, line_end)
    out: list[tuple[int, int, int]] = []
    for i in range(line_start - 1, min(line_end, len(lines))):
        m = _ITEM_LEM_RE.match(lines[i])
        if not m:
            continue
        end = min(_find_block(lines, i, [_ITEM_LEM_RE, _HEADING_RE]), line_end)
        out.append((i, int(m.group(1)), end))
    return out


def extract_le(ref: str) -> tuple[str, str]:
    """LE: questão, subitem, intro_item, Introdução/Prolegômenos, ou conclusão."""
    md_path = PENTATEUCO_DIR / "livro-dos-espiritos.md"
    lines = _read_lines(md_path)

    # 0. Prolegômenos (declaração assinada dos Espíritos, ao fim da Introdução).
    # Bloco inteiro — markup interno irregular, itens não extraídos isoladamente.
    if _PROLEG_RE.search(ref):
        return _extract_named_section("LE", md_path, _PROLEG_START_RE, "Prolegômenos")

    # 1. Introdução, item X
    m_intro = _INTRO_IT_RE.search(ref)
    if m_intro:
        item = m_intro.group("r").upper()
        intro_start = next(
            (i for i, ln in enumerate(lines) if ln.startswith("## Introdução")), None
        )
        intro_end = next(
            (i for i, ln in enumerate(lines) if i > (intro_start or 0) and ln.startswith("## Parte ")),
            len(lines),
        )
        if intro_start is None:
            return _err_unexpected(ref)
        for i in range(intro_start + 1, intro_end):
            m = _BOLD_ROMAN_RE.match(lines[i])
            if m and m.group(1).upper() == item:
                end = _find_block(lines, i, [_BOLD_ROMAN_RE, _HEADING_RE])
                end = min(end, intro_end)
                header = f"(LE, Introdução, item {item}) — linhas {i + 1}-{end}\n{_rel(md_path)}:{i + 1}-{end}"
                body = "\n".join(lines[i:end])
                return header, body
        return _err_unexpected(ref)

    # 1b. Introdução inteira (sem item).
    if _INTRO_RE.search(ref):
        return _extract_named_section("LE", md_path, _INTRO_START_RE, "Introdução")

    # 2. Conclusão, X
    m_conc = _CONCLUSAO_RE.search(ref)
    if m_conc:
        roman = m_conc.group(1).upper()
        # Conclusão fica depois do último "## Parte quarta" → no fim do arquivo.
        # No LE não há heading "## Conclusão" — os romanos **I**…**IX** aparecem
        # diretamente como linhas isoladas. Procurar a partir do último ~10% do arquivo.
        scan_start = int(len(lines) * 0.85)
        for i in range(scan_start, len(lines)):
            m = _BOLD_ROMAN_RE.match(lines[i])
            if m and m.group(1).upper() == roman:
                end = _find_block(lines, i, [_BOLD_ROMAN_RE, _HEADING_RE])
                header = f"(LE, Conclusão, {roman}) — linhas {i + 1}-{end}\n{_rel(md_path)}:{i + 1}-{end}"
                body = "\n".join(lines[i:end])
                return header, body
        return _err_unexpected(ref)

    # 3. q. N ou q. Nx
    m_qsub = _Q_SUBITEM_RE.search(ref)
    if m_qsub:
        n = int(m_qsub.group(1))
        subitem = m_qsub.group(2).lower()
    else:
        m_q = _Q_RE.search(ref)
        if not m_q:
            return _err_unexpected(ref)
        n = int(m_q.group("n"))
        subitem = None

    for i, ln in enumerate(lines):
        m = _ITEM_LEM_RE.match(ln)
        if m and int(m.group(1)) == n:
            end = _find_block(lines, i, [_ITEM_LEM_RE, _HEADING_RE])
            if subitem is None:
                pretty = _le_pretty_locus(n)
                loc_str = f"{pretty} — " if pretty else ""
                header = f"(LE, q. {n}) — {loc_str}linhas {i + 1}-{end}\n{_rel(md_path)}:{i + 1}-{end}"
                body = "\n".join(lines[i:end])
                return header, body
            # Subitem dentro do bloco.
            for j in range(i + 1, end):
                m_sub = _SUBITEM_RE.match(lines[j])
                if m_sub and m_sub.group(1).lower() == subitem:
                    sub_end = _find_block(lines, j, [_SUBITEM_RE, _ITEM_LEM_RE, _HEADING_RE])
                    sub_end = min(sub_end, end)
                    pretty = _le_pretty_locus(n)
                    loc_str = f"{pretty} — " if pretty else ""
                    header = f"(LE, q. {n}{subitem}) — {loc_str}linhas {j + 1}-{sub_end}\n{_rel(md_path)}:{j + 1}-{sub_end}"
                    body = "\n".join(lines[j:sub_end])
                    return header, body
            return _err(f"subitem {subitem}) não encontrado em q. {n} (linhas {i + 1}-{end})")

    if n == 1011:
        return _err(
            "q. 1011 não existe no LE: Kardec saltou esse número na numeração "
            "(Nota dos Revisores, após a q. 1012). A sequência vai q. 1010 → q. 1012; "
            "as questões finais usam numeração dupla 'Kardec [sequencial]' até q. 1019."
        )
    return _err(f"q. {n} não encontrada em {_rel(md_path)}")


def extract_lm(ref: str) -> tuple[str, str]:
    """LM: item N (numeração contínua 1–350). Citação sem item (capítulo inteiro,
    range, Introdução) delega para a maquinaria estrutural de extract_capitulo —
    o LM tem `.index.md` com partes e capítulos como ESE/C&I/Gênese."""
    md_path = PENTATEUCO_DIR / "livro-dos-mediuns.md"
    lines = _read_lines(md_path)

    m_q = _Q_RE.search(ref)
    m_item = re.search(r"item\s+(\d+)", ref, re.IGNORECASE)
    n = None
    if m_q:
        n = int(m_q.group("n"))
    elif m_item:
        n = int(m_item.group(1))
    if n is None:
        # Sem item/questão: Introdução, capítulo inteiro ou range de capítulos.
        # extract_capitulo é part-aware (o LM tem dois "Capítulo I", um por parte).
        if _INTRO_RE.search(ref) or _CAP_RANGE_RE.search(ref) or _CAP_RE.search(ref):
            return extract_capitulo("LM", ref)
        return _err_unexpected(ref)

    for i, ln in enumerate(lines):
        m = _ITEM_LEM_RE.match(ln)
        if m and int(m.group(1)) == n:
            end = _find_block(lines, i, [_ITEM_LEM_RE, _HEADING_RE])
            header = f"(LM, item {n}) — linhas {i + 1}-{end}\n{_rel(md_path)}:{i + 1}-{end}"
            body = "\n".join(lines[i:end])
            return header, body
    return _err(f"item {n} não encontrado em {_rel(md_path)}")


def _find_chapter_range(
    index_path: Path, cap_roman: str, part: int | None = None
) -> tuple[int, int, int | None] | None:
    """Lê o .index.md e devolve (line_start, line_end, parte) do capítulo.

    `part` (1, 2, …) restringe a busca a uma parte da obra — indispensável em
    C&I, onde o algarismo romano se repete entre 1ª e 2ª parte (cap. I existe em
    ambas). Sem `part`, devolve o PRIMEIRO capítulo com aquele romano (legado;
    correto para ESE/Gênese, sem partes). Com `part`, só casa sob a parte pedida
    e devolve `None` se não houver — melhor errar explícito que devolver a parte
    errada silenciosamente. O 3º elemento é a parte em que o capítulo foi achado
    (ou `None` quando a obra não tem partes), usado para o aviso de C&I 2ª parte.
    """
    cur_part: int | None = None
    for line in index_path.read_text(encoding="utf-8").splitlines():
        m_part = _INDEX_PART_RE.match(line)
        if m_part:
            cur_part = _PART_ORDINAL.get(m_part.group(1).lower())
            continue
        m = _INDEX_LINE_RE.search(line)
        if m and m.group(1).upper() == cap_roman.upper():
            if part is not None and cur_part != part:
                continue
            return int(m.group(2)), int(m.group(3)), cur_part
    return None


def _extract_named_section(
    sigla: str, md_path: Path, start_re: re.Pattern, label: str
) -> tuple[str, str]:
    """Dump de uma seção avulsa (Introdução, Prolegômenos), do marcador de início
    (`start_re`) até o 1º `## Capítulo`/`## Parte`.

    Itens internos NÃO são extraídos isoladamente: o markup mistura negrito inline
    (`**II —`), heading (`## III —`) e numeração arábica divergente nas citações;
    para uma ferramenta de verificação, devolver o bloco inteiro (ou erro) é
    preferível a arriscar o trecho errado."""
    lines = _read_lines(md_path)
    start = next((i for i, ln in enumerate(lines) if start_re.match(ln)), None)
    if start is None:
        return _err(f"{label} não localizada em {_rel(md_path)}")
    end = next(
        (i for i in range(start + 1, len(lines)) if _SECTION_END_RE.match(lines[i])),
        len(lines),
    )
    header = (
        f"({sigla}, {label}) — linhas {start + 1}-{end}\n"
        f"{_rel(md_path)}:{start + 1}-{end}"
    )
    body = "\n".join(lines[start:end])
    return header, body


def _extract_intro(sigla: str, md_path: Path) -> tuple[str, str]:
    """Introdução inteira — heading `## Introdução` ou negrito `**INTRODUÇÃO**`."""
    return _extract_named_section(sigla, md_path, _INTRO_START_RE, "Introdução")


def _extract_cap_range(
    sigla: str, md_path: Path, index_path: Path,
    m_range: re.Match, req_part: int | None,
) -> tuple[str, str]:
    """Range de capítulos `(sigla, caps. A–B)`: dump do início de A ao fim de B."""
    a, b = m_range.group(1).upper(), m_range.group(2).upper()
    rng_a = _find_chapter_range(index_path, a, req_part)
    rng_b = _find_chapter_range(index_path, b, req_part)
    if rng_a is None or rng_b is None:
        falta = a if rng_a is None else b
        pl = f"{req_part}ª parte, " if req_part else ""
        return _err(
            f"{pl}cap. {falta} (do range {a}–{b}) não localizado em {_rel(index_path)}"
        )
    line_start, line_end, part = rng_a[0], rng_b[1], rng_a[2]
    if line_end < line_start:  # B antes de A no arquivo — normaliza pelo span real
        line_start = min(rng_a[0], rng_b[0])
        line_end = max(rng_a[1], rng_b[1])
    part_lbl = f"{part}ª parte, " if part else ""
    lines = _read_lines(md_path)
    header = (
        f"({sigla}, {part_lbl}caps. {a}–{b}) — linhas {line_start}-{line_end}\n"
        f"{_rel(md_path)}:{line_start}-{line_end}"
    )
    body = "\n".join(lines[line_start - 1:line_end])
    return header, body


def extract_capitulo(sigla: str, ref: str) -> tuple[str, str]:
    """ESE / C&I / Gênese: cap. X (com ou sem item Y), ou Introdução inteira."""
    # Citação multi-obra ("(ESE, cap. III; C&I, 1ª parte, cap. III)"): o `ref`
    # carrega a obra seguinte. Cortar no próximo sigla impede que o `_PART_NUM_RE`
    # capture a "parte" da OUTRA obra (espelha resolve_locus). Sem isto, a 1ª
    # parte da C&I era aplicada à ESE — que não tem partes — e a citação falhava.
    cut = NEXT_SIGLA_RE.search(ref)
    if cut:
        ref = ref[:cut.start()]

    slug = SIGLA_TO_SLUG[sigla]
    md_path = PENTATEUCO_DIR / f"{slug}.md"
    index_path = PENTATEUCO_DIR / f"{slug}.index.md"

    m_part = _PART_NUM_RE.search(ref)
    req_part = int(m_part.group("n")) if m_part else None

    # Range de capítulos: (sigla, caps. III–V) — antes do capítulo singular,
    # porque "caps." não casa o _CAP_RE (que exige "cap.").
    m_range = _CAP_RANGE_RE.search(ref)
    if m_range:
        return _extract_cap_range(sigla, md_path, index_path, m_range, req_part)

    m_cap = _CAP_RE.search(ref)
    if not m_cap:
        # Sem capítulo: só a Introdução inteira é extraível. Item da Introdução
        # tem markup irregular (ver _extract_intro) — erro explícito, não dump
        # do item errado.
        if _INTRO_IT_RE.search(ref):
            return _err(
                f"itens da Introdução não são extraídos ({sigla}); o markup é "
                "irregular. Use a Introdução inteira (sem 'item N') e localize o "
                "trecho manualmente."
            )
        if _INTRO_RE.search(ref):
            return _extract_intro(sigla, md_path)
        return _err_unexpected(ref)
    cap_roman = m_cap.group("r").upper()

    rng = _find_chapter_range(index_path, cap_roman, req_part)
    if rng is None:
        loc = f"{req_part}ª parte, cap. {cap_roman}" if req_part else f"cap. {cap_roman}"
        return _err(f"{loc} não localizado em {_rel(index_path)}")
    line_start, line_end, part = rng
    part_lbl = f"{part}ª parte, " if part else ""
    lines = _read_lines(md_path)

    m_item = _CAP_ITEM_RE.search(ref)
    if m_item:
        target = int(m_item.group(1))
        # Marcadores REAIS do capítulo (filtra versículo bíblico, linha de tabela,
        # ordinal de enumeração — ver _chapter_items). O fim do bloco é o próximo
        # marcador REAL ou o próximo heading: usar _ITEM_RE cru como terminador
        # truncava o corpo no primeiro marcador falso.
        for i, n, end in chapter_item_blocks(lines, line_start, line_end):
            if n == target:
                end_idx = end
                # Aviso especial para C&I 2ª parte (relatos nominais).
                warn = ""
                if sigla == "C&I" and part == 2:
                    warn = (
                        "AVISO: C&I 2ª parte usa relatos nominais; cobertura "
                        "limitada de itens numerados.\n"
                    )
                header = (
                    f"({sigla}, {part_lbl}cap. {cap_roman}, item {target}) — "
                    f"linhas {i + 1}-{end_idx}\n{_rel(md_path)}:{i + 1}-{end_idx}"
                )
                body = warn + "\n".join(lines[i:end_idx])
                return header, body
        return _err(
            f"item {target} não encontrado em {part_lbl}cap. {cap_roman} "
            f"(linhas {line_start}-{line_end})"
        )

    # Sem item: dump do capítulo inteiro.
    if sigla == "C&I" and part == 2:
        sys.stderr.write(
            "aviso: C&I 2ª parte (Exemplos) — relatos nominais sem numeração.\n"
        )
    header = (
        f"({sigla}, {part_lbl}cap. {cap_roman}) — linhas {line_start}-{line_end}\n"
        f"{_rel(md_path)}:{line_start}-{line_end}"
    )
    body = "\n".join(lines[line_start - 1:line_end])
    return header, body


# Siglas aceitas pelo helper programático — formas que o KARDEC_RE do
# link_citations captura ("Gênese"/"Genese"). C&I/LE/LM/ESE passam direto.
_HELPER_SIGLA_NORM = {"GÊNESE": "Genese", "GENESE": "Genese"}


def literal_text(sigla: str, ref: str) -> str | None:
    """Texto literal de `(sigla, ref)` do Pentateuco, ou `None` se o locus não
    resolver. Reuso programático dos extractors da CLI — sem print nem sys.exit.

    Consumido por `check_literal_quote_exists` (lint) para validar a existência de
    uma aspa literal de Kardec. `None` significa "locus inválido/não encontrado" —
    o caller deve pular (o erro de locus já é coberto por check_citation_resolves)."""
    sigla = _HELPER_SIGLA_NORM.get(sigla.upper(), sigla)
    if sigla not in SIGLA_TO_SLUG:
        return None
    try:
        if sigla == "LE":
            _, body = extract_le(ref)
        elif sigla == "LM":
            _, body = extract_lm(ref)
        else:
            _, body = extract_capitulo(sigla, ref)
    except SystemExit:
        return None
    return body


def _err(msg: str) -> tuple[str, str]:
    raise SystemExit(f"erro: {msg}")


def _err_unexpected(ref: str) -> tuple[str, str]:
    raise SystemExit(f"erro: referência não reconhecida: {ref!r}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Extrai texto literal de uma passagem do Pentateuco.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("sigla", help="LE | LM | ESE | C&I | Gênese")
    parser.add_argument("ref", help='Ex.: "q. 150", "cap. XVII, item 4", "1ª parte, cap. VI"')
    args = parser.parse_args(argv)

    sigla = SIGLA_INPUT_NORM.get(args.sigla.upper(), args.sigla)
    if sigla not in SIGLA_TO_SLUG:
        print(
            f"erro: sigla desconhecida {args.sigla!r}. Use uma de: "
            f"{', '.join(sorted(SIGLA_TO_SLUG))}",
            file=sys.stderr,
        )
        return 2

    # Validação semântica: o locus existe na obra?
    structures = load_structures()
    ok, motivo = resolve_locus(sigla, args.ref, structures[sigla])
    if not ok:
        print(
            f"erro: locus inválido em ({sigla}, {args.ref}): {motivo}. "
            f"cf. raw/kardec/pentateuco/{SIGLA_TO_SLUG[sigla]}.index.md",
            file=sys.stderr,
        )
        return 2

    try:
        if sigla == "LE":
            header, body = extract_le(args.ref)
        elif sigla == "LM":
            header, body = extract_lm(args.ref)
        else:
            header, body = extract_capitulo(sigla, args.ref)
    except SystemExit as e:
        print(str(e), file=sys.stderr)
        return 2

    sys.stdout.write(_format(header, body))
    return 0


if __name__ == "__main__":
    sys.exit(main())
