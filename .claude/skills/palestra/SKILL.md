---
name: palestra
description: Monta um dossiê de preparação de palestra a partir de uma página da wiki IsAbel — multi-agente, caro em tokens. Varredura Pentateuco-primeiro do corpus (wiki + raw), definição julgada de termos-chave, caça a casos/histórias com crítico, verificação adversarial de citação (cite.py) e painel socrático que entrega um arco pronto para /slides. Grava o dossiê em reports/palestra/. Use com /palestra <página> [--foco "..."], "preparar palestra sobre X", "dossiê de palestra de X".
---

# /palestra

Gatilhos: `/palestra <página-wiki> [--foco "<recorte>"]` · "preparar palestra sobre X" · "dossiê de palestra de X"

Camada de **preparação de palestra** que o `/slides` (que gera o deck de UMA página) não cobre: faz uma varredura exaustiva do corpus em torno de um tema, **começando por Jesus e pelo Pentateuco**, verifica cada citação adversarialmente, define os termos-chave, levanta casos e histórias para contar (com crítico que mata misatribuição), e propõe um arco socrático já testado por um júri. É **cara** (multi-agente, leitura profunda + verificação) → rodar sob demanda quando se vai preparar uma palestra de verdade, não em loop. O dossiê alimenta depois o `/slides`.

A maquinaria é o workflow `.claude/workflows/palestra-dossie.js`; esta skill é o wrapper serial (lê a semente, monta `args`, invoca o workflow e grava o relatório). Nada em `wiki/` é tocado.

## Passo 1 — Resolver a página-semente e o foco

O argumento é uma página existente em `wiki/` (ex.: `wiki/conceitos/bem-aventuranca-dos-misericordiosos.md`). Se vier só um tema (`/palestra indulgência`), procurar em `wiki/conceitos/`, `wiki/sinteses/`, `wiki/aprofundamentos/`, `wiki/questoes/` (via `mcp__qmd__query`, collection `wiki`). Se ambíguo, perguntar com `AskUserQuestion`.

O `--foco "<recorte>"` é opcional e dá peso central a um aspecto do tema (ex.: `--foco "a indulgência"` sobre a bem-aventurança dos misericordiosos). Sem foco, a palestra cobre o tema inteiro.

**Ler a semente** (`Read <página>`) para extrair: obra-base e range (`fontes:` + citações), eixo doutrinário (`tema/*`), e os termos centrais. Disso saem `tema` e os `termosObrigatorios` (os termos que o usuário pediu explicitamente para definir, se houver — o workflow ainda julga necessidade e pode acrescentar outros).

## Passo 2 — (Opcional) Logística da palestra

Se o usuário já vai querer o arco calibrado para uma ocasião, coletar via `AskUserQuestion` (não bloquear o dossiê por isso — são opcionais): **data** (YYYY-MM-DD, nunca a data atual), **casa espírita**, **público** (iniciantes / regulares / evangelizadores / misto). Default de público: `misto`. Esses campos só afetam o ângulo do arco socrático.

## Passo 3 — Estimar custo e CONFIRMAR

Avisar que o run é caro **antes de gastar** (multi-agente: ~5 lentes de varredura + termos + 2 finders de casos + 1 crítico + N×verifyDepth verificações + 3 arcos + júri + síntese ≈ 15-25 chamadas de agente). Pedir o aval. Para um número grande de citações/casos, tudo bem — é o ponto do workflow; mas confirmar o tamanho com o usuário.

## Passo 4 — Rodar o workflow

Invocar a tool **Workflow**:

- `name`: `palestra-dossie` (script em `.claude/workflows/palestra-dossie.js`)
- `args`: `{ "seedPath": "<página>", "foco": "<recorte ou ''>", "termosObrigatorios": ["<termo>", ...], "tema": "tema/<x>", "data": "<YYYY-MM-DD ou ''>", "casa": "<nome ou ''>", "publico": "<iniciantes|regulares|evangelizadores|misto>", "imagens": "momentos-chave", "permitirIA": false }`

