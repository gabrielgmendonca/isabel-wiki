#!/usr/bin/env bash
# Leva os commits da worktree atual para `main`.
#
# Fluxo:
#   1. Verifica que a worktree atual está limpa e ahead de main
#   2. Faz rebase da branch atual sobre main (com rerere)
#   3. Fast-forward em main, na worktree onde main está checked out
#
# Em conflito que não pode ser resolvido automaticamente, aborta o rebase e
# sai com mensagem de erro listando os arquivos pendentes.
#
# Flags:
#   --merge        usa merge --no-ff em vez de rebase
#   --keep-branch  não apaga a branch após sucesso (default: apaga)
#   --dry-run      mostra o que faria, sem aplicar

set -euo pipefail

MAIN_BRANCH="${MAIN_BRANCH:-main}"
USE_MERGE=0
KEEP_BRANCH=0
DRY_RUN=0

for arg in "$@"; do
  case "$arg" in
    --merge) USE_MERGE=1 ;;
    --keep-branch) KEEP_BRANCH=1 ;;
    --dry-run) DRY_RUN=1 ;;
    -h|--help)
      awk 'NR>1 && /^#/ {sub(/^# ?/, ""); print; next} NR>1 {exit}' "$0"
      exit 0
      ;;
    *)
      echo "erro: flag desconhecida: $arg" >&2
      exit 64
      ;;
  esac
done

run() {
  if [[ $DRY_RUN -eq 1 ]]; then
    printf '[dry-run] %s\n' "$*"
  else
    "$@"
  fi
}

die() {
  echo "erro: $*" >&2
  exit 1
}

CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
[[ "$CURRENT_BRANCH" != "HEAD" ]] || die "HEAD destacado; faça checkout numa branch antes."
[[ "$CURRENT_BRANCH" != "$MAIN_BRANCH" ]] || die "já estamos em $MAIN_BRANCH; nada a integrar."

# Worktree atual deve estar limpa.
if ! git diff --quiet || ! git diff --cached --quiet; then
  die "working tree suja. Commit ou stash antes de rodar."
fi

# Localiza a worktree onde main está checked out (precisamos dela para fast-forward).
MAIN_WORKTREE="$(git worktree list --porcelain | awk -v b="refs/heads/$MAIN_BRANCH" '
  /^worktree / { wt = substr($0, 10) }
  $0 == "branch " b { print wt; exit }
')"
[[ -n "$MAIN_WORKTREE" ]] || die "$MAIN_BRANCH não está checked out em nenhuma worktree."

# Garante que main está limpa também (vamos mexer no working tree dela no ff).
if ! git -C "$MAIN_WORKTREE" diff --quiet \
   || ! git -C "$MAIN_WORKTREE" diff --cached --quiet; then
  die "worktree de $MAIN_BRANCH ($MAIN_WORKTREE) está suja. Limpe antes."
fi

AHEAD="$(git rev-list --count "$MAIN_BRANCH..HEAD")"
BEHIND="$(git rev-list --count "HEAD..$MAIN_BRANCH")"

if [[ "$AHEAD" -eq 0 ]]; then
  echo "$CURRENT_BRANCH não tem commits novos sobre $MAIN_BRANCH; nada a fazer."
  exit 0
fi

echo "→ $CURRENT_BRANCH: $AHEAD commit(s) ahead, $BEHIND behind de $MAIN_BRANCH"
echo "→ main worktree: $MAIN_WORKTREE"

if [[ $USE_MERGE -eq 1 ]]; then
  # Estratégia merge: faz tudo dentro da worktree do main.
  echo "→ merge --no-ff de $CURRENT_BRANCH em $MAIN_BRANCH"
  if ! run git -C "$MAIN_WORKTREE" -c rerere.enabled=true \
         merge --no-ff --no-edit "$CURRENT_BRANCH"; then
    {
      echo "conflitos no merge não resolvidos automaticamente. Arquivos:"
      while IFS= read -r -d '' f; do printf '  %s\n' "$f"; done \
        < <(git -C "$MAIN_WORKTREE" diff -z --name-only --diff-filter=U || true)
      echo
      echo "resolva manualmente em $MAIN_WORKTREE com:"
      echo "  git -C $MAIN_WORKTREE merge $CURRENT_BRANCH"
    } >&2
    run git -C "$MAIN_WORKTREE" merge --abort || true
    exit 2
  fi
else
  # Estratégia rebase: rebase aqui, depois fast-forward main.
  echo "→ rebase de $CURRENT_BRANCH sobre $MAIN_BRANCH (rerere ligado)"
  if ! run git -c rerere.enabled=true rebase "$MAIN_BRANCH"; then
    {
      echo "conflitos no rebase não resolvidos automaticamente. Arquivos:"
      while IFS= read -r -d '' f; do printf '  %s\n' "$f"; done \
        < <(git diff -z --name-only --diff-filter=U || true)
      echo
      echo "resolva manualmente nesta worktree com:"
      echo "  git rebase $MAIN_BRANCH"
      echo "  # …resolva conflitos, git add, git rebase --continue…"
      echo "  $0  # rode de novo quando estiver clean"
    } >&2
    run git rebase --abort || true
    exit 2
  fi

  NEW_TIP="$(git rev-parse HEAD)"
  echo "→ fast-forward de $MAIN_BRANCH para $NEW_TIP"
  if ! run git -C "$MAIN_WORKTREE" merge --ff-only "$NEW_TIP"; then
    die "fast-forward de $MAIN_BRANCH falhou (não é ancestral). Algo mudou em main durante o rebase?"
  fi
fi

# Cleanup: apaga a branch local (se não for a única referência aos commits).
if [[ $KEEP_BRANCH -eq 0 && $DRY_RUN -eq 0 && $USE_MERGE -eq 0 ]]; then
  # Volta esta worktree para um estado neutro antes de apagar a branch.
  # Como a branch já está mergeada em main por fast-forward, é seguro.
  echo "→ apagando branch $CURRENT_BRANCH (mergeada)"
  git checkout --detach >/dev/null 2>&1 || true
  git branch -d "$CURRENT_BRANCH" || {
    echo "aviso: não consegui apagar $CURRENT_BRANCH; rode 'git branch -D $CURRENT_BRANCH' se quiser forçar." >&2
  }
fi

echo "✓ $MAIN_BRANCH agora em $(git -C "$MAIN_WORKTREE" rev-parse --short HEAD)"
