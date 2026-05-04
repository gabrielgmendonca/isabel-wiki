# Roadmap — IsAbel Wiki Espírita

> Melhorias de maior complexidade planejadas para a wiki.
> Organizadas por eixo temático, não por ordem cronológica.

---

## 0. Higiene das skills e documentação (concluído 2026-04-26)

Tirados de uma auditoria de `CLAUDE.md` + 4 skills + rules + hook (2026-04-26). Resolvidos em bloco antes de avançar para §1+: bugs factuais, lacunas de doc, DRY, UX e config. Lint passa sem regressão (`skills_consistency: 0`).

### 0.1 Inconsistências factuais (bugs)

- [x] **`wiki/parabolas/` fantasma** — 3 referências redirecionadas para `wiki/sinteses/parabolas-de-jesus`. Diretório permanece não criado; parábolas seguem como índice único.
- [x] **CLAUDE.md §4 lista só `/ingest` e `/lint`** — `/slides` e `/stats` adicionados como bullets em §4.
- [x] **`/ingest` Passo 0 cita só "Nível 1, 2 ou 3"** — corrigido para "Nível 1, 2, 3 ou 4".
- [x] **`EnterPlanMode` vs auto mode** — instrução reescrita para "apresente o outline em texto e aguarde confirmação", robusta a ambos os modos. Plan mode continua sendo a implementação canônica em modo manual.

### 0.2 Lacunas de documentação

- [x] **Autoria de psicografias** — promovida para CLAUDE.md §3 como subseção própria (`Autor espiritual / Médium`). `slides/SKILL.md` agora referencia §3.
- [x] **Uso do `qmd`** — documentado em §4 (subseção Query): coleções `raw`/`wiki`, tipos `lex`/`vec`/`hyde`, quando combinar.
- [x] **Regra `uv run python`** — extraída para `.claude/rules/scripts.md` com `paths: .claude/skills/**`. Hook injeta automaticamente quando se edita skill. PyYAML adicionado ao `pyproject.toml` para o hook.
- [x] **Promover "default = oferecer arquivar"** — virou subseção dedicada em §4 com 3 sub-bullets (sinteses/aprofundamentos/questoes).
- [x] **Regra prática Jesus-vs-Kardec** — adicionado parágrafo em §2 com protocolo prático (alegoria, interpolação, contexto semita).

### 0.3 DRY / manutenibilidade

- [x] **Deduplicar formato de citação** — `convencoes-slides.md` agora referencia §3 sem repetir exemplos.
- [x] **Lint não loga em `log.md` quando é puro diagnóstico** — Passo 5 reescrito para logar só quando o usuário corrige achados.

### 0.4 UX / fluxo

- [x] **Skill `/estudo`** (originalmente proposta como `/query`) — decisão: não criar skill autocontido. Workflow promovido a subseção dedicada em CLAUDE.md §4. Mais leve, mesma orientação.
- [x] **`/ingest` sugerir `/lint` no final** — Passo 10 sugere rodar `/lint` após ingest.
- [x] **`/ingest` usar qmd para checar duplicatas** — novo Passo 3 com query `lex` + `vec` em `wiki/` antes de criar páginas.

### 0.5 Higiene de config

- [x] **Limpar `settings.local.json`** — removidos `Bash(qmd query/search/vsearch/status:*)` (cobertos por `mcp__qmd__*`) e entradas one-off de teste (`unzip ...pptx`, `Read(//tmp/test_pptx/...)`).
- [x] **`inject-rules.py` parser YAML** — migrado para `yaml.safe_load`; erros logados em stderr; hook command em `.claude/settings.json` agora usa `uv run --project ... python` para acessar PyYAML do venv. Smoke-tested.

---

## 1. Cobertura de fontes

Completar a base doutrinária para que o leitor encontre o essencial da codificação.

