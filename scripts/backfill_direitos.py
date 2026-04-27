#!/usr/bin/env python3
"""Adiciona o bloco `direitos:` ao frontmatter de cada página em wiki/obras/.

One-shot: roda uma vez para popular o campo nas ~30 obras existentes. Casos
`desconhecido` (palestras, autores ambíguos) viram backlog manual — o script
marca como `desconhecido` e o usuário revisa caso a caso.

Uso:
    uv run python scripts/backfill_direitos.py --dry-run   # mostra diff
    uv run python scripts/backfill_direitos.py             # aplica
"""

import argparse
import sys
from pathlib import Path

OBRAS_DIR = Path("wiki/obras")

# Mapeamento slug → bloco direitos. Determinístico e auditável.
# Detentores e ano_dp_estimado calibrados pela hierarquia da wiki (CLAUDE.md §2)
# e pela Lei 9.610/98 (DP no Brasil = 1º jan do ano seguinte aos 70 anos pmcs).

URL_FEB = "https://www.febnet.org.br/loja/"
URL_BOA_NOVA = "https://www.editoraboanova.com.br/"

DIREITOS: dict[str, dict] = {
    # Domínio público — Kardec (m. 1869)
    "livro-dos-espiritos": {"detentor": "dominio-publico"},
    "livro-dos-mediuns": {"detentor": "dominio-publico"},
    "evangelho-segundo-o-espiritismo": {"detentor": "dominio-publico"},
    "ceu-e-inferno": {"detentor": "dominio-publico"},
    "genese": {"detentor": "dominio-publico"},
    "obras-postumas": {"detentor": "dominio-publico"},
    "o-que-e-o-espiritismo": {"detentor": "dominio-publico"},
    "viagem-espirita-em-1862": {"detentor": "dominio-publico"},
    "espiritismo-mais-simples-expressao": {"detentor": "dominio-publico"},
    "resumo-da-lei-dos-fenomenos-espiritas": {"detentor": "dominio-publico"},

    # Domínio público — Léon Denis (m. 1927)
    "cristianismo-e-espiritismo": {"detentor": "dominio-publico"},
    "depois-da-morte": {"detentor": "dominio-publico"},
    "o-grande-enigma": {"detentor": "dominio-publico"},
    "o-problema-do-ser-e-do-destino": {"detentor": "dominio-publico"},

    # Domínio público — Novo Testamento (textos antigos)
    "atos-dos-apostolos": {"detentor": "dominio-publico"},
    "epistola-aos-hebreus": {"detentor": "dominio-publico"},
    "epistola-aos-romanos": {"detentor": "dominio-publico"},
    "evangelho-segundo-joao": {"detentor": "dominio-publico"},
    "evangelho-segundo-lucas": {"detentor": "dominio-publico"},
    "evangelho-segundo-marcos": {"detentor": "dominio-publico"},
    "evangelho-segundo-mateus": {"detentor": "dominio-publico"},
    "primeira-epistola-aos-corintios": {"detentor": "dominio-publico"},

    # FEB — Chico Xavier (m. 2002 → DP em 2073) e médiuns associados
    "a-caminho-da-luz": {
        "detentor": "FEB",
        "ano_dp_estimado": 2073,
        "url_aquisicao": URL_FEB,
    },
    "entre-a-terra-e-o-ceu": {
        "detentor": "FEB",
        "ano_dp_estimado": 2073,
        "url_aquisicao": URL_FEB,
    },
    "evolucao-em-dois-mundos": {
        "detentor": "FEB",
        "ano_dp_estimado": 2073,
        "url_aquisicao": URL_FEB,
    },
    "vida-e-sexo": {
        "detentor": "FEB",
        "ano_dp_estimado": 2073,
        "url_aquisicao": URL_FEB,
    },

    # Boa Nova — Hammed (Francisco do Espírito Santo Neto, vivo)
    "as-dores-da-alma": {
        "detentor": "Boa-Nova",
        "url_aquisicao": URL_BOA_NOVA,
    },

    # Palestras (direitos do palestrante; texto-base de obras DP) — desconhecido
    "conquista-da-saude-psicologica": {
        "detentor": "desconhecido",
        "observacao": "Palestra; texto-base em DP, mas direitos da fala são do palestrante",
    },
    "felizes-os-pobres-em-espirito-carlos-mendonca": {
        "detentor": "desconhecido",
        "observacao": "Palestra (Carlos Mendonça); texto-base em DP (ESE)",
    },
    "jesus-ensina-em-cafarnaum-eelde": {
        "detentor": "desconhecido",
        "observacao": "Palestra (EELDE); texto-base em DP (ESE/LM)",
    },
    "parabola-do-semeador-carlos-mendonca": {
        "detentor": "desconhecido",
        "observacao": "Palestra (Carlos Mendonça); texto-base em DP (ESE)",
    },
    "quando-o-invisivel-se-torna-inevitavel": {
        "detentor": "desconhecido",
        "observacao": "Palestra; texto-base em DP (LE/LM)",
    },
}


