# Relatório de crítica profunda — 2026-06-10

## 1. Metadados do run

- **Data:** 2026-06-10
- **Escopo:** `--limit 5 (loop, lote 4)`
- **Budget:** ~777k tokens (17 agentes)
- **Modelos:** critica=opus, verificacao=sonnet
- **Páginas devidas / criticadas / puladas:** 5 / 5 / 0
- **Total de achados:** 23 (2 auto, 21 diferidos, 0 descartados)

## 2. Páginas avaliadas

| Página | Tipo | Veredito | Achados | Auto | Diferidos |
|--------|------|----------|---------|------|-----------|
| `wiki/conceitos/mundos-regeneradores.md` | conceito | ⚠ 6 diferidos | 6 | 0 | 6 |
| `wiki/conceitos/parabola-da-candeia-sob-o-alqueire.md` | conceito | ⚠ 6 diferidos | 6 | 0 | 6 |
| `wiki/conceitos/parabola-da-casa-sobre-a-rocha.md` | conceito | ⚠ 2 diferidos | 2 | 0 | 2 |
| `wiki/conceitos/parabola-da-figueira-seca.md` | conceito | ✓ 2 auto · ⚠ 4 diferidos | 6 | 2 | 4 |
| `wiki/conceitos/parabola-do-credor-incompassivo.md` | conceito | ⚠ 3 diferidos | 3 | 0 | 3 |

## 3. Achados por eixo

### Eixo 2 — Citações (12)

- **[alta]** `wiki/conceitos/mundos-regeneradores.md`:19 — ⚠ diferido a humano
  - Afirmação: Blockquote atribuído a (ESE, cap. III, item 16) como literal.
  - Evidência: Item 16 trata da existência cósmica dos mundos; o texto é paráfrase do item 17. Locus errado + não-literal.
  - Verificação: **confirmed** — cite.py: item 16 ≠ definição de transição; texto é paráfrase do item 17.
- **[alta]** `wiki/conceitos/mundos-regeneradores.md`:23 — ⚠ diferido a humano
  - Afirmação: Blockquote (item 17): 'doenças, sofrimentos, tribulações já são passado'.
  - Evidência: Item 17 literal: 'ainda sujeito às leis que regem a matéria... ainda tem de suportar provas'. A página INVERTE o sentido.
  - Verificação: **confirmed** — Contradição direta: Kardec diz 'ainda sujeito às vicissitudes', a página diz 'já são passado'.
- **[alta]** `wiki/conceitos/mundos-regeneradores.md`:27 — ⚠ diferido a humano
  - Afirmação: Blockquote (item 17) com frases sobre ajuda mútua e autoridade.
  - Evidência: Frases ('autoridade conquistada pela superioridade moral', 'ninguém se arvora em senhor') inexistentes no ESE (grep zero).
  - Verificação: **confirmed** — grep no ESC inteiro: frases não existem. Citação fabricada atribuída ao item 17.
- **[alta]** `wiki/conceitos/mundos-regeneradores.md`:35 — ⚠ diferido a humano
  - Afirmação: Blockquote atribuído ao item 18 ('felicidade entrevista').
  - Evidência: Item 18 trata de falibilidade/recaída; o conteúdo é do item 17. Locus errado + não-literal.
  - Verificação: **confirmed** — Item 18 = risco de recaída; a 'aurora da felicidade' é do item 17.
- **[alta]** `wiki/conceitos/parabola-da-figueira-seca.md`:31 — ⚠ diferido a humano
  - Afirmação: 'A fé é a mãe da esperança e da caridade' entre aspas atribuída ao item 10.
  - Evidência: Item 10 = médiuns; a ideia (não literal) está no item 11. Locus errado + aspas sobre paráfrase.
  - Verificação: **confirmed** — cite.py: item 10 = médiuns; nem o item 11 tem a frase literal. Locus errado + falsa literalidade.
- **[media]** `wiki/conceitos/mundos-regeneradores.md`:31 — ⚠ diferido a humano
  - Afirmação: Blockquote (item 17): 'procuram caminhar... seguindo as Suas leis'.
  - Evidência: Literal: 'tentam caminhar... cumprindo-lhe as leis'. Paráfrase leve como literal.
  - Verificação: **confirmed** — Duas trocas verificáveis; substância idêntica mas não é literal.
