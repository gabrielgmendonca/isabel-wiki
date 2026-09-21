---
name: palestra
description: Monta um dossiê de preparação de palestra a partir de uma página da wiki IsAbel — multi-agente, com três modos de custo. Varredura Pentateuco-primeiro do corpus (wiki + raw), definição julgada de termos-chave, caça a casos/histórias com crítico, verificação de citação em lote (cite.py) e painel socrático que entrega um arco pronto para /slides. Grava o dossiê em reports/palestra/. Use com /palestra <página> [--foco "..."] [--rapido|--fundo] [--imagens], "preparar palestra sobre X", "dossiê de palestra de X".
---

# /palestra

Gatilhos: `/palestra <página-wiki> [--foco "<recorte>"] [--rapido|--fundo] [--imagens]` · "preparar palestra sobre X" · "dossiê de palestra de X"

Camada de **preparação de palestra** que o `/slides` (que gera o deck de UMA página) não cobre: faz uma varredura do corpus em torno de um tema, **começando por Jesus e pelo Pentateuco**, verifica as citações, define os termos-chave, levanta casos e histórias para contar (com crítico que mata misatribuição), e propõe um arco socrático já testado por um júri. O dossiê alimenta depois o `/slides`.

A maquinaria é o workflow `.claude/workflows/palestra-dossie.js`; esta skill é o wrapper serial (faz o trabalho de camada 0, monta `args`, invoca o workflow e grava o relatório). Nada em `wiki/` é tocado.

**Princípio de custo** (CLAUDE.md §4): o que é decidível por código roda aqui, serialmente, de graça — digest da semente, pré-busca qmd, mapa da wiki, repertório já contado. O workflow só recebe o que sobra para julgamento. Os Passos 2 a 3b abaixo **não são preparo opcional**: são o que faz o run caber no orçamento.

## Passo 1 — Resolver a página-semente, o foco e ler a semente UMA vez

O argumento é uma página existente em `wiki/` (ex.: `wiki/conceitos/bem-aventuranca-dos-misericordiosos.md`). Se vier só um tema (`/palestra indulgência`), procurar em `wiki/conceitos/`, `wiki/sinteses/`, `wiki/aprofundamentos/`, `wiki/questoes/` (via `mcp__qmd__query`, collection `wiki`). Se ambíguo, perguntar com `AskUserQuestion`.

O `--foco "<recorte>"` é opcional e dá peso central a um aspecto do tema (ex.: `--foco "a indulgência"` sobre a bem-aventurança dos misericordiosos). Sem foco, a palestra cobre o tema inteiro.

**Ler a semente aqui, uma única vez** (`Read <página>`), e extrair: obra-base e range (`fontes:` + citações), eixo doutrinário (`tema/*`), termos centrais. Disso saem `tema` e os `termosObrigatorios`.

O `seedTexto` que vai ao workflow (os agentes recebem a semente **inline** e não dão `Read` nela) sai do script — recortar digest à mão é decidível por código:

```bash
uv run python .claude/skills/palestra/scripts/seed_digest.py <página> --saida <estado>/seed.md
```

Ele devolve a página inteira até ~12.000 caracteres e, acima disso, um digest (frontmatter + headers + linhas com locus) — imprimindo no stderr o `seedTruncado` a usar. **Seções de roteiro e música vão inteiras**, mesmo sem locus: no run de 2026-09-12 o digest por locus apagou a moldura musical da semente e o dossiê saiu sem ela.

## Passo 2 — Pré-busca compartilhada (camada 0)

Rodar aqui, **serialmente**, 2-3 `mcp__qmd__query` sobre o tema/foco (uma em `["wiki"]`, uma em `["raw"]`, `lex` + `vec`, `intent` claro) e condensar os hits em uma lista compacta `caminho — snippet de uma linha`. Isso vira `preBusca`.

Sem isso, cada uma das lentes refazia por conta própria a mesma primeira rodada de busca. O prompt do workflow diz explicitamente aos agentes para partirem daqui e só consultarem o qmd para o que falta à lente deles.