- [x] **Ingerir O Livro dos Médiuns** — concluído
- [ ] **Ingerir Kardec complementar** — 6 fontes em `raw/kardec/complementares/`; 3 já ingeridas (O Que é o Espiritismo, Obras Póstumas, Viagem Espírita); faltam Instruções Práticas, Resumo da Lei dos Fenômenos Espíritas, Espiritismo em Sua Mais Simples Expressão
- [ ] **Expandir autores nível 3** — Léon Denis avançado (4 obras ingeridas), Chico Xavier parcial (A Caminho da Luz ingerido); faltam O Consolador, Nosso Lar, Cairbar Schutel, Martins Peralva, Eurípedes Barsanulfo
- [x] **Corrigir coautoria mediúnica em `wiki/obras/evolucao-em-dois-mundos.md`** (1958) — lista apenas Chico Xavier em `fontes:`, mas é coautoria com Waldo Vieira (mesma parceria de *Sexo e Destino*, corrigida em 2026-05-03 — ver `log.md`). Atualizar `fontes:` para `[André Luiz/Chico Xavier+Waldo Vieira]`, dados bibliográficos e seção Fontes; cruzar com a página nova [[wiki/personalidades/waldo-vieira]].
- [ ] **Ingerir Novo Testamento restante** — 19/27 livros ingeridos: Evangelhos, Atos, Romanos, 1/2-Coríntios, Gálatas, Efésios, Filipenses, Colossenses, **1-Tessalonicenses** (ingerida 2026-05-04 — fonte apostólica do livre exame em 5:21), Hebreus, Tiago, 1/2-Pedro, 1-João, Apocalipse. Faltam 8 (todos baixa prioridade — Kardec cita pouco ou nada):
  - **Paulinas remanescentes** — 2-Tessalonicenses, 1/2-Timóteo, Tito, Filemom. Pastorais (1/2-Tim, Tito) e Filemom têm pouquíssima tração doutrinária no Pentateuco; 2 Ts entra só pontualmente
  - **Cartas gerais remanescentes** — 2/3-João, Judas. Curtas, citadas raramente; 1-João e 2-Pedro já ingeridos cobrem o essencial joânico/petrino
- [x] **Expandir personalidades-âncora** — stubs (<105 palavras) reescritos: Chico Xavier (88→~700), Espíritos Reveladores (103→~1170, agora cobre lista completa dos signatários dos Prolegômenos, Espírito de Verdade como Cristo no ESE cap. VI, e o critério de universalidade), Carlos Mendonça (61→~715, com método EELDE e três palestras associadas), Joseph Bré (97→~710, com a distinção honestidade-perante-homens vs perante-Deus), Eric Stanislas (104→~780, com a doutrina da reunião séria como santuário e expiação-vira-serviço)
- [ ] **Pipeline de palestras** — consolidar workflow YouTube → transcrição → summary → ingest; hoje funciona mas é manual demais
- [x] **Pre-flight check em `/ingest` Passo 0** (2026-05-04) — Passo 0 da skill renomeado para "Pre-flight e pré-checagem de escopo" e ganhou dois sub-passos materiais antes da classificação doutrinária: (1) `test -e raw/<caminho>` com sugestão via `find raw -iname '*<chave>*'` quando ausente; (2) `git rev-parse --abbrev-ref HEAD` + `git rev-list --count HEAD..main` (comparação local, sem `fetch`) — se a branch não for `main` e estiver atrás, PARE e sugerir rebase/merge. Custo ~30s; cobre os dois modos de falha registrados no report de uso (raw inexistente na worktree, worktree atrás de main mascarando arquivos).

---

## 2. Experiência do leitor público

A wiki já é publicada, mas foi pensada para uso pessoal. Adaptar para que qualquer estudante sério consiga navegar e aprender.

