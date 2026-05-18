"""Helpers de slug e layout canônico de raw/.

Centraliza a lógica usada por:
- scripts/link_citations.py (resolução de wikilinks)
- scripts/list_pending_ingest.py (matching raw↔wiki)
- scripts/normalize_raw_layout.py (migração de layout)
- .claude/skills/lint/scripts/lint_wiki.py (check_raw_layout)
"""

from __future__ import annotations

import re
import unicodedata


CANONICAL_SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

# Subpastas diretas de raw/ que são esperadas. Qualquer outro nome em raw/
# acende warning no check_raw_layout.
RAW_TOP_LEVEL_DIRS: frozenset[str] = frozenset({
    "autores",
    "mediuns",
    "palestras",
    "artigos",
    "kardec",
    "biblia-acf",
    "assets",
})

# Sufixos artefato comuns deixados por extratores de PDF/HTML. Sempre removidos
# antes de slugificar — `obra_compress.pdf` vira `obra.pdf`.
ARTIFACT_SUFFIXES: tuple[str, ...] = (
    "_compress",
    "-compress",
    "_min",
    "-min",
    "pdf_compress",
    "pdfcompress",
    # `pdf` colado no fim (resíduo de extratores que incluem a extensão no nome
    # do diretório derivado). Só removido se sobrar conteúdo antes — strip_artifact_suffixes
    # garante len(stem) > len(suf).
    "pdf",
)

# Sequências de UTF-8 URL-encoded escapado que aparecem em alguns dumps
# (ex.: "à" → "c3a0", "â" → "c3a2"). Detectamos como artefato sem tentar
# decodificar — o operador humano decide o slug correto.
URL_ENCODED_ARTIFACT_RE = re.compile(r"c3a[0-9a-f]")


def _decode_url_encoded(s: str) -> str:
    """Decodifica sequências UTF-8 escapadas em hex que aparecem em alguns
    dumps (ex.: `c3a0` → 'à', `c3a2` → 'â'). Tenta decodificar; em caso de
    falha, simplesmente remove o token para evitar lixo no slug.
    """
    def _replace(m: re.Match[str]) -> str:
        token = m.group(0)
        try:
            return bytes.fromhex(token).decode("utf-8")
        except (ValueError, UnicodeDecodeError):
            return ""
    # Captura sequências de 2+ pares hex contíguos começando com c3 (range
    # comum de letras acentuadas latinas em UTF-8). Genérico o bastante para
    # lidar com c3a0, c3a1, c3a2, c3a7 (ç) etc.
    return re.sub(r"(?:c3[0-9a-f]{2})+", _replace, s)


def slugify(text: str) -> str:
    """kebab-case ASCII a partir de string arbitrária.

    Pipeline: decodifica UTF-8 escapado → NFKD → strip diacríticos → lowercase
    → colapsa não-alfanumérico em '-'. Não remove stopwords (isso é
    responsabilidade de quem precisa de matching mais agressivo, ex.:
    list_pending_ingest.normalize).
    """
    s = _decode_url_encoded(text)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def strip_artifact_suffixes(stem: str) -> str:
    """Remove sufixos artefato conhecidos do final do stem (sem extensão).

    Aplicado repetidamente até estabilizar — `x_compress_min` vira `x`.
    """
    prev = None
    cur = stem
    while cur != prev:
        prev = cur
        for suf in ARTIFACT_SUFFIXES:
            if cur.endswith(suf) and len(cur) > len(suf):
                cur = cur[: -len(suf)]
                break
    return cur


def has_artifact_marker(name: str) -> bool:
    """True se `name` contém marcador de artefato (sufixo real ou UTF-8 escapado).

    Espelha `strip_artifact_suffixes`: o marcador só conta quando é sufixo de
    fato no fim do stem (extensão removida), nunca substring solta. Evita
    falso-positivo em palavras legítimas que contêm "min"/"pdf" no meio
    (ex.: "...proporcoes-minusculas.pdf"). Usado pelo check para flaggar slugs
    sujos sem precisar normalizar.
    """
    if URL_ENCODED_ARTIFACT_RE.search(name):
        return True
    if "." in name and not name.startswith("."):
        stem = name.rpartition(".")[0]
    else:
        stem = name
    stem = stem.lower()
    return strip_artifact_suffixes(stem) != stem


def is_canonical_slug(s: str) -> bool:
    """True se `s` bate com kebab-case ASCII puro."""
    return bool(CANONICAL_SLUG_RE.match(s))


def canonical_for(raw_name: str) -> str:
    """Sugestão de slug canônico para um nome bruto (arquivo ou pasta).

    Pipeline: separa extensão → strip_artifact_suffixes → slugify → recompõe.
    """
    if "." in raw_name and not raw_name.startswith("."):
        stem, _, ext = raw_name.rpartition(".")
        stem_clean = strip_artifact_suffixes(stem)
        return f"{slugify(stem_clean)}.{ext.lower()}"
    return slugify(strip_artifact_suffixes(raw_name))
