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
#     do ROADMAP §11 já foi resolvido.
#
#   Nível 1 (barato) — só SE houver candidata: uma sessão `claude -p /dreno N`
#     em que um agente julga a completude editorial de N páginas do /ingest.
#
# Os DOIS níveis entregam PR que ESPERA revisão humana. Se não há trabalho, o dia
# custa ZERO token e nenhum PR é aberto.
#
# ── Por que NENHUM dos dois automescla (mudou em 2026-07-14) ─────────────────
#
# O nível 0 automesclava, apoiado em dois fatos. Auditoria adversarial mostrou
# que os DOIS eram falsos:
#
#   1. "O diff é só troca de `status:` — e isso é VERIFICADO, não assumido."
#      O guarda que verificava (`so_troca_de_status`) falhava ABERTO. Ele filtrava
#      o diff com `grep -E '^[+-][^+-]'`, que descarta toda linha cujo CONTEÚDO
#      começa com `-` — ou seja, todo bullet em coluna zero. 639 páginas da wiki
#      têm um: é a lista do `## Fontes`. Uma citação adulterada junto da promoção
#      passava como "só status" e ia para main sem ninguém olhar. O guarda também
#      era cego a arquivo novo não-rastreado — que o `git add -A` do `abre_pr`
#      commitava logo em seguida.
#
#   2. "O leitor do site não vê diferença — rascunho já é público."
#      Vê. O `deploy-wiki.yml` copia `quartz-overrides/components/DraftNotice.tsx`
#      para dentro do build e o `quartz.layout.ts` o renderiza: `status: rascunho`
#      estampa na página o aviso "pode conter lacunas, seções incompletas ou
#      citações não verificadas". Promover APAGA esse aviso do site público.
#
# Somados: o único PR que entrava em main sem revisão era justamente o que
# removia o aviso de que a página não fora revisada — guardado por um guarda que
# não guardava. Enquanto não existir uma verificação que valha o que promete
# (ver ROADMAP §5), os dois níveis esperam você.
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

# ── abre PR a partir do estado atual da worktree ─────────────────────────────
#   $1 branch · $2 título · $3 corpo
#
# Sempre PR de revisão — nada automescla. Além dos dois motivos do cabeçalho, o
# próprio `gh pr merge --squash --delete-branch` era uma armadilha aqui: para
# apagar a branch local ele faz `git checkout main` DENTRO da worktree, e o main
# já está checado no seu repo principal → `fatal: 'main' is already used by
# worktree at ...` → o `&&` devolve 1 → `set -e` matava o script, e o nível 1
# nunca rodava nos dias em que o nível 0 mesclava. (Pior: se você estivesse numa
# feature branch, o checkout SUCEDIA e a worktree do loop roubava o seu `main`.)
abre_pr() {
  branch="$1"; titulo="$2"; corpo="$3"

  git -C "$WT" checkout -q -B "$branch"
  git -C "$WT" add -A
  git -C "$WT" -c user.name="loop-diario" \
               -c user.email="loop@isabel.local" \
               commit -qm "$titulo"
  git -C "$WT" push -q --force-with-lease -u origin "$branch"

  url=$(cd "$WT" && gh pr create --base main --head "$branch" \
          --title "$titulo" --body "$corpo")
  log "PR aberto: $url"
  log "  ↳ aguarda SUA revisão."
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

# `status --porcelain`, não `git diff`: é o que o `git add -A` do abre_pr vai
# realmente commitar. `git diff` é cego a arquivo novo não-rastreado — e era
# justamente essa assimetria que deixava passar, sem exame, o que entrava no
# commit.
if [ -z "$SECO" ] && [ -n "$(git -C "$WT" status --porcelain)" ]; then
  N=$(git -C "$WT" status --porcelain | wc -l | tr -d ' ')

  abre_pr "loop/auto-$HOJE" \
    "dreno: promove $N rascunho(s) resolvido(s) a \`ativo\`" \
    "Lote **determinístico** do loop diário — zero tokens, zero juízo.

Promove a \`ativo\` os rascunhos cujos itens do ROADMAP §11 já estão \`[x]\`.
Invariantes travadas por \`tests/test_dreno.py\`: não bumpa \`atualizado_em\`
(senão a página recai na fila do Opus) e slug ambíguo (bucket F) nunca promove.

⚠ Promover **apaga do site público** o aviso \`DraftNotice\` (\"página em
rascunho — pode conter lacunas e citações não verificadas\"). Confira que cada
página listada tem mesmo o SEU item \`[x]\` no §11 antes de mesclar.

Lint: $RESUMO_LINT

🤖 Gerado por \`scripts/loop-diario.sh\`"
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

🤖 Gerado por \`scripts/loop-diario.sh\`"

log "════ fim. ════"
