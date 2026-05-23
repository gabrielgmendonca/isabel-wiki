---
paths:
  - "slides/**"
  - ".claude/skills/slides/**"
---

# Perguntas socráticas em slides

Critérios para as **perguntas-ponte** entre citações nos decks de `/slides`. Pergunta-ponte é todo slide-pergunta que **não** seja a pergunta literal do LE (essa já tem regra em `convencoes-slides.md` §4): a abertura, as transições antes de citações de ESE/LM/C&I, e as perguntas dentro de uma parte temática que conecta duas citações da mesma obra.

A reclamação que origina esta rule: muitas perguntas-ponte saíam vagas ("E se quem partiu pudesse falar?", "E a fé que ainda não raciocina, vale?") — títulos de slide com ponto de interrogação, não perguntas que forçam pensamento. O padrão socrático das palestras de Gabriel é mais exigente.

## Os três critérios

Toda pergunta-ponte precisa satisfazer **pelo menos um** deles. Se nenhum se aplica naturalmente, suprimir a pergunta e deixar o section header carregar a transição.

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

## Quando suprimir

Cadência preferida: **pergunta forte → 1–3 citações → pergunta forte**. Não forçar par pergunta+citação a cada slide. Se duas citações se sustentam juntas (ex.: dois trechos do mesmo Sanson), encadeá-las sem pergunta no meio. O section header de transição já dá a respiração.

## Onde isso é aplicado pela skill

- **Passo 4** (outline): ao propor a "Pergunta de abertura" via `AskUserQuestion`, os 3 candidatos precisam satisfazer A, B ou C. Se forem todos genéricos, regerar.
- **Passo 6** (refinar deck.md): ao preencher `<!-- skill: ... -->` em slides-pergunta entre citações ESE/LM/C&I, checar cada pergunta contra os três critérios. Se nenhuma satisfaz, **remover o slide** em vez de inventar uma fraca.
