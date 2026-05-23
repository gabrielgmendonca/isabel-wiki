#!/usr/bin/env bash
#
# convert_pdf_to_md.sh — converte um PDF born-digital em Markdown via marker e
# salva o .md já no lugar certo do raw/: ao lado do PDF de origem.
#
# Uso:
#   ./scripts/convert_pdf_to_md.sh <caminho/para/arquivo.pdf> [dir_de_saida] [args extras p/ marker]
#
# Exemplo:
#   ./scripts/convert_pdf_to_md.sh raw/autores/camille-flammarion/a-morte-e-o-seu-misterio/a-morte-e-o-seu-misterio-vol-3.pdf
#   -> gera raw/autores/camille-flammarion/a-morte-e-o-seu-misterio/a-morte-e-o-seu-misterio-vol-3.md
#
# Defaults validados por smoke test (mai/2026, corpus Bozzano/Léon Denis/Flammarion):
# - SEM LLM por padrão. Nestes PDFs born-digital de prosa o --use_llm do marker
#   produz saída byte-idêntica à sem LLM (LLMSectionHeaderProcessor não muda
#   nada; LLMPageCorrectionProcessor nem dispara): só custaria API + latência.
#   Ative com USE_LLM=1 apenas em obras com tabelas/layout sujo onde ajuda.
# - --disable_ocr + --disable_image_extraction: o corpus tem text-layer real
#   (OCR desnecessário e pior) e as imagens já eram descartadas de qualquer modo.
# - TORCH_DEVICE=cpu. NÃO use mps: trava com torch.AcceleratorError no encoder
#   de layout do surya nesta versão do marker (1.10.x). cpu ~= 6s/página.
# - USE_LLM=1 fixa gemini-2.5-flash-lite (o default gemini-2.0-flash do marker
#   está deprecado) e aí sim exige GEMINI_API_KEY no .env.
# - .env só é necessário/carregado quando USE_LLM=1.
# - Args extras após o 2º são repassados ao marker_single (ex.: --page_range 0-10).

set -euo pipefail

usage() { echo "Uso: $0 <arquivo.pdf> [dir_de_saida] [args extras p/ marker]  (env: USE_LLM=1 p/ ativar LLM)" >&2; exit 1; }

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

SRC_DIR="$(cd "$(dirname "$PDF")" && pwd)"
REPO_ROOT="$(git -C "$SRC_DIR" rev-parse --show-toplevel 2>/dev/null || pwd)"

# Args base: sem OCR (text-layer real) e sem extração de imagens (eram descartadas).
MARKER_ARGS=(--disable_ocr --disable_image_extraction)

USE_LLM="${USE_LLM:-0}"
if [ "$USE_LLM" = "1" ]; then
  # Localiza o .env: raiz do repo; em worktree, fallback p/ a árvore principal.
  ENV_FILE="$REPO_ROOT/.env"
  if [ ! -f "$ENV_FILE" ]; then
    COMMON_DIR="$(git -C "$REPO_ROOT" rev-parse --path-format=absolute --git-common-dir 2>/dev/null || true)"
    [ -n "$COMMON_DIR" ] && [ -f "$(dirname "$COMMON_DIR")/.env" ] && ENV_FILE="$(dirname "$COMMON_DIR")/.env"
  fi
  [ -f "$ENV_FILE" ] || { echo "Erro: USE_LLM=1 mas .env não encontrado (procurei em $REPO_ROOT/.env)" >&2; exit 1; }
  set -a; . "$ENV_FILE"; set +a
  [ -n "${GEMINI_API_KEY:-}" ] || { echo "Erro: USE_LLM=1 mas GEMINI_API_KEY ausente em $ENV_FILE" >&2; exit 1; }
  # gemini-2.0-flash (default do marker 1.10.2) está deprecado — fixar 2.5-flash-lite.
  MARKER_ARGS+=(--use_llm --gemini_api_key "$GEMINI_API_KEY" --gemini_model_name gemini-2.5-flash-lite)
fi

# cpu fixo por default: mps trava (AcceleratorError no encoder de layout do surya).
export TORCH_DEVICE="${TORCH_DEVICE:-cpu}"

STEM="$(basename "${PDF%.[pP][dD][fF]}")"
TMP_OUT="$(mktemp -d)"
trap 'rm -rf "$TMP_OUT"' EXIT

echo "→ Convertendo: $PDF"
echo "  TORCH_DEVICE=$TORCH_DEVICE  USE_LLM=$USE_LLM"
uv run --project "$REPO_ROOT" marker_single "$PDF" \
  --output_dir "$TMP_OUT" \
  "${MARKER_ARGS[@]}" \
  "$@"

MD_SRC="$TMP_OUT/$STEM/$STEM.md"
[ -f "$MD_SRC" ] || { echo "Erro: marker não gerou $MD_SRC" >&2; exit 1; }
mv -f "$MD_SRC" "$OUT_DIR/$STEM.md"

echo "✓ Markdown salvo em: $OUT_DIR/$STEM.md"
