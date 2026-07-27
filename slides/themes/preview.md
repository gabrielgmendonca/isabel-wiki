---
marp: true
theme: isabel
paginate: true
header: 'Preview do tema isabel — não é palestra'
footer: 'slides/themes/preview.md · regressão visual do isabel.css'
---

<!--
Deck de demonstração do tema. Um slide por classe/padrão, para inspecionar o
isabel.css sem gastar uma palestra real (ROADMAP §7). O cabeçalho de cada slide
diz o que aquele slide testa. As citações são reais e verificadas por cite.py
(LE q. 886; ESE cap. X, itens 4 e 16) — mas o deck NÃO é uma palestra: a ordem
segue a cobertura do tema, não um arco socrático.

Build:  uv run python .claude/skills/slides/scripts/build_deck.py slides/themes/preview.md
-->

<!-- _header: 'CAPA · default + bg right:43% — h1 com régua, obra em negrito' -->

![bg right:43%](assets/fixture-placeholder.jpg)

# "Atire a primeira pedra": a indulgência não é fraqueza

**O Evangelho Segundo o Espiritismo · cap. X**

Gabriel Mendonça · 00/00/0000 · Casa Espírita Exemplo

---

<!--
_class: pergunta
_header: 'CLASSE .pergunta · pergunta curta (13 palavras) — h2 64px centralizado'
-->

## Severos com os outros, indulgentes conosco: o que muda ao inverter a direção?

*O Evangelho Segundo o Espiritismo, cap. X, item 16*

---

<!--
_class: pergunta
_header: '.pergunta · LIMITE conhecido (30 palavras) — acima disso, quebrar em duas'
-->

## Se a misericórdia é "o esquecimento e o perdão das ofensas", sem limites, não seria pregar que tudo se releva — que o indulgente é o frouxo que tudo desculpa?

---

<!--
_class: section
_header: 'CLASSE .section · transição entre partes (fundo accent, texto claro)'
-->

## Parte 2

### A correção de Jesus: indulgência é dever, porque dela todos precisamos

---

<!-- _header: 'NÚCLEO Q&A · pergunta literal do LE (default, sem imagem)' -->

## O Livro dos Espíritos, q. 886

Qual o verdadeiro sentido da palavra caridade, como a entendia Jesus?

---

<!--
_class: quote
_header: 'CLASSE .quote · citação curta (fundo #ecf2e7, serif 34px, filete accent)'
-->

> Benevolência para com todos, indulgência para as imperfeições dos outros, perdão das ofensas.

**O Livro dos Espíritos, q. 886 (Resposta dos Espíritos)**

---

<!--
_class: quote
_header: '.quote · LIMITE conhecido (~65 palavras) — acima disso, elipsar ou dividir'
-->

> A indulgência não vê os defeitos de outrem, ou, se os vê, evita falar deles, divulgá-los. (...) Sede, pois, severos para convosco, indulgentes para com os outros. (...) Sede indulgentes, meus amigos, porquanto a indulgência atrai, acalma, ergue, ao passo que o rigor desanima, afasta e irrita.

**O Evangelho Segundo o Espiritismo, cap. X, item 16 (José, Espírito protetor)**

---

<!--
_header: 'SPLIT bg left:45% · Para meditar — crédito de imagem no rodapé'
_footer: 'Fixture sintético do tema · sem direitos de terceiros · ver assets/creditos.json'
-->

![bg left:45%](assets/fixture-placeholder.jpg)

## Lemaire

*O Céu e o Inferno, 2ª parte, cap. VI — "Criminosos arrependidos"*

O criminoso que, no além, vê as próprias vítimas em paz — e ainda as odeia.

O rancor não pune quem o recebe: pune quem o guarda.

---

<!-- _header: 'SÍNTESE · 3 bullets longos — CABE com folga' -->

## Síntese

- "Atire a primeira pedra" **não** relativiza o erro — faz da indulgência um **dever** de quem também precisa dela (cap. X, item 13).
- A indulgência é o **avesso do nosso hábito**: virtude ativa que ergue, não omissão que cala (item 16).
- **Não é laxismo**: repreender com moderação e fim útil continua dever (item 19).

---

<!--
_header: 'SÍNTESE · 5 bullets longos — TRANSBORDA (caso que calibra check_slide_overflow)'
lint: overflow-esperado
-->

## Síntese

- "Atire a primeira pedra" **não** relativiza o erro — faz da indulgência um **dever** de quem também precisa dela (cap. X, item 13).
- A indulgência é o **avesso do nosso hábito**: "severos para convosco, indulgentes para com os outros" — virtude ativa que ergue, não omissão que cala (item 16).
- **Não é laxismo**: repreender com moderação e fim útil continua dever (item 19); o perdão dos lábios que guarda rancor não conta diante de Deus (item 15).
- O alcance é **espiritual**: o rancor não saldado é raiz da maioria das obsessões e se perpetua em outras vidas (cap. X, item 6).
- Por isso "**obterão misericórdia**" não é prêmio arbitrário, mas **lei de causa e efeito**: de indulgência precisamos nós mesmos (O Livro dos Espíritos, q. 886).

---

<!-- _header: 'ESPÉCIME TIPOGRÁFICO · escala e tokens do isabel.css' -->

# Título de slide — h1, 56 px

## Subtítulo — h2, 44 px, cor accent

### Terciário — h3, 32 px, cor muted, com **negrito em accent**

Parágrafo corrido a 30 px, entrelinha 1,45. Área útil do slide: 1080 × 560 px (1280 × 720 menos padding de 80/100) — cerca de **12 linhas** a 30 px.

- Item de lista, também 30 px
- Tokens: bg `#fbfaf6` · fg `#1f1b16` · muted `#5e665a` · accent `#3d5a3d` · rule `#c8d2c0`

---

<!-- _header: 'CHECKLIST · o que conferir depois de mexer no isabel.css' -->

## O que este deck testa

- **Capa**: régua sob o h1; a imagem à direita não invade o texto.
- **`.pergunta`**: h2 centralizado nos dois eixos, sem imagem.
- **`.quote`**: fundo mais escuro, serif itálico, filete à esquerda.
- **`.section`**: texto claro sobre accent — header e rodapé inclusive.
- **Split bg**: texto sempre sobre fundo claro (full-bleed aqui é ilegível).
- **Capacidade**: o slide de 5 bullets transborda; o de 3, não.
