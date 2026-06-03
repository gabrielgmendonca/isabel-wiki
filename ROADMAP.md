# Roadmap — IsAbel Wiki Espírita

> Melhorias de maior complexidade planejadas para a wiki.
> Organizadas por eixo temático, não por ordem cronológica.

---

## 0. Higiene das skills e documentação

- [x] **Auditoria CLAUDE.md + 4 skills + rules + hook** (2026-04-26) — bugs factuais, lacunas de doc, DRY, UX e config resolvidos em bloco. Lint passa sem regressão.

---

## 1. Cobertura de fontes

Completar a base doutrinária. Três frentes: **obras a ingerir** (gargalo principal), **curadoria de páginas existentes** e **pipeline/processos**.

### 1.1 Obras a ingerir

> **Onde vive a lista (2026-06-03)**: esta seção é **estratégia** — qual autor priorizar e por quê. O **estado factual** das duas filas do pipeline (`aquisição → raw/ → /ingest → wiki/`) vive fora daqui, para não envelhecer:
> - **Fila de ingestão** (obra em `raw/` sem página em `wiki/obras/`) → `uv run python scripts/list_pending_ingest.py` (derivada, nunca mantida à mão; 564 pendentes na última medição, pós-CEAK).
> - **Fila de aquisição** (obra ainda não em `raw/`) → `tracking/` (FEB, CEAK, triagem de direitos).
>
> As contagens por-autor abaixo podem estar defasadas em relação ao script — após a ingestão do catálogo CEAK (commit `c3c0d87`), vários "gargalos" mudaram (ex.: Cairbar/Peralva deixaram de ter pastas vazias). **Checar o script antes de assumir que um autor está descoberto.** Não é exaustiva quanto a `raw/mediuns/chico-xavier/**` nem `raw/mediuns/divaldo-franco/**`.

**Nível 1 — Pentateuco**
- [x] Pentateuco 5/5 (fechado com *O Livro dos Médiuns*).

**Nível 2 — Kardec complementar**
- [x] 6/6 completo (verificado 2026-06-02). Ingeridas: O Que é o Espiritismo, Obras Póstumas, Viagem Espírita em 1862, Instruções Práticas, Resumo da Lei dos Fenômenos Espíritas, Espiritismo em Sua Mais Simples Expressão.

**Novo Testamento canônico**
- [x] 27/27 completo (fechado 2026-05-18 com 2-João, 3-João, Judas). Tratamento inline de divergências culturais; cross-link a páginas estruturais já existentes.

