---
name: ingest
description: Ingere uma nova fonte de raw/ na wiki IsAbel — lê a fonte, discute pontos-chave com o usuário, cria página da obra, atualiza conceitos/entidades, flagga divergências com Kardec, atualiza catalogo.md e log.md. Use quando o usuário disser "faça ingest de X", "acabei de adicionar X em raw/", ou invocar /ingest.
---

# /ingest

Gatilhos: "faça ingest de X" · "acabei de adicionar X em raw/" · `/ingest <caminho>`

## Fase de análise

A regra é: **nada em `wiki/` é editado antes do usuário aprovar um plano explícito**. Para garantir isso, esta fase **sempre termina em `EnterPlanMode`** — independente do modo do harness (manual ou auto). A aprovação do plano é o gate para a fase de escrita.

### Passo 0 — Pre-flight e pré-checagem de escopo

Custo ~30s; evita o ciclo completo de análise descartado quando o raw está ausente desta worktree ou a branch está atrás de `main`.

**Pre-flight material** (rodar antes de qualquer leitura ou query):

1. **`raw/<caminho>` existe nesta worktree?** `test -e raw/<caminho>` (ou `ls`). Se não existir, PARE — pode estar em outra worktree, em `main` à frente desta branch, ou nunca foi adicionado. Sugerir candidatos com `find raw -iname '*<chave>*'` antes de pedir confirmação ao usuário.
2. **Branch alinhada com `main`?** `git rev-parse --abbrev-ref HEAD` para identificar a branch; se não for `main`, `git rev-list --count HEAD..main` (comparação local, sem `fetch`). Se >0, PARE — `main` está à frente desta branch e o arquivo pode estar visível só lá; sugerir `git rebase main` (ou `git merge main`) antes de prosseguir.
3. **Índice qmd fresco?** `qmd status` → ler `lastUpdated` das coleções `wiki` e `raw`. Comparar com `git log -1 --format=%cI -- wiki raw` (timestamp do último commit que tocou conteúdo indexável). Se algum `lastUpdated` < timestamp do commit, rodar `qmd update && qmd embed` antes de prosseguir — leva segundos no caso comum, e sem isso a checagem de duplicatas do Passo 2 pode falsamente reportar "não existe". O caminho feliz é skip: `/ship` reindexa ao final, então normalmente não há nada a fazer aqui.

**Layout e dedup em `raw/`** (sobretudo se a fonte é PDF a converter): conversões manuais vivem em **subpasta por obra** — `raw/.../<slug>/<slug>.md`, com o PDF um nível acima (`raw/.../<slug>.pdf`). Considerar a obra **já feita** se houver `.md` rastreado (`git ls-files`) com o mesmo *stem* **em qualquer lugar sob `raw/`** (não só irmão do PDF) OU página correspondente em `wiki/obras/`. Antes de qualquer lote de conversão, fazer dry-run e confirmar escopo — checar só o irmão de mesmo nome quase reconverteu 25 obras prontas.

**Pré-checagem de escopo:**

4. Identifique autor e obra pelo nome/caminho do arquivo em `raw/`.
5. Classifique conforme seção 2 do CLAUDE.md:
   - Nível 1, 2, 3 ou 4 → siga adiante.
   - **Nível 3 vs 4**: nível 3 é reservado a autores **consagrados** (Léon Denis / Chico / Divaldo-tier, ou peso doutrinário comparável: Emmanuel, André Luiz, Bezerra, Cairbar, Joanna de Ângelis). Complementar alinhado mas sem essa estatura (Hammed/Espírito Santo Neto, palestras isoladas) → nível 4. Em dúvida, perguntar antes de classificar.
   - **Fora de escopo** → PARE. Informe o conflito e aguarde confirmação explícita antes de prosseguir (sem `EnterPlanMode` ainda — a confirmação aqui é prosa).
   - Autor desconhecido/ambíguo → pergunte ao usuário antes de classificar.

### Passos 1–4 — Leitura, dedup e plano

