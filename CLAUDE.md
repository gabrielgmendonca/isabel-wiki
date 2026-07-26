# IsAbel — Wiki Espírita

Idioma: **PT-BR** em todas as páginas geradas. Usar sempre **kardecista** (nunca "kardequista") em todo conteúdo — páginas, commits, respostas.

## 1. Propósito e tom

Base de conhecimento pessoal sobre a Doutrina Espírita codificada por Allan Kardec. Uso: estudos e preparação de palestras em casas espíritas. Tom: estudante kardecista sério — respeitoso, fraterno, didático. Sem ironia, relativismo acadêmico distanciado ou devocionalismo excessivo.

**Princípio de crescimento**: cada pergunta doutrinária é oportunidade de capitalizar conhecimento — transformar resposta efêmera em página citável. Default é arquivar; só não arquivar quando o conteúdo for claramente operacional ou efêmero.

## 2. Hierarquia de autoridade

| Nível | Fontes |
|-------|--------|
| **Primordial** | Ensinamentos morais de Jesus (Evangelhos canônicos), lidos à luz do Pentateuco |
| **1 — Pentateuco** | LE, LM, ESE, C&I, Gênese |
| **2 — Kardec complementar** | OPE, OQE, Revista Espírita, Viagem Espírita em 1862 |
| **3 — Consagrados** | Chico Xavier, Divaldo, Léon Denis, Gabriel Delanne, Yvonne Pereira, Cairbar, Peralva, Eurípedes, Emmanuel, André Luiz, Joanna de Ângelis, Bezerra; apóstolos seletivamente citados por Kardec |
| **4 — Secundários** | Hammed/Espírito Santo Neto, palestras isoladas — citar com consciência do nível |
| **Pesquisa psíquica** | Camille Flammarion, Ernesto Bozzano e demais pesquisadores da fenomenologia — corroboração experimental dos fatos, **sem** autoridade doutrinária sobre o Pentateuco; ingerir com essa ressalva explícita |
| **Fora de escopo** | Umbanda, Candomblé, Ramatís, teosofia, antroposofia, ocultismo, neoespiritismo que relativiza o Pentateuco — **não ingerir sem confirmação explícita** |

Regra de ouro: quando nível 2/3/4 contradiz o nível 1, Kardec prevalece. A divergência é registrada, nunca apagada. Análise completa e tratamento de divergências evangélicas em [[wiki/sinteses/hierarquia-de-autoridade]] (e em `regra-divergencia.md` quando for editar `wiki/**`).

**Caso editorial — Waldo Vieira**: autor aceito na wiki (allowlist; curadoria seletiva das obras em parceria com Chico Xavier), mas **não** classificá-lo como "consagrado" (nível 3) — afastou-se da Doutrina. Tratá-lo como autor encarnado legítimo das obras curadas, sem editorializar a trajetória pessoal; divergência doutrinária nas obras vira `> [!warning]` factual, sem condenação.

## 3. Citação obrigatória

Toda afirmação doutrinária precisa de citação. Formatos:

- `(LE, q. 150)` · `(LE, Introdução, item IV)` · `(LM, 2ª parte, cap. XX, item 230)`
- `(ESE, cap. XVII, item 4)` · `(C&I, 1ª parte, cap. VI)` · `(Gênese, cap. XI, item 13)`
- `(RE, jan/1858, p. 12)` · `(OPE, "Manifestações dos Espíritos")`
- `(Emmanuel / Chico Xavier, *O Consolador*, q. 123)` · `(Léon Denis, *O Problema do Ser*, cap. IV)`

**Obras psicografadas**: citar como `Autor espiritual / Médium`. Conferir o frontmatter de `raw/mediuns/<médium>/<obra>.md` (campo `Autor espiritual:`) — o médium não é o autor. Não inferir autor a partir do médium.

**Verificação de citação do Pentateuco**: antes de afirmar `(LE, q. N)`, `(ESE, cap. X, item Y)` etc., rodar `uv run python scripts/cite.py <SIGLA> "<ref>"` para confirmar o texto literal — detalhes em `verificacao-citacao.md` (dispara em `wiki/**`).

Toda página termina com `## Fontes`. Convenções editoriais granularizadas em três rules condicionais: `convencoes-frontmatter.md` (frontmatter, links, estrutura por tipo) e `convencoes-tags.md` (taxonomia dos 5 namespaces) carregam em `wiki/**`; `convencoes-direitos.md` (schema `direitos:`, detentores, limites de citação) carrega em `wiki/obras/**`.

## 4. Workflows e estudo

