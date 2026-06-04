"""Verdade estrutural do Pentateuco — base do check_citation_resolves leve.

Para cada obra do Pentateuco, expõe um conjunto fechado de capítulos / partes /
intro_items que existem na fonte. Bate-se contra esse conjunto a referência
extraída de cada citação `(sigla, ref)` em páginas de `wiki/` — emite-se item
de lint quando o locus referenciado não existe na estrutura da obra.

Fontes de verdade, em ordem de preferência:

1. `raw/kardec/pentateuco/<obra>.index.md` (gerado por
   `scripts/generate_obra_index.py`) — cobre LM, ESE, Gênese, C&I.
2. `data/kardec-mapping.json` (mapping da Kardecpedia) — cobre LE (cujo
   markdown não traz heading das 4 partes "Livro Primeiro/Segundo/…") e
   complementa intro_items quando o index não os captura.

A camada é **leve** por desenho: prova só que **o locus (capítulo, parte,
questão, intro_item) existe na obra**. Verificação de que "o trecho cita o que
afirma" depende da granularidade questão/item em `raw/` (§4 do ROADMAP) e fica
para a versão estrita.
"""
from __future__ import annotations

import functools
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PENTATEUCO_DIR = ROOT / "raw" / "kardec" / "pentateuco"
MAPPING_PATH = ROOT / "data" / "kardec-mapping.json"

# Regexes reusados de link_citations.py — repetidos aqui para evitar
# dependência circular (resolve_locus consumido por lint_wiki).
_CAP_RE = re.compile(r"cap\.\s*(?P<r>[ivxlcdm]+)\b", re.IGNORECASE)
_Q_RE = re.compile(r"q\.\s*(?P<n>\d+)")
_INTRO_RE = re.compile(r"introdu[çc][ãa]o", re.IGNORECASE)
_INTRO_IT_RE = re.compile(
    r"introdu[çc][ãa]o[^,]*,\s*item\s+(?P<r>[ivxlcdm]+)", re.IGNORECASE
)
_PART_NUM_RE = re.compile(r"(?P<n>[1-5])\s*[ªa°]?\s*parte", re.IGNORECASE)

# Em `(LE, q. 200; ESE, cap. XVII)` o `rest` capturado pelo regex externo
# inclui "...; ESE, cap. XVII" — sem corte, CAP_RE encontraria XVII e o check
# falsamente acusaria LE. Truncar no primeiro `[,;]\s*<outra-sigla>` deixa o
# rest mono-sigla. Aceita:
# - prefixo opcional `cf.` em pontes editoriais ("…; cf. C&I 1ª parte cap. III sobre…")
# - sigla embrulhada em wikilink-com-alias ("…; [[wiki/obras/ceu-e-inferno|C&I]] 1ª parte cap. IX")
NEXT_SIGLA_RE = re.compile(
    r"[,;]\s*(?:\[\[[^\]|]+\|)?(?:cf\.?\s+)?(LE|LM|ESE|C&I|G[êe]nese)\b"
)

SIGLA_NORM = {"Gênese": "Genese"}

# Range máximo de questão/item — fixado pelo cânon, não pelo raw.
# LE: a numeração de Kardec vai até 1019, mas ele SALTOU o nº 1011 (lapso
# mantido nas 14 edições; ver "Nota dos Revisores" no raw após a q. 1012).
# Logo há 1018 questões reais, numeradas 1..1010 e 1012..1019. As finais
# (q. 1012–1019) vêm no raw em numeração dupla "<Kardec> [<sequencial>]."
# (ex.: "1019 [1018].") — por isso `grep ^[0-9]+\.` parava em 1010; o
# _ITEM_RE de cite.py reconhece esse formato e indexa pelo nº de Kardec.
# A "Conclusão" (romanos I–IX) é prosa SEPARATE, depois da q. 1019.
# Mantemos 1019 como teto; q. 1011 é inexistente por design.
# LM: items numerados continuamente até 350 entre as duas partes.
LE_MAX_QUESTAO = 1019
LM_MAX_ITEM = 350

# Obras que possuem Introdução (heading explícito OU bloco `**INTRODUÇÃO**`
# inline, ambos editoriais válidos). C&I tem Prefácio mas não Introdução
# kardequiana — `(C&I, Introdução)` é citação inválida na fonte.
_OBRAS_COM_INTRODUCAO = {"LE", "LM", "ESE", "Genese"}

# Slugs canônicos das obras → sigla de citação.
OBRA_SIGLA = {
    "livro-dos-espiritos": "LE",
    "livro-dos-mediuns": "LM",
    "evangelho-segundo-o-espiritismo": "ESE",
    "ceu-e-inferno": "C&I",
    "genese": "Genese",
}

