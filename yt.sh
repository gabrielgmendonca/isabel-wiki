#!/usr/bin/env bash
set -euo pipefail

URL="${1:?Uso: ./yt.sh <URL do YouTube>}"

lint_md() {
  local file="$1"
  awk '
    # Linha estrutural de markdown: não juntar com adjacentes
    function is_structural(line) {
      return line ~ /^(#|[-*>|!]|\[|```|Fonte:)/
    }
    {
      # trim trailing whitespace
      sub(/[[:space:]]+$/, "")
    }
    # Linha em branco: flush buffer e imprimir uma linha em branco
    /^[[:space:]]*$/ {
      if (buf != "") { print buf; buf = "" }
      if (!last_blank) print ""
      last_blank = 1
      next
    }
    {
      last_blank = 0
      if (is_structural($0)) {
        if (buf != "") { print buf; buf = "" }
        print
      } else if (buf == "") {
        buf = $0
      } else {
        buf = buf " " $0
      }
    }
    END { if (buf != "") print buf }
  ' "$file" > "$file.tmp" && mv "$file.tmp" "$file"
}

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

echo "Limpando markdown..."
lint_md "$TRANSCRIPT"
lint_md "$SUMMARY"

echo "Pronto!"