## Passo 3 — Mapa da wiki (camada 0)

Montar `mapaWiki` sem gastar agente — é `grep` + qmd + a própria semente:

1. A seção "Páginas relacionadas" da semente (já lida no Passo 1).
2. Backlinks — quem já aponta para ela. Os wikilinks da wiki usam o **caminho completo** e podem ter alias (`[[wiki/conceitos/<slug>|Misericordiosos]]`), com o pipe às vezes escapado dentro de tabela, então a forma curta `[[<slug>]]` não casa com nada:

   ```bash
   grep -rlE "\[\[(wiki/[a-z-]+/)?<slug>(\\\\?\|[^]]*)?\]\]" wiki/
   ```
3. Os hits de `wiki/` da pré-busca do Passo 2.

Condensar em linhas `wiki/<tipo>/<slug> — como entra na palestra`. Quando `mapaWiki` vem preenchido, o workflow **dispensa a lente `wiki`** (exceto em `--fundo`, onde o julgamento de relevância semântica ainda vale um agente). Precedente: o run de 2026-09-04 fez esse mapa em código e o dossiê não perdeu nada.

## Passo 3b — Repertório já contado (camada 0)

```bash
uv run python .claude/skills/palestra/scripts/repertorio.py
```

Lê os decks de `slides/` e as palestras já apresentadas em `raw/palestras/gabriel-mendonca/` (`.pptx`/`.odp` direto) e devolve dois blocos, que juntos viram o arg `repertorio`:

- **Casos já contados** — cruzamento com o registro de nomes que a wiki mantém (`wiki/personalidades/`, `wiki/conceitos/parabola-*`, com `aliases:`). Vai para os finders e o crítico.
- **Ângulos já usados** — título da palestra, títulos de parte e perguntas-ponte autorais de cada deck (descarta a pergunta literal do Pentateuco e a fala de Espírito evocado, que não são autorais). Vai para o arco, como herança de estilo: é a parte do trabalho da lente de palestras que **não** exige julgamento.

O que sobra para a lente de palestras (ligada no modo default e no `--fundo`) é o que só julgamento resolve: *por que* aquele enquadramento funcionou, e o que dele serve a este tema.

**É informação, não veto.** O palestrante fala em casas diferentes e recontar um bom caso é legítimo — o dossiê anota *"já contado em \<deck\>"* e a decisão é dele. O que se evita é a surpresa: no run de 2026-09-12 o arco propôs a rainha de Oude + Szymel Slizgol sem saber que eram o miolo narrativo de `orgulho-e-humildade.pptx`.

## Passo 4 — (Opcional) Logística da palestra

Se o usuário já vai querer o arco calibrado para uma ocasião, coletar via `AskUserQuestion` (não bloquear o dossiê por isso — são opcionais): **data** (YYYY-MM-DD, nunca a data atual), **casa espírita**, **público** (iniciantes / regulares / evangelizadores / misto). Default de público: `misto`. Esses campos só afetam o ângulo do arco socrático.

## Passo 5 — Escolher o modo e CONFIRMAR

Três modos. Anunciar o número **real** de agentes antes de gastar e pedir o aval:

| Modo | Agentes | Composição | Quando |
|------|---------|-----------|--------|
| `--rapido` | **~12** (medido) | 3 lentes, 1 finder, 1 arco sem júri, sem imagens; Sonnet fora do núcleo/arco/síntese | explorar um tema, primeira passada, palestra curta |
| *(default)* | **~15-16** | 4 lentes, 2 finders, 3 arcos + júri, sem imagens; Opus só em núcleo/arcos/júri/síntese | o caso normal |
| `--fundo` | **~19-21** | 5 lentes (inclui a lente wiki), 2 passadas de verificação, imagens ligadas, tudo no modelo da sessão | a palestra que importa de verdade |

`--imagens` liga a iconografia fora do `--fundo` (custa ~1 agente por 3 momentos-chave). Ela vem **desligada** por default: é o estágio mais caro por agente (WebFetch de páginas de acervo) e a colocação no deck segue manual (ROADMAP §7) — pagava-se o mais caro para gerar sugestão que o humano revisa à mão de todo jeito.

