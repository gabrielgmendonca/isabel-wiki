# Roadmap — IsAbel Wiki Espírita

> Melhorias de maior complexidade planejadas para a wiki.
> Organizadas por eixo temático, não por ordem cronológica.
> Itens **concluídos** vivem condensados no apêndice [Concluído](#concluído) — o detalhe fica no git.
> Última revisão: 2026-06-15.

---

## 1. Cobertura de fontes

Completar a base doutrinária. Três frentes: **obras a ingerir** (gargalo principal), **curadoria de páginas existentes** e **pipeline/processos**.

### 1.1 Obras a ingerir

> **Onde vive a lista**: esta seção é **estratégia** — qual autor priorizar e por quê. O **estado factual** das duas filas do pipeline (`aquisição → raw/ → /ingest → wiki/`) vive fora daqui, para não envelhecer:
> - **Fila de ingestão** (obra em `raw/` sem página em `wiki/obras/`) → `uv run python scripts/list_pending_ingest.py` (derivada, nunca mantida à mão; ~563 pendentes na última medição, pós-CEAK).
> - **Fila de aquisição** (obra ainda não em `raw/`) → `tracking/` (FEB, CEAK, triagem de direitos).
>
> As contagens por-autor abaixo podem estar defasadas em relação ao script — após a ingestão do catálogo CEAK (commit `c3c0d87`) vários "gargalos" mudaram (Cairbar e Gabriel Delanne deixaram de ter pasta vazia; **Peralva e Eurípedes seguem vazios**). **Checar o script antes de assumir que um autor está descoberto.** Não é exaustiva quanto a `raw/mediuns/chico-xavier/**` nem `raw/mediuns/divaldo-franco/**`.

**Nível 1 — Pentateuco · Nível 2 — Kardec complementar · Novo Testamento canônico** — fechados (ver [Concluído](#concluído)).

**Nível 3 — Consagrados** (cobertura parcial)
- [ ] **6 títulos André Luiz pendentes**: `agenda-crista`, `apostilas-da-vida`, `desobsessao`, `enderecos-da-paz`, `respostas-da-vida`, `sinal-verde` (raw atual 13/19 ingerido).
- [ ] **Yvonne Pereira** (nível 3) — **6 ingeridas** (A Luz do Consolador, Recordações da Mediunidade, Memórias de um Suicida, Contos e Apólogos, Evangelho aos Simples, Nas Telas do Infinito; o raw cresceu além das 14 originais via CEAK). Pendentes em `raw/autores/yvonne-pereira/`: `a-familia-espirita`, `a-tragedia-de-santa-maria`, `amor-e-odio`, `as-tres-revelacoes`, `devassando-o-invisivel`, `dramas-da-obsessao`, `nas-voragens-do-pecado`, `o-cavaleiro-de-numiers`, `o-drama-da-bretanha`, `ressurreicao-e-vida`, `sublimacao` (conferir contagem exata no script).
- [ ] **Gabriel Delanne** (nível 3 — discípulo direto de Kardec) — 0 ingeridas; ~14 títulos em `raw/autores/gabriel-delanne/` (A Alma é Imortal, A Reencarnação, A Evolução Anímica, O Espiritismo perante a Ciência, O Fenômeno Espírita, A Mediunidade Mecânica, Automatismo da Escrita Psicográfica e outros via CEAK). Vários em `.doc` — converter antes do ingest.
- [ ] **Cairbar Schutel** — **agora com raw** (18 títulos via CEAK em `raw/autores/cairbar-schutel/`); deixou de ser gargalo de aquisição → vira tarefa de *ingest* (definir obra-âncora ≥1).
- [ ] **Martins Peralva, Eurípedes Barsanulfo** — sem obra-âncora e **pastas vazias** (`raw/autores/{martins-peralva,euripedes-barsanulfo}/`). Gargalo de **aquisição** persiste — ingest depende de adquirir a fonte primeiro. Definition of done: ≥1 obra-âncora por autor.

**Pesquisa psíquica / espiritismo científico** (categoria do CLAUDE.md §2 — corroboração experimental dos fatos, **sem** autoridade doutrinária sobre o Pentateuco; ingerir com a ressalva explícita)
- [~] **Camille Flammarion** — 8/9 já ingeridas; falta `o-desconhecido-e-os-problemas-psiquicos`. ⚠️ As 8 páginas **precedem** a classificação — revisar para inserir a ressalva de "pesquisa psíquica" (sem autoridade doutrinária) onde couber.
- [ ] **Ernesto Bozzano** — 0 ingeridas; ~54 títulos em `raw/autores/ernesto-bozzano/` (vários `.doc`/`.pdf`). Definir prioridade antes de qualquer ingest — fenomenologia metapsíquica, frequentemente neutra quanto à reencarnação.

### 1.2 Curadoria de páginas existentes

Frente contínua (sem itens fixos em aberto). Itens nominais entregues — coautoria mediúnica em obras psicografadas e expansão de personalidades-âncora — em [Concluído](#concluído). Novos itens entram conforme `/lint`/`/critica` apontarem stub ou drift.

### 1.3 Pipeline e processos

- [ ] **Manifest de progresso em lotes longos** — JSON de itens concluídos, checado no início, para retomar conversão de catálogo / ingest multi-livro após limite de uso ou timeout. **Pré-requisito de segurança do loop autônomo roadmap-driven** (versão atenuada com gate humano, análoga ao `/autolint` em §5).
- [ ] **Pipeline de palestras** — consolidar workflow YouTube → transcrição → summary → ingest; hoje funciona (`/yt`, `/yt-bulk`) mas a curadoria via `/ingest` é manual demais.

---

## 2. Experiência do leitor público

- [~] **Trilhas de estudo guiadas** — as 4 trilhas da home (primeiros-passos, esde, palestras, leitura-livre) + decisoes-dificeis **estão preenchidas** com sequência comentada (~74-96 linhas cada, `status: ativo`) — não são mais stubs (medição 2026-06-17). **Resta TODO:** aferição de progresso e trilhas extras ("As Leis Morais em ordem", "Mediunidade: do básico ao avançado").
- [~] **Glossário navegável** — stub em `wiki/sinteses/glossario.md` com ~15 conceitos-raiz. Popular ~126 restantes, uma linha por termo, é TODO.
- [ ] **Expandir affordances da home** — considerar 6ª/7ª entrada (ex.: Divergências, Personalidades) conforme crescer. Manter 5 hoje para não sobrecarregar.
- [~] **Tags e filtragem** — 5 namespaces canônicos documentados em `convencoes-tags.md`; lint estendido (`check_tag_taxonomy`, `check_tag_coverage`); `enrich_tags_autor.py`/`enrich_tags_grau.py` idempotentes. **Faltando:** passada manual de `tema/*` nas ~345 páginas listadas pelo `tag_coverage`.
- [ ] **Revisar tags `tema/`** — auditar o conjunto canônico de 12 valores; identificar temas sub-representados, sobrepostos ou ausentes; reavaliar granularidade (ex.: separar `mediunidade` de `obsessao`). Revisar páginas tagueadas em massa (commit `5629049`) para corrigir falsos positivos.
- [~] **Acessibilidade para leitores de tela** — VoiceOver/NVDA/JAWS leem na ordem do DOM. Quartz v4.4.0 emite `.left → .center → .right` como `<div>`s genéricas (sem `<nav>/<main>/<aside>`), então o leitor passa pelo Explorer inteiro antes do conteúdo ("leitura presa no menu lateral", reportado 2026-05-22).
  - **Landmarks no SSR — FEITO (2026-06-17):** `quartz-overrides/components/renderPage.tsx` (cópia do upstream v4.4.0, diff mínimo) troca as 3 `<div class="left|center|right">` por `<nav aria-label="Navegação do site">` / `<main>` / `<aside aria-label="Conteúdo complementar">`. Classes preservadas (o CSS do Quartz mira só por classe — confirmado: `.sidebar.left`, `.center > article`; nenhum seletor por-tag). Os únicos seletores JS são `closest(".sidebar")` (por classe). **Custo menor que o previsto:** o glob `cp -r quartz-overrides/components/*` já existente no `deploy-wiki.yml` e no `serve-local.sh` copia o arquivo automaticamente — **nenhuma edição de workflow necessária**. Validado por build local: HTML emitido traz exatamente 1 `<main>`, e os 2 `<nav>` (sidebar + breadcrumbs) ficam distinguíveis por `aria-label`. **Pendente:** validação com VoiceOver/NVDA reais (estrutura HTML conferida, comportamento do leitor não).
  - **Tentativa descartada (2026-05-22):** componente `SkipLink` custom injetando `<a class="skip-link">` + `role`s via JS `beforeDOMLoaded`. Build OK, mas VoiceOver não movia foco para `<main>` mesmo com `tabindex="-1"` + `.focus()`. Hipóteses: rotor do VO retém o item atual; `enableSPA` pode interceptar hash links; landmark via JS pós-hidratação chega tarde. Revertido sem commit. (O landmark real no SSR acima dispensa essa dança de JS+foco; um skip-link agora teria alvo `<main>` legítimo, se quiser revisitar.)
  - **Itens correlatos** (independentes do landmark): (a) alt text em embeds YouTube `![](url)` + `check_alt_text` no `lint_wiki.py`; (b) callouts `> [!warning]`/`> [!note]` viram `<blockquote>` comum sem `role` — exigiria transformer custom; (c) botões `A+`/`A−` em `FontSize.tsx` mudam `data-fontScale` sem `aria-live`; (d) `lang="pt"` e ARIA em Darkmode/Search/FontSize já presentes — o problema concentra-se nos landmarks.
- [x] **Marcar rascunhos visualmente para o leitor (2026-06-17)** — `status: rascunho` é campo custom (não o `draft:` do Quartz), então essas páginas são publicadas e renderizavam **idênticas** às `ativo` — o público não distinguia maturidade. Novo componente `quartz-overrides/components/DraftNotice.tsx` (em `beforeBody`, após o título) renderiza um aviso âmbar discreto ("Página em rascunho — conteúdo em revisão…") só quando `frontmatter.status === "rascunho"`, `null` caso contrário. Validado por build local (banner só em página rascunho; ausente em `ativo`). Complementa o banner "trabalho em andamento" da home enquanto o débito de rascunhos (§10.3, 155 hoje / 82 stale) é drenado.
- [x] **Título = slug em ~98% das páginas (2026-06-17)** — as páginas não usam `title:` no frontmatter (convenção: abrir com `# Título`); o Quartz, sem `title:`, usava o **nome do arquivo (slug)** como `<h1 class="article-title">` — "reencarnacao" (minúsculo, sem acento) acima do `# Reencarnação` do markdown: **dois `<h1>` por página**, o primeiro um identificador de máquina. Só 21/1049 páginas tinham `title:`. Override `quartz-overrides/components/ArticleTitle.tsx`: quando não há `title:` explícito, usa o texto do primeiro `# H1` do conteúdo; e **remove esse H1 líder do corpo** quando ele só repete o título (a árvore é compartilhada por referência; `beforeBody` renderiza antes do `Content`). Validado em escala sobre as 1049 páginas: 0 títulos com cara de slug, 0 `<h1>` duplicados. **Limite:** corrige o `<h1>` visível; título da aba/OG/busca/breadcrumb ainda vem de `frontmatter.title` (Head/Breadcrumbs renderizam antes) — fix completo exigiria um transformer que preencha `title:` na origem (candidato a follow-up).

---

## 3. Conteúdo de síntese e estudo

As categorias `questoes/` e `sinteses/` estão sub-representadas. São as mais valiosas para o leitor. (Snapshot operacional com medições e páginas concretas a escrever está em §10.)

- [ ] **Extrair questões-chave do Pentateuco** — selecionar as mais importantes de cada obra. **Priorizar blocos sub-cobertos do LE** (ver §10.1). Capitalizar Q&A ancorada em questão única antes de novas sínteses.
- [ ] **Promover conceitos centrais a aprofundamentos sistemáticos** — `/stats` mostra cadência ingest:aprofundamento desproporcional. Top PageRank com massa para estudo de 1h: `reencarnacao`, `progresso-espiritual`, `livre-arbitrio`, `perispirito`, `caridade`.
- [ ] **Sínteses temáticas** — comparativos entre obras sobre o mesmo tema (ex.: "O que cada obra diz sobre obsessão"; "Reencarnação: de Kardec a Léon Denis").
- [ ] **Quadros comparativos** — tabelas que cruzam conceitos entre obras ou autores.
- [ ] **Perguntas frequentes** — FAQ baseada em dúvidas comuns de estudantes, com respostas fundamentadas e citadas.

---

## 4. Cross-references enriquecidas

A wiki tem links, mas pode ser mais densa em conexões.

- [ ] **Parábolas ↔ conceitos** — cada parábola do ESE linka explicitamente os conceitos morais que ilustra, e vice-versa.
- [ ] **Leis morais ↔ exemplos práticos** — conectar cada lei a parábolas, questões e casos concretos.
- [ ] **Personalidades ↔ conceitos** — Espíritos citados em C&I linkam conceitos que suas histórias ilustram.
- [ ] **Obras ↔ obras** — referências cruzadas quando uma obra cita ou complementa outra (ex.: Gênese referencia LE em vários pontos).
- [ ] **Grafo temático** — "hub pages" por tema agregando conceitos, personalidades, obras, questões (ex.: hub de "Mediunidade").
- [ ] **Tração inversa do cluster epistolar** — epístolas dominam o grau de saída mas não aparecem no grau de entrada nem no PageRank. Auditar: para cada conceito tratado numa epístola (caridade em 1 Cor 13, fé viva em Tiago 2), o conceito cita a obra epistolar?

### Citações inline como links

Auto-link Markdown→Kardecpedia em build time já cobre capítulo **e** questão/item (deep-link, ver [Concluído](#concluído)). Aprofundar:

- [x] **Fase 2 do híbrido — link interno preferencial** (2026-06-05) — **desvio deliberado da redação original**: em vez de editar `raw/kardec/pentateuco/*.md` in place e remover `raw` do `ignorePatterns` (o que (a) alteraria o texto do Kardec e (b) publicaria TODO o `raw/` — palestras, médiuns, obras integrais — com implicação de direitos), adotou-se o **padrão da Bíblia** (`publish_biblia_nt.py`): cópia derivada. `scripts/publish_pentateuco.py` gera `wiki/pentateuco/<obra>/<cap>.md` (130 páginas, tipo `capitulo-pentateuco` + 6 `obra-pentateuco`) com âncora `## q. N` / `## item N` por questão/item, reusando os extractors auditados do `cite.py`. `raw/` fica **intocado** (o publisher só lê; teste `RawUntouchedTests` prova) e `ignorePatterns` fica intacto. Manifest `data/pentateuco-anchors.json` (2524 âncoras: LE 1017, LM 306, ESE 382, C&I 164, Gênese 655). `link_citations.kardec_url`/`link_kardec` agora preferem `[[wiki/pentateuco/…#âncora|label]]` quando o locus tem âncora, com **fallback ao Kardecpedia** (Introdução-item, Conclusão, e capítulos irregulares — C&I 2ª parte nominal, ESE cap. XXVIII — caem no externo, cobertura idêntica à de hoje). **Garantia anti-perda determinística**: cada âncora só entra no manifest se o bloco sob ela for byte-a-byte igual ao `cite.literal_text` do raw (round-trip embutido no publisher + `RoundTripTests`). Lint: `wiki/pentateuco/**` tratado como corpus (set `_CORPUS_TIPOS`, espelhando a Bíblia) — fora de Fontes/órfãos/catálogo/tag-obra/citation-format/mundos-naming; capítulos verbatim ficam fora do `check_broken_links` porque trazem marcadores de nota de rodapé `[[1]](#_ftnref1)` do raw (alterá-los mexeria no texto). Testes: `tests/test_publish_pentateuco.py` (15). **Pré-requisito de direitos**: confirmado pelo usuário que o texto integral do Pentateuco (tradução PT-BR) pode ser publicado, como já feito com a Bíblia ACF. **Cosmético diferido**: os marcadores `[[1]](#_ftnref1)` renderizam como wikilink quebrado no site; manter verbatim (fidelidade > estética) ou limpar numa passada futura que NÃO altere o texto doutrinário. **Regenerar**: `uv run python scripts/publish_pentateuco.py` (idempotente; artefatos commitados como na Bíblia).
- [ ] **Cobrir Kardec complementar no auto-link** — estender mapping para RE, OPE, OQE, Viagem Espírita em 1862.
- [x] **Granularidade por questão/item — link externo (Kardecpedia)** (2026-06-05) — `build_kardec_mapping.py` agora **retém** a URL por questão/item que o crawler já buscava e descartava (`questions[last] = key` deixava cair o `path`). LE → `question_urls` (nº global, flat); LM → `item_urls` flat (item contínuo 1–350); ESE/C&I/Gênese → `item_urls` chaveado por `cap:item` (nº reinicia por capítulo). `link_citations.py:kardec_url` prefere a URL granular, com fallback ao capítulo quando o Kardecpedia não expõe a sub-página (ex.: ESE cap. XXVIII). Cobertura: LE 996, LM 327, ESE 476, C&I 180, Gênese 391. Diff do re-crawl confirmou core (chapters/questions/intro) inalterado. Testes: `DeepLinkTests` em `test_link_citations.py`. **Link interno preferencial** segue na Fase 2 (precisa dos headings no `raw/`).
- [x] **Linkar referências bíblicas** (2026-05-22) — NT linka interno (`[[wiki/biblia/<slug>/<cap>#<vers>|...]]`); AT linka externo (bibliaonline.com.br no nível do capítulo). Destravado pela publicação do NT (`fcfe9f9`) + mapping bíblico abaixo.
- [x] **Decisão sobre `wiki/biblia/`** (2026-05-22) — escolhido **(c) híbrido**: NT publicado em `wiki/biblia/<livro>/<capitulo>.md` (27 livros, ~260 arquivos); AT permanece em `raw/biblia-acf/` (39 livros) + link externo. Razão: NT é onde Jesus está (fonte primordial) e já é tratado obra-a-obra em `wiki/obras/`; AT é fonte ocasional. Achado durante o levantamento: `wiki/obras/biblia/` nunca existiu — os 27 livros NT vivem flat em `wiki/obras/<slug>.md`; e os wikilinks `[[raw/biblia-acf/<livro>/1]]` em `wiki/obras/evangelho-segundo-*.md` estão silenciosamente quebrados (Quartz ignora `raw/` no `ignorePatterns`).
- [x] **Publicar NT em `wiki/biblia/`** (feito no commit `7c1141a`; checkbox atualizado 2026-06-05) — **concluído**: 287 capítulos publicados em `wiki/biblia/<livro>/<cap>.md`, 27 `index.md` por livro (sub-decisão opcional abaixo resolvida = sim), `scripts/publish_biblia_nt.py` rastreado, substituição dos `[[raw/biblia-acf/…]]` feita (0 ocorrências restantes em `wiki/obras/`). Integridade verificada: os 27 slugs NT do `biblia-livros.json` resolvem para diretórios reais, anchor `#N` casa com heading `## N` por verso. Granularidade fixada (2026-05-22): **arquivo por capítulo** (~260 páginas, mesma cardinalidade do `raw/biblia-acf/<livro>/<cap>.md`). Razão: anchor de versículo estável, paridade 1:1 com a fonte ACF, leitor de capítulo isolado sem rolagem longa. Trade-off aceito: ~260 nós-folha no grafo do Quartz (mitigado por cross-link dos `wiki/obras/evangelho-segundo-*.md` e do auto-link de citações). Sub-tarefas:
  - Definir frontmatter padrão (tipo novo `capitulo-biblico`? `obra`? `raw-publicado`?) e schema mínimo (livro, capitulo, testamento, autor tradicional). Capítulo médio = ~110 linhas em ACF — preservar quebra de versículo.
  - Script `scripts/publish_biblia_nt.py` que copia 27 livros NT de `raw/biblia-acf/` para `wiki/biblia/<livro>/<cap>.md`, gera frontmatter, injeta heading por versículo (`## v.5`) para anchor estável.
  - Substituir `[[raw/biblia-acf/<livro>/1]]` por `[[wiki/biblia/<livro>/1]]` nos 27 `wiki/obras/evangelho-segundo-*.md` / epístolas / Atos / Apocalipse.
  - Decidir se cada livro recebe `wiki/biblia/<livro>/index.md` (página-âncora com lista de capítulos) — ajuda navegação por breadcrumb mas adiciona +27 páginas.
- [x] **Bible mapping em `link_citations.py`** (2026-05-22) — `data/biblia-livros.json` (66 livros + variantes Mt/Mateus, Gn/Gênesis, 1Co/1 Coríntios, S. Mateus); `build_biblia_mapping()`/`link_biblia()` no script, regex com alternação ordenada por tamanho desc para resolver longest-match (`1 Coríntios` antes de `1 Co`). NT → `[[wiki/biblia/<slug>/<cap>#<vers>|...]]` (anchor `#<N>` casa com heading `## <N>` do capítulo publicado — não `#v<N>` como esta linha grafava antes). AT → `bibliaonline.com.br/acf/<abbrev>/<cap>` no nível do capítulo (versículo via URL é instável). Range/lista de versos (`13:1-3`, `5:3,5,8`) linka primeiro verso e preserva label original; aceita en-dash além de ASCII hífen. Ambiguidade Jó/João resolvida exigindo diacrítico (`Jo` sem til não casa nem com um nem com outro). 14 testes em `tests/test_link_citations.py` (43 no total).
- [ ] **Fase 2 do híbrido — link interno preferencial** — normalizar `raw/kardec/pentateuco/*.md` com headings granulares (`## q. 990`, `## cap. VII, item 16`), remover `raw` do `ignorePatterns` do Quartz e preferir link interno sobre Kardecpedia quando disponível. **Dependência:** destrava também a "versão estrita" do check de citação (§5).
- [ ] **Cobrir Kardec complementar no auto-link** — estender o mapping para RE, OPE, OQE, Viagem Espírita em 1862.

---

## 5. Qualidade e automação

### Princípio das 3 camadas (fixado 2026-07-14)

Toda automação da wiki se aloca em três camadas, do mais barato ao mais caro:

| Camada | Quem | Quando | Custo |
|---|---|---|---|
| **0 — código** | `lint_wiki.py` (30 checks) | CI, **todo push** | grátis, instantâneo, é gate |
| **1 — LLM** | `/critica` · `/autocritica` | loop, em lotes, com teto | caro (Opus + verificação) |
| **2 — humano** | Gabriel | fila do §11 | **o recurso mais escasso do projeto** |

**A regra:** todo achado deve ser **produzido** pela camada mais barata capaz de produzi-lo, e **consumido** pela camada mais barata capaz de resolvê-lo.

O modo de falha é o trabalho **vazar para baixo**. A taxa de diferimento de 92% era exatamente essa medida: achado que nasceu na camada errada e desceu até o humano. O caso-tipo era o eixo 4 — um agente Opus derivava "falta wikilink a [[caridade]]", a preço de token, e o resultado ainda virava uma decisão do Gabriel. Duas camadas de desperdício no mesmo achado. Dos 45 itens do §11 que ele já fechou, **25 eram isso**.

Ao propor qualquer automação nova, a primeira pergunta é: *isto é decidível por código?* Se for, é lint — não é prompt.

### Itens

- [x] **Movimento 1 — eixo 4 sai da /critica e vira lint** (feito 2026-07-14) — `check_unlinked_concept_mention`: página-conceito existe, é nomeada na prosa de outra página, e não é linkada. É o espelho do `missing_concept_pages` (que só pegava link → página inexistente), e estava faltando. O eixo 4 foi **removido inteiro** do `critica-profunda.js` (schema `axis` agora é `[1,2,3]`): a metade "wikilink" virou este check; a metade "tag `tema/*`" já era coberta por `check_tag_coverage` (hoje em 0); e o resíduo ("candidato a mais uma tag") foi **descartado** — não vale token nem decisão humana.
  - **O sinal útil é TF-IDF, não "mencionou".** A versão ingênua rende **3198 achados em 768 páginas** — ruído que ninguém age. O check exige conceito **específico** (nomeado em ≤3% das páginas; acima disso é vocabulário ambiente como "orgulho"/"família") e **saliente** (≥2 menções na página): **64 achados em 54 páginas**, e a amostra é de cross-refs genuínos (`missao-de-kardec` nomeia "constituição do espiritismo" 10× sem linkar).
  - **Invariante travada por teste** (`tests/test_lint_unlinked_concept.py`, 8 testes): **nunca** sugerir wikilink dentro de citação literal (`>`) nem em texto-fonte (`capitulo-pentateuco`, `capitulo-biblico`, `livro-biblico`) — enfiar `[[...]]` no meio de Kardec adultera a fonte primária. Casa ignorando acento (o H1 de `conceitos/demonios.md` é "Demonios"; a prosa alheia escreve "demônios").

- [ ] **Movimento 2 — tirar do Opus o resíduo determinístico do eixo 3** — o eixo 3 (padrão editorial) mistura o que é código com o que é juízo. Já são lint: `check_fontes_section`, `check_frontmatter`, `check_citation_format`, `check_canonical_names`, `check_naming_consistency`; e a terminologia com `auto_fix=true` é tabela (`data/terminologia.json`), não juízo. Sobra para a LLM só o desvio de **tom/enquadramento**. Auditar o que o agente ainda deriva de eixo 3 que o lint já sabe, e cortar do prompt. Mesmo ganho do movimento 1, escala menor.

- [ ] **Movimento 3 — tirar o nível 0 do cron e o lint redundante do loop** — dois desperdícios estruturais em `scripts/loop-diario.sh`:
  1. `dreno.py promover` é determinístico e seu gatilho é um **evento** (o Gabriel marcar `[x]` no §11), não a passagem do tempo. Cron diário é o gatilho errado: a promoção deve ser passo do `/ship` (ou um check que reporta "N promovíveis"), não um lote noturno.
  2. O loop re-roda `lint_wiki.py` que o CI **já rodou no mesmo commit**, só para colar o resumo no corpo do PR. Duplicação pura.

  Feito isso, o loop passa a ter **exatamente um trabalho: rodar a camada 1** (a `/critica`) sobre o backlog, com teto — que é a única coisa que justifica um loop com orçamento de tokens.

- [ ] **Validação de deploy** — checar se o build do Quartz não quebrou links internos após deploy.
- [x] **`cite.py` não resolve itens `**N.**` em capítulos do ESE com subtítulos entremeados** (resolvido — verificado 2026-06-15) — `cite.py ESE "cap. X, item 13"` retorna o texto correto (linhas 1908-1910, a indulgência). Fechado pelos commits `24f77ac` (tolerância ao marcador em negrito `**N.**`) + `1494161` (resolução part-aware do range do capítulo). Coberto por `tests/test_cite.py`.
- [ ] **Versão estrita do check de citação** — verifica que o trecho citado **sustenta** a afirmação, não só que o locus existe.
  - **Destravado e construído (existência da aspa):** `check_literal_quote_exists` confirma que a frase entre aspas **existe** no locus citado (via `cite.py:literal_text` + cobertura fuzzy de palavras). Não dependia de granularidade no `raw/`. Entrou como **`info`, fora do CI e do hook** (aid de auditoria, não gate). Ver §12.
  - **Ainda bloqueado (sustentação semântica):** "Kardec diz X em (LE, q. 460)" quando q. 460 trata de Y permanece editorial — depende da granularidade por questão/item (§4 Fase 2). Atacado por via LLM no `/critica` (eixo 2), que não substitui a versão determinística estrita.
- [~] **Triagem das aspas literais fabricadas em `wiki/**`** — `check_literal_quote_exists` apontou **128 candidatos** (cobertura<0.5) na primeira passada wiki-wide; spot-check confirmou true-positives reais misturados a artefatos de extração (`cite.py` erra o bloco em capítulos de numeração irregular — ESE cap. XXVIII, C&I 2ª parte). **Resta a passada humana** de triagem dos 128 — converter as fabricadas em paráfrase ou citação ancorada. (Arquitetura completa em §12.)
- [ ] **Varredura de "cosmologia / cosmológic*"** — termo estranho ao registro doutrinário kardecista. Levantar ocorrências em `wiki/**`, avaliar caso a caso e substituir por formas próximas do registro espírita. Candidato a check `info`-level (`check_no_cosmologia`) se houver volume — análogo a `check_mundos_habitados_naming`.
- [ ] **Baseline de performance do build** — registrar tempo do build do Quartz e do `link_citations.py` em CI; alertar se regredir além de threshold (ex.: +50%).
- [ ] **Lint do pipeline pós-transform** — `check_broken_links` audita só o source; transforms de CI (`link_citations.py`, `wrap_glossary_terms.py`, `inject_copyright.py`) podem injetar wikilink quebrado em `/tmp/quartz/content` sem o lint pegar. Aplicar os transforms numa cópia e relintar (modo `--include-pipeline`). Trava regressão "transformer gera link quebrado".
- [ ] **`/autolint` com cap de iterações e gate humano** — slash command em loop `lint → categorizar → corrigir baixo risco → re-lint`, até zero findings ou 3 iterações, **pausando** quando o finding exige julgamento. Versão atenuada do "self-healing lint loop".
  - **Análogo-crítica construído:** `/autocritica` (`.claude/skills/autocritica/`) é o equivalente semântico — wrapper não-interativo e capped do `/critica`, drenando o backlog de páginas devidas em lotes via `/loop /autocritica`. Cap `--limit N` no lugar do gate de confirmação; doutrinário continua diferido a `rascunho` + ROADMAP §11. O `/autolint` (lado lint determinístico) segue aberto.
- [x] **`/dreno` — o contrapeso que fecha o que a crítica abre** (construído 2026-07-13) — `.claude/skills/dreno/`. **O problema que resolve:** a crítica difere em **~92%** das páginas (110 de 120 criticadas geraram diferido → `rascunho` + item no §11). Rodar `/autocritica` nas ~640 páginas restantes, nessa taxa, produziria ~590 novos rascunhos e ~590 itens de decisão humana — o loop enterraria o autor em vez de melhorar a wiki. O `/dreno` fecha: promove a `ativo` os rascunhos cujos itens do §11 já estão `[x]` (determinístico, zero tokens) e tria os rascunhos do `/ingest` em esboço vs candidata. Primeira passada promoveu 8 páginas; `rascunho_stale` caiu 152 → 144. **Duas invariantes travadas por `tests/test_dreno.py` — não afrouxar:** (1) **não bumpa `atualizado_em`** — bumpar faria a página casar o motivo `atualizado-apos-critica` do `critica_scope.py`, voltar à fila do Opus, ser diferida de novo e virar rascunho outra vez (moto-perpétuo que queima tokens sem mudar uma linha); (2) **slug ambíguo nunca promove** — o §11 mistura `**wiki/conceitos/x**` e `**x**`, e há slugs repetidos entre diretórios (`reencarnacao`, `alma-dos-animais`, `plenitude`).
  - **Bug corrigido em 2026-07-14 (auditoria adversarial):** a invariante (2) era **falsa na marca `[x]`**, e o teste que a "travava" só cobria o caso `[ ]`. O fan-out é simétrico: um item ambíguo ABERTO soma `abertos` em todas as homônimas e bloqueia todas (seguro), mas um item ambíguo FECHADO somava `fechados` em todas — e `fechados > 0` é justamente a condição de **promover**. O mecanismo vendido como salvaguarda era um amplificador: um único `[x]` seu, dirigido a UMA página, promovia TODAS as homônimas. A promovida por engano ia a `ativo` com diferidos doutrinários em aberto e, como o corpo não muda (`content_sha` bate) e `atualizado_em` não é bumpado, **nunca mais voltava à fila da crítica**. Conserto: contador `ambiguos` no `parse_roadmap_items` + **bucket F** (não-promovível), com teste do caso fechado. Estava a **um checkbox de disparar**: `- [ ] **alma-dos-animais**` é ambíguo e está aberto no §11 agora. Dano histórico: **zero** — as 8 promoções do commit `794929b` foram auditadas uma a uma e todas têm seu `[x]` próprio e não-ambíguo.
- [x] **Loop diário local** (construído 2026-07-13) — `scripts/loop-diario.sh` + `scripts/com.isabel.loop-diario.plist` (launchd, 9h). Cascata de custo crescente: nível 0 grátis (dreno determinístico + 29 checks do lint) roda sempre; nível 1 (sessão `claude -p /dreno N`) **só** é invocado se o nível 0 encontrar candidata. Dia sem trabalho custa **zero token**.
  - **Nunca toca no working tree.** Roda numa worktree dedicada (`.claude/worktrees/loop-diario`), resetada a `origin/main` a cada execução — não colide com trabalho em andamento nem acumula sujeira. O checkout principal é resolvido por `--git-common-dir` (resolver por `dirname $0/..` aninharia a worktree dentro de outra quando o script fosse chamado de dentro de uma).
  - **Entrega por Pull Request** — os **dois** níveis abrem PR que espera revisão humana. Os conjuntos de páginas são disjuntos (nível 0 mexe nos buckets C/E, nível 1 no bucket A), então as duas branches nunca conflitam.
  - **Por que PR e não push direto:** o ruleset "Protect main" exige pull request. É a mesma regra que mantém o `stats-daily.yml` desligado: o bot do Actions não está no bypass e leva GH013.
  - **O auto-merge do nível 0 foi REMOVIDO** (2026-07-14, auditoria adversarial). Ele se apoiava em dois fatos, e os dois eram falsos:
    1. *"O diff é só troca de `status:` — e isso é VERIFICADO."* O guarda (`so_troca_de_status`) **falhava aberto**: filtrava o diff com `grep -E '^[+-][^+-]'`, que descarta toda linha cujo conteúdo começa com `-` — isto é, **todo bullet em coluna zero**, e 639 páginas têm um (a lista do `## Fontes`). Reproduzido: uma citação adulterada junto da promoção passava como "só status". O guarda também era cego a arquivo novo não-rastreado, que o `git add -A` commitava em seguida.
    2. *"O leitor do site não vê diferença — `rascunho` já é público."* **Vê.** O `deploy-wiki.yml` copia `quartz-overrides/components/DraftNotice.tsx` para o build e o `quartz.layout.ts` o renderiza: `status: rascunho` estampa na página o aviso *"pode conter lacunas, seções incompletas ou citações não verificadas"*. Promover **apaga esse aviso do site público**.

    Somados: o único PR que entrava em main sem revisão era justamente o que removia o aviso de que a página não fora revisada — guardado por um guarda que não guardava. Bônus: o `gh pr merge --squash --delete-branch` era ele próprio uma armadilha (para apagar a branch local ele faz `git checkout main` dentro da worktree, onde o main já está checado no repo principal → `set -e` matava o script, e **o nível 1 nunca rodava nos dias em que o nível 0 mesclava**).
  - **Para religar o auto-merge** é preciso um verificador que valha o que promete: comparar `git diff --cached --name-status` (o que o `add -A` vai commitar, não o unstaged), exigir que todo arquivo seja `M` + `wiki/**/*.md`, e que a única diferença por arquivo seja a chave `status:`. Em Python, não em `grep` de diff unificado. **Enquanto isso não existir, os dois níveis esperam revisão.**

- [ ] **Loop: PR duplicado por dia enquanto você não mesclar (o pior modo de falha em aberto)** — a worktree reseta a `origin/main` todo dia e a triagem é determinística (`sorted(rglob)` + ordem por `atualizado_em` + corte nos N primeiros). Se o PR de nível 1 de ontem não foi mesclado, `origin/main` não mudou → **hoje o loop escolhe exatamente as mesmas 3 páginas**, paga os mesmos tokens e abre outro PR. 30 dias sem revisar = 30 PRs abertos sobre os mesmos 3 arquivos, todos conflitando entre si depois que o primeiro pousar. Não há nada que feche ou expire PR velho. **Conserto mínimo (1 linha):** antes de invocar o `claude -p`, sair se já houver PR aberto do loop — `[ "$(gh pr list --search 'head:loop/revisao- is:open' --json number -q length)" -gt 0 ] && exit 0`. Mata o gasto e o entulho de uma vez. Some sozinho se o **movimento 3** tirar o nível 0 do cron e o **item ★** reapontar o loop.

- [ ] **Loop: falha e ociosidade são indistinguíveis (nenhum canal de saída)** — os logs vão para `reports/loop-diario/`, que é **gitignored**: nunca são commitados, empurrados nem enviados. Não há `osascript`/notificação/e-mail. E como o nível 0 tem **0 promovíveis** hoje, "nenhum PR hoje" *é o dia normal esperado* — que é exatamente o sintoma de keychain bloqueado, `gh` sem auth ou `claude` fora do PATH. Um loop morto há três semanas é indistinguível de um loop saudável e ocioso. **Conserto mínimo:** trap que notifica no erro (`trap 'rc=$?; [ $rc -ne 0 ] && osascript -e "display notification ..."' EXIT`) + heartbeat (avisar se o log mais recente tiver >48h).

- [ ] **Loop: `set -e` mata o script sem deixar rastro** — em `scripts/loop-diario.sh`, `(cd "$WT" && gh …) && log "sucesso"`: se o comando falha, a lista devolve não-zero → `set -e` mata ali, e como o `log` é o lado direito do `&&`, **nenhuma linha é escrita**. Mesma classe: `uv run … | tee` sob `pipefail` (um crash do dreno mata o dia e o traceback morre num log que ninguém lê); e `lint_wiki.py` sai 1 quando há erro, então o `|| echo "lint não rodou"` **engole exatamente o caso em que a wiki está quebrada**. Adicionar `trap 'log "ERRO na linha $LINENO"' ERR` e `|| log "ERRO: …"` nos pontos de falha.

- [ ] **Loop: robustez do git (3 itens pequenos)** — (a) `git worktree add` só é tentado se o diretório não existe; se ele for apagado à mão sem `git worktree prune`, o `add` falha com *"missing but already registered worktree"* e o loop **morre todo dia** até intervenção manual → rodar `worktree prune` antes. (b) `git fetch` sem `--prune`: depois de um PR mesclado com `--delete-branch`, a ref remota fica obsoleta e o push do dia seguinte é rejeitado com *stale info*. (c) branch nomeada só pela data colide se o loop rodar 2× no mesmo dia (`gh pr create` falha → `set -e` mata) → sufixo de hora/sha, e `gh pr create || gh pr edit`.

- [ ] **Loop: a trava tem TOCTOU e pode deadlockar em silêncio** — entre o `mkdir "$LOCK"` e o `echo $$ > "$LOCK/pid"` há uma janela em que o dir existe e o pid não; quem chegar nela lê `DONO="?"`, conclui "trava órfã" e faz `rm -rf` na trava **viva** do primeiro (reproduzido: os dois entraram na seção crítica). E um `kill -9` deixa a trava para trás; se o PID for reciclado por outro processo, `kill -0` sucede → o loop diz "já há um loop rodando", sai 0, e **nunca mais roda**, em silêncio. Gravar o pid como parte da aquisição, e guardar também timestamp + nome do processo.

- [ ] **Dreno: os baldes D e X nunca drenam, e ninguém os vê** — o `anatomia` reporta hoje 1 página em **D** (a crítica diferiu, mas não há item no §11 — rastro perdido) e 1 em **X** (corpo alterado depois da crítica — veredito obsoleto). Nenhum dos dois tem mecanismo de drenagem, e o `loop-diario.sh` não os surfa. São poucos hoje; crescem em silêncio. Fazer o loop reportá-los, e definir o dono de cada um (D → humano confere; X → devolver à fila da `/critica`).

- [ ] **Dreno: os 21 esboços do bucket A não são trabalho de ninguém** — dos 78 rascunhos do `/ingest`, 57 são "candidata" (o loop revisa) e **21 são esboço** — falta escrita, não promoção. Estão explicitamente fora do escopo do `/dreno` (`SKILL.md`: "não é trabalho do dreno: anotar no §10.3 e seguir"). Ou seja: as páginas que **mais** precisam de melhoria são as únicas que nenhuma automação toca. Cruza com §10.3.

- [ ] **Dreno: o agente do nível 1 refaz o que o código já fez** — o prompt manda o Haiku conferir "tem `## Fontes`? afirmações citadas?" — mas `dreno.py completude()` já calculou os dois deterministicamente antes de invocá-lo (e `check_fontes_section` + `check_low_citations` já rodam no CI). Sobra de irredutivelmente-semântico só "nada visivelmente incompleto / tom do projeto". Estreitar o prompt para isso. É o princípio das 3 camadas aplicado ao próprio dreno.
- [ ] **★ PRIORITÁRIO — Reapontar o loop: entregar DECISÃO PRONTA, não pedido de revisão** (aberto 2026-07-14, após auditoria adversarial dos commits do loop) — **o loop diário, como está, não remove o gargalo humano; ele o reposiciona.** Antes o Gabriel rodava a skill; agora ele revisa um PR. A vazão da wiki continua sendo a vazão dele.

  **O diagnóstico, com números medidos em 2026-07-14:**
  - O nível 0 (grátis, determinístico) tem **0 páginas promovíveis** — e não é acidente de calendário: ele só promove o que tem `[x]` no §11, e **nada no repositório escreve `[x]`** (`critica_apply.py` só emite `[ ]`). O único produtor de `[x]` é o humano. O balde que o loop drena de graça só enche na velocidade dele.
  - O nível 1 tem 57 candidatas, mas o PR **espera revisão** e a worktree reseta a `origin/main` todo dia. Sem merge, a triagem é determinística e **amanhã escolhe as mesmas 3 páginas** → um PR duplicado por dia, para sempre.
  - **O loop não roda `/critica` nem `/autocritica`** — a única coisa que melhora conteúdo está fora dele. 701 páginas devidas continuam devidas.
  - Colocar o `/autocritica` no loop **pioraria**: a 92% de diferimento, as 701 devidas abrem ~645 rascunhos + ~645 itens `[ ]` que só o humano fecha. O `/dreno` não fecha dívida — ele **colhe** decisões já tomadas. "Contrapeso" superestima o que ele faz.

  **A alavanca (onde o gargalo realmente está):** dos 133 itens `[ ]` abertos no §11 — 55 são eixo 2 (citação não sustenta a afirmação), 25 eixo 3, 41 sem eixo, e só 12 eixo 4. Mas dos **45 já fechados, 25 eram eixo 4** — polimento mecânico. Mais da metade do tempo de decisão gasto até hoje foi aprovando "adicionar wikilink a [[caridade]]" enquanto os 55 achados de eixo 2 esperavam. (Metade disso já foi cortada — ver o item do eixo 4 abaixo.)

  **O que construir:** em vez de "promover rascunhos e pedir revisão", o loop deve **preparar a decisão**. Para cada item do §11 (eixo 2 primeiro): rodar `cite.py`, trazer o texto literal do locus ao lado da afirmação da página, e **redigir o conserto proposto**. O ato humano vira aprovar/rejeitar em vez de investigar. É isso que converte julgamento escasso em `[x]` a taxa alta — e aí o `/dreno` colhe sozinho, que é para o que ele foi feito. Hoje o loop automatiza a colheita e deixa a semeadura com o humano: está invertido.

  Cruza com: "Triagem barata antes do Opus" e "Taxa de diferimento" (abaixo), §11 e §10.3.

- [ ] **git-lfs: 18 arquivos em `raw/assets/` estão commitados como bytes crus, não como ponteiros** — toda operação de worktree/reset cospe `Encountered 18 files that should have been pointers`. Pré-existente, não-fatal, mas polui o log do loop diário. Corrigir com `git lfs migrate import --include="raw/assets/*"` (reescreve histórico — combinar antes).
- [ ] **Triagem barata antes do Opus (nível 1 da cascata)** — hoje o `critica_scope.py` ordena as devidas por `(motivo, tipo, atualizado_em, path)`: varredura cega, sem sinal de suspeita (é por isso que o próximo lote são 5 `parabola-do-*` em ordem alfabética). Com 701 páginas devidas, isso são ~140 lotes de Opus gastos igualmente em página boa e ruim. Propor: usar os achados do lint (grátis) + um agente Haiku por página como **pré-filtro de suspeita**, e só o que passar sobe ao Opus. Corta o custo do backlog em ~5-6×.
- [~] **Taxa de diferimento de 92% é alta demais** — investigar se o critério "na dúvida, diferir" está capturando achado cosmético (tag faltando, cross-ref opcional) como se fosse doutrinário. Um diferimento deveria custar uma decisão humana; hoje custa pouco demais para quem difere e muito para quem drena. Cruza com o §11.
  - **Confirmado e parcialmente atacado (2026-07-14).** A suspeita estava certa, e era pior do que parecia: dos **45 itens do §11 já fechados, 25 eram eixo 4** (tag/wikilink) — mais da metade do tempo de decisão humana gasto em polimento mecânico, enquanto **55 achados de eixo 2** (citação que não sustenta a afirmação) esperavam na fila. A causa estava no prompt: o `PASSO 5` do `critica-profunda.js` mandava eixo 3 **e eixo 4** "direto a diferir", e o fecho "na dúvida, `deferred`" dava ao agente a saída fácil.
  - **Conserto aplicado:** o eixo 4 foi **removido inteiro** da crítica e virou lint (movimento 1, acima) — não é mais questão de "auto-aplicar em vez de diferir": a camada cara simplesmente **não deriva mais** o que um grep resolve. O prompt agora manda ignorar wikilink faltando, e o schema `axis` só aceita `[1,2,3]`. Os SKILLs passaram a dizer, nas duas pontas, o que um diferido **custa** (rascunho + item que só o Gabriel fecha) e a instruir: na dúvida entre diferir e não reportar, não reporte o que não muda o que a página *afirma*.
  - **Falta medir:** rodar um lote e conferir a nova taxa. A hipótese é que ela caia bem abaixo de 92%, mas isso é **previsão, não medição**. E os **41 itens "sem eixo"** do §11 ainda não foram classificados — podem esconder mais polimento. Classificá-los é pré-requisito para saber se a taxa caiu de verdade ou se só mudou de nome.
- [ ] **Conserto manual de diferido devolve a página à fila cara** — ao resolver um item do §11 à mão, o corpo muda → `content_sha` diverge → a página reentra na fila do `/critica` como `corpo-alterado` (39 páginas nessa situação hoje). É defensável (revalidar o conserto), mas é um default caro. Avaliar um `record --touch` que revalide sem Opus quando o diff for pequeno.

---

## 6. Busca e navegação avançada

- [ ] **Pagefind** — substituir ou complementar o flexsearch do Quartz por [Pagefind](https://pagefind.app/); índice estático no build, browser sem backend. (Busca local do autor via qmd já feita — ver [Concluído](#concluído).)
- [ ] **Índice por conceito-raiz** — hierárquico, refletindo a estrutura conceitual da doutrina (Deus > Leis Divinas > Lei de Causa e Efeito > ...).

---

## 7. Ferramentas de estudo e difusão

- [ ] **Automatizar a colocação de imagem no deck (`/slides`)** — o *sourcing* já está pronto (estágio **Iconografia** do `/palestra` + `convencoes-imagens.md`); falta automatizar a **colocação**, hoje manual no Passo 6. Alvo: `scaffold_deck.py` (ou um passo novo no `/slides`) lê a seção "Sugestões de imagem" do dossiê (`reports/palestra/<slug>/dados.json`, campo `iconografia`), o humano **escolhe** o candidato por momento-chave, e o script baixa p/ `slides/<slug>/assets/`, otimiza, emite o `![bg]` e grava `creditos.json`. Humano-no-circuito na escolha (o modelo não vê a imagem).
  - **Descobertas (sessão 2026-06-15, deck `slides/indulgencia/`, validado renderizando o PDF):**
    - **Legibilidade:** o tema `isabel.css` é texto escuro sobre fundo claro → **`![bg]` full-bleed atrás de texto fica ilegível**. Padrão que funciona: **split background** (`![bg right:43%]` / `![bg left:45%]`) — texto no fundo claro, arte ao lado. Slides de pergunta (`.pergunta`) ficam **sem imagem** (a pergunta grande centralizada já é o impacto).
    - **Build:** `build_deck.py` já passa `--allow-local-files` (necessário p/ bg local); PPTX/PDF exigem **`CHROME_PATH`** (Chrome for Testing do puppeteer) — ver memória `setup-marp-chrome-path`.
    - **Download:** Wikimedia exige **User-Agent** no `curl` (senão 403); otimizar com `sips -Z 1800` (originais chegam a ~9000px → ~430–900 KB).
    - **Capacidade do slide:** ~5 bullets longos **transbordam** (32px, padding 80/100) — colidem com o rodapé. O passo de colocação/refino deve dividir conteúdo longo (ex.: síntese em 2 slides). → promovido a item próprio abaixo (`check_slide_overflow`).
    - **Cobertura default** = momentos-chave (capa/abertura, casos/"Para meditar", síntese/encerramento); o núcleo Q&A fica tipográfico.
- [x] **Ver o tema sem gastar uma palestra — `slides/themes/preview.md` + lint de overflow** ✅ **(2026-07-27)** — hoje o único jeito de inspecionar o `isabel.css` (125 linhas) é buildar um deck inteiro: as descobertas de legibilidade e de capacidade do slide registradas acima custaram uma palestra real (`slides/indulgencia/`) e só apareceram ao renderizar o PDF. Dois passos, ambos **camada 0**:
  - **(a) Deck de demonstração** ✅ **feito (2026-07-27)** — `slides/themes/preview.md`: 11 slides (capa com `![bg right:43%]`, `.pergunta` curta e no limite, `.section`, Q&A tipográfico, `.quote` curta e no limite, split `![bg left:45%]` com crédito no rodapé, síntese que cabe × síntese que transborda, espécime tipográfico, checklist). O `_header` de cada slide diz o que ele testa. Fixture sintético em `themes/assets/` (gradiente na paleta; `creditos.json` registra que não é obra de terceiros). Build: `build_deck.py slides/themes/preview.md --formats pdf`.
    - **O que o preview achou já na primeira rodada — e que foi consertado no mesmo dia.** Os três eram drift herdado do `@import 'default'` do Marp, que o `isabel.css` nunca sobrescreveu; todos declarados lá com `light-dark()`, isto é, **a cor dependia do color-scheme da máquina que buildava**. Corrigidos por 5 linhas de token em `section` + `section.section`:
      - **`h1` saía azul-marinho** (`--h1-color: #246`) — o elemento mais visível do deck, o título da capa, estava fora da paleta desde sempre. Agora `var(--isabel-fg)` (decisão do Gabriel, 2026-07-27: o verde accent continua sendo a voz exclusiva de h2/`.pergunta`/`.quote`).
      - **Negrito dentro de heading saía azul-claro** (`--heading-strong-color: #48c`) — já acontecia em produção, em `slides/bem-aventuranca-dos-misericordiosos/deck.md:11`. Agora accent (o Marp força `font-weight: inherit` em `strong` dentro de heading, então a cor é a única marca de ênfase disponível).
      - **Paginação a `#777` não era sobrescrita na `.section`** — número de página cinza-médio sobre o verde accent. Agora claro, como header e footer.
    - **Rebuildar os decks antigos** se algum for reapresentado: o `build/` é gitignored, então os PPTX/PDF em disco ainda têm a capa azul.
  - **(b) `check_slide_overflow`** ✅ **feito (2026-07-27)** — severidade `info`, em `lint_wiki.py`, sobre `slides/**/*.md` com `marp: true`. Não conta linhas por heurística: reconstrói a caixa de cada bloco a partir do CSS que o Marp gera (line-height 1.25 em heading e 1.45 no corpo, margens que **colapsam** — somá-las inflava ~60 px e dava falso positivo), estreita a coluna quando há split background, e compara com os 560 px úteis.
    - **Calibragem medida, não estimada**: a razão largura-do-glifo/font-size saiu de resolver, contra 13 contagens de linha observadas no PDF do preview, a faixa consistente com todas — sans [0,474; 0,502], serif [0,326; 0,397]. O resultado bate com o render dentro de ~2% nos quatro slides medidos. `tests/test_lint_slide_overflow.py` (13 testes) trava isso: se alguém mexer na geometria, quebra o teste em vez do projetor.
    - **Achados na estreia, os dois conferidos no PDF**: `bem-aventuranca-dos-misericordiosos` slide 43 (síntese de 5 bullets — o último **encosta no rodapé**, que é exatamente o modo de falha descrito acima) e `indulgencia` slide 2 (`.pergunta` de 30 palavras que invade o cabeçalho). Zero falso positivo em ~200 slides de 7 decks.
    - Slide que transborda de propósito declara `<!-- lint: overflow-esperado -->` — usado no slide de calibragem do preview.
  - **Descartado (avaliação 2026-07-27):** mover a identidade visual dos slides para um design system externo (Claude Design / `claude.ai/design`). É repositório de biblioteca de componentes HTML com cards de preview — não renderiza PPTX/PDF (o Marp continuaria necessário), quebra o offline-first exigido pelo projetor da casa (`convencoes-imagens.md`), tira o deck do markdown versionado que dá alcance ao `cite.py`, e move para a **camada 2** (revisão humana, o recurso mais escasso) uma consistência que 125 linhas de CSS já garantem na camada 0. Escala não justifica: 4 tipos de slide, 1 consumidor, 1 pessoa.
- [~] **Mapas conceituais** — Mermaid validado como zero-plumbing (Quartz v4.4.0 renderiza ` ```mermaid ` nativo via OFM, tema-aware; transforms pulam blocos cercados). Convenção em `convencoes-mermaid.md`; smoke-test em `hierarquia-de-autoridade.md`. **Faltando:** lint `check_mermaid_labels` (drift de nomenclatura em rótulo); skill `/mapa` qmd-driven e/ou derivação automática do grafo networkx do `/stats`.
- [ ] **Export temático** — PDF/EPUB de um conjunto de páginas sobre um tema, para estudo offline.
- [ ] **Flashcards** — pares pergunta/resposta a partir de `questoes/` para revisão espaçada (Anki-compatível).

---

## 8. Governança e direitos autorais

Kardec (m. 1869) e Léon Denis (m. 1927) estão em domínio público; Chico Xavier, Emmanuel, André Luiz, Bezerra, Divaldo, Joanna, Hammed **não** estão. Política de citação, aviso ao leitor, frontmatter `direitos:` e exclusão de `raw/` do build — todos entregues (ver [Concluído](#concluído)).

- [ ] **Auditoria de conteúdo gerado por LLM** — `/ingest`, `/slides` e `/stats` produzem texto que entra na wiki. Em 12-24 meses, se a base for citada por terceiros, distinguir "Kardec disse X" de "síntese gerada" importa. Opções: campo `revisao_humana:` (data), marcação em rodapé, ou `## Notas` em sínteses. **Adiada para fase 2** — `/ingest` já tem humano-no-circuito; ganho marginal hoje é baixo.

---

## 9. Eficiência de tokens no workflow

Eixo essencialmente fechado (cinco frentes da auditoria de 2026-05-02 entregues — ver [Concluído](#concluído)). Itens descartados: validação explícita de prompt caching (Claude Code já cacheia 5min), `references/` carregado sob demanda nas skills (não é prioridade até SKILL.md passar de 200 linhas).

---

## 10. Varredura de backlog (snapshot operacional)

Descobertas concretas do `/stats` + `/lint` que apontam **páginas a escrever** (não-ingest). Cruza com os eixos §1, §3 e §4 — esta seção é o instantâneo operacional; a estratégia segue lá.

### 10.1 Cobertura doutrinária — blocos do LE sub-cobertos

Medição 2026-05-26 (LE 385/1019 = 37.8%):

| Bloco | Cobertura | Prioridade |
|-------|-----------|------------|
| 301–400 | 16% | 🔴 alta — intervenção dos espíritos, influência oculta |
| 501–600 | 20% | 🔴 alta — retorno à vida corporal, união alma/corpo |
| 401–500 | 21% | 🟡 média — retorno à vida espiritual, sensações pós-morte |
| 201–300 | 29% | 🟡 média — emancipação da alma, sonho/sonambulismo |
| 1–100 | 35% | 🟢 baixa — primeiros princípios (já citados, faltam Q&A próprias) |

Sub-cobertura no LM (28/33 caps. 2ª parte citados) e Gênese (15/18). Identificar quais 5 caps. de LM e 3 de Gênese ficaram fora.

- [ ] **Extrair 5 questões-chave do LE 301–400** em `wiki/questoes/`.
- [ ] **Extrair 5 questões-chave do LE 501–600** em `wiki/questoes/`.
- [ ] **Extrair 3 questões-chave do LE 401–500** em `wiki/questoes/`.
- [ ] **Levantar caps. LM/Gênese sem ancoragem** (script ad-hoc cruzando regex de citação com `kardec-mapping.json`).

### 10.2 Páginas-índice bíblicas — stubs órfãs

Os 27 `wiki/biblia/<livro>/index.md` (`tipo: livro-biblico`) foram criados mas **seguem como stub de ~15 palavras**, todos órfãos no grafo. Esquema mínimo em `convencoes-frontmatter.md`: H1, nota breve (autor tradicional, ocasião, contexto histórico), lista de capítulos como wikilinks, cross-link para `wiki/obras/<evangelho/epístola>`.

- [ ] **Expandir 4 índices de Evangelhos** (`joao`, `lucas`, `marcos`, `mateus`) — mais alta prioridade pelo peso doutrinário.
- [ ] **Expandir índice de Atos e Apocalipse**.
- [ ] **Expandir 13 índices de epístolas paulinas + Hebreus**.
- [ ] **Expandir 7 índices de epístolas católicas** (`tiago`, `1/2-pedro`, `1/2/3-joao`, `judas`).

Cada índice destrava backlink dos capítulos correspondentes (resolve em parte os órfãos da varredura).

### 10.3 Rascunhos > 14 dias — promoção a `ativo`

**Agora automatizado pelo `/dreno`** (§5). A anatomia de 2026-07-13 desmontou a premissa de que "rascunho parado = dívida da crítica" — rodar `uv run python .claude/skills/dreno/scripts/dreno.py anatomia` para o número do dia. Dos 158 rascunhos medidos:

| Bucket | Qtd | O que é | Ação |
|---|---|---|---|
| **A** | 78 | nunca-criticada — rascunho do `/ingest`, **não** é dívida da crítica | triagem do `/dreno` |
| **B** | 70 | diferido **aberto** no §11 | `rascunho` correto — não tocar |
| **C** | 8 | diferido **fechado** no §11 | ✅ promovidas 2026-07-13 |
| **D** | 1 | crítica diferiu, sem item no §11 (`sinteses/logoterapia-e-espiritismo` — está no §11 como nota em prosa, não como `- [ ]`) | rastro perdido |
| **X** | 1 | corpo alterado após crítica limpa (`aprofundamentos/reencarnacao`) | devolver ao `/critica` |

O bucket **A** (o que esta seção sempre quis dizer) se divide, por sinais determinísticos, em **57 candidatas** (tem `## Fontes`, ≥250 palavras, ≥1 citação — pronto para o agente barato confirmar e promover) e **21 esboços reais** que precisam de *escrita*, não de promoção:

- **Personalidades**: `gregorio`, `druso`, `silas`, `ernesto-fantini`, `alexandre`, `aniceto`, `jeronimo-assistente`.
- **Obras**: `acao-e-reacao`, `os-mensageiros`, `missionarios-da-luz`.

(As páginas de personalidade citam no formato `(Autor, *Obra*, cap.)`, não por sigla do Pentateuco — a triagem conta **as duas** formas. Contar só as siglas rotulava `clarencio` — 682 palavras, Fontes, 7 citações — como esboço.)

### 10.4 Aprofundamentos sugeridos por massa de vocabulário

- [ ] **`wiki/aprofundamentos/atributos-de-deus`** — `deus` é #1 (3855 ocs). Base: LE Parte 1 + ESE cap. I-III.
- [ ] **`wiki/aprofundamentos/lugar-do-homem-na-criacao`** — `homem` (1574), `mundo` (1116), `terra` (1100). Base: LE q. 132–144, Gênese cap. XI.
- [ ] **`wiki/aprofundamentos/morte-corporal-e-passagem`** — `morte` (1223). Base: LE q. 154–165, C&I 1ª parte cap. III.

### 10.5 Sínteses panorâmicas faltantes

- [ ] **`wiki/sinteses/cristo-na-doutrina`** — `cristo` (1697) top-10 sem síntese-âncora. Articular Jesus enquanto Guia, Modelo e Governador da Terra cruzando ESE, Gênese cap. XV e C&I.
- [ ] **`wiki/sinteses/serie-andre-luiz`** — bigrama #1 (`andré luiz`, 496 ocs). Arco-narrativo dos 16 livros, leitura recomendada, lar canônico (Nosso Lar) como porta de entrada.

### 10.6 Órfãs prioritárias a integrar

- [ ] **`wiki/personalidades/arthur-conan-doyle`** — órfã + drift de nomenclatura ("Conan Doyle", "Sir Arthur Conan Doyle").
- [ ] **`wiki/conceitos/sonhos`** — órfã apesar de atravessar emancipação da alma (LE q. 400–418).
- [ ] **`wiki/aprofundamentos/silencio-interior-o-ser-consciente`** — órfã (também em §11).

---

## 11. Crítica profunda — itens diferidos a decisão humana

> Itens levantados por `/critica` que exigem julgamento doutrinário (não auto-corrigíveis). **Relatório do lote 2026-06-03**: `reports/critica/2026-06-03-1903/`. Eixos: cit=citação · edit=editorial · tag=tags/links.
>
> **Nota 2026-06-04 — cluster "q. 1009/1015–1019" é falso-positivo de lacuna de corpus.** Vários itens acusavam citações a LE q. 1009 e q. 1015–1019 como "fabricadas/inexistentes". Diagnóstico corrigido: essas questões **existem** (são as finais do LE); o `raw` as traz em numeração dupla `<Kardec> [<sequencial>]` porque Kardec saltou o nº 1011 — e o `cite.py` não reconhecia o formato. **Raiz consertada** (`scripts/cite.py`, +3 testes; commit `5c28452`): q. 1012–1019 resolvem pelo nº de Kardec. **Os loci q. 1009 e q. 1015–1019 são legítimos — NÃO removê-los.** Resíduo real e menor (eixo editorial): em algumas páginas o texto rotulado "síntese/paráfrase" está formatado como blockquote com aspas (estilo que simula verbatim); polir. Ver memória `le-corpus-gap-q1011-1019`.

> **Nota 2026-07-12 — intervalo `q. 873-919` da Lei de Justiça, Amor e Caridade atravessa fronteira de capítulo (achado sistêmico, PENDENTE).** Levantado pela verificação adversarial do run `reports/critica/2026-07-12-2146/` (página `sinteses/logoterapia-e-espiritismo`). **O fato** (confirmado no `.index.md` do LE e via `cite.py`): **Cap. XI — Lei de justiça, de amor e de caridade = q. 873–892**; **Cap. XII — Da perfeição moral = q. 893–919**. **O problema**: a rule `.claude/rules/convencoes-tags.md` registra `lei/justica-amor-caridade` como "q. 873-919", engolindo o Cap. XII inteiro — e esse intervalo **já se propagou para 27 linhas em 13 arquivos** da wiki, citado como locus da Lei. A ocorrência mais explícita (`aprofundamentos/fora-da-caridade-nao-ha-salvacao.md:57`) afirma textualmente *"No LE, Parte 3, **Cap. XI** … (q. 873-919)"* — factualmente errado. **Cuidado**: os usos de **q. 893–919** para conteúdo do Cap. XII (`egoismo`, `homem-de-bem`, `perfeicao-moral`, `orgulho`, `dor-rigidez` e outros — 13 arquivos) estão **corretos, não tocar**. **Proposta em 3 partes**: (1) rule → `q. 873-892 (cap. XI)` + nota de que o Cap. XII recebe a tag por extensão temática (preserva as 125 páginas tagueadas); (2) corrigir as 27 ocorrências que apresentam 873-919 como locus do Cap. XI; (3) check de lint **data-driven** que sinalize intervalo de questões atravessando fronteira de capítulo do LE, derivado do `.index.md` (nada hardcoded) — teria pego este erro e os 27 anteriores. **Diferido a sessão própria** (escopo transversal: rule + 13 arquivos + lint; não misturar com o ingest da página que o revelou). Diagnóstico completo e post-mortem da sessão: `reports/post-mortem/2026-07-12-sessao-logoterapia.md`.

O lote anterior (2026-05-31, 28 itens) está **100% resolvido** — ver [Concluído](#concluído).

### aprofundamentos/
- [ ] **expiacao-e-arrependimento** (edit,tag; 2) — L96 atribui a *Gênese* uma citação que é de ESE.
- [ ] **missao-de-kardec** (cit; 3) — aspa "A revelação espírita não foi feita só por intermédio de um homem…" — conferir locus (ESE Introd. II §49 / Gênese I,13).
- [ ] **sexualidade-em-emmanuel** (cit; 1) — tese "consciências livres" ancorada em LE q. 622 vs q. 843 / Lei de Liberdade.
- [ ] **criacao-do-planeta-terra** (cit; 1) — blockquote "literal" de Gênese cap. X item 17 (princípio vital).
- [ ] **sexualidade-em-andre-luiz** (cit,edit,tag; 4) — ancoragem + "kardequiano/a" em 4 pontos (cruza §13).
- [ ] **aborto** (edit; 1) — L170 ordem de palavras truncada ("moldura de Kardec ampla").
- [ ] **dor-rigidez** (cit,edit; 3) — autoexame "Que fiz do orgulho e da vaidade?" atribuído a ESE cap. XVII / LE Conclusão.
- [ ] **silencio-interior-o-ser-consciente** (cit,edit; 6) — comentário à q. 919 atribuído a Kardec (é Santo Agostinho) + 5 achados.
- [ ] **sofrimento-em-joanna-de-angelis** (cit,edit; 2) — "agradecer pelas provas" ancorado em ESE cap. XIV vs cap. V/III.
- [ ] **escolha-de-provas** (cit; 2) — aspa "literal" de LE q. 984–985 não casa.
- [ ] **sexualidade-em-joanna-de-angelis** (cit,edit; 3) — tese clínica de Camazão ancorada em LE q. 155.
- [ ] **fora-da-caridade-nao-ha-salvacao** (cit; 1) — range "LE q. 873–919" cruza cap. XI e XII.
- [ ] **por-que-mediuns-falham** (edit; 1) — L150 rótulo de Otávio "(suicídio inconsciente)" diverge do corpo.
- [ ] **decisoes-de-vida-e-providencia** (cit; 1) — Mt 6:33 atribuída a ESE cap. XXV.

### divergencias/
- [ ] **celibato-como-ideal-paulino** (cit; 1) — ESE cap. XXVII item 4 sustenta "graça proporcional ao chamado individual"?
- [ ] **pecado-original-em-romanos-5** (cit; 3) — LE q. 612 (afeições) vs q. 621/q. 642.
- [ ] **recaida-sem-arrependimento-em-hebreus** (cit,edit; 3) — **FP q. 1009/1015–1016 (legítimas)**; resíduo: blockquote estilizado como literal + ancoragem q. 171.
- [ ] **uma-morte-e-juizo-em-hebreus-9** (cit; 2) — "juízo" pós-morte ancorado 3× em C&I 1ª parte cap. II.
- [ ] **sangue-expiatorio-em-1-joao** (cit; 5) — **FP q. 1015–1019 (legítimas)**; resíduo: blockquote "Q. 636" com pergunta/resposta não-literal + outros.
- [ ] **sangue-expiatorio-em-1-pedro** (cit,tag; 3) — **FP q. 1015–1019 (legítimas)**; resíduo: tag.
- [ ] **escravidao-em-efesios-6** (cit; 3) — blockquote de LE q. 825 fabricado.
- [ ] **predestinacao-em-romanos-8-9** (cit,edit; 4) — **FP "Q. 1009" (legítima)**; resíduo: blockquote estilizado como literal.
- [ ] **sangue-expiatorio-em-galatas** (cit; 3) — **FP cluster**; resíduo: blockquote ESE cap. XXVII item 14 não confirmado.
- [ ] **sujeicao-conjugal-em-efesios-5** (cit,edit; 3) — comentário à q. 822 como blockquote com texto alterado.
- [ ] **diabo-ontologico-em-apocalipse** (cit,edit; 5) — blockquote "literal" de LE q. 131 (pergunta/resposta divergem).
- [ ] **jesus-igual-a-deus-em-filipenses-2** (cit; 2) — **FP cluster**; comentário "literal" à q. 625 — conferir.
- [ ] **penas-eternas-em-apocalipse** (cit,edit; 2) — **FP q. 1015–1019 (legítimas)**; resíduo: range "universalidade do progresso".
- [ ] **anjos-rebeldes-em-2-pedro-2** (cit; 5) — blockquote "literal" de LE q. 131.
- [ ] **mudanca-de-sexo-reencarnacao** (edit; 2) — "kardequiano/a" repetido (cruza §13).
- [ ] **continuidade-do-principio-inteligente-ate-o-homem** (edit; 1) — classificação "não é divergência estrutural, é adoção de um dos dois sistemas".
- [ ] **condenacao-dos-incredulos-em-marcos-16** (cit,tag; 2) — paráfrase de LE q. 621 ("lei inscrita em todo coração").
- [x] **fogo-eterno-em-mateus-25** (tag; 1) — candidato a 3º `tema/*` (Jesus/vida-futura). · ✓ resolvido 2026-06-17 (tema/jesus adicionada)
- [ ] **morte-de-ananias-e-safira** (edit,tag; 2) — enquadramento crítico-textual (Formgeschichte) co-igual à divergência doutrinária.
- [ ] **sinais-de-marcos-16** (cit,tag; 3) — "novas línguas" atribuída a LM cap. XIX vs cap. XVI item 189.

### questoes/
- [ ] **paternidade-como-missao** (cit; 3) — aspa "A semente mais fecunda é o exemplo" (ESE cap. XIV item 9).
- [ ] **por-que-a-acao-dos-espiritos-e-oculta** (cit; 4) — aspa "o mérito está na luta" (LE q. 843).
- [ ] **arrependimento-expiacao-e-reparacao** (cit; 1) — blockquotes "literais" divergem da tradução FEB citada em Fontes.
- [ ] **o-que-devemos-pedir-na-prece** (edit; 1) — prece "pode verbalizar o desejo concreto" vs ESE cap. XXVII item 22.
- [x] **obediencia-e-resignacao** (tag; 1) — candidato a `tema/livre-arbitrio`. · ✓ resolvido 2026-06-17 (tema/livre-arbitrio adicionada — 3 tema/*)
- [x] **transicao-do-principio-inteligente** (tag; 1) — Léon Denis/André Luiz sem wikilink-personalidade. · ✓ resolvido 2026-06-17 (wikilinks [[leon-denis]] e [[andre-luiz]] na prosa)
- [x] **esquecimento-do-passado** (tag; 1) — "registro perispirítico" sem link a `perispirito`. · ✓ resolvido 2026-06-17 (wikilink [[perispirito]] na l.116)
- [ ] **a-infancia-e-o-veu-da-inocencia** (edit; 1) — ênfase "sobretudo" atribuída a Kardec (q. 385).
- [ ] **unicidade-do-espirito** (tag; 1) — "individualidade" como termo central sem conceito (≠ `individuacao`). · NOTA 2026-06-17: sem alvo (individualidade não existe, ≠ individuacao); requer criar página ou decidir não-linkar — diferido.
- [ ] **alma-dos-animais** (cit,tag; 2) — "crueldade contra animais ofende Deus" (LE q. 750, q. 752).
- [ ] **espiritos-e-as-leis-da-natureza** (cit,edit; 2) — "morte tem momento fixado" simplifica demais q. 853.
- [ ] **o-que-e-deus** (cit,tag; 3) — "sete atributos clássicos listados na q. 13".
- [x] **pactos-com-satanas-como-alegoria** (tag; 1) — "Negação das penas eternas" sem wikilink. · ✓ resolvido 2026-06-17 (wikilink [[penas-eternas]] na l.58)

### sinteses/
- [ ] **veracidade-das-mensagens-psicografadas** (cit,edit; 2) — atribuição do "Controle Universal do Ensino dos Espíritos".
- [ ] **hierarquia-de-autoridade** (edit,tag; 3) — formas proibidas "kardequiana"/"kardeciana" (cruza §13).
- [ ] **parabolas-de-jesus** (cit,edit; 3) — tesouro escondido/pérola atribuída a ESE cap. XVI.
- [ ] **lar-como-fortaleza** (cit,tag; 2) — aspa ESE cap. XXVII item 9 (vs cap. XXVIII item 5).
- [ ] **possessos-de-morzine** (cit; 1) — três graus "estabelecidos com clareza programática" pelo artigo dez/1862.
- [x] **colecao-fonte-viva-emmanuel** (tag; 2) — "reencarnação" como eixo sem wikilink. · ✓ resolvido 2026-06-17 (wikilink [[reencarnacao]] na l.75)
- [ ] **psicopatologias-na-doutrina-espirita** (edit; 1) — "kardequiano/a" 8× (cruza §13).
- [ ] **serie-psicologica-joanna-de-angelis** (cit; 1) — "(LE q. 540)" como locus do "princípio inteligente".
- [ ] **sermao-do-monte-em-emmanuel** (edit; 1) — "Quatro capítulos a articular" mas lista sete.
- [ ] **oracoes-do-canal-espiritualidade-e-vida** (edit; 1) — "Catálogo (18 peças)" mas 1ª entrada é palestra, não oração.
- [ ] **sermao-do-monte** (cit; 2) — ESE cap. XVII item 3 vs cap. XV item 3.

---
- [x] **wiki/conceitos/espirito** (eixo 2, 2026-06-09) — transcrição literal de (LE, q. 76) entre aspas diverge do corpus em 2 palavras ('Universo'→'universo', 'fora do mundo'→'fora o mundo') · evidência: cite.py LE q. 76 (livro-dos-espiritos.md:422-424) · relatório: reports/critica/2026-06-09-2013 · ✓ resolvido 2026-06-10 (/autocritica → revisão humana; correções híbridas eixo 2/3, decisão eixo 4)
- [x] **wiki/conceitos/pluralidade-das-existencias** (eixo 2, 2026-06-09) — frase 'antes dele os druidas' atribuída a (LE, q. 222), mas q. 222 traça Pitágoras a filósofos indianos/egípcios; druidas são tese de Léon Denis (nível 3) · evidência: cite.py LE q. 222 (livro-dos-espiritos.md:909-960) · relatório: reports/critica/2026-06-09-2013 · ✓ resolvido 2026-06-10 (/autocritica → revisão humana; correções híbridas eixo 2/3, decisão eixo 4)
- [x] **wiki/conceitos/pluralidade-das-existencias** (eixo 3, 2026-06-09) — cabeçalhos fora do template canônico de conceito (faltam 'Ensino de Kardec', 'Desdobramentos', 'Aplicação prática', 'Divergências') · evidência: convencoes-frontmatter.md, Estrutura por tipo · relatório: reports/critica/2026-06-09-2013 · ✓ resolvido 2026-06-10 (/autocritica → revisão humana; correções híbridas eixo 2/3, decisão eixo 4)
- [x] **wiki/conceitos/avareza** (eixo 2, 2026-06-09) — frase entre aspas 'A riqueza é um depósito cujo emprego Deus pedirá conta' atribuída a (ESE, cap. XVI, item 7), que não a contém; texto literal é de Fénelon no item 13 · evidência: ESE cap. XVI item 7 vs item 13 (evangelho-segundo-o-espiritismo.md:2624-2647) · relatório: reports/critica/2026-06-09-2013 · ✓ resolvido 2026-06-10 (/autocritica → revisão humana; correções híbridas eixo 2/3, decisão eixo 4)
- [x] **wiki/conceitos/confianca-em-deus** (eixo 2, 2026-06-09) — citação 'Ter confiança na Providência é não se deixar abater...' atribuída a (ESE, cap. XXV, item 3) é inexistente na obra (item 3 trata da lei do trabalho); citação fabricada/deturpada · evidência: cite.py ESE cap. XXV item 3 (evangelho-segundo-o-espiritismo.md:4967-4972) + grep zero ocorrências · relatório: reports/critica/2026-06-09-2013 · ✓ resolvido 2026-06-10 (/autocritica → revisão humana; correções híbridas eixo 2/3, decisão eixo 4)
- [x] **wiki/conceitos/confianca-em-deus** (eixo 3, 2026-06-09) — faltam seções 'Desdobramentos' e 'Divergências' do template canônico de conceito · evidência: convencoes-frontmatter.md, Estrutura por tipo · relatório: reports/critica/2026-06-09-2013 · ✓ resolvido 2026-06-10 (/autocritica → revisão humana; correções híbridas eixo 2/3, decisão eixo 4)
- [x] **wiki/conceitos/demonios** (eixo 3, 2026-06-09) — falta seção '## Divergências'; agente recomenda manter (a página JÁ É a divergência Igreja×Espiritismo) · evidência: convencoes-frontmatter.md · relatório: reports/critica/2026-06-09-2029 · ✓ resolvido 2026-06-10 (/autocritica → revisão humana; correções híbridas eixo 2/3, decisão eixo 4)
- [x] **wiki/conceitos/demonios** (eixo 4, 2026-06-09) — avaliar tema/vida-futura além de tema/espiritos (peso de céu/inferno/penas) · evidência: convencoes-tags.md · relatório: reports/critica/2026-06-09-2029 · ✓ resolvido 2026-06-10 (/autocritica → revisão humana; correções híbridas eixo 2/3, decisão eixo 4)
- [x] **wiki/conceitos/desapego-dos-bens-terrenos** (eixo 2, 2026-06-09) — 'Servir a Mamon é subordinar...' entre aspas atribuída a (ESE, cap. XVI, item 2), que é a transcrição de Mateus 19; frase inexistente no ESE · evidência: ESE cap. XVI item 2 (evangelho-segundo-o-espiritismo.md:2600-2664) · relatório: reports/critica/2026-06-09-2029 · ✓ resolvido 2026-06-10 (/autocritica → revisão humana; correções híbridas eixo 2/3, decisão eixo 4)
- [x] **wiki/conceitos/desapego-dos-bens-terrenos** (eixo 2, 2026-06-09) — 'Verdadeira propriedade...' atribuída a item 8 (Desigualdade das riquezas); conteúdo é do item 9 (Pascal) e a frase entre aspas é paráfrase · evidência: ESE cap. XVI itens 8-9 (l.2631-2638) · relatório: reports/critica/2026-06-09-2029 · ✓ resolvido 2026-06-10 (/autocritica → revisão humana; correções híbridas eixo 2/3, decisão eixo 4)
- [x] **wiki/conceitos/desapego-dos-bens-terrenos** (eixo 2, 2026-06-09) — parábola de Lázaro + frase entre aspas atribuída a item 7; parábola é item 5 e a frase é inexistente no ESE · evidência: ESE cap. XVI itens 5,7 (l.2615-2630) · relatório: reports/critica/2026-06-09-2029 · ✓ resolvido 2026-06-10 (/autocritica → revisão humana; correções híbridas eixo 2/3, decisão eixo 4)
- [x] **wiki/conceitos/desapego-dos-bens-terrenos** (eixo 2, 2026-06-09) — 'O homem não é mais que um depositário...' atribuída a item 9; ideia é do item 13 (Fénelon), parábola dos talentos é item 6 · evidência: ESE cap. XVI itens 9,13,6 (l.2636-2647) · relatório: reports/critica/2026-06-09-2029 · ✓ resolvido 2026-06-10 (/autocritica → revisão humana; correções híbridas eixo 2/3, decisão eixo 4)
- [x] **wiki/conceitos/desapego-dos-bens-terrenos** (eixo 2, 2026-06-09) — 'O emprego da fortuna é benefício ou malefício...' atribuída a item 10; frase inexistente no ESE (grep zero); tema está em itens 11/13 · evidência: ESE cap. XVI item 10 vs 11,13 · relatório: reports/critica/2026-06-09-2029 · ✓ resolvido 2026-06-10 (/autocritica → revisão humana; correções híbridas eixo 2/3, decisão eixo 4)
- [x] **wiki/conceitos/desapego-dos-bens-terrenos** (eixo 2, 2026-06-09) — 'A miséria e a riqueza são provas igualmente difíceis' entre aspas atribuída a (LE, q. 814); paráfrase, e contradiz ESE cap. XVI item 7 (riqueza mais perigosa) · evidência: cite.py LE q. 814 · relatório: reports/critica/2026-06-09-2029 · ✓ resolvido 2026-06-10 (/autocritica → revisão humana; correções híbridas eixo 2/3, decisão eixo 4)
- [x] **wiki/conceitos/desapego-dos-bens-terrenos** (eixo 2, 2026-06-09) — desigualdade de riquezas por diversidade de inteligência atribuída a (LE, q. 806), que diz só que a desigualdade social é obra do homem; argumento é do ESE cap. XVI item 8 · evidência: cite.py LE q. 806 · relatório: reports/critica/2026-06-09-2029 · ✓ resolvido 2026-06-10 (/autocritica → revisão humana; correções híbridas eixo 2/3, decisão eixo 4)
- [x] **wiki/conceitos/desligamento-do-espirito** (eixo 2, 2026-06-09) — morte violenta atribuída também a (LM, 2ª parte, cap. I), que trata da ação dos Espíritos sobre a matéria; afirmação sustentada por LE q. 161-162 e C&I 2ª parte cap. I item 12 · evidência: LM 2ª parte cap. I (livro-dos-mediuns.md:1316-1507) · relatório: reports/critica/2026-06-09-2029 · ✓ resolvido 2026-06-10 (/autocritica → revisão humana; correções híbridas eixo 2/3, decisão eixo 4)
- [x] **wiki/conceitos/desligamento-do-espirito** (eixo 2, 2026-06-09) — frase entre aspas atribuída a (LE, q. 155) é paráfrase ('e as circunstâncias' acrescentado), não literal da tradução Guillon Ribeiro · evidência: cite.py LE q. 155 (livro-dos-espiritos.md:683-687) · relatório: reports/critica/2026-06-09-2029 · ✓ resolvido 2026-06-10 (/autocritica → revisão humana; correções híbridas eixo 2/3, decisão eixo 4)
- [x] **wiki/conceitos/desligamento-do-espirito** (eixo 3, 2026-06-09) — Fontes ainda lista C&I '1ª parte, cap. I' que deixou de ser usada após auto-fix do locus para 2ª parte · evidência: linha 46 das Fontes · relatório: reports/critica/2026-06-09-2029 · ✓ resolvido 2026-06-10 (/autocritica → revisão humana; correções híbridas eixo 2/3, decisão eixo 4)
- [x] **wiki/conceitos/desligamento-do-espirito** (eixo 4, 2026-06-09) — avaliar tema/encarnacao além de tema/vida-futura (trata perispírito/laço perispiritual) · evidência: convencoes-tags.md · relatório: reports/critica/2026-06-09-2029 · ✓ resolvido 2026-06-10 (/autocritica → revisão humana; correções híbridas eixo 2/3, decisão eixo 4)
- [x] **wiki/conceitos/emigracoes-e-imigracoes-dos-espiritos** (eixo 4, 2026-06-09) — avaliar tema/encarnacao e/ou tema/vida-futura além de tema/espiritos · evidência: convencoes-tags.md · relatório: reports/critica/2026-06-09-2029 · ✓ resolvido 2026-06-10 (/autocritica → revisão humana; correções híbridas eixo 2/3, decisão eixo 4)
- [x] **wiki/conceitos/encarnacao** (eixo 2, 2026-06-09) — necessidade/progresso/expiação atribuída a (ESE, cap. IV, itens 16-18), que tratam de ressurreição/laços de família; conteúdo está no item 25 ('Necessidade da encarnação') · evidência: cite.py ESE cap. IV itens 16-18,25 · relatório: reports/critica/2026-06-09-2029 · ✓ resolvido 2026-06-10 (/autocritica → revisão humana; correções híbridas eixo 2/3, decisão eixo 4)
- [x] **wiki/conceitos/encarnacao** (eixo 2, 2026-06-09) — 'não eterna nem ilimitada em número' ancorada genericamente em cap. IV contradiz itens 24-25 (sem limites precisos; reencarnação pode prolongar-se indefinidamente) · evidência: cite.py ESE cap. IV itens 24-25 · relatório: reports/critica/2026-06-09-2029 · ✓ resolvido 2026-06-10 (/autocritica → revisão humana; correções híbridas eixo 2/3, decisão eixo 4)
- [x] **wiki/conceitos/encarnacao** (eixo 3, 2026-06-09) — estrutura de seções fora do template canônico de conceito (faltam 'Ensino de Kardec', 'Aplicação prática', 'Divergências') · evidência: convencoes-frontmatter.md · relatório: reports/critica/2026-06-09-2029 · ✓ resolvido 2026-06-10 (/autocritica → revisão humana; correções híbridas eixo 2/3, decisão eixo 4)
- [ ] **wiki/conceitos/erraticidade** (eixo 2, 2026-06-10) — função 'auxiliar encarnados como protetor/guia' atribuída a (LE, q. 229), que trata da retenção das más paixões; locus real é q. 226 (missões) / q. 489 ss. (Espíritos protetores) · evidência: cite.py LE q. 229 (livro-dos-espiritos.md:984-985) · relatório: reports/critica/2026-06-10-0938
- [ ] **wiki/conceitos/erraticidade** (eixo 3, 2026-06-10) — faltam seções 'Desdobramentos' e 'Divergências' do template de conceito · evidência: convencoes-frontmatter.md · relatório: reports/critica/2026-06-10-0938
- [ ] **wiki/conceitos/evocacao** (eixo 2, 2026-06-10) — 'Qualquer Espírito acode' + frase entre aspas atribuída a (LM, item 272), que trata da dificuldade das evocações; item 282 (2ª-3ª) condiciona e lista Espíritos que NUNCA podem comunicar-se · evidência: cite.py LM item 272 vs 282 (livro-dos-mediuns.md:7868-8175) · relatório: reports/critica/2026-06-10-0938
- [ ] **wiki/conceitos/evocacao** (eixo 3, 2026-06-10) — faltam seções 'Desdobramentos' e 'Divergências' do template de conceito · evidência: convencoes-frontmatter.md · relatório: reports/critica/2026-06-10-0938
- [x] **wiki/conceitos/futuro-e-o-nada** (eixo 4, 2026-06-10) — cross-ref opcional a [[wiki/conceitos/materialismo]] na linha 47 (adversário central do argumento de C&I cap. I) · evidência: convencoes-frontmatter.md · relatório: reports/critica/2026-06-10-0938 · ✓ resolvido 2026-06-17 (wikilink inline em "materialismo contemporâneo")
- [ ] **wiki/conceitos/homem-de-bem** (eixo 2, 2026-06-10) — fórmula 'A perfeição moral consiste em praticar a lei de justiça, amor e caridade...' atribuída a (LE, q. 893), que trata da virtude mais meritória; a fórmula é da q. 918 · evidência: cite.py LE q. 893 vs q. 918 · relatório: reports/critica/2026-06-10-0938
- [ ] **wiki/conceitos/homem-de-bem** (eixo 3, 2026-06-10) — paráfrases de (ESE, cap. XVII, item 3) apresentadas entre aspas como literais (linhas 21,25,27,29); locus correto, mas converter para literal ou de-quote · evidência: cite.py ESE cap. XVII item 3 · relatório: reports/critica/2026-06-10-0938
- [ ] **wiki/conceitos/ligacao-espirito-corpo** (eixo 2, 2026-06-10) — afirma rompimento 'mais abrupto na morte violenta' (LE q. 155-162), INVERTENDO Kardec: na morte violenta o desligamento é mais LENTO e os laços mais tenazes (q. 162 nota, q. 165) · evidência: cite.py LE q. 162/165 · relatório: reports/critica/2026-06-10-0938
- [ ] **wiki/conceitos/ligacao-espirito-corpo** (eixo 2, 2026-06-10) — emancipação da alma em sono/êxtase citada com (LM, 2ª parte, cap. VI), que trata de manifestações visuais; locus real é LE q. 400-455 (Da emancipação da alma) · evidência: cite.py LM 2ª parte cap. VI vs LE q. 400-455 · relatório: reports/critica/2026-06-10-0938
- [ ] **wiki/conceitos/mundos-regeneradores** (eixo 2, 2026-06-10) — blockquote linha 19 atribuído a (ESE, cap. III, item 16) é paráfrase do item 17; locus errado + não-literal · evidência: cite.py ESE cap. III itens 16-17 · relatório: reports/critica/2026-06-10-0949
- [ ] **wiki/conceitos/mundos-regeneradores** (eixo 2, 2026-06-10) — blockquote linha 23 (item 17) 'doenças/sofrimentos já são passado' INVERTE Kardec ('ainda sujeito às vicissitudes... ainda tem de suportar provas') · evidência: cite.py ESE cap. III item 17 · relatório: reports/critica/2026-06-10-0949
- [ ] **wiki/conceitos/mundos-regeneradores** (eixo 2, 2026-06-10) — blockquote linha 27 (item 17) com frases inexistentes no ESE (grep zero): 'autoridade conquistada pela superioridade moral' etc. · evidência: cite.py ESE cap. III item 17 + grep · relatório: reports/critica/2026-06-10-0949
- [ ] **wiki/conceitos/mundos-regeneradores** (eixo 2, 2026-06-10) — blockquote linha 31 (item 17) paráfrase leve ('procuram'→'tentam'; 'seguindo as Suas leis'→'cumprindo-lhe as leis') como literal · evidência: cite.py ESE cap. III item 17 · relatório: reports/critica/2026-06-10-0949
- [ ] **wiki/conceitos/mundos-regeneradores** (eixo 2, 2026-06-10) — blockquote linha 35 atribuído a item 18 (que trata de falibilidade/recaída); conteúdo 'felicidade entrevista' é do item 17 · evidência: cite.py ESE cap. III itens 17-18 · relatório: reports/critica/2026-06-10-0949
- [ ] **wiki/conceitos/mundos-regeneradores** (eixo 3, 2026-06-10) — desdobramento 'transição da Terra a mundo regenerador' atribuído a 'muitos espíritas' sem âncora citável; opcional ancorar em Gênese cap. XVIII · evidência: Gênese cap. XVIII · relatório: reports/critica/2026-06-10-0949
- [ ] **wiki/conceitos/parabola-da-candeia-sob-o-alqueire** (eixo 2, 2026-06-10) — 'por que Jesus ensinava por parábolas' atribuído ao item 3 (versículo Mt 13:10-15); comentário de Kardec é o item 4 · evidência: cite.py ESE cap. XXIV itens 3-4 · relatório: reports/critica/2026-06-10-0949
- [ ] **wiki/conceitos/parabola-da-candeia-sob-o-alqueire** (eixo 2, 2026-06-10) — 'tudo o que está oculto será revelado' atribuído ao item 4; está no item 5 · evidência: cite.py ESE cap. XXIV itens 4-5 · relatório: reports/critica/2026-06-10-0949
- [ ] **wiki/conceitos/parabola-da-candeia-sob-o-alqueire** (eixo 2, 2026-06-10) — 'Espiritismo é candeia / responsabilidade dos espíritas' atribuído ao item 2 (versículo Lc 8:16-17); está nos itens 7 e 10 · evidência: cite.py ESE cap. XXIV itens 2,7,10 · relatório: reports/critica/2026-06-10-0949
- [ ] **wiki/conceitos/parabola-da-candeia-sob-o-alqueire** (eixo 3, 2026-06-10) — blockquote linha 17 (Mt 5:15) usa 'velador' vs. 'candeeiro' da tradução Guillon/FEB (fonte declarada) · evidência: ESE cap. XXIV item 1 · relatório: reports/critica/2026-06-10-0949
- [ ] **wiki/conceitos/parabola-da-candeia-sob-o-alqueire** (eixo 3, 2026-06-10) — blockquote linha 19 (Lc 8:16-17) com fraseado divergente da fonte ESE (Guillon/FEB) · evidência: ESE cap. XXIV item 2 · relatório: reports/critica/2026-06-10-0949
- [x] **wiki/conceitos/parabola-da-candeia-sob-o-alqueire** (eixo 4, 2026-06-10) — avaliar tema/historia-doutrina (eixo central é o dever de divulgação) além de tema/jesus · evidência: convencoes-tags.md · relatório: reports/critica/2026-06-10-0949 · ✓ resolvido 2026-06-17 (tema/historia-doutrina adicionada)
- [ ] **wiki/conceitos/parabola-da-casa-sobre-a-rocha** (eixo 3, 2026-06-10) — estrutura fora do template de conceito ('Texto da parábola' extra; faltam Desdobramentos/Divergências) · evidência: convencoes-frontmatter.md · relatório: reports/critica/2026-06-10-0949
- [ ] **wiki/conceitos/parabola-da-casa-sobre-a-rocha** (eixo 2, 2026-06-10) — inconsistência de range: corpo (l.23) diz 'itens 7-9', Fontes (l.45) diz 'itens 6-9'; correto é 6-9 (prosa ancora no item 6) · evidência: cite.py ESE cap. XVIII itens 6-9 · relatório: reports/critica/2026-06-10-0949
- [ ] **wiki/conceitos/parabola-da-figueira-seca** (eixo 2, 2026-06-10) — 'A fé é a mãe da esperança e da caridade' entre aspas atribuída ao item 10 (que trata de médiuns); ideia é do item 11 mas não literal · evidência: cite.py ESE cap. XIX itens 10-11 · relatório: reports/critica/2026-06-10-0949
- [ ] **wiki/conceitos/parabola-da-figueira-seca** (eixo 2, 2026-06-10) — 'montanhas = dificuldades/obstáculos' creditado aos itens 9-10; está no item 2, e 'fé como alavanca' no item 12 · evidência: cite.py ESE cap. XIX itens 2,9,10,12 · relatório: reports/critica/2026-06-10-0949
- [ ] **wiki/conceitos/parabola-da-figueira-seca** (eixo 3, 2026-06-10) — conexão com parábola do semeador/festim de bodas apresentada como sendo de Kardec (item 9), mas é leitura do redator · evidência: cite.py ESE cap. XIX item 9 · relatório: reports/critica/2026-06-10-0949
- [ ] **wiki/conceitos/parabola-da-figueira-seca** (eixo 3, 2026-06-10) — estrutura fora do template de conceito ('Texto da parábola' extra; falta Desdobramentos) · evidência: convencoes-frontmatter.md · relatório: reports/critica/2026-06-10-0949
- [ ] **wiki/conceitos/parabola-do-credor-incompassivo** (eixo 2, 2026-06-10) — Oração Dominical 'Perdoai as nossas ofensas...' atribuída ao item 3 (Mt 18:15,21,22); literal está no item 17, lógica da medida nos itens 11/13 · evidência: cite.py ESE cap. X itens 3,11,17 · relatório: reports/critica/2026-06-10-0949
- [x] **wiki/conceitos/parabola-do-credor-incompassivo** (eixo 4, 2026-06-10) — avaliar tema/prece-caridade ou tema/moral (eixo é perdão/caridade prática) além de tema/jesus · evidência: convencoes-tags.md · relatório: reports/critica/2026-06-10-0949 · ✓ resolvido 2026-06-17 (tema/prece-caridade adicionada)
- [x] **wiki/conceitos/parabola-do-credor-incompassivo** (eixo 4, 2026-06-10) — linkar [[wiki/conceitos/bem-aventuranca-dos-misericordiosos]] (cap. X) em Páginas relacionadas · evidência: página-conceito adjacente existe · relatório: reports/critica/2026-06-10-0949 · ✓ resolvido 2026-06-17 (entrada em Páginas relacionadas)
- [ ] **wiki/conceitos/parabola-do-festim-de-bodas** (eixo 2, 2026-06-10) — cabeçalho cita (ESE, cap. XVIII, itens 1-3); a análise está toda no item 2; item 3 é 'A porta estreita' (Mt 7:13-14), perícope distinta. Estreitar para itens 1-2 · evidência: cite.py ESE cap. XVIII · relatório: reports/critica/2026-06-10-1001
- [x] **wiki/conceitos/parabola-do-festim-de-bodas** (eixo 4, 2026-06-10) — avaliar tema/moral (túnica nupcial = pureza/caridade) além de tema/jesus · evidência: convencoes-tags.md · relatório: reports/critica/2026-06-10-1001 · ✓ resolvido 2026-06-17 (tema/moral adicionada)
- [ ] **wiki/conceitos/parabola-dos-trabalhadores-da-ultima-hora** (eixo 3, 2026-06-10) — enquadramento 'recompensa proporcional ao esforço individual' (l.29) tensiona ESE cap. XX item 3 (últimos podem receber recompensa MAIOR por herdarem o labor dos predecessores); refinar · evidência: cite.py ESE cap. XX item 3 · relatório: reports/critica/2026-06-10-1001
- [ ] **wiki/conceitos/parabola-dos-trabalhadores-da-ultima-hora** (eixo 3, 2026-06-10) — estrutura fora do template ('Texto da parábola' extra; faltam Desdobramentos/Divergências) · evidência: convencoes-frontmatter.md · relatório: reports/critica/2026-06-10-1001
- [x] **wiki/conceitos/penas-eternas** (eixo 4, 2026-06-10) — Páginas relacionadas linka anjos/demonios sem âncora na prosa; avaliar manter (relação via céu-e-inferno) ou remover · evidência: linhas 90-91 · relatório: reports/critica/2026-06-10-1001 · ✓ resolvido 2026-06-17 (mantido — relação temática legítima via céu/inferno; sem alteração)
- [ ] **wiki/conceitos/penas-eternas** (eixo 3, 2026-06-10) — faltam 'Desdobramentos' e 'Divergências' do template (Divergências legitimamente ausente — página é a posição de Kardec) · evidência: convencoes-frontmatter.md · relatório: reports/critica/2026-06-10-1001
- [ ] **wiki/conceitos/perfeicao-moral** (eixo 2, 2026-06-10) — blockquote de (LE, q. 893) l.17 não-literal ('Toda virtude tem seu mérito próprio' vs. 'Todas as virtudes têm seu mérito'); conformar à edição FEB/Guillon · evidência: cite.py LE q. 893 · relatório: reports/critica/2026-06-10-1001
- [ ] **wiki/conceitos/perfeicao-moral** (eixo 2, 2026-06-10) — blockquote de (LE, q. 909) l.33 não-literal ('frequentemente, fazendo esforços muito insignificantes' vs. 'por vezes fazendo esforços bem pequenos') · evidência: cite.py LE q. 909 · relatório: reports/critica/2026-06-10-1001
- [ ] **wiki/conceitos/perfeicao-moral** (eixo 2, 2026-06-10) — blockquote de (LE, q. 917) l.43 usa 'entretenimento' onde Guillon/FEB traz 'manutenção' · evidência: cite.py LE q. 917 · relatório: reports/critica/2026-06-10-1001
- [ ] **wiki/conceitos/perfeicao-moral** (eixo 3, 2026-06-10) — estrutura temática própria, sem 'Aplicação prática' nem 'Divergências' do template de conceito · evidência: convencoes-frontmatter.md · relatório: reports/critica/2026-06-10-1001
- [ ] **wiki/conceitos/perturbacao** (eixo 2 / TOOLING — página CORRETA, não alterar, 2026-06-10) — cite.py não desambígua os dois 'cap. I' de C&I (1ª parte 'O futuro e o nada' vs. 2ª parte 'A passagem') e resolve sempre p/ a 1ª; as citações da página (2ª parte cap. I itens 4-15) batem com ceu-e-inferno.md:2295-2318. Risco: futuras auditorias 'corrigirem' loci corretos. Fix no resolve_locus de cite.py · evidência: ceu-e-inferno.md:2295-2318 · relatório: reports/critica/2026-06-10-1001
- [x] **wiki/conceitos/perturbacao** (eixo 4, 2026-06-10) — avaliar wikilink [[wiki/conceitos/obsessao|desobsessão]] (display alternativo) na linha 60 · evidência: convencoes-mundos-habitados (display alt) · relatório: reports/critica/2026-06-10-1001 · ✓ resolvido 2026-06-17 (wikilink [[obsessao|desobsessão]] na l.60)
- [ ] **wiki/conceitos/principio-vital** (eixo 4, 2026-06-10) — prosa e tag pressupõem [[wiki/conceitos/fluido-vital]], que NÃO existe (data/terminologia.json registra o slug). Criar a página (distinção princípio vital vs. fluido vital — LE q. 70 comentário; Gênese cap. X item 19) ou remover o slug órfão · evidência: data/terminologia.json · relatório: reports/critica/2026-06-10-1017 · NOTA 2026-06-17: não há wikilink quebrado ("fluido vital" é prosa/tag livre, não [[link]]); requer decisão de criar página fluido-vital vs. manter tratado em principio-vital — diferido.
- [ ] **wiki/conceitos/proibicao-de-evocar-os-mortos** (eixo 2, 2026-06-10) — l.23 cita (C&I, 1ª parte, cap. XI, item 4) para dois exemplos; o boi do Êxodo está no item 5 (item 4 = só sacerdotes). Trocar para 'itens 4-5' · evidência: cite.py C&I cap. XI (ceu-e-inferno.md:2112-2194) · relatório: reports/critica/2026-06-10-1017
- [ ] **wiki/conceitos/proibicao-de-evocar-os-mortos** (eixo 3, 2026-06-10) — sem heading 'Definição'; seção 'Na Viagem Espírita em 1862' no lugar de Desdobramentos/Divergências · evidência: convencoes-frontmatter.md · relatório: reports/critica/2026-06-10-1017
- [x] **wiki/conceitos/psicografia** (eixo 4, 2026-06-10) — 'Casos notáveis' trata de psicografias via Divaldo/Chico; avaliar autor/divaldo-franco + autor/chico-xavier além de autor/kardec · evidência: convencoes-tags.md · relatório: reports/critica/2026-06-10-1017 · ✓ resolvido 2026-06-17 (autor/divaldo-franco + autor/chico-xavier adicionadas)
- [ ] **wiki/conceitos/psicografia** (eixo 3, 2026-06-10) — 'Casos notáveis' no lugar de 'Desdobramentos'; avaliar realocar · evidência: convencoes-frontmatter.md · relatório: reports/critica/2026-06-10-1017
- [x] **wiki/conceitos/purgatorio** (eixo 4, 2026-06-10) — adicionar [[wiki/conceitos/expiacao]] em Páginas relacionadas (conceito central na prosa e tag) · evidência: página-conceito existe · relatório: reports/critica/2026-06-10-1017 · ✓ resolvido 2026-06-17 (entrada em Páginas relacionadas)
- [ ] **wiki/conceitos/raca-adamica** (eixo 2, 2026-06-10) — blockquote l.23 (RE mar/1860) abre com frase 'Para nós é evidente que as raças primitivas...' inexistente no artigo (grep zero); só a 2ª metade ('Adão... há 6000 anos') é verbatim · evidência: revista-espirita/1860/03-marco.md:141-162 · relatório: reports/critica/2026-06-10-1017
- [ ] **wiki/conceitos/raca-adamica** (eixo 2, 2026-06-10) — blockquote l.70 (A Caminho da Luz cap. 3) troca 'desolados' por 'angustiados' dentro de aspas · evidência: a-caminho-da-luz.md:120 · relatório: reports/critica/2026-06-10-1017
- [ ] **wiki/conceitos/raca-adamica** (eixo 3 / possível DIVERGÊNCIA, 2026-06-10) — 'Desenvolvimento por Emmanuel' (origem em Capela, raça adâmica = raças brancas) vai além de Kardec, que NÃO racializa a raça adâmica (Gênese cap. XI item 39); avaliar seção Divergências/callout (nível 3 vs. Pentateuco) · slug sugerido: raca-adamica-identificacao-capela-emmanuel · evidência: Gênese cap. XI item 39 (genese.md:5460-5477) · relatório: reports/critica/2026-06-10-1017
- [x] **wiki/conceitos/raca-adamica** (eixo 4, 2026-06-10) — 'anjos decaídos' central sem wikilink a [[wiki/conceitos/anjos]] (termo só em títulos/quotes; exige tocar prosa) · evidência: wiki/conceitos/anjos.md existe · relatório: reports/critica/2026-06-10-1017 · ✓ resolvido 2026-06-17 (wikilink [[anjos]] inline na prosa l.31)
- [ ] **wiki/conceitos/resignacao** (eixo 2, 2026-06-10) — trecho 'Os Espíritos bons nos atraem para o bem...' (verbatim) citado como (LE, Parte 2, cap. I, Introdução); locus real é (LE, Introdução, item VI) · evidência: cite.py LE 'Introdução, item VI' (livro-dos-espiritos.md:84) · relatório: reports/critica/2026-06-10-1037
- [ ] **wiki/conceitos/resignacao** (eixo 2, 2026-06-10) — 'Bem-aventurados os aflitos, porque serão consolados' (Mt 5:4) mescla sujeito do ESE item 18 com predicado do item 1; fraseado composto inexistente · evidência: cite.py ESE cap. V itens 1,18 · relatório: reports/critica/2026-06-10-1037
- [ ] **wiki/conceitos/separacao-e-reencontro** (eixo 2, 2026-06-10) — blockquote 'Os que se amaram se reencontram após a morte e se reconhecem' atribuído a (LE, q. 274-276) (hierarquia); locus real é q. 285, e a frase não é literal nem lá · evidência: cite.py LE q. 274-276,285 · relatório: reports/critica/2026-06-10-1037
- [ ] **wiki/conceitos/separacao-e-reencontro** (eixo 2, 2026-06-10) — 'acompanhar/proteger como guia espiritual' ancorado em (LE, q. 284-285) (individualidade/reconhecimento); é doutrina dos Espíritos protetores (LE q. 489 ss.) · evidência: cite.py LE q. 284-285,489 · relatório: reports/critica/2026-06-10-1037
- [ ] **wiki/conceitos/separacao-e-reencontro** (eixo 2, 2026-06-10) — grupos por simpatia + inversão pai/filho citados como (LE, q. 274-278); grupos é q. 278 e a inversão de laços é q. 205; remover q.274-276 · evidência: cite.py LE q. 278,205 · relatório: reports/critica/2026-06-10-1037
- [ ] **wiki/conceitos/separacao-e-reencontro** (eixo 2, 2026-06-10) — 'reencarnar juntos para prosseguir relações anteriores' ancorado em (LE, q. 284-285); locus real é q. 205 · evidência: cite.py LE q. 284-285,205 · relatório: reports/critica/2026-06-10-1037
- [ ] **wiki/conceitos/separacao-e-reencontro** (eixo 3, 2026-06-10) — Fontes resume range como 'cap. VI, q. 274-285'; após corrigir loci, refletir cap. IV q. 205 + cap. VI q. 278,285 · evidência: cite.py · relatório: reports/critica/2026-06-10-1037
- [ ] **wiki/conceitos/vida-espirita** (eixo 2, 2026-06-10) — blockquote (LE, q. 224) não-literal ('que espera' vs. 'fica esperando'); locus correto · evidência: cite.py LE q. 224 (livro-dos-espiritos.md:968-973) · relatório: reports/critica/2026-06-10-1037
- [ ] **wiki/conceitos/vida-espirita** (eixo 3, 2026-06-10) — estrutura fora do template (headings próprios; faltam 'Ensino de Kardec', 'Desdobramentos', 'Aplicação prática', 'Divergências') · evidência: convencoes-frontmatter.md · relatório: reports/critica/2026-06-10-1037
- [ ] **wiki/conceitos/vida-futura** (eixo 2, 2026-06-10) — 'A vida futura é a vida normal do Espírito...' citado como literal de (ESE, cap. II, item 2); deriva alterado do cap. XXIII item 8 ('vida espiritual'/'existência terrestre', não 'vida futura'/'vida corpórea') · evidência: cite.py ESE cap. II item 2 vs cap. XXIII item 8 · relatório: reports/critica/2026-06-10-1037
- [ ] **wiki/conceitos/vida-futura** (eixo 2, 2026-06-10) — 'A vida corporal é necessária ao aperfeiçoamento... encarnação se reproduza' citado como literal de (ESE, cap. II, item 5); frase inexistente no ESE/LE (grep zero) · evidência: cite.py ESE cap. II item 5 + grep · relatório: reports/critica/2026-06-10-1037
- [ ] **wiki/conceitos/vida-futura** (eixo 2, 2026-06-10) — 'Aquele que se considera apenas viajante de passagem...' citado como literal de (ESE, cap. II, item 3); frase inexistente; tese está no item 5 com outra formulação · evidência: cite.py ESE cap. II itens 3,5 + grep · relatório: reports/critica/2026-06-10-1037
- [ ] **wiki/conceitos/evangelizacao-infantojuvenil** (eixo 2, 2026-06-10) — 'guiar os Espíritos que Deus lhes confiou para a vida terrestre' entre aspas como literal de (ESE, cap. XIV, item 9); ideia fiel mas frase não-literal (de-quote ou usar 'ponde todo o vosso amor em aproximar de Deus essa alma') · evidência: ESE cap. XIV item 9 (evangelho-segundo-o-espiritismo.md:2528-2567) · relatório: reports/critica/2026-06-10-1037
- [ ] **wiki/conceitos/harmonia-das-esferas** (eixo 3, 2026-06-10) — 'harpa cósmica' e 'degraus harmônicos' entre aspas são cunhagem da página, não literal de Léon Denis ('imensa harpa', '320 degraus ou ondas harmônicas'); de-quote ou citar literal · evidência: o-grande-enigma.md:587,651 · relatório: reports/critica/2026-06-10-1053
- [ ] **wiki/conceitos/morte** (eixo 2, 2026-06-10) — 'porta de entrada na vida, e não como a porta do nada' (C&I 1ª parte cap. II) — literal é 'a porta da vida' (sem 'de entrada'); 3 divergências da fonte · evidência: cite.py C&I cap. II item 7/10 · relatório: reports/critica/2026-06-10-1053
- [ ] **wiki/conceitos/morte** (eixo 3, 2026-06-10) — typo 'não se aprende diante da morte' → 'não se apreende' (cap. 'Da apreensão diante da morte'); inverte o sentido · evidência: C&I cap. II · relatório: reports/critica/2026-06-10-1053
- [ ] **wiki/conceitos/morte** (eixo 3 / TERMINOLOGIA, 2026-06-10) — 'reafirma o ancoramento kardequista' (l.66) usa forma proibida; trocar por 'de Kardec'/'no Pentateuco de Kardec' (derivados-de-kardec, auto_fix=false, correção contextual) · evidência: data/terminologia.json · relatório: reports/critica/2026-06-10-1053
- [x] **wiki/conceitos/morte** (eixo 4, 2026-06-10) — avaliar tema/encarnacao (mecanismo perispiritual da separação) além de tema/vida-futura · evidência: convencoes-tags.md · relatório: reports/critica/2026-06-10-1053 · ✓ resolvido 2026-06-17 (tema/encarnacao adicionada)
- [ ] **wiki/conceitos/parabola-do-semeador** (eixo 2, 2026-06-10) — 'a condenação do egoísmo, da indiferença, do amor das riquezas e da vaidade' entre aspas atribuída a (ESE, cap. XVII, item 6); frase INEXISTENTE no ESE (grep zero) — citação fabricada · evidência: cite.py ESE cap. XVII item 6 + grep · relatório: reports/critica/2026-06-10-1053
- [ ] **wiki/conceitos/parabola-do-semeador** (eixo 3, 2026-06-10) — estrutura com seções extras ('Texto da parábola', 'Na palestra de Carlos Mendonça'); sem 'Desdobramentos' · evidência: convencoes-frontmatter.md · relatório: reports/critica/2026-06-10-1053
- [ ] **wiki/conceitos/potencias-da-alma** (eixo 2, 2026-06-10) — 'Querendo, o Espírito atua sobre a matéria...' entre aspas atribuída a (LE, q. 459), que trata da influência dos Espíritos nos pensamentos; tema é Gênese cap. XIV/RE jun/1868 · evidência: cite.py LE q. 459 · relatório: reports/critica/2026-06-10-1053
- [ ] **wiki/conceitos/potencias-da-alma** (eixo 2, 2026-06-10) — 'a vontade cresce com o adiantamento moral' atribuída a (LE, q. 635), que trata de posições sociais; candidato é q. 872 ('força moral') · evidência: cite.py LE q. 635,872 · relatório: reports/critica/2026-06-10-1053
- [ ] **wiki/conceitos/potencias-da-alma** (eixo 2, 2026-06-10) — 'a lei que Deus gravou no coração do homem' entre aspas como (LE, q. 621); q.621 diz só 'Na consciência'; a formulação é de Romanos 2:15/ESE · evidência: cite.py LE q. 621 · relatório: reports/critica/2026-06-10-1053
- [ ] **wiki/conceitos/progresso-espiritual** (eixo 2, 2026-06-10) — 'uns avançaram mais depressa no livre exercício da vontade' (LE, q. 115); q.115 atribui o avanço à aceitação submissa das provas; complementar com q. 119 · evidência: cite.py LE q. 115,119 · relatório: reports/critica/2026-06-10-1053
- [ ] **wiki/conceitos/progresso-espiritual** (eixo 3, 2026-06-10) — estrutura com cabeçalhos próprios; sem 'Ensino de Kardec'/'Aplicação prática'/'Divergências' · evidência: convencoes-frontmatter.md · relatório: reports/critica/2026-06-10-1053
- [ ] **wiki/conceitos/verdadeiro-espirita** (eixo 2, 2026-06-10) — 'dá de si mesmo o mais formal desmentido' atribuída a (ESE, cap. XV, item 10); a frase é do cap. XXI item 10 (falsos profetas da erraticidade), contexto diverso; reancorar em cap. XV item 10 ('verdadeiro espírita = verdadeiro cristão') · evidência: cite.py ESE cap. XV vs XXI item 10 · relatório: reports/critica/2026-06-10-1114
- [ ] **wiki/conceitos/verdadeiro-espirita** (eixo 2, 2026-06-10) — 'Fiz o bem que podia? Sacrifiquei algum interesse...' entre aspas como (LE, Conclusão, item III), que é polêmica contra materialismo; autoexame é q. 919, mas a frase não é literal nem lá · evidência: cite.py LE Conclusão item III, q. 919 · relatório: reports/critica/2026-06-10-1114
- [x] **wiki/conceitos/verdadeiro-espirita** (eixo 4, 2026-06-10) — avaliar tema/prece-caridade (caridade prática é o núcleo) além de tema/moral · evidência: convencoes-tags.md · relatório: reports/critica/2026-06-10-1114 · ✓ resolvido 2026-06-17 (tema/prece-caridade adicionada)
- [ ] **wiki/conceitos/parabola-da-dracma-perdida** (eixo 2 / CLUSTER Lucas 15, 2026-06-10) — afirma que Kardec trata as 3 parábolas de Lucas 15 no ESE cap. XI; Kardec NÃO comenta dracma/ovelha/pródigo no ESE (grep 'dracma' = 0); cap. XI é a lei de amor. Misattribuição replicada em parabola-da-ovelha-perdida e parabola-do-filho-prodigo (fora deste lote) — corrigir o cluster · evidência: cite.py ESE cap. XI + grep · relatório: reports/critica/2026-06-10-1114
- [x] **wiki/conceitos/parabola-da-dracma-perdida** (eixo 4, 2026-06-10) — avaliar tema/vida-futura (reencarnações sucessivas/misericórdia eterna) além de tema/jesus · evidência: convencoes-tags.md · relatório: reports/critica/2026-06-10-1114 · ✓ resolvido 2026-06-17 (tema/vida-futura adicionada)
- [ ] **wiki/conceitos/parabola-da-ovelha-perdida** (eixo 2 / CLUSTER Lucas 15, 2026-06-10) — festejo pelo arrependido atribuído a (ESE, cap. XI, item 10), que é o ditado de Sanson ('Amai bastante para serdes amados'); locus real do bom Pastor/festejo é (LE, q. 1009) · evidência: cite.py ESE cap. XI item 10, LE q. 1009 · relatório: reports/critica/2026-06-10-1114
- [ ] **wiki/conceitos/parabola-da-ovelha-perdida** (eixo 2, 2026-06-10) — afirma que Kardec discute a parábola no cap. XVIII (cuidado com os 'pequeninos'); cap. XVIII é o festim de bodas; tema dos pequeninos (Mt 18) está no cap. VIII · evidência: cite.py ESE cap. XVIII · relatório: reports/critica/2026-06-10-1114
- [ ] **wiki/conceitos/parabola-da-ovelha-perdida** (eixo 3, 2026-06-10) — Fontes lista 'caps. XI, XVIII'; ajustar após corrigir os loci (remover cap. XVIII) · evidência: cite.py · relatório: reports/critica/2026-06-10-1114
- [ ] **wiki/conceitos/parabola-da-rede** (eixo 2 / CLUSTER joio-trigo, 2026-06-10) — 'Kardec a trata em paralelo à parábola do joio e do trigo (ESE, cap. XVIII)'; cap. XVIII é festim de bodas + casa sobre a rocha, NÃO o joio; triagem está em ESE cap. III item 13 + Gênese cap. XVIII (já citados). Mesmo erro em parabola-do-joio-e-do-trigo (cap. XVIII item 7, que é a casa sobre a rocha) — corrigir o par · evidência: cite.py ESE cap. XVIII · relatório: reports/critica/2026-06-10-1114
- [ ] **wiki/conceitos/parabola-da-rede** (eixo 2, 2026-06-10) — 'anjos ceifeiros' como organizadores da triagem com (C&I, 1ª parte) genérico; precisar o locus ou substituir (anjos = Espíritos adiantados é C&I 1ª parte cap. VIII item 13, mas não trata de 'ceifeiros') · evidência: cite.py C&I 1ª parte cap. VIII item 13 · relatório: reports/critica/2026-06-10-1114
- [ ] **wiki/conceitos/parabola-da-semente-que-cresce-por-si** (eixo 2 / CLUSTER mostarda, 2026-06-10) — autopropagação do Espiritismo atribuída a (ESE, cap. XVIII, item 2 — 'grão de mostarda e fermento'); cap. XVIII item 2 é o festim de bodas; ESE NÃO comenta mostarda/fermento; tese da autopropagação está na Introdução item VI. Mesmo erro em parabola-do-grao-de-mostarda (cap. XVIII item 5, que é a porta estreita) — corrigir o par · evidência: cite.py ESE cap. XVIII item 2 + grep + Introdução item VI · relatório: reports/critica/2026-06-10-1114
- [x] **wiki/conceitos/parabola-da-semente-que-cresce-por-si** (eixo 4, 2026-06-10) — adicionar [[wiki/conceitos/progresso-espiritual]] em Páginas relacionadas · evidência: página existe · relatório: reports/critica/2026-06-10-1114 · ✓ resolvido 2026-06-17 (entrada em Páginas relacionadas)
- [x] **wiki/conceitos/parabola-da-videira-verdadeira** (eixo 4, 2026-06-10) — polimento: wikilink inline a [[wiki/conceitos/fe-raciocinada]] (l.23) e [[wiki/conceitos/caridade]] (l.46); alvos já em Páginas relacionadas · evidência: páginas existem · relatório: reports/critica/2026-06-10-1129 · ✓ resolvido 2026-06-17 (2 wikilinks inline)
- [ ] **wiki/conceitos/parabola-das-dez-virgens** (eixo 2, 2026-06-10) — afirma que Kardec comenta a parábola no ESE cap. XVIII; esse cap. é o festim de bodas (Mt 22), NÃO as dez virgens — que só aparecem como alusão de passagem no cap. I item 10. Reenquadrar a leitura do azeite como síntese do estudante (LE q.132-134, ESE cap. III, Gênese cap. XVIII) · evidência: cite.py ESE cap. XVIII item 1 + grep · relatório: reports/critica/2026-06-10-1129
- [ ] **wiki/conceitos/parabola-do-bom-pastor** (eixo 2, 2026-06-10) — citação de OPE 'Estudo sobre a natureza do Cristo' aponta §VIII ('O Verbo se fez carne', Jo 1) para a glosa de Jo 10:30; locus real é §III; e a frase entre aspas ('fazia distinção... não disse: Eu sou o Pai') não é literal de Kardec (grep zero) · evidência: obras-postumas §III l.1515 · relatório: reports/critica/2026-06-10-1129
- [x] **wiki/conceitos/parabola-do-bom-pastor** (eixo 4, 2026-06-10) — avaliar tema/moral (liderança moral pastor vs. mercenário) além de tema/jesus · evidência: convencoes-tags.md · relatório: reports/critica/2026-06-10-1129 · ✓ resolvido 2026-06-17 (tema/moral adicionada)
- [ ] **wiki/conceitos/parabola-do-bom-samaritano** (eixo 2, 2026-06-10) — blockquote 'Texto da parábola' (l.17,19) em tradução não-declarada (nem Guillon/ESE nem Almeida/wiki-bíblia); ranges de versículo corretos. Alinhar à tradução da ESE (Guillon, cap. XV item 2) · evidência: cite.py ESE cap. XV item 2 vs wiki/biblia/lucas/10 · relatório: reports/critica/2026-06-10-1129
- [ ] **wiki/conceitos/parabola-do-fariseu-e-do-publicano** (eixo 2, 2026-06-10) — TODAS as citações ao ESE no locus errado: ancora em cap. VII item 9 (inexistente), cap. X itens 7-8, cap. XXVIII; Kardec comenta a parábola no cap. XXVII itens 3-4 ('orai com humildade como o publicano'). Reancorar a página inteira · evidência: cite.py ESE cap. VII vs XXVII · relatório: reports/critica/2026-06-10-1129
- [ ] **wiki/conceitos/parabola-do-fariseu-e-do-publicano** (eixo 2, 2026-06-10) — Definição (l.13) diz 'Kardec comenta extensamente no capítulo VII'; cap. VII comenta a parábola das bodas (Lc 14), não a do publicano. Corrigir para cap. XXVII itens 3-4 · evidência: cite.py ESE cap. VII item 5 · relatório: reports/critica/2026-06-10-1129
- [ ] **wiki/conceitos/parabola-do-fariseu-e-do-publicano** (eixo 3, 2026-06-10) — heading 'Definição' (a convenção pede 'Definição curta' como conteúdo, não título literal — cosmético) · evidência: convencoes-frontmatter.md · relatório: reports/critica/2026-06-10-1129

## 12. Verificação determinística de aspas do Pentateuco

> Motivação: a `/critica` de 2026-06-03 revelou um padrão sistêmico — **blockquotes apresentados como citação literal de Kardec que não existem na fonte** (ou apontam para o locus errado), maioria dos achados de severidade alta. Teste empírico: a wiki e o corpus `raw/kardec/pentateuco/` usam a mesma edição (Guillon Ribeiro/FEB), então aspa genuína bate **verbatim** com `cite.py` (~100%), enquanto aspa fabricada diverge muito (~40–55%). A separação de sinal sustenta um threshold de fuzzy match.

**3 sub-classes:** (1) **aspa fabricada** — texto "literal" inexistente → 100% determinístico; (2) **locus errado** — a aspa existe mas o `(SIGLA, ref)` aponta para outra questão → determinístico; (3) **range largo / paráfrase mal-ancorada** → irredutivelmente LLM. As classes 1 e 2 são as mais graves e automatizáveis; ficam fora da `/critica`, aliviando seu custo.

**Estado:** a **classe 2 (locus errado) virou determinística** — entregue o **índice reverso** (`scripts/reverse_locus.py`, 2026-06-15): dada a aspa, varre a obra e acha o locus de cobertura máxima por **cobertura contígua** (runs ≥3 palavras via `difflib`, robusta a acento/caixa/elisão e a frases quebradas entre linhas, onde `grep` falha; min-block mata o ruído de palavras funcionais que inflava o match contra questões longas). Reusa a segmentação do `cite.py` com **filtro monotônico** (descarta ordinais internos "1.º"/sub-perguntas que viravam itens espúrios — o item 223 do LM gerava 27 "item 2" falsos). `check_literal_quote_exists` agora **classifica** cada candidato (`reverse_locus.classify`) em: **misattributed** (sugere o `ref` certo, auto-corrigível), **fabricated**, **paraphrase** (locus certo, não-verbatim), **uncertain**, e **suprime supported** (a aspa está no locus citado — FP de extração em capítulo irregular). Citação em range (`q. 161–162`, `cap. X, itens 6-9`) tolerada via `cited_covers`. CLI para conferência humana: `uv run python scripts/reverse_locus.py <SIGLA> "<aspa>"`. Testes: `tests/test_reverse_locus.py` (15). `check_citation_resolves` (classe de locus inexistente) segue **`error`/CI gate** em 0 (ver [Concluído](#concluído)).

> **Calibração wiki-wide (2026-06-15)**: 153 candidatos → 25 misattributed · 97 fabricated · 8 paraphrase · 23 uncertain. **As 25 mal-atribuídas foram corrigidas no mesmo dia** (commit desta leva) — 22 trocas de locus + 2 de-quotes (paráfrase no locus certo, sugestão do índice descartada na verificação) + 1 falso-positivo mantido (`parabola-do-bom-samaritano`: a máxima "Fora da caridade não há salvação" está mesmo no ESE cap. XV item 10 citado; o índice preferiu o item 8 por ser wikilink). Várias batiam itens abertos do §11 (ex.: `bem-aventurancas` "Toda a moral de Jesus…" → ESE cap. XV item 3 e não XVII; `calunia` regra de ouro → LE q. 822). Pós-correção: **129 candidatos** (97 fabricated · 23 uncertain · 8 paraphrase · 1 FP). Lista acionável em `reports/citacao/triagem-aspas.md` (fora do build).

Abertos:

- [x] **Triagem das 128 aspas restantes CONCLUÍDA (2026-07-04).** Ciclo completo: dry-run (70 agentes) → validação adversarial (70 céticos) → aplicação. **64 auto-aplicados** (59 de-quote + 5 reanchor, gated pelo adversário) + **45 revisados à mão** (35 de-quote + reanchor a verbatim + 1 reescrita doutrinária: `cartas-vivas` afirmava o oposto de LM item 226) + **5 de-quotes que escaparam por colisão** + **2 blockquotes fabricados** (`escravidao` falsos q.825/q.829 → q.829/q.830). `literal_quote_exists` 128→21 (só keep verbatim que o `cite.py` não fragmenta + 1 FP allowlistado). Relatórios em `reports/citacao/triagem-{veredictos,final,digest-defer}-*.md`. **Descoberta:** blockquotes não são varridos (§12 Fase 3).
- [~] **Fase 1 — promover a check a gate.** **`misattributed` promovida a `warning` + hook (2026-06-17)**: virou check próprio `check_quote_misattributed` (separado do `check_literal_quote_exists`, que fica em `info` com fab/par/incerta), entrou no `CHECK_REGISTRY` e no `SINGLE_FILE_CHECKS` — toda mal-atribuição nova surge no PostToolUse na edição, com `detail` acionável (`locus citado → trocar por sugerido (cob. x→y)`). O scan do índice reverso é compartilhado pelos dois checks via memo (não dobra custo). FPs verificados à mão ficam na allowlist data-driven `data/citacao-aspas-aceitas.json` (hoje só `parabola-do-bom-samaritano`); wiki em 0 warnings. Testes: `tests/test_lint_literal_quote.py` (+5). **Falta:** promover `misattributed` a `error`/CI gate quando a confiança consolidar; **`fabricated`** depois (calibrar o threshold contra as 97). `supported` já é suprimido. Manter `uncertain`/`paraphrase` como `info`. Aspas inline só após blockquote estar sólido.
- [x] **Fase 2 — prevenção (fechar a torneira)** (2026-06-17) — `scripts/insert_quote.py`: dado o locus, puxa o texto verbatim da fonte via `cite.py` e emite o blockquote pronto (`> "..." (SIGLA, ref)`), **auto-verificado** contra a fonte (cobertura contígua ≥0.95 — se não bater, aborta; nunca emite aspa suspeita). `--sentence "<trecho>"` recorta só a(s) frase(s) da fonte que contêm o trecho (o recorte também vem da fonte; sem match, aborta — não fabrica); `--italic`; `--path P --after "<âncora>"` insere no arquivo. Testes: `tests/test_insert_quote.py` (8). Canonizado na regra `verificacao-citacao.md` (aspa do Pentateuco **só** via `cite.py`/`insert_quote.py`, nunca de memória). **É o conserto durável** — o índice reverso (Fase 1) drena o estoque e detecta; o `insert_quote` impede a reincidência na origem.
- [~] **Fase 3 — cobertura.**
  - **Detecção em blockquote — FEITO (2026-07-13).** Era o ponto cego: `_scan_literal_quotes` rodava `_strip_blockquotes` antes de casar, então **nenhuma** aspa de Kardec em blockquote (`> "..." (cite)`) jamais foi verificada — justamente a forma em que a transcrição literal mais aparece (~490 blockquotes com citação ao Pentateuco). As 128 triadas em 2026-07-04 eram só as inline. Conserto: `_logical_lines()` desembrulha o marcador `>` e junta parágrafos de blockquote numa unidade só (o regex proíbe `\n` dentro da aspa, e a transcrição pergunta/resposta do LE quebra entre duas linhas `>` — 34 casos), preservando o nº da linha de abertura; callouts entram no scan. O conector do `_QUOTE_BEFORE_CITE_RE` passou a aceitar ênfase (`*"…"* (LE, q. N)`), que também escapava inline. O teste `test_blockquote_ignored` **codificava o ponto cego como comportamento esperado** — invertido em 6 testes novos. Efeito: candidatos **21 → 105** (69 em blockquote, 35 inline). **Bônus:** `insert_quote.py` descascava mal as bordas e emitia aspa dupla (`"“Sim, porquanto…"`) — a fonte já traz `“…”` e o wrap somava a aspa reta; corrigido + teste.
  - **6 mal-atribuições novas corrigidas (2026-07-13)**, todas conferidas contra a fonte por `cite.py` antes do reanchor: `responsabilidade` q.640→**q.940** (erro de dígito; verbatim na q. 940*a*), `contentamento` q.662→**q.660** (+ aspa reescrita ao literal), `diabo-ontologico-em-apocalipse` C&I 1ª p. cap. IX item 19→**item 15**, `mudanca-de-sexo-reencarnacao` C&I 2ª p. cap. I "O Passamento"→**cap. II item 11** ("Espíritos felizes" — o diálogo com o Sr. Sanson; a própria página já citava certo no parágrafo seguinte), `as-casas-mal-assombradas` ESE "Introdução; cap. I"→**cap. VI item 4**, `o-problema-do-ser-e-do-destino` LE q.223→**q.224** (+ verbatim "alguns milhares"). Fontes das páginas atualizadas junto. Wiki de volta a **0 `warning`** em `check_quote_misattributed`.
  - [x] **Sombreamento de item no `cite.py` — RESOLVIDO (2026-07-13).** Os FPs de extração não eram "capítulo irregular": eram **marcadores falsos que sombreavam o item verdadeiro**. Um `N.` no início de linha que não é item faz o extractor ancorar nele *e* truncar o corpo do item anterior. Quatro classes achadas no corpus, todas consertadas — a aspa **genuína** dessas páginas era acusada de fabricada:
    1. **Número decimal de tabela** — o cap. X da Gênese traz a composição química (`Fibrina / 53.360 / 7.021 / 19.686`); `19.686` virava "item 19" e `literal_text` devolvia a string `"19.686"`.
    2. **Enumeração ordinal com parêntese** — `2.ª) Preces por aquele mesmo que ora;` (preâmbulo do ESE cap. XXVIII) sombreava o item 2 real.
    3. **Versículo bíblico transcrito** — no cap. XII da Gênese, Kardec transcreve o Gênesis encadeando versículos por ` — N. `; quando a quebra de linha cai após o travessão, o nº do versículo amanhece no início da linha. `item 2` resolvia para *"A Terra era uniforme…"* (versículo!) em vez do item 2 de Kardec. Resolvido por três filtros em `_chapter_items`: **continuação** (linha anterior termina em travessão), **política de ordinais** (ordinal só é item quando o capítulo não tem marcador simples — preserva os 33 itens ordinais de C&I 1ª parte cap. VII) e **sequencial** (item só é aceito se for o próximo esperado).
    4. **Ordinal interno no LE/LM** — `_ITEM_LEM_RE` rejeita ordinais nessas obras (onde nunca são item). **De quebra, isso fecha a "limitação residual deliberada"** registrada em jun/2026: o corpo do item não é mais truncado por enumeração interna (C&I 1ª p. cap. IX item 9 ia de 41 → 4828 chars).
    - **Fonte única de segmentação**: `cite.item_blocks(sigla, …)`, agora consumida pelo `publish_pentateuco` — que tinha **cópia própria** com `_ITEM_RE` cru e ancorava `## item 6` num versículo bíblico enquanto o `cite.py` já resolvia certo. O round-trip é fail-safe (descarta a âncora em silêncio), então a divergência não quebrava teste nenhum: novo teste de piso de cobertura por obra + teste de contrato `item_blocks`↔`literal_text` travam isso.
    - **Verificação:** das 2192 citações Kardec da wiki, **0 perdidas**, 39 corrigidas, 0 encolheram. Âncoras do Pentateuco **2524 → 2690** (as 10 removidas são itens-fantasma do cap. X da Gênese, que eram linhas de tabela). `raw/` intocado; publisher idempotente. Testes: 176 → 187 (invariante de monotonicidade varrendo LE/LM/ESE/C&I/Gênese, que foi quem **achou** as classes 3 e 4).
  - [ ] **Triagem dos 79 restantes** (56 fabricated · 13 paraphrase · 10 uncertain). Inventário acionável em `reports/citacao/triagem-blockquotes-2026-07-13.md` (fora do build). Rodar o mesmo ciclo que fechou as 128 inline: dry-run + adversário + aplicação. Os FPs de extração estão em **0** (eram 8) — o que sobra é candidato real, mas **verificar por item** mesmo assim (há true-positives claros, como `contentamento` atribuindo à q. 919 — que é o "Conhece-te a ti mesmo" — uma frase que não está lá).
  - [ ] Estender a aspas de loci que o `cite.py` não fragmenta (Introdução/Conclusão por item); onde não resolve, abster.

**Limites:** cobre só o **Pentateuco** (onde há `cite.py` + edição idêntica); aspas de autores complementares seguem dependentes da LLM (aceitável — as aspas mais sensíveis são as de Kardec). Aspa inline tem risco de falso-positivo — começar só por blockquote.

---

## 13. Varredura wiki-wide de "kardequiano/a" → "de Kardec" ✅ CONCLUÍDO (2026-06-07)

> Deriva terminológica sistêmica detectada por grep em 2026-06-03: **~654 ocorrências de "kardequiano/a" em ~238 páginas**. Violava a regra do usuário (memória `feedback-kardequiano-vs-de-kardec`): nunca "kardequiano/a"; "kardecista" só para o movimento, não para Kardec. **Eixo fechado**: detecção + correção wiki-wide + gate de regressão. Detalhe condensado em [Concluído](#concluído).

- [x] **Detecção (determinística)** (2026-06-07) — `check_kardequiano` no `lint_wiki.py`, **data-driven** (formas proibidas em `data/terminologia.json` → `derivados-de-kardec`). Promovido a **`error`/CI gate** após a contagem zerar. Testes: `tests/test_lint_kardequiano.py` (14).
- [x] **Correção (contextual, não cega)** (2026-06-07) — **688 → 0** em toda a wiki. Molde 1 (`<núcleo>` → `de Kardec`), Molde 2 (`em chave kardequiana` → **`à luz de Kardec`**, decisão do usuário), Molde 3 (resíduo manual: adjetivo após wikilink/negrito, predicativos, negação `não-kardequiana` → `alheia a Kardec`, casos de sentido como `Espírito kardequiano` → `Espírito na acepção de Kardec`). Callouts editoriais (`> [!note]`/`[!warning]`) incluídos; citações literais de fonte preservadas.
- [x] **Fonte do template Bíblia** (2026-06-07) — `scripts/publish_biblia_nt.py` gerava "leitura kardequiana" nos 27 `wiki/biblia/<livro>/index.md`; corrigido no gerador + nos 27 arquivos (senão regenera).

---

## Priorização

### Aberto, impacto alto — fidelidade doutrinária (núcleo do projeto)

- **Triagem do §11** — 66 itens diferidos do `/critica` de 2026-06-03 (já descontados os falso-positivos q. 1009/1015–1019). Cruza com o débito de rascunhos rebaixados (§10.3).
- ~~**Triagem das 128 aspas restantes do §12**~~ — **CONCLUÍDA (2026-07-04)**: dry-run + adversário + aplicação (64 auto + 45 manuais + 5 escapes + 2 blockquotes). `literal_quote_exists` 128→21 (resíduo = keep verbatim). Ver [Concluído] e §12. **Mas cobria só as aspas inline** — ver o item seguinte.
- **Triagem das 79 aspas em blockquote (§12 Fase 3)** — o scan passou a varrer blockquotes em 2026-07-13 e o backlog reabriu (56 fabricated · 13 paraphrase · 10 uncertain). Inventário em `reports/citacao/triagem-blockquotes-2026-07-13.md`. O sombreamento de item no `cite.py` (que acusava aspa genuína de fabricada) já foi consertado — FPs de extração em 0.
- **Triagem do §11** — **133 itens `[ ]` abertos** (medido 2026-07-14; o número antigo, "66 de 2026-06-03", estava defasado). Composição: **55 eixo 2** (citação não sustenta a afirmação), 25 eixo 3, 41 sem eixo classificado, 12 eixo 4. **Esta fila é o gargalo do projeto inteiro** — nenhuma automação a fecha, e o `/dreno` só *colhe* o que já foi decidido aqui. Cruza com o item ★ (que existe para tornar cada decisão rápida) e com o débito de rascunhos rebaixados (§10.3).
- ~~**Triagem das 128 aspas restantes do §12**~~ — **CONCLUÍDA (2026-07-04)**: dry-run + adversário + aplicação (64 auto + 45 manuais + 5 escapes + 2 blockquotes). `literal_quote_exists` 128→21 (resíduo = keep verbatim). Ver [Concluído] e §12.
- ~~**§13 sweep "kardequiano/a" → "de Kardec"**~~ — **CONCLUÍDO (2026-06-07)**: 688 → 0 em toda a wiki + check promovido a CI gate. Ver [Concluído](#concluído).
- ~~**§12 Fase 1+2 — detecção e prevenção**~~ — **CONCLUÍDO (2026-06-17)**: `misattributed` → `warning`+hook (`check_quote_misattributed`); `insert_quote.py` fecha a torneira na origem (aspa verbatim da fonte, auto-verificada). **Conserto durável.** Resta promover o check a `error`/CI gate quando a confiança consolidar.

### Aberto, impacto alto — conteúdo / leitor

- **§10.1 questões-chave do LE** (blocos 301–400 e 501–600) — fecha o pior gap doutrinário, alimenta `/slides` e palestras.
- **§10.3 limpar rascunhos ≥ 28 dias** — débito visível no `/lint`.
- **§10.2 índices de Evangelhos** (4) — desbloqueia 4 evangelhos no grafo com custo baixo.

### Aberto, impacto alto — workflow

- **★ §5 Reapontar o loop: entregar decisão pronta, não pedido de revisão** — **o item de maior alavanca do projeto hoje.** O loop diário não remove o gargalo humano; ele o reposiciona (de "rodar a skill" para "revisar um PR"). Enquanto a fila do §11 só for fechada à mão, a wiki avança na velocidade do Gabriel — e nenhuma automação do lado da *colheita* muda isso. O que muda: o loop preparar a decisão (cite.py rodado, texto literal ao lado, conserto redigido) para que o ato humano seja aprovar/rejeitar.
- **§1.3 Pipeline de palestras** — reduz fricção significativa.
- **§1.3 Manifest de progresso em lotes longos** — pré-requisito de segurança do loop autônomo roadmap-driven.
- **§5 `/autolint`** — complementa o hook PostToolUse; versão atenuada do self-healing loop.

### Médio prazo

§5 validação de deploy e baseline de build; §8 auditoria de LLM (cresce com o tempo); §2 trilhas e glossário; §6 Pagefind; §10.4/§10.5 aprofundamentos e sínteses por massa de vocabulário; §4 cobrir Kardec complementar no auto-link.

### Dependências

- §5 "versão estrita do check" — a parte **"a aspa existe"** já foi destravada e construída; só a parte **"o trecho sustenta a afirmação"** segue bloqueada por §4 Fase 2 (headings granulares no `raw/`).
- §4 "link interno preferencial" — depende dos mesmos headings granulares (§4 Fase 2).
- §1.3 Manifest de progresso → pré-requisito do loop autônomo.
- §13 correção em lote → depende da detecção (grep/check) primeiro.

---

## Princípios

- **Kardec prevalece** — toda melhoria respeita a hierarquia de autoridade (CLAUDE.md §2).
- **Citação obrigatória** — nenhum conteúdo novo sem fundamentação (§3).
- **Humano no circuito** — ingest e sínteses passam pelo usuário antes de publicar.
- **Incremental** — cada melhoria entrega valor isoladamente; sem dependência rígida entre eixos.

---

## Estado-alvo (definition of done por eixo)

- **§1 Cobertura** — Pentateuco com cobertura conceitual ≥80% no `/stats`; cada autor de nível 3 com ≥1 obra-âncora; nenhuma personalidade-âncora citada em 5+ páginas como stub.
- **§2 Leitor público** — 5 affordances da home com trilha completa (não stub); glossário ≥100 termos; canal de feedback ✓.
- **§3 Síntese** — 10 leis morais ✓; ≥30 questões-chave do Pentateuco extraídas; ≥5 sínteses temáticas comparativas.
- **§4 Cross-references** — todas as parábolas linkam conceitos morais (e vice-versa); nenhuma página em `wiki/divergencias/` órfã do conceito que diverge.
- **§5 Automação** — lint em CI verde por 30 dias; baseline de build com alerta; testes do `link_citations.py` ✓.
- **§8 Governança** — política de fair-use ✓; nenhuma obra protegida sem `direitos:` ✓; aviso ao leitor em todas as obras nível 3 ✓. Resta `revisao_humana:` (§8).
- **§11/§12/§13 Fidelidade** — 0 aspas literais fabricadas de Kardec; 0 loci inexistentes (já é CI gate); 0 ocorrências de "kardequiano/a".

Revisar a cada trimestre — alvo móvel é melhor que alvo nenhum.

---

## Concluído

> Registro condensado (um item por linha). O detalhe vive no histórico do git.

**§0 — Higiene de skills e documentação**
- Auditoria CLAUDE.md + 4 skills + rules + hook (2026-04-26).

**§1 — Cobertura de fontes**
- Pentateuco 5/5 (fechado com *O Livro dos Médiuns*).
- Nível 2 Kardec complementar 6/6 (2026-06-02).
- Novo Testamento canônico 27/27 (2026-05-18).
- Léon Denis 4/4 do raw atual.
- Chico Xavier / série André Luiz 13/19 ingeridos; auditoria 2026-05-26 promoveu conceitos e personalidades-âncora da série.
- Ingest *Memórias de um Suicida* (Camilo Castelo Branco / Yvonne) (2026-06-05).
- Coautoria mediúnica em `evolucao-em-dois-mundos.md` (André Luiz/Chico+Waldo Vieira).
- Personalidades-âncora expandidas (>700 palavras): Chico Xavier, Espíritos Reveladores, Carlos Mendonça, Joseph Bré, Eric Stanislas.
- Pre-flight check no `/ingest` Passo 0 (2026-05-04).
- Endurecimento do pipeline pós-report (2026-05-18→20): hook PreToolUse de pre-flight de branch; `qmd get` com offset; rule `convencoes-shell.md` + `SHELL_HAZARD_RE`.
- Ergonomia da revisão humana no `/ingest` (2026-05-19) — plano em 3 blocos; check de lar canônico; relatório por exceção.

**§2 — Leitor público**
- Home orientada por affordances (`index.md` como grid de cartões).
- Breadcrumbs semânticos (2026-05-05) + 9 `index.md` em pastas-raiz; cluster Leis Morais movido para `wiki/conceitos/leis-morais/`.
- Canal de feedback do leitor (2026-05-06) — "Sugerir correção" no Footer + issue templates `errata.yml`/`duvida.yml`.

**§3 — Síntese e estudo**
- 10 Leis Morais como página completa (2026-04-30).
- `sexualidade-em-andre-luiz.md` com *Sexo e Destino* (2026-05-04).

**§4 — Cross-references**
- Granularidade por questão/item — deep-link externo (Kardecpedia) (2026-06-05): LE 996, LM 327, ESE 476, C&I 180, Gênese 391; `DeepLinkTests`.
- Linkar referências bíblicas (2026-05-22) — NT interno, AT externo.
- Decisão sobre `wiki/biblia/` (2026-05-22) — híbrido: NT publicado, AT externo.
- Publicar NT em `wiki/biblia/<livro>/<cap>.md` (commit `7c1141a`) — 287 capítulos + 27 `index.md`; `publish_biblia_nt.py`.
- Bible mapping em `link_citations.py` (2026-05-22) — `data/biblia-livros.json`; 14 testes.

**§5 — Qualidade e automação**
- Lint em CI (`lint_wiki.py` a cada push).
- Métricas de cobertura (`stats_wiki.py`).
- Lint evolutivo (`low_citations`, `frequent_missing_concepts`, `naming_consistency`).
- Higiene de `stats_wiki.py` (meta-páginas excluídas; seções-template removidas).
- Backup e portabilidade (2026-05-16) — `docs/migracao.md` + `.env.example` + scripts; bump Python 3.12→3.14.
- Testes de `link_citations.py` (2026-05-01).
- `check_citation_resolves` — versão leve (2026-05-21) + **promovido a `error`/CI gate** (2026-06-05, commit `39e2a33`): locus do Pentateuco que não resolve reprova o PR e bloqueia o deploy.
- `check_literal_quote_exists` construído (2026-06-05) — info, fora do CI/hook (triagem dos 128 segue aberta, §12).
- §13 varredura "kardequiano/a" → "de Kardec" (2026-06-07) — `check_kardequiano` data-driven (`data/terminologia.json`/`derivados-de-kardec`) promovido a `error`/CI gate; correção contextual wiki-wide 688→0 ("em chave" → "à luz de Kardec"); gerador `publish_biblia_nt.py` corrigido na fonte; `tests/test_lint_kardequiano.py` (14).
- Workflow `/critica` — crítica doutrinária profunda (2026-05-31); vocabulários canônicos em `data/terminologia.json`.
- Aliases canônicos para personalidades e obras (2026-05-04) — `convencoes-aliases.md` + `check_canonical_names`.
- Uniformizar tipos de mundos habitados (2026-05-05) — `convencoes-mundos-habitados.md` + `check_mundos_habitados_naming`.
- `link_citations.py` não injeta wikilink em heading (2026-05-22).
- Skill `/ship` (2026-05-04).
- Hook PostToolUse de lint leve por arquivo (2026-05-04).
- Hook PostToolUse de mirror `wiki/**` → `/tmp/quartz/content` (2026-05-26).
- Rule `convencoes-merge.md` (2026-05-04).

**§6 — Busca**
- qmd como MCP server local (BM25 + vetorial + re-ranking, on-device).

**§7 — Ferramentas**
- Apresentações Marp — skill `/slides` (padrão socrático Q&A; PPTX+PDF).
- Preparação de palestra — skill `/palestra` + workflow `palestra-dossie` (2026-06-15): varredura Pentateuco-primeiro do corpus, definição julgada de termos, caça a casos com crítico, verificação adversarial de citação (`cite.py`) e painel socrático; estágio **Iconografia** (arte em domínio público via busca web) + rule `convencoes-imagens.md`. Dossiê em `reports/palestra/`. 1º deck com imagens: `slides/indulgencia/`. Colocação automática segue aberta (§7).

**§8 — Governança**
- Política de citação para nível 3 protegido (2026-04-27) — limites + `check_quote_proportion`.
- Aviso ao leitor em obras protegidas (2026-04-27) — `inject_copyright.py`.
- Frontmatter `direitos:` em obras nível 3 (2026-04-27) — `check_direitos_obras`.
- Status de `raw/` no Quartz (2026-04-27) — excluído do build; `check_raw_excluded`.

**§9 — Eficiência de tokens** (auditoria 2026-05-02)
- Disciplina nas queries `qmd` (defaults `limit`/`minScore`/`collections`).
- Granularizar `convencoes-paginas.md` em rules condicionais.
- Fragmentar Revista Espírita em `raw/` (partição mensal).
- Haiku para triagem em `/lint` e `/glossario`.
- Pré-resumo de obras monolíticas (`.index.md` + `.resumo.md`).

**§11 — Crítica profunda**
- Lote 2026-05-31: 28/28 itens diferidos resolvidos (fechado 2026-06-02, commit `b18c351`) — inclui criação de `wiki/conceitos/principio-inteligente` e reclassificações.
