#!/usr/bin/env bash
#
# pdf_to_md.sh — converte um PDF em Markdown (marker + Gemini) e salva o .md
# já no lugar certo do raw/: ao lado do PDF de origem.
#
# Uso:
#   ./pdf_to_md.sh <caminho/para/arquivo.pdf> [dir_de_saida]
#
# Exemplo:
#   ./pdf_to_md.sh raw/autores/camille-flammarion/a-morte-e-o-seu-misterio/a-morte-e-o-seu-misterio-vol-3.pdf
#   -> gera raw/autores/camille-flammarion/a-morte-e-o-seu-misterio/a-morte-e-o-seu-misterio-vol-3.md
#
# - dir_de_saida default = diretório do próprio PDF (não precisa mais passar à mão).
# - TORCH_DEVICE default = cpu. Sobrescreva no ambiente: TORCH_DEVICE=mps ./pdf_to_md.sh ...
# - .env é localizado sozinho (raiz do repo; em worktree cai no .env da árvore principal).
# - Subdir do marker é achatado; _meta.json e imagens extraídas são descartados.
# - Args extras após o 2º são repassados ao marker_single (ex.: --page_range 0-10).

set -euo pipefail

usage() { echo "Uso: $0 <arquivo.pdf> [dir_de_saida] [args extras p/ marker]" >&2; exit 1; }

[ $# -ge 1 ] || usage
PDF="$1"; shift
[ -f "$PDF" ] || { echo "Erro: PDF não encontrado: $PDF" >&2; exit 1; }
case "$PDF" in *.pdf|*.PDF) ;; *) echo "Erro: esperado um .pdf, recebi: $PDF" >&2; exit 1;; esac

# Diretório de saída: 2º arg se fornecido e não for uma flag; senão, a pasta do PDF.
OUT_DIR="$(cd "$(dirname "$PDF")" && pwd)"
if [ $# -ge 1 ] && [ "${1#-}" = "$1" ]; then
  OUT_DIR="$1"; shift
fi
mkdir -p "$OUT_DIR"

# Localiza o .env: raiz do repo; em worktree, faz fallback p/ a árvore principal.
SRC_DIR="$(cd "$(dirname "$PDF")" && pwd)"
REPO_ROOT="$(git -C "$SRC_DIR" rev-parse --show-toplevel 2>/dev/null || pwd)"
ENV_FILE="$REPO_ROOT/.env"
if [ ! -f "$ENV_FILE" ]; then
  COMMON_DIR="$(git -C "$REPO_ROOT" rev-parse --path-format=absolute --git-common-dir 2>/dev/null || true)"
  [ -n "$COMMON_DIR" ] && [ -f "$(dirname "$COMMON_DIR")/.env" ] && ENV_FILE="$(dirname "$COMMON_DIR")/.env"
fi
[ -f "$ENV_FILE" ] || { echo "Erro: .env não encontrado (procurei em $REPO_ROOT/.env)" >&2; exit 1; }

set -a; . "$ENV_FILE"; set +a
[ -n "${GEMINI_API_KEY:-}" ] || { echo "Erro: GEMINI_API_KEY ausente em $ENV_FILE" >&2; exit 1; }
export TORCH_DEVICE="${TORCH_DEVICE:-cpu}"

STEM="$(basename "${PDF%.[pP][dD][fF]}")"
TMP_OUT="$(mktemp -d)"
trap 'rm -rf "$TMP_OUT"' EXIT

echo "→ Convertendo: $PDF"
echo "  TORCH_DEVICE=$TORCH_DEVICE  .env=$ENV_FILE"
uv run --project "$REPO_ROOT" marker_single "$PDF" \
  --output_dir "$TMP_OUT" \
  --use_llm \
  --gemini_api_key "$GEMINI_API_KEY" \
  "$@"

MD_SRC="$TMP_OUT/$STEM/$STEM.md"
[ -f "$MD_SRC" ] || { echo "Erro: marker não gerou $MD_SRC" >&2; exit 1; }

IMG_COUNT="$(find "$TMP_OUT/$STEM" -type f \( -iname '*.jpeg' -o -iname '*.jpg' -o -iname '*.png' \) | wc -l | tr -d ' ')"
mv -f "$MD_SRC" "$OUT_DIR/$STEM.md"

echo "✓ Markdown salvo em: $OUT_DIR/$STEM.md"
[ "$IMG_COUNT" -gt 0 ] && echo "  (descartadas $IMG_COUNT imagens extraídas e o _meta.json — refs de imagem no .md ficarão quebradas)"
