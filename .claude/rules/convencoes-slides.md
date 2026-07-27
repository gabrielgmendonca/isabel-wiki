---
paths:
  - "slides/**"
  - ".claude/skills/slides/**"
---

# Convenções de slides (Marp)

Slides para palestras espíritas de Gabriel Mendonça. Padrão extraído dos PPTX em `raw/palestras/gabriel-mendonca/`.

## Estrutura socrática (invariante)

Toda palestra segue:

1. **Capa** — título + nome completo da obra-base com range de questões/itens (ex: `O Livro dos Espíritos · q. 674–685`) + autor + data da palestra + casa espírita
2. **Pergunta de abertura** — curta, retórica, ancora o tema (1 slide)
3. **Partes temáticas** — cada parte começa com section header (`<!-- _class: section -->`) nomeando o bloco
4. **Núcleo Q&A** — para LE: par pergunta literal + resposta dos Espíritos (dois slides). Para ESE/LM/C&I: citação completa em slide único. Elipses `(...)` em trechos longos não-essenciais
5. **"Para meditar"** — 1 slide com título + referência de uma parábola evangélica, caso de C&I, personalidade de André Luiz (Entre a Terra e o Céu, Nosso Lar) ou página de `wiki/personalidades/` / `wiki/sinteses/parabolas-de-jesus`. NUNCA texto integral
6. **Síntese final** — retoma a pergunta de abertura com a resposta consolidada (3-5 bullets)
7. **Encerramento** — citação consolidadora (opcional)

**Sem slides em branco** (`<!-- _class: blank -->` é legado). Transições são feitas por section headers.

Total típico: 25-50 slides.

## Densidade

- **Perguntas**: 5-15 palavras. Uma única ideia. Letra grande.
- **Respostas**: citação literal entre aspas, parágrafos preservados, referência ao final entre parênteses.
- **Slides em branco**: zero texto, só pausa.
- Evitar bullets densos no estilo PowerPoint corporativo. Cada slide é um pensamento.

### Capacidade do slide (limite físico, não estético)

A caixa útil é de **1080 × 560 px** — cerca de **12 linhas** de corpo a 30 px. Acima
disso o texto colide com o rodapé e é cortado no PPTX/PDF; já aconteceu em palestra
apresentada (`bem-aventuranca-dos-misericordiosos`, slide 43).

- **Síntese de 5 bullets longos não cabe** — dividir em dois slides de 3 + 2. Três
  bullets longos cabem com folga.
- **Pergunta de ~30 palavras** é o teto da `.pergunta`; acima disso, quebrar em duas.
- **Split background** (`![bg right:43%]`) estreita a coluna de texto para ~530 px —
  a capa aceita menos texto do que um slide comum.

Conferir sem renderizar: `lint_wiki.py --check slide_overflow`. Ver o efeito de cada
classe: `slides/themes/preview.md`.

## Citações

Mesmo formato de CLAUDE.md §3 (não duplicar exemplos aqui — fonte canônica é o §3). Respostas dos Espíritos sempre entre aspas. Nos slides usar nome completo da obra ao invés da sigla.

## Front-matter Marp

```yaml
---
marp: true
theme: isabel
paginate: true
header: '<tema da palestra>'
footer: 'Gabriel Mendonça · <data> · Casa Espírita <nome>'
---
```

Tema customizado em `slides/themes/isabel.css`. Build via `--theme slides/themes/isabel.css`.

## Classes de slide

- (default) — capa, perguntas, sínteses
- `<!-- _class: quote -->` — resposta dos Espíritos (serif, recuo, aspas grandes)
- `<!-- _class: blank -->` — slide em branco para pausa

## Localização

- `slides/<slug-do-tema>/deck.md` — versionado
- `slides/<slug-do-tema>/build/deck.pptx` e `.pdf` — gitignored
- `slides/themes/isabel.css` — versionado

## Hierarquia

Pentateuco prevalece (CLAUDE.md §2). Se citar nível 2/3 que diverge, registrar a divergência na wiki, não na palestra.