- **[media]** `wiki/conceitos/parabola-da-candeia-sob-o-alqueire.md`:30 — ⚠ diferido a humano
  - Afirmação: 'Por que Jesus ensinava por parábolas' atribuído ao item 3.
  - Evidência: Item 3 é o versículo (Mt 13:10-15); o comentário de Kardec é o item 4.
  - Verificação: **confirmed** — cite.py: item 3 = versículo; comentário no item 4.
- **[media]** `wiki/conceitos/parabola-da-candeia-sob-o-alqueire.md`:34 — ⚠ diferido a humano
  - Afirmação: 'Tudo o que está oculto será revelado' atribuído ao item 4.
  - Evidência: Item 4 = progressividade do ensino; a promessa está no item 5.
  - Verificação: **confirmed** — cite.py: item 4 ≠ revelação futura; está no item 5.
- **[media]** `wiki/conceitos/parabola-da-candeia-sob-o-alqueire.md`:27 — ⚠ diferido a humano
  - Afirmação: 'Espiritismo é candeia / responsabilidade dos espíritas' atribuído ao item 2.
  - Evidência: Item 2 = versículo (Lc 8:16-17); o conteúdo está nos itens 7 e 10.
  - Verificação: **confirmed** — cite.py: item 2 = versículo bíblico; argumento nos itens 7/10.
- **[media]** `wiki/conceitos/parabola-da-figueira-seca.md`:23 — ⚠ diferido a humano
  - Afirmação: 'montanhas = dificuldades' e 'fé como alavanca' creditados aos itens 9-10.
  - Evidência: Montanhas é item 2; alavanca é item 12. Itens 9-10 são figueira/médiuns.
  - Verificação: **confirmed** — cite.py: deslocamento de locus — item 2 (montanhas) e item 12 (alavanca).
- **[media]** `wiki/conceitos/parabola-do-credor-incompassivo.md`:29 — ⚠ diferido a humano
  - Afirmação: Oração Dominical 'Perdoai as nossas ofensas...' atribuída ao item 3.
  - Evidência: Item 3 = Mt 18:15,21,22 (perdão 70x7); o literal da Oração está no item 17; a lógica da medida nos itens 11/13.
  - Verificação: **confirmed** — cite.py: item 3 não contém a frase; literal no item 17, lógica da medida no item 11.
- **[baixa]** `wiki/conceitos/parabola-da-casa-sobre-a-rocha.md`:23 — ⚠ diferido a humano
  - Afirmação: Range inconsistente: corpo 'itens 7-9' vs Fontes 'itens 6-9'.
  - Evidência: Prosa ancora no item 6 (linha 25); range correto é 6-9.
  - Verificação: **confirmed** — cite.py: item 6 = aviso 'Senhor! Senhor!'; a prosa usa-o. Range correto 6-9.

### Eixo 3 — Padrão editorial (6)

- **[media]** `wiki/conceitos/parabola-da-figueira-seca.md`:27 — ⚠ diferido a humano
  - Afirmação: Conexão com semeador/festim apresentada como sendo de Kardec (item 9).
  - Evidência: Item 9 não menciona; é leitura do redator. Marcar como tal ou ancorar na fonte.
- **[baixa]** `wiki/conceitos/mundos-regeneradores.md`:39 — ⚠ diferido a humano
  - Afirmação: Desdobramento 'transição da Terra a mundo regenerador' atribuído a 'muitos espíritas' sem âncora citável.
  - Evidência: Leitura corrente, mas sem citação. Opcional ancorar em Gênese cap. XVIII.
- **[baixa]** `wiki/conceitos/parabola-da-candeia-sob-o-alqueire.md`:17 — ⚠ diferido a humano
  - Afirmação: Blockquote (Mt 5:15) usa 'velador' vs. 'candeeiro' da fonte declarada (Guillon/FEB).
  - Evidência: ESE cap. XXIV item 1 usa 'candeeiro' e formulação distinta.
