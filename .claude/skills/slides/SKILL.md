---
name: slides
description: Gera apresentação Marp (PPTX + PDF) a partir de uma página da wiki IsAbel, no padrão socrático Q&A das palestras de Gabriel. Use com /slides <página-wiki>, "gerar slides de X", "fazer deck para palestra sobre X".
---

# /slides

Gatilhos: `/slides <página>` · "fazer slides de X" · "deck para palestra sobre X"

Convenções obrigatórias: ler `.claude/rules/convencoes-slides.md` antes de propor outline.

## Premissa

O tema da palestra sempre vem de um conjunto de **questões do LE** ou **itens do ESE** (ou outra obra do Pentateuco) referenciados na página wiki. Identifique obra-base e range no frontmatter (`fontes: [LE]`) e nas citações do corpo — isso vai para a capa.

## Fase de planejamento

Ao iniciar, **apresente o outline em texto e aguarde confirmação do usuário antes de qualquer escrita**. Em plan mode, isso é o próprio `EnterPlanMode`; em auto mode, é uma pausa explícita pedindo aprovação. Nada em `slides/` pode ser escrito antes da aprovação.

### Passo 1 — Validar input

Confirmar que o argumento é uma página existente em `wiki/`. Se vier só um tema (ex: `/slides livre-arbítrio`), procurar em `wiki/conceitos/`, `wiki/sinteses/`, `wiki/aprofundamentos/`, `wiki/questoes/`. Se ambíguo, perguntar.

### Passo 2 — Coletar metadados da palestra

Usar `AskUserQuestion` para obter:
- **Data da palestra** (YYYY-MM-DD) — obrigatória, nunca usar a data atual
- **Casa espírita** (opcional, ex: "Centro Espírita Allan Kardec") — valor cru vai direto no footer, sem prefixo

### Passo 3 — Buscar material via qmd

Queries read-only em `raw/` e `wiki/` para montar o outline com conteúdo real, não placeholders:

- **Pergunta + resposta literais do Kardec** (LE): query em collection `raw` pela pergunta e resposta dos Espíritos. Se a resposta >300 palavras, aplicar elipses `(...)` em trechos não-essenciais, mantendo núcleo doutrinário.
- **Citação integral** (ESE/LM/C&I): query em `raw` pela passagem referenciada.
- **"Para meditar"**: query em `wiki/sinteses/parabolas-de-jesus`, `wiki/personalidades/`, e `raw/` (Novo Testamento, C&I, André Luiz, Léon Denis, Chico Xavier) buscando ilustração pertinente ao tema. Selecionar 1-3 candidatos — apenas título + referência, nunca texto integral.

### Passo 4 — Propor outline ao usuário

Apresentar o deck completo em texto, pronto para crítica:

- **Capa** (título, obra+range, data, casa)
- **Pergunta de abertura** (5-15 palavras)
- **Partes temáticas** com Q&A já preenchido (perguntas literais + trechos de resposta com elipses quando longas)
- **"Para meditar"** — 1-3 candidatos (parábola evangélica, caso de C&I, personalidade de André Luiz) para escolha
- **Síntese final** (3-5 bullets rascunho)
- **Encerramento** — citação consolidadora opcional

Aguardar validação. Em seguida, prosseguir para a fase de geração.

## Fase de geração (pós-aprovação)

### Passo 5 — Scaffold determinístico

```bash
uv run python .claude/skills/slides/scripts/scaffold_deck.py <caminho-wiki> \
  --date <YYYY-MM-DD> [--casa "<nome da casa>"] [--out slides/<slug>/deck.md]
```

O script emite um esqueleto Marp com:

1. **Capa**: título + nome completo da obra com range (ex: `O Livro dos Espíritos · q. 674–685`) + autor + data + casa
2. **Abertura**: slide com TODO para pergunta socrática
3. **Partes** — cada seção `##` do wiki que contenha blockquotes vira uma parte, com section header `<!-- _class: section -->` de transição
4. **Q&A** — para citações LE, par pergunta+resposta; para outras obras, slide único de citação expandida
5. **Para meditar** — slide de parábola/caso/personalidade
6. **Síntese** — section header + slide de bullets
7. **Encerramento** — citação consolidadora opcional

TODOs a preencher ficam marcados como `*<!-- skill: ... -->*` em itálico.

### Passo 6 — Refinar o deck.md

Substituir todos os `<!-- skill: ... -->` com o conteúdo aprovado no Passo 4:
- Pergunta de abertura
- Perguntas e respostas literais do LE (com elipses quando longas)
- Título + referência da parábola/caso/personalidade escolhida (sem texto integral)
- Síntese (3-5 bullets)
- Encerramento (ou remover slide se não couber)

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