- [x] **Página de boas-vindas** — substituir o index do Quartz por uma landing page com: propósito da wiki, como navegar, hierarquia de autoridade, aviso de que é work-in-progress
- [x] **Home orientada por affordances** — `index.md` reescrito como grid de cartões (Chegando agora, ESDE, Palestras, Leitura livre, Consulta rápida); catálogo linear removido em favor do Explorer + Search do Quartz
- [~] **Trilhas de estudo guiadas** — stubs criados em `wiki/trilhas/` (primeiros-passos, esde, palestras, leitura-livre) como destinos dos cartões da home. Expandir cada trilha com sequência comentada, leituras complementares e aferição de progresso ainda é TODO. Considerar também "As Leis Morais em ordem" e "Mediunidade: do básico ao avançado"
- [~] **Glossário navegável** — stub em `wiki/sinteses/glossario.md` com ~15 conceitos-raiz (Deus, Espírito, alma, perispírito, reencarnação, mediunidade, obsessão, prece, caridade, fluido cósmico, escala espírita, expiação, livre-arbítrio, anjos, transição planetária). Popular com os ~126 conceitos restantes, ordenados alfabeticamente com uma linha por termo, é TODO
- [ ] **Expandir affordances da home** — considerar 6ª/7ª entrada (ex.: "Divergências" para leitores curiosos, "Personalidades" para quem estuda mediunidade e C&I) conforme a wiki crescer. Manter 5 hoje para não sobrecarregar
- [~] **Melhorar tags e filtragem** — três novos namespaces controlados (`grau/*` 3 valores, `tema/*` 12 valores, `autor/*` 16 valores) somam-se a `obra/*` e `lei/*`. Conjuntos canônicos documentados em `.claude/rules/convencoes-tags.md`. Lint estendido (`check_tag_taxonomy` cobre todos os 5; novo `check_tag_coverage` info-level marca páginas sem `tema/*`). `scripts/enrich_tags_autor.py` (backfill via `fontes:` + tags livres canônicas, 342 páginas) e `scripts/enrich_tags_grau.py` (default por `tipo:`, 299 páginas) idempotentes. `/ingest` instrui aplicar todos os namespaces em páginas novas. **Faltando:** passada manual de `tema/*` nas 345 páginas listadas pelo `tag_coverage` (lint info dirige o trabalho).
- [ ] **Revisar e melhorar tags `tema/`** — auditar o conjunto canônico de 12 valores (`.claude/rules/convencoes-tags.md`) à luz da cobertura atual: identificar temas sub-representados, sobrepostos ou ausentes; reavaliar granularidade (ex.: separar `mediunidade` de `obsessao`, ou agrupar). Em seguida, revisar páginas já tagueadas em massa (commit `5629049`) para corrigir falsos positivos do backfill automático e completar páginas com `tema/` único quando justifiquem múltiplos.
- [ ] **Breadcrumbs semânticos** — revisar estrutura de pastas para que os breadcrumbs do Quartz façam sentido para o leitor (Conceitos > Leis Morais > Lei de Causa e Efeito)
- [ ] **Canal de feedback do leitor** — definir rota explícita para errata e dúvidas: link "Sugerir correção" no rodapé do Quartz apontando para issue template no GitHub, ou e-mail dedicado. Hoje a wiki está pública sem caminho óbvio para o leitor reportar erro doutrinário ou typo.

---

## 3. Conteúdo de síntese e estudo

As categorias `questoes/` e `sinteses/` estão sub-representadas. São as mais valiosas para o leitor.

- [ ] **Extrair questões-chave do Pentateuco** — selecionar as questões mais importantes de cada obra e criar páginas em `questoes/` com pergunta, resposta dos Espíritos, comentário de Kardec e análise
- [x] **Completar páginas das 10 Leis Morais** (2026-04-30) — todas as 10 leis acima de 600 palavras com cobertura das subseções principais do capítulo do LE, aplicação prática e cruzamentos pertinentes. Trabalho/Adoração/Reprodução/Sociedade já haviam sido expandidos antes do roadmap ser atualizado (698–995 palavras); nesta rodada foram tratados os 4 stubs reais: Conservação (276→838), Liberdade (341→1195), Progresso (377→1172) e Igualdade (448→1276). Numeração corrigida (Conservação é a 4ª, Progresso a 7ª, Igualdade a 8ª, Liberdade a 9ª — o LE numera dentro da Parte 3, não da sequência geral)
- [ ] **Sínteses temáticas** — criar comparativos entre obras sobre o mesmo tema (ex: "O que cada obra diz sobre obsessão", "Reencarnação: de Kardec a Léon Denis")
- [x] **Enriquecer `wiki/aprofundamentos/sexualidade-em-andre-luiz.md`** com material de *Sexo e Destino* (1963) (concluído 2026-05-04) — novo eixo "7. *Sexo e Destino* (1963)" cobrindo tese ativa (sexo construtor de destino, cena Almas Irmãs), possessão partilhada (Parte 1, cap. 8) e dignidade de homossexuais e intersexos (Parte 2, cap. 5). Síntese passa de 6 para 7 eixos cronológicos (1945→1963).
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
- [ ] **Decisão sobre `wiki/biblia/`** — pré-requisito do item acima. ACF integral já está em `raw/biblia-acf/` (excluído do build). Decidir: (a) publicar como `wiki/biblia/<livro>/<capitulo>.md` para link interno completo, (b) manter externo e linkar para Bíblia online, (c) híbrido — publicar só os livros já tratados em `wiki/obras/biblia/` (Mateus, Marcos, Lucas, João, Atos) e externos para o resto. Afeta tamanho da wiki publicada, ruído no grafo do Quartz e o output do `link_citations.py`.

