#!/usr/bin/env bash
# Build local Quartz mirror do CI e sobe servidor em http://localhost:8080.
# Replica o workflow de .github/workflows/deploy-wiki.yml passo a passo.
#
# Uso:  ./scripts/serve-local.sh            # build + serve
#       ./scripts/serve-local.sh --build    # só build, sem serve
#       ./scripts/serve-local.sh --clean    # apaga /tmp/quartz e refaz tudo

set -euo pipefail

QUARTZ_DIR="/tmp/quartz"
QUARTZ_VERSION="v4.4.0"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

MODE="${1:-serve}"

if [[ "$MODE" == "--clean" ]]; then
  echo "==> Limpando $QUARTZ_DIR"
  rm -rf "$QUARTZ_DIR"
  MODE="serve"
fi

if [[ ! -d "$QUARTZ_DIR" ]]; then
  echo "==> Clonando Quartz $QUARTZ_VERSION em $QUARTZ_DIR"
  git clone --depth 1 --branch "$QUARTZ_VERSION" \
    https://github.com/jackyzha0/quartz.git "$QUARTZ_DIR"
  echo "==> npm ci"
  (cd "$QUARTZ_DIR" && npm ci)
fi

echo "==> Copiando conteúdo e configs"
rm -rf "$QUARTZ_DIR/content/wiki" "$QUARTZ_DIR/content/raw"
mkdir -p "$QUARTZ_DIR/content"
cp -r "$REPO_ROOT/wiki" "$QUARTZ_DIR/content/wiki"
cp -r "$REPO_ROOT/raw" "$QUARTZ_DIR/content/raw"
cp "$REPO_ROOT/index.md" "$QUARTZ_DIR/content/"
cp "$REPO_ROOT/logo-isabel.svg" "$QUARTZ_DIR/content/"
cp "$REPO_ROOT/static/icon.png" "$QUARTZ_DIR/quartz/static/icon.png"
cp "$REPO_ROOT/static/og-image.png" "$QUARTZ_DIR/quartz/static/og-image.png"
cp "$REPO_ROOT/quartz.config.ts" "$QUARTZ_DIR/quartz.config.ts"
cp "$REPO_ROOT/quartz.layout.ts" "$QUARTZ_DIR/quartz.layout.ts"
cp -r "$REPO_ROOT/quartz-overrides/components/"* "$QUARTZ_DIR/quartz/components/"

echo "==> Aplicando link_citations.py"
uv run python "$REPO_ROOT/scripts/link_citations.py" --apply "$QUARTZ_DIR/content/wiki"
uv run python "$REPO_ROOT/scripts/link_citations.py" --apply "$QUARTZ_DIR/content/index.md"

echo "==> Injetando avisos de direitos autorais"
uv run python "$REPO_ROOT/scripts/inject_copyright.py" --apply "$QUARTZ_DIR/content/wiki"

if [[ "$MODE" == "--build" ]]; then
  echo "==> Build (sem serve)"
  (cd "$QUARTZ_DIR" && npx quartz build)
else
  echo "==> Build + serve em http://localhost:8080"
  (cd "$QUARTZ_DIR" && npx quartz build --serve)
fi
