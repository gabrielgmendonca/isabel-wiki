---
name: critica
description: Crítica doutrinária PROFUNDA das páginas recém-editadas da wiki IsAbel — multi-agente, caro em tokens, complementa o /lint. Audita 4 eixos (divergências não-registradas com o Pentateuco, citações que não sustentam a afirmação, desvio editorial, tags/cross-references), aplica correções seguras e difere decisões doutrinárias a revisão humana. Gera relatório HTML+Markdown. Use com /critica, "crítica profunda", "auditar fidelidade da wiki".
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

Mostrar ao usuário quantas páginas estão devidas e pedir confirmação **antes de gastar tokens** (a crítica é cara). Estimativa grosseira: ~2–4 chamadas de agente por página (1 crítica + 1–3 verificações de achados high-stakes). Se forem muitas (>~15), sugerir `--limit` ou recorte por `--path`. Não prosseguir sem o aval do usuário sobre o tamanho do lote.

Capturar o conjunto final em JSON (será passado ao workflow):

```bash
uv run python .claude/skills/critica/scripts/critica_scope.py --limit <N> > /tmp/critica-scope.json
```

## Passo 3 — Rodar o workflow

Invocar a tool **Workflow** com o script salvo e os argumentos. Ler `/tmp/critica-scope.json` e passar seu campo `pages` como `args.pages`:

- `name`: `critica-profunda` (script em `.claude/workflows/critica-profunda.js`)
- `args`: `{ "pages": <array pages do scope JSON>, "dryRun": <bool>, "terminologiaPath": "data/terminologia.json" }`

Para um ensaio sem mutar nada, passar `"dryRun": true`. **Antes** de invocar o workflow em dryRun, criar o sentinela determinístico (o `critica_apply.py` recusa qualquer escrita enquanto ele existir — não depende do agente honrar o dryRun):

```bash
touch .claude/skills/critica/state/.dryrun
```

E **removê-lo ao final** do run dryRun:

```bash
rm -f .claude/skills/critica/state/.dryrun
```

O workflow roda um pipeline por página: **Crítica** (1 agente Opus por página — monta o dossiê com `cite.py`/qmd, critica os 4 eixos, aplica só correções seguras na própria página) → **Verificação** (céticos Sonnet adversariais por achado de eixo 1/2, para matar falso-positivo). Ele **não** escreve em arquivos compartilhados — retorna `{ pages: [...] }`, cada página com `applied[]` (correções seguras já aplicadas) e `deferred[]` (achados de qualquer eixo que exigem decisão humana; cada um com `disposition: "deferred"` ou `"dropped"` — `dropped` = a verificação adversarial refutou, ignorar).

## Passo 4 — Síntese (escritas compartilhadas, SERIAL no main-session)

Tudo que toca arquivo compartilhado acontece **aqui**, serial, nunca em agente paralelo. A partir do retorno do workflow:

### 4a. Rotear os diferidos
Para cada página, para cada item em `deferred` com `disposition: "deferred"` (itens `"dropped"` foram refutados pela verificação — ignorar, entram no relatório só como descartados):
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

### 4b. Montar o findings JSON e renderizar o relatório
Construir o JSON no schema de `critica_report.py` (run + pages + findings, cada finding com `disposition` ∈ `auto_fixed|deferred|dropped`). Gravar em `/tmp/critica-findings.json`. Carimbo do run via `date +%Y-%m-%d-%H%M`. Então:

```bash
uv run python .claude/skills/critica/scripts/critica_report.py --from /tmp/critica-findings.json
```

Imprime os caminhos `reports/critica/<timestamp>/report.{md,html}`. Mostrar ao usuário o resumo e o caminho do HTML.

### 4c. Registrar o estado (histórico)
Recomputa o hash do corpo ATUAL de cada página criticada (já com auto-fixes) e grava a data:

```bash
uv run python .claude/skills/critica/scripts/critica_scope.py record --from /tmp/critica-findings.json
```

(`record` aceita o mesmo JSON; usa `pages[].path/verdict/findings_count/deferred_count`.)

### 4d. Atualizar log.md (condicional)
Só se houve mudança ou diferimento (run 100% limpo **não** é logado, espelhando `/lint`):

```
## [YYYY-MM-DD] critica | Crítica profunda — N páginas (X auto-fixes, Y diferidos)
<2–3 frases: o que foi auto-corrigido, o que foi diferido (com link ROADMAP §11), quantos falsos-positivos a verificação descartou. Caminho do relatório.>
```

## Regras

- **Conservadorismo doutrinário.** Na dúvida, diferir (rascunho + ROADMAP), nunca auto-corrigir sentido. Correção de citação só quando `cite.py` prova o locus; citação de autor complementar (qmd) **sempre** difere.
- **Kardec prevalece.** Divergência é registrada (stub `status: aberta`), nunca apagada.
- **Sem escrita compartilhada em paralelo.** log.md, ROADMAP.md, state e relatório só no Passo 4 serial.
- **Humano no circuito.** Páginas diferidas viram `rascunho`; o usuário revisa o relatório e o ROADMAP antes de promover de volta a `ativo`.
- Em `dryRun`, nenhum arquivo é mutado — útil para calibrar o escopo antes do gasto real.