---

## 5. Qualidade e automação

Hoje o lint roda sob demanda. Automatizar para manter a qualidade conforme a wiki cresce.

- [x] **Lint em CI** — `lint_wiki.py` roda no GitHub Actions (`deploy-wiki.yml`) em cada push
- [x] **Métricas de cobertura** — `stats_wiki.py` agora gera: % do Pentateuco citado por obra (LE 215/1019 = 21%, ESE 28/28, Gênese 10/18, LM 24/33, C&I 18/18), cobertura do LE por bloco de 100 questões, wikilinks quebrados com freq ≥ 5, razão conceitos/questões e sugestões automáticas priorizadas (blocos LE sub-cobertos, razão distorcida, targets candidatos a nova página). Fase 2 — detectar conceitos mencionados em texto fluido sem wikilink — fica para quando a fase 1 exibir gaps
- [ ] **Validação de deploy** — checar se o build do Quartz não quebrou links internos após cada deploy
- [x] **Lint evolutivo** — três novos checks em `lint_wiki.py`: `low_citations` (páginas doutrinárias com corpo ≥ 200 palavras e <2 citações reconhecidas; surfou 4 parábolas de stub), `frequent_missing_concepts` (conceitos linkados em 5+ páginas distintas mas sem página própria; warning-level isolado a partir de `missing_concept_pages` agora agregado por count) e `naming_consistency` (variantes de mesma raiz em tags por case/diacrítico ou par plural/singular ambos circulando; surfou `perispirito`/`perispírito`, `parabola`/`parabolas` etc.)
- [x] **Higiene do script de estatísticas** — meta-páginas (`tipo: sintese` + tag `meta`) excluídas de grafo, vocabulário e tamanho; seções-template (`## Fontes`, `## Páginas relacionadas`, `## Páginas referenciadas`, `## Conceitos relacionados`) removidas antes da tokenização. Top bigramas agora refletem doutrina ("mundo espiritual", "ensino kardec", "aplicação prática") em vez de aparato bibliográfico
- [ ] **Backup e portabilidade** — `qmd` mantém índice SQLite local, `raw/` tem 700+ docs (boa parte fruto de OCR/transcrição manual), `data/kardec-mapping.json` e hooks só existem no laptop. git cobre `raw/`, `wiki/` e scripts; falta plano para o que está fora do git (índice qmd é regerável, mas custa tempo) e checklist de "subir tudo do zero em outra máquina".
- [x] **Testes do `scripts/link_citations.py`** (2026-05-01) — `tests/test_link_citations.py` (25 casos, `unittest` puro, sem nova dependência) cobre: code block fenced/inline, link Markdown e wikilink existentes, heading, sigla ambígua (Léon Denis vs LE), range composto (`LE q. 150-152` → primeira), Pentateuco completo (intro+item, intro só, capítulo, capítulo com parte, normalização Gênese), Revista Espírita (mês casado, fallback de ano, separador "de", ano desconhecido) e complementares (slug exato, strip de artigo, obra inexistente). Roda em CI no `deploy-wiki.yml` logo após o lint, antes do build.
- [ ] **Aliases canônicos para personalidades e obras** — política explícita de nomenclatura: forma canônica preferencial (ex.: "Allan Kardec" não "Rivail", "Chico Xavier" não "Francisco Cândido", "Léon Denis" não "Denis"); aliases registrados em frontmatter (`aliases: [...]`); check de lint que avisa quando uma página usa nome não-canônico de personalidade/obra existente. Reduz drift conforme a wiki cresce.
- [ ] **Uniformizar nomenclatura dos tipos de mundos habitados** — Kardec classifica em *A Gênese* cap. III (mundos primitivos, de provas e expiações, regeneradores, ditosos/felizes, celestes/divinos), mas a wiki mistura formas variantes ("mundo de prova" vs "mundos de provas e expiações", "mundos felizes" vs "ditosos", "inferiores"/"superiores" como atalhos). Revisar páginas que tratam do tema, fixar forma canônica para cada categoria, atualizar links e considerar aliases.
- [ ] **Baseline de performance do build** — registrar tempo atual do build do Quartz (~207 páginas) e do `link_citations.py` em CI; alertar se regredir além de threshold (ex.: +50% sobre baseline). Hoje não dói; o ponto é instalar o velocímetro antes que doa, porque se o build ficar lento de repente vai ser difícil bissectar.
- [x] **Skill `/ship` para o ciclo commit→land** (2026-05-04) — `.claude/skills/ship/SKILL.md` empacota: (1) inventário via `git status`/`diff`/`log main..HEAD` e classificação do estado (commitado / pendente / vazio), (2) commit por unidade lógica com mensagem proposta em PT-BR e stage seletivo (sem `git add -A`), (3) invocação de `scripts/land-to-main.sh`, (4) em conflito refaz `git rebase main` manualmente aplicando o protocolo de `convencoes-merge.md` por tipo de arquivo, (5) lint determinístico (`uv run python .claude/skills/lint/scripts/lint_wiki.py`) — **não** invoca a skill `/lint`. Pré-requisito (rule `convencoes-merge.md`) escrito junto.
- [x] **Hook `PostToolUse` para lint leve por arquivo** (2026-05-04) — `lint_wiki.py` ganhou flag `--file <path>` (função `lint_single_file()` que reusa o `CHECK_REGISTRY` sobre uma página e filtra items pelo path da fonte; subset `SINGLE_FILE_CHECKS` cobre 11 checks isoláveis: frontmatter, fontes_missing, citation_format, broken_links, low_citations, rascunho_stale, divergencias_aberta, tag_taxonomy, tag_coverage, direitos_obras, quote_proportion). `.claude/hooks/lint-on-edit.py` registrado em `Edit|Write|MultiEdit`, gateado a `wiki/**/*.md`, importa `lint_single_file` direto (evita 2º `uv run`); surfa só error+warning via `hookSpecificOutput.additionalContext` (info fica para o `/lint` global). Latência medida: ~50ms script puro, ~70ms ponta-a-ponta com uv startup. Decidido reusar `lint_wiki.py` em vez de novo script: roadmap explicita o pré-requisito e replicar parser de frontmatter, taxonomia de tags e regex de citação garantiria drift conforme novos checks evoluem.
- [x] **Rule `convencoes-merge.md`** (2026-05-04) — criada em `.claude/rules/convencoes-merge.md` (paths: `wiki/personalidades/**`, `log.md`, `wiki/sinteses/catalogo.md`) cobrindo (a) tabela dos drivers de `.gitattributes` (`merge=union` em log/catalogo/ROADMAP, `merge=ours` em estatisticas-da-wiki) com nota sobre `rerere.enabled=true`, (b) protocolo de união cronológica em páginas de personalidade (preservar ambos os lados, ordenar por data, deduplicar, costurar prosa), (c) `uv run python .claude/skills/lint/scripts/lint_wiki.py` antes de `git add` + `git rebase --continue`.
- [ ] **`/autolint` com cap de iterações e gate humano** — slash command que executa loop `scripts/lint_wiki.py (script determinístico) → categorizar findings → corrigir os de baixo risco (broken_links com target único óbvio, frontmatter mal-formatado) → re-lint`, até zero findings ou 3 iterações, **pausando para o usuário** quando o finding exige julgamento (link com múltiplos candidatos, divergência doutrinária implícita). Loop usa o script Python determinístico para detectar e re-validar; LLM atua só na fase de correção. Versão atenuada do "self-healing lint loop" do report (2026-05-04) — fully-autonomous viola humano-no-circuito.

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

