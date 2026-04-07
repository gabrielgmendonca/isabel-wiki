#!/usr/bin/env bash
set -euo pipefail

URL="${1:?Uso: ./yt.sh <URL do YouTube>}"

TITLE=$(yt-dlp --get-title "$URL")
echo "Título: $TITLE"

DIR="raw/palestras"
TRANSCRIPT="$DIR/$TITLE.md"
SUMMARY="$DIR/summary-$TITLE.md"

echo "Extraindo transcrição..."
{
  echo "Fonte: $URL"
  echo ""
  summarize --format md --youtube web --extract --model google/gemini-3.1-flash-lite-preview "$URL"
} > "$TRANSCRIPT"
echo "  → $TRANSCRIPT"

echo "Gerando resumo..."
summarize --format md --youtube web --model google/gemini-3.1-flash-lite-preview "$URL" > "$SUMMARY"
echo "  → $SUMMARY"

echo "Pronto!"
