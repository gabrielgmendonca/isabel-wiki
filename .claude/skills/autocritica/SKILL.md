---
name: autocritica
description: Roda UM lote não-interativo da crítica doutrinária profunda (/critica) sobre as próximas N páginas devidas, sem o gate de confirmação humana — o cap --limit é a salvaguarda de custo. Aplica correções seguras, difere o doutrinário a rascunho+ROADMAP, gera relatório e registra o estado. Feito para rodar em loop (`/loop /autocritica`). Use com /autocritica, /autocritica N, /autocritica --dry.
---

# /autocritica

Gatilhos: `/autocritica` · `/autocritica <N>` · `/autocritica --dry` · usado por `/loop /autocritica`

Wrapper **não-interativo** e **capped** do `/critica`. Mesma maquinaria, mesmo conservadorismo doutrinário — a única diferença é que **não há gate humano de confirmação** (o Passo 2 do `/critica`): no lugar, um **cap rígido** `--limit N` por lote torna o custo previsível e pequeno. Pensado para ser invocado repetidamente por `/loop`, drenando o backlog de páginas devidas em lotes, e ocioso quando não há nada devido.

É o análogo, para a crítica semântica, do `/autolint` previsto no ROADMAP (§5/§11): loop atenuado com cap por iteração e **humano no circuito nos achados doutrinários** (que continuam diferidos a `rascunho` + ROADMAP, nunca auto-corrigidos).

Reutiliza 100% dos scripts do `/critica` — não há código novo. Leia o SKILL do `/critica` (`.claude/skills/critica/SKILL.md`) para o detalhe de cada passo; aqui só muda o gate e o pacing.

## Argumentos

- **`<N>`** — tamanho do lote (default **5**). Vira `--limit N` no scope. Cap rígido de custo (~N agentes Opus de crítica + verificação Sonnet dos achados de eixo 1/2).
- **`--dry`** — lote report-only: cria o sentinela `.dryrun` (nenhuma página é mutada) e passa `dryRun:true` ao workflow. Útil para calibrar antes de gastar de verdade.
- **`--path GLOB`**, **`--status STATUS`**, **`--since YYYY-MM-DD`** — repassados ao scope quando o usuário quer recortar (ex.: `/autocritica --path 'wiki/questoes/*'`).

## Passo 1 — Escopo (cap rígido, SEM gate)

```bash
uv run python .claude/skills/critica/scripts/critica_scope.py --limit <N> --format json > /tmp/autocritica-scope.json
```

Ler o JSON. **Se `due_count == 0`**: não há nada devido — reportar "backlog vazio" e **encerrar a iteração**. Em loop, este é o sinal para dormir longo (re-checar edições novas mais tarde — ver "Uso com /loop"). Não invocar o workflow.

Se `due_count > 0`, seguir. **Não pedir confirmação ao usuário** — o cap já bounda o custo. (Esta é a diferença deliberada para o `/critica` interativo.)

## Passo 2 — Sentinela de dry-run

- **Modo apply (default):** garantir que o sentinela **não** exista — o lote vai mutar de verdade.
  ```bash
  rm -f .claude/skills/critica/state/.dryrun
  ```
- **Modo `--dry`:** criar o sentinela antes do workflow (o `critica_apply.py` recusa qualquer escrita enquanto ele existir, independente do agente) e removê-lo ao final do Passo 4.
  ```bash
  touch .claude/skills/critica/state/.dryrun
  ```

## Passo 3 — Rodar o workflow

Invocar a tool **Workflow** (a opt-in vem deste SKILL instruir o uso):

- `name`: `critica-profunda`
- `args`: `{ "pages": <campo pages do /tmp/autocritica-scope.json>, "dryRun": <true se --dry, senão false>, "terminologiaPath": "data/terminologia.json" }`

O workflow roda um pipeline por página (Crítica Opus → Verificação Sonnet adversarial dos achados de eixo 1/2) e **não** escreve em arquivos compartilhados — retorna `{ pages: [{ path, applied[], deferred[], summary }] }`. Cada `deferred` traz `disposition: "deferred"` (manter) ou `"dropped"` (a verificação refutou — só entra no relatório como descartado).

## Passo 4 — Síntese serial (idêntica ao Passo 4 do /critica)

Tudo que toca arquivo compartilhado acontece **aqui, serial no main-session**, nunca em agente paralelo. (Em `--dry`, o sentinela bloqueia toda escrita do `critica_apply.py`; ainda assim gerar o relatório.)

### 4a. Rotear os diferidos
Para cada página, para cada `deferred` com `disposition: "deferred"`:
1. Marcar a página como rascunho:
   ```bash
   uv run python .claude/skills/critica/scripts/critica_apply.py set-status --path <page> --status rascunho
   ```