# Capítulos por parte no .index.md:
#   "### Primeira parte — Doutrina"
#   "- **Capítulo I — …**" (logo abaixo)
INDEX_PART_RE = re.compile(
    r"^###\s+(?P<title>"
    r"(?:Primeira|Segunda|Terceira|Quarta|Quinta|Sexta|Sétima|Oitava|Nona|Décima)"
    r"\s+parte"
    # LE inverte a ordem ("Parte primeira"); sincronizar com PART_RE em
    # scripts/generate_obra_index.py.
    r"|Parte\s+(?P<ordinal>primeira|segunda|terceira|quarta|quinta|sexta|sétima|oitava|nona|décima)"
    r"|Parte\s+(?P<roman>[IVXLCDM]+)"
    r"|Introdução"
    r")\b",
    re.IGNORECASE,
)
INDEX_CHAPTER_RE = re.compile(
    r"^-\s+\*\*(?:Capítulo|Cap\.)\s+(?P<roman>[IVXLCDM]+)\b",
    re.IGNORECASE,
)

PART_ORDINAL = {
    "primeira": 1, "segunda": 2, "terceira": 3, "quarta": 4,
    "quinta": 5, "sexta": 6, "sétima": 7, "oitava": 8,
    "nona": 9, "décima": 10,
}


@dataclass
class Structure:
    """Estrutura de uma obra do Pentateuco, ground truth para o check leve.

    `chapters` armazena chaves no formato `"N:R"` quando a obra tem partes
    (LE, LM, C&I), ou só `"R"` quando não (ESE, Gênese), onde N é o número
    da parte e R é o algarismo romano do capítulo (maiúsculo). Isso espelha
    o esquema usado em `data/kardec-mapping.json`.

    `questoes` é um intervalo `(min, max)` inclusivo — não um set — para
    tolerar gaps de numeração que existem em LE (Kardecpedia mapeia 996 de
    1010 sem que os 14 ausentes representem typos). Vazio quando não aplica.
    """

    chapters: set[str] = field(default_factory=set)
    parts: set[int] = field(default_factory=set)
    intro_items: set[str] = field(default_factory=set)
    has_intro: bool = False
    questoes_range: tuple[int, int] | None = None  # LE
    items_range: tuple[int, int] | None = None     # LM


def _parse_index(index_path: Path) -> Structure:
    """Lê um `<obra>.index.md` e devolve a estrutura derivada.

    Acompanha a parte "corrente" enquanto varre as linhas: quando encontra
    `### <parte>` muda o contexto; quando encontra `- **Capítulo R …**`
    grava `f"{N}:{R}"` (ou só `R` se ainda não houver parte).
    """
    s = Structure()
    current_part: int | None = None

    for line in index_path.read_text(encoding="utf-8").splitlines():
        m_part = INDEX_PART_RE.match(line)
        if m_part:
            title = m_part.group("title").strip().lower()
            if title.startswith("introdução") or title == "introducao":
                s.has_intro = True
                current_part = None
                continue
            roman = m_part.group("roman")
            ordinal = m_part.group("ordinal")
            if roman:
                n = _roman_to_int(roman.upper())
            elif ordinal:
                n = PART_ORDINAL.get(ordinal.lower())
            else:
                first_word = title.split()[0]
                n = PART_ORDINAL.get(first_word)
            if n is not None:
                current_part = n
                s.parts.add(n)
            continue

        m_chap = INDEX_CHAPTER_RE.match(line)
        if m_chap:
            roman = m_chap.group("roman").upper()
            key = f"{current_part}:{roman}" if current_part else roman
            s.chapters.add(key)

    return s


_ROMAN = [
    ("M", 1000), ("CM", 900), ("D", 500), ("CD", 400),
    ("C", 100), ("XC", 90), ("L", 50), ("XL", 40),
    ("X", 10), ("IX", 9), ("V", 5), ("IV", 4), ("I", 1),
]


def _roman_to_int(s: str) -> int | None:
    """Converte algarismo romano (maiúsculo) em inteiro. None se inválido."""
    n, i = 0, 0
    for sym, val in _ROMAN:
        while s[i:i + len(sym)] == sym:
            n += val
            i += len(sym)
            if i >= len(s):
                return n
    return n if i == len(s) else None


def _augment_le_from_mapping(s: Structure, mapping_path: Path) -> Structure:
    """LE não tem heading de parte no markdown — completa pelo mapping da
    Kardecpedia (que tem 17 intro_items, 29 capítulos `parte:cap` em 4 partes).
    """
    data = json.loads(mapping_path.read_text(encoding="utf-8"))
    le = data.get("books", {}).get("LE", {})
    s.chapters |= set(le.get("chapters", {}).keys())
    s.intro_items |= set(le.get("intro_items", {}).keys())
    s.has_intro = s.has_intro or bool(le.get("intro"))
    for key in s.chapters:
        if ":" in key:
            s.parts.add(int(key.split(":", 1)[0]))
    s.questoes_range = (1, LE_MAX_QUESTAO)
    return s


