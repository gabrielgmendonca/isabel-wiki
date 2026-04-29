---
name: ingest
description: Ingere uma nova fonte de raw/ na wiki IsAbel — lê a fonte, discute pontos-chave com o usuário, cria página da obra, atualiza conceitos/entidades, flagga divergências com Kardec, atualiza catalogo.md e log.md. Use quando o usuário disser "faça ingest de X", "acabei de adicionar X em raw/", ou invocar /ingest.
---

# /ingest

Gatilhos: "faça ingest de X" · "acabei de adicionar X em raw/" · `/ingest <caminho>`

## Fase de análise

A regra é: **nada em `wiki/` é editado antes do usuário aprovar um plano explícito**. Para garantir isso, esta fase **sempre termina em `EnterPlanMode`** — independente do modo do harness (manual ou auto). A aprovação do plano é o gate para a fase de escrita.

### Passo 0 — Pré-checagem de escopo

1. Identifique autor e obra pelo nome/caminho do arquivo em `raw/`.
2. Classifique conforme seção 2 do CLAUDE.md:
   - Nível 1, 2, 3 ou 4 → siga adiante.
   - **Fora de escopo** → PARE. Informe o conflito e aguarde confirmação explícita antes de prosseguir (sem `EnterPlanMode` ainda — a confirmação aqui é prosa).
   - Autor desconhecido/ambíguo → pergunte ao usuário antes de classificar.

### Passos 1–2 — Leitura, discussão e plano

1. **Ler** o arquivo em `raw/`.
2. **Checar duplicatas via qmd**: query `lex` + `vec` em coleção `wiki` por título da obra e conceitos centrais. Resultado entra no plano (se já existir página próxima, propor consolidação em vez de criar nova).
3. **Apresentar 5–10 pontos-chave em prosa** para o usuário (resposta de texto normal, sem tool call). Isso permite ajustes antes do plano formal.
4. **Chamar `EnterPlanMode`** com o plano de escrita estruturado. O plano deve conter, no mínimo:
   - **Classificação**: nível doutrinário (1/2/3/4) e justificativa.
   - **Páginas a criar**: lista de `wiki/obras/<slug>.md`, `wiki/personalidades/<slug>.md`, `wiki/conceitos/<slug>.md` com 1 linha de propósito cada.
   - **Páginas a atualizar**: existentes que ganham seção/citação (resultado da checagem de duplicatas).
   - **Direitos autorais**: detentor previsto e `url_aquisicao` (se obra protegida).
   - **Divergências com Kardec**: lista de pontos a flaggar (ou "nenhuma identificada").
   - **Atualizações finais**: `catalogo.md`, `log.md`, recálculo de `index.md`.
   
   Se o usuário rejeitar o plano, ajustar e re-submeter — não escrever nada.

## Fase de escrita

Apenas após o usuário aprovar o plano via `EnterPlanMode`, executar:

1. **Criar** `wiki/obras/<slug>.md` ou `wiki/personalidades/<slug>.md`. Nos Dados bibliográficos da página de obra, incluir `**Texto integral:** [[raw/<caminho-da-fonte>]]` apontando para o arquivo original em `raw/`.

   **1.1 — direitos autorais (apenas `wiki/obras/`):** preencher o bloco `direitos:` no frontmatter com base no detentor da obra. Tabela canônica de detentores em `.claude/rules/convencoes-paginas.md` (subseção "Direitos autorais"). Em dúvida (palestras, autores nível 4 sem mapeamento claro), marcar `desconhecido` e perguntar ao usuário durante a confirmação. Para obras protegidas, incluir `url_aquisicao` quando conhecido (FEB, Boa Nova, LEAL).

   Para livros da FEB Editora, usar o helper `find_feb_url.py`:
   1. `uv run python .claude/skills/ingest/scripts/find_feb_url.py wiki/obras/<slug>.md` — imprime a URL de busca da FEB Editora a partir do título da obra.
   2. WebFetch nessa URL para listar candidatos. Escolher o slug canônico (mais curto, sem variantes `--ingles-`, `--novo-projeto2`, `-para-criancas`).
   3. `uv run python .claude/skills/ingest/scripts/find_feb_url.py wiki/obras/<slug>.md --set https://www.febeditora.com.br/<produto>` — grava em `direitos.url_aquisicao`.
2. **Extrair e vincular**:
   - **Autor(es) da obra**: atualizar `wiki/personalidades/<slug>.md` adicionando a nova obra em `## Obras associadas` (ou criar a página se não existir). Para psicografias, fazer isso tanto para o médium quanto para o autor espiritual (ex.: Chico Xavier **e** Emmanuel para *O Consolador*).
   - **Personalidades citadas e conceitos**: atualizar páginas existentes (consolidar, não substituir) ou criar novas.
   - **Série André Luiz** — para todo livro da série, identificar o(s) **Espírito(s) orientador(es)** que conduz(em) a narrativa (varia por volume) e garantir que tenha(m) página própria em `wiki/personalidades/`. Se ainda não existir, criar; se existir, enriquecer com material da nova obra. Não assumir o orientador a partir de memória — confirmar lendo o próprio texto em `raw/`.

> [!note] Escopo
> `/ingest` só produz páginas de `obras/`, `personalidades/` e `conceitos/`. Páginas de `wiki/questoes/` (Q&A direta ancorada em uma única questão ou item pontual do Pentateuco) e `wiki/aprofundamentos/` (estudo sistemático de um tema/bloco doutrinário — subseção do LE, capítulo do ESE, etc.) emergem do workflow **Query** (CLAUDE.md §4), não da ingestão.
3. **Checar alinhamento com Kardec**: flaggar divergências conforme regra de divergência (`.claude/rules/regra-divergencia.md`).
4. **Atualizar `wiki/sinteses/catalogo.md`** com links e resumos das páginas novas (a home `index.md` é landing de trilhas e não lista páginas individuais).
5. **Enriquecer tags `obra/`**: rodar `uv run python scripts/enrich_tags_obra.py` para preencher as tags `obra/*` derivadas do campo `fontes` nas páginas novas/atualizadas. Idempotente — skipa páginas já completas. A taxonomia `obra/` está documentada em `.claude/rules/convencoes-paginas.md`.
6. **Recalcular "Status do projeto"**: rodar `uv run python .claude/skills/ingest/scripts/update_status.py` para atualizar a linha `**Cobertura atual:**` em `index.md` (contagens de obras, conceitos etc.).
7. **Append em `log.md`**: `## [YYYY-MM-DD] ingest | <título>` + 2–3 frases.
8. **Reportar** arquivos criados/atualizados e sugerir rodar `/lint` para verificar integridade da wiki após a ingestão (links, frontmatter, taxonomia).
