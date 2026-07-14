#!/bin/bash
#
# Loop diário da wiki — o "Loop Engineering" do IsAbel.
#
# NUNCA toca no seu working tree. Roda numa worktree dedicada, resetada a
# origin/main a cada execução, e entrega o resultado como Pull Request.
#
# ── Cascata de custo crescente ───────────────────────────────────────────────
#
#   Nível 0 (ZERO tokens) — dreno determinístico: promove os rascunhos cujo item
#     do ROADMAP §11 já foi resolvido. Invariantes travadas por teste; o leitor
#     do site não vê diferença (rascunho já é público — nada usa `draft:`, então
#     o RemoveDrafts do Quartz não filtra nada). É contabilidade interna.
#     → PR que se MESCLA SOZINHO quando o lint-pr passa.
#
#   Nível 1 (barato) — só SE houver candidata: uma sessão `claude -p /dreno N`
#     em que um agente julga a completude editorial de N páginas do /ingest.
#     Houve juízo, e o resultado é conteúdo numa wiki pública.
#     → PR que ESPERA a sua revisão.
#
# Se não há trabalho, o dia custa ZERO token e nenhum PR é aberto.
#
# ── Por que PR, e não push direto ────────────────────────────────────────────
#
# O ruleset "Protect main" exige pull request (com 0 aprovações). É por isso que
# o stats-daily.yml está desligado: o bot do GitHub Actions não está na lista de
# bypass e leva GH013. Rodando local, o push sai com a SUA credencial — mas o PR
# ainda é o caminho certo: dá trilha de auditoria e passa pelo lint-pr de graça.
#
# ── Uso ──────────────────────────────────────────────────────────────────────
#
#   ./scripts/loop-diario.sh          # lote normal (N=3)
#   ./scripts/loop-diario.sh 5        # lote de 5
#   DRENO_DRY=1 ./scripts/loop-diario.sh   # seco: não escreve, não commita, não abre PR
#
# Instalar como cron diário: ver scripts/com.isabel.loop-diario.plist.

set -euo pipefail

# O checkout PRINCIPAL do repo — não o diretório do script. Se este script for
# invocado de dentro de uma worktree, `dirname $0/..` apontaria para ela, e a
# worktree do loop nasceria aninhada dentro de outra. `--git-common-dir` sempre
# resolve o .git compartilhado; o pai dele é o checkout principal.
GIT_COMMON="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --path-format=absolute --git-common-dir)"
ROOT="$(cd "$(dirname "$GIT_COMMON")" && pwd)"
WT="$ROOT/.claude/worktrees/loop-diario"
HOJE="$(date +%Y-%m-%d)"
LIMITE="${1:-3}"
SECO="${DRENO_DRY:-}"

# Base da worktree. `origin/main` é o certo em produção — o loop trabalha sempre
# sobre o que está publicado, nunca sobre o seu working tree. Sobrescrever só
# para testar antes de o /dreno ter sido levado a main (ex.: LOOP_BASE=HEAD).
BASE="${LOOP_BASE:-origin/main}"

LOG_DIR="$ROOT/reports/loop-diario"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/$HOJE.log"

# launchd não herda o PATH do shell interativo — resolver as ferramentas aqui.
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"

log() { echo "[$(date +%H:%M:%S)] $*" | tee -a "$LOG"; }

# ── trava de execução única ──────────────────────────────────────────────────
# Sem isto, o launchd disparando às 9h enquanto uma execução manual ainda roda
# dava DUAS execuções fazendo `reset --hard` e `clean -fd` na MESMA worktree ao
# mesmo tempo — receita para commit pela metade e worktree corrompida.
# `mkdir` é atômico em POSIX; um lock por arquivo não seria.
LOCK="$LOG_DIR/.lock"
if ! mkdir "$LOCK" 2>/dev/null; then
  DONO=$(cat "$LOCK/pid" 2>/dev/null || echo "?")
  if [ "$DONO" != "?" ] && kill -0 "$DONO" 2>/dev/null; then
    log "já há um loop rodando (pid $DONO) — saindo sem fazer nada."
    exit 0
  fi
  log "trava órfã encontrada (pid $DONO morto) — reivindicando."
  rm -rf "$LOCK" && mkdir "$LOCK"
fi
echo $$ > "$LOCK/pid"
trap 'rm -rf "$LOCK"' EXIT INT TERM

