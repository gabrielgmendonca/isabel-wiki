---
name: slides
description: Gera apresentação Marp (PPTX + PDF) a partir de uma página da wiki IsAbel, no padrão socrático Q&A das palestras de Gabriel. Use com /slides <página-wiki>, "gerar slides de X", "fazer deck para palestra sobre X".
---

# /slides

Gatilhos: `/slides <página>` · "fazer slides de X" · "deck para palestra sobre X"

Convenções obrigatórias: ler `.claude/rules/convencoes-slides.md` (estrutura e densidade) e `.claude/rules/convencoes-perguntas-socraticas.md` (critérios A/B/C para perguntas-ponte) antes de propor outline.

## Premissa

O tema da palestra sempre vem de um conjunto de **questões do LE** ou **itens do ESE** (ou outra obra do Pentateuco) referenciados na página wiki. Identifique obra-base e range no frontmatter (`fontes: [LE]`) e nas citações do corpo — isso vai para a capa.

## Fase de planejamento

Ao iniciar, **apresente o outline em texto e aguarde confirmação do usuário antes de qualquer escrita**. Em plan mode, isso é o próprio `EnterPlanMode`; em auto mode, é uma pausa explícita pedindo aprovação. Nada em `slides/` pode ser escrito antes da aprovação.

### Passo 1 — Validar input

Confirmar que o argumento é uma página existente em `wiki/`. Se vier só um tema (ex: `/slides livre-arbítrio`), procurar em `wiki/conceitos/`, `wiki/sinteses/`, `wiki/aprofundamentos/`, `wiki/questoes/`. Se ambíguo, perguntar.

### Passo 2 — Coletar metadados da palestra

Duas chamadas `AskUserQuestion` (limite é 4 perguntas por chamada). Não prosseguir sem todos os campos respondidos.

**Chamada 1 — Logística** (3 perguntas):
- **Data da palestra** (YYYY-MM-DD) — obrigatória, nunca usar a data atual. Oferecer 2-3 datas-âncora (próximo sábado, próximo domingo) + "Other" para data explícita.
- **Casa espírita** (opcional, ex: "Centro Espírita Allan Kardec") — valor cru vai direto no footer, sem prefixo. Oferecer casas recentes do histórico de `slides/` + "Sem casa" + "Other".
- **Duração** — 30 / 45 / 60 / 90 min. Afeta quantidade de partes temáticas e profundidade de cada Q&A. Default sugerido: 60 min.

**Chamada 2 — Formato** (3 perguntas):
- **Perfil da audiência** — iniciantes / estudantes regulares / evangelizadores / misto. Muda densidade de citação, necessidade de glosa e tom didático.
- **Ângulo da palestra** — **Didático** (explica do zero, ideal para iniciantes; mais glosa e exemplos) / **Problematização** (questiona uma leitura corrente mal compreendida do tema — ex.: "Espiritismo não é religião?", "evangelizar é doutrinar?"; abre com a tese a contestar) / **Q&A puro** (segue as questões do LE/ESE sem desvio; plateia acompanha o texto). Calibra a postura editorial do outline e do deck final.
- **Interação com a plateia** — sem / pergunta retórica entre partes / slide explícito de discussão. Estrutural: o scaffold insere o slide correspondente.

### Passo 3 — Buscar material via qmd

Queries read-only em `raw/` e `wiki/` para montar o outline com conteúdo real, não placeholders. Defaults: `mcp__qmd__query` com `limit: 5`, `minScore: 0.5`, `intent` sempre presente, `collections` explícito. Para abrir trechos longos em seguida, `mcp__qmd__get` com offset (`file.md:100-300`) — nunca `Read` integral em arquivos `raw/` > 1000 linhas (Revista Espírita por ano, Livro dos Médiuns, etc.).

- **Pergunta + resposta literais do Kardec** (LE): query em collection `raw` pela pergunta e resposta dos Espíritos. Se a resposta >300 palavras, aplicar elipses `(...)` em trechos não-essenciais, mantendo núcleo doutrinário.
- **Citação integral** (ESE/LM/C&I): query em `raw` pela passagem referenciada.
- **"Para meditar"**: query em `wiki/sinteses/parabolas-de-jesus`, `wiki/personalidades/`, e `raw/` (Novo Testamento, C&I, André Luiz, Léon Denis, Chico Xavier) buscando ilustração pertinente ao tema. Selecionar 1-3 candidatos — apenas título + referência, nunca texto integral.

### Passo 4 — Propor outline ao usuário

**Gate de aprovação: nada em `slides/` pode ser escrito antes do usuário aprovar este outline.** Em plan mode, isso é o `EnterPlanMode`; em auto mode, é uma pausa explícita pedindo OK antes de invocar o scaffold do Passo 5.

Apresentar o deck completo em texto para crítica do usuário. O outline deve **refletir o ângulo escolhido no Passo 2**: uma palestra **Didática** puxa mais glosas e exemplos entre as citações; uma de **Problematização** abre com a tese corrente a contestar (não com pergunta neutra) e organiza as partes em torno do contraste; um **Q&A puro** segue a ordem das questões/itens da obra-base sem desvio, com mínimo de glosa.

- **Capa** (título, obra+range, data, casa)
- **Partes temáticas** com Q&A já preenchido (perguntas literais + trechos de resposta com elipses quando longas) — estrutura aberta a reordenação/corte pelo usuário no texto livre
- **Síntese final** (3-5 bullets rascunho)