## 8. Governança e direitos autorais

A wiki é publicada no GitHub Pages e `LICENSE-CONTENT.md` cobre apenas o conteúdo curado em `wiki/` (CC BY-NC-SA 4.0). Falta política explícita sobre o que **citamos de terceiros** — sobretudo psicografias e obras vivas do nível 3 ainda protegidas por direitos autorais. Kardec (m. 1869) e Léon Denis (m. 1927) estão em domínio público; Chico Xavier, Emmanuel, André Luiz, Bezerra de Menezes (publicações via FEB), Divaldo Franco, Joanna de Ângelis e Hammed **não** estão. A wiki é pública e cita esses autores.

- [x] **Política de citação para nível 3 protegido** (2026-04-27) — `CLAUDE.md` §3 documenta limites operacionais (até 400 palavras / 25% / 3 questões consecutivas, paráfrase quando exceder). Não é doc jurídico de fair-use; é guia editorial. Detentores conhecidos tabulados em `.claude/rules/convencoes-direitos.md`. Lint `check_quote_proportion` (info) marca páginas que excedem.
- [x] **Aviso ao leitor em obras protegidas** (2026-04-27) — `scripts/inject_copyright.py` injeta callout `> [!note] Direitos autorais` no topo de cada `wiki/obras/<slug>.md` com `direitos.detentor != dominio-publico` durante o build (mesmo padrão de `link_citations.py`, sobre `/tmp/quartz/content`). Nota perene em `index.md` cobre o leitor que entra pela home. URL de aquisição (`url_aquisicao`) renderizada como link no callout quando presente.
- [x] **Frontmatter `direitos:` em obras nível 3** (2026-04-27) — schema aninhado (`detentor`, `ano_dp_estimado`, `url_aquisicao`, `observacao`) documentado em `.claude/rules/convencoes-direitos.md`. Backfill via `scripts/backfill_direitos.py` populou as 32 obras: 23 `dominio-publico`, 4 FEB (Chico Xavier), 1 Boa-Nova (Hammed), 5 `desconhecido` (palestras). Lint `check_direitos_obras` verifica conjunto canônico (error em detentor inválido, info em ausente). Parser de frontmatter em `_lib/wiki_utils.py` foi expandido para aceitar dicts aninhados sem nova dependência.
- [x] **Status de `raw/` no Quartz** (2026-04-27) — `quartz.config.ts` já excluía `raw/` (`ignorePatterns`); a decisão e o motivo foram documentados em `CLAUDE.md` §4 ("Build público — escopo"). Lint `check_raw_excluded` (error) trava regressão.
- [ ] **Auditoria de conteúdo gerado por LLM** — `/ingest`, `/slides` e `/stats` produzem texto que entra na wiki. Para uma base que se quer citável, distinguir "Kardec disse X (LE q. 150)" de "síntese gerada a partir de X" é tema de credibilidade, não só de processo. Opções: campo `revisao_humana:` (data) no frontmatter de páginas geradas, marcação visível em rodapé ("Síntese revisada por humano em YYYY-MM-DD"), ou seção `## Notas` em sínteses que cite explicitamente quando há paráfrase vs citação direta. Decidir o nível mínimo aceitável. **Adiada para fase 2** — `/ingest` já tem humano-no-circuito explícito e `/stats` já marca origem em prosa; ganho marginal hoje é baixo.