1. **Ler** o arquivo em `raw/`. Para fontes grandes (>1000 linhas), abrir via `mcp__qmd__get <path>:<offset>` em vez de `Read` integral (ver `busca-qmd.md`).
2. **Checar duplicatas via qmd**: `mcp__qmd__query` com `intent`, `collections: ["wiki"]`, `limit: 5`, `minScore: 0.5` e duas sub-queries — `lex` pelo título da obra, `vec` pelos conceitos centrais.
3. **Checar lar canônico de cada fio conceitual**: antes de cunhar qualquer slug de conceito novo, rodar qmd + `ls wiki/conceitos/` por termos **kardecianos** vizinhos. Se já houver página na terminologia de Kardec, o plano propõe consolidar nela; só criar nova quando nenhum lar existir, nomeando pela linguagem da fonte/Kardec — nunca rótulo cunhado (`primado-das-obras-basicas` era glosa de `fe-raciocinada`; slug inventado polui o grafo e duplica doutrina já presente).
4. **Chamar `EnterPlanMode`** com o plano em três blocos visualmente separados. Disciplina de tamanho é contrato da skill — o plano é superfície de revisão, não relatório; cada bloco tem orçamento próprio:

   **§0 — Ficha da fonte** (teto ~15 linhas, mesma forma toda vez — o olho do revisor aprende onde olhar):
   - Linha 1: obra · autor (espiritual/médium se psicografia) · nível doutrinário proposto + justificativa em 1 frase.
   - 3–6 teses centrais, 1 linha cada, **cada uma com a citação-âncora** `(sigla, ref)`.
   - Divergências candidatas com Kardec: 1 linha cada, ou "nenhuma aparente".
   - Duplicatas qmd: "consolidar em [[X]]" (com score) ou "nada próximo".

   **§A — Decisões (precisa do seu julgamento)** — só itens decision-grade, 1 linha de razão cada:
   - Classificação nível 1/2/3/4 + justificativa.
   - Consolidação: páginas existentes que absorvem o material (resultado da dedup) em vez de página nova.
   - Conceitos **página própria vs. inline**: para cada um, o fio conceitual + resultado da checagem de lar canônico (Passo 3 acima) + slug proposto na terminologia de Kardec/fonte. É aqui que o julgamento editorial mais erra.
   - Divergências a flaggar (ou "nenhuma").
   - Direitos: detentor previsto (ou "desconhecido — confirmo com você") e `url_aquisicao` se protegida.

   **§B — Execução (idempotente — FYI, não aprova item a item)** — lista compacta, sem prosa:
   - Páginas a criar: `wiki/obras/<slug>.md`, `wiki/personalidades/<slug>.md`, `wiki/conceitos/<slug>.md` — só os slugs.
   - Páginas existentes a enriquecer: slugs que ganham seção/citação nova (distinto da consolidação em §A — aqui a página continua sobre seu tema, só recebe afirmação citada nova). Mapa de edição; as `(sigla, ref)` agregadas vão no relatório do Passo 7.
   - Enrich scripts a rodar; `catalogo.md`; `log.md`. `index.md` **não** é tocado (linha "Cobertura atual" é do `/stats` na `main` — evita conflito entre worktrees).

   Se o usuário rejeitar o plano, ajustar e re-submeter — não escrever nada. Uma leitura errada da fonte aparece em §0 e custa só uma rejeição, não conteúdo escrito.

## Fase de escrita

Apenas após o usuário aprovar o plano via `EnterPlanMode`, executar. **Trabalhar sem narração intermediária** — não anunciar cada passo ("agora crio X… agora atualizo Y…"). As únicas superfícies que falam com o usuário são o plano (§0/§A/§B) e o relatório de verificação final (Passo 7).

1. **Criar** `wiki/obras/<slug>.md` ou `wiki/personalidades/<slug>.md`. Nos Dados bibliográficos da página de obra, incluir `**Texto integral:** [[raw/<caminho-da-fonte>]]` apontando para o arquivo original em `raw/`.

   **1.1 — direitos autorais (apenas `wiki/obras/`):** preencher o bloco `direitos:` no frontmatter com base no detentor da obra. Tabela canônica de detentores em `.claude/rules/convencoes-direitos.md`. Em dúvida (palestras, autores nível 4 sem mapeamento claro), marcar `desconhecido` e perguntar ao usuário durante a confirmação. Para obras protegidas, incluir `url_aquisicao` quando conhecido (FEB, Boa Nova, LEAL).

   Para livros da FEB Editora, usar o helper `find_feb_url.py`:
   1. `uv run python .claude/skills/ingest/scripts/find_feb_url.py wiki/obras/<slug>.md` — imprime a URL de busca da FEB Editora a partir do título da obra.
   2. WebFetch nessa URL para listar candidatos. Escolher o slug canônico (mais curto, sem variantes `--ingles-`, `--novo-projeto2`, `-para-criancas`).
   3. `uv run python .claude/skills/ingest/scripts/find_feb_url.py wiki/obras/<slug>.md --set https://www.febeditora.com.br/<produto>` — grava em `direitos.url_aquisicao`.

   Para livros da Livraria Leal (Divaldo Franco / Joanna de Ângelis), usar `find_leal_url.py`. A Leal não tem busca por query string, mas o helper consulta `sitemap_produtos.xml` direto e ranqueia por slug do título — não precisa special-casear "Série Psicológica":
   1. `uv run python .claude/skills/ingest/scripts/find_leal_url.py wiki/obras/<slug>.md` — imprime URLs candidatas (match exato + parciais).
   2. Escolher entre as candidatas. Se houver match exato único, usar essa URL; em caso de múltiplos ou apenas parciais, abrir cada uma com WebFetch para confirmar título/edição.
   3. `uv run python .claude/skills/ingest/scripts/find_leal_url.py wiki/obras/<slug>.md --set https://www.livrarialeal.com.br/<categoria>/<slug>.html` — grava em `direitos.url_aquisicao`.
