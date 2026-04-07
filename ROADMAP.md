# Roadmap — IsAbel Wiki Espírita

> Melhorias de maior complexidade planejadas para a wiki.
> Organizadas por eixo temático, não por ordem cronológica.

---

## Estado atual (abril 2026)

- 194 páginas wiki (97 conceitos, 80 entidades, 13 obras, 2 divergências, 1 questão, 1 síntese)
- Publicação via Quartz v4.4.0 + GitHub Actions + GitHub Pages
- Skills `/lint` e `/ingest` operacionais
- 4/5 do Pentateuco ingerido (falta O Livro dos Médiuns)
- Zero erros de lint

---

## 1. Cobertura de fontes

Completar a base doutrinária para que o leitor encontre o essencial da codificação.

- [ ] **Ingerir O Livro dos Médiuns** — última obra do Pentateuco pendente; fonte já existe em `raw/kardec/pentateuco/livro-dos-mediuns.md`
- [ ] **Ingerir Kardec complementar** — 5 fontes já em `raw/kardec/complementares/` (O Que é o Espiritismo, Obras Póstumas, Instruções Práticas, Viagem Espírita, Resumo da Lei dos Fenômenos Espíritas)
- [ ] **Expandir autores nível 3** — Chico Xavier (O Consolador, Nosso Lar), Cairbar Schutel, Martins Peralva, Eurípedes Barsanulfo; pastas já criadas em `raw/` mas sem conversão MD
- [ ] **Pipeline de palestras** — consolidar workflow YouTube → transcrição → summary → ingest; hoje funciona mas é manual demais

---

## 2. Experiência do leitor público

A wiki já é publicada, mas foi pensada para uso pessoal. Adaptar para que qualquer estudante sério consiga navegar e aprender.

- [ ] **Página de boas-vindas** — substituir o index do Quartz por uma landing page com: propósito da wiki, como navegar, hierarquia de autoridade, aviso de que é work-in-progress
- [ ] **Trilhas de estudo guiadas** — páginas especiais que sequenciam conceitos para quem está começando (ex: "Primeiros passos no Espiritismo", "As Leis Morais em ordem", "Mediunidade: do básico ao avançado")
- [ ] **Glossário navegável** — página consolidada com definições curtas de todos os conceitos, linkando para as páginas completas; útil como ponto de entrada rápido
- [ ] **Melhorar tags e filtragem** — enriquecer tags no frontmatter para permitir navegação temática no Quartz (ex: por lei moral, por obra de origem, por grau de complexidade)
- [ ] **Breadcrumbs semânticos** — revisar estrutura de pastas para que os breadcrumbs do Quartz façam sentido para o leitor (Conceitos > Leis Morais > Lei de Causa e Efeito)

---

## 3. Conteúdo de síntese e estudo

As categorias `questoes/` e `sinteses/` estão sub-representadas (1 página cada). São as mais valiosas para o leitor.

- [ ] **Extrair questões-chave do Pentateuco** — selecionar as questões mais importantes de cada obra e criar páginas em `questoes/` com pergunta, resposta dos Espíritos, comentário de Kardec e análise
- [ ] **Sínteses temáticas** — criar comparativos entre obras sobre o mesmo tema (ex: "O que cada obra diz sobre obsessão", "Reencarnação: de Kardec a Léon Denis")
- [ ] **Quadros comparativos** — tabelas que cruzam conceitos entre obras ou autores, úteis para estudo sistemático
- [ ] **Perguntas frequentes** — página de FAQ baseada em dúvidas comuns de estudantes, com respostas fundamentadas e citadas

---

## 4. Cross-references enriquecidas

A wiki tem links, mas pode ser mais densa em conexões — o grafo do Quartz fica mais útil quanto mais interligado.

- [ ] **Parábolas ↔ conceitos** — cada parábola do ESE deve linkar explicitamente os conceitos morais que ilustra, e vice-versa
- [ ] **Leis morais ↔ exemplos práticos** — conectar cada lei moral a parábolas, questões e casos concretos que a exemplificam
- [ ] **Entidades ↔ conceitos** — Espíritos citados em C&I e outras obras devem linkar para os conceitos que suas histórias ilustram
- [ ] **Obras ↔ obras** — referências cruzadas quando uma obra cita ou complementa outra (ex: Gênese referencia LE em vários pontos)
- [ ] **Grafo temático** — considerar criar "hub pages" por tema que agreguem todos os links relevantes (ex: hub de "Mediunidade" linkando conceitos, entidades, obras, questões)

---

## 5. Qualidade e automação

Hoje o lint roda sob demanda. Automatizar para manter a qualidade conforme a wiki cresce.

- [ ] **Lint em CI** — rodar `lint_wiki.py` no GitHub Actions em cada PR; falhar o build se houver erros críticos (links quebrados, frontmatter inválido)
- [ ] **Métricas de cobertura** — script que gera relatório: % do Pentateuco coberto, conceitos sem página própria, entidades mencionadas mas sem página, razão conceitos/questões
- [ ] **Validação de deploy** — checar se o build do Quartz não quebrou links internos após cada deploy
- [ ] **Lint evolutivo** — adicionar checks: páginas com poucas citações, conceitos referenciados em 5+ páginas mas sem página própria, inconsistências de nomenclatura entre páginas

---

## 6. Busca e navegação avançada

O Quartz tem busca full-text básica. Para queries mais sofisticadas (especialmente via LLM), precisamos de mais.

- [ ] **Busca híbrida local** — integrar [qmd](https://github.com/tobi/qmd) ou similar para busca BM25 + vetorial sobre as páginas wiki; útil para o LLM encontrar páginas relevantes em queries complexas
- [ ] **MCP server de busca** — expor a busca como tool MCP para que o Claude Code consulte a wiki semanticamente durante queries
- [ ] **Índice por conceito-raiz** — além do `index.md` linear, criar índice hierárquico que reflita a estrutura conceitual da doutrina (Deus > Leis Divinas > Lei de Causa e Efeito > ...)

---

## 7. Ferramentas de estudo e difusão

Formatos além de markdown para tornar o conteúdo mais acessível.

- [ ] **Apresentações Marp** — gerar slides a partir de páginas wiki para uso em palestras; criar skill `/slides` que monta deck a partir de um tema
- [ ] **Mapas conceituais** — gerar visualizações (Mermaid ou similar) das relações entre conceitos de um tema
- [ ] **Export temático** — gerar PDF/EPUB de um conjunto de páginas sobre um tema, para estudo offline
- [ ] **Flashcards** — gerar pares pergunta/resposta a partir de `questoes/` para revisão espaçada (formato Anki-compatível)

---

## Princípios

- **Kardec prevalece** — toda melhoria respeita a hierarquia de autoridade (seção 2 do CLAUDE.md)
- **Citação obrigatória** — nenhum conteúdo novo sem fundamentação (seção 4)
- **Humano no circuito** — ingest e sínteses passam pelo usuário antes de serem publicados
- **Incremental** — cada melhoria entrega valor isoladamente; não há dependência rígida entre eixos