- **[baixa]** `wiki/conceitos/parabola-da-candeia-sob-o-alqueire.md`:19 — ⚠ diferido a humano
  - Afirmação: Blockquote (Lc 8:16-17) com fraseado divergente da fonte ESE.
  - Evidência: ESE cap. XXIV item 2 (Guillon/FEB) tem formulação diferente.
- **[baixa]** `wiki/conceitos/parabola-da-casa-sobre-a-rocha.md`:15 — ⚠ diferido a humano
  - Afirmação: Estrutura fora do template ('Texto da parábola' extra; faltam Desdobramentos/Divergências).
  - Evidência: convencoes-frontmatter.md.
- **[baixa]** `wiki/conceitos/parabola-da-figueira-seca.md`:15 — ⚠ diferido a humano
  - Afirmação: Estrutura fora do template ('Texto da parábola' extra; falta Desdobramentos).
  - Evidência: convencoes-frontmatter.md.

### Eixo 4 — Tags e cross-references (5)

- **[baixa]** `wiki/conceitos/parabola-da-candeia-sob-o-alqueire.md`:4 — ⚠ diferido a humano
  - Afirmação: Só tema/jesus; eixo central é o dever de divulgação.
  - Evidência: Avaliar tema/historia-doutrina (divulgação).
- **[baixa]** `wiki/conceitos/parabola-da-figueira-seca.md`:4 — ✓ auto-corrigido
  - Afirmação: Só tema/jesus; conteúdo atravessa o eixo moral.
  - Evidência: 'A fé sem obras é morta', caridade prática, hipocrisia.
  - Ação: `add-tag` — Adicionada tag tema/moral ao frontmatter.
- **[baixa]** `wiki/conceitos/parabola-da-figueira-seca.md`:27 — ✓ auto-corrigido
  - Afirmação: 'parábola do semeador' sem wikilink (página existe).
  - Evidência: Linha 27; alvo wiki/conceitos/parabola-do-semeador.md existe.
  - Ação: `add-wikilink` — Envolvido 'parábola do semeador' em [[wiki/conceitos/parabola-do-semeador|parábola do semeador]].
- **[baixa]** `wiki/conceitos/parabola-do-credor-incompassivo.md`:4 — ⚠ diferido a humano
  - Afirmação: Só tema/jesus; eixo é perdão/caridade prática.
  - Evidência: Avaliar tema/prece-caridade ou tema/moral.
- **[baixa]** `wiki/conceitos/parabola-do-credor-incompassivo.md`:41 — ⚠ diferido a humano
  - Afirmação: Não linka wiki/conceitos/bem-aventuranca-dos-misericordiosos (cap. X).
  - Evidência: Página-conceito adjacente existe; cap. X é discutido na prosa.

## 4. Mudanças auto-aplicadas

- `wiki/conceitos/parabola-da-figueira-seca.md`:4 — `add-tag`: Adicionada tag tema/moral ao frontmatter.
- `wiki/conceitos/parabola-da-figueira-seca.md`:27 — `add-wikilink`: Envolvido 'parábola do semeador' em [[wiki/conceitos/parabola-do-semeador|parábola do semeador]].

## 5. Diferidos a decisão humana

> Páginas marcadas `status: rascunho`; itens anotados no ROADMAP.md §11.

