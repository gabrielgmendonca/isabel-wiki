---
name: autocritica
description: Roda UM lote não-interativo da crítica doutrinária profunda (/critica) sobre as próximas N páginas devidas, sem o gate de confirmação humana — o cap --limit é a salvaguarda de custo. Aplica correções seguras, difere o doutrinário a rascunho+ROADMAP, gera relatório e registra o estado. Feito para rodar em loop (`/loop /autocritica`). Use com /autocritica, /autocritica N, /autocritica --dry.
---

# /autocritica

Gatilhos: `/autocritica` · `/autocritica <N>` · `/autocritica --dry` · usado por `/loop /autocritica`

Wrapper **não-interativo** e **capped** do `/critica`. Mesma maquinaria, mesmo conservadorismo doutrinário — a única diferença é que **não há gate humano de confirmação** (o gate do Passo 2 do `/critica`): no lugar, um **cap rígido** `--limit N` por lote torna o custo previsível e pequeno. Pensado para ser invocado repetidamente por `/loop`, drenando o backlog de páginas devidas em lotes, e ocioso quando não há nada devido.

É o análogo, para a crítica semântica, do `/autolint` previsto no ROADMAP (§5/§11): loop atenuado com cap por iteração e **humano no circuito nos achados doutrinários** (que continuam diferidos a `rascunho` + ROADMAP, nunca auto-corrigidos).

Reutiliza 100% da maquinaria do `/critica` — scripts, prompts dos subagentes (`.claude/skills/critica/prompts/`) e a cola `critica_merge.py`. Leia o SKILL do `/critica` (`.claude/skills/critica/SKILL.md`) para o detalhe de cada passo; aqui só muda o gate e o pacing.

## Argumentos

- **`<N>`** — tamanho do lote (default **5**). Vira `--limit N` no scope. Cap rígido de custo (~N agentes Opus de crítica + verificação Sonnet dos achados de eixo 1/2).
- **`--dry`** — lote report-only: cria o sentinela `.dryrun` (nenhuma página é mutada) e passa `DRYRUN: true` aos subagentes. Útil para calibrar antes de gastar de verdade.
- **`--path GLOB`**, **`--status STATUS`**, **`--since YYYY-MM-DD`** — repassados ao scope quando o usuário quer recortar (ex.: `/autocritica --path 'wiki/questoes/*'`).

## Passo 1 — Escopo (cap rígido, SEM gate)

```bash
uv run python .claude/skills/critica/scripts/critica_scope.py --limit <N> --format json > /tmp/autocritica-scope.json
```

Ler o JSON. **Se `due_count == 0`**: não há nada devido — reportar "backlog vazio" e **encerrar a iteração**. Em loop, este é o sinal para dormir longo (re-checar edições novas mais tarde — ver "Uso com /loop"). Não lançar subagentes.

Se `due_count > 0`, preparar o run (carimbo via `date +%Y-%m-%d-%H%M`):

```bash
uv run python .claude/skills/critica/scripts/critica_merge.py plan --scope /tmp/autocritica-scope.json --run-dir /tmp/critica-run/<stamp>
```

Seguir. **Não pedir confirmação ao usuário** — o cap já bounda o custo. (Esta é a diferença deliberada para o `/critica` interativo.)

## Passo 2 — Sentinela de dry-run

- **Modo apply (default):** garantir que o sentinela **não** exista — o lote vai mutar de verdade.
  ```bash
  rm -f .claude/skills/critica/state/.dryrun
  ```
- **Modo `--dry`:** criar o sentinela antes dos subagentes (o `critica_apply.py` recusa qualquer escrita enquanto ele existir, independente do agente) e removê-lo ao final do Passo 4.
  ```bash
  touch .claude/skills/critica/state/.dryrun
  ```

## Passo 3 — Crítica + verificação por subagentes

Exatamente os Passos 3 e 4 do `/critica`: um subagente **Agent** (`general-purpose`, `model: opus`) por página com o prompt curto que aponta para `prompts/critica.md` (`DRYRUN: true` se `--dry`), todos na mesma mensagem; depois `critica_merge.py verify-list` e um cético (`model: sonnet`, `prompts/verificacao.md`) por achado de eixo 1/2. Subagentes não escrevem em arquivo compartilhado — só na própria página (auto-fix seguro) e no próprio arquivo de saída do run-dir.

## Passo 4 — Síntese serial (idêntica ao Passo 4 do /critica)

Tudo que toca arquivo compartilhado acontece **aqui, serial no main-session**, nunca em agente paralelo. (Em `--dry`, o sentinela bloqueia toda escrita do `critica_apply.py`; ainda assim gerar o relatório.)

### 4a. Rotear os diferidos

Cada item roteado aqui **custa uma decisão humana**: a página vira `rascunho` e abre-se um item `[ ]` no §11 que só o Gabriel fecha. Isso importa mais aqui do que no `/critica` interativo — este skill roda **em loop**, então um critério frouxo enche a fila dele lote após lote, sem que ninguém veja acontecer. Não existe eixo 4: tags e wikilinks são lint (`check_unlinked_concept_mention`, `check_tag_coverage`), grátis e em todo push.

Executar os comandos `set-status` / `divergencia-stub` / `roadmap-append` exatamente como no Passo 5a do `/critica`, para cada finding com `disposition: "deferred"`. Itens `"dropped"` não geram ação.

### 4b. Montar o findings JSON e renderizar o relatório
```bash
uv run python .claude/skills/critica/scripts/critica_merge.py merge --run-dir /tmp/critica-run/<stamp> \
  --scope-flags "--limit <N> <recortes>" --out /tmp/autocritica-findings.json [--dry]
uv run python .claude/skills/critica/scripts/critica_report.py --from /tmp/autocritica-findings.json
```
(`pages_due` sai do manifest do `plan`; páginas cujo subagente não gravou saída entram como puladas e continuam devidas.)

`reports/` é versionado mas fora do build público; o relatório entra no repo no `/ship` seguinte.

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
- **Conservadorismo doutrinário.** Na dúvida entre auto-corrigir e diferir, diferir (rascunho + ROADMAP) — nunca auto-corrigir sentido. Citação de autor complementar (qmd) **sempre** difere. (Imposto pelo prompt do subagente.)
- **Diferir em loop é o que transforma automação em dívida humana.** Na dúvida entre diferir e **não reportar**, não reporte o que não muda o que a página *afirma*. Polimento não é achado.
- **Kardec prevalece.** Divergência vira stub `status: aberta`, nunca apagada.
- **Sem escrita compartilhada em paralelo.** log.md, ROADMAP.md, state e relatório só no Passo 4 serial no main-session.
- **Humano no circuito.** Páginas diferidas viram `rascunho`; o usuário revisa o relatório + ROADMAP antes de promover de volta a `ativo`.
- **`uv run python`** para todo script local (ver `rules/scripts.md`).
