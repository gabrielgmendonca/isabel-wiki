# Relatório de crítica profunda — 2026-06-10

## 1. Metadados do run

- **Data:** 2026-06-10
- **Escopo:** `--limit 5 (loop, lote 10)`
- **Budget:** ~650k tokens (10 agentes)
- **Modelos:** critica=opus, verificacao=sonnet
- **Páginas devidas / criticadas / puladas:** 5 / 5 / 0
- **Total de achados:** 12 (4 auto, 8 diferidos, 0 descartados)

## 2. Páginas avaliadas

| Página | Tipo | Veredito | Achados | Auto | Diferidos |
|--------|------|----------|---------|------|-----------|
| `wiki/conceitos/parabola-da-videira-verdadeira.md` | conceito | ✓ 1 auto · ⚠ 1 diferido | 2 | 1 | 1 |
| `wiki/conceitos/parabola-das-dez-virgens.md` | conceito | ⚠ 1 diferido | 1 | 0 | 1 |
| `wiki/conceitos/parabola-do-bom-pastor.md` | conceito | ✓ 2 auto · ⚠ 2 diferidos | 4 | 2 | 2 |
| `wiki/conceitos/parabola-do-bom-samaritano.md` | conceito | ✓ 1 auto · ⚠ 1 diferido | 2 | 1 | 1 |
| `wiki/conceitos/parabola-do-fariseu-e-do-publicano.md` | conceito | ⚠ 3 diferidos | 3 | 0 | 3 |

## 3. Achados por eixo

### Eixo 2 — Citações (7)

- **[alta]** `wiki/conceitos/parabola-das-dez-virgens.md`:21 — ⚠ diferido a humano
  - Afirmação: 'Kardec comenta a parábola das dez virgens no ESE, cap. XVIII'.
  - Evidência: Cap. XVIII = festim de bodas (Mt 22). As dez virgens só aparecem como alusão de passagem no cap. I item 10. Kardec não comenta a parábola no ESE.
  - Verificação: **confirmed** — cite.py + grep: cap. XVIII item 1 = festim de bodas; única ocorrência de 'virgens loucas' é alusão em comunicação mediúnica (cap. I item 10). Reenquadrar como síntese do estudante.
- **[alta]** `wiki/conceitos/parabola-do-bom-pastor.md`:33 — ⚠ diferido a humano
  - Afirmação: 'Jesus... fazia distinção entre as duas pessoas, visto que não disse: Eu sou o Pai' como literal de OPE §VIII.
  - Evidência: §VIII = 'O Verbo se fez carne' (Jo 1). A glosa de Jo 10:30 está no §III ('são um pelo pensamento...'). A frase entre aspas não é verbatim (grep zero).
  - Verificação: **confirmed** — obras-postumas: locus errado (§VIII→§III) + paráfrase entre aspas como literal. Substância (unidade moral) fiel.
- **[alta]** `wiki/conceitos/parabola-do-fariseu-e-do-publicano.md`:27 — ⚠ diferido a humano
  - Afirmação: Ancora a parábola em ESE cap. VII item 9, cap. X itens 7-8, cap. XXVIII.
  - Evidência: Cap. VII item 9 não existe; a parábola é comentada no cap. XXVII itens 3-4 ('orai com humildade como o publicano'). Reancorar a página inteira.
  - Verificação: **confirmed** — cite.py: cap. VII item 9 = erro 'não encontrado'; cap. XXVII itens 3-4 = locus real; cap. X itens 7-8 é remissão interna, não análise; cap. XXVIII = coletânea de preces.
- **[alta]** `wiki/conceitos/parabola-do-fariseu-e-do-publicano.md`:13 — ⚠ diferido a humano
  - Afirmação: Definição: 'Kardec comenta extensamente a parábola no capítulo VII do ESE'.
  - Evidência: Cap. VII comenta a parábola das bodas (Lc 14, item 5), não a do publicano (cap. XXVII item 3).
  - Verificação: **confirmed** — cite.py: cap. VII item 5 = parábola das bodas; a do publicano está no cap. XXVII item 3. Corrigir a Definição.
- **[media]** `wiki/conceitos/parabola-do-bom-pastor.md`:29 — ✓ auto-corrigido
  - Afirmação: Atribui 'Não se pode servir a Deus e a Mamon' ao ESE cap. XXIV.
  - Evidência: É o cap. XVI (índice); XXIV é 'Não ponhais a candeia debaixo do alqueire'.
  - Ação: `replace-text` — Linha 29: cap. XXIV → cap. XVI (typo de locus confirmado pelo índice).
- **[baixa]** `wiki/conceitos/parabola-do-bom-pastor.md`:66 — ✓ auto-corrigido
  - Afirmação: Fontes lista 'Caps. III, VI, XXI, XXIV'.
  - Evidência: Reflete o mesmo erro; XXIV não é citado no corpo.
  - Ação: `replace-text` — Linha 66: 'Caps. III, VI, XXI, XXIV.' → 'Caps. III, VI, XVI, XXI.'
- **[baixa]** `wiki/conceitos/parabola-do-bom-samaritano.md`:17 — ⚠ diferido a humano
  - Afirmação: Blockquote 'Texto da parábola' (S. Lucas 10:30-34) em tradução que não bate com ESE/Guillon nem Almeida.
  - Evidência: Ranges corretos, mas 'mãos de ladrões'/'maltratado'/'cavalgadura' são de uma 3ª tradução não-declarada. Alinhar à ESE/Guillon (item 2).
  - Verificação: **confirmed** — cite.py: o texto não corresponde a nenhuma das duas fontes declaradas; é tradução não identificada apresentada como literal.

