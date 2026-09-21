"""Digest da página-semente, para o Passo 1 do `/palestra`.

Uma semente grande não cabe inteira no prompt de cada agente (a de *Pão Nosso*
cap. 173 tem 50k caracteres). O digest mantém frontmatter + todos os headers +
as linhas que carregam locus de citação.

**Seções preservadas na íntegra** (`SECOES_INTEIRAS`): o roteiro de palestra, a
música e as notas de entrega não têm locus em quase nenhuma linha — no run de
2026-09-12 o digest por locus apagou a moldura musical inteira da semente
("Além das Janelas" / "Redenção") e o dossiê saiu sem ela. São exatamente as
seções que o dossiê mais precisa herdar, então vão inteiras.

    uv run python .claude/skills/palestra/scripts/seed_digest.py <página.md> [--saida arq] [--max N]
"""
import argparse
import re
import sys
import unicodedata
from pathlib import Path

# Casa contra o texto do header, sem acento e em minúscula.
SECOES_INTEIRAS = ("uso em palestra", "roteiro", "musica", "recursos de palestra", "como contar")

LOCUS = re.compile(
    r"\((LE|LM|ESE|C&I|Gênese|OPE|OQE|RE)[,\s]"           # (LE, q. 642)
    r"|\b(LE|ESE|LM|C&I),? (q\.|cap\.|item|\d)"           # LE q. 642 · ESE cap. XV
    r"|\b(q\.|cap\.|item)\s*\d"                           # q. 642 solto na prosa
    r"|/\s?(Chico Xavier|Divaldo|Espírito Santo Neto)"    # psicografia: Autor / Médium
    r"|\[\[(wiki/biblia|raw/)"                            # versículo ou fonte linkada
    r"|\((At|Jo|Mt|Mc|Lc|Fp|Tg|1 Co|2 Co|Rm|Hb)\s?\d"     # (At 1.8)
)


def sem_acento(s):
    return unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode("ascii").lower()


def digest(texto):
    linhas = texto.splitlines()
    if not linhas or linhas[0] != "---":
        print("aviso: semente sem frontmatter", file=sys.stderr)
        fim = -1
    else:
        fim = linhas.index("---", 1)
    saida = linhas[: fim + 1]
    inteira = False
    for ln in linhas[fim + 1 :]:
        if ln.startswith("#"):
            titulo = sem_acento(re.sub(r"^#+\s*", "", ln))
            # um header de mesmo nível ou acima encerra a seção preservada
            inteira = any(s in titulo for s in SECOES_INTEIRAS)
            saida += ["", ln]
        elif inteira or LOCUS.search(ln):
            saida.append(ln)
    return "\n".join(saida).strip() + "\n"


def preparar(texto, teto=12000):
    """Devolve (seedTexto, seedTruncado) — a decisão do Passo 1 em uma função."""
    return (texto, False) if len(texto) <= teto else (digest(texto), True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pagina", type=Path)
    ap.add_argument("--saida", type=Path, help="grava aqui (default: stdout)")
    ap.add_argument("--max", type=int, default=12000,
                    help="acima deste tamanho a semente vira digest (default: 12000)")
    args = ap.parse_args()

    texto = args.pagina.read_text(encoding="utf-8")
    saida, truncado = preparar(texto, args.max)

    print(f"{args.pagina}: {len(texto)} chars -> {len(saida)} chars; seedTruncado={str(truncado).lower()}",
          file=sys.stderr)
    if args.saida:
        args.saida.write_text(saida, encoding="utf-8")
    else:
        sys.stdout.write(saida)


if __name__ == "__main__":
    main()