2. Eixo 1 (divergência) — criar o stub (`status: aberta`):
   ```bash
   uv run python .claude/skills/critica/scripts/critica_apply.py divergencia-stub \
     --slug <divergencia_slug> --titulo "<título>" --conceito <page-sem-.md> --fontes "<siglas>" --tema "tema/<x>" \
     --kardec-pos "<...>" --kardec-cite "<locus>" --outra-pos "<...>" --outra-cite "<...>"
   ```
3. Anotar no ROADMAP §11:
   ```bash
   uv run python .claude/skills/critica/scripts/critica_apply.py roadmap-append \
     --item "[ ] **<page-sem-.md>** (<eixo>, <data>) — <tensão> · evidência: <locus/cite> · relatório: <report-dir>"
   ```
Itens `"dropped"` não geram ação.

### 4b. Montar o findings JSON e renderizar o relatório
Construir `/tmp/autocritica-findings.json` no schema de `critica_report.py` (`run` + `pages` + `findings`; cada finding com `disposition` ∈ `auto_fixed|deferred|dropped` e, quando houver, `action`/`verdict`). Em `run`, preencher `scope_flags` (ex.: `--limit N` + recortes), `pages_due` (do scope), `pages_critiqued`, `pages_skipped`. Carimbo via `date +%Y-%m-%d-%H%M`. Então:

```bash
uv run python .claude/skills/critica/scripts/critica_report.py --from /tmp/autocritica-findings.json
```

Imprime os caminhos `reports/critica/<timestamp>/report.{md,html}`. `reports/` é **versionado no git** (não está no `.gitignore`) mas **fora do build público** (`quartz.config.ts` `ignorePatterns`) — trilha de auditoria histórica, igual aos relatórios do `/critica`. O relatório entra no repo no `/ship` seguinte, junto com as mudanças das páginas.

### 4c. Registrar o estado (impede re-processar o mesmo no próximo lote)
```bash
uv run python .claude/skills/critica/scripts/critica_scope.py record --from /tmp/autocritica-findings.json
```
(O `record` recomputa o hash do corpo ATUAL — pós auto-fix — então a página sai do backlog **mesmo sem commit**. **Pular em `--dry`**: nada foi aplicado, registrar mentiria o estado.)

### 4d. Atualizar log.md (condicional)
Só se houve mudança ou diferimento (lote 100% limpo **não** é logado):
```
## [YYYY-MM-DD] autocritica | Lote de crítica — N páginas (X auto-fixes, Y diferidos)
<2–3 frases: o que foi auto-corrigido, o que foi diferido (link ROADMAP §11), quantos falsos-positivos a verificação descartou. Caminho do relatório.>
```

### 4e. (`--dry` apenas) Remover o sentinela
```bash
rm -f .claude/skills/critica/state/.dryrun
```

## Passo 5 — Reportar o backlog restante (pacing do loop)

Reexecutar o scope read-only e imprimir o **backlog restante** — é o que guia a cadência do loop:

```bash
uv run python .claude/skills/critica/scripts/critica_scope.py --limit <N> --format summary
```

Reportar em uma linha: páginas no lote, X auto-fixes, Y diferidos, Z descartados, caminho do HTML, e **`due_count` restante**.

## Uso com /loop

Self-paced (sem intervalo fixo — eu mesmo me reagendo a cada iteração):

```
/loop /autocritica
```

Pacing pelo `due_count` restante do Passo 5:
- **Restante > 0** → reagendar curto (próximo lote logo, cache quente: ~120–270s) até drenar o backlog.
- **Restante == 0** (ou Passo 1 já achou backlog vazio) → reagendar longo (~1800s / 30 min) só para pegar páginas recém-editadas. O usuário interrompe o loop quando quiser.

Para um lote único agora, sem recorrência: `/autocritica` (ou `/autocritica <N>`) sem `/loop`.

## Commit (default: NÃO commitar)

As mudanças do lote ficam no working tree. O `critica-state.json` já garante idempotência sem commit (Passo 4c), e cada lote deixa trilha de auditoria em `reports/critica/` + `log.md`. O usuário revisa o diff acumulado e roda `/ship` quando quiser levar a `main` — honra a política do projeto ("commitar/pushar só quando pedido") e evita commit direto em `main` na worktree. **Não** chamar `/ship` automaticamente daqui.

## Regras

- **Cap é a salvaguarda.** Sem gate humano por design; o `--limit` bounda o custo de cada lote. Não remover o cap em loop.
- **Conservadorismo doutrinário.** Na dúvida, diferir (rascunho + ROADMAP), nunca auto-corrigir sentido. Citação de autor complementar (qmd) **sempre** difere. (Imposto pelo próprio workflow.)
- **Kardec prevalece.** Divergência vira stub `status: aberta`, nunca apagada.
- **Sem escrita compartilhada em paralelo.** log.md, ROADMAP.md, state e relatório só no Passo 4 serial no main-session.
- **Humano no circuito.** Páginas diferidas viram `rascunho`; o usuário revisa o relatório + ROADMAP antes de promover de volta a `ativo`.
- **`uv run python`** para todo script local (ver `rules/scripts.md`).