---

## 9. Eficiência de tokens no workflow

A wiki cresce e cada conversa com o Claude Code consome mais tokens. Auditoria (2026-05-02) identificou três focos principais: leitura de `raw/` inteiros em `/ingest`, rules grandes injetadas em todo Edit, e queries `qmd` sem limites. Itens abaixo reduzem custo sem comprometer Kardec ou a qualidade das páginas — qualidade é inegociável; o que se otimiza é o caminho até ela.

- [x] **Disciplina nas queries `qmd`** (2026-05-02) — defaults `limit: 5` e `minScore: 0.5` injetados em `/ingest` (Passo 2) e `/slides` (preâmbulo do Passo 3) na prosa que o modelo lê ao executar a skill; `.claude/rules/busca-qmd.md` enriquecido com seção "Defaults de triagem" (limit/minScore/collections explícito) e "Abrir o documento depois" (preferir `mcp__qmd__get` com offset a `Read` integral em raw/ > 1000 linhas). Bug menor corrigido no rule: `collection` (singular, fora do schema) → `collections=["wiki"]` (array). `/glossario` ficou de fora — usa `sugerir_termos.py` (Python determinístico), não `mcp__qmd__query`.
- [x] **Granularizar `convencoes-paginas.md`** (2026-05-02) — quebrado em três: `convencoes-frontmatter.md` (paths: `wiki/**`, núcleo: frontmatter + links/slugs + estrutura por tipo), `convencoes-tags.md` (paths: `wiki/**`, taxonomia completa dos 5 namespaces) e `convencoes-direitos.md` (paths: `wiki/obras/**`, schema `direitos:` + tabela de detentores + limites de citação). Edições em `wiki/**` fora de `wiki/obras/` (conceitos, sínteses, questões, aprofundamentos, personalidades, divergências, trilhas) deixam de carregar ~2.6 KB de bloco de direitos por turno (medido via hook: 12.524 chars vs 15.178 em `wiki/obras/`). Referências atualizadas em `CLAUDE.md`, `.claude/skills/ingest/SKILL.md`, `find_feb_url.py`, `enrich_tags_grau.py`.
- [x] **Fragmentar Revista Espírita em `raw/`** — partição mensal (commits `35e04b6` + `bdeec27`): cada ano virou 12 arquivos `<ano>/<mes>-<nome>.md` (340-2141 linhas, mediana ~900). Reduz substancialmente o overhead em `/ingest` e melhora score do `qmd` vs. ano monolítico. Per-artigo (150-300 linhas) descartado: bloqueado por falta de marcadores claros de início de artigo dentro de cada mês, e o `mcp__qmd__get` com offset já dá granularidade suficiente — ganho marginal não compensa o custo de parser dedicado.
- [x] **Haiku para triagem em `/lint` e `/glossario`** (2026-05-02) — `lint/SKILL.md` Passo 3 e `glossario/SKILL.md` Passo 2 agora delegam a subagente com `model: "haiku"` (Explore para o lint, general-purpose para o glossário). Input é compacto e estruturado; output é classificação. Exceções documentadas (sessão já em Haiku ou volume de input baixo → fica no main para evitar overhead de spin-up). `/stats` continua 100% Python — sem LLM no loop.
- [x] **Pré-resumo de obras monolíticas** (2026-05-02) — três obras nível 1 do Pentateuco (LM 11.9K linhas, Gênese 11.1K, ESE 5.5K) ganharam dois artefatos adjacentes: `<obra>.index.md` (índice estrutural determinístico — capítulos, range de linhas, primeira sentença — gerado por `scripts/generate_obra_index.py`) e `<obra>.resumo.md` (~500 palavras: propósito, escopo, aportes, quando recorrer — gerado uma vez por subagente Haiku). Os 6 arquivos somam 245 linhas para representar 28K linhas de obras (~115× redução). `.claude/rules/busca-qmd.md` ganhou seção "Pré-resumos para obras monolíticas" instruindo a ler `.index.md` antes de abrir o monolítico — o range vira `mcp__qmd__get <obra>.md:<inicio>-<fim>`. Léon Denis "Problema do Ser" (16K linhas, `-old`) é versão obsoleta — já tem contraparte particionada e fica fora.

