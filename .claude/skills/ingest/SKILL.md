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

   **Passo 4.5 — direitos autorais (apenas `wiki/obras/`):** preencher o bloco `direitos:` no frontmatter com base no detentor da obra. Tabela canônica de detentores em `.claude/rules/convencoes-paginas.md` (subseção "Direitos autorais"). Em dúvida (palestras, autores nível 4 sem mapeamento claro), marcar `desconhecido` e perguntar ao usuário durante a confirmação. Para obras protegidas, incluir `url_aquisicao` quando conhecido (FEB, Boa Nova, LEAL).

   Para livros da FEB Editora, usar o helper `find_feb_url.py`:
   1. `uv run python .claude/skills/ingest/scripts/find_feb_url.py wiki/obras/<slug>.md` — imprime a URL de busca da FEB Editora a partir do título da obra.
   2. WebFetch nessa URL para listar candidatos. Escolher o slug canônico (mais curto, sem variantes `--ingles-`, `--novo-projeto2`, `-para-criancas`).
   3. `uv run python .claude/skills/ingest/scripts/find_feb_url.py wiki/obras/<slug>.md --set https://www.febeditora.com.br/<produto>` — grava em `direitos.url_aquisicao`.
5. **Extrair e vincular**:
   - **Autor(es) da obra**: atualizar `wiki/personalidades/<slug>.md` adicionando a nova obra em `## Obras associadas` (ou criar a página se não existir). Para psicografias, fazer isso tanto para o médium quanto para o autor espiritual (ex.: Chico Xavier **e** Emmanuel para *O Consolador*).
   - **Personalidades citadas e conceitos**: atualizar páginas existentes (consolidar, não substituir) ou criar novas.
   - **Série André Luiz** — para todo livro da série, garantir que o **Espírito orientador** da obra tenha página própria em `wiki/personalidades/`. Em *Nosso Lar* e *Entre a Terra e o Céu* o orientador é Clarêncio; em outros volumes podem ser Alexandre (*Os Mensageiros*), Aniceto (*Missionários da Luz*), Gúbio (*Obreiros da Vida Eterna*) etc. Se a página do orientador ainda não existir, criar; se existir, enriquecer com material da nova obra.

> [!note] Escopo
> `/ingest` só produz páginas de `obras/`, `personalidades/` e `conceitos/`. Páginas de `wiki/questoes/` (Q&A direta ancorada em uma única questão ou item pontual do Pentateuco) e `wiki/aprofundamentos/` (estudo sistemático de um tema/bloco doutrinário — subseção do LE, capítulo do ESE, etc.) emergem do workflow **Query** (CLAUDE.md §4), não da ingestão.
6. **Checar alinhamento com Kardec**: flaggar divergências conforme regra de divergência (`.claude/rules/regra-divergencia.md`).
7. **Atualizar `wiki/sinteses/catalogo.md`** com links e resumos das páginas novas (a home `index.md` é landing de trilhas e não lista páginas individuais).
8. **Recalcular "Status do projeto"**: rodar `uv run python .claude/skills/ingest/scripts/update_status.py` para atualizar a linha `**Cobertura atual:**` em `index.md` (contagens de obras, conceitos etc.).
9. **Append em `log.md`**: `## [YYYY-MM-DD] ingest | <título>` + 2–3 frases.
10. **Reportar** arquivos criados/atualizados e sugerir rodar `/lint` para verificar integridade da wiki após a ingestão (links, frontmatter, taxonomia).

**Passo 4 — link ao texto integral:** nos Dados bibliográficos da página de obra, incluir `**Texto integral:** [[raw/<caminho-da-fonte>]]` apontando para o arquivo original em `raw/`.