# ── preflight: falhar CEDO, antes de mutar qualquer coisa ────────────────────
# A chave SSH deste repo tem passphrase no keychain (`UseKeychain yes`) e o
# token do gh vive no keyring. Num LaunchAgent com o keychain bloqueado, ambos
# falham — e é muito melhor descobrir isso ANTES de criar branch e commit.
preflight() {
  if ! gh auth status >/dev/null 2>&1; then
    log "ERRO: o gh não está autenticado neste contexto (keychain bloqueado?)."
    exit 1
  fi
  if ! git -C "$ROOT" ls-remote --exit-code origin HEAD >/dev/null 2>&1; then
    log "ERRO: sem acesso ao origin por SSH (chave/keychain indisponível?)."
    exit 1
  fi
}

# ── worktree limpa, sempre em cima de origin/main ────────────────────────────
# `git clean -fd` (sem -x) remove só o não-rastreado NÃO-ignorado: preserva
# .venv e node_modules (caros de recriar) e não toca em __pycache__.
prepara_worktree() {
  git -C "$ROOT" fetch --quiet origin
  if [ ! -d "$WT" ]; then
    log "criando worktree dedicada em $WT"
    git -C "$ROOT" worktree add --detach --quiet "$WT" "$BASE"
  fi
  # `--detach` ANTES do reset: na segunda chamada a worktree ainda está na
  # branch que o abre_pr criou, e um `reset --hard` ali moveria o ponteiro DELA
  # para origin/main — desfazendo localmente o commit que acabou de virar PR.
  git -C "$WT" checkout -q --detach
  git -C "$WT" reset --hard --quiet "$BASE"
  git -C "$WT" clean -fdq

  # Guarda: sem isto, o launchd falharia com um erro críptico de "arquivo não
  # encontrado" enquanto o /dreno não tivesse sido levado a main.
  if [ ! -f "$WT/.claude/skills/dreno/scripts/dreno.py" ]; then
    log "ERRO: o /dreno não existe em $BASE."
    log "      Leve-o a main primeiro (/ship). Para testar antes: LOOP_BASE=<ref>"
    exit 1
  fi
}

# ── o diff do nível 0 é MESMO só troca de status? ────────────────────────────
# O auto-merge se justifica por este fato — então ele é VERIFICADO, não assumido.
# Se qualquer linha fora de `status:` aparecer no diff, o lote é rebaixado a
# revisão humana em vez de entrar em main sem ninguém olhar.
so_troca_de_status() {
  linhas=$(git -C "$WT" diff -U0 | grep -E '^[+-][^+-]' || true)
  fora=$(echo "$linhas" | grep -vE '^[+-]status: (rascunho|ativo)$' || true)
  [ -z "$fora" ]
}

# ── espera o CI com teto de tempo ────────────────────────────────────────────
# `gh pr checks --watch` não tem timeout: se o CI travar, o job do launchd fica
# pendurado para sempre. macOS não traz o `timeout` do GNU, então é na mão.
espera_ci() {
  branch="$1"; teto="${2:-900}"
  (cd "$WT" && gh pr checks "$branch" --watch --fail-fast >/dev/null 2>&1) &
  pid=$!
  ( sleep "$teto"; kill "$pid" 2>/dev/null ) &
  vigia=$!
  if wait "$pid" 2>/dev/null; then
    kill "$vigia" 2>/dev/null || true
    return 0
  fi
  kill "$vigia" 2>/dev/null || true
  return 1
}

# ── abre PR a partir do estado atual da worktree ─────────────────────────────
#   $1 branch · $2 título · $3 corpo · $4 "auto" p/ mesclar após CI verde
abre_pr() {
  branch="$1"; titulo="$2"; corpo="$3"; modo="$4"

  git -C "$WT" checkout -q -B "$branch"
  git -C "$WT" add -A
  git -C "$WT" -c user.name="loop-diario" \
               -c user.email="loop@isabel.local" \
               commit -qm "$titulo"
  git -C "$WT" push -q --force-with-lease -u origin "$branch"

  url=$(cd "$WT" && gh pr create --base main --head "$branch" \
          --title "$titulo" --body "$corpo")
  log "PR aberto: $url"

  if [ "$modo" != "auto" ]; then
    log "  ↳ aguarda SUA revisão (houve juízo de agente)."
    return 0
  fi

  log "  ↳ esperando o lint-pr (teto de 15min)…"
  if espera_ci "$branch" 900; then
    (cd "$WT" && gh pr merge "$branch" --squash --delete-branch) \
      && log "  ↳ CI verde → mesclado automaticamente. ✓"
  else
    log "  ↳ CI vermelho, ausente ou estourou o teto → PR fica aberto p/ você. ⚠"
  fi
}

log "════ loop diário — $HOJE ════"
[ -z "$SECO" ] && preflight
prepara_worktree
cd "$WT"

# ── NÍVEL 0 — determinístico, zero tokens ────────────────────────────────────
if [ -n "$SECO" ]; then
  log "nível 0 [SECO] — o que SERIA promovido:"
  uv run python .claude/skills/dreno/scripts/dreno.py promover --dry-run 2>&1 | tee -a "$LOG"
