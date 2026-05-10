#!/usr/bin/env python3
"""Normaliza o layout de raw/ para o esquema canônico.

Esquema:
- Slugs kebab-case ASCII puros (sem `_`, sem espaços, sem maiúsculas, sem
  diacríticos, sem sufixos artefato `_compress`/`-min`).
- `raw/mediuns/<medium>/<autor-espiritual>/<obra>` (sempre 3 níveis).
- `<slug>.pdf` no nível pai + `<slug>/<slug>.md` + `<slug>/_meta.json` +
  `<slug>/assets/_page_*.jpeg` (imagens dentro de assets/).
- `summary-*.md` em `palestras/` migra para `_summaries/<slug>.md` (sem prefixo).

Uso:
  uv run python scripts/normalize_raw_layout.py [--dry-run]
  uv run python scripts/normalize_raw_layout.py --apply
  uv run python scripts/normalize_raw_layout.py --apply --scope raw/palestras

Refusa rodar com --apply se houver staged/uncommitted em raw/ (evita misturar
mudanças manuais com renomeação automática).
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"

sys.path.insert(0, str(ROOT / "scripts"))
from _slug import (  # noqa: E402
    canonical_for,
    has_artifact_marker,
    is_canonical_slug,
)

EXCEPTIONS_FILE = RAW / ".normalize-exceptions.txt"

# Heurísticas para inferir o autor espiritual a partir do nome de um arquivo
# em raw/mediuns/<medium>/. Aplicadas em ordem; o primeiro match ganha.
SPIRIT_AUTHOR_HINTS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"joanna[\s_\-]*de[\s_\-]*[âa]ngelis", re.I), "joanna-de-angelis"),
    (re.compile(r"\bja\b|joanna", re.I), "joanna-de-angelis"),
    (re.compile(r"andr[ée][\s_\-]*luiz", re.I), "andre-luiz"),
    (re.compile(r"\bemmanuel\b", re.I), "emmanuel"),
    (re.compile(r"bezerra[\s_\-]*de[\s_\-]*menezes", re.I), "bezerra-de-menezes"),
    (re.compile(r"\bhumberto[\s_\-]*de[\s_\-]*campos\b", re.I), "humberto-de-campos"),
]
SPIRIT_AUTHOR_FALLBACK = "diversos"

# Mapping obra → autor espiritual para psicografias famosas. Resolve casos
# onde o filename não cita o autor espiritual (ex.: "nosso-lar.md" → andre-luiz).
# Chave: slug canônico (após canonical_for) sem extensão.
# `__default__` define o autor espiritual presumido quando nem o mapping
# nem as regex SPIRIT_AUTHOR_HINTS resolvem. Use só quando a esmagadora
# maioria das obras do médium sai via um único espírito (Divaldo/Joanna).
OBRA_TO_SPIRIT: dict[str, dict[str, str]] = {
    "divaldo-franco": {
        "__default__": "joanna-de-angelis",
    },
    "chico-xavier": {
        # Emmanuel
        "o-consolador": "emmanuel",
        "pao-nosso": "emmanuel",
        "fonte-viva": "emmanuel",
        "vinha-de-luz": "emmanuel",
        "caminho-verdade-e-vida": "emmanuel",
        "paulo-e-estevao": "emmanuel",
        "ha-dois-mil-anos": "emmanuel",
        "50-anos-depois": "emmanuel",
        "ave-cristo": "emmanuel",
        "renuncia": "emmanuel",
        "palavras-de-vida-eterna": "emmanuel",
        "agenda-crista": "emmanuel",
        "boa-nova": "humberto-de-campos",
        # André Luiz
        "nosso-lar": "andre-luiz",
        "missionarios-da-luz": "andre-luiz",
        "obreiros-da-vida-eterna": "andre-luiz",
        "e-a-vida-continua": "andre-luiz",
        "no-mundo-maior": "andre-luiz",
        "entre-a-terra-e-o-ceu": "andre-luiz",
        "libertacao": "andre-luiz",
        "evolucao-em-dois-mundos": "andre-luiz",
        "mecanismos-da-mediunidade": "andre-luiz",
        "nos-dominios-da-mediunidade": "andre-luiz",
        "sexo-e-destino": "andre-luiz",
        "vida-e-sexo": "andre-luiz",
        "acao-e-reacao": "andre-luiz",
        "desobsessao": "andre-luiz",
        "os-mensageiros": "andre-luiz",
    },
}

# Pastas top-level cujo conteúdo é tocado pelo normalizador.
NORMALIZED_TOPS = ("autores", "mediuns", "palestras", "artigos")


def load_exceptions() -> set[str]:
    if not EXCEPTIONS_FILE.exists():
        return set()
    return {
        line.strip()
        for line in EXCEPTIONS_FILE.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    }


def git_dirty_in_raw() -> bool:
    """True se há staged/unstaged em raw/ (untracked OK — vão ser regularizados)."""
    out = subprocess.run(
        ["git", "status", "--porcelain", "raw/"],
        capture_output=True, text=True, cwd=ROOT,
    )
    for line in out.stdout.splitlines():
        # Status string XY <path>; X=staged, Y=unstaged. ?? = untracked.
        if not line:
            continue
        xy = line[:2]
        if xy.strip() and xy != "??":
            return True
    return False


def infer_spirit_author(filename: str, medium_slug: str | None = None) -> str:
    """Inferência em três níveis:

    1. Mapping canônico OBRA_TO_SPIRIT[medium][slug-canônico-sem-extensão].
    2. Regex SPIRIT_AUTHOR_HINTS contra o filename original.
    3. Fallback `diversos`.
    """
    medium_map = OBRA_TO_SPIRIT.get(medium_slug or "", {})
    if medium_map:
        # Slug canônico do filename (sem extensão e sem artefatos)
        if "." in filename:
            stem = filename.rpartition(".")[0]
        else:
            stem = filename
        canonical_stem = canonical_for(stem)  # já é kebab-case ASCII
        if canonical_stem in medium_map:
            return medium_map[canonical_stem]
    for pat, slug in SPIRIT_AUTHOR_HINTS:
        if pat.search(filename):
            return slug
    if medium_map and "__default__" in medium_map:
        return medium_map["__default__"]
    return SPIRIT_AUTHOR_FALLBACK


# ─── Plano de renomeações ──────────────────────────────────────────────────────

def plan_renames(scope: Path | None, exceptions: set[str]) -> list[tuple[Path, Path]]:
    """Calcula a lista de renames (src, dst) — sempre dentro de raw/.

    Estratégia em passes (um por classe de violação) para deixar a saída
    auditável. Cada pass produz renames independentes; conflitos (dst já
    existe) são reportados pelo --dry-run e exigem intervenção manual.
    """
    plan: list[tuple[Path, Path]] = []

    def in_scope(p: Path) -> bool:
        if scope is None:
            return True
        try:
            p.relative_to(scope)
            return True
        except ValueError:
            return False

    def excluded(p: Path) -> bool:
        return str(p.relative_to(ROOT)) in exceptions

    # Nota: a convenção .claude/rules/convencoes-palestras.md exige `<TÍTULO>.md`
    # + `summary-<TÍTULO>.md` lado a lado. Não movemos summaries para subpasta;
    # o Pass 3 abaixo apenas slugifica o título preservando o prefixo `summary-`.

    # Pass 2: arquivos diretos em mediuns/<medium>/ → mediuns/<medium>/<spirit>/
    mediuns = RAW / "mediuns"
    if mediuns.exists():
        for medium_dir in sorted(mediuns.iterdir()):
            if not medium_dir.is_dir() or medium_dir.name.startswith("."):
                continue
            for child in sorted(medium_dir.iterdir()):
                if child.name.startswith(".") or not in_scope(child) or excluded(child):
                    continue
                if child.is_file():
                    spirit = infer_spirit_author(child.name, medium_dir.name)
                    new_name = canonical_for(child.name)
                    dst = medium_dir / spirit / new_name
                    plan.append((child, dst))
                else:
                    # Subdiretório: se já bate com slug canônico, é o autor
                    # espiritual — não toca aqui (Pass 4 cuida do conteúdo).
                    # Se não bate, é uma obra solta (caso Divaldo) e move pra
                    # <medium>/<spirit>/<obra-canonica>/
                    if is_canonical_slug(child.name) and len(child.name) <= 30:
                        # heurística rasa: nomes curtos e canônicos provavelmente
                        # são pastas de autor espiritual já corretas
                        # (emmanuel, andre-luiz, joanna-de-angelis...)
                        continue
                    spirit = infer_spirit_author(child.name, medium_dir.name)
                    new_dirname = canonical_for(child.name)
                    dst = medium_dir / spirit / new_dirname
                    plan.append((child, dst))

    # Pass 3: slugs não-canônicos em autores/ e palestras/ (e os filhos
    # diretos de mediuns/<medium>/<spirit>/ que ainda não foram capturados)
    for top in NORMALIZED_TOPS:
        base = RAW / top
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if p.name.startswith(".") or "_summaries" in p.parts:
                continue
            if not in_scope(p) or excluded(p):
                continue
            # Skip _page_* / _meta.json / assets — nomes estruturais
            if (
                p.name.startswith("_page_")
                or p.name == "assets"
                or p.name.endswith("_meta.json")
                or p.stem.endswith("_meta")
            ):
                # Para `<slug>_meta.json`, preservar o sufixo `_meta` mas
                # canonicalizar o slug que vem antes.
                if p.name.endswith("_meta.json"):
                    base_slug = p.name[: -len("_meta.json")]
                    if has_artifact_marker(base_slug) or not is_canonical_slug(base_slug):
                        new_base = canonical_for(base_slug)
                        if new_base and new_base != base_slug:
                            dst = p.parent / f"{new_base}_meta.json"
                            if not any(src == p for src, _ in plan):
                                plan.append((p, dst))
                continue
            target_name = p.stem if p.is_file() else p.name
            if not has_artifact_marker(target_name) and is_canonical_slug(target_name):
                continue
            new_name = canonical_for(p.name)
            if new_name == p.name:
                continue
            dst = p.parent / new_name
            # Evita duplicar se já planejamos mover este path em outro pass
            if any(src == p for src, _ in plan):
                continue
            plan.append((p, dst))

    # Pass 4: imagens _page_*.jpeg soltas em <slug>/ → <slug>/assets/
    for top in ("autores", "mediuns"):
        base = RAW / top
        if not base.exists():
            continue
        for slug_dir in base.rglob("*"):
            if not slug_dir.is_dir() or slug_dir.name == "assets":
                continue
            if not in_scope(slug_dir) or excluded(slug_dir):
                continue
            for img in slug_dir.iterdir():
                if not img.is_file():
                    continue
                if not img.name.startswith("_page_"):
                    continue
                if img.suffix.lower() not in (".jpeg", ".jpg", ".png"):
                    continue
                dst = slug_dir / "assets" / img.name
                plan.append((img, dst))

    return plan


def _is_same_file_case_insensitive(src: Path, dst: Path) -> bool:
    """True se src e dst apontam para o mesmo arquivo num filesystem
    case-insensitive (APFS macOS default). Detectamos comparando inodes —
    se o `dst` "existe" e tem o mesmo inode do `src`, é só case-rename.
    """
    try:
        return src.exists() and dst.exists() and src.stat().st_ino == dst.stat().st_ino
    except OSError:
        return False


def detect_conflicts(plan: list[tuple[Path, Path]]) -> list[str]:
    """Reporta destinos que já existem ou colidem entre renames planejados.

    Ignora o caso APFS case-insensitive (src e dst apontam para o mesmo
    inode) — isso é tratado como rename-via-tmp em apply_renames.
    """
    issues: list[str] = []
    seen_dst_ci: dict[str, Path] = {}
    sources = {src for src, _ in plan}
    for src, dst in plan:
        if dst.exists() and dst not in sources and not _is_same_file_case_insensitive(src, dst):
            issues.append(f"DESTINO JÁ EXISTE: {dst}  ←  {src}")
        # Comparar caminhos case-insensitive para detectar colisões reais.
        dst_key = str(dst).lower()
        if dst_key in seen_dst_ci:
            issues.append(f"COLISÃO ENTRE RENAMES: {dst}  ←  {src} e {seen_dst_ci[dst_key]}")
        else:
            seen_dst_ci[dst_key] = src
    return issues


def _git_mv(src: Path, dst: Path) -> None:
    is_tracked = subprocess.run(
        ["git", "ls-files", "--error-unmatch", str(src.relative_to(ROOT))],
        capture_output=True, text=True, cwd=ROOT,
    ).returncode == 0
    if is_tracked:
        subprocess.run(
            ["git", "mv", str(src.relative_to(ROOT)), str(dst.relative_to(ROOT))],
            check=True, cwd=ROOT,
        )
    else:
        src.rename(dst)


def apply_renames(plan: list[tuple[Path, Path]]) -> None:
    """Executa renames via `git mv` (preserva histórico).

    Para case-only renames em FS case-insensitive (APFS), usa rename via
    arquivo temporário para evitar colisão.

    Quando o plano contém um rename de diretório seguido de renames de
    filhos com o caminho antigo, remapeamos o `src` de cada entry através
    dos diretórios já renomeados. Sem isso, a segunda entry tenta mexer
    em um caminho que deixou de existir após o primeiro `git mv`.
    """
    dir_renames: list[tuple[Path, Path]] = []

    def _rewrite(p: Path) -> Path:
        for old_dir, new_dir in dir_renames:
            try:
                rel = p.relative_to(old_dir)
            except ValueError:
                continue
            return new_dir / rel
        return p

    for src, dst in plan:
        src = _rewrite(src)
        dst = _rewrite(dst)
        if src == dst:
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        if _is_same_file_case_insensitive(src, dst):
            tmp = src.parent / f".{src.name}.case-tmp"
            _git_mv(src, tmp)
            _git_mv(tmp, dst)
        else:
            _git_mv(src, dst)
        if dst.is_dir():
            dir_renames.append((src, dst))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dry-run", action="store_true", default=True,
                        help="Imprime tabela OLD→NEW sem executar (default).")
    parser.add_argument("--apply", action="store_true",
                        help="Executa os renames via git mv. Refusa se houver "
                             "staged/uncommitted em raw/.")
    parser.add_argument("--scope", metavar="PATH", default=None,
                        help="Limita a um subdir de raw/ (ex.: raw/palestras/divaldo-franco).")
    args = parser.parse_args()

    if not RAW.exists():
        print("raw/ não existe.", file=sys.stderr)
        return 1

    scope = None
    if args.scope:
        scope = Path(args.scope).resolve()
        try:
            scope.relative_to(RAW.resolve())
        except ValueError:
            print(f"--scope deve estar dentro de raw/: {scope}", file=sys.stderr)
            return 2

    if args.apply and git_dirty_in_raw():
        print(
            "raw/ tem staged/unstaged. Commit ou stash antes de rodar --apply.",
            file=sys.stderr,
        )
        return 3

    exceptions = load_exceptions()
    plan = plan_renames(scope, exceptions)
    conflicts = detect_conflicts(plan)

    print(f"# normalize_raw_layout — {len(plan)} renames planejados")
    if scope:
        print(f"# scope: {scope.relative_to(ROOT)}")
    if exceptions:
        print(f"# {len(exceptions)} exceção(ões) carregada(s) de {EXCEPTIONS_FILE.name}")
    print()

    for src, dst in plan:
        print(f"{src.relative_to(ROOT)}  →  {dst.relative_to(ROOT)}")

    if conflicts:
        print()
        print(f"# {len(conflicts)} conflito(s) — renames acima NÃO podem ser aplicados:")
        for c in conflicts:
            print(f"  ! {c}")
        return 4

    if args.apply:
        print()
        print("# aplicando…")
        apply_renames(plan)
        print(f"# {len(plan)} rename(s) executados via git mv.")
    else:
        print()
        print("# dry-run (default). Use --apply para executar.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