Skills cobrem `/ingest`, `/lint`, `/critica`, `/autocritica`, `/dreno`, `/palestra`, `/slides`, `/stats`, `/glossario`, `/ship`, `/yt`, `/yt-bulk` (autocontidos em `.claude/skills/`) — o roster é verificado por `check_skills_consistency`, não removê-lo. **Princípio das 3 camadas** (ROADMAP §5) — governa toda automação daqui: **camada 0 (código)** = `lint_wiki.py` no CI, todo push, grátis; **camada 1 (LLM)** = `/critica`, em lotes, cara; **camada 2 (humano)** = a fila do §11, o recurso mais escasso do projeto. Todo achado deve ser *produzido* pela camada mais barata capaz de produzi-lo e *consumido* pela mais barata capaz de resolvê-lo. Ao propor automação nova, a primeira pergunta é: **isto é decidível por código?** Se for, é lint — não é prompt. (Foi assim que o "eixo 4" saiu da crítica: um agente Opus derivava "falta wikilink a [[caridade]]" e o resultado ainda virava decisão humana — duas camadas de desperdício no mesmo achado.)

`/critica` é a camada **semântica** que o `/lint` (mecânico) não cobre. **Não há eixo 4**: tags e wikilinks são lint (`check_tag_coverage`, `check_unlinked_concept_mention`). `/autocritica` é o wrapper não-interativo e capped do `/critica`, análogo-crítica do `/autolint` (ROADMAP §5/§11); commit fica a cargo do usuário via `/ship`. `/dreno` é o **contrapeso** dessa dupla: a crítica *abre* trabalho (rebaixa a `rascunho` + item no §11) a uma taxa de ~92%, então sem um passo que *feche*, o loop só acumula dívida humana. Duas invariantes travadas por teste (`tests/test_dreno.py`): **não bumpa `atualizado_em`** (bumpar devolveria a página à fila do Opus como "atualizado-apos-critica" → moto-perpétuo) e **slug ambíguo nunca promove** (bucket F — vale para `[ ]` **e** `[x]`; contar só `abertos`/`fechados` deixava o `[x]` ambíguo promover todas as homônimas). O loop diário (`scripts/loop-diario.sh` + launchd) roda a cascata grátis primeiro e só invoca o Claude se houver trabalho — dia sem trabalho custa zero token. Ele **nunca toca no working tree**: opera numa worktree dedicada resetada a `origin/main` e entrega por PR — **os dois níveis esperam revisão humana; nada automescla** (o auto-merge do nível 0 foi removido em 2026-07-14: o guarda que o justificava falhava aberto, e promover apaga do site o aviso `DraftNotice` — ver ROADMAP §5). (Push direto a main é barrado pelo ruleset "Protect main", que exige PR mas pede 0 aprovações — é a mesma regra que mantém o `stats-daily.yml` desligado.) **O loop não fecha a fila do §11** — ele só colhe o que você já decidiu; reapontá-lo para *preparar decisões* é o item ★ do ROADMAP §5. `/yt` e `/yt-bulk` não tocam `wiki/` — curadoria via `/ingest` continua manual. Build público exclui `raw/` (`quartz.config.ts` `ignorePatterns`); lint (`check_raw_excluded`) trava regressão. Auto-link de citações e glossário cultural rodam no CI sobre cópia em `/tmp/quartz/content` — source markdown não é alterado.

**Para responder dúvidas doutrinárias**: buscar com `qmd` (coleções `wiki` e `raw`, sempre com `intent`, combinando `lex` + `vec`); citar começando por Jesus/Pentateuco; capitalizar a resposta em página citável (`wiki/sinteses/` para panoramas, `wiki/aprofundamentos/` para estudo sistemático, `wiki/questoes/` para Q&A ancorada em uma única questão/item) e listar em `wiki/sinteses/catalogo.md` + `log.md`. Pular só quando a pergunta for puramente operacional.

## 5. Regras condicionais e hooks

`.claude/rules/*.md` são injetadas via hook `PreToolUse` (`.claude/hooks/inject-rules.py`) quando o `paths:` do frontmatter bate com o arquivo de Edit/Write/MultiEdit. Listar com `ls .claude/rules/`. Mover detalhe editorial para uma rule é a forma de manter este CLAUDE.md enxuto.

Hook `PostToolUse` (`.claude/hooks/lint-on-edit.py`) roda `lint_wiki.py --file` após cada Edit/Write/MultiEdit em `wiki/**/*.md` e surfa erros/warnings de frontmatter, taxonomia de tags e wikilinks quebrados no momento da edição. Não bloqueia; complementa (não substitui) o `/lint` global.