Itens descartados desta lista por impacto baixo ou não-aplicável: hábito de RTK (já intercepta automaticamente; só monitorar), validação explícita de prompt caching (Claude Code já cacheia system+CLAUDE.md por 5min; sem ação se está funcionando), `references/` carregado sob demanda nas skills (SKILL.md hoje 45-117 linhas — não é prioridade até passar de 200).

---

## Priorização para o workflow autor + Claude Code

Itens ranqueados pelo impacto na qualidade e velocidade de construção da wiki (ingest, queries, sínteses), com uma categoria à parte para **risco/robustez** — onde o custo de mitigar é baixo e o custo de não mitigar pode ser alto.

### Concluído

- **§0 Higiene das skills e doc** (2026-04-26) — bugs em CLAUDE.md/skills, plan mode em auto mode, regra de psicografia, deduplicação de citação, etc.
- **qmd como MCP server local (§6)** — busca semântica local (BM25 + vetorial) sobre 920 docs (`raw` + `wiki`). Já é a base de `/ingest` e queries.
- **§8 Governança e direitos autorais — pacote 1** (2026-04-27) — política de citação operacional (CLAUDE.md §3), aviso ao leitor via transformer Python (`inject_copyright.py`) + nota em landing, frontmatter `direitos:` populado nas 32 obras, exclusão de `raw/` documentada. Auditoria de LLM (§8.5) fica para fase 2.

### Impacto alto — muda o jogo

1. **Métricas de cobertura (§5)** — Saber o que falta é tão valioso quanto saber o que existe. Reportar conceitos mencionados em 5+ páginas sem página própria, % do Pentateuco coberto, razão conceitos/questões — dá lista de trabalho priorizada em vez de depender de intuição.
2. **Lint evolutivo (§5)** — Checks de conteúdo (páginas com poucas citações, nomenclatura inconsistente, aliases) mantêm qualidade conforme a wiki cresce. Hoje isso depende de o Claude Code "perceber" problemas durante ingest.

### Risco e robustez — custo baixo de mitigar, alto de não mitigar

