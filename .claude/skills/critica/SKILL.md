---
name: critica
description: Crítica doutrinária PROFUNDA das páginas recém-editadas da wiki IsAbel — multi-agente, caro em tokens, complementa o /lint. Audita 3 eixos (divergências não-registradas com o Pentateuco, citações que não sustentam a afirmação, desvio editorial), aplica correções seguras e difere decisões doutrinárias a revisão humana. Gera relatório HTML+Markdown. Use com /critica, "crítica profunda", "auditar fidelidade da wiki".
---

# /critica

Gatilhos: `/critica` · "crítica profunda" · "auditar fidelidade doutrinária"

Camada **semântica** que o `/lint` não cobre: o lint pega erro mecânico (locus inexistente, tag fora da taxonomia, link quebrado); a `/critica` pergunta *o trecho citado sustenta a afirmação?* e *há divergência com o Pentateuco que ninguém registrou?*. É **cara** (multi-agente, leitura profunda + verificação adversarial) → rodar com pouca frequência, só sobre páginas recém-editadas. Histórico em `.claude/skills/critica/state/critica-state.json` evita re-avaliar páginas inalteradas.

## Passo 1 — Levantar o escopo

```bash
uv run python .claude/skills/critica/scripts/critica_scope.py --format summary
```

Sem argumentos, lista as páginas **devidas** (nunca criticadas, ou com corpo alterado, ou `atualizado_em` posterior à última crítica). Flags: `--limit N`, `--path GLOB`, `--status ativo`, `--since YYYY-MM-DD`, `--all`. Traduzir pedidos do usuário ("só conceitos", "as 10 mais antigas") para as flags.

## Passo 2 — Estimar custo e CONFIRMAR

Mostrar ao usuário quantas páginas estão devidas e pedir confirmação **antes de gastar tokens** (a crítica é cara). Estimativa grosseira: 1 subagente Opus por página + 1 cético Sonnet por achado de eixo 1/2 (tipicamente 0–3 por página). Se forem muitas (>~15), sugerir `--limit` ou recorte por `--path`. Não prosseguir sem o aval do usuário sobre o tamanho do lote.

Capturar o conjunto final em JSON e preparar o diretório do run (carimbo via `date +%Y-%m-%d-%H%M`):

```bash
uv run python .claude/skills/critica/scripts/critica_scope.py --limit <N> > /tmp/critica-scope.json
uv run python .claude/skills/critica/scripts/critica_merge.py plan --scope /tmp/critica-scope.json --run-dir /tmp/critica-run/<stamp>
```

O `plan` imprime uma linha por página: `path  tipo  arquivo-de-saída`. Esse arquivo é o **contrato** com o subagente — o resultado é lido do disco, nunca do eco textual do agente.

Para um ensaio sem mutar nada (dry-run), criar **antes** o sentinela determinístico — o `critica_apply.py` recusa qualquer escrita enquanto ele existir, sem depender do agente — e removê-lo ao final do Passo 5:

```bash
touch .claude/skills/critica/state/.dryrun
```

## Passo 3 — Crítica: 1 subagente por página

Lançar com a tool **Agent** (`subagent_type: general-purpose`, `model: opus`), **várias chamadas na mesma mensagem** para rodarem em paralelo — lotes de até ~8; acima disso, uma mensagem por lote. O prompt de cada um é curto; as instruções completas estão versionadas em `prompts/critica.md`:

```
Leia .claude/skills/critica/prompts/critica.md e siga-o à risca.
PÁGINA: <path>
TIPO: <tipo>
SAÍDA: <arquivo-de-saída do plan>
DRYRUN: <true|false>
```

Cada subagente lê a página, monta o dossiê (`cite.py`, qmd, lint, `data/terminologia.json`), critica os 3 eixos, aplica **só** correções seguras na própria página via `critica_apply.py replace-text` e grava `{path, tipo, summary, applied[], deferred[]}` em `SAÍDA`. Não toca arquivo compartilhado.

## Passo 4 — Verificação adversarial: 1 cético por achado de eixo 1/2

```bash
uv run python .claude/skills/critica/scripts/critica_merge.py verify-list --run-dir /tmp/critica-run/<stamp>
```

Devolve `verify[]` (achados de eixo 1/2 ainda sem veredito, cada um com `critica`, `indice`, `lente`, `saida`) e `missing_critique[]` (páginas cujo agente não gravou saída — relançar uma vez; se falhar de novo, seguir sem ela: a página fica de fora do `record` e continua devida).

Para cada item de `verify`, lançar um cético com **Agent** (`subagent_type: general-purpose`, `model: sonnet`), todos na mesma mensagem:

```
Leia .claude/skills/critica/prompts/verificacao.md e siga-o à risca.
CRÍTICA: <critica>
ÍNDICE: <indice>
LENTE: <lente>
SAÍDA: <saida>
```