@functools.cache
def load_structures(
    pentateuco_dir: Path = PENTATEUCO_DIR,
    mapping_path: Path = MAPPING_PATH,
) -> dict[str, Structure]:
    """Constrói o dicionário sigla → Structure para todas as 5 obras.

    Cacheado: o hook PostToolUse roda este check após cada Edit em wiki/**;
    relê os 4 .index.md + 1 json para cada arquivo seria desperdício.
    """
    out: dict[str, Structure] = {}
    for slug, sigla in OBRA_SIGLA.items():
        index_file = pentateuco_dir / f"{slug}.index.md"
        if index_file.exists():
            s = _parse_index(index_file)
        else:
            s = Structure()
        if sigla == "LE":
            s = _augment_le_from_mapping(s, mapping_path)
        if sigla == "LM":
            s.items_range = (1, LM_MAX_ITEM)
        # Sobrescreve has_intro pelo cânon: LM marca Introdução com bloco
        # `**INTRODUÇÃO**` inline, não como heading, então o parser do index
        # não a detecta. Genese tem heading "Capítulo I — Caráter da revelação
        # espírita" sem Introdução dedicada — só Prefácio. ESE tem Introdução
        # detectada normalmente; LE pega do mapping.
        s.has_intro = sigla in _OBRAS_COM_INTRODUCAO
        out[sigla] = s
    return out


def resolve_locus(sigla_raw: str, rest: str, structure: Structure) -> tuple[bool, str]:
    """Decide se `(sigla, rest)` aponta para um locus que existe na obra.

    Devolve `(ok, motivo)`: `ok=True` quando o locus existe ou não pode ser
    falsificado (padrão de citação fora dos quatro reconhecidos); `ok=False`
    com motivo curto quando há certeza de inexistência. Conservador: prefere
    silêncio a falso-positivo, porque `check_citation_format` já cobre a
    forma malformada da citação.

    Quatro padrões reconhecidos, na ordem:
    1. `Introdução, item X` — intro_items.
    2. `Introdução` — has_intro.
    3. `cap. X` ou `Nª parte, cap. X` — chapters (chave `"N:R"` ou `"R"`).
    4. `q. N` — questoes_range (LE) ou items_range (LM).
    """
    # Corta no primeiro `; OUTRA_SIGLA`/`, OUTRA_SIGLA` — referência seguinte
    # pertence a outra obra e não deve poluir esta resolução.
    cut = NEXT_SIGLA_RE.search(rest)
    if cut:
        rest = rest[:cut.start()]

    # Caso 1: Introdução com item — (LE, Introdução, item IV)
    m = _INTRO_IT_RE.search(rest)
    if m:
        if not structure.has_intro:
            return False, "obra sem Introdução"
        item = m.group("r").upper()
        if structure.intro_items and item not in structure.intro_items:
            return False, f"Introdução não tem item {item}"
        return True, ""

    # Caso 2: Introdução sem item — (LE, Introdução)
    if _INTRO_RE.search(rest):
        if not structure.has_intro:
            return False, "obra sem Introdução"
        return True, ""

    # Caso 3: capítulo com ou sem parte — (ESE, cap. XVII) | (C&I, 1ª parte, cap. VI)
    cap_m = _CAP_RE.search(rest)
    part_m = _PART_NUM_RE.search(rest)
    if cap_m:
        cap = cap_m.group("r").upper()
        if part_m:
            n = int(part_m.group("n"))
            if structure.parts and n not in structure.parts:
                return False, f"{n}ª parte inexistente"
            key = f"{n}:{cap}"
            if structure.chapters and key not in structure.chapters:
                return False, f"{n}ª parte, cap. {cap} inexistente"
            return True, ""
        # Sem parte explícita: se a obra usa partes, aceitar quando o cap.
        # existe sob qualquer uma; senão exigir match direto sem parte.
        if structure.parts:
            if any(k.endswith(f":{cap}") or k == cap for k in structure.chapters):
                return True, ""
            return False, f"cap. {cap} inexistente"
        if structure.chapters and cap not in structure.chapters:
            return False, f"cap. {cap} inexistente"
        return True, ""

    # Caso 4: questão (LE) ou item global (LM) — (LE, q. 990)
    q_m = _Q_RE.search(rest)
    if q_m:
        n = int(q_m.group("n"))
        rng = structure.questoes_range or structure.items_range
        if rng:
            lo, hi = rng
            if not (lo <= n <= hi):
                return False, f"q. {n} fora do range [{lo}, {hi}]"
        return True, ""

    return True, ""
