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

Skills cobrem `/ingest`, `/lint`, `/critica`, `/slides`, `/stats`, `/glossario`, `/ship`, `/yt`, `/yt-bulk` (autocontidos em `.claude/skills/`). `/critica` é a camada **semântica** que o `/lint` (mecânico) não cobre: workflow multi-agente caro que audita fidelidade doutrinária (divergências não-registradas com o Pentateuco, citações que não sustentam a afirmação, desvio editorial, tags/links) só sobre páginas recém-editadas, aplica correções seguras, difere decisões a `rascunho`+`ROADMAP.md`, e gera relatório HTML+MD em `reports/critica/` (excluído do build). Orquestração em `.claude/workflows/critica-profunda.js`; histórico em `.claude/skills/critica/state/critica-state.json`. `/yt <URL>` e `/yt-bulk <canal> --limit N` baixam transcrição + resumo de palestras do YouTube em `raw/palestras/<canal-slug>/` sem tocar `wiki/` — curadoria via `/ingest` continua manual. Build público exclui `raw/` (`quartz.config.ts` `ignorePatterns`); lint (`check_raw_excluded`) trava regressão. Auto-link de citações e glossário cultural rodam no CI sobre cópia em `/tmp/quartz/content` — source markdown não é alterado.

**Para responder dúvidas doutrinárias**: buscar com `qmd` (coleções `wiki` e `raw`, sempre com `intent`, combinando `lex` + `vec`); citar começando por Jesus/Pentateuco; capitalizar a resposta em página citável (`wiki/sinteses/` para panoramas, `wiki/aprofundamentos/` para estudo sistemático, `wiki/questoes/` para Q&A ancorada em uma única questão/item) e listar em `wiki/sinteses/catalogo.md` + `log.md`. Pular só quando a pergunta for puramente operacional.

## 5. Regras condicionais e hooks

`.claude/rules/*.md` são injetadas via hook `PreToolUse` (`.claude/hooks/inject-rules.py`) quando o `paths:` do frontmatter bate com o arquivo de Edit/Write/MultiEdit. Listar com `ls .claude/rules/`. Mover detalhe editorial para uma rule é a forma de manter este CLAUDE.md enxuto.

Hook `PostToolUse` (`.claude/hooks/lint-on-edit.py`) roda `lint_wiki.py --file` após cada Edit/Write/MultiEdit em `wiki/**/*.md` e surfa erros/warnings de frontmatter, taxonomia de tags e wikilinks quebrados no momento da edição. Não bloqueia; complementa (não substitui) o `/lint` global.