2. **Extrair e vincular**:
   - **Autor(es) da obra**: atualizar `wiki/personalidades/<slug>.md` adicionando a nova obra em `## Obras associadas` (ou criar a página se não existir). Para psicografias, fazer isso tanto para o médium quanto para o autor espiritual (ex.: Chico Xavier **e** Emmanuel para *O Consolador*).
   - **Personalidades citadas e conceitos**: atualizar páginas existentes (consolidar, não substituir) ou criar novas. **Conceito tratável isoladamente** (tem definição, ensino de Kardec e aplicação prática) → **página própria linkada**, nunca seção inline numa página maior — só assim aparece em buscas e alimenta o grafo. Levantar proativamente os fios conceituais transversais que atravessam vários capítulos da obra e pedem destinação dedicada, mesmo quando já existe um conceito-mãe (pode haver subconceito autônomo). Seção inline apenas para desdobramento sem autonomia conceitual; em dúvida, default para página própria — **mas esse default só vale sem lar canônico**: se a checagem de lar canônico (Passo 3 da fase de análise) achou página na terminologia de Kardec, consolidar nela; slug novo nomeia pela linguagem da fonte/Kardec, nunca rótulo cunhado.
   - **Série André Luiz** — para todo livro da série, identificar o(s) **Espírito(s) orientador(es)** que conduz(em) a narrativa (varia por volume) e garantir que tenha(m) página própria em `wiki/personalidades/`. Se ainda não existir, criar; se existir, enriquecer com material da nova obra. Não assumir o orientador a partir de memória — confirmar lendo o próprio texto em `raw/`.

> [!note] Escopo
> `/ingest` só produz páginas de `obras/`, `personalidades/` e `conceitos/`. Páginas de `wiki/questoes/` (Q&A direta ancorada em uma única questão ou item pontual do Pentateuco) e `wiki/aprofundamentos/` (estudo sistemático de um tema/bloco doutrinário — subseção do LE, capítulo do ESE, etc.) emergem do workflow **Query** (CLAUDE.md §4), não da ingestão.
3. **Checar alinhamento com Kardec**: flaggar divergências conforme regra de divergência (`.claude/rules/regra-divergencia.md`).
4. **Atualizar `wiki/sinteses/catalogo.md`** com links e resumos das páginas novas (a home `index.md` é landing de trilhas e não lista páginas individuais).
5. **Enriquecer tags hierárquicas**: rodar os enrich scripts para preencher os namespaces validados. Todos idempotentes — skipam páginas já completas. Taxonomia completa em `.claude/rules/convencoes-tags.md`.
   - `uv run python scripts/enrich_tags_obra.py` — `obra/*` a partir de `fontes:`.
   - `uv run python scripts/enrich_tags_autor.py` — `autor/*` a partir de `fontes:` e tags livres canônicas (espírito + médium para psicografias).
   - `uv run python scripts/enrich_tags_grau.py` — `grau/*` por default heurístico (`questao`→introdutorio, `conceito`/`parabola`/`personalidade`→intermediario, `aprofundamento`/`sintese`/`divergencia`→avancado). Revisar caso a caso após gravar; promover/rebaixar manualmente quando o conteúdo discordar do default.
   - **`tema/*`** (1-3 valores em conjunto fechado: `tema/deus`, `tema/espiritos`, `tema/encarnacao`, `tema/mediunidade`, `tema/moral`, `tema/jesus`, `tema/vida-futura`, `tema/sociedade`, `tema/livre-arbitrio`, `tema/prece-caridade`, `tema/sofrimento`, `tema/historia-doutrina`) — **atribuir manualmente** no frontmatter de cada página criada/atualizada. Não há script; o significado é semântico.
   - `lei/*` (10 valores) quando a página tratar de lei moral — `uv run python scripts/enrich_tags_lei.py --apply` cobre os casos óbvios; complementar manual.
6. **Append em `log.md`**: `## [YYYY-MM-DD] ingest | <título>` + 2–3 frases. Não tocar `index.md` — a linha "Cobertura atual" é regenerada pelo `/stats` na `main` (evita conflito entre worktrees paralelas; `log.md` usa `merge=union` no `.gitattributes` e auto-mescla).
7. **Relatório de verificação** (por exceção, forma fixa — substitui a lista chapada de arquivos):
   - **Citações novas afirmadas**: lista `(sigla, ref) — página` de toda afirmação doutrinária nova, para spot-check do usuário.
   - **Divergências flaggadas**: onde e o quê, 1 linha cada (ou "nenhuma").
   - **Desvios do plano aprovado**: o que mudou na escrita vs. §A, declarado explicitamente (ou "sem desvios").
   - **Arquivos**: criados/atualizados em 1 linha, no fim.
   - Sugerir rodar `/lint` para verificar integridade da wiki (links, frontmatter, taxonomia).