**Nível 3 — Consagrados** (cobertura parcial)
- [x] **Léon Denis** — raw atual 4/4 ingerido (Depois da Morte, O Problema do Ser/Destino/Dor, Cristianismo e Espiritismo, O Grande Enigma). Ampliar exige adquirir fonte nova (ex.: *Joana d'Arc Médium*, *No Invisível*) — sem raw pendente.
- [x] **Chico Xavier / série André Luiz** — *A Caminho da Luz*, *O Consolador* e a série André Luiz parcialmente ingeridas (**13/19** títulos de `raw/mediuns/chico-xavier/andre-luiz/`). Auditoria 2026-05-26 promoveu 3 conceitos (`ministerios-de-nosso-lar`, `camaras-de-retificacao`, `volitacao`) + 3 personalidades-âncora (Henrique de Luna, Tobias, Veneranda) que atravessam a série inteira.
- [ ] **6 títulos André Luiz pendentes**: `agenda-crista`, `apostilas-da-vida`, `desobsessao`, `enderecos-da-paz`, `respostas-da-vida`, `sinal-verde`.
- [ ] **Yvonne Pereira** (classificada nível 3 em 2026-06-02) — 2/14 ingeridas (*A Luz do Consolador*, *Recordações da Mediunidade*). **12 pendentes** em `raw/autores/yvonne-pereira/`: `a-familia-espirita`, `a-tragedia-de-santa-maria`, `amor-e-odio`, `as-tres-revelacoes`, `devassando-o-invisivel`, `dramas-da-obsessao`, `memorias-de-um-suicida`, `nas-voragens-do-pecado`, `o-cavaleiro-de-numiers`, `o-drama-da-bretanha`, `ressurreicao-e-vida`, `sublimacao`.
- [ ] **Gabriel Delanne** (classificado nível 3 em 2026-06-02 — discípulo direto de Kardec) — 0 ingeridas; **7 títulos** em `raw/autores/gabriel-delanne/` (A Alma é Imortal, A Reencarnação, A Evolução Anímica, O Espiritismo perante a Ciência, O Fenômeno Espírita, A Mediunidade Mecânica, Automatismo da Escrita Psicográfica). Vários em `.doc` — converter antes do ingest.
- [ ] **Cairbar Schutel, Martins Peralva, Eurípedes Barsanulfo** — sem obra-âncora. Definition of done exige ≥1 por autor. **Gargalo persiste**: pastas `raw/autores/{cairbar-schutel,euripedes-barsanulfo,martins-peralva}/` existem mas **vazias** — ingest depende de aquisição da fonte primeiro.

**Pesquisa psíquica / espiritismo científico** (categoria criada no CLAUDE.md §2 em 2026-06-02 — corroboração experimental dos fatos, **sem** autoridade doutrinária sobre o Pentateuco; ingerir com a ressalva explícita)
- [~] **Camille Flammarion** — 8/9 já ingeridas (Urânia, Estela, A Morte e o Seu Mistério, O Fim do Mundo, Narrações do Infinito, Deus na Natureza, As Casas Mal-Assombradas, Como Acabará o Mundo); falta `o-desconhecido-e-os-problemas-psiquicos`. ⚠️ As 8 páginas **precedem** a classificação — revisar para inserir a ressalva de "pesquisa psíquica" (sem autoridade doutrinária) onde couber.
- [ ] **Ernesto Bozzano** — 0 ingeridas; ~22 títulos em `raw/autores/ernesto-bozzano/` (vários `.doc`/`.pdf`). Definir prioridade antes de qualquer ingest — fenomenologia metapsíquica, frequentemente neutra quanto à reencarnação.

### 1.2 Curadoria de páginas existentes

- [x] Coautoria mediúnica em `wiki/obras/evolucao-em-dois-mundos.md` (André Luiz/Chico Xavier+Waldo Vieira).
- [x] Personalidades-âncora expandidas: Chico Xavier, Espíritos Reveladores, Carlos Mendonça, Joseph Bré, Eric Stanislas (todas >700 palavras).

### 1.3 Pipeline e processos

- [x] **Pre-flight check no `/ingest` Passo 0** (2026-05-04) — checagem de `raw/<caminho>` + estado da branch (sem `fetch`).
- [x] **Endurecer pipeline pós-report de uso** (2026-05-18→05-20):
  - [x] Hook PreToolUse de pre-flight de branch (`.claude/hooks/preflight-ingest.py`) — gate determinístico que substitui as duas checagens de branch do Passo 0.
  - [x] `qmd get` com offset no Passo 1 do SKILL para fontes >1000 linhas.
  - [x] Rule `.claude/rules/convencoes-shell.md` (bash 3.2, BSD vs GNU sed, antipadrão `for`+`sed`) + `SHELL_HAZARD_RE` em `inject-rules.py` que injeta a rule também antes de Bash com `sed -i`/`mapfile`/`readarray`.
  - [ ] **Manifest de progresso em lotes longos** — JSON de itens concluídos, checado no início, para retomar conversão de catálogo / ingest multi-livro após limite de uso ou timeout.

  Os quatro são pré-requisito de segurança do loop autônomo roadmap-driven (versão atenuada com gate humano do "self-driving ingest loop", análoga ao `/autolint` em §5).
- [x] **Ergonomia da revisão humana no `/ingest`** (2026-05-19) — plano em 3 blocos (§0 ficha da fonte, §A decisões, §B execução); Passo 3 de checagem de lar canônico antes de cunhar slug de conceito; relatório de verificação por exceção. Ponto cego de fidelidade roteado para `check_citation_resolves` em §5 (solução determinística, não auto-auditoria LLM).
- [ ] **Pipeline de palestras** — consolidar workflow YouTube → transcrição → summary → ingest; hoje funciona mas é manual demais.

---

## 2. Experiência do leitor público

- [x] **Página de boas-vindas e home orientada por affordances** — `index.md` como grid de cartões (Chegando agora, ESDE, Palestras, Leitura livre, Consulta rápida).
- [~] **Trilhas de estudo guiadas** — stubs em `wiki/trilhas/` (primeiros-passos, esde, palestras, leitura-livre). Expandir cada com sequência comentada, leituras complementares e aferição de progresso ainda é TODO. Considerar também "As Leis Morais em ordem" e "Mediunidade: do básico ao avançado".
- [~] **Glossário navegável** — stub em `wiki/sinteses/glossario.md` com ~15 conceitos-raiz. Popular ~126 restantes, uma linha por termo, é TODO.
- [ ] **Expandir affordances da home** — considerar 6ª/7ª entrada (ex.: Divergências, Personalidades) conforme crescer. Manter 5 hoje para não sobrecarregar.
- [~] **Tags e filtragem** — 5 namespaces canônicos (`obra/*`, `lei/*`, `grau/*` 3 valores, `tema/*` 12 valores, `autor/*` 16 valores) documentados em `convencoes-tags.md`. Lint estendido (`check_tag_taxonomy`, `check_tag_coverage`). `enrich_tags_autor.py` e `enrich_tags_grau.py` idempotentes. **Faltando:** passada manual de `tema/*` nas 345 páginas listadas pelo `tag_coverage`.
- [ ] **Revisar tags `tema/`** — auditar conjunto canônico de 12 valores; identificar temas sub-representados, sobrepostos ou ausentes; reavaliar granularidade (ex.: separar `mediunidade` de `obsessao`). Revisar páginas tagueadas em massa (commit `5629049`) para corrigir falsos positivos.
- [x] **Breadcrumbs semânticos** (2026-05-05) — `Component.Breadcrumbs` com `rootName: "Início"`, `spacerSymbol: "›"`, `resolveFrontmatterTitle: true` + 9 `index.md` em pastas-raiz; cluster Leis Morais movido para `wiki/conceitos/leis-morais/`; ~481 wikilinks reescritos.
- [x] **Canal de feedback do leitor** (2026-05-06) — "Sugerir correção" no `Component.Footer` + issue templates `errata.yml` e `duvida.yml` em YAML forms.
- [ ] **Acessibilidade para leitores de tela** — VoiceOver/NVDA/JAWS leem linearmente na ordem do DOM. Quartz v4.4.0 emite `.left → .center → .right` como `<div>`s genéricas (sem `<nav>/<main>/<aside>`), então o leitor passa pelo Explorer inteiro antes do conteúdo. Sintoma reportado em 2026-05-22: leitura "presa no menu lateral".
  - **Tentativa descartada (2026-05-22):** componente `SkipLink` custom em `quartz-overrides/` injetando `<a class="skip-link">` no topo do `<body>` + `role="main"/navigation/complementary` em `.center/.left/.right` via JS `beforeDOMLoaded` (evento `nav`). CSS/HTML/build OK, mas VoiceOver ficou repetindo "Pular para o conteúdo principal" sem mover foco para o `<main>` mesmo com `tabindex="-1"` + `e.preventDefault()` + `.focus()` programático. Hipóteses: rotor do VO retém current item independente do `.focus()`; `enableSPA: true` do Quartz pode interceptar hash links; landmark via JS pós-hidratação chega tarde demais para o índice do leitor. Mudanças revertidas via `git restore`, sem commit.
  - **Caminho sugerido:** patch direto em `renderPage.tsx` do Quartz (copiado para `/tmp/quartz/` em build-time, mesmo padrão dos `quartz-overrides/components/`) trocando as 3 `<div class="left|center|right">` por `<nav>/<main>/<aside>` semânticos **no SSR**. Landmark real no HTML estático elimina toda a dança de JS+foco — leitor de tela passa a oferecer navegação por região nativamente, sem skip-link necessário. Custo: adicionar `renderPage.tsx` à lista de arquivos copiados em `.github/workflows/deploy-wiki.yml` e `scripts/serve-local.sh`, e manter o diff curto contra a versão upstream do Quartz. Validar com VoiceOver real antes de declarar fechado.
  - **Itens correlatos** (auditoria 2026-05-22, podem ser tratados independentes do landmark): (a) alt text em embeds YouTube `![](url)` em `wiki/.../palestras/` + `check_alt_text` no `lint_wiki.py`; (b) callouts `> [!warning]`/`> [!note]` viram `<blockquote>` comum, sem `role="note"`/`alert` — exigiria transformer custom; (c) botões `A+`/`A−` em `quartz-overrides/components/FontSize.tsx` mudam `data-fontScale` sem `aria-live`, mudança não é anunciada; (d) `lang="pt"` no `<html>` já vem do `locale: "pt-BR"` (verificado em `renderPage.tsx:217`), ARIA em Darkmode/Search/FontSize já presentes — base do Quartz é decente, problema concentra-se nos landmarks.

---

## 3. Conteúdo de síntese e estudo

As categorias `questoes/` e `sinteses/` estão sub-representadas. São as mais valiosas para o leitor.

- [ ] **Extrair questões-chave do Pentateuco** — selecionar as questões mais importantes de cada obra. **Priorizar blocos sub-cobertos do LE** (medição 2026-05-07 via `/stats`): q.201–300 (19%), q.301–400 (8%), q.401–500 (17%) — miolo metafísico (Deus, criação, princípio vital, alma, escolha das provas). Razão conceitos/questões em 17.2 (189:11); capitalizar Q&A ancorada em questão única antes de novas sínteses.
- [x] **10 Leis Morais como página completa** (2026-04-30) — todas >600 palavras; numeração corrigida (Conservação 4ª, Progresso 7ª, Igualdade 8ª, Liberdade 9ª — dentro da Parte 3 do LE).
- [ ] **Promover conceitos centrais a aprofundamentos sistemáticos** — `/stats` (2026-05-07): apenas 9 páginas em `wiki/aprofundamentos/` vs 189 conceitos; cadência ingest:aprofundamento 98:1. Top PageRank com massa crítica para estudo tipo palestra de 1h: `reencarnacao` (0.0247), `progresso-espiritual` (0.0227), `livre-arbitrio` (0.0165), `perispirito` (0.0147), `caridade` (0.0142).
- [ ] **Sínteses temáticas** — comparativos entre obras sobre o mesmo tema (ex: "O que cada obra diz sobre obsessão"; "Reencarnação: de Kardec a Léon Denis").
- [x] **`sexualidade-em-andre-luiz.md` com *Sexo e Destino*** (2026-05-04) — novo eixo 7 (1963): tese ativa, possessão partilhada, dignidade de homossexuais e intersexos.
- [ ] **Quadros comparativos** — tabelas que cruzam conceitos entre obras ou autores.
- [ ] **Perguntas frequentes** — FAQ baseada em dúvidas comuns de estudantes, com respostas fundamentadas e citadas.

---

## 4. Cross-references enriquecidas

A wiki tem links, mas pode ser mais densa em conexões.

- [ ] **Parábolas ↔ conceitos** — cada parábola do ESE linka explicitamente os conceitos morais que ilustra, e vice-versa.
- [ ] **Leis morais ↔ exemplos práticos** — conectar cada lei a parábolas, questões e casos concretos.
- [ ] **Personalidades ↔ conceitos** — Espíritos citados em C&I linkam conceitos que suas histórias ilustram.
- [ ] **Obras ↔ obras** — referências cruzadas quando uma obra cita ou complementa outra (ex: Gênese referencia LE em vários pontos).
- [ ] **Grafo temático** — "hub pages" por tema agregando conceitos, personalidades, obras, questões (ex: hub de "Mediunidade").
- [ ] **Tração inversa do cluster epistolar** — `/stats` (2026-05-07): epístolas dominam o top de grau de saída (1 Pedro 51, Tiago 50, Romanos 44, 2 Pedro 42, Gálatas 41, 2 Coríntios 40, Apocalipse 40) mas só Apocalipse aparece no top de tamanho e nenhuma figura no top de grau de entrada (PageRank dominado por reencarnação, ESE, progresso, livre-arbítrio). Auditar: para cada conceito tratado em uma epístola (caridade em 1 Cor 13, fé viva em Tiago 2), o conceito cita a obra epistolar?

### Citações inline como links

Após a fase 1 (auto-link Markdown→Kardecpedia em build time, capítulo — `scripts/link_citations.py`), aprofundar:

- [ ] **Fase 2 do híbrido — link interno preferencial** — normalizar `raw/kardec/pentateuco/*.md` com headings granulares (`## q. 990`, `## cap. VII, item 16`), remover `raw` do `ignorePatterns` do Quartz e preferir link interno sobre Kardecpedia quando disponível.
- [ ] **Cobrir Kardec complementar no auto-link** — estender mapping para RE, OPE, OQE, Viagem Espírita em 1862.
- [ ] **Granularidade por questão/item** — mapear itens individuais no Kardecpedia (o crawler já coleta os ids, falta usar).
- [x] **Linkar referências bíblicas** (2026-05-22) — NT linka interno (`[[wiki/biblia/<slug>/<cap>#<vers>|...]]`); AT linka externo (bibliaonline.com.br no nível do capítulo). Destravado pela publicação do NT (`fcfe9f9`) + mapping bíblico abaixo.
- [x] **Decisão sobre `wiki/biblia/`** (2026-05-22) — escolhido **(c) híbrido**: NT publicado em `wiki/biblia/<livro>/<capitulo>.md` (27 livros, ~260 arquivos); AT permanece em `raw/biblia-acf/` (39 livros) + link externo. Razão: NT é onde Jesus está (fonte primordial) e já é tratado obra-a-obra em `wiki/obras/`; AT é fonte ocasional. Achado durante o levantamento: `wiki/obras/biblia/` nunca existiu — os 27 livros NT vivem flat em `wiki/obras/<slug>.md`; e os wikilinks `[[raw/biblia-acf/<livro>/1]]` em `wiki/obras/evangelho-segundo-*.md` estão silenciosamente quebrados (Quartz ignora `raw/` no `ignorePatterns`).
- [ ] **Publicar NT em `wiki/biblia/`** — destravado pela decisão acima. Granularidade fixada (2026-05-22): **arquivo por capítulo** (~260 páginas, mesma cardinalidade do `raw/biblia-acf/<livro>/<cap>.md`). Razão: anchor de versículo estável, paridade 1:1 com a fonte ACF, leitor de capítulo isolado sem rolagem longa. Trade-off aceito: ~260 nós-folha no grafo do Quartz (mitigado por cross-link dos `wiki/obras/evangelho-segundo-*.md` e do auto-link de citações). Sub-tarefas:
  - Definir frontmatter padrão (tipo novo `capitulo-biblico`? `obra`? `raw-publicado`?) e schema mínimo (livro, capitulo, testamento, autor tradicional). Capítulo médio = ~110 linhas em ACF — preservar quebra de versículo.
  - Script `scripts/publish_biblia_nt.py` que copia 27 livros NT de `raw/biblia-acf/` para `wiki/biblia/<livro>/<cap>.md`, gera frontmatter, injeta heading por versículo (`## v.5`) para anchor estável.
  - Substituir `[[raw/biblia-acf/<livro>/1]]` por `[[wiki/biblia/<livro>/1]]` nos 27 `wiki/obras/evangelho-segundo-*.md` / epístolas / Atos / Apocalipse.
  - Decidir se cada livro recebe `wiki/biblia/<livro>/index.md` (página-âncora com lista de capítulos) — ajuda navegação por breadcrumb mas adiciona +27 páginas.
- [x] **Bible mapping em `link_citations.py`** (2026-05-22) — `data/biblia-livros.json` (66 livros + variantes Mt/Mateus, Gn/Gênesis, 1Co/1 Coríntios, S. Mateus); `build_biblia_mapping()`/`link_biblia()` no script, regex com alternação ordenada por tamanho desc para resolver longest-match (`1 Coríntios` antes de `1 Co`). NT → `[[wiki/biblia/<slug>/<cap>#<vers>|...]]` (anchor `#<N>` casa com heading `## <N>` do capítulo publicado — não `#v<N>` como esta linha grafava antes). AT → `bibliaonline.com.br/acf/<abbrev>/<cap>` no nível do capítulo (versículo via URL é instável). Range/lista de versos (`13:1-3`, `5:3,5,8`) linka primeiro verso e preserva label original; aceita en-dash além de ASCII hífen. Ambiguidade Jó/João resolvida exigindo diacrítico (`Jo` sem til não casa nem com um nem com outro). 14 testes em `tests/test_link_citations.py` (43 no total).

---

## 5. Qualidade e automação

- [x] **Lint em CI** — `lint_wiki.py` no GitHub Actions a cada push.
- [x] **Métricas de cobertura** — `stats_wiki.py` gera % do Pentateuco citado por obra (LE 21%, ESE 28/28, Gênese 10/18, LM 24/33, C&I 18/18), cobertura LE por bloco de 100 questões, wikilinks quebrados ≥ 5, razão conceitos/questões e sugestões priorizadas.
- [ ] **Validação de deploy** — checar se build do Quartz não quebrou links internos após deploy.
- [x] **Lint evolutivo** — `low_citations`, `frequent_missing_concepts`, `naming_consistency` (case/diacrítico, plural/singular).
- [x] **Higiene de `stats_wiki.py`** — meta-páginas excluídas; seções-template removidas antes de tokenizar (top bigramas agora refletem doutrina, não aparato bibliográfico).
- [x] **Backup e portabilidade** (2026-05-16) — `docs/migracao.md` (Setup/Migração) + `.env.example` + `scripts/{preflight,bootstrap}.sh`; bump Python 3.12→3.14 (lock relock, lint+testes verdes); 10 memórias locais consolidadas em docs rastreados.
- [x] **Testes de `link_citations.py`** (2026-05-01) — 25 casos em `tests/test_link_citations.py` (unittest puro), rodando em CI antes do build.
- [x] **Check determinístico de resolução de citação — versão leve** (`check_citation_resolves`, 2026-05-21) — `scripts/kardec_structure.py` carrega a estrutura do Pentateuco dos 4 `.index.md` (+ gerado para C&I) e do `kardec-mapping.json` (LE, sem partes detectáveis no markdown); novo check em `lint_wiki.py` bate cada `(sigla, ref)` contra parts/chapters/intro_items/range de questão. Pega typo de número, sigla com parte inexistente, cap. fora de range. Suite de 20 testes em `tests/test_kardec_structure.py` (truncagem de citação encadeada, ponte `cf.`, q. de Conclusão q. 1011-1019). Achados pós-rollout: 2 itens, ambos true positives (cap. VI da LM 1ª parte → na verdade 2ª; epístola perdeu sigla C&I no encadeamento). Passo 7 do `/ingest` ajustado: relatório lista citações **inválidas**, não todas — atenção humana focada no que falhou. Hook PostToolUse roda automático por arquivo.
- [ ] **Versão estrita do check** — verifica que o trecho citado **sustenta** a afirmação, não só que o locus existe. Bloqueado: depende da granularidade por questão/item em `raw/kardec/pentateuco/` (§4 "fase 2 do híbrido"). Sem isso, a checagem **determinística** da camada baixa cobre os erros de typo/sigla, mas alegação como "Kardec diz X em (LE, q. 460)" quando q. 460 trata de Y permanece editorial. **Atacado por via LLM** pelo `/critica` abaixo (eixo 2), que roda `cite.py` e compara o texto literal com a afirmação — caro, infrequente, com verificação adversarial; não substitui a versão estrita determinística (que continua o alvo quando houver granularidade).
- [x] **Workflow `/critica` — crítica doutrinária profunda** (2026-05-31) — camada semântica que o `/lint` (mecânico) não cobre. Multi-agente (`.claude/workflows/critica-profunda.js`): pipeline por página = crítica Opus (4 eixos: divergência não-registrada com Pentateuco, citação que não sustenta a afirmação, desvio editorial, tags/links) → verificação adversarial Sonnet dos achados high-stakes (mata falso-positivo). Reusa `cite.py` (verdade-fonte do Pentateuco), qmd `raw` (complementares), `lint_wiki.py --file`. **Caro → infrequente**: escopo só de páginas recém-editadas via `critica_scope.py` (estado de hash de corpo em `.claude/skills/critica/state/critica-state.json`, separado do `log.md`). Correções seguras auto-aplicadas (`critica_apply.py`: typo de locus confirmado por cite.py, terminologia canônica, tema/* faltando, wikilink a conceito existente); decisões doutrinárias → `status: rascunho` + stub `wiki/divergencias/` (`status: aberta`) + ROADMAP §11. Relatório HTML+MD em `reports/critica/<data>/` (`critica_report.py`, stdlib-only, fora do build). Vocabulários canônicos data-driven em `data/terminologia.json` (generaliza `check_mundos_habitados_naming` p/ escala espírita, fenômenos, fluidos, parábolas, bem-aventuranças).
- [ ] **Auditar aspas literais fabricadas em `wiki/**` (todos os tipos)** (anotado 2026-06-01, ampliado 2026-06-02) — o passe do §11 confirmou um padrão recorrente: **frase apresentada entre aspas como citação literal de Kardec, mas inexistente na obra** (paráfrase vestida de citação, às vezes com locus de capítulo errado). Apareceu em 4 das 5 páginas de divergência auditadas pelo `/critica`; e o caso de `sinais-de-marcos-16` L23 (aspa atribuída a Gênese cap. XIV item 1, `grep`=0) **não foi pego pelo `/critica`** — só foi achado por estar no mesmo bloco de um item do §11. **Confirmação 2026-06-02 fora de `divergencias/`**: a revisão de `wiki/aprofundamentos/por-que-mediuns-falham.md` (rascunho ≥28d, §10.3) achou **duas aspas literais fabricadas** atribuídas ao mesmo item (LM cap. XX, item 226; ambas `grep`=0), mais capítulo/título/range errados (cap. XXVIII rotulado "Médiuns imperfeitos"; ESE "pelos frutos" atribuído a cap. XXIV em vez de cap. XXI). O padrão **não é exclusivo de `divergencias/`** — qualquer página que confronte Pentateuco com nível 3 está exposta. **Ação**: estender o levantamento a **todo `wiki/**`** (não só `divergencias/`) fora do histórico do `/critica` (`critica-state.json`) e, para cada aspa literal de Pentateuco, validar com `grep` literal no `raw/` + `cite.py`; converter as fabricadas em paráfrase ou citação real ancorada no texto. Candidato a check determinístico futuro (`check_literal_quote_exists`: extrair spans entre aspas adjacentes a `(SIGLA, ...)` e checar substring no `raw/` correspondente) — bloqueado pela mesma granularidade da "Versão estrita do check" acima, mas a checagem de **existência literal** (mais fraca que "sustenta a afirmação") já seria viável e teria pego todos esses casos.
- [x] **Aliases canônicos para personalidades e obras** (2026-05-04) — `convencoes-aliases.md` (canônico = H1; aliases ≥ 4 caracteres em `aliases:`) + backfill em 9 páginas-âncora + lint `check_canonical_names` (info-level) surfando 32 candidatos.
- [x] **Uniformizar tipos de mundos habitados** (2026-05-05) — fonte canônica fixada em **ESE cap. III, item 4** (não Gênese cap. III como o ROADMAP grafava). Rule `convencoes-mundos-habitados.md` + 2 páginas-conceito novas (`mundos-primitivos`, `mundos-celestes-ou-divinos`) + lint `check_mundos_habitados_naming` + backfill em 10 arquivos.
- [ ] **Varredura de "cosmologia / cosmológic*"** — termo técnico estranho ao registro doutrinário kardecista, identificado em revisão de `bonus-hora.md` (2026-05-22). Usuário relatou uso disseminado. Levantar ocorrências em `wiki/**`, avaliar caso a caso e substituir por formas mais próximas do registro espírita ("descrição da vida espiritual", "narrativa espiritual", "panorama"). Candidato a check `info`-level (`check_no_cosmologia`) se houver volume — análogo a `check_mundos_habitados_naming`.
- [ ] **Baseline de performance do build** — registrar tempo do build do Quartz (~207 páginas) e do `link_citations.py` em CI; alertar se regredir além de threshold (ex.: +50%). Instalar velocímetro antes que doa.
- [ ] **Lint do pipeline pós-transform** — `check_broken_links` audita só o source; transforms de CI (`link_citations.py`, `wrap_glossary_terms.py`, `inject_copyright.py`) podem injetar wikilink quebrado em `/tmp/quartz/content` sem o lint pegar. Caso concreto (2026-05-22): `link_citations.py` gerava `[[obras/<slug>|…]]` sem prefixo `wiki/`. Aplicar `link_citations.py --apply` em `/tmp/quartz/content` no CI e em seguida `lint_wiki.py` apontando para esse dir (ou modo `--include-pipeline` que invoca os transforms in-memory e relinta o resultado). Trava regressão do tipo "transformer gera link quebrado" para qualquer transform futuro.
- [x] **`link_citations.py` não deve injetar wikilink em heading** (2026-05-22) — safe zone `^#+\s[^\n]*` no `SAFE_RE` (com `re.MULTILINE`) preserva heading inteiro; cobre tanto auto-link Kardec quanto wikilink complementar. Caso concreto que motivou: H3 de `wiki/conceitos/bonus-hora.md` que virava `### O sistema [[wiki/obras/nosso-lar|…]]`. Testes adicionados (`test_citation_in_heading_is_left_intact`, `test_complementar_in_heading_is_left_intact`, `test_heading_safe_zone_does_not_leak_to_next_line`). Pergunta editorial "citação em heading deveria migrar para a primeira linha do corpo?" segue em aberto — fora do escopo do fix automático.
- [x] **Skill `/ship`** (2026-05-04) — empacota ciclo commit→land com inventário via `git status/diff/log`, mensagem PT-BR, stage seletivo, invocação de `land-to-main.sh`, protocolo de `convencoes-merge.md` em conflito, lint determinístico final.
- [x] **Hook PostToolUse de lint leve por arquivo** (2026-05-04) — `lint_wiki.py --file <path>` + `.claude/hooks/lint-on-edit.py` em `Edit|Write|MultiEdit` para `wiki/**/*.md`; subset `SINGLE_FILE_CHECKS` cobre 11 checks; latência ~70ms.
- [x] **Hook PostToolUse para mirror local `wiki/**` → `/tmp/quartz/content/wiki/**`** (2026-05-26) — `.claude/hooks/mirror-to-quartz.py` em `Edit|Write|MultiEdit` copia `wiki/**/*.md` (e `index.md` da raiz) editado para o mirror; Quartz hot-rebuilda. Trava de segurança `(MIRROR_ROOT/"wiki").is_dir()` torna noop silencioso em sessão sem `serve-local.sh` ativo. Pre-processadores (`link_citations.py`, `wrap_glossary_terms.py`, `inject_copyright.py`) **não** rodam no espelhado — preview de dev fica "raw" (sem auto-link Kardecpedia, sem `<abbr>`, sem callout de direitos). Aceitável para inspeção visual de estrutura, tipografia, Mermaid e wikilinks internos; CI aplica todos os transforms no deploy.
- [x] **Rule `convencoes-merge.md`** (2026-05-04) — drivers `.gitattributes` (`merge=union`/`merge=ours`, `rerere.enabled=true`), protocolo de união cronológica em personalidades, lint antes de `git add`.
- [ ] **`/autolint` com cap de iterações e gate humano** — slash command em loop `lint → categorizar → corrigir baixo risco (broken_links com target único, frontmatter mal-formatado) → re-lint`, até zero findings ou 3 iterações, **pausando** quando o finding exige julgamento. Versão atenuada do "self-healing lint loop" — fully-autonomous viola humano-no-circuito.

---

## 6. Busca e navegação avançada

### Para o autor (local, Claude Code)

- [x] **qmd como MCP server local** — [qmd](https://github.com/tobi/qmd) (BM25 + vetorial + re-ranking, SQLite + node-llama-cpp, on-device). Base de `/ingest` e queries.

### Para o leitor público (estático, GitHub Pages)

- [ ] **Pagefind** — substituir ou complementar o flexsearch do Quartz por [Pagefind](https://pagefind.app/); índice estático no build, browser sem backend.

### Navegação

- [ ] **Índice por conceito-raiz** — hierárquico, refletindo a estrutura conceitual da doutrina (Deus > Leis Divinas > Lei de Causa e Efeito > ...).

---

## 7. Ferramentas de estudo e difusão

- [x] **Apresentações Marp** — skill `/slides` no padrão socrático Q&A (capa → perguntas/respostas com citação → parábola → síntese → fontes); build PPTX+PDF via npx; tema em `slides/themes/isabel.css`.
- [~] **Mapas conceituais** — Mermaid validado como zero-plumbing (2026-05-17): Quartz v4.4.0 já renderiza ` ```mermaid ` nativo via OFM, tema-aware; `link_citations.py`/`wrap_glossary_terms.py` pulam blocos cercados. Convenção em `convencoes-mermaid.md`; smoke-test em `wiki/sinteses/hierarquia-de-autoridade.md`. **Faltando:** lint `check_mermaid_labels` (drift de nomenclatura em rótulo não é detectado); skill `/mapa` qmd-driven e/ou derivação automática do grafo networkx do `/stats`.
- [ ] **Export temático** — PDF/EPUB de um conjunto de páginas sobre um tema, para estudo offline.
- [ ] **Flashcards** — pares pergunta/resposta a partir de `questoes/` para revisão espaçada (Anki-compatível).

---

## 8. Governança e direitos autorais

Kardec (m. 1869) e Léon Denis (m. 1927) estão em domínio público; Chico Xavier, Emmanuel, André Luiz, Bezerra, Divaldo, Joanna, Hammed **não** estão.

- [x] **Política de citação para nível 3 protegido** (2026-04-27) — CLAUDE.md §3 (limites: 400 palavras / 25% / 3 questões consecutivas) + tabela de detentores em `convencoes-direitos.md` + lint `check_quote_proportion`.
- [x] **Aviso ao leitor em obras protegidas** (2026-04-27) — `scripts/inject_copyright.py` injeta callout no topo durante o build (sobre `/tmp/quartz/content`) + nota perene em `index.md`.
- [x] **Frontmatter `direitos:` em obras nível 3** (2026-04-27) — schema aninhado documentado em `convencoes-direitos.md`; backfill nas 32 obras (23 dominio-publico, 4 FEB, 1 Boa-Nova, 5 desconhecido); lint `check_direitos_obras`.
- [x] **Status de `raw/` no Quartz** (2026-04-27) — excluído do build (`ignorePatterns`); decisão documentada em CLAUDE.md §4; lint `check_raw_excluded` (error) trava regressão.
- [ ] **Auditoria de conteúdo gerado por LLM** — `/ingest`, `/slides` e `/stats` produzem texto que entra na wiki. Em 12-24 meses, se a base for citada por terceiros, distinguir "Kardec disse X" de "síntese gerada" importa. Opções: campo `revisao_humana:` (data), marcação em rodapé, ou `## Notas` em sínteses. **Adiada para fase 2** — `/ingest` já tem humano-no-circuito; ganho marginal hoje é baixo.

---

## 9. Eficiência de tokens no workflow

Auditoria (2026-05-02) identificou três focos: leitura de `raw/` inteiros em `/ingest`, rules grandes injetadas em todo Edit, queries `qmd` sem limites.

- [x] **Disciplina nas queries `qmd`** (2026-05-02) — defaults `limit: 5`, `minScore: 0.5`, `collections=["wiki"]` na prosa de `/ingest` (Passo 2) e `/slides` (Passo 3); `busca-qmd.md` com seção "Defaults de triagem" e "Abrir o documento depois" (preferir `mcp__qmd__get` com offset a `Read` integral).
- [x] **Granularizar `convencoes-paginas.md`** (2026-05-02) — três rules: `convencoes-frontmatter.md` + `convencoes-tags.md` carregam em `wiki/**`; `convencoes-direitos.md` apenas em `wiki/obras/**`. Edições fora de `wiki/obras/` deixam de carregar ~2.6 KB por turno (12.524 vs 15.178 chars).
- [x] **Fragmentar Revista Espírita em `raw/`** — partição mensal `<ano>/<mes>-<nome>.md` (340-2141 linhas, mediana ~900). Per-artigo descartado: marcadores ausentes + `qmd get` com offset já dá granularidade.
- [x] **Haiku para triagem em `/lint` e `/glossario`** (2026-05-02) — subagente `model: "haiku"` (Explore para lint, general-purpose para glossário). Exceções documentadas; `/stats` continua 100% Python.
- [x] **Pré-resumo de obras monolíticas** (2026-05-02) — três obras nível 1 (LM 11.9K linhas, Gênese 11.1K, ESE 5.5K) com `<obra>.index.md` (estrutural, gerado por `scripts/generate_obra_index.py`) + `<obra>.resumo.md` (~500 palavras, gerado uma vez por Haiku). 6 arquivos = 245 linhas representando 28K (~115× redução).

Itens descartados: hábito de RTK (já intercepta), validação explícita de prompt caching (Claude Code já cacheia 5min), `references/` carregado sob demanda nas skills (SKILL.md 45-117 linhas — não é prioridade até passar de 200).

---

## Priorização

### Em aberto, impacto alto

- **Pipeline de palestras (§1.3)** — YouTube → transcrição → MD reduz fricção significativa.
- **Manifest de progresso em lotes longos (§1.3)** — pré-requisito de segurança do loop autônomo roadmap-driven.
- **Check determinístico de citação (§5)** — fecha ponto cego de fidelidade do `/ingest`. Bloqueado por granularidade questão/item.
- **`/autolint` (§5)** — versão atenuada do self-healing loop; complementa o hook PostToolUse.

### Médio prazo

Validação de deploy (§5); auditoria de LLM (§8 — cresce com o tempo); trilhas e glossário (§2 — impacto no leitor, não no workflow); Pagefind; baseline de build.

---

## Princípios

- **Kardec prevalece** — toda melhoria respeita a hierarquia de autoridade (CLAUDE.md §2)
- **Citação obrigatória** — nenhum conteúdo novo sem fundamentação (§3)
- **Humano no circuito** — ingest e sínteses passam pelo usuário antes de publicar
- **Incremental** — cada melhoria entrega valor isoladamente; sem dependência rígida entre eixos

---

## Estado-alvo (definition of done por eixo)

- **§1 Cobertura** — Pentateuco com cobertura conceitual ≥80% no `/stats`; cada autor de nível 3 com ≥1 obra-âncora; nenhuma personalidade-âncora citada em 5+ páginas como stub.
- **§2 Leitor público** — 5 affordances da home com trilha completa (não stub); glossário ≥100 termos; canal de feedback ✓.
- **§3 Síntese** — 10 leis morais ✓; ≥30 questões-chave do Pentateuco extraídas; ≥5 sínteses temáticas comparativas.
- **§4 Cross-references** — todas as parábolas linkam conceitos morais (e vice-versa); nenhuma página em `wiki/divergencias/` órfã do conceito que diverge.
- **§5 Automação** — lint em CI verde por 30 dias; baseline de build com alerta; testes do `link_citations.py` ✓.
- **§8 Governança** — política de fair-use ✓; nenhuma obra protegida sem `direitos:` ✓; aviso ao leitor em todas as obras nível 3 ✓. Resta `revisao_humana:` (§8.5).

Revisar a cada trimestre — alvo móvel é melhor que alvo nenhum.

---

## 10. Varredura de backlog (2026-05-31)

Descobertas concretas do `/stats` + `/lint` que apontam **páginas a escrever** (não-ingest). Cruza com eixos §1, §3 e §4 — esta seção é o instantâneo operacional; a estratégia segue lá.

### 10.1 Cobertura doutrinária — blocos do LE sub-cobertos

Medição 2026-05-26 (LE 385/1019 = 37.8%). Atualização vs. medição 2026-05-07 — blocos sub-cobertos diferentes; q.301–400 caiu de 8% (jan/26) para 16%, mas continua o pior:

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

Decisão de publicar NT em `wiki/biblia/<livro>/<capitulo>.md` foi executada (§4 — bible mapping 2026-05-22). Os 27 `wiki/biblia/<livro>/index.md` (`tipo: livro-biblico`) foram criados mas seguem como stub de 15 palavras, todos órfãos no grafo. Esquema mínimo em `convencoes-frontmatter.md` (livro-biblico): H1, nota breve (autor tradicional, ocasião, contexto histórico), lista de capítulos como wikilinks, cross-link para `wiki/obras/<evangelho/epístola>`.

- [ ] **Expandir 4 índices de Evangelhos** (`joao`, `lucas`, `marcos`, `mateus`) — mais alta prioridade pelo peso doutrinário.
- [ ] **Expandir índice de Atos e Apocalipse**.
- [ ] **Expandir 13 índices de epístolas paulinas + Hebreus** (`romanos`, `1/2-corintios`, `galatas`, `efesios`, `filipenses`, `colossenses`, `1/2-tessalonicenses`, `1/2-timoteo`, `tito`, `filemom`, `hebreus`).
- [ ] **Expandir 7 índices de epístolas católicas** (`tiago`, `1/2-pedro`, `1/2/3-joao`, `judas`).

Cada índice destrava backlink dos capítulos correspondentes (resolve em parte os 28 órfãos da varredura).

### 10.3 Rascunhos > 14 dias — promoção a `ativo`

52 páginas com `status: rascunho` e `atualizado_em` > 14 dias. Prioridade pelos ≥ 28 dias parados (15 páginas):

- **Aprofundamento**: ~~`por-que-mediuns-falham`~~ → **promovido a `ativo` em 2026-06-02** (revisão profunda: corrigidas 2 aspas fabricadas no LM cap. XX e os loci de cap. XXVIII/ESE cap. XXI; ver §5 "Auditar aspas literais fabricadas").
- **Conceitos (7)**: `calunia`, `cartas-vivas-de-jesus`, `centros-vitais`, `colonia-espiritual`, `mercantilizacao-da-mediunidade`, `passe`.
- **Obras (3)**: `missionarios-da-luz`, `obreiros-da-vida-eterna`, `os-mensageiros`.
- **Personalidades (5)**: `alexandre`, `aniceto`, `clarencio`, `jeronimo-assistente`, `lisias`.

Não é escrita "nova" — é revisão + completar Fontes + flipar `status: ativo`. Cabe em batch por categoria.

### 10.4 Aprofundamentos sugeridos por massa de vocabulário

Cruzando top-50 termos do vocabulário com `wiki/aprofundamentos/` (13 páginas hoje, cadência ingest:aprofundamento ainda desproporcional):

- [ ] **`wiki/aprofundamentos/atributos-de-deus`** — `deus` é #1 (3855 ocs). Base: LE Parte 1 + ESE cap. I-III.
- [ ] **`wiki/aprofundamentos/lugar-do-homem-na-criacao`** — `homem` (1574), `mundo` (1116), `terra` (1100). Base: LE q. 132–144, Gênese cap. XI.
- [ ] **`wiki/aprofundamentos/morte-corporal-e-passagem`** — `morte` (1223). Base: LE q. 154–165, C&I 1ª parte cap. III.

### 10.5 Sínteses panorâmicas faltantes

- [ ] **`wiki/sinteses/cristo-na-doutrina`** — `cristo` (1697) top-10 sem síntese-âncora. Articular Jesus enquanto Guia, Modelo e Governador da Terra cruzando ESE, Gênese cap. XV e C&I.
- [ ] **`wiki/sinteses/serie-andre-luiz`** — bigrama #1 (`andré luiz`, 496 ocs). Arco-narrativo dos 16 livros, leitura recomendada, lar canônico (Nosso Lar) como porta de entrada.

### 10.6 Órfãs prioritárias a integrar

Backlink + revisão (não páginas novas, mas cabe na frente de escrita):

- [ ] **`wiki/personalidades/arthur-conan-doyle`** — órfã + drift de nomenclatura ("Conan Doyle", "Sir Arthur Conan Doyle" em `catalogo.md`).
- [ ] **`wiki/conceitos/sonhos`** — órfã apesar de atravessar emancipação da alma (LE q. 400–418).
- [ ] **`wiki/aprofundamentos/silencio-interior-o-ser-consciente`** — órfã.

### Priorização sugerida

1. **§10.1 (questões LE 301–400)** — fecha o pior gap doutrinário, alimenta `/slides` e palestras.
2. **§10.2 evangelhos (4 índices)** — desbloqueia 4 evangelhos no grafo com custo baixo por página.
3. **§10.3 rascunhos ≥ 28 dias** — limpa débito visível no `/lint`.
4. **§10.4 + §10.5** — geram alavancagem (PageRank + temas dominantes do vocabulário).

## 11. Crítica profunda — itens diferidos a decisão humana

> Itens levantados por `/critica` que exigem julgamento doutrinário (não auto-corrigíveis). Formato: `- [ ] **<página>** (<eixo>, <data>) — <tensão> · evidência: <locus/cite> · relatório: <path>`

- [x] **wiki/divergencias/condenacao-dos-incredulos-em-marcos-16** (eixo 2/citação, alta, 2026-05-31) L25 — A frase entre aspas atribuída a Kardec — 'A justiça de Deus não castiga aquele que não pôde crer' — é apresentada como citação literal de (LE, q. 1009; C&I, 1ª parte, cap. VII, §VII), mas não apare… · evidência: (LE, q. 1009; C&I, 1ª parte, cap. VII; ESE, cap. XIX, item 7) vs Texto da própria página, linha 25 · relatório: reports/critica/2026-05-31-1320 · **RESOLVIDO 2026-05-31**: falsa citação literal (não consta em q. 1009 nem em C&I; `§VII` inválido) convertida em paráfrase ancorada no fragmento literal de LE q. 1009 ("uma infração de suas leis [...] praticada pelos que não as conheciam")
- [x] **wiki/divergencias/condenacao-dos-incredulos-em-marcos-16** (eixo 3/editorial, baixa, 2026-05-31) L39 — A 'Análise' reenquadra a divergência como sendo 'com a tradição dogmática literalista, não com o Evangelho em si', e introduz argumento de crítica textual (final longo de Marcos como adição posteri… · evidência: linha 39 · relatório: reports/critica/2026-05-31-1320 · **RESOLVIDO 2026-05-31**: argumento crítico-textual rebaixado de "nível de divergência" co-igual para `> [!note]` contextual (explicitando que não é de Kardec e que a refutação não depende dele); eixo doutrinário reforçado com o fragmento literal "palavras emblemáticas" de LE q. 1009; reenquadramento "não com o Evangelho em si" mantido e qualificado (conflito com o literalismo, não com o ensino de Jesus); `status: aberta` preservado
- [x] **wiki/divergencias/fogo-eterno-em-mateus-25** (eixo 2/citação, alta, 2026-05-31) L54 — A página afirma que Kardec comenta a parábola do mau rico e Lázaro (Lc 16:19–31) em 'ESE, cap. XVI, itens 7–8', tratando-a como alegórica (inversão de posições, abismo moral). · evidência: ESE, cap. V (epígrafe e itens sobre provas/expiações) vs ESE, cap. XVI, itens 7–8 · relatório: reports/critica/2026-05-31-1320 · **RESOLVIDO 2026-05-31**: diagnóstico do /critica parcialmente incorreto — a parábola está mesmo no cap. XVI (epígrafe item 5), não no cap. V, e os itens 7–8 existem (são comentário de Kardec). Erro real: itens 7–8 tratam da **riqueza como prova providencial**, não da escatologia alegórica do "abismo"/"chama". L54 reescrita: itens 7–8 atribuídos corretamente (inversão rico↔pobre como prova, com citação literal do item 8); leitura figurada de "chama"/"abismo" roteada a C&I caps. IV–VII + ESE cap. III (aiônios). Token (LE, q. 1009–1011) preservado para Item seguinte
- [x] **wiki/divergencias/fogo-eterno-em-mateus-25** (eixo 2/citação, media, 2026-05-31) L54 — A página cita 'LE, q. 1009–1011' para o progresso nas existências sucessivas que permite transpor o 'abismo'. · evidência: LE, q. 1009–1010 vs LE, q. 1009–1011 · relatório: reports/critica/2026-05-31-1320 · **RESOLVIDO 2026-05-31**: q. 1011 **não existe** no LE — Kardec salteou o n.º 1011 (Nota dos Revisores, livro-dos-espiritos.md:3299; a questão seguinte é "1012 [1011]"). Range corrigido para q. 1009–1010 (1009 = penas temporárias/cedem ao arrependimento; 1010 = pluralidade das existências/reencarnação)
- [x] **wiki/divergencias/fogo-eterno-em-mateus-25** (eixo 2/citação, alta, 2026-05-31) L29 — Atribui a C&I, 1ª parte, cap. VII, §IV a citação literal entre aspas: 'As penas são temporárias e proporcionais às faltas'. · evidência: C&I, 1ª parte, cap. VII, itens 12.º–14.º vs C&I, 1ª parte, cap. VII, §IV · relatório: reports/critica/2026-05-31-1320 · **RESOLVIDO 2026-05-31**: aspa não-literal (fundia temporariedade do item 30.º + proporcionalidade do item 3.º) e `§IV` inválido (cap. usa itens 1.º–33.º). Bullet "Temporárias" agora cita texto **literal** do item 13.º ("A duração do castigo está subordinada ao aperfeiçoamento... Nenhuma condenação por um tempo determinado é pronunciada contra ele"); removida a duplicação com a claim 2 (Proporcionais)
- [x] **wiki/divergencias/fogo-eterno-em-mateus-25** (eixo 2/citação, media, 2026-05-31) L31 — Atribui a C&I, 1ª parte, cap. VII a citação literal entre aspas: 'Deus tem por si a eternidade para aguardar o arrependimento do culpado'. · evidência: C&I, 1ª parte, cap. VII, itens 13.º/17.º/19.º vs C&I, 1ª parte, cap. VII · relatório: reports/critica/2026-05-31-1320 · **RESOLVIDO 2026-05-31**: frase **inexistente** em todo o Pentateuco (grep literal = 0). Substituída por texto literal do item 30.º ("subordinadas ao arrependimento e à reparação, que dependem da livre vontade do homem"), que corresponde exatamente ao rótulo do bullet. NOTA: a mesma falsa citação aparece em condenacao-dos-incredulos-em-marcos-16 L27 (não estava no §11) — corrigir num passe futuro
- [x] **wiki/divergencias/fogo-eterno-em-mateus-25** (eixo 2/citação, media, 2026-05-31) L34 — A página afirma que 'No ESE, cap. III (item 6), Kardec indica que a palavra grega aiônios... significa duração longa e indeterminada, não perpétua'. · evidência: LE, q. 1009; C&I, 1ª parte, cap. VII, item 15.º vs ESE, cap. III, item 6 · relatório: reports/critica/2026-05-31-1320 · **RESOLVIDO 2026-05-31**: erro duplo — ESE cap. III item 6 trata da população da Terra (não de aiônios); e "aiônios" não consta no Pentateuco (grep=0), logo a atribuição da tese grega a Kardec era falsa. Reescrito com os textos literais reais: C&I cap. VII item 15.º (nota "eterno/perpétuo = indeterminado") + LE q. 1009 ("eternidade das penas é relativa e não absoluta"). Menção ao grego *aiônios* removida (observação erudita correta, mas não é de Kardec)
- [x] **wiki/divergencias/fogo-eterno-em-mateus-25** (eixo 3/editorial, media, 2026-05-31) L3 — O frontmatter 'fontes: [ESE, "C&I", NT]' omite LE, embora a página se apoie em LE q. 1009–1010 (a fonte mais direta da refutação da eternidade das penas) em três pontos (linhas 46 e 54). · evidência: linha 3 · relatório: reports/critica/2026-05-31-1320 · **RESOLVIDO 2026-05-31**: LE adicionado a `fontes:` (primeiro, tier-1) e tag `obra/le` incluída em paralelo (derivada de fontes)
- [x] **wiki/divergencias/fogo-eterno-em-mateus-25** (eixo 3/editorial, baixa, 2026-05-31) L52 — A página usa 'kardequiana' (linha 52), enquanto o CLAUDE.md fixa 'kardecista'. · evidência: linha 52 · relatório: reports/critica/2026-05-31-1320 · **RESOLVIDO 2026-05-31**: "posição kardequiana" → "posição **de Kardec**" (regra do usuário: nunca "kardequiano/a"; usar "de Kardec"; NÃO usar "kardecista" aqui, que conota o movimento). Mesmo ajuste pendente em espiritos-e-as-leis-da-natureza L48 e sinais-de-marcos-16 L49
- [x] **wiki/divergencias/fogo-eterno-em-mateus-25** (eixo 4/tags-links, baixa, 2026-05-31) L56 — A seção 'Páginas relacionadas' omite páginas-conceito existentes e diretamente centrais ao tema (penas eternas, inferno, código penal da vida futura). · evidência: linha 56 · relatório: reports/critica/2026-05-31-1320 · **RESOLVIDO 2026-06-01**: adicionados [[wiki/conceitos/penas-eternas]], [[wiki/conceitos/inferno]], [[wiki/conceitos/codigo-penal-da-vida-futura]] e backlink recíproco a [[wiki/divergencias/morte-de-ananias-e-safira]] (divergência análoga)
- [x] **wiki/divergencias/morte-de-ananias-e-safira** (eixo 2/citação, alta, 2026-05-31) L31 — Claim 2 atribui a LE q. 1001-1008 a tese 'Deus concede ao Espírito faltoso novas provas [...] Jamais é fechada a via do arrependimento', em aspas. · evidência: LE, q. 1009 vs LE, q. 1001-1008 (como está na página) · relatório: reports/critica/2026-05-31-1320 · **RESOLVIDO 2026-06-01**: q. 1001-1008 errado (q. 1001 trata de legar bens em testamento). Aspa não-literal substituída por dois textos literais reais: C&I cap. VII item 4.º ("Deus não repudia nenhum de seus filhos") + LE q. 1008 ("acolhe sempre o arrependimento, e infrutífero jamais fica o desejo que o Espírito manifeste de se melhorar")
- [x] **wiki/divergencias/morte-de-ananias-e-safira** (eixo 2/citação, alta, 2026-05-31) L33 — Claim 3 atribui a '(LE, q. 963; ESE, cap. VI, item 6)' a frase 'Atribuir a Deus a cólera, a vingança [...] é rebaixá-lo ao nível das paixões humanas'. · evidência: LE, q. 1009 vs LE, q. 963; ESE, cap. VI, item 6 (como está na página) · relatório: reports/critica/2026-05-31-1320 · **RESOLVIDO 2026-06-01**: q. 963 (Deus se ocupa de cada homem) e ESE cap. VI item 6 (consolar os pobres) não sustentam. Aspa parafraseada substituída pelo texto literal de LE q. 1009 ("um Deus terrível, cioso e vingativo... atribuíam à divindade as paixões dos homens. Esse, todavia, não é o Deus dos cristãos")
- [x] **wiki/divergencias/morte-de-ananias-e-safira** (eixo 2/citação, alta, 2026-05-31) L35 — Claim 4 cita '(LE, q. 934; ESE, cap. X, item 20)' para 'A mentira e a hipocrisia são condenadas' e a frase 'a caridade está na intenção'. · evidência: ESE, cap. X, item 17 vs LE, q. 934; ESE, cap. X, item 20 (como está na página) · relatório: reports/critica/2026-05-31-1320 · **RESOLVIDO 2026-06-01**: q. 934 (luto) removido; ESE cap. X item 20 ("Tudo depende da intenção", sobre observar imperfeições alheias) não sustenta — e 'a caridade está na intenção' não é literal. Locus correto = ESE cap. X **item 21** (São Luís): "desmascarar a hipocrisia e a mentira pode constituir um dever". Lei de causa e efeito ancorada em C&I cap. VII item 9.º (texto literal)
- [x] **wiki/divergencias/morte-de-ananias-e-safira** (eixo 2/citação, media, 2026-05-31) L29 — Claim 1 atribui a C&I 1ª parte cap. VII a frase em aspas 'As penas não são arbitrárias; consequência lógica da falta, carregam em si mesmas o remédio'. · evidência: C&I, 1ª parte, cap. VII (penas como consequência natural) vs C&I, 1ª parte, cap. VII (aspas literais na página) · relatório: reports/critica/2026-05-31-1320 · **RESOLVIDO 2026-06-01**: aspa não-literal substituída por três textos literais reais do "Código penal da vida futura": item 14.º (duração subordinada à melhoria), item 30.º ("castigos e remédios que devem ajudar a curar as feridas do mal") e item 33.º ("traz consigo seu próprio castigo, por suas consequências naturais e inevitáveis... sem... condenação especial")
- [x] **wiki/divergencias/morte-de-ananias-e-safira** (eixo 4/tags-links, baixa, 2026-05-31) L35 — A prosa nomeia conceitos com página própria ('arrependimento', 'reparação/expiação') sem wikilink. · evidência: linha 35 · relatório: reports/critica/2026-05-31-1320 · **RESOLVIDO 2026-06-01**: wikilinks adicionados a [[wiki/conceitos/arrependimento]] (Claim 2), [[wiki/conceitos/expiacao]] e [[wiki/conceitos/leis-morais/lei-de-causa-e-efeito]] (Claim 4). `reparacao` não tem página própria — coberto por expiacao
- [x] **wiki/divergencias/sinais-de-marcos-16** (eixo 3/editorial, baixa, 2026-05-31) L49 — A linha 49 usa "A posição kardequiana é firme". · evidência: linha 49 · relatório: reports/critica/2026-05-31-1320 · **RESOLVIDO 2026-06-01**: "A posição kardequiana é firme" → "A posição de Kardec é firme"
- [x] **wiki/divergencias/sinais-de-marcos-16** (eixo 4/tags-links, baixa, 2026-05-31) L25 — O item 2 (linha 25) trata extensamente da cura por imposição de mãos e do magnetismo espiritual, sem wikilink a uma página-conceito de mediunidade de cura. · evidência: linha 25 · relatório: reports/critica/2026-05-31-1320 · **RESOLVIDO 2026-06-01**: rótulo do item 2 agora linka [[wiki/conceitos/mediunidade-de-cura]]. **Achado bônus (não estava no §11)**: L23 atribuía a "Gênese, cap. XIV, item 1" uma aspa literal inexistente na obra (grep=0; cap. XIV é "Os fluidos", não trata da definição de milagre). Corrigido para texto literal real do cap. XIII item 1 ("derrogação das leis da natureza..."; "seja ou não seja conhecida a lei, já não pode haver milagres"); Fontes/relacionadas atualizadas para caps. XIII–XV
- [x] **wiki/questoes/alma-dos-animais** (eixo 1/divergência, alta, 2026-05-31) L65 — A página afirma que o estado latente da vida inteligente animal 'sugere uma continuidade do princípio inteligente que, atravessando a escala dos seres, eventualmente alcança o estado humano — não p… · evidência: (LE, q. 613) vs wiki/questoes/alma-dos-animais.md, linha 65 (apoiada implicitamente em Léon Denis, Depois da Morte, cap. X, e André Luiz, Evolução em Dois Mu… · relatório: reports/critica/2026-05-31-1320 · **RESOLVIDO 2026-05-31**: criada `wiki/divergencias/continuidade-do-principio-inteligente-ate-o-homem` (status: aberta) e inserido `> [!warning]` + link na L65 da página-origem, registrando que LE q. 613 (conferida via cite.py) deixa o tema em aberto entre dois sistemas e inclina ao que afasta o homem da fieira animal. Pendente ainda: reenquadrar/substituir os loci de apoio (q. 540, q. 604, Gênese X,17 → q. 613) — ver item eixo 2 abaixo
- [x] **wiki/questoes/alma-dos-animais** (eixo 2/citação, media, 2026-05-31) L65 — A afirmação de que o princípio inteligente 'atravessando a escala dos seres eventualmente alcança o estado humano' é ancorada em (LE, q. 540, q. 604; Gênese, cap. X, item 17). · evidência: (LE, q. 604), (LE, q. 540), (Gênese, cap. X, item 17) vs wiki/questoes/alma-dos-animais.md, linha 65 · relatório: reports/critica/2026-05-31-1320 · **RESOLVIDO 2026-06-01**: os três loci não sustentam a ascensão (q. 540 = Espíritos que presidem fenômenos da natureza; q. 604 = "animais só possuem a inteligência da vida material", reforça a distinção; Gênese X,17 = princípio **vital**, não inteligente). Removidos da frase; reancorada em LE q. 598 (fonte literal de "estado latente", já citada na página) + LE q. 613 (os dois sistemas em aberto), em harmonia com o `> [!warning]` do eixo-1. q. 540/q. 604 preservadas onde de fato sustentam (L73/L77)
- [x] **wiki/questoes/alma-dos-animais** (eixo 4/tags-links, baixa, 2026-05-31) L11 — A prosa nomeia repetidamente 'princípio inteligente' como eixo central da página (parágrafo de abertura e várias seções), mas não há wikilink ao conceito. · evidência: linha 11 · relatório: reports/critica/2026-05-31-1320 · **RESOLVIDO 2026-06-01** (decisão do usuário: criar a página-conceito): criada `wiki/conceitos/principio-inteligente` (tipo: conceito, status: ativo) — todas as citações verificadas com `cite.py` (LE q. 23–24, q. 71–73, q. 597–600, q. 604–605, q. 611–613; Gênese cap. XI item 6). L11 agora linka [[wiki/conceitos/principio-inteligente]] (e "discussão **kardequiana**" → "discussão **de Kardec**", achado bônus). Backlinks recíprocos em principio-vital, conceito/questao/divergência irmãs; entrada em catalogo.md (Princípio vital e fluidos). Destrava o último item de §11 — agora **28/28**
- [x] **wiki/questoes/espiritos-e-as-leis-da-natureza** (eixo 2/citação, media, 2026-05-31) L42 — A página apresenta como CITAÇÃO LITERAL de Kardec (aspas + reticências + locus 'Gênese, cap. XIII, item 1; cap. XV') a frase: 'Os milagres, no sentido teológico do termo, […] constituiriam uma derr… · evidência: (Gênese, cap. XIII, item 1) vs Linha 42 da página (blockquote inline com aspas) · relatório: reports/critica/2026-05-31-1320 · **RESOLVIDO 2026-06-01**: aspa fabricada (condicional "constituiriam" + "o que não pode ser" não existem na obra) substituída pelo texto literal real de Gênese cap. XIII item 1 ("no sentido teológico, é uma derrogação das leis da natureza, por meio da qual Deus manifesta o seu poder"), reenquadrada como a definição teológica que Kardec recusa. Corrigido de passagem o título do cap. XIII em Fontes ("Os fluidos" → "Caracteres dos milagres"; "Os fluidos" é o cap. XIV)
- [x] **wiki/questoes/espiritos-e-as-leis-da-natureza** (eixo 3/editorial, baixa, 2026-05-31) L48 — Linha 48 usa 'doutrina kardequiana'. O projeto (CLAUDE.md) padroniza 'kardecista' e proíbe 'kardequista', mas não fixa explicitamente a forma do adjetivo derivado de Kardec ('kardequiano/a' é forma… · evidência: linha 48 · relatório: reports/critica/2026-05-31-1320 · **RESOLVIDO 2026-06-01**: "Na doutrina kardequiana:" → "Na doutrina de Kardec:" (regra do usuário: nunca "kardequiano/a"; usar "de Kardec")
- [x] **wiki/questoes/espiritos-e-as-leis-da-natureza** (eixo 4/tags-links, baixa, 2026-05-31) L59 — Item 'Prece e providência' (linha 59) discute a prece e cita ESE cap. XXVII item 10, mas não há wikilink para a página-conceito existente wiki/conceitos/prece. · evidência: linha 59 · relatório: reports/critica/2026-05-31-1320 · **RESOLVIDO 2026-06-01**: rótulo do item agora linka [[wiki/conceitos/prece|Prece]]
- [x] **wiki/questoes/fora-da-caridade-nao-ha-salvacao** (eixo 3/editorial, baixa, 2026-05-31) L2 — O tipo declarado é 'questao', cuja convenção pede ancoragem em UMA única questão/item pontual; mas a página atravessa os itens 1-10 do ESE cap. XV, mais LE q. 886 e Viagem Espírita em 1862 — escopo… · evidência: linha 2 · relatório: reports/critica/2026-05-31-1320 · **RESOLVIDO 2026-06-01** (decisão do usuário): reclassificada `questao` → **aprofundamento**. `grau/introdutorio` → `grau/avancado`; estrutura reorganizada (Contexto doutrinário · A máxima/citação literal · Comentário de Kardec · Instrução de Paulo · Análise por eixos · Síntese · Aprofundamento); arquivo movido `wiki/questoes/` → `wiki/aprofundamentos/` (git mv) com 7 wikilinks de entrada reescritos e entrada do `catalogo.md` repositionada de Questões → Aprofundamentos
- [x] **wiki/questoes/fora-da-caridade-nao-ha-salvacao** (eixo 4/tags-links, baixa, 2026-05-31) L4 — tema/prece-caridade (eixo 'adoração, prece, caridade prática') também seria defensável, dado o foco em caridade ativa/praticada. · evidência: linha 4 · relatório: reports/critica/2026-05-31-1320 · **RESOLVIDO 2026-06-01**: adicionada tag `tema/prece-caridade` (agora 3 tema/*: moral + jesus + prece-caridade). Nova localização: `wiki/aprofundamentos/fora-da-caridade-nao-ha-salvacao`
- [x] **wiki/questoes/o-que-e-deus** (eixo 2/citação, media, 2026-05-31) L54 — Linha 54: a página afirma que o atributo da q. 2 é 'infinito em suas perfeições' — 'e do atributo complementar da q. 2 (infinito em suas perfeições)'. · evidência: (LE, q. 2) e (LE, q. 3, nota de Kardec) vs wiki/questoes/o-que-e-deus.md, linha 54 · relatório: reports/critica/2026-05-31-1320 · **RESOLVIDO 2026-06-01**: q. 2 define "infinito" abstratamente ("o que não tem começo nem fim; o desconhecido"). A formulação "infinito em suas perfeições" é da **nota de Kardec à q. 3**. L54 reescrita: atributos completados "pela nota de Kardec à q. 3, segundo a qual 'Deus é infinito em suas perfeições, mas o infinito é uma abstração'" (texto literal)
- [x] **wiki/questoes/pactos-com-satanas-como-alegoria** (eixo 2/citação, media, 2026-05-31) L29 — A página afirma que a distinção entre símbolo alegórico (verdade moral em roupagem figurada) e narrativa literal é estabelecida 'em A Gênese (caps. II–III) e em O Evangelho Segundo o Espiritismo (c… · evidência: (LE, q. 131); (LE, q. 550) vs (ESE, cap. XIV, item 7); (Gênese, caps. II–III) · relatório: reports/critica/2026-05-31-1320 · **RESOLVIDO 2026-06-01**: Gênese caps. II–III ("Deus"/"O bem e o mal") e ESE cap. XIV item 7 (indiferença aparente de Jesus à mãe) não enunciam o princípio hermenêutico. Loci substituídos por Gênese **cap. XII** ("Gênese moisaica"), onde Kardec lê o Éden/serpente/tentador como alegoria, com o texto literal do item 16 ("podem ser tomadas em sentido material, moral, alegórico, em sentido próprio e figurado"); o princípio também está na própria q. 550 já citada
- [x] **wiki/questoes/pactos-com-satanas-como-alegoria** (eixo 4/tags-links, baixa, 2026-05-31) L4 — A página tem uma seção substancial 'Conexão com obsessão' (LM, 2ª parte, cap. XXIII; LE q. 498) que atravessa o eixo da mediunidade/obsessão, mas só carrega tema/espiritos. · evidência: linha 4 · relatório: reports/critica/2026-05-31-1320 · **RESOLVIDO 2026-06-01**: adicionada tag `tema/mediunidade` (agora 2 tema/*, dentro do limite 1-3)
