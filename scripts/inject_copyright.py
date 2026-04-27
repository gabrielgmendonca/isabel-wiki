#!/usr/bin/env python3
"""Pré-processa wiki/obras/*.md adicionando callout de direitos autorais.

Para obras com `direitos.detentor` em {FEB, Boa-Nova, LEAL, IDE}, insere um
callout Markdown `> [!note] Direitos autorais` entre o frontmatter e o primeiro
heading. Obras em domínio público ou com detentor `desconhecido` não recebem
callout.

Roda no pipeline de build (mesmo lugar que `link_citations.py`) sobre a cópia
em `/tmp/quartz/content`, sem alterar arquivos do repo.

Uso:
    uv run python scripts/inject_copyright.py --check /tmp/quartz/content/wiki
    uv run python scripts/inject_copyright.py --apply /tmp/quartz/content/wiki
    uv run python scripts/inject_copyright.py --check wiki/obras/evolucao-em-dois-mundos.md
"""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / ".claude" / "skills"))
from _lib.wiki_utils import parse_frontmatter  # noqa: E402

PROTECTED_DETENTORES = {"FEB", "Boa-Nova", "LEAL", "IDE"}
CALLOUT_MARKER = "> [!note] Direitos autorais"


def render_callout(direitos: dict) -> str | None:
    detentor = direitos.get("detentor")
    if detentor not in PROTECTED_DETENTORES:
        return None
    url = direitos.get("url_aquisicao")
    base = (
        f"{CALLOUT_MARKER}\n"
        f"> Os trechos citados nesta página pertencem aos detentores "
        f"({detentor}). O uso aqui é estudo e comentário; não substitui a obra original."
    )
    if url:
        return f"{base} [Onde adquirir]({url}).\n"
    return base + "\n"


def has_callout(text: str) -> bool:
    return CALLOUT_MARKER in text


def find_frontmatter_end(lines: list[str]) -> int:
    """Retorna o índice (0-based) do `---` de fechamento, ou -1 se não houver."""
    if not lines or lines[0].strip() != "---":
        return -1
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == "---":
            return i
    return -1


def inject_into_text(text: str, callout: str) -> str:
    """Insere callout entre o frontmatter e o primeiro conteúdo."""
    if has_callout(text):
        return text
    lines = text.splitlines(keepends=True)
    end_fm = find_frontmatter_end(lines)
    if end_fm == -1:
        return text
    # Padrão: ---\n\n<callout>\n<resto>
    head = lines[: end_fm + 1]
    tail = lines[end_fm + 1 :]
    # Garantir uma linha em branco entre fechamento do FM e o callout
    if not head[-1].endswith("\n"):
        head[-1] += "\n"
    insertion = ["\n", callout if callout.endswith("\n") else callout + "\n", "\n"]
    return "".join(head + insertion + tail)


def process_file(path: Path, apply: bool) -> bool:
    fm, _ = parse_frontmatter(path)
    if fm.get("tipo") != "obra":
        return False
    direitos = fm.get("direitos")
    if not isinstance(direitos, dict):
        return False
    callout = render_callout(direitos)
    if callout is None:
        return False
    text = path.read_text(encoding="utf-8")
    if has_callout(text):
        return False
    new_text = inject_into_text(text, callout)
    if new_text == text:
        return False
    if apply:
        path.write_text(new_text, encoding="utf-8")
    return True


def iter_targets(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    obras_dir = path / "obras" if (path / "obras").is_dir() else path
    if not obras_dir.is_dir():
        return []
    return sorted(obras_dir.glob("*.md"))


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true", help="reporta sem escrever")
    g.add_argument("--apply", action="store_true", help="escreve in-place")
    ap.add_argument("path", type=Path, help="arquivo .md ou diretório (wiki/ ou wiki/obras/)")
    args = ap.parse_args(argv)

    targets = iter_targets(args.path)
    if not targets:
        print(f"ERRO: nenhum target encontrado em {args.path}", file=sys.stderr)
        return 1

    n = 0
    for p in targets:
        if process_file(p, args.apply):
            n += 1
            print(f"  {'[applied]' if args.apply else '[check]'} {p}")

    label = "Modificadas" if args.apply else "A modificar"
    print(f"\n{label}: {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
