#!/usr/bin/env bash
# Regenera o estado local que NÃO está no git, numa máquina nova.
# Idempotente: pode rodar de novo sem estragar nada.
#
# Faz:
#   1. uv sync               (recria o .venv a partir do uv.lock)
#   2. coleções qmd wiki/raw (índice nomeado "isabel", usado pelo MCP)
#   3. contextos qmd         (resumos de coleção escritos à mão)
#   4. qmd update            (indexa os .md)
#   5. qmd embed             (gera embeddings — CUSTA HORAS na 1ª vez)
#
# Uso:  bash scripts/bootstrap.sh              # tudo, incluindo embed
#       bash scripts/bootstrap.sh --skip-embed # pula o embed (use se
#                                              # copiou ~/.cache/qmd/isabel.sqlite*
#                                              # da máquina antiga — ver README,
#                                              # "Atalho do índice qmd")
#
# NÃO cobre (passos manuais — o script avisa no fim):
#   - .env                  (cp .env.example .env + preencher)
#   - .claude/settings.local.json
#   - registro do MCP qmd no Claude Code

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
QMD_INDEX="isabel"
SKIP_EMBED=0
[[ "${1:-}" == "--skip-embed" ]] && SKIP_EMBED=1

cd "$REPO_ROOT"

if [[ ! -f "$REPO_ROOT/pyproject.toml" ]]; then
  echo "ERRO: rode a partir do repositório clonado (pyproject.toml não encontrado)." >&2
  exit 1
fi
for bin in uv qmd; do
  command -v "$bin" >/dev/null 2>&1 || {
    echo "ERRO: '$bin' não está no PATH. Veja README.md → toolchain." >&2
    exit 1
  }
done

# pillow (via torchvision) costuma não ter wheel quando o Python pinado é muito
# novo: o uv compila do fonte e o build precisa do libjpeg. No macOS o jpeg do
# Homebrew é keg-only — exporta as flags para o build do pillow achá-lo (no-op
# fora do macOS, sem Homebrew, ou sem a formula). Ver README → Toolchain.
if [[ "${OSTYPE:-}" == darwin* ]] && command -v brew >/dev/null 2>&1; then
  jpeg_prefix="$(brew --prefix jpeg 2>/dev/null || true)"
  if [[ -n "$jpeg_prefix" && -d "$jpeg_prefix/include" ]]; then
    export CPPFLAGS="-I$jpeg_prefix/include${CPPFLAGS:+ $CPPFLAGS}"
    export LDFLAGS="-L$jpeg_prefix/lib${LDFLAGS:+ $LDFLAGS}"
    export CPATH="$jpeg_prefix/include${CPATH:+:$CPATH}"
    export LIBRARY_PATH="$jpeg_prefix/lib${LIBRARY_PATH:+:$LIBRARY_PATH}"
  else
    echo "    aviso: formula 'jpeg' do Homebrew não encontrada — se 'uv sync'" >&2
    echo "    falhar compilando pillow, rode 'brew install jpeg' (README)." >&2
  fi
fi

echo "==> 1/5  uv sync"
uv sync

# qmd: adiciona a coleção só se ainda não existir no índice "isabel".
qmd_collection_present() {
  qmd --index "$QMD_INDEX" collection list 2>/dev/null \
    | grep -qE "^${1} \(qmd://"
}
add_collection() {
  local name="$1" path="$2"
  if qmd_collection_present "$name"; then
    echo "    coleção '$name' já existe — ok"
  else
    echo "    adicionando coleção '$name' -> $path"
    qmd --index "$QMD_INDEX" collection add "$path" --name "$name"
  fi
}

echo "==> 2/5  coleções qmd (índice '$QMD_INDEX')"
add_collection wiki "$REPO_ROOT/wiki"
add_collection raw  "$REPO_ROOT/raw"

# Contextos: strings exatas capturadas de `qmd context list` nesta máquina.
add_context() {
  local vpath="$1" text="$2"
  if qmd --index "$QMD_INDEX" context list 2>/dev/null | grep -qF "$text"; then
    echo "    contexto de '$vpath' já presente — ok"
  else
    echo "    adicionando contexto de '$vpath'"
    qmd --index "$QMD_INDEX" context add "$vpath" "$text"
  fi
}

echo "==> 3/5  contextos qmd"
add_context "qmd://wiki/" "Páginas curadas: conceitos doutrinários, obras, entidades, questões, sínteses, divergências. Frontmatter YAML, citações com sigla (LE, ESE, LM...), seção Fontes."
add_context "qmd://raw/"  "Material-fonte: livros transcritos (Kardec, Léon Denis, Chico Xavier), palestras, resumos. Organizado por autor/médium."

echo "==> 4/5  qmd update (re-indexa os .md)"
qmd --index "$QMD_INDEX" update

if [[ "$SKIP_EMBED" -eq 1 ]]; then
  echo "==> 5/5  qmd embed PULADO (--skip-embed)"
  echo "    Lembre de copiar ~/.cache/qmd/$QMD_INDEX.sqlite* da máquina antiga"
  echo "    (índice nomeado '$QMD_INDEX' — NÃO o ~/.cache/qmd/index.sqlite default;"
  echo "    ver README, 'Atalho do índice qmd'),"
  echo "    ou rode 'qmd --index $QMD_INDEX embed' quando puder esperar horas."
else
  echo "==> 5/5  qmd embed (gera embeddings — pode levar horas)"
  qmd --index "$QMD_INDEX" embed
fi

cat <<EOF

==> Bootstrap concluído. Faltam os passos manuais fora do git
    (independem da ordem em relação a este script — ver README passos 5/6/8):

  1. Segredos:
       cp .env.example .env   # depois preencha GEMINI_API_KEY / OPENROUTER_API_KEY

  2. .claude/settings.local.json — copie da máquina antiga (hook RTK + allowlist).

  3. Registre o MCP qmd no Claude Code (escopo local deste projeto):
       claude mcp add qmd -- qmd --index $QMD_INDEX mcp
     (confirme com 'claude mcp list'; o objeto fica em ~/.claude.json, ou
      \$CLAUDE_CONFIG_DIR/.claude.json se você definir CLAUDE_CONFIG_DIR)

  Smoke test: uv run python .claude/skills/lint/scripts/lint_wiki.py
EOF