def render_block(direitos: dict) -> list[str]:
    """Serializa o dict direitos como bloco YAML aninhado (2 espaços de indent)."""
    lines = ["direitos:"]
    # Ordem fixa: detentor sempre primeiro; demais campos em ordem estável.
    order = ["detentor", "ano_dp_estimado", "url_aquisicao", "observacao"]
    for key in order:
        if key not in direitos:
            continue
        val = direitos[key]
        # Strings com `:` ou aspas precisam de quoting; URLs e observações curtas
        # ficam OK sem aspas para a maioria dos casos. Aspas conservadoras p/ obs.
        if key == "observacao":
            escaped = str(val).replace('"', '\\"')
            lines.append(f'  {key}: "{escaped}"')
        else:
            lines.append(f"  {key}: {val}")
    return lines


def has_direitos(lines: list[str]) -> bool:
    """Detecta se o frontmatter já tem campo direitos: (top-level)."""
    in_fm = False
    for line in lines:
        stripped = line.strip()
        if stripped == "---":
            if in_fm:
                return False
            in_fm = True
            continue
        if not in_fm:
            continue
        # Top-level key (sem indent inicial)
        if line and line[0] not in (" ", "\t") and stripped.startswith("direitos:"):
            return True
    return False


def insert_direitos(lines: list[str], block: list[str]) -> list[str] | None:
    """Insere o bloco direitos: antes de `atualizado_em:` no frontmatter.

    Retorna nova lista, ou None se não foi possível inserir (frontmatter mal formado).
    """
    in_fm = False
    insert_at: int | None = None
    fm_end: int | None = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == "---":
            if in_fm:
                fm_end = i
                break
            in_fm = True
            continue
        if in_fm and line and line[0] not in (" ", "\t") and stripped.startswith("atualizado_em:"):
            insert_at = i
            break

    if insert_at is None:
        # Sem atualizado_em: inserir antes do --- de fechamento
        if fm_end is None:
            return None
        insert_at = fm_end

    return lines[:insert_at] + block + lines[insert_at:]


def process_file(path: Path, dry_run: bool) -> str:
    """Retorna 'modified' | 'skipped-existing' | 'skipped-unmapped' | 'error'."""
    slug = path.stem
    if slug not in DIREITOS:
        return "skipped-unmapped"
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if has_direitos(lines):
        return "skipped-existing"
    block = render_block(DIREITOS[slug])
    new_lines = insert_direitos(lines, block)
    if new_lines is None:
        return "error"
    if not dry_run:
        # Preservar trailing newline se houver
        trailing = "\n" if text.endswith("\n") else ""
        path.write_text("\n".join(new_lines) + trailing, encoding="utf-8")
    return "modified"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--dry-run", action="store_true", help="Não escreve, só reporta o que faria")
    args = parser.parse_args(argv)

    if not OBRAS_DIR.exists():
        print(f"ERRO: {OBRAS_DIR} não encontrado", file=sys.stderr)
        return 1

    counts = {"modified": 0, "skipped-existing": 0, "skipped-unmapped": 0, "error": 0}
    unmapped_paths: list[Path] = []
    for path in sorted(OBRAS_DIR.glob("*.md")):
        result = process_file(path, args.dry_run)
        counts[result] += 1
        prefix = "[dry-run]" if args.dry_run else "[applied]"
        if result == "modified":
            slug = path.stem
            detentor = DIREITOS[slug]["detentor"]
            print(f"  {prefix} {path}  ->  detentor: {detentor}")
        elif result == "skipped-unmapped":
            unmapped_paths.append(path)
        elif result == "error":
            print(f"  ERRO: {path} — frontmatter mal formado")

    print()
    print(f"Modificadas: {counts['modified']}")
    print(f"Já tinham direitos: {counts['skipped-existing']}")
    print(f"Não mapeadas (slug ausente em DIREITOS): {counts['skipped-unmapped']}")
    if unmapped_paths:
        print("  Slugs:")
        for p in unmapped_paths:
            print(f"    - {p.stem}")
    print(f"Erros: {counts['error']}")
    if args.dry_run:
        print("\nDry-run: nenhum arquivo modificado. Rode sem --dry-run para aplicar.")
    return 0 if counts["error"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