**Calibração medida** (soma do `usage` por chamada de API nos transcripts dos subagentes):

| Run | Agentes | Tokens |
|-----|---------|--------|
| 2026-06-14, antes da economia | 49 (19 Opus) | não medido |
| 2026-09-04, default | 18 (8 morreram em 429) | 24,6M em subagentes + 11,3M no main-session |
| 2026-09-12, `--rapido` | 12 | **14,1M** (+5,9M perdidos em 429) |

O custo é ~linear no **número de rounds de tool-call**, não no modelo: naquele run a lente de tensões (Sonnet, 27 rounds) custou 2,8M e o arco (Opus, 4 rounds) custou 0,27M. Daí o teto de exploração no prompt das lentes e o `cite.py` em lote. Se o usuário pedir "vá fundo", é `--fundo` — não é voltar ao comportamento de junho.

## Passo 6 — Rodar o workflow

Invocar a tool **Workflow**:

- `name`: `palestra-dossie` (script em `.claude/workflows/palestra-dossie.js`)
- `args`: `{ "seedPath": "<página>", "seedTexto": "<conteúdo ou digest>", "seedTruncado": false, "preBusca": "<lista do Passo 2>", "mapaWiki": "<lista do Passo 3>", "repertorio": "<lista do Passo 3b>", "foco": "<recorte ou ''>", "termosObrigatorios": ["<termo>", ...], "tema": "tema/<x>", "data": "<YYYY-MM-DD ou ''>", "casa": "<nome ou ''>", "publico": "<iniciantes|regulares|evangelizadores|misto>", "modo": "<rapido|normal|fundo>", "imagens": "<off|momentos-chave|casos|quase-todos>", "permitirIA": false }`

> **Se a tool `Workflow` não existir nesta sessão** (foi o caso em 2026-09-04 e 2026-09-12 — conferir antes de montar o run), **não orquestre à mão**: use o executor versionado, que roda o mesmo `palestra-dossie.js` e só troca a função `agent()`.
>
> ```bash
> # grave os args acima em <estado>/args.json, depois:
> node .claude/skills/palestra/scripts/run_workflow.mjs --args <estado>/args.json
> ```
>
> Ele avança até o próximo estágio e para, listando os agentes pendentes com **prompt, modelo e o caminho do JSON a gravar**. Despachar cada um como subagente (`general-purpose`, `model: sonnet` quando o pendente disser `model=sonnet`; envelope curto mandando ler o prompt, executá-lo e gravar o JSON no caminho indicado), depois rodar o comando de novo. Repetir até `CONCLUÍDO`.
>
> O estado fica em disco, então **um 429 no meio de um estágio custa relançar só os agentes que faltaram** — não o run inteiro. Use `<estado>` dentro de `reports/palestra/` (nunca `/tmp`, que é limpo entre sessões). `--stub` roda a orquestração inteira com fixtures, sem gastar token — é o smoke test depois de mexer no workflow.

`imagens` controla a cobertura do estágio **Iconografia** (`off` é o default fora do `--fundo`). `permitirIA` (default `false`) libera geração por IA **só para imagem atmosférica/abstrata** — nunca figura sagrada (ver `convencoes-imagens.md`). O estágio busca arte em **domínio público/CC** (Doré, Tissot, Wikimedia…) e sai na seção "Sugestões de imagem" do dossiê — **propõe, não baixa**; a colocação é no `/slides`.

Estágios: **Varredura** (3-5 lentes paralelas conforme o modo) + **Termos** + **Casos** (1-2 finders) → **Crítica de casos** → **Verificação** (cite.py em lote: um laço Bash por lote de ~10 loci, depois o julgamento semântico) → **Arco socrático** (1 arco, ou painel de 3 + júri) → **Iconografia** (em lotes de 3 momentos, quando ligada) → **Síntese**. Retorna `{ meta: { modo, agentes, ... }, dossie: { markdown, resumo_executivo, lacunas, paginas_a_criar }, detalhe: {...} }`.

