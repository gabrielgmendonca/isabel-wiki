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

**Nível 1 — Pentateuco**
- [x] Pentateuco 5/5 (fechado com *O Livro dos Médiuns*).

**Nível 2 — Kardec complementar** (3 de 6 pendentes)
- [ ] **Ingerir 3 fontes restantes** em `raw/kardec/complementares/`: Instruções Práticas, Resumo da Lei dos Fenômenos Espíritas, Espiritismo em Sua Mais Simples Expressão. Já ingeridas: O Que é o Espiritismo, Obras Póstumas, Viagem Espírita em 1862.

**Novo Testamento canônico**
- [x] 27/27 completo (fechado 2026-05-18 com 2-João, 3-João, Judas). Tratamento inline de divergências culturais; cross-link a páginas estruturais já existentes.

**Nível 3 — Consagrados** (cobertura parcial)
- [ ] **Léon Denis** — 4 obras ingeridas. Levantar restante prioritário.
- [ ] **Chico Xavier** — *A Caminho da Luz* e *O Consolador* ingeridos; falta âncora André Luiz *Nosso Lar* (1944, abre a série).
- [ ] **Cairbar Schutel, Martins Peralva, Eurípedes Barsanulfo** — sem obra-âncora. Definition of done exige ≥1 por autor.

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
- [ ] **Linkar referências bíblicas** — `(Mateus 5:3)`, `(João 14:2)` etc. para Bíblia online (ACF já está em `raw/biblia-acf/`).
- [ ] **Decisão sobre `wiki/biblia/`** — pré-requisito do item acima. (a) publicar como `wiki/biblia/<livro>/<capitulo>.md`, (b) manter externo, ou (c) híbrido — só os livros já tratados em `wiki/obras/biblia/` (Mateus, Marcos, Lucas, João, Atos). Afeta tamanho da wiki, ruído no grafo do Quartz e output do `link_citations.py`.

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
- [ ] **Versão estrita do check** — verifica que o trecho citado **sustenta** a afirmação, não só que o locus existe. Bloqueado: depende da granularidade por questão/item em `raw/kardec/pentateuco/` (§4 "fase 2 do híbrido"). Sem isso, a checagem da camada baixa cobre os erros de typo/sigla, mas alegação como "Kardec diz X em (LE, q. 460)" quando q. 460 trata de Y permanece editorial.
- [x] **Aliases canônicos para personalidades e obras** (2026-05-04) — `convencoes-aliases.md` (canônico = H1; aliases ≥ 4 caracteres em `aliases:`) + backfill em 9 páginas-âncora + lint `check_canonical_names` (info-level) surfando 32 candidatos.
- [x] **Uniformizar tipos de mundos habitados** (2026-05-05) — fonte canônica fixada em **ESE cap. III, item 4** (não Gênese cap. III como o ROADMAP grafava). Rule `convencoes-mundos-habitados.md` + 2 páginas-conceito novas (`mundos-primitivos`, `mundos-celestes-ou-divinos`) + lint `check_mundos_habitados_naming` + backfill em 10 arquivos.
- [ ] **Varredura de "cosmologia / cosmológic*"** — termo técnico estranho ao registro doutrinário kardecista, identificado em revisão de `bonus-hora.md` (2026-05-22). Usuário relatou uso disseminado. Levantar ocorrências em `wiki/**`, avaliar caso a caso e substituir por formas mais próximas do registro espírita ("descrição da vida espiritual", "narrativa espiritual", "panorama"). Candidato a check `info`-level (`check_no_cosmologia`) se houver volume — análogo a `check_mundos_habitados_naming`.
- [ ] **Baseline de performance do build** — registrar tempo do build do Quartz (~207 páginas) e do `link_citations.py` em CI; alertar se regredir além de threshold (ex.: +50%). Instalar velocímetro antes que doa.
- [ ] **Lint do pipeline pós-transform** — `check_broken_links` audita só o source; transforms de CI (`link_citations.py`, `wrap_glossary_terms.py`, `inject_copyright.py`) podem injetar wikilink quebrado em `/tmp/quartz/content` sem o lint pegar. Caso concreto (2026-05-22): `link_citations.py` gerava `[[obras/<slug>|…]]` sem prefixo `wiki/`. Aplicar `link_citations.py --apply` em `/tmp/quartz/content` no CI e em seguida `lint_wiki.py` apontando para esse dir (ou modo `--include-pipeline` que invoca os transforms in-memory e relinta o resultado). Trava regressão do tipo "transformer gera link quebrado" para qualquer transform futuro.
- [x] **Skill `/ship`** (2026-05-04) — empacota ciclo commit→land com inventário via `git status/diff/log`, mensagem PT-BR, stage seletivo, invocação de `land-to-main.sh`, protocolo de `convencoes-merge.md` em conflito, lint determinístico final.
- [x] **Hook PostToolUse de lint leve por arquivo** (2026-05-04) — `lint_wiki.py --file <path>` + `.claude/hooks/lint-on-edit.py` em `Edit|Write|MultiEdit` para `wiki/**/*.md`; subset `SINGLE_FILE_CHECKS` cobre 11 checks; latência ~70ms.
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
- **Decisão sobre `wiki/biblia/` (§4)** — destrava "linkar referências bíblicas" e dá casa estrutural ao NT já ingerido. Não é trabalho grande; é uma escolha.
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