Eixo 3 não passa por cético (vai direto a diferir). A regra de descarte é código, no `merge`: `refuted` → `dropped`; `confirmed`, `uncertain` ou veredito ausente → `deferred`. `verify-list` pula o que já tem veredito, então rodar de novo é retomada segura.

Se o `verify-list` vier vazio, pular direto ao Passo 5.

## Passo 5 — Síntese (escritas compartilhadas, SERIAL no main-session)

Tudo que toca arquivo compartilhado acontece **aqui**, serial, nunca em subagente. Primeiro, montar o findings JSON (schema do `critica_report.py`):

```bash
uv run python .claude/skills/critica/scripts/critica_merge.py merge --run-dir /tmp/critica-run/<stamp> \
  --scope-flags "<flags usadas>" --out /tmp/critica-findings.json [--dry]
```

Imprime a contagem (páginas, auto, diferidos, descartados, puladas). Os achados a rotear são os de `findings[]` com `disposition: "deferred"` — trazem `divergencia_slug`, `kardec_pos/cite`, `outra_pos/cite` e `proposta` vindos do subagente.

### 5a. Rotear os diferidos

Cada item roteado aqui **custa uma decisão sua**: a página vira `rascunho` (o site passa a estampar o aviso do `DraftNotice`) e abre-se um item `[ ]` no §11 que só você fecha. Essa fila é o gargalo do projeto — trate-a como recurso escasso.

Para cada finding com `disposition: "deferred"` (itens `"dropped"` foram refutados pela verificação — ignorar, entram no relatório só como descartados). Em dry-run o sentinela recusa estas escritas — pular o 5a:
1. Marcar a página como rascunho:
   ```bash
   uv run python .claude/skills/critica/scripts/critica_apply.py set-status --path <page> --status rascunho
   ```
2. Eixo 1 (divergência) — criar o stub de divergência (`status: aberta`):
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
Itens com `disposition: "dropped"` (verificação refutou) **não** geram ação — entram no relatório como descartados.

### 5b. Renderizar o relatório

```bash
uv run python .claude/skills/critica/scripts/critica_report.py --from /tmp/critica-findings.json
```

Imprime os caminhos `reports/critica/<timestamp>/report.{md,html}`. Mostrar ao usuário o resumo e o caminho do HTML.

### 5c. Registrar o estado (histórico)
**Pular em dry-run** (nada foi aplicado; registrar mentiria o estado). Recomputa o hash do corpo ATUAL de cada página criticada (já com auto-fixes) e grava a data:

```bash
uv run python .claude/skills/critica/scripts/critica_scope.py record --from /tmp/critica-findings.json
```

(`record` aceita o mesmo JSON; usa `pages[].path/verdict/findings_count/deferred_count`.)

### 5d. Atualizar log.md (condicional)
Só se houve mudança ou diferimento (run 100% limpo **não** é logado, espelhando `/lint`):

```
## [YYYY-MM-DD] critica | Crítica profunda — N páginas (X auto-fixes, Y diferidos)
<2–3 frases: o que foi auto-corrigido, o que foi diferido (com link ROADMAP §11), quantos falsos-positivos a verificação descartou. Caminho do relatório.>
```

### 5e. (dry-run apenas) Remover o sentinela
```bash
rm -f .claude/skills/critica/state/.dryrun
```

## Regras

- **Conservadorismo doutrinário.** Na dúvida entre auto-corrigir e diferir, diferir (rascunho + ROADMAP) — nunca auto-corrigir sentido. Correção de citação só quando `cite.py` prova o locus; citação de autor complementar (qmd) **sempre** difere.
- **Mas diferir também tem custo.** Cada diferido consome uma decisão humana, e a fila do §11 é o gargalo do projeto. Na dúvida entre diferir e **não reportar**, não reporte o que não muda o que a página *afirma*.
- **Só o que exige juízo semântico entra aqui.** Tag e wikilink saíram para o lint (`check_unlinked_concept_mention`, `check_tag_coverage`) — grátis, em todo push. Gastar Opus para derivar o que um grep resolve, e ainda mandar o resultado para a fila humana, era o pior dos dois mundos. Ver o princípio das 3 camadas no ROADMAP §5.
- **Kardec prevalece.** Divergência é registrada (stub `status: aberta`), nunca apagada.
- **Sem escrita compartilhada em paralelo.** log.md, ROADMAP.md, state e relatório só no Passo 5 serial. Subagentes só escrevem na própria página (auto-fix seguro) e no próprio arquivo de saída.
- **Humano no circuito.** Páginas diferidas viram `rascunho`; o usuário revisa o relatório e o ROADMAP antes de promover de volta a `ativo`.
- **Orçamento de subagente é rounds × contexto.** Os prompts pedem chamadas agrupadas; não relançar um agente inteiro por um achado — só o que o `verify-list`/`missing_critique` apontar.
- Em dry-run, nenhum arquivo é mutado — útil para calibrar o escopo antes do gasto real.