Em paralelo, uma chamada `AskUserQuestion` com 3 perguntas para as escolhas discretas (cada uma com 2-4 opções):

- **Pergunta de abertura** — gerar 3 candidatos (5-15 palavras cada, retóricos, ângulos diferentes do tema). Usuário escolhe 1 ou pede outra via "Other".
- **Para meditar** — listar 2-4 candidatos selecionados no Passo 3 (parábola evangélica, caso de C&I, personalidade de André Luiz, página de `wiki/personalidades/`). Apenas título + referência, nunca texto integral.
- **Encerramento** — citação consolidadora (Jesus/Kardec/Pentateuco) / convite à ação (chamada prática à reforma íntima) / sem encerramento (síntese fecha a palestra).

Aguardar validação do outline em texto **e** respostas das 3 perguntas. Sem o "OK" explícito do usuário ao outline (e sem as 3 escolhas discretas resolvidas), não invocar o scaffold do Passo 5 — nenhum arquivo em `slides/` pode ser criado ou tocado antes disso. Em seguida, prosseguir para a fase de geração.

## Fase de geração (pós-aprovação)

### Passo 5 — Scaffold determinístico

```bash
uv run python .claude/skills/slides/scripts/scaffold_deck.py <caminho-wiki> \
  --date <YYYY-MM-DD> [--casa "<nome da casa>"] \
  --duracao <30|45|60|90> \
  --audiencia <iniciantes|regulares|evangelizadores|misto> \
  --interacao <sem|retorica|discussao> \
  [--out slides/<slug>/deck.md]
```

Os flags `--duracao`, `--audiencia`, `--interacao` vêm das respostas do Passo 2. Duração e audiência são metadados que o modelo usa para calibrar densidade no Passo 6; `interacao` é estrutural e altera o scaffold.

O script emite um esqueleto Marp com:

1. **Capa**: título + nome completo da obra com range (ex: `O Livro dos Espíritos · q. 674–685`) + autor + data + casa
2. **Abertura**: slide com TODO para pergunta socrática
3. **Partes** — cada seção `##` do wiki que contenha blockquotes vira uma parte, com section header `<!-- _class: section -->` de transição
4. **Q&A** — para citações LE, par pergunta+resposta; para outras obras, slide único de citação expandida
5. **Interação com plateia** (se `--interacao` != `sem`) — inserida antes de "Para meditar". `retorica` → 1 slide com TODO de pergunta retórica; `discussao` → section header "Pausa para conversa" + slide convidando comentários.
6. **Para meditar** — slide de parábola/caso/personalidade
7. **Síntese** — section header + slide de bullets
8. **Encerramento** — citação consolidadora opcional

TODOs a preencher ficam marcados como `*<!-- skill: ... -->*` em itálico.

### Passo 6 — Refinar o deck.md

Substituir todos os `<!-- skill: ... -->` com o conteúdo aprovado no Passo 4 e calibrar densidade pelos metadados do Passo 2:

- **Pergunta de abertura** — opção escolhida no AskUserQuestion do Passo 4
- **Perguntas e respostas literais do LE** (com elipses quando longas) — quantidade calibrada por `duracao` (30min ≈ 3-5 pares; 60min ≈ 8-12; 90min ≈ 12-15)
- **Glosa / explicação** — calibrada por `audiencia`: iniciantes pedem mais paráfrase em linguagem corrente, regulares aceitam citação seca, evangelizadores recebem ganchos para a prática de evangelização
- **Slide de interação** (se inserido pelo scaffold) — preencher a pergunta retórica ou o convite à plateia
- **Título + referência da parábola/caso/personalidade** escolhida no AskUserQuestion (sem texto integral)
- **Síntese** (3-5 bullets)
- **Encerramento** — conforme escolha do AskUserQuestion: preencher slide de citação consolidadora, substituir por slide de convite à ação, ou remover o slide

**Não inserir slides em branco** (`<!-- _class: blank -->`). Transições são feitas com `<!-- _class: section -->`.

### Passo 7 — Build PPTX + PDF

```bash
uv run python .claude/skills/slides/scripts/build_deck.py slides/<slug>/deck.md
```

Escreve em `slides/<slug>/build/`.

### Passo 8 — Reportar

- Caminho do `deck.md` (versionado)
- Caminhos de `build/deck.pptx` e `build/deck.pdf` (gitignored)
- Sugestão: abrir o PPTX no Keynote para ajustes finais

## Regras

- **Citação obrigatória** em toda afirmação doutrinária (CLAUDE.md §3). Sempre usar nome completo da obra, não sigla, nos slides.
- **Autoria de obras psicografadas**: ver CLAUDE.md §3 (formato `Autor espiritual / Médium`).
- **Texto integral da obra básica**: LE em dois passos (pergunta + resposta); ESE/LM/C&I em citação completa. Elipses `(...)` para trechos longos não-essenciais.
- **Sem slides em branco**: transições com section headers.
- **Hierarquia de autoridade** respeitada (CLAUDE.md §2): Pentateuco prevalece.
- **Não publicar na wiki**: `slides/` fica fora do build do Quartz.
- **Não tocar `wiki/`** durante a geração.
- **Plan mode bloqueia escrita** até o usuário aprovar o outline.
