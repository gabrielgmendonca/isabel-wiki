# Roadmap — IsAbel Wiki Espírita

> Estratégia e pendências abertas, organizadas por eixo (não por cronologia). Itens **concluídos** saem do corpo e viram uma linha no apêndice [Concluído](#concluído) — o detalhe vive no git e, quando é lição que precisa sobreviver, numa rule ou memória.
> **Números operacionais vêm de script** (o comando fica ao lado) e não são congelados aqui: medição velha no ROADMAP envelhece em silêncio.
> A numeração das seções é estável — código, testes e skills referenciam `§5`, `§10.3`, `§11`, `§12`.
> Última revisão: 2026-10-10.

---

## Prioridades

1. **★ Repensar o fechamento do §11** (§5) — a tentativa de julho (`/preparo`) foi abandonada por pouco prática; o §11 segue com 117 itens abertos que só o Gabriel fecha. É o gargalo do projeto.
2. **Promover os gates de aspas** (§12) — o backlog foi a zero em 2026-10-10; sem gate, aspa escrita de memória volta a entrar. Barato: é só severidade + hook.
3. **Check de intervalo de questões que atravessa capítulo do LE** (§5) — camada 0; fecha a classe do `q. 873-919`.
4. **Medir a taxa de diferimento da `/critica`** (§5) — pré-requisito para voltar a rodá-la em escala.
5. **Questões-chave dos blocos sub-cobertos do LE** (§3) — o maior buraco de conteúdo.

---

## 1. Cobertura de fontes

### 1.1 Obras a ingerir

Esta seção é **estratégia** (qual autor priorizar e por quê). O estado factual vive fora daqui:
- **Fila de ingestão** (obra em `raw/` sem página em `wiki/obras/`) → `uv run python scripts/list_pending_ingest.py`.
- **Fila de aquisição** (obra ainda não em `raw/`) → `tracking/` (FEB, CEAK, triagem de direitos).

Pentateuco, Kardec complementar e Novo Testamento estão fechados. Ordem de prioridade do que falta:

- [ ] **Nível 3 sem obra-âncora, com raw disponível** — **Gabriel Delanne** (discípulo direto de Kardec; vários títulos em `.doc`, converter antes) e **Cairbar Schutel** (raw via CEAK). Definition of done: ≥1 obra-âncora por autor.
- [ ] **Nível 3 sem obra-âncora e sem raw** — **Martins Peralva** e **Eurípedes Barsanulfo**: pastas vazias; o gargalo é aquisição, não ingest.
- [ ] **Nível 3 parciais** — André Luiz (títulos restantes da série) e Yvonne Pereira.
- [~] **Pesquisa psíquica — Flammarion**: falta 1 obra; as páginas já ingeridas precedem a classificação de "pesquisa psíquica" (CLAUDE.md §2) — inserir a ressalva de que não têm autoridade doutrinária.
- [ ] **Pesquisa psíquica — Bozzano**: ~54 títulos; definir 1–3 prioritários antes de qualquer ingest (fenomenologia metapsíquica, frequentemente neutra quanto à reencarnação).

### 1.2 Curadoria de páginas existentes

Frente contínua, sem itens fixos: entra o que o `/lint` ou a `/critica` apontarem (stub, drift).

### 1.3 Pipeline e processos

- [ ] **Áudio e vídeo → wiki num caminho só** — hoje há dois pipelines que funcionam isolados: `/yt`/`/yt-bulk` (legenda do YouTube + resumo) e a transcrição local de áudio antigo (`mlx-whisper` large-v3, usada no Pinga-Fogo, com revisão em camadas e cobertura medida por código). Consolidar em (fonte) → transcrição → revisão → `/ingest`, e reduzir a curadoria manual entre `raw/palestras/` e a wiki.
- [ ] **Manifest de progresso em lotes longos** — JSON de itens concluídos, checado no início, para retomar conversão de catálogo / ingest multi-livro após limite de uso ou timeout.

---

## 2. Experiência do leitor público

- [~] **Trilhas de estudo** — as trilhas da home estão preenchidas. Falta: trilhas extras ("As Leis Morais em ordem", "Mediunidade: do básico ao avançado").
- [~] **Glossário navegável** — `wiki/sinteses/glossario.md` ainda curto; meta ≥100 termos, uma linha cada.
- [~] **Tags `tema/*`** — taxonomia e lint prontos (`check_tag_taxonomy`, `check_tag_coverage`). Falta: auditar os 12 valores canônicos (sobreposição, granularidade — ex.: `mediunidade` × `obsessao`) e revisar os falsos positivos da marcação em massa (commit `5629049`).
- [~] **Acessibilidade para leitores de tela** — landmarks `<nav>/<main>/<aside>` no SSR já entregues (`quartz-overrides/components/renderPage.tsx`). Falta: (a) validar com VoiceOver/NVDA reais; (b) alt text nos embeds do YouTube + `check_alt_text`; (c) callouts sem `role`; (d) `aria-live` nos botões `A+`/`A−`. Um skip-link via JS foi tentado e descartado em mai/2026 — com o `<main>` real no SSR, pode ser revisitado.
- [ ] **Título da aba/OG/busca/breadcrumb ainda vem do slug** — o override `ArticleTitle.tsx` corrigiu só o `<h1>` visível. Fix completo: transformer que preencha `title:` a partir do H1 na origem.
- [ ] **Notas de rodapé do Pentateuco publicado** — os marcadores `[[1]](#_ftnref1)` herdados do raw renderizam como wikilink quebrado em `wiki/pentateuco/**`. Limpar só na apresentação, sem alterar o texto doutrinário.

---

## 3. Conteúdo de síntese e estudo

`questoes/` e `sinteses/` são as categorias mais valiosas para o leitor e as menos povoadas.

- [ ] **Questões-chave dos blocos sub-cobertos do LE** — cobertura atual: `/stats` (42,9% em jul/2026). Na última medição por bloco (mai/2026) os piores eram **301–400** (intervenção dos Espíritos), **501–600** (retorno à vida corporal) e **401–500** (retorno à vida espiritual). Remedir antes de escolher.
- [ ] **Capítulos do LM e da Gênese sem ancoragem** — levantar por script (regex de citação × `kardec-mapping.json`).
- [ ] **Aprofundamentos dos conceitos centrais** — candidatos por PageRank e massa de vocabulário: `progresso-espiritual`, `livre-arbitrio`, `perispirito`, `caridade`, `atributos-de-deus` (LE Parte 1 + ESE I–III), `lugar-do-homem-na-criacao` (LE q. 132–144, Gênese XI), `morte-corporal-e-passagem` (LE q. 154–165, C&I 1ª parte III).
- [ ] **Sínteses panorâmicas** — `cristo-na-doutrina` (Guia, Modelo e Governador da Terra: ESE, Gênese XV, C&I) e `serie-andre-luiz` (arco dos 16 livros, ordem de leitura).
- [ ] **Sínteses comparativas e quadros** — o mesmo tema através das obras (ex.: "Obsessão de Kardec a Philomeno de Miranda").
- [ ] **Perguntas frequentes** — dúvidas comuns de estudantes, respondidas e citadas.
- [ ] **Palestras entregues voltam para a wiki** — cada palestra preparada (`/palestra` → `/slides`) produz casos, recortes e aprofundamentos que hoje ficam no dossiê. Definir o passo de devolução (o que vira página, o que vira caso em página existente).

---

## 4. Cross-references enriquecidas

- [ ] **Parábolas ↔ conceitos morais**, **leis morais ↔ exemplos** (parábolas, questões, casos), **personalidades de C&I ↔ conceitos**, **obras ↔ obras** que se citam.
- [ ] **Hub pages por tema** (ex.: Mediunidade) agregando conceitos, personalidades, obras e questões.
- [ ] **Tração inversa do cluster epistolar** — as epístolas dominam o grau de saída mas não o de entrada: o conceito tratado numa epístola (caridade em 1 Cor 13, fé viva em Tiago 2) cita a epístola?
- [ ] **Índices dos livros do NT** (`wiki/biblia/<livro>/index.md`) — ainda stubs de ~40–70 palavras. Ordem: 4 Evangelhos → Atos e Apocalipse → epístolas. Esquema em `convencoes-frontmatter.md`.
- [ ] **Auto-link de Kardec complementar** — estender o mapping a RE, OPE, OQE e Viagem Espírita em 1862.

---

## 5. Qualidade e automação

### Princípio das 3 camadas (fixado 2026-07-14)

| Camada | Quem | Quando | Custo |
|---|---|---|---|
| **0 — código** | `lint_wiki.py` | CI, **todo push** | grátis, instantâneo, é gate |
| **1 — LLM** | `/critica` · `/autocritica` | em lotes, com teto | caro |
| **2 — humano** | Gabriel | fila do §11 | **o recurso mais escasso do projeto** |

**A regra:** todo achado é **produzido** pela camada mais barata capaz de produzi-lo e **consumido** pela camada mais barata capaz de resolvê-lo. O modo de falha é o trabalho vazar para baixo — achado que nasce na camada errada e desce até o humano. Ao propor automação nova, a primeira pergunta é: *isto é decidível por código?* Se for, é lint, não prompt.

### ★ Fechar o §11 sem transformar o Gabriel em revisor de fila

- [ ] **Repensar o mecanismo** (reaberto 2026-10-09). O diagnóstico de julho segue válido: o loop **colhe** decisões (o `/dreno` promove o que tem `[x]`), mas a **semeadura** — decidir cada item — é toda humana, e é ela que trava. A resposta de julho foi o `/preparo`: dossiê HTML com evidência lado a lado, consertos redigidos pela LLM, `quote_guard` rebaixando páginas automaticamente. **Foi abandonado** (worktree descartada em 2026-10-09): ~2.000 linhas de máquina para continuar entregando ~100 decisões item a item, e a contenção automática *aumentava* a fila (+56 itens). Lição: melhorar a ergonomia da fila não resolve; o que resolve é ter **menos decisões**. Direções a avaliar:
  - **Decidir por classe, não por item.** Boa parte do §11 cabe em poucas regras editoriais. Ex.: os ~14 itens "estrutura fora do template" se resolvem com **uma** decisão (o template é guia, não norma → fechar todos; ou é norma → vira lint). Os ~40 "paráfrase entre aspas" se resolvem por política (desaspar mantendo o locus, sem revisão por item). Uma decisão sua fecha dezenas.
  - **Resolver quando a página é tocada, não em sessão de fila.** Um hook (como o `inject-rules`) mostra os itens abertos do §11 ao editar a página; o conserto acontece quando a página já está aberta por um motivo real (palestra, ingest, revisão). Páginas que ninguém toca podem esperar.
  - **Tirar o §11 do ROADMAP.** Mais de 100 linhas por página não são estratégia. Um arquivo de dados (`data/diferidos.json` ou campo no frontmatter da página) elimina o parse frágil de markdown (offsets, slugs ambíguos) e permite que o `/dreno` e o lint o consumam direto.
  - **Fechar a torneira.** Não rodar a `/critica` em escala enquanto a taxa de diferimento não for medida (item abaixo).

### Itens

- [ ] **Check de intervalo de questões que atravessa capítulo do LE** — `q. 873-919` é citado como locus da Lei de Justiça, Amor e Caridade (cap. XI = q. 873–892), mas engole o cap. XII (q. 893–919, Da perfeição moral). Já está em `convencoes-tags.md` e em ~27 linhas de 13 arquivos. **Cuidado:** os usos de q. 893–919 para conteúdo do cap. XII estão **corretos**. Três partes: (1) corrigir a rule para `q. 873-892 (cap. XI)`, com nota de que o cap. XII recebe a tag por extensão temática; (2) corrigir as ocorrências que apresentam 873-919 como locus do cap. XI; (3) check **data-driven** derivado do `.index.md` do LE (nada hardcoded). Diagnóstico: `reports/post-mortem/2026-07-12-sessao-logoterapia.md`.
- [~] **Taxa de diferimento da `/critica`** — era 92% (110 de 120 páginas viravam rascunho + item no §11). Conserto aplicado em 2026-07-14: o eixo 4 saiu da crítica e virou lint, e o prompt deixou de ter "na dúvida, difira". **Falta medir:** rodar um lote pequeno e comparar. Classificar os itens "sem eixo" do §11 (formato antigo `cit/edit/tag`) é pré-requisito para a comparação valer.
- [ ] **Tirar do prompt da `/critica` o resíduo determinístico do eixo 3** — Fontes, frontmatter, formato de citação, nomes canônicos e terminologia já são lint. Auditar o que o agente ainda deriva disso e cortar do prompt; sobra para a LLM só tom e enquadramento.
- [ ] **Triagem barata antes do Opus** — o `critica_scope.py` ordena as páginas devidas sem sinal de suspeita (varredura alfabética). Usar os achados do lint (grátis) + um agente barato como pré-filtro, e só o suspeito sobe ao Opus.
- [ ] **Conserto manual devolve a página à fila cara** — resolver um item do §11 à mão muda o corpo → `content_sha` diverge → a página volta à fila da `/critica` como `corpo-alterado`. Avaliar `record --touch` que revalide sem Opus quando o diff for pequeno.
- [ ] **Loop diário: decidir o destino** — `scripts/loop-diario.sh` existe mas **não está instalado** (sem plist em `~/Library/LaunchAgents`, sem logs). A auditoria de 2026-07-14 achou defeitos ainda não corrigidos: PR duplicado por dia enquanto o anterior não é mesclado; falha indistinguível de ociosidade (sem notificação nem heartbeat); `set -e` matando o script sem log; `worktree prune`/`fetch --prune` ausentes; branch nomeada só pela data; trava com TOCTOU. Se o loop for religado, corrigir tudo antes; depois do ★ acima, decidir se ele ainda tem trabalho (hoje o nível 0 tem 0 promovíveis por construção, e o nível 1 só revisa rascunho do `/ingest`). Invariantes do dreno/loop: `.claude/rules/dreno-loop-invariantes.md`.
- [ ] **Dreno: baldes D e X não drenam** — D = a crítica diferiu sem item no §11 (rastro perdido); X = corpo alterado depois da crítica (veredito obsoleto). Hoje 1 de cada (`dreno.py anatomia`). Definir dono: D → humano confere; X → volta à fila da `/critica`.
- [ ] **Dreno: o prompt do nível 1 refaz o que o código já fez** — `dreno.py completude()` já checa Fontes e citações antes de chamar o agente. Estreitar o prompt para o que é semântico ("nada visivelmente incompleto", tom).
- [ ] **Versão estrita do check de citação** — o trecho citado **sustenta** a afirmação? (A existência da aspa já é determinística, §12.) A sustentação semântica segue com a `/critica` (eixo 2); as âncoras por questão/item em `wiki/pentateuco/` (entregues em jun/2026) eram a dependência apontada para uma versão por código — reavaliar se ela é viável.
- [ ] **Varredura de "cosmologia / cosmológic*"** — termo estranho ao registro doutrinário. Levantar ocorrências e, se houver volume, entrar como vocabulário em `data/terminologia.json` (check data-driven), não como check avulso.
- [ ] **Lint do pipeline pós-transform** — os transforms de CI (`link_citations.py`, `wrap_glossary_terms.py`, `inject_copyright.py`) podem injetar link quebrado sem o lint ver. Aplicar os transforms numa cópia e relintar (`--include-pipeline`).
- [ ] **Validação de deploy e baseline de build** — checar links internos após o deploy; registrar o tempo do build do Quartz e do `link_citations.py` e alertar em regressão (ex.: +50%).
- [ ] **`/autolint`** — loop `lint → corrigir baixo risco → re-lint`, no máximo 3 iterações, pausando no que exige julgamento.
- [ ] **git-lfs em `raw/assets/`** — arquivos commitados como bytes crus em vez de ponteiros (`Encountered N files that should have been pointers`). Corrigir com `git lfs migrate import --include="raw/assets/*"` (reescreve histórico — combinar antes).

---

## 6. Busca e navegação avançada

- [ ] **Pagefind** — índice estático no build, no lugar ou ao lado do flexsearch do Quartz.
- [ ] **Índice por conceito-raiz** — hierárquico (Deus > Leis Divinas > Lei de Causa e Efeito > …).

---

## 7. Ferramentas de estudo e difusão

- [ ] **Colocação de imagem no deck (`/slides`)** — o sourcing já existe (estágio Iconografia do `/palestra` + `convencoes-imagens.md`); falta automatizar a colocação: ler `iconografia` do `dados.json` do dossiê, o humano escolhe o candidato por momento-chave, o script baixa para `slides/<slug>/assets/`, otimiza (`sips -Z 1800`; Wikimedia exige User-Agent), emite o `![bg right:43%]` e grava `creditos.json`. Padrões validados: layout dividido (nunca full-bleed atrás de texto), slides `.pergunta` sem imagem.
- [~] **Mapas conceituais (Mermaid)** — renderização validada, convenção em `convencoes-mermaid.md`. Falta: `check_mermaid_labels` (drift de nomenclatura em rótulo) e, se valer, derivação a partir do grafo do `/stats`.
- [ ] **Export temático** — PDF/EPUB de um conjunto de páginas sobre um tema.
- [ ] **Flashcards** — pares pergunta/resposta a partir de `questoes/` (compatível com Anki).

---

## 8. Governança e direitos autorais

Política de citação, aviso ao leitor, `direitos:` e exclusão de `raw/` do build estão entregues (ver [Concluído](#concluído)).

- [ ] **Marcar conteúdo revisado por humano** (`revisao_humana:` com data, ou nota no rodapé) — distinguir "Kardec disse X" de "síntese gerada" importa se a wiki passar a ser citada por terceiros. **Gatilho para retomar:** primeira citação externa conhecida, ou abertura pública da wiki para além do uso pessoal.

---

## 9. Eficiência de tokens no workflow

A auditoria de 2026-05 foi entregue; em 2026-09 as rules passaram a ser injetadas uma vez por sessão (`inject-rules.py`) e as rules e o CLAUDE.md foram enxugados (~78 → 31 KB). Pendente:

- [ ] **Prompts do `palestra-dossie.js` (~60 KB)** — o custo é `rounds × contexto` por agente. **Medir antes de cortar** (quanto texto chega a cada agente, em quantos rounds); só então condensar o que se repete entre estágios.
- [~] **Corpo das skills** — enxugadas em 2026-10 (commit `16243d8`). Conferir o que sobrou acima de ~10 KB (`ingest`, `palestra`, `slides`) e seguir uma skill por fatia, sem mexer nas `description:`.

---

## 10. Backlog operacional

Os números deste eixo saem de script; aqui fica só o que não tem outro lugar.

### 10.3 Esboços a escrever

Rascunhos do `/ingest` que precisam de **escrita**, não de promoção — o `/dreno` não os toca e os anota aqui (`dreno.py triagem` dá a lista do dia; `dreno.py anatomia` dá os baldes).

- **Personalidades**: `gregorio`, `druso`, `silas`, `ernesto-fantini`, `alexandre`, `aniceto`, `jeronimo-assistente`.
- **Obras**: `acao-e-reacao`, `os-mensageiros`, `missionarios-da-luz`.

---

## 11. Crítica profunda — itens diferidos a decisão humana

> Achados da `/critica` que exigem julgamento (não auto-corrigíveis). Só itens **abertos** ficam aqui: ao marcar `[x]`, o `/dreno` promove a página, e o item é arquivado na revisão seguinte do ROADMAP. Relatórios: `reports/critica/<data>/`. Formato antigo (lote 2026-06-03): eixos `cit`/`edit`/`tag`; formato novo: `eixo N`.
>
> **Não remover os loci LE q. 1009 e q. 1015–1019** — são as questões finais legítimas do LE (Kardec saltou o nº 1011); itens que os acusam de inexistentes são falso-positivo, e o resíduo real é só aspa estilizada como literal.
>
> Como reduzir esta fila: ver o ★ do §5 (decidir por classe, resolver ao tocar a página).

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
- [ ] **continuidade-do-principio-inteligente-ate-o-homem** (edit; 1) — classificação "não é divergência estrutural, é adoção de um dos dois sistemas".
- [ ] **condenacao-dos-incredulos-em-marcos-16** (cit,tag; 2) — paráfrase de LE q. 621 ("lei inscrita em todo coração").
- [ ] **morte-de-ananias-e-safira** (edit,tag; 2) — enquadramento crítico-textual (Formgeschichte) co-igual à divergência doutrinária.
- [ ] **sinais-de-marcos-16** (cit,tag; 3) — "novas línguas" atribuída a LM cap. XIX vs cap. XVI item 189.

### questoes/
- [ ] **paternidade-como-missao** (cit; 3) — aspa "A semente mais fecunda é o exemplo" (ESE cap. XIV item 9).
- [ ] **por-que-a-acao-dos-espiritos-e-oculta** (cit; 4) — aspa "o mérito está na luta" (LE q. 843).
- [ ] **arrependimento-expiacao-e-reparacao** (cit; 1) — blockquotes "literais" divergem da tradução FEB citada em Fontes.
- [ ] **o-que-devemos-pedir-na-prece** (edit; 1) — prece "pode verbalizar o desejo concreto" vs ESE cap. XXVII item 22.
- [ ] **a-infancia-e-o-veu-da-inocencia** (edit; 1) — ênfase "sobretudo" atribuída a Kardec (q. 385).
- [ ] **unicidade-do-espirito** (tag; 1) — "individualidade" como termo central sem conceito (≠ `individuacao`). · NOTA 2026-06-17: sem alvo (individualidade não existe, ≠ individuacao); requer criar página ou decidir não-linkar — diferido.
- [ ] **alma-dos-animais** (cit,tag; 2) — "crueldade contra animais ofende Deus" (LE q. 750, q. 752).
- [ ] **espiritos-e-as-leis-da-natureza** (cit,edit; 2) — "morte tem momento fixado" simplifica demais q. 853.
- [ ] **o-que-e-deus** (cit,tag; 3) — "sete atributos clássicos listados na q. 13".

### sinteses/
- [ ] **veracidade-das-mensagens-psicografadas** (cit,edit; 2) — atribuição do "Controle Universal do Ensino dos Espíritos".
- [ ] **parabolas-de-jesus** (cit,edit; 3) — tesouro escondido/pérola atribuída a ESE cap. XVI.
- [ ] **lar-como-fortaleza** (cit,tag; 2) — aspa ESE cap. XXVII item 9 (vs cap. XXVIII item 5).
- [ ] **possessos-de-morzine** (cit; 1) — três graus "estabelecidos com clareza programática" pelo artigo dez/1862.
- [ ] **serie-psicologica-joanna-de-angelis** (cit; 1) — "(LE q. 540)" como locus do "princípio inteligente".
- [ ] **sermao-do-monte-em-emmanuel** (edit; 1) — "Quatro capítulos a articular" mas lista sete.
- [ ] **oracoes-do-canal-espiritualidade-e-vida** (edit; 1) — "Catálogo (18 peças)" mas 1ª entrada é palestra, não oração.
- [ ] **sermao-do-monte** (cit; 2) — ESE cap. XVII item 3 vs cap. XV item 3.

### conceitos/ (lotes de 2026-06-10)
- [ ] **wiki/conceitos/erraticidade** (eixo 2, 2026-06-10) — função 'auxiliar encarnados como protetor/guia' atribuída a (LE, q. 229), que trata da retenção das más paixões; locus real é q. 226 (missões) / q. 489 ss. (Espíritos protetores) · evidência: cite.py LE q. 229 (livro-dos-espiritos.md:984-985) · relatório: reports/critica/2026-06-10-0938
- [ ] **wiki/conceitos/erraticidade** (eixo 3, 2026-06-10) — faltam seções 'Desdobramentos' e 'Divergências' do template de conceito · evidência: convencoes-frontmatter.md · relatório: reports/critica/2026-06-10-0938
- [ ] **wiki/conceitos/evocacao** (eixo 2, 2026-06-10) — 'Qualquer Espírito acode' + frase entre aspas atribuída a (LM, item 272), que trata da dificuldade das evocações; item 282 (2ª-3ª) condiciona e lista Espíritos que NUNCA podem comunicar-se · evidência: cite.py LM item 272 vs 282 (livro-dos-mediuns.md:7868-8175) · relatório: reports/critica/2026-06-10-0938
- [ ] **wiki/conceitos/evocacao** (eixo 3, 2026-06-10) — faltam seções 'Desdobramentos' e 'Divergências' do template de conceito · evidência: convencoes-frontmatter.md · relatório: reports/critica/2026-06-10-0938
- [ ] **wiki/conceitos/homem-de-bem** (eixo 2, 2026-06-10) — fórmula 'A perfeição moral consiste em praticar a lei de justiça, amor e caridade...' atribuída a (LE, q. 893), que trata da virtude mais meritória; a fórmula é da q. 918 · evidência: cite.py LE q. 893 vs q. 918 · relatório: reports/critica/2026-06-10-0938
- [ ] **wiki/conceitos/homem-de-bem** (eixo 3, 2026-06-10) — paráfrases de (ESE, cap. XVII, item 3) apresentadas entre aspas como literais (linhas 21,25,27,29); locus correto, mas converter para literal ou de-quote · evidência: cite.py ESE cap. XVII item 3 · relatório: reports/critica/2026-06-10-0938
- [ ] **wiki/conceitos/ligacao-espirito-corpo** (eixo 2, 2026-06-10) — afirma rompimento 'mais abrupto na morte violenta' (LE q. 155-162), INVERTENDO Kardec: na morte violenta o desligamento é mais LENTO e os laços mais tenazes (q. 162 nota, q. 165) · evidência: cite.py LE q. 162/165 · relatório: reports/critica/2026-06-10-0938
- [ ] **wiki/conceitos/ligacao-espirito-corpo** (eixo 2, 2026-06-10) — emancipação da alma em sono/êxtase citada com (LM, 2ª parte, cap. VI), que trata de manifestações visuais; locus real é LE q. 400-455 (Da emancipação da alma) · evidência: cite.py LM 2ª parte cap. VI vs LE q. 400-455 · relatório: reports/critica/2026-06-10-0938
- [ ] **wiki/conceitos/mundos-regeneradores** (eixo 2, 2026-06-10) — blockquote linha 23 (item 17) 'doenças/sofrimentos já são passado' INVERTE Kardec ('ainda sujeito às vicissitudes... ainda tem de suportar provas') · evidência: cite.py ESE cap. III item 17 · relatório: reports/critica/2026-06-10-0949
- [ ] **wiki/conceitos/mundos-regeneradores** (eixo 2, 2026-06-10) — blockquote linha 27 (item 17) com frases inexistentes no ESE (grep zero): 'autoridade conquistada pela superioridade moral' etc. · evidência: cite.py ESE cap. III item 17 + grep · relatório: reports/critica/2026-06-10-0949
- [ ] **wiki/conceitos/mundos-regeneradores** (eixo 3, 2026-06-10) — desdobramento 'transição da Terra a mundo regenerador' atribuído a 'muitos espíritas' sem âncora citável; opcional ancorar em Gênese cap. XVIII · evidência: Gênese cap. XVIII · relatório: reports/critica/2026-06-10-0949
- [ ] **wiki/conceitos/parabola-da-candeia-sob-o-alqueire** (eixo 2, 2026-06-10) — 'Espiritismo é candeia / responsabilidade dos espíritas' atribuído ao item 2 (versículo Lc 8:16-17); está nos itens 7 e 10 · evidência: cite.py ESE cap. XXIV itens 2,7,10 · relatório: reports/critica/2026-06-10-0949
- [ ] **wiki/conceitos/parabola-da-candeia-sob-o-alqueire** (eixo 3, 2026-06-10) — blockquote linha 17 (Mt 5:15) usa 'velador' vs. 'candeeiro' da tradução Guillon/FEB (fonte declarada) · evidência: ESE cap. XXIV item 1 · relatório: reports/critica/2026-06-10-0949
- [ ] **wiki/conceitos/parabola-da-candeia-sob-o-alqueire** (eixo 3, 2026-06-10) — blockquote linha 19 (Lc 8:16-17) com fraseado divergente da fonte ESE (Guillon/FEB) · evidência: ESE cap. XXIV item 2 · relatório: reports/critica/2026-06-10-0949
- [ ] **wiki/conceitos/parabola-da-casa-sobre-a-rocha** (eixo 3, 2026-06-10) — estrutura fora do template de conceito ('Texto da parábola' extra; faltam Desdobramentos/Divergências) · evidência: convencoes-frontmatter.md · relatório: reports/critica/2026-06-10-0949
- [ ] **wiki/conceitos/parabola-da-figueira-seca** (eixo 2, 2026-06-10) — 'A fé é a mãe da esperança e da caridade' entre aspas atribuída ao item 10 (que trata de médiuns); ideia é do item 11 mas não literal · evidência: cite.py ESE cap. XIX itens 10-11 · relatório: reports/critica/2026-06-10-0949
- [ ] **wiki/conceitos/parabola-da-figueira-seca** (eixo 2, 2026-06-10) — 'montanhas = dificuldades/obstáculos' creditado aos itens 9-10; está no item 2, e 'fé como alavanca' no item 12 · evidência: cite.py ESE cap. XIX itens 2,9,10,12 · relatório: reports/critica/2026-06-10-0949
- [ ] **wiki/conceitos/parabola-da-figueira-seca** (eixo 3, 2026-06-10) — conexão com parábola do semeador/festim de bodas apresentada como sendo de Kardec (item 9), mas é leitura do redator · evidência: cite.py ESE cap. XIX item 9 · relatório: reports/critica/2026-06-10-0949
- [ ] **wiki/conceitos/parabola-da-figueira-seca** (eixo 3, 2026-06-10) — estrutura fora do template de conceito ('Texto da parábola' extra; falta Desdobramentos) · evidência: convencoes-frontmatter.md · relatório: reports/critica/2026-06-10-0949
- [ ] **wiki/conceitos/parabola-dos-trabalhadores-da-ultima-hora** (eixo 3, 2026-06-10) — enquadramento 'recompensa proporcional ao esforço individual' (l.29) tensiona ESE cap. XX item 3 (últimos podem receber recompensa MAIOR por herdarem o labor dos predecessores); refinar · evidência: cite.py ESE cap. XX item 3 · relatório: reports/critica/2026-06-10-1001
- [ ] **wiki/conceitos/parabola-dos-trabalhadores-da-ultima-hora** (eixo 3, 2026-06-10) — estrutura fora do template ('Texto da parábola' extra; faltam Desdobramentos/Divergências) · evidência: convencoes-frontmatter.md · relatório: reports/critica/2026-06-10-1001
- [ ] **wiki/conceitos/penas-eternas** (eixo 3, 2026-06-10) — faltam 'Desdobramentos' e 'Divergências' do template (Divergências legitimamente ausente — página é a posição de Kardec) · evidência: convencoes-frontmatter.md · relatório: reports/critica/2026-06-10-1001
- [ ] **wiki/conceitos/perfeicao-moral** (eixo 2, 2026-06-10) — blockquote de (LE, q. 893) l.17 não-literal ('Toda virtude tem seu mérito próprio' vs. 'Todas as virtudes têm seu mérito'); conformar à edição FEB/Guillon · evidência: cite.py LE q. 893 · relatório: reports/critica/2026-06-10-1001
- [ ] **wiki/conceitos/perfeicao-moral** (eixo 2, 2026-06-10) — blockquote de (LE, q. 909) l.33 não-literal ('frequentemente, fazendo esforços muito insignificantes' vs. 'por vezes fazendo esforços bem pequenos') · evidência: cite.py LE q. 909 · relatório: reports/critica/2026-06-10-1001
- [ ] **wiki/conceitos/perfeicao-moral** (eixo 3, 2026-06-10) — estrutura temática própria, sem 'Aplicação prática' nem 'Divergências' do template de conceito · evidência: convencoes-frontmatter.md · relatório: reports/critica/2026-06-10-1001
- [ ] **wiki/conceitos/perturbacao** (eixo 2 / TOOLING — página CORRETA, não alterar, 2026-06-10) — cite.py não desambígua os dois 'cap. I' de C&I (1ª parte 'O futuro e o nada' vs. 2ª parte 'A passagem') e resolve sempre p/ a 1ª; as citações da página (2ª parte cap. I itens 4-15) batem com ceu-e-inferno.md:2295-2318. Risco: futuras auditorias 'corrigirem' loci corretos. Fix no resolve_locus de cite.py · evidência: ceu-e-inferno.md:2295-2318 · relatório: reports/critica/2026-06-10-1001
- [ ] **wiki/conceitos/principio-vital** (eixo 4, 2026-06-10) — prosa e tag pressupõem [[wiki/conceitos/fluido-vital]], que NÃO existe (data/terminologia.json registra o slug). Criar a página (distinção princípio vital vs. fluido vital — LE q. 70 comentário; Gênese cap. X item 19) ou remover o slug órfão · evidência: data/terminologia.json · relatório: reports/critica/2026-06-10-1017 · NOTA 2026-06-17: não há wikilink quebrado ("fluido vital" é prosa/tag livre, não [[link]]); requer decisão de criar página fluido-vital vs. manter tratado em principio-vital — diferido.
- [ ] **wiki/conceitos/proibicao-de-evocar-os-mortos** (eixo 3, 2026-06-10) — sem heading 'Definição'; seção 'Na Viagem Espírita em 1862' no lugar de Desdobramentos/Divergências · evidência: convencoes-frontmatter.md · relatório: reports/critica/2026-06-10-1017
- [ ] **wiki/conceitos/psicografia** (eixo 3, 2026-06-10) — 'Casos notáveis' no lugar de 'Desdobramentos'; avaliar realocar · evidência: convencoes-frontmatter.md · relatório: reports/critica/2026-06-10-1017
- [ ] **wiki/conceitos/raca-adamica** (eixo 2, 2026-06-10) — blockquote l.23 (RE mar/1860) abre com frase 'Para nós é evidente que as raças primitivas...' inexistente no artigo (grep zero); só a 2ª metade ('Adão... há 6000 anos') é verbatim · evidência: revista-espirita/1860/03-marco.md:141-162 · relatório: reports/critica/2026-06-10-1017
- [ ] **wiki/conceitos/raca-adamica** (eixo 2, 2026-06-10) — blockquote l.70 (A Caminho da Luz cap. 3) troca 'desolados' por 'angustiados' dentro de aspas · evidência: a-caminho-da-luz.md:120 · relatório: reports/critica/2026-06-10-1017
- [ ] **wiki/conceitos/raca-adamica** (eixo 3 / possível DIVERGÊNCIA, 2026-06-10) — 'Desenvolvimento por Emmanuel' (origem em Capela, raça adâmica = raças brancas) vai além de Kardec, que NÃO racializa a raça adâmica (Gênese cap. XI item 39); avaliar seção Divergências/callout (nível 3 vs. Pentateuco) · slug sugerido: raca-adamica-identificacao-capela-emmanuel · evidência: Gênese cap. XI item 39 (genese.md:5460-5477) · relatório: reports/critica/2026-06-10-1017
- [ ] **wiki/conceitos/resignacao** (eixo 2, 2026-06-10) — 'Bem-aventurados os aflitos, porque serão consolados' (Mt 5:4) mescla sujeito do ESE item 18 com predicado do item 1; fraseado composto inexistente · evidência: cite.py ESE cap. V itens 1,18 · relatório: reports/critica/2026-06-10-1037
- [ ] **wiki/conceitos/separacao-e-reencontro** (eixo 2, 2026-06-10) — blockquote 'Os que se amaram se reencontram após a morte e se reconhecem' atribuído a (LE, q. 274-276) (hierarquia); locus real é q. 285, e a frase não é literal nem lá · evidência: cite.py LE q. 274-276,285 · relatório: reports/critica/2026-06-10-1037
- [ ] **wiki/conceitos/separacao-e-reencontro** (eixo 2, 2026-06-10) — 'acompanhar/proteger como guia espiritual' ancorado em (LE, q. 284-285) (individualidade/reconhecimento); é doutrina dos Espíritos protetores (LE q. 489 ss.) · evidência: cite.py LE q. 284-285,489 · relatório: reports/critica/2026-06-10-1037
- [ ] **wiki/conceitos/separacao-e-reencontro** (eixo 2, 2026-06-10) — grupos por simpatia + inversão pai/filho citados como (LE, q. 274-278); grupos é q. 278 e a inversão de laços é q. 205; remover q.274-276 · evidência: cite.py LE q. 278,205 · relatório: reports/critica/2026-06-10-1037
- [ ] **wiki/conceitos/separacao-e-reencontro** (eixo 2, 2026-06-10) — 'reencarnar juntos para prosseguir relações anteriores' ancorado em (LE, q. 284-285); locus real é q. 205 · evidência: cite.py LE q. 284-285,205 · relatório: reports/critica/2026-06-10-1037
- [ ] **wiki/conceitos/separacao-e-reencontro** (eixo 3, 2026-06-10) — Fontes resume range como 'cap. VI, q. 274-285'; após corrigir loci, refletir cap. IV q. 205 + cap. VI q. 278,285 · evidência: cite.py · relatório: reports/critica/2026-06-10-1037
- [ ] **wiki/conceitos/vida-espirita** (eixo 3, 2026-06-10) — estrutura fora do template (headings próprios; faltam 'Ensino de Kardec', 'Desdobramentos', 'Aplicação prática', 'Divergências') · evidência: convencoes-frontmatter.md · relatório: reports/critica/2026-06-10-1037
- [ ] **wiki/conceitos/vida-futura** (eixo 2, 2026-06-10) — 'A vida futura é a vida normal do Espírito...' citado como literal de (ESE, cap. II, item 2); deriva alterado do cap. XXIII item 8 ('vida espiritual'/'existência terrestre', não 'vida futura'/'vida corpórea') · evidência: cite.py ESE cap. II item 2 vs cap. XXIII item 8 · relatório: reports/critica/2026-06-10-1037
- [ ] **wiki/conceitos/vida-futura** (eixo 2, 2026-06-10) — 'A vida corporal é necessária ao aperfeiçoamento... encarnação se reproduza' citado como literal de (ESE, cap. II, item 5); frase inexistente no ESE/LE (grep zero) · evidência: cite.py ESE cap. II item 5 + grep · relatório: reports/critica/2026-06-10-1037
- [ ] **wiki/conceitos/vida-futura** (eixo 2, 2026-06-10) — 'Aquele que se considera apenas viajante de passagem...' citado como literal de (ESE, cap. II, item 3); frase inexistente; tese está no item 5 com outra formulação · evidência: cite.py ESE cap. II itens 3,5 + grep · relatório: reports/critica/2026-06-10-1037
- [ ] **wiki/conceitos/evangelizacao-infantojuvenil** (eixo 2, 2026-06-10) — 'guiar os Espíritos que Deus lhes confiou para a vida terrestre' entre aspas como literal de (ESE, cap. XIV, item 9); ideia fiel mas frase não-literal (de-quote ou usar 'ponde todo o vosso amor em aproximar de Deus essa alma') · evidência: ESE cap. XIV item 9 (evangelho-segundo-o-espiritismo.md:2528-2567) · relatório: reports/critica/2026-06-10-1037
- [ ] **wiki/conceitos/harmonia-das-esferas** (eixo 3, 2026-06-10) — 'harpa cósmica' e 'degraus harmônicos' entre aspas são cunhagem da página, não literal de Léon Denis ('imensa harpa', '320 degraus ou ondas harmônicas'); de-quote ou citar literal · evidência: o-grande-enigma.md:587,651 · relatório: reports/critica/2026-06-10-1053
- [ ] **wiki/conceitos/morte** (eixo 2, 2026-06-10) — 'porta de entrada na vida, e não como a porta do nada' (C&I 1ª parte cap. II) — literal é 'a porta da vida' (sem 'de entrada'); 3 divergências da fonte · evidência: cite.py C&I cap. II item 7/10 · relatório: reports/critica/2026-06-10-1053
- [ ] **wiki/conceitos/morte** (eixo 3, 2026-06-10) — typo 'não se aprende diante da morte' → 'não se apreende' (cap. 'Da apreensão diante da morte'); inverte o sentido · evidência: C&I cap. II · relatório: reports/critica/2026-06-10-1053
- [ ] **wiki/conceitos/parabola-do-semeador** (eixo 2, 2026-06-10) — 'a condenação do egoísmo, da indiferença, do amor das riquezas e da vaidade' entre aspas atribuída a (ESE, cap. XVII, item 6); frase INEXISTENTE no ESE (grep zero) — citação fabricada · evidência: cite.py ESE cap. XVII item 6 + grep · relatório: reports/critica/2026-06-10-1053
- [ ] **wiki/conceitos/parabola-do-semeador** (eixo 3, 2026-06-10) — estrutura com seções extras ('Texto da parábola', 'Na palestra de Carlos Mendonça'); sem 'Desdobramentos' · evidência: convencoes-frontmatter.md · relatório: reports/critica/2026-06-10-1053
- [ ] **wiki/conceitos/potencias-da-alma** (eixo 2, 2026-06-10) — 'Querendo, o Espírito atua sobre a matéria...' entre aspas atribuída a (LE, q. 459), que trata da influência dos Espíritos nos pensamentos; tema é Gênese cap. XIV/RE jun/1868 · evidência: cite.py LE q. 459 · relatório: reports/critica/2026-06-10-1053
- [ ] **wiki/conceitos/potencias-da-alma** (eixo 2, 2026-06-10) — 'a vontade cresce com o adiantamento moral' atribuída a (LE, q. 635), que trata de posições sociais; candidato é q. 872 ('força moral') · evidência: cite.py LE q. 635,872 · relatório: reports/critica/2026-06-10-1053
- [ ] **wiki/conceitos/potencias-da-alma** (eixo 2, 2026-06-10) — 'a lei que Deus gravou no coração do homem' entre aspas como (LE, q. 621); q.621 diz só 'Na consciência'; a formulação é de Romanos 2:15/ESE · evidência: cite.py LE q. 621 · relatório: reports/critica/2026-06-10-1053
- [ ] **wiki/conceitos/progresso-espiritual** (eixo 2, 2026-06-10) — 'uns avançaram mais depressa no livre exercício da vontade' (LE, q. 115); q.115 atribui o avanço à aceitação submissa das provas; complementar com q. 119 · evidência: cite.py LE q. 115,119 · relatório: reports/critica/2026-06-10-1053
- [ ] **wiki/conceitos/progresso-espiritual** (eixo 3, 2026-06-10) — estrutura com cabeçalhos próprios; sem 'Ensino de Kardec'/'Aplicação prática'/'Divergências' · evidência: convencoes-frontmatter.md · relatório: reports/critica/2026-06-10-1053
- [ ] **wiki/conceitos/verdadeiro-espirita** (eixo 2, 2026-06-10) — 'dá de si mesmo o mais formal desmentido' atribuída a (ESE, cap. XV, item 10); a frase é do cap. XXI item 10 (falsos profetas da erraticidade), contexto diverso; reancorar em cap. XV item 10 ('verdadeiro espírita = verdadeiro cristão') · evidência: cite.py ESE cap. XV vs XXI item 10 · relatório: reports/critica/2026-06-10-1114
- [ ] **wiki/conceitos/verdadeiro-espirita** (eixo 2, 2026-06-10) — 'Fiz o bem que podia? Sacrifiquei algum interesse...' entre aspas como (LE, Conclusão, item III), que é polêmica contra materialismo; autoexame é q. 919, mas a frase não é literal nem lá · evidência: cite.py LE Conclusão item III, q. 919 · relatório: reports/critica/2026-06-10-1114
- [ ] **wiki/conceitos/parabola-da-dracma-perdida** (eixo 2 / CLUSTER Lucas 15, 2026-06-10) — afirma que Kardec trata as 3 parábolas de Lucas 15 no ESE cap. XI; Kardec NÃO comenta dracma/ovelha/pródigo no ESE (grep 'dracma' = 0); cap. XI é a lei de amor. Misattribuição replicada em parabola-da-ovelha-perdida e parabola-do-filho-prodigo (fora deste lote) — corrigir o cluster · evidência: cite.py ESE cap. XI + grep · relatório: reports/critica/2026-06-10-1114
- [ ] **wiki/conceitos/parabola-da-ovelha-perdida** (eixo 2 / CLUSTER Lucas 15, 2026-06-10) — festejo pelo arrependido atribuído a (ESE, cap. XI, item 10), que é o ditado de Sanson ('Amai bastante para serdes amados'); locus real do bom Pastor/festejo é (LE, q. 1009) · evidência: cite.py ESE cap. XI item 10, LE q. 1009 · relatório: reports/critica/2026-06-10-1114
- [ ] **wiki/conceitos/parabola-da-ovelha-perdida** (eixo 2, 2026-06-10) — afirma que Kardec discute a parábola no cap. XVIII (cuidado com os 'pequeninos'); cap. XVIII é o festim de bodas; tema dos pequeninos (Mt 18) está no cap. VIII · evidência: cite.py ESE cap. XVIII · relatório: reports/critica/2026-06-10-1114
- [ ] **wiki/conceitos/parabola-da-ovelha-perdida** (eixo 3, 2026-06-10) — Fontes lista 'caps. XI, XVIII'; ajustar após corrigir os loci (remover cap. XVIII) · evidência: cite.py · relatório: reports/critica/2026-06-10-1114
- [ ] **wiki/conceitos/parabola-da-rede** (eixo 2 / CLUSTER joio-trigo, 2026-06-10) — 'Kardec a trata em paralelo à parábola do joio e do trigo (ESE, cap. XVIII)'; cap. XVIII é festim de bodas + casa sobre a rocha, NÃO o joio; triagem está em ESE cap. III item 13 + Gênese cap. XVIII (já citados). Mesmo erro em parabola-do-joio-e-do-trigo (cap. XVIII item 7, que é a casa sobre a rocha) — corrigir o par · evidência: cite.py ESE cap. XVIII · relatório: reports/critica/2026-06-10-1114
- [ ] **wiki/conceitos/parabola-da-rede** (eixo 2, 2026-06-10) — 'anjos ceifeiros' como organizadores da triagem com (C&I, 1ª parte) genérico; precisar o locus ou substituir (anjos = Espíritos adiantados é C&I 1ª parte cap. VIII item 13, mas não trata de 'ceifeiros') · evidência: cite.py C&I 1ª parte cap. VIII item 13 · relatório: reports/critica/2026-06-10-1114
- [ ] **wiki/conceitos/parabola-da-semente-que-cresce-por-si** (eixo 2 / CLUSTER mostarda, 2026-06-10) — autopropagação do Espiritismo atribuída a (ESE, cap. XVIII, item 2 — 'grão de mostarda e fermento'); cap. XVIII item 2 é o festim de bodas; ESE NÃO comenta mostarda/fermento; tese da autopropagação está na Introdução item VI. Mesmo erro em parabola-do-grao-de-mostarda (cap. XVIII item 5, que é a porta estreita) — corrigir o par · evidência: cite.py ESE cap. XVIII item 2 + grep + Introdução item VI · relatório: reports/critica/2026-06-10-1114
- [ ] **wiki/conceitos/parabola-das-dez-virgens** (eixo 2, 2026-06-10) — afirma que Kardec comenta a parábola no ESE cap. XVIII; esse cap. é o festim de bodas (Mt 22), NÃO as dez virgens — que só aparecem como alusão de passagem no cap. I item 10. Reenquadrar a leitura do azeite como síntese do estudante (LE q.132-134, ESE cap. III, Gênese cap. XVIII) · evidência: cite.py ESE cap. XVIII item 1 + grep · relatório: reports/critica/2026-06-10-1129
- [ ] **wiki/conceitos/parabola-do-bom-pastor** (eixo 2, 2026-06-10) — citação de OPE 'Estudo sobre a natureza do Cristo' aponta §VIII ('O Verbo se fez carne', Jo 1) para a glosa de Jo 10:30; locus real é §III; e a frase entre aspas ('fazia distinção... não disse: Eu sou o Pai') não é literal de Kardec (grep zero) · evidência: obras-postumas §III l.1515 · relatório: reports/critica/2026-06-10-1129
- [ ] **wiki/conceitos/parabola-do-bom-samaritano** (eixo 2, 2026-06-10) — blockquote 'Texto da parábola' (l.17,19) em tradução não-declarada (nem Guillon/ESE nem Almeida/wiki-bíblia); ranges de versículo corretos. Alinhar à tradução da ESE (Guillon, cap. XV item 2) · evidência: cite.py ESE cap. XV item 2 vs wiki/biblia/lucas/10 · relatório: reports/critica/2026-06-10-1129
- [ ] **wiki/conceitos/parabola-do-fariseu-e-do-publicano** (eixo 2, 2026-06-10) — TODAS as citações ao ESE no locus errado: ancora em cap. VII item 9 (inexistente), cap. X itens 7-8, cap. XXVIII; Kardec comenta a parábola no cap. XXVII itens 3-4 ('orai com humildade como o publicano'). Reancorar a página inteira · evidência: cite.py ESE cap. VII vs XXVII · relatório: reports/critica/2026-06-10-1129
- [ ] **wiki/conceitos/parabola-do-fariseu-e-do-publicano** (eixo 2, 2026-06-10) — Definição (l.13) diz 'Kardec comenta extensamente no capítulo VII'; cap. VII comenta a parábola das bodas (Lc 14), não a do publicano. Corrigir para cap. XXVII itens 3-4 · evidência: cite.py ESE cap. VII item 5 · relatório: reports/critica/2026-06-10-1129
- [ ] **wiki/conceitos/parabola-do-fariseu-e-do-publicano** (eixo 3, 2026-06-10) — heading 'Definição' (a convenção pede 'Definição curta' como conteúdo, não título literal — cosmético) · evidência: convencoes-frontmatter.md · relatório: reports/critica/2026-06-10-1129

## 12. Verificação determinística de aspas do Pentateuco

A wiki e `raw/kardec/pentateuco/` usam a mesma edição (Guillon Ribeiro/FEB): aspa genuína bate verbatim com o `cite.py`; aspa fabricada diverge muito. `reverse_locus.classify` separa os candidatos em **misattributed** (aspa existe, noutro locus), **fabricated**, **paraphrase** e **uncertain**. Prevenção na origem: `insert_quote.py` (aspa só da fonte, autoverificada) + rule `verificacao-citacao.md`. Estado dos gates: `check_citation_resolves` = `error`/CI; `check_quote_misattributed` = `warning` + hook (allowlist em `data/citacao-aspas-aceitas.json`); `check_literal_quote_exists` = `info`.

- [ ] **Promover os gates** — o backlog está em **0** desde 2026-10-10 (`check_literal_quote_exists` e `check_quote_misattributed` zerados), então a "baseline que só encolhe" já nasce vazia: `fabricated` pode ir direto a `warning` + hook de edição (como a `misattributed`) e ambas a `error`/CI depois de algumas semanas sem falso positivo. Manter `uncertain`/`paraphrase` como `info`.
- [ ] **Aspa com a citação ANTES** — o scan só casa `"aspa" (LOCUS)`. A forma `ESE cap. V item 12 ensina que "…"` e a aspa solta sem parêntese adjacente não são conferidas (vistas em `vazio-existencial`, `medo`, `egoismo` durante a triagem). Medir antes de decidir: é ponto cego do mesmo tamanho que o do wikilink?
- [ ] **Estender a loci que o `cite.py` não fragmenta** (Introdução/Conclusão por item); onde não resolve, abster.

**Limites:** cobre só o Pentateuco. Aspas de autores complementares seguem dependentes da LLM — aceitável, porque as mais sensíveis são as de Kardec.

---

## 13. Terminologia "kardequiano/a" → "de Kardec" ✅

Eixo fechado: `check_kardequiano` é `error`/CI gate, data-driven (`data/terminologia.json` → `derivados-de-kardec`). Em 2026-10-09 o mapa ganhou "kardequista(s)", que escapava do gate (12 ocorrências corrigidas no contexto).

---

## Princípios

- **Kardec prevalece** — toda melhoria respeita a hierarquia de autoridade (CLAUDE.md §2).
- **Citação obrigatória** — nenhum conteúdo novo sem fundamentação.
- **Humano no circuito** — ingest e sínteses passam pelo Gabriel antes de publicar; nada é mesclado automaticamente.
- **Camada mais barata** — o que é decidível por código vira lint (§5).
- **Incremental** — cada melhoria entrega valor sozinha; sem dependência rígida entre eixos.

---

## Estado-alvo (definition of done por eixo)

- **§1 Cobertura** — Pentateuco com cobertura conceitual ≥80% no `/stats`; cada autor de nível 3 com ≥1 obra-âncora.
- **§2 Leitor** — trilhas completas; glossário ≥100 termos; leitor de tela navegando por landmarks.
- **§3 Síntese** — ≥30 questões-chave do Pentateuco; ≥5 sínteses comparativas.
- **§4 Cross-references** — todas as parábolas linkam conceitos morais (e vice-versa); índices do NT fora do estado de stub.
- **§5 Automação** — lint em CI verde por 30 dias; baseline de build com alerta.
- **§8 Governança** — resta a marcação de revisão humana.
- **§11 Fila humana** — teto de ~30 itens abertos; nenhum item com mais de 90 dias.
- **§11/§12/§13 Fidelidade** — 0 aspas fabricadas atribuídas a Kardec; 0 loci inexistentes (já é gate); 0 formas proibidas (já é gate).

Revisar a cada trimestre.

---

## Concluído

> Uma linha por item. O detalhe vive no histórico do git.

**§0 — Higiene de skills e documentação**
- Auditoria CLAUDE.md + skills + rules + hook (2026-04-26).
- Instruções enxutas: rules injetadas 1× por sessão (`inject-rules.py`), CLAUDE.md e skills sem duplicação (2026-09/10).

**§1 — Cobertura de fontes**
- Pentateuco 5/5; Kardec complementar 6/6 (2026-06-02); Novo Testamento 27/27 (2026-05-18); Léon Denis 4/4 do raw.
- Série André Luiz 13/19 + conceitos e personalidades-âncora (2026-05-26); *Memórias de um Suicida* (2026-06-05); *Conduta Espírita* (2026-07).
- Pinga-Fogo I e II transcritos do áudio (mlx-whisper + revisão em 3 camadas) e ingeridos, com páginas por tema e índices (2026-09/10).
- Coautoria mediúnica em `evolucao-em-dois-mundos.md`; personalidades-âncora expandidas (>700 palavras).
- Pre-flight no `/ingest` (2026-05-04); hook PreToolUse de pre-flight de branch, `qmd get` com offset, rule `convencoes-shell.md` (2026-05-18→20); ergonomia da revisão humana no `/ingest` (2026-05-19).
- `yt-dlp[default]` + deno resolvem o 403 do YouTube (2026-09).

**§2 — Leitor público**
- Home por affordances; breadcrumbs semânticos + `index.md` nas pastas-raiz (2026-05-05); canal "Sugerir correção" + issue templates (2026-05-06).
- Landmarks `<nav>/<main>/<aside>` no SSR (2026-06-17).
- Aviso visual em páginas `status: rascunho` (`DraftNotice.tsx`, 2026-06-17).
- Título visível a partir do H1, sem `<h1>` duplicado (`ArticleTitle.tsx`, 2026-06-17).
- Trilhas da home preenchidas (2026-06-17).
- Home revisada: compromissos, acervo, destaques, leitura de citações (2026-10).

**§3 — Síntese e estudo**
- 10 Leis Morais como página completa (2026-04-30); `sexualidade-em-andre-luiz.md` com *Sexo e Destino* (2026-05-04).
- Aprofundamentos de palestra: anjos guardiães (LE 489-521), "Bem e mal sofrer" e "O mal e o remédio" (ESE V, 18-19), cap. 173 de *Pão Nosso* (2026-07/09).

**§4 — Cross-references**
- Bíblia: NT publicado em `wiki/biblia/` (287 capítulos + 27 índices), AT por link externo; `link_citations.py` linka referências bíblicas (2026-05-22).
- Kardecpedia: deep-link por questão/item (2026-06-05).
- Pentateuco publicado em `wiki/pentateuco/` com âncora por questão/item e link interno preferencial; round-trip byte a byte contra o `cite.py` (2026-06-05).

**§5 — Qualidade e automação**
- Lint em CI; métricas (`stats_wiki.py`); lint evolutivo; testes do `link_citations.py`; backup e portabilidade (`docs/migracao.md`).
- `check_citation_resolves` como `error`/CI gate (2026-06-05).
- Aliases canônicos + `check_canonical_names`; mundos habitados + `check_mundos_habitados_naming` (2026-05).
- Skill `/ship`; hooks PostToolUse de lint e de mirror para o Quartz; rule `convencoes-merge.md`.
- `/critica` (2026-05-31) e `/autocritica`; vocabulários em `data/terminologia.json`.
- `cite.py`: marcador em negrito do ESE, sombreamento de item (tabela decimal, ordinal, versículo, ordinal interno), "Conclusão, item N" e ordinal ASCII da Gênese (2026-06 → 2026-10-09).
- Eixo 4 da crítica virou lint: `check_unlinked_concept_mention` (TF-IDF; nunca dentro de citação literal) (2026-07-14).
- `/dreno` (promove o rascunho cujo diferido foi fechado; nunca bumpa `atualizado_em`; slug ambíguo nunca promove) e loop diário com entrega por PR; auto-merge do nível 0 removido por guarda que falhava aberto (2026-07-13/14).
- `/preparo` + `quote_guard` (dossiê de decisão e contenção automática de aspa fabricada) — **tentados e abandonados** (2026-07-14→17); 9 consertos de citação e 2 do `cite.py` foram salvos em 2026-10-09.

**§6 — Busca**
- qmd como MCP server local (BM25 + vetorial + re-ranking).

**§7 — Ferramentas**
- `/slides` (Marp, padrão socrático Q&A, PPTX+PDF); `/palestra` + workflow `palestra-dossie` com estágio Iconografia (2026-06-15).
- Preview do tema (`slides/themes/preview.md`) + `check_slide_overflow` calibrado contra o PDF (2026-07-27).
- Descartado: identidade visual dos slides num design system externo (não renderiza PPTX/PDF, quebra o offline, tira o deck do markdown versionado).

**§8 — Governança**
- Política de citação para nível 3 + `check_quote_proportion`; aviso ao leitor (`inject_copyright.py`); `direitos:` + `check_direitos_obras`; `raw/` fora do build + `check_raw_excluded` (2026-04-27).

**§9 — Eficiência de tokens**
- Disciplina nas queries `qmd`; rules condicionais; Revista Espírita particionada; Haiku na triagem do `/lint` e do `/glossario`; `.index.md` + `.resumo.md` das obras monolíticas (2026-05-02).

**§11 — Crítica profunda**
- Lote 2026-05-31: 28/28 resolvidos (2026-06-02).
- Itens `[x]` dos lotes de jun/2026 arquivados (2026-10-09) — as páginas correspondentes já tinham sido promovidas pelo `/dreno`.

**§12 — Aspas**
- Índice reverso `reverse_locus.py` + classificação (2026-06-15); 25 mal-atribuições corrigidas no mesmo dia.
- `check_quote_misattributed` como `warning` + hook; `insert_quote.py` (2026-06-17).
- Triagem das 128 aspas inline (2026-07-04).
- Scan de blockquotes + 6 mal-atribuições corrigidas (2026-07-13).
- Fase 3 fechada: 86 aspas que não batiam com a fonte trocadas pelo literal (ou reancoradas, ou desaspadas) em 49 páginas — backlog 75 → 0; scan passa a ver sigla em wikilink; `cite.py` resolve subperguntas "N.a." do LM e a "Nota sobre esta nova edição" do LE (2026-10-10).

**§13 — Terminologia**
- "kardequiano/a" → "de Kardec": 688 → 0 + `check_kardequiano` como gate (2026-06-07); "kardequista" adicionado (2026-10-09).
