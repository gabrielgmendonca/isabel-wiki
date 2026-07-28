---
paths:
  - "slides/**"
  - ".claude/skills/slides/**"
---

# Títulos de palestra e de seção

Critérios para o **título da palestra** (H1 da capa + `header:`) e para os **títulos de parte** (section headers `<!-- _class: section -->`) nos decks de `/slides`.

A reclamação que origina esta rule: os títulos saíam ruins porque **nunca eram escritos** — o scaffold herdava o H1 da página wiki para a capa e cada `##` da página para as partes. Um título de wiki é **verbete de índice**: nominal, taxonômico, otimizado para busca e desambiguação ("Expiação e arrependimento", "A causa que escapa ao olhar terreno", "O excesso íntimo"). Um título de palestra é anunciado a uma plateia que está entrando na sala. São peças diferentes, e a herança nunca produz a segunda.

## Teste de origem (o único obrigatório)

**O título do deck e os títulos de parte não podem ser iguais aos headings da página wiki de origem.** Se forem, não foram escritos — foram copiados. O lint (`slide_titulos`) trava isso; a rule diz o que colocar no lugar.

Corolário: `## Parte 1` sem nome não é título. Numerar é opcional; nomear não é.

## Padrões que funcionam

Extraídos do que deu certo no corpus (`slides/`, `raw/palestras/gabriel-mendonca/`), em ordem de preferência:

### 1. Palavra de Jesus ou de Kardec, verbatim

O Pentateuco já escreveu o título. Mesmo princípio do critério C de `convencoes-perguntas-socraticas.md`.

- ✓ "Bem-aventurados os misericordiosos" (ESE, cap. X)
- ✓ "Ajuda-te a ti mesmo, que o céu te ajudará" (ESE, cap. XXV)
- ✓ "Sede severos para convosco, indulgentes para com os outros"

### 2. Cena + tese

A cena concreta que a palestra já cita, seguida da afirmação que ela sustenta. Casa com a `convencoes-imagens.md` (a cena é também o gancho de imagem).

- ✓ "'Atire a primeira pedra': a indulgência não é fraqueza, é justiça"

### 3. Afirmação contestável

Uma frase com a qual a plateia pode discordar antes de você falar. As melhores do corpus saíram assim — e saíram como títulos de *parte*, não de capa:

- ✓ "Ninguém é irrecuperável"
- ✓ "O futuro jamais se fecha"
- ✓ "Indulgência não é conivência nem perdão fingido"

Para **títulos de parte**, este é o padrão default: um section header deve ser uma **afirmação ou uma cena**, nunca um rótulo de tópico. "Ninguém é irrecuperável" > "A tríade".

## Antipadrões

- **Coordenação de conceitos** — "Expiação e arrependimento", "A justiça das aflições e a fé que consola". O "X e Y" é a assinatura do título de wiki.
- **Telegráfico com dois-pontos** — "Dor: Rigidez".
- **Parte sem nome** — "Parte 1", "I —", "Parte II" sozinhos.
- **Nominalização abstrata** — "A causa que escapa ao olhar terreno", "O excesso íntimo", "A tríade", "A dureza social". Rótulo de sumário, não título de bloco falado.
- **Título que repete a pergunta de abertura** — se o section header e a pergunta-ponte seguinte dizem a mesma coisa, um dos dois é supérfluo (ver antipadrão "reformulação vazia" em `convencoes-perguntas-socraticas.md`).

## Comprimento

- **Capa**: até ~12 palavras. Com `![bg right:43%]` a coluna cai para ~530 px — ver capacidade do slide em `convencoes-slides.md`.
- **Parte**: até ~8 palavras. O section header é lido em um golpe de vista.

## Onde isso é aplicado pela skill

- **Passo 4** (outline): o título da palestra é uma das perguntas do `AskUserQuestion` — 3 candidatos, cada um de um padrão diferente acima, nenhum igual ao H1 da wiki. O usuário escolhe ou dá o seu via "Other".
- **Passo 4a** (refutação): os candidatos passam por `validate_candidates.py --tipo titulo` antes de chegar ao usuário — o script reprova o que é decidível por código (origem, comprimento, telegráfico, rótulo curto, padrões repetidos) e a skill regera. O julgamento "rótulo ou afirmação?" em títulos de 7+ palavras **não** é alcançado pelo script: fica na auto-refutação do `SKILL.md`.
- **Passo 6** (refinar deck.md): todo `<!-- skill: renomear título da parte -->` é **obrigatório**, não opcional. Herdar o heading da wiki é a falha, não o fallback. Conferir os títulos de parte com `validate_candidates.py --tipo secao --wiki-page <página>`.
- **CI** (camada 0): `lint_wiki.py --check slide_titulos` trava no push o que escapou — parte sem nome e pergunta acima de 22 palavras são `error`.