else
  log "nível 0 — dreno: promovendo rascunhos já resolvidos…"
  uv run python .claude/skills/dreno/scripts/dreno.py promover 2>&1 | tee -a "$LOG"
fi

log "nível 0 — lint (29 checks determinísticos)…"
RESUMO_LINT=$(uv run python .claude/skills/lint/scripts/lint_wiki.py 2>/dev/null \
  | grep '"summary"' | sed 's/.*: "//; s/".*//' || echo "lint não rodou")
log "  $RESUMO_LINT"

if [ -z "$SECO" ] && ! git -C "$WT" diff --quiet; then
  N=$(git -C "$WT" diff --name-only | wc -l | tr -d ' ')

  # O auto-merge se apoia em "este diff só troca `status:`". Isso é VERIFICADO
  # aqui, não assumido — se qualquer outra linha aparecer (um script passou a
  # escrever um arquivo, um `git add -A` pegou algo inesperado), o lote é
  # rebaixado a revisão humana em vez de entrar em main sem ninguém olhar.
  if so_troca_de_status; then
    MODO="auto"
    NOTA="Diff verificado: **só** linhas \`status: rascunho\` → \`status: ativo\`."
  else
    MODO="revisao"
    NOTA="⚠ **Automescla cancelada.** O diff tem linhas fora de \`status:\` — algo
mudou além das promoções. Revise antes de mesclar."
    log "  ⚠ diff do nível 0 tem linha fora de \`status:\` → rebaixado a revisão."
  fi

  abre_pr "loop/auto-$HOJE" \
    "dreno: promove $N rascunho(s) resolvido(s) a \`ativo\`" \
    "Lote **determinístico** do loop diário — zero tokens, zero juízo.

Promove a \`ativo\` os rascunhos cujos itens do ROADMAP §11 já estão \`[x]\`.
Invariantes travadas por \`tests/test_dreno.py\`: não bumpa \`atualizado_em\`
(senão a página recai na fila do Opus) e slug ambíguo nunca promove.

O leitor do site não vê diferença: rascunho já é público (nada usa \`draft:\`).

$NOTA

Lint: $RESUMO_LINT

🤖 Gerado por \`scripts/loop-diario.sh\`" \
    "$MODO"
else
  log "nível 0 — nada a promover."
fi

# ── NÍVEL 1 — agente barato, só se houver trabalho ───────────────────────────
CANDIDATAS=$(uv run python .claude/skills/dreno/scripts/dreno.py triagem --format json \
  | python3 -c 'import json,sys; print(len(json.load(sys.stdin)["candidata"]))')
log "nível 1 — $CANDIDATAS candidata(s) do /ingest aguardando revisão editorial."

if [ "$CANDIDATAS" -eq 0 ]; then
  log "════ nada a revisar — dia encerrado sem gastar token. ✓ ════"
  exit 0
fi

if [ -n "$SECO" ]; then
  log "[SECO] — não invocando o Claude, não abrindo PR. ✓"
  log "  as $LIMITE primeiras que seriam revisadas:"
  uv run python .claude/skills/dreno/scripts/dreno.py triagem --limit "$LIMITE" 2>/dev/null \
    | sed -n '/CANDIDATA/,/^$/p' | tail -n +2 | tee -a "$LOG"
  exit 0
fi

# Parte de origin/main de novo: o nível 0 já virou PR próprio. Os conjuntos de
# páginas são disjuntos (nível 0 mexe nos buckets C/E; nível 1, no bucket A),
# então as duas branches nunca conflitam entre si.
prepara_worktree
cd "$WT"

log "nível 1 — invocando /dreno $LIMITE (sessão headless)…"
claude -p "/dreno $LIMITE" --permission-mode acceptEdits 2>&1 | tee -a "$LOG"

if git -C "$WT" diff --quiet && [ -z "$(git -C "$WT" status --porcelain)" ]; then
  log "nível 1 — o agente não mudou nada."
  log "════ fim. ════"
  exit 0
fi

abre_pr "loop/revisao-$HOJE" \
  "dreno: revisão editorial de até $LIMITE rascunho(s) do /ingest" \
  "Lote **julgado por agente** do loop diário — precisa dos seus olhos.

Um agente barato leu cada página e julgou **completude editorial** (tem
\`## Fontes\`? afirmações citadas? nada truncado?). Ele **não** audita
fidelidade doutrinária — isso é do \`/critica\`.

Confira as promoções a \`ativo\` antes de mesclar.

Lint: $RESUMO_LINT

🤖 Gerado por \`scripts/loop-diario.sh\`" \
  "revisao"

log "════ fim. ════"