## Passo 7 — Gravar o dossiê (serial, no main-session)

A escrita acontece **aqui** (workflows não escrevem em disco).

1. Carimbar o run: `date +%Y-%m-%d-%H%M`. Slug da semente: o basename sem `.md`.
2. Criar `reports/palestra/<slug>-<timestamp>/` — que é também o `<estado>` do Passo 6 (o subdiretório `estado/` é gitignored; o dossiê, não) — e gravar:
   - `dossie.md` ← campo `dossie.markdown`.
   - `dados.json` ← `meta` + o `detalhe` completo (rastreabilidade: o que cada lente achou, vereditos dos casos, vereditos de verificação, scores do júri).
3. `reports/` está em `ignorePatterns` do `quartz.config.ts` — o dossiê fica **fora do build** (não vaza para a wiki pública), como os relatórios de `/critica`.

## Passo 8 — Reportar ao usuário

- Caminho do `reports/palestra/<slug>-<timestamp>/dossie.md`.
- O `resumo_executivo` e o **arco socrático sugerido** (que vira input do `/slides`).
- **O custo real**: `meta.modo` e `meta.agentes` — o que o run de fato gastou, não a estimativa de bula.
- As **lacunas** e **páginas a criar** (princípio de crescimento, CLAUDE.md §1) — oferecer capitalizar via `/ingest`/edição da wiki, ou registrar no `ROADMAP.md`.
- Quaisquer citações marcadas `⚠ uncertain/refuted` na verificação — pontos a conferir antes de subir ao palco.

## Regras

- **Pentateuco primeiro.** O dossiê ancora em Jesus e no Pentateuco; níveis 2/3/4 entram com ressalva de nível; pesquisa psíquica (Flammarion/Bozzano) é corroboração fatual sem autoridade doutrinária. Divergência é registrada, nunca apagada (CLAUDE.md §2).
- **Citação verificada.** Toda citação do Pentateuco passa por `cite.py`. O dossiê só usa as `confirmed`; marca `uncertain`/`refuted` com ⚠. O `cite.py` resolve o LE até a q. 1019 (as finais em numeração dupla "Kardec [sequencial]"); a q. 1011 não existe porque Kardec saltou o número, e o `cite.py` explica isso no erro — citação a q. 1011 é fabricada, não lacuna de corpus.
- **Camada mais barata que resolva.** Semente (`seed_digest.py`), pré-busca, mapa da wiki e repertório (`repertorio.py`) são camada 0 e ficam nesta skill; o workflow só recebe o que exige julgamento. Ao acrescentar estágio novo, a primeira pergunta é se ele é decidível por código.
- **Casos sem misatribuição.** O crítico reprova caso mal-atribuído (autor espiritual ≠ médium; parábola atribuída ao evangelho errado) — não contar caso que o crítico não aprovou.
- **Caso repetido não é veto.** O `repertorio` só anota *"já contado em \<deck\>"*. O palestrante fala em casas diferentes e recontar um bom caso é legítimo — a escolha é dele, e nem o finder nem o crítico devem rebaixar um caso por isso.
- **Verificação cobre o que o dossiê imprime.** Os loci não vêm só do núcleo: as lentes complementares e os casos também produzem citação do Pentateuco (no campo livre `fonte`), e o workflow os extrai para o mesmo lote de `cite.py`. Locus que escapar disso entra no dossiê marcado como não-conferido — nunca como se estivesse verificado.
- **Não toca `wiki/` nem publica.** O dossiê é artefato de trabalho em `reports/palestra/` (fora do build). Capitalizar conteúdo na wiki é passo manual posterior (`/ingest`, edição), não automático.
- **Termos: doutrinário ≠ cultural.** A definição doutrinária (Kardec/wiki, com locus) e a glosa cultural (`data/dicionario.json`) são registros distintos — o dossiê os mantém separados.
- **Alimenta o `/slides`.** O arco socrático do dossiê é desenhado para virar deck: mesmos critérios de pergunta-ponte (A/B/C) de `convencoes-perguntas-socraticas.md`.
