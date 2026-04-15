---
paths:
  - "slides/**"
  - ".claude/skills/slides/**"
---

# Convenções de slides (Marp)

Slides para palestras espíritas de Gabriel Mendonça. Padrão extraído dos PPTX em `raw/palestras/gabriel-mendonca/`.

## Estrutura socrática (invariante)

Toda palestra segue:

1. **Capa** — título + fonte canônica (sigla + questões) + autor + data
2. **Pergunta de abertura** — curta, retórica, ancora o tema (1 slide)
3. **Núcleo Q&A** — alterna pergunta (slide com poucas palavras) + resposta (citação literal entre aspas, multi-parágrafo, com referência completa)
4. **Parábola ou caso ilustrativo** (2-4 slides) — bíblica (Filho Pródigo, Pedro na prisão), mediúnica (Encontro Marcado) ou histórica (Rainha de Oude)
5. **Slides em branco intercalados** — pausa narrativa entre blocos (use `<!-- _class: blank -->`)
6. **Síntese final** — retoma a pergunta de abertura com a resposta consolidada
7. **Encerramento** — citação consolidadora ou slide visual

Total típico: 25-50 slides.

## Densidade

- **Perguntas**: 5-15 palavras. Uma única ideia. Letra grande.
- **Respostas**: citação literal entre aspas, parágrafos preservados, referência ao final entre parênteses.
- **Slides em branco**: zero texto, só pausa.
- Evitar bullets densos no estilo PowerPoint corporativo. Cada slide é um pensamento.

## Citações

Mesmo formato de CLAUDE.md §3:

- `(LE, q. 674)` · `(LE, Introdução, item IV)`
- `(LM, 2ª parte, cap. XX, item 230)`
- `(ESE, cap. XVII, item 4)`
- `(C&I, 1ª parte, cap. VI)`
- `(Gênese, cap. XI, item 13)`

Respostas dos Espíritos sempre entre aspas.

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
- `<!-- _class: source -->` — slide final `## Fontes`

## Localização

- `slides/<slug-do-tema>/deck.md` — versionado
- `slides/<slug-do-tema>/build/deck.pptx` e `.pdf` — gitignored
- `slides/themes/isabel.css` — versionado

## Hierarquia

Pentateuco prevalece (CLAUDE.md §2). Se citar nível 2/3 que diverge, registrar a divergência na wiki, não na palestra.
