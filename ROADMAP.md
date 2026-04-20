# Roadmap — IsAbel Wiki Espírita

> Melhorias de maior complexidade planejadas para a wiki.
> Organizadas por eixo temático, não por ordem cronológica.

---

## 1. Cobertura de fontes

Completar a base doutrinária para que o leitor encontre o essencial da codificação.

- [x] **Ingerir O Livro dos Médiuns** — concluído
- [ ] **Ingerir Kardec complementar** — 6 fontes em `raw/kardec/complementares/`; 3 já ingeridas (O Que é o Espiritismo, Obras Póstumas, Viagem Espírita); faltam Instruções Práticas, Resumo da Lei dos Fenômenos Espíritas, Espiritismo em Sua Mais Simples Expressão
- [ ] **Expandir autores nível 3** — Léon Denis avançado (4 obras ingeridas), Chico Xavier parcial (A Caminho da Luz ingerido); faltam O Consolador, Nosso Lar, Cairbar Schutel, Martins Peralva, Eurípedes Barsanulfo
- [ ] **Ingerir Novo Testamento restante** — Evangelhos + Atos já ingeridos. Prioridade sugerida pelos escritos apostólicos (nível 3, seletivamente citados por Kardec):
  1. **1-coríntios** — cap. 13 (caridade) e 15 (ressurreição/corpo espiritual), muito citados no ESE
  2. **romanos** — Paulo sobre fé, lei moral, livre-arbítrio
  3. **tiago** — "fé sem obras é morta", linguagem próxima ao ESE
  4. **1-joão** — "Deus é amor", discernimento de espíritos (4:1)
  5. **1-pedro** — pregação aos espíritos em prisão (3:19), reabilitação
  6. **hebreus** — tipologia sacerdotal, fé
  7. Demais paulinas (2-coríntios, gálatas, efésios, filipenses, colossenses, 1/2-tessalonicenses, 1/2-timóteo, tito, filemom) e gerais (2-pedro, 2/3-joão, judas)
  8. **apocalipse** — usar com cautela; Kardec interpreta seletivamente na *Gênese*
- [ ] **Expandir personalidades-âncora** — várias personalidades centrais estão como stubs (<105 palavras): Chico Xavier (88), Carlos Mendonça (61), Espíritos Reveladores (103), Joseph Brès (97), Eric Stanislas (104). Priorizar as referenciadas em 5+ páginas — completar identificação, papel doutrinário, obras associadas e citações relevantes
- [ ] **Pipeline de palestras** — consolidar workflow YouTube → transcrição → summary → ingest; hoje funciona mas é manual demais

---

## 2. Experiência do leitor público

A wiki já é publicada, mas foi pensada para uso pessoal. Adaptar para que qualquer estudante sério consiga navegar e aprender.

- [x] **Página de boas-vindas** — substituir o index do Quartz por uma landing page com: propósito da wiki, como navegar, hierarquia de autoridade, aviso de que é work-in-progress
- [x] **Home orientada por affordances** — `index.md` reescrito como grid de cartões (Chegando agora, ESDE, Palestras, Leitura livre, Consulta rápida); catálogo linear removido em favor do Explorer + Search do Quartz
- [~] **Trilhas de estudo guiadas** — stubs criados em `wiki/trilhas/` (primeiros-passos, esde, palestras, leitura-livre) como destinos dos cartões da home. Expandir cada trilha com sequência comentada, leituras complementares e aferição de progresso ainda é TODO. Considerar também "As Leis Morais em ordem" e "Mediunidade: do básico ao avançado"
- [~] **Glossário navegável** — stub em `wiki/sinteses/glossario.md` com ~15 conceitos-raiz (Deus, Espírito, alma, perispírito, reencarnação, mediunidade, obsessão, prece, caridade, fluido cósmico, escala espírita, expiação, livre-arbítrio, anjos, transição planetária). Popular com os ~126 conceitos restantes, ordenados alfabeticamente com uma linha por termo, é TODO
- [ ] **Expandir affordances da home** — considerar 6ª/7ª entrada (ex.: "Divergências" para leitores curiosos, "Personalidades" para quem estuda mediunidade e C&I) conforme a wiki crescer. Manter 5 hoje para não sobrecarregar
- [ ] **Melhorar tags e filtragem** — enriquecer tags no frontmatter para permitir navegação temática no Quartz (ex: por lei moral, por obra de origem, por grau de complexidade)
- [ ] **Breadcrumbs semânticos** — revisar estrutura de pastas para que os breadcrumbs do Quartz façam sentido para o leitor (Conceitos > Leis Morais > Lei de Causa e Efeito)

