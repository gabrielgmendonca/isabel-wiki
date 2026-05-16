#!/usr/bin/env bash
# Diagnóstico de "esta máquina está pronta para o projeto?".
# Não-fatal: roda todos os checks e imprime ✓/✗ + um resumo no fim.
# Rode logo após clonar, e de novo depois do bootstrap.
#
# Uso:  bash scripts/preflight.sh

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
QMD_INDEX="isabel"
CLAUDE_CFG="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
PASS=0
FAIL=0

ok()   { printf '  \033[32m✓\033[0m %s\n' "$1"; PASS=$((PASS + 1)); }
bad()  { printf '  \033[31m✗\033[0m %s\n' "$1"; FAIL=$((FAIL + 1)); }
have() { command -v "$1" >/dev/null 2>&1; }

echo "Preflight — $REPO_ROOT"
echo
echo "Ferramentas:"
have brew && ok "Homebrew ($(brew --version 2>/dev/null | head -1))" || bad "Homebrew ausente"
have git  && ok "git ($(git --version | awk '{print $3}'))"          || bad "git ausente"
have gh   && ok "gh"                                                  || bad "gh (GitHub CLI) ausente"
# ssh para o GitHub sai com código 1 mesmo quando autentica ("no shell access");
# capturar a saída antes de testar evita o pipefail mascarar o sucesso.
ssh_out="$(ssh -o BatchMode=yes -o ConnectTimeout=5 -T git@github.com 2>&1 || true)"
case "$ssh_out" in
  *"successfully authenticated"*) ok "SSH para github.com autenticado" ;;
  *) bad "SSH para github.com não autenticado (chave não configurada?)" ;;
esac
have uv && ok "uv ($(uv --version | awk '{print $2}'))" || bad "uv ausente"
if have node; then
  nv="$(node --version)"; nmaj="$(echo "$nv" | sed 's/^v//' | cut -d. -f1)"
  if [[ "$nmaj" =~ ^[0-9]+$ ]] && [[ "$nmaj" -ge 22 ]]; then
    ok "Node $nv (>= v22, CI usa v22)"
  else
    bad "Node $nv (precisa >= v22; CI usa v22)"
  fi
else
  bad "Node ausente (precisa >= v22; CI usa v22)"
fi
if have qmd; then
  ok "qmd ($(qmd --version 2>/dev/null | awk '{print $2}'))"
else
  bad "qmd ausente (brew; upstream github.com/tobi/qmd)"
fi
have rtk && ok "rtk" || bad "rtk ausente (Rust Token Killer)"

echo
echo "Versão do Python:"
want_py="$(tr -d '[:space:]' < "$REPO_ROOT/.python-version" 2>/dev/null || echo '?')"
if have uv && uv run --no-sync python --version >/dev/null 2>&1; then
  got_py="$(uv run --no-sync python --version 2>&1 | awk '{print $2}')"
  case "$got_py" in
    "$want_py"*) ok "Python do projeto $got_py (pin: $want_py)" ;;
    *)           bad "Python $got_py difere do pin $want_py (rode 'uv sync')" ;;
  esac
else
  bad "Não foi possível resolver o Python do projeto (pin: $want_py — rode 'uv sync')"
fi

echo
echo "Estado local (fora do git):"
ENV_FILE="$REPO_ROOT/.env"
if [[ -f "$ENV_FILE" ]]; then
  ok ".env presente"
  # OPENAI_BASE_URL já vem preenchida no .env.example — só checamos o que o
  # usuário precisa colar do gerenciador de senhas.
  for key in GEMINI_API_KEY OPENROUTER_API_KEY; do
    val="$(grep -E "^${key}=" "$ENV_FILE" | head -1 | cut -d= -f2- | tr -d '"'"'"' ')"
    [[ -n "$val" ]] && ok "  $key preenchida" || bad "  $key vazia/ausente em .env"
  done
else
  bad ".env ausente (cp .env.example .env e preencha)"
fi
[[ -f "$REPO_ROOT/.claude/settings.local.json" ]] \
  && ok ".claude/settings.local.json presente" \
  || bad ".claude/settings.local.json ausente (copie da máquina antiga)"
[[ -d "$REPO_ROOT/.venv" ]] \
  && ok ".venv presente" \
  || bad ".venv ausente (rode 'uv sync' ou scripts/bootstrap.sh)"

echo
echo "qmd:"
if have qmd && qmd --index "$QMD_INDEX" status >/dev/null 2>&1; then
  docs="$(qmd --index "$QMD_INDEX" status 2>/dev/null | grep -iE 'Total:' | head -1 | tr -dc '0-9')"
  ok "índice '$QMD_INDEX' acessível (${docs:-?} docs)"
else
  bad "índice qmd '$QMD_INDEX' inacessível (rode scripts/bootstrap.sh)"
fi
if [[ -f "$CLAUDE_CFG/.claude.json" ]] \
   && grep -q '"qmd"' "$CLAUDE_CFG/.claude.json" 2>/dev/null \
   && grep -q "\"$QMD_INDEX\"" "$CLAUDE_CFG/.claude.json" 2>/dev/null; then
  ok "MCP qmd registrado em $CLAUDE_CFG/.claude.json"
else
  bad "MCP qmd não registrado (claude mcp add qmd -- qmd --index $QMD_INDEX mcp)"
fi

echo
echo "Resumo: $PASS ok, $FAIL pendência(s)."
[[ "$FAIL" -eq 0 ]] && echo "Tudo pronto." || echo "Resolva as pendências acima (veja README.md → Setup / Migração)."
exit 0
