#!/usr/bin/env bash
set -euo pipefail

URL="${1:?Uso: ./yt.sh <URL do YouTube>}"

# Cookies do navegador para o YouTube não bloquear como bot.
# Override via env: BROWSER_COOKIES=chrome ./yt.sh <URL>
BROWSER_COOKIES="${BROWSER_COOKIES:-safari}"
export SUMMARIZE_YT_DLP_COOKIES_FROM_BROWSER="$BROWSER_COOKIES"

# Kebab-case ASCII: minúsculas, sem acento, só [a-z0-9-].
slugify() {
  python3 - "$1" <<'PY'
import re, sys, unicodedata
t = unicodedata.normalize('NFKD', sys.argv[1]).encode('ascii', 'ignore').decode('ascii').lower()
print(re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', t)).strip('-'))
PY
}

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

# Uma chamada para resolver canal + título.
META=$(uv run yt-dlp \
  --cookies-from-browser "$BROWSER_COOKIES" \
  --skip-download \
  --print "%(channel)s" \
  --print "%(title)s" \
  "$URL")
CHANNEL=$(printf '%s\n' "$META" | sed -n '1p')
TITLE=$(printf '%s\n' "$META" | sed -n '2p')
[[ -n "$CHANNEL" && -n "$TITLE" ]] || { echo "Erro: não obteve canal/título para $URL" >&2; exit 1; }

echo "Canal: $CHANNEL"
echo "Título: $TITLE"

CHANNEL_SLUG=$(slugify "$CHANNEL")
TITLE_SLUG=$(slugify "$TITLE")

DIR="raw/palestras/$CHANNEL_SLUG"
mkdir -p "$DIR"
TRANSCRIPT="$DIR/$TITLE_SLUG.md"
SUMMARY="$DIR/summary-$TITLE_SLUG.md"

echo "Extraindo transcrição..."
{
  echo "Fonte: $URL"
  echo ""
  summarize --format md --youtube web --extract --cli claude "$URL"
} > "$TRANSCRIPT"
echo "  → $TRANSCRIPT"

echo "Gerando resumo..."
summarize --format md --youtube web --cli claude "$URL" > "$SUMMARY"
echo "  → $SUMMARY"

echo "Limpando markdown..."
lint_md "$TRANSCRIPT"
lint_md "$SUMMARY"

echo "Pronto!"