---

## 3. Conteúdo de síntese e estudo

As categorias `questoes/` e `sinteses/` estão sub-representadas. São as mais valiosas para o leitor.

- [ ] **Extrair questões-chave do Pentateuco** — selecionar as questões mais importantes de cada obra e criar páginas em `questoes/` com pergunta, resposta dos Espíritos, comentário de Kardec e análise
- [ ] **Completar páginas das 10 Leis Morais** — 4 das 10 leis estão como stubs (<105 palavras): Trabalho, Adoração, Reprodução, Sociedade. São conceitos centrais da Parte 3 do LE (q. 649-919) e fundamento da tag-namespace `lei/`. Expandir com: definição, ensino dos Espíritos, desdobramentos, aplicação prática e cruzamento com ESE
- [ ] **Sínteses temáticas** — criar comparativos entre obras sobre o mesmo tema (ex: "O que cada obra diz sobre obsessão", "Reencarnação: de Kardec a Léon Denis")
- [ ] **Quadros comparativos** — tabelas que cruzam conceitos entre obras ou autores, úteis para estudo sistemático
- [ ] **Perguntas frequentes** — página de FAQ baseada em dúvidas comuns de estudantes, com respostas fundamentadas e citadas

---

## 4. Cross-references enriquecidas

A wiki tem links, mas pode ser mais densa em conexões — o grafo do Quartz fica mais útil quanto mais interligado.

- [ ] **Parábolas ↔ conceitos** — cada parábola do ESE deve linkar explicitamente os conceitos morais que ilustra, e vice-versa
- [ ] **Leis morais ↔ exemplos práticos** — conectar cada lei moral a parábolas, questões e casos concretos que a exemplificam
- [ ] **Personalidades ↔ conceitos** — Espíritos citados em C&I e outras obras devem linkar para os conceitos que suas histórias ilustram
- [ ] **Obras ↔ obras** — referências cruzadas quando uma obra cita ou complementa outra (ex: Gênese referencia LE em vários pontos)
- [ ] **Grafo temático** — considerar criar "hub pages" por tema que agreguem todos os links relevantes (ex: hub de "Mediunidade" linkando conceitos, personalidades, obras, questões)

### Citações inline como links

Após a fase 1 (auto-link Markdown→Kardecpedia em build time, capítulo — `scripts/link_citations.py`), aprofundar:

- [ ] **Fase 2 do híbrido — link interno preferencial** — normalizar `raw/kardec/pentateuco/*.md` com headings granulares (`## q. 990`, `## cap. VII, item 16`), remover `raw` do `ignorePatterns` do Quartz e fazer o pré-processador preferir link interno sobre Kardecpedia quando disponível
- [ ] **Cobrir Kardec complementar no auto-link** — estender mapping para `RE` (Revista Espírita), `OPE` (Obras Póstumas), `OQE` (O Que é o Espiritismo), `Viagem Espírita em 1862`
- [ ] **Granularidade por questão/item** — mapear não só capítulos mas itens individuais no Kardecpedia (link direto à q. 990 em vez de ao topo do cap. II); o crawler já coleta os ids, falta usar
- [ ] **Linkar referências bíblicas** — `(Mateus 5:3)`, `(João 14:2)` etc. para uma fonte bíblica online (ACF já existe em `raw/biblia-acf/`; eventual publicação no Quartz dá link interno)

---

## 5. Qualidade e automação

Hoje o lint roda sob demanda. Automatizar para manter a qualidade conforme a wiki cresce.

- [x] **Lint em CI** — `lint_wiki.py` roda no GitHub Actions (`deploy-wiki.yml`) em cada push
- [x] **Métricas de cobertura** — `stats_wiki.py` agora gera: % do Pentateuco citado por obra (LE 215/1019 = 21%, ESE 28/28, Gênese 10/18, LM 24/33, C&I 18/18), cobertura do LE por bloco de 100 questões, wikilinks quebrados com freq ≥ 5, razão conceitos/questões e sugestões automáticas priorizadas (blocos LE sub-cobertos, razão distorcida, targets candidatos a nova página). Fase 2 — detectar conceitos mencionados em texto fluido sem wikilink — fica para quando a fase 1 exibir gaps
- [ ] **Validação de deploy** — checar se o build do Quartz não quebrou links internos após cada deploy
- [ ] **Lint evolutivo** — adicionar checks: páginas com poucas citações, conceitos referenciados em 5+ páginas mas sem página própria, inconsistências de nomenclatura entre páginas
- [x] **Higiene do script de estatísticas** — meta-páginas (`tipo: sintese` + tag `meta`) excluídas de grafo, vocabulário e tamanho; seções-template (`## Fontes`, `## Páginas relacionadas`, `## Páginas referenciadas`, `## Conceitos relacionados`) removidas antes da tokenização. Top bigramas agora refletem doutrina ("mundo espiritual", "ensino kardec", "aplicação prática") em vez de aparato bibliográfico