3. ~~**Política de fair-use para nível 3 protegido (§8)**~~ — concluído em 2026-04-27 (ver bloco "Concluído" acima).
4. ~~**Testes do `scripts/link_citations.py` (§5)**~~ — concluído em 2026-05-01 (25 casos em `tests/`, rodando em CI).
5. **Backup do que está fora do git (§5)** — `raw/`, `wiki/` e scripts já estão no git; índice qmd e estado local de hooks não. Regerar qmd do zero custa horas, não dias — então é mais documentação de checklist do que infraestrutura de backup. Vale fazer enquanto a memória do setup é fresca.

### Impacto médio — acelera o que já funciona

6. **Pipeline de palestras (§1)** — Automatizar YouTube → transcrição → MD reduz fricção significativa; cada palestra hoje exige vários passos manuais antes do ingest.
7. **Lint em CI (§5)** — Rede de segurança útil, mas já rodamos `/lint` manualmente; ganho incremental.
8. **Auditoria de conteúdo gerado por LLM (§8)** — Importância cresce com o tempo. Hoje a wiki é pessoal-pública; em 12-24 meses, se for citada por terceiros, transparência sobre paráfrase vs citação importa muito mais. Implementação simples (campo de frontmatter); o trabalho é definir a política.
9. **Eficiência de tokens — eixo §9** — concluído (2026-05-04): disciplina em queries `qmd`, granularização de `convencoes-paginas.md`, partição mensal da Revista Espírita, Haiku para `/lint` e `/glossario`, pré-resumo de obras monolíticas (LM/Gênese/ESE). Custo composto: ganho pequeno por turno, alto somado em meses de uso. Per-artigo da Revista Espírita descartado — partição mensal + `qmd get` com offset já cobrem o overhead.

### Decisões arquiteturais a destravar

- **Decisão sobre `wiki/biblia/` (§4.2)** — Bloqueia "linkar referências bíblicas" e dá casa estrutural ao NT que está sendo ingerido em §1. Não é trabalho grande; é uma escolha (publicar tudo, nada, ou só o ingerido) que precisa ser tomada antes de §4.2 avançar.

### Impacto menor para o workflow (alto para o leitor)

- **Trilhas de estudo, glossário, Pagefind, breadcrumbs** — ótimos para o leitor público, mas não mudam como o conteúdo é construído.
- **Canal de feedback do leitor (§2)** — Não muda workflow, mas é o caminho para erratas e diálogo com a comunidade. Custo: issue template no GH + link no rodapé do Quartz.

---

## Princípios

- **Kardec prevalece** — toda melhoria respeita a hierarquia de autoridade (seção 2 do CLAUDE.md)
- **Citação obrigatória** — nenhum conteúdo novo sem fundamentação (seção 4)
- **Humano no circuito** — ingest e sínteses passam pelo usuário antes de serem publicados
- **Incremental** — cada melhoria entrega valor isoladamente; não há dependência rígida entre eixos

---

## Estado-alvo (definition of done por eixo)

O roadmap é uma lista aberta. Para evitar deriva e saber quando um eixo "já entregou o suficiente, foco em outro", esboçar critérios mínimos. Não é compromisso de prazo — é critério de fechamento.

- **§1 Cobertura** — Pentateuco com cobertura conceitual ≥80% medida pelo `/stats`; cada autor de nível 3 com ao menos uma obra-âncora ingerida; nenhuma personalidade-âncora citada em 5+ páginas como stub.
- **§2 Leitor público** — todas as 5 affordances da home com trilha completa (não stub); glossário ≥100 termos; canal de feedback explícito.
- **§3 Síntese** — 10 leis morais como página completa; ≥30 questões-chave do Pentateuco extraídas; ≥5 sínteses temáticas comparativas.
- **§4 Cross-references** — todas as parábolas linkam conceitos morais que ilustram (e vice-versa); nenhuma página em `wiki/divergencias/` órfã do conceito que diverge.
- **§5 Automação** — lint em CI verde por 30 dias consecutivos; baseline de build com alerta de regressão; testes do `link_citations.py` cobrindo casos-canto ✓ (2026-05-01).
- **§8 Governança** — política de fair-use escrita ✓; nenhuma obra protegida sem campo `direitos:` ✓; aviso ao leitor visível em todas as obras nível 3 protegidas ✓. Resta `revisao_humana:` (§8.5) quando a wiki for citada por terceiros.

Revisar a cada trimestre — alvo móvel é melhor que alvo nenhum.
