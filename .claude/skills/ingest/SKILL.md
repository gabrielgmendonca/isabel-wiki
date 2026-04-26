---
name: ingest
description: Ingere uma nova fonte de raw/ na wiki IsAbel — lê a fonte, discute pontos-chave com o usuário, cria página da obra, atualiza conceitos/entidades, flagga divergências com Kardec, atualiza catalogo.md e log.md. Use quando o usuário disser "faça ingest de X", "acabei de adicionar X em raw/", ou invocar /ingest.
---

# /ingest

Gatilhos: "faça ingest de X" · "acabei de adicionar X em raw/" · `/ingest <caminho>`

## Fase de análise

Ao iniciar, **apresente o outline em texto e aguarde confirmação do usuário antes de qualquer escrita**. Em plan mode (modo manual), isso é o próprio `EnterPlanMode`; em auto mode, é uma pausa explícita pedindo aprovação. A regra é: nada em `wiki/` é editado antes do usuário aprovar.

### Passo 0 — Pré-checagem de escopo

1. Identifique autor e obra pelo nome/caminho do arquivo em `raw/`.
2. Classifique conforme seção 2 do CLAUDE.md:
   - Nível 1, 2, 3 ou 4 → siga adiante.
   - **Fora de escopo** → PARE. Informe o conflito e aguarde confirmação explícita antes de prosseguir.
   - Autor desconhecido/ambíguo → pergunte ao usuário antes de classificar.

### Passos 1–2 — Leitura e discussão

1. **Ler** o arquivo em `raw/`.
2. **Conversar**: apresentar 5–10 pontos-chave e aguardar confirmação. **Não escrever nenhuma página antes disso.**

## Fase de escrita

Após confirmação do usuário, prosseguir para a fase de escrita:

3. **Checar duplicatas via qmd** antes de criar páginas: query `lex` + `vec` em coleção `wiki` por título da obra e conceitos centrais. Se já existir página próxima, consolidar nela (adicionar seção/citação) ao invés de criar nova.
4. **Criar** `wiki/obras/<slug>.md` ou `wiki/personalidades/<slug>.md`.
5. **Extrair e vincular**:
   - **Autor(es) da obra**: atualizar `wiki/personalidades/<slug>.md` adicionando a nova obra em `## Obras associadas` (ou criar a página se não existir). Para psicografias, fazer isso tanto para o médium quanto para o autor espiritual (ex.: Chico Xavier **e** Emmanuel para *O Consolador*).
   - **Personalidades citadas e conceitos**: atualizar páginas existentes (consolidar, não substituir) ou criar novas.

> [!note] Escopo
> `/ingest` só produz páginas de `obras/`, `personalidades/` e `conceitos/`. Páginas de `wiki/questoes/` (Q&A direta ancorada em uma única questão ou item pontual do Pentateuco) e `wiki/aprofundamentos/` (estudo sistemático de um tema/bloco doutrinário — subseção do LE, capítulo do ESE, etc.) emergem do workflow **Query** (CLAUDE.md §4), não da ingestão.
6. **Checar alinhamento com Kardec**: flaggar divergências conforme regra de divergência (`.claude/rules/regra-divergencia.md`).
7. **Atualizar `wiki/sinteses/catalogo.md`** com links e resumos das páginas novas (a home `index.md` é landing de trilhas e não lista páginas individuais).
8. **Recalcular "Status do projeto"**: rodar `uv run python .claude/skills/ingest/scripts/update_status.py` para atualizar a linha `**Cobertura atual:**` em `index.md` (contagens de obras, conceitos etc.).
9. **Append em `log.md`**: `## [YYYY-MM-DD] ingest | <título>` + 2–3 frases.
10. **Reportar** arquivos criados/atualizados e sugerir rodar `/lint` para verificar integridade da wiki após a ingestão (links, frontmatter, taxonomia).

**Passo 4 — link ao texto integral:** nos Dados bibliográficos da página de obra, incluir `**Texto integral:** [[raw/<caminho-da-fonte>]]` apontando para o arquivo original em `raw/`.
