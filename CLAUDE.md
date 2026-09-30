# IsAbel — Wiki Espírita

Idioma: **PT-BR** em todas as páginas. Sempre **kardecista** (nunca "kardequista") em páginas, commits e respostas.

## 1. Propósito e tom

Base de conhecimento pessoal sobre a Doutrina Espírita codificada por Allan Kardec, para estudo e preparação de palestras em casas espíritas. Tom de estudante kardecista sério: respeitoso, fraterno, didático. Sem ironia, relativismo acadêmico distanciado nem devocionalismo excessivo.

**Princípio de crescimento** — capitalizar por default: toda pergunta doutrinária vira página citável — `wiki/sinteses/` (panorama), `wiki/aprofundamentos/` (estudo sistemático), `wiki/questoes/` (uma única questão/item) —, registrada em `wiki/sinteses/catalogo.md` + `log.md`. Só não arquivar o que for operacional ou efêmero. Para pesquisar: `qmd` nas coleções `wiki` e `raw`, com `intent`, `lex` + `vec`; citar começando por Jesus/Pentateuco.

## 2. Hierarquia de autoridade

| Nível | Fontes |
|-------|--------|
| **Primordial** | Ensinamentos morais de Jesus (Evangelhos canônicos), lidos à luz do Pentateuco |
| **1 — Pentateuco** | LE, LM, ESE, C&I, Gênese |
| **2 — Kardec complementar** | OPE, OQE, Revista Espírita, Viagem Espírita em 1862 |
| **3 — Consagrados** | Chico Xavier, Divaldo, Léon Denis, Gabriel Delanne, Yvonne Pereira, Cairbar, Peralva, Eurípedes, Emmanuel, André Luiz, Joanna de Ângelis, Bezerra; apóstolos seletivamente citados por Kardec |
| **4 — Secundários** | Hammed/Espírito Santo Neto, palestras isoladas — citar com consciência do nível |
| **Pesquisa psíquica** | Flammarion, Bozzano e demais pesquisadores da fenomenologia — corroboração experimental, **sem** autoridade doutrinária; ingerir com essa ressalva explícita |
| **Fora de escopo** | Umbanda, Candomblé, Ramatís, teosofia, antroposofia, ocultismo, neoespiritismo que relativiza o Pentateuco — **não ingerir sem confirmação explícita** |

**Regra de ouro**: quando nível 2/3/4 contradiz o nível 1, Kardec prevalece; a divergência é registrada, nunca apagada. Análise completa em [[wiki/sinteses/hierarquia-de-autoridade]].

**Waldo Vieira**: aceito (curadoria seletiva das obras com Chico Xavier), mas **não** é nível 3 — afastou-se da Doutrina. Tratar como autor legítimo das obras curadas, sem editorializar a trajetória; divergência nas obras vira `> [!warning]` factual, sem condenação.

## 3. Citação obrigatória

Toda afirmação doutrinária tem citação. Toda página termina com `## Fontes`.

- `(LE, q. 150)` · `(LE, Introdução, item IV)` · `(LM, 2ª parte, cap. XX, item 230)`
- `(ESE, cap. XVII, item 4)` · `(C&I, 1ª parte, cap. VI)` · `(Gênese, cap. XI, item 13)`
- `(RE, jan/1858, p. 12)` · `(OPE, "Manifestações dos Espíritos")`
- `(Emmanuel / Chico Xavier, *O Consolador*, q. 123)` · `(Léon Denis, *O Problema do Ser*, cap. IV)`

**Psicografia**: `Autor espiritual / Médium`, conforme o campo `Autor espiritual:` do frontmatter em `raw/mediuns/<médium>/<obra>.md`. Nunca inferir o autor a partir do médium.

**Pentateuco**: conferir o texto com `uv run python scripts/cite.py <SIGLA> "<ref>"` antes de afirmar.

## 4. Workflows

Skills (autocontidas em `.claude/skills/`; o roster é verificado pelo lint — não remover): `/ingest`, `/lint`, `/critica`, `/autocritica`, `/dreno`, `/palestra`, `/slides`, `/stats`, `/glossario`, `/ship`, `/yt`, `/yt-bulk`.

**Princípio das 3 camadas** (ROADMAP §5): camada 0 = código (`lint_wiki.py` no CI, grátis) · camada 1 = LLM (`/critica`, cara) · camada 2 = humano (fila do ROADMAP §11, o recurso mais escasso). Cada achado deve ser produzido e resolvido pela camada mais barata capaz. **Ao propor automação: se é decidível por código, é lint, não prompt.**

- `/critica` é a camada semântica (3 eixos; tags e wikilinks são lint). `/autocritica` = lote não interativo e capped dela. `/dreno` é o contrapeso que *fecha* rascunhos — suas invariantes (e as do loop) estão na rule `dreno-loop-invariantes.md` e travadas por `tests/test_dreno.py`.
- Loop diário (`scripts/loop-diario.sh`): worktree dedicada em `origin/main`, entrega por PR, **nada automescla**; não fecha a fila do §11.
- `/yt` e `/yt-bulk` não tocam `wiki/`; curadoria é via `/ingest`.
- O "Bypassed rule violations" no push direto do `/ship` é esperado (bypass intencional da conta do Gabriel) — não reportar.
- Build público exclui `raw/`; auto-link de citações e glossário rodam no CI sobre cópia — o markdown-fonte não é alterado.

## 5. Rules e hooks

Convenções detalhadas vivem em `.claude/rules/*.md` e são injetadas pelo hook `inject-rules.py` quando o arquivo editado casa com `paths:` — **uma vez por sessão** (e de novo após compactação). Frontmatter opcional: `quando:` (regex sobre o conteúdo escrito) e `bash: true` (vale também para buscas via Bash). Detalhe editorial novo vai para uma rule, não para cá.

`lint-on-edit.py` roda o lint no arquivo após cada edição em `wiki/**/*.md` e aponta erros/warnings; não substitui o `/lint` global.