`imagens` controla a cobertura do estágio **Iconografia** (`momentos-chave` = abertura+casos+síntese; `casos`; `quase-todos`; `off`). `permitirIA` (default `false`) libera geração por IA **só para imagem atmosférica/abstrata** — nunca figura sagrada (ver `convencoes-imagens.md`). O estágio busca arte em **domínio público/CC** (Doré, Tissot, Wikimedia…) por momento-chave e sai na seção "Sugestões de imagem" do dossiê — **propõe, não baixa**; a colocação é no `/slides`.

Para escalar a profundidade (mais céticos por citação, pools maiores), o usuário pode prefixar o turno com um alvo de budget (`+400k`) — o workflow lê `budget.total` e sobe `verifyDepth`. Sem budget, o default já é generoso (`verifyDepth=2`).

O workflow roda os estágios: **Varredura** (5 lentes paralelas: núcleo Jesus→Pentateuco, consagrados, wiki, palestras raw, tensões) + **Termos** (definição julgada) + **Casos** (2 finders) → **Crítica de casos** (aptidão + risco de misatribuição) → **Verificação** (cético adversarial por citação do Pentateuco, via `cite.py`) → **Arco socrático** (painel de 3 ângulos + júri) → **Síntese** (montagem do dossiê + lacunas). Retorna `{ dossie: { markdown, resumo_executivo, lacunas, paginas_a_criar }, detalhe: {...} }`.

## Passo 5 — Gravar o dossiê (serial, no main-session)

A escrita acontece **aqui** (workflows não escrevem em disco).

1. Carimbar o run: `date +%Y-%m-%d-%H%M`. Slug da semente: o basename sem `.md`.
2. Criar `reports/palestra/<slug>-<timestamp>/` e gravar:
   - `dossie.md` ← campo `dossie.markdown`.
   - `dados.json` ← o `detalhe` completo (rastreabilidade: o que cada lente achou, vereditos dos casos, votos de verificação, scores do júri).
3. `reports/` está em `ignorePatterns` do `quartz.config.ts` — o dossiê fica **fora do build** (não vaza para a wiki pública), como os relatórios de `/critica`.

## Passo 6 — Reportar ao usuário

- Caminho do `reports/palestra/<slug>-<timestamp>/dossie.md`.
- O `resumo_executivo` e o **arco socrático sugerido** (que vira input do `/slides`).
- As **lacunas** e **páginas a criar** (princípio de crescimento, CLAUDE.md §1) — oferecer capitalizar via `/ingest`/edição da wiki, ou registrar no `ROADMAP.md`.
- Quaisquer citações marcadas `⚠ uncertain/refuted` na verificação — pontos a conferir antes de subir ao palco.

## Regras

- **Pentateuco primeiro.** O dossiê ancora em Jesus e no Pentateuco; níveis 2/3/4 entram com ressalva de nível; pesquisa psíquica (Flammarion/Bozzano) é corroboração fatual sem autoridade doutrinária. Divergência é registrada, nunca apagada (CLAUDE.md §2).
- **Citação verificada.** Toda citação do Pentateuco passa por `cite.py` (verificação adversarial). O dossiê só usa as `confirmed`; marca `uncertain`/`refuted` com ⚠.
- **Casos sem misatribuição.** O crítico reprova caso mal-atribuído (autor espiritual ≠ médium; parábola atribuída ao evangelho errado) — não contar caso que o crítico não aprovou.
- **Não toca `wiki/` nem publica.** O dossiê é artefato de trabalho em `reports/palestra/` (fora do build). Capitalizar conteúdo na wiki é passo manual posterior (`/ingest`, edição), não automático.
- **Termos: doutrinário ≠ cultural.** A definição doutrinária (Kardec/wiki, com locus) e a glosa cultural (`data/dicionario.json`) são registros distintos — o dossiê os mantém separados.
- **Alimenta o `/slides`.** O arco socrático do dossiê é desenhado para virar deck: mesmos critérios de pergunta-ponte (A/B/C) de `convencoes-perguntas-socraticas.md`.