- `wiki/conceitos/mundos-regeneradores.md` (eixo 2, alta) — Blockquote atribuído a (ESE, cap. III, item 16) como literal.
- `wiki/conceitos/mundos-regeneradores.md` (eixo 2, alta) — Blockquote (item 17): 'doenças, sofrimentos, tribulações já são passado'.
- `wiki/conceitos/mundos-regeneradores.md` (eixo 2, alta) — Blockquote (item 17) com frases sobre ajuda mútua e autoridade.
- `wiki/conceitos/mundos-regeneradores.md` (eixo 2, media) — Blockquote (item 17): 'procuram caminhar... seguindo as Suas leis'.
- `wiki/conceitos/mundos-regeneradores.md` (eixo 2, alta) — Blockquote atribuído ao item 18 ('felicidade entrevista').
- `wiki/conceitos/mundos-regeneradores.md` (eixo 3, baixa) — Desdobramento 'transição da Terra a mundo regenerador' atribuído a 'muitos espíritas' sem âncora citável.
- `wiki/conceitos/parabola-da-candeia-sob-o-alqueire.md` (eixo 2, media) — 'Por que Jesus ensinava por parábolas' atribuído ao item 3.
- `wiki/conceitos/parabola-da-candeia-sob-o-alqueire.md` (eixo 2, media) — 'Tudo o que está oculto será revelado' atribuído ao item 4.
- `wiki/conceitos/parabola-da-candeia-sob-o-alqueire.md` (eixo 2, media) — 'Espiritismo é candeia / responsabilidade dos espíritas' atribuído ao item 2.
- `wiki/conceitos/parabola-da-candeia-sob-o-alqueire.md` (eixo 3, baixa) — Blockquote (Mt 5:15) usa 'velador' vs. 'candeeiro' da fonte declarada (Guillon/FEB).
- `wiki/conceitos/parabola-da-candeia-sob-o-alqueire.md` (eixo 3, baixa) — Blockquote (Lc 8:16-17) com fraseado divergente da fonte ESE.
- `wiki/conceitos/parabola-da-candeia-sob-o-alqueire.md` (eixo 4, baixa) — Só tema/jesus; eixo central é o dever de divulgação.
- `wiki/conceitos/parabola-da-casa-sobre-a-rocha.md` (eixo 3, baixa) — Estrutura fora do template ('Texto da parábola' extra; faltam Desdobramentos/Divergências).
- `wiki/conceitos/parabola-da-casa-sobre-a-rocha.md` (eixo 2, baixa) — Range inconsistente: corpo 'itens 7-9' vs Fontes 'itens 6-9'.
- `wiki/conceitos/parabola-da-figueira-seca.md` (eixo 2, alta) — 'A fé é a mãe da esperança e da caridade' entre aspas atribuída ao item 10.
- `wiki/conceitos/parabola-da-figueira-seca.md` (eixo 2, media) — 'montanhas = dificuldades' e 'fé como alavanca' creditados aos itens 9-10.
- `wiki/conceitos/parabola-da-figueira-seca.md` (eixo 3, media) — Conexão com semeador/festim apresentada como sendo de Kardec (item 9).
- `wiki/conceitos/parabola-da-figueira-seca.md` (eixo 3, baixa) — Estrutura fora do template ('Texto da parábola' extra; falta Desdobramentos).
- `wiki/conceitos/parabola-do-credor-incompassivo.md` (eixo 2, media) — Oração Dominical 'Perdoai as nossas ofensas...' atribuída ao item 3.
- `wiki/conceitos/parabola-do-credor-incompassivo.md` (eixo 4, baixa) — Só tema/jesus; eixo é perdão/caridade prática.
- `wiki/conceitos/parabola-do-credor-incompassivo.md` (eixo 4, baixa) — Não linka wiki/conceitos/bem-aventuranca-dos-misericordiosos (cap. X).

## 6. Resumo por página

### `wiki/conceitos/mundos-regeneradores.md`
Fiel na substância e na terminologia canônica, mas TODOS os blockquotes têm texto entre aspas que não corresponde ao locus (item 16 traz texto do 17; loci 17/18 com redação inexistente; item 18 INVERTE Kardec).

### `wiki/conceitos/parabola-da-candeia-sob-o-alqueire.md`
Fiel ao ESE cap. XXIV; loci trocados (versículos citados em vez do comentário de Kardec: item 3→4, 4→5, 2→7/10) e blockquotes em tradução divergente da fonte declarada.

### `wiki/conceitos/parabola-da-casa-sobre-a-rocha.md`
Sólida e lint-clean; range de itens inconsistente (corpo '7-9' vs Fontes '6-9'; correto 6-9) e desvio do template.

### `wiki/conceitos/parabola-da-figueira-seca.md`
Fiel à interpretação de Kardec; tag tema/moral + wikilink semeador aplicados; 'A fé é a mãe...' entre aspas em locus errado (item 10→11), 'montanhas' creditado a 9-10 quando é item 2/12.

### `wiki/conceitos/parabola-do-credor-incompassivo.md`
Sólida e lint-clean; Oração Dominical atribuída ao item 3 (Mt 18) quando o literal está no item 17; tags e cross-ref opcionais.
