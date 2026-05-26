#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat >&2 <<'EOF'
Uso: ./yt-bulk.sh <URL-do-canal> --limit N

Transcreve em massa os N vídeos mais recentes de um canal do YouTube.
Pula vídeos cujo par <slug>.md + summary-<slug>.md já existe em
raw/palestras/<canal-slug>/.

Env:
  BROWSER_COOKIES   Navegador para --cookies-from-browser (default: safari)
EOF
  exit 64
}

URL=""
LIMIT=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --limit)
      LIMIT="${2:-}"
      shift 2
      ;;
    --limit=*)
      LIMIT="${1#--limit=}"
      shift
      ;;
    -h|--help)
      usage
      ;;
    -*)
      echo "Erro: flag desconhecida: $1" >&2
      usage
      ;;
    *)
      if [[ -z "$URL" ]]; then
        URL="$1"
      else
        echo "Erro: argumento posicional extra: $1" >&2
        usage
      fi
      shift
      ;;
  esac
done

[[ -z "$URL" ]] && { echo "Erro: URL do canal é obrigatória." >&2; usage; }
[[ -z "$LIMIT" ]] && { echo "Erro: --limit N é obrigatório." >&2; usage; }
[[ "$LIMIT" =~ ^[0-9]+$ && "$LIMIT" -gt 0 ]] || { echo "Erro: --limit precisa ser inteiro positivo." >&2; usage; }

BROWSER_COOKIES="${BROWSER_COOKIES:-safari}"
export BROWSER_COOKIES

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
YT_SCRIPT="$SCRIPT_DIR/../../yt/scripts/yt.sh"
[[ -x "$YT_SCRIPT" ]] || { echo "Erro: não encontrei $YT_SCRIPT executável." >&2; exit 1; }

# Kebab-case ASCII: minúsculas, sem acento, só [a-z0-9-].
# Precisa bater 1-pra-1 com a slugify de yt.sh.
slugify() {
  python3 - "$1" <<'PY'
import re, sys, unicodedata
t = unicodedata.normalize('NFKD', sys.argv[1]).encode('ascii', 'ignore').decode('ascii').lower()
print(re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', t)).strip('-'))
PY
}

# Normaliza URL: se for a raiz de um canal (sem aba específica), anexa /videos.
# Sem isso, yt-dlp resolve cada aba (Vídeos/Shorts/Lives) como playlist separada
# e --playlist-end N é aplicado por aba, não no total.
URL="${URL%/}"
case "$URL" in
  *youtube.com/watch*|*youtube.com/playlist*|*youtube.com/embed*|*youtu.be/*)
    : ;;  # vídeo único ou playlist explícita
  *youtube.com/@*/*|*youtube.com/c/*/*|*youtube.com/channel/*/*|*youtube.com/user/*/*)
    : ;;  # já tem aba específica
  *youtube.com/@*|*youtube.com/c/*|*youtube.com/channel/*|*youtube.com/user/*)
    URL="$URL/videos"
    echo "URL normalizada para: $URL"
    ;;
esac

DIR="raw/palestras"
mkdir -p "$DIR"

echo "Listando até $LIMIT vídeos mais recentes de: $URL"
IDS=$(uv run yt-dlp \
  --cookies-from-browser "$BROWSER_COOKIES" \
  --flat-playlist \
  --playlist-end "$LIMIT" \
  --print "%(id)s" \
  "$URL")

if [[ -z "$IDS" ]]; then
  echo "Nenhum vídeo encontrado para $URL." >&2
  exit 1
fi

TOTAL=$(echo "$IDS" | wc -l | tr -d ' ')
echo "Encontrados $TOTAL vídeos. Iniciando processamento sequencial."
echo ""

processed=0
skipped=0
failed=0
new_files=()
failed_urls=()

idx=0
while IFS= read -r id; do
  [[ -z "$id" ]] && continue
  idx=$((idx+1))
  video_url="https://www.youtube.com/watch?v=$id"

  echo "[$idx/$TOTAL] $video_url"

  meta=$(uv run yt-dlp \
    --cookies-from-browser "$BROWSER_COOKIES" \
    --skip-download \
    --print "%(channel)s" \
    --print "%(title)s" \
    "$video_url" 2>/dev/null || true)
  channel=$(printf '%s\n' "$meta" | sed -n '1p')
  title=$(printf '%s\n' "$meta" | sed -n '2p')
  if [[ -z "$channel" || -z "$title" ]]; then
    echo "  [fail] não foi possível obter canal/título"
    failed=$((failed+1))
    failed_urls+=("$video_url (metadata)")
    continue
  fi

  channel_slug=$(slugify "$channel")
  title_slug=$(slugify "$title")
  transcript="$DIR/$channel_slug/$title_slug.md"
  summary="$DIR/$channel_slug/summary-$title_slug.md"

  # Considera completo só quando ambos existem e não estão vazios.
  # yt.sh deixa o arquivo vazio se summarize falhar no meio (redirect > cria antes).
  if [[ -s "$transcript" && -s "$summary" ]]; then
    echo "  [skip] já existe: $transcript"
    skipped=$((skipped+1))
    continue
  fi
  # Reaproveitar parciais corromperia; apaga para yt.sh recriar limpo.
  rm -f "$transcript" "$summary"

  if "$YT_SCRIPT" "$video_url"; then
    processed=$((processed+1))
    new_files+=("$transcript")
  else
    echo "  [fail] yt.sh retornou erro"
    failed=$((failed+1))
    failed_urls+=("$video_url ($title)")
  fi
done <<< "$IDS"

echo ""
echo "============================="
echo "Resumo: processed=$processed skipped=$skipped failed=$failed (total=$TOTAL)"
echo "============================="

if (( ${#new_files[@]} > 0 )); then
  echo ""
  echo "Novos arquivos:"
  printf '  %s\n' "${new_files[@]}"
fi

if (( ${#failed_urls[@]} > 0 )); then
  echo ""
  echo "Falhas (retry via /yt <URL>):"
  printf '  %s\n' "${failed_urls[@]}"
  exit 2
fi
