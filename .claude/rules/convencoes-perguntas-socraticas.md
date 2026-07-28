---
paths:
  - "slides/**"
  - ".claude/skills/slides/**"
---

# Perguntas socráticas em slides

Critérios para as **perguntas-ponte** entre citações nos decks de `/slides`. Pergunta-ponte é todo slide-pergunta que **não** seja a pergunta literal do LE (essa já tem regra em `convencoes-slides.md` §4): a abertura, as transições antes de citações de ESE/LM/C&I, e as perguntas dentro de uma parte temática que conecta duas citações da mesma obra.

A reclamação que origina esta rule: muitas perguntas-ponte saíam vagas ("E se quem partiu pudesse falar?", "E a fé que ainda não raciocina, vale?") — títulos de slide com ponto de interrogação, não perguntas que forçam pensamento. O padrão socrático das palestras de Gabriel é mais exigente.

## Orçamento: 15 palavras no h2, âncora no subtítulo

**Restrição dura, anterior aos três critérios.** `section.pergunta h2` renderiza a **64px** — a pergunta ocupa o slide inteiro em letra de palco. O teto é **15 palavras** (`convencoes-slides.md` §Densidade); acima de ~22 vira parágrafo que a plateia lê em vez de ouvir o orador.

O modo de falha conhecido (deck `indulgencia`, jun/2026 — perguntas de 23, 24, 26 e 30 palavras): para satisfazer o critério A, o modelo enfia a âncora **dentro** da frase da pergunta, produzindo frase de contexto + pergunta. O tema já tem o slot certo para a âncora: `section.pergunta p`, 24px, cinza, logo abaixo.

**Âncora vai no subtítulo; a pergunta fica com uma frase só.**

```markdown
<!-- _class: pergunta -->

## Por que os mais velhos largaram a pedra primeiro?

*"...retiraram-se, um após outro, afastando-se primeiro os velhos" — O Evangelho Segundo o Espiritismo, cap. X, item 12*
```

- ✗ "Diante da adúltera, os acusadores se retiraram 'afastando-se primeiro os velhos'. Por que os mais velhos foram os primeiros a largar a pedra?" (23 palavras, duas frases)
- ✗ "Se a misericórdia é 'o esquecimento e o perdão das ofensas, sem limites', não seria pregar que tudo se releva — que o indulgente é o frouxo que tudo desculpa?" (30 palavras)
- ✓ "Perdão sem limites — então o indulgente é um frouxo?" (10 palavras, com a citação no subtítulo)

Duas frases no h2 é o sinal de que a âncora está no lugar errado. O lint (`slide_titulos`) avisa.

## Os três critérios

Toda pergunta-ponte precisa satisfazer **pelo menos um** deles — **dentro** do orçamento acima; ancorar não autoriza estourar. Se nenhum se aplica naturalmente, suprimir a pergunta e deixar o section header carregar a transição.

### A. Ancorar num particular concreto

Nome próprio, cena, número, objeto, caso já mencionado no deck. Nunca conceito abstrato sozinho.

- ✓ "Marcel pediu pílulas para não incomodar; que fé sustenta isso aos 8 anos?"
- ✓ "Como uma mãe que perdeu a filha de seis anos pode, ainda assim, agradecer a Deus?"
- ✗ "Que tipo de fé essa família tinha?" (ancoraria, mas o "essa família" é vago — não fixou nome nem cena)
- ✗ "Como manter a fé na adversidade?"

### B. Expor tensão com a resposta anterior

Usar uma afirmação que acabou de ser citada para extrair uma objeção legítima — a pergunta nasce do que o slide anterior afirmou.

- ✓ "Se a causa é anterior, por que esquecemos?" (depois de citar que a aflição tem causa em vidas passadas)
- ✓ "Se a morte prematura é benefício, por que doi tanto em quem fica?"
- ✗ "E quando a aflição não tem culpa visível?" (não retoma o que veio antes; poderia abrir qualquer capítulo)

### C. Reproduzir pergunta literal de Kardec ou do próprio Cristo

Quando o capítulo de ESE/LM/C&I começa com uma pergunta retórica (ex.: cap. V do ESE — "Por que sofrem uns mais do que outros?"), usar **a pergunta original como está**. Mesmo princípio para perguntas atribuídas a Jesus nos Evangelhos ("Quem é minha mãe?", "Que aproveita ao homem ganhar o mundo inteiro…?"). Kardec e Jesus já fizeram o trabalho socrático; o palestrante só precisa entregar a pergunta.

Esse critério estende a regra do §4 de `convencoes-slides.md` (que só cobria pares Q&A literais do LE).

## Antipadrões

- **Teaser sentimental**: "E se quem partiu pudesse falar?", "E se o sofrimento tivesse uma voz?"
- **Reformulação vazia do título da seção**: section header diz "A causa que escapa ao olhar terreno" e a pergunta-ponte diz "Como entender a causa que escapa ao olhar?".
- **Pergunta hipotética abstrata**: "E se a vida fosse mais longa do que parece?"
- **Pergunta intercambiável**: se a mesma pergunta pudesse preceder qualquer outra citação do mesmo tema sem mudança de sentido, está fraca.
- **Pergunta de "sim/não" suave**: "E a fé que ainda não raciocina, vale?" — convida só a confirmar.
- **Pergunta-parágrafo**: setup + pergunta na mesma caixa de 64px. Ver o orçamento acima — a âncora desce para o subtítulo.

## Quando suprimir

Cadência preferida: **pergunta forte → 1–3 citações → pergunta forte**. Não forçar par pergunta+citação a cada slide. Se duas citações se sustentam juntas (ex.: dois trechos do mesmo Sanson), encadeá-las sem pergunta no meio. O section header de transição já dá a respiração.

## Onde isso é aplicado pela skill

- **Passo 4** (outline): ao propor a "Pergunta de abertura" via `AskUserQuestion`, os 3 candidatos precisam satisfazer A, B ou C. Se forem todos genéricos, regerar.
- **Passo 4a** (refutação): antes do `AskUserQuestion`, rodar `validate_candidates.py --tipo pergunta [--contexto-secao "<header>"]`. O script reprova o mecânico — teaser com "E se/E a/E quando", duas frases no h2, acima de 22 palavras, reciclagem do section header — e a skill regera. Os testes de intercambiabilidade e de "e daí?" ficam na auto-refutação semântica do `SKILL.md`, porque não são decidíveis por código.
- **Passo 6** (refinar deck.md): ao preencher `<!-- skill: ... -->` em slides-pergunta entre citações ESE/LM/C&I, checar cada pergunta contra os três critérios. Se nenhuma satisfaz, **remover o slide** em vez de inventar uma fraca.