---

## 6. Busca e navegação avançada

### Para o autor (local, Claude Code)

O Quartz tem busca full-text básica, suficiente para o leitor. Para queries semânticas durante ingest, sínteses e estudo via LLM, precisamos de busca local mais sofisticada.

- [x] **qmd como MCP server local** — integrar [qmd](https://github.com/tobi/qmd) (BM25 + vetorial + re-ranking, tudo on-device) como MCP server para que o Claude Code consulte a wiki semanticamente durante `/ingest`, queries e sínteses. Roda localmente com SQLite + node-llama-cpp, sem servidor externo.

### Para o leitor público (estático, GitHub Pages)

- [ ] **Pagefind** — substituir ou complementar o flexsearch do Quartz por [Pagefind](https://pagefind.app/), que gera índice estático no build e roda no browser sem backend. Integrável ao GH Actions.

### Navegação

- [ ] **Índice por conceito-raiz** — além do `index.md` linear, criar índice hierárquico que reflita a estrutura conceitual da doutrina (Deus > Leis Divinas > Lei de Causa e Efeito > ...)

---

## 7. Ferramentas de estudo e difusão

Formatos além de markdown para tornar o conteúdo mais acessível.

- [x] **Apresentações Marp** — skill `/slides <página-wiki>` gera deck Marp no padrão socrático Q&A (capa → perguntas/respostas com citação → parábola → síntese → fontes); build PPTX+PDF via npx; tema customizado em `slides/themes/isabel.css`
- [ ] **Mapas conceituais** — gerar visualizações (Mermaid ou similar) das relações entre conceitos de um tema
- [ ] **Export temático** — gerar PDF/EPUB de um conjunto de páginas sobre um tema, para estudo offline
- [ ] **Flashcards** — gerar pares pergunta/resposta a partir de `questoes/` para revisão espaçada (formato Anki-compatível)

---

## Priorização para o workflow autor + Claude Code

Itens ranqueados pelo impacto na qualidade e velocidade de construção da wiki (ingest, queries, sínteses).

### Impacto alto — muda o jogo

1. **qmd como MCP server local (§6)** — Hoje o Claude Code busca páginas relevantes lendo `index.md` e abrindo arquivos um a um. Busca semântica local permitiria: encontrar todos os conceitos relacionados durante ingest (menos duplicatas, mais cross-references), detectar contradições entre fonte nova e wiki existente, responder queries com cobertura completa. É a diferença entre "procurar num índice" e "entender o corpus".
2. **Métricas de cobertura (§5)** — Saber o que falta é tão valioso quanto saber o que existe. Um script que reporte conceitos mencionados em 5+ páginas sem página própria, % do Pentateuco coberto, razão conceitos/questões — dá lista de trabalho priorizada em vez de depender de intuição.
3. **Lint evolutivo (§5)** — Checks de conteúdo (páginas com poucas citações, nomenclatura inconsistente) mantêm qualidade conforme a wiki cresce. Hoje isso depende de o Claude Code "perceber" problemas durante ingest.

### Impacto médio — acelera o que já funciona

4. **Pipeline de palestras (§1)** — Automatizar YouTube → transcrição → MD reduz fricção significativa; cada palestra hoje exige vários passos manuais antes do ingest.
5. **Lint em CI (§5)** — Rede de segurança útil, mas já rodamos `/lint` manualmente; ganho incremental.

### Impacto menor para o workflow (alto para o leitor)

- Trilhas de estudo, glossário, Pagefind, breadcrumbs — ótimos para o leitor público, mas não mudam como o conteúdo é construído.

---

## Princípios

- **Kardec prevalece** — toda melhoria respeita a hierarquia de autoridade (seção 2 do CLAUDE.md)
- **Citação obrigatória** — nenhum conteúdo novo sem fundamentação (seção 4)
- **Humano no circuito** — ingest e sínteses passam pelo usuário antes de serem publicados
- **Incremental** — cada melhoria entrega valor isoladamente; não há dependência rígida entre eixos
