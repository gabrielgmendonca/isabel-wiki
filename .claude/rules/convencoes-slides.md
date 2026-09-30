---
paths:
  - "slides/**"
  - ".claude/skills/slides/**"
---

# Convenções de slides (Marp)

Padrão das palestras de Gabriel Mendonça (`raw/palestras/gabriel-mendonca/`). Típico: 25-50 slides.

## Estrutura socrática (invariante)

1. **Capa** — título + obra-base com range (`O Livro dos Espíritos · q. 674–685`) + autor + data + casa espírita.
2. **Pergunta de abertura** — curta, ancora o tema.
3. **Partes temáticas** — cada uma abre com `<!-- _class: section -->`.
4. **Núcleo Q&A** — LE: pergunta literal + resposta dos Espíritos (dois slides). ESE/LM/C&I: citação completa em slide único; `(...)` em trechos não essenciais.
5. **"Para meditar"** — 1 slide com título + referência (parábola, caso de C&I, André Luiz, página da wiki). Nunca texto integral.
6. **Síntese final** — retoma a pergunta de abertura (3-5 bullets).
7. **Encerramento** — citação consolidadora (opcional).

Sem slides em branco (`_class: blank` é legado); transição é por section header.

## Densidade e capacidade

- Um pensamento por slide; nada de bullets corporativos. Pergunta: 5-15 palavras. Resposta: citação literal entre aspas, referência entre parênteses, **nome da obra por extenso** (não sigla).
- Caixa útil **1080 × 560 px ≈ 12 linhas** — acima disso o texto é cortado no PPTX/PDF. 5 bullets longos → dividir em 3 + 2. Teto da `.pergunta`: ~30 palavras. `![bg right:43%]` estreita a coluna para ~530 px.
- Conferir: `lint_wiki.py --check slide_overflow`; classes visíveis em `slides/themes/preview.md`.

## Arquivos

```yaml
---
marp: true
theme: isabel
paginate: true
header: '<tema da palestra>'
footer: 'Gabriel Mendonça · <data> · Casa Espírita <nome>'
---
```

`slides/<slug>/deck.md` (versionado) · `slides/<slug>/build/` (gitignored) · tema `slides/themes/isabel.css` (`--theme`). Classes: default, `quote` (resposta dos Espíritos), `section`, `pergunta`.

Divergência de nível 2/3 com o Pentateuco é registrada na wiki, não na palestra.