### Eixo 3 — Padrão editorial (1)

- **[media]** `wiki/conceitos/parabola-do-fariseu-e-do-publicano.md`:11 — ⚠ diferido a humano
  - Afirmação: Heading 'Definição' (convenção pede 'Definição curta' como conteúdo).
  - Evidência: Cosmético; lint passa limpo.

### Eixo 4 — Tags e cross-references (4)

- **[baixa]** `wiki/conceitos/parabola-da-videira-verdadeira.md`:21 — ✓ auto-corrigido
  - Afirmação: Eixo central é o fruto moral/caridade, mas só tema/jesus.
  - Evidência: Linhas 21,46; tema/moral cabe.
  - Ação: `add-tag` — Adicionada tag tema/moral (2 temas, jesus+moral).
- **[baixa]** `wiki/conceitos/parabola-da-videira-verdadeira.md`:23 — ⚠ diferido a humano
  - Afirmação: 'fé raciocinada' e 'caridade' sem wikilink inline (alvos em Páginas relacionadas).
  - Evidência: Polimento de densidade de links; grafo já íntegro.
- **[baixa]** `wiki/conceitos/parabola-do-bom-pastor.md`:4 — ⚠ diferido a humano
  - Afirmação: Liderança moral (pastor vs. mercenário) mas só tema/jesus.
  - Evidência: Avaliar tema/moral.
- **[baixa]** `wiki/conceitos/parabola-do-bom-samaritano.md`:29 — ✓ auto-corrigido
  - Afirmação: 'Fora da caridade não há salvação' sem wikilink (aprofundamento existe).
  - Evidência: Linha 29; wiki/aprofundamentos/fora-da-caridade-nao-ha-salvacao (qmd 0.93).
  - Ação: `add-wikilink` — Envolveu 'Fora da caridade não há salvação' em wikilink ao aprofundamento.

## 4. Mudanças auto-aplicadas

- `wiki/conceitos/parabola-da-videira-verdadeira.md`:21 — `add-tag`: Adicionada tag tema/moral (2 temas, jesus+moral).
- `wiki/conceitos/parabola-do-bom-pastor.md`:29 — `replace-text`: Linha 29: cap. XXIV → cap. XVI (typo de locus confirmado pelo índice).
- `wiki/conceitos/parabola-do-bom-pastor.md`:66 — `replace-text`: Linha 66: 'Caps. III, VI, XXI, XXIV.' → 'Caps. III, VI, XVI, XXI.'
- `wiki/conceitos/parabola-do-bom-samaritano.md`:29 — `add-wikilink`: Envolveu 'Fora da caridade não há salvação' em wikilink ao aprofundamento.

## 5. Diferidos a decisão humana

> Páginas marcadas `status: rascunho`; itens anotados no ROADMAP.md §11.

- `wiki/conceitos/parabola-da-videira-verdadeira.md` (eixo 4, baixa) — 'fé raciocinada' e 'caridade' sem wikilink inline (alvos em Páginas relacionadas).
- `wiki/conceitos/parabola-das-dez-virgens.md` (eixo 2, alta) — 'Kardec comenta a parábola das dez virgens no ESE, cap. XVIII'.
- `wiki/conceitos/parabola-do-bom-pastor.md` (eixo 2, alta) — 'Jesus... fazia distinção entre as duas pessoas, visto que não disse: Eu sou o Pai' como literal de OPE §VIII.
- `wiki/conceitos/parabola-do-bom-pastor.md` (eixo 4, baixa) — Liderança moral (pastor vs. mercenário) mas só tema/jesus.
- `wiki/conceitos/parabola-do-bom-samaritano.md` (eixo 2, baixa) — Blockquote 'Texto da parábola' (S. Lucas 10:30-34) em tradução que não bate com ESE/Guillon nem Almeida.
- `wiki/conceitos/parabola-do-fariseu-e-do-publicano.md` (eixo 2, alta) — Ancora a parábola em ESE cap. VII item 9, cap. X itens 7-8, cap. XXVIII.
- `wiki/conceitos/parabola-do-fariseu-e-do-publicano.md` (eixo 2, alta) — Definição: 'Kardec comenta extensamente a parábola no capítulo VII do ESE'.
- `wiki/conceitos/parabola-do-fariseu-e-do-publicano.md` (eixo 3, media) — Heading 'Definição' (convenção pede 'Definição curta' como conteúdo).

## 6. Resumo por página

### `wiki/conceitos/parabola-da-videira-verdadeira.md`
Sólida: lint limpo, citações conferem, tensão (fogo eterno) já registrada; tag tema/moral aplicada; só um polimento de wikilinks inline.

### `wiki/conceitos/parabola-das-dez-virgens.md`
Leitura espírita sólida (azeite=mérito, LE q.132-134), mas atribui a Kardec um comentário às dez virgens no ESE cap. XVIII (que é o festim de bodas — Kardec não as comenta).

### `wiki/conceitos/parabola-do-bom-pastor.md`
Fiel (unidade moral); locus ESE XXIV→XVI corrigido + Fontes; citação de OPE com §VIII errado (é §III) e paráfrase entre aspas; tag opcional.

### `wiki/conceitos/parabola-do-bom-samaritano.md`
Citações ao Pentateuco conferem; wikilink fora-da-caridade aplicado; blockquote da parábola em tradução não-declarada (ranges corretos).

### `wiki/conceitos/parabola-do-fariseu-e-do-publicano.md`
Doutrina fiel, mas TODAS as citações ao ESE no locus errado: a parábola é comentada no cap. XXVII itens 3-4, não em cap. VII (que comenta a parábola das bodas)/X/XXVIII.
