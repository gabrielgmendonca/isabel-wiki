# Relatório de crítica profunda — 2026-06-10

## 1. Metadados do run

- **Data:** 2026-06-10
- **Escopo:** `--limit 5 (loop, lote 7)`
- **Budget:** ~810k tokens (16 agentes)
- **Modelos:** critica=opus, verificacao=sonnet
- **Páginas devidas / criticadas / puladas:** 5 / 5 / 0
- **Total de achados:** 18 (5 auto, 13 diferidos, 0 descartados)

## 2. Páginas avaliadas

| Página | Tipo | Veredito | Achados | Auto | Diferidos |
|--------|------|----------|---------|------|-----------|
| `wiki/conceitos/resignacao.md` | conceito | ✓ 2 auto · ⚠ 2 diferidos | 4 | 2 | 2 |
| `wiki/conceitos/separacao-e-reencontro.md` | conceito | ⚠ 5 diferidos | 5 | 0 | 5 |
| `wiki/conceitos/vida-espirita.md` | conceito | ✓ 2 auto · ⚠ 2 diferidos | 4 | 2 | 2 |
| `wiki/conceitos/vida-futura.md` | conceito | ⚠ 3 diferidos | 3 | 0 | 3 |
| `wiki/conceitos/evangelizacao-infantojuvenil.md` | conceito | ✓ 1 auto · ⚠ 1 diferido | 2 | 1 | 1 |

## 3. Achados por eixo

### Eixo 2 — Citações (11)

- **[alta]** `wiki/conceitos/separacao-e-reencontro.md`:19 — ⚠ diferido a humano
  - Afirmação: Blockquote 'Os que se amaram se reencontram após a morte e se reconhecem' atribuído a (LE, q. 274-276).
  - Evidência: q.274-276 = hierarquia dos Espíritos. Reconhecimento é q.285, mas a frase não é literal nem lá.
  - Verificação: **confirmed** — cite.py: q.274-276 = hierarquia; locus correto q.285; frase não-literal apresentada como citação.
- **[alta]** `wiki/conceitos/separacao-e-reencontro.md`:21 — ⚠ diferido a humano
  - Afirmação: 'acompanhar/proteger os que ficaram, servindo de guia espiritual' (LE, q. 284-285).
  - Evidência: q.284-285 = individualidade/reconhecimento. Proteção/guia é doutrina dos Espíritos protetores (LE q.489 ss.).
  - Verificação: **confirmed** — cite.py: locus errado; reancorar em q.489 ss. e linkar [[wiki/conceitos/anjos]].
- **[alta]** `wiki/conceitos/separacao-e-reencontro.md`:29 — ⚠ diferido a humano
  - Afirmação: 'reencarnar juntos para prosseguir relações anteriores' (LE, q. 284-285).
  - Evidência: q.284-285 = individualidade/reconhecimento, não reencarnação conjunta. Locus real: q.205.
  - Verificação: **confirmed** — cite.py: afirmação correta, locus errado; q.205 trata de afeições anteriores reconstituídas na família.
- **[alta]** `wiki/conceitos/vida-futura.md`:19 — ⚠ diferido a humano
  - Afirmação: 'A vida futura é a vida normal do Espírito; a vida corpórea é transitória' como literal de (ESE, cap. II, item 2).
  - Evidência: Item 2 = 'eixo do ensino do Cristo', não contém a frase. Deriva do cap. XXIII item 8 ('vida espiritual'/'existência terrestre'), com termos trocados.
  - Verificação: **confirmed** — cite.py: locus errado + dois termos doutrinários trocados; texto real está no cap. XXIII item 8.
- **[alta]** `wiki/conceitos/vida-futura.md`:23 — ⚠ diferido a humano
  - Afirmação: 'A vida corporal é necessária ao aperfeiçoamento... encarnação se reproduza' como literal de (ESE, cap. II, item 5).
  - Evidência: Item 5 trata de outra coisa; grep em raw zero para 'encarnação se reproduza'. Frase fabricada.
  - Verificação: **confirmed** — cite.py + grep: frase inexistente no ESE/LE; deturpação, não typo de locus.
- **[alta]** `wiki/conceitos/vida-futura.md`:27 — ⚠ diferido a humano
  - Afirmação: 'Aquele que se considera apenas viajante de passagem...' como literal de (ESE, cap. II, item 3).
  - Evidência: Item 3 = ideia vaga dos judeus; grep zero para 'viajante de passagem'. A tese está no item 5 com outra formulação.
  - Verificação: **confirmed** — cite.py + grep: frase não localizável; fabricada ou de origem desconhecida atribuída ao item 3.
- **[media]** `wiki/conceitos/resignacao.md`:17 — ⚠ diferido a humano
  - Afirmação: 'Os Espíritos bons nos atraem para o bem...' citado como (LE, Parte 2, cap. I, Introdução).
  - Evidência: Verbatim em livro-dos-espiritos.md:84, mas é a Introdução item VI; o locus citado inexiste. Forma canônica: (LE, Introdução, item VI).
  - Verificação: **confirmed** — cite.py 'Introdução, item VI' resolve e retorna verbatim; 'Parte 2, cap. I, Introdução' = referência não reconhecida.
- **[media]** `wiki/conceitos/separacao-e-reencontro.md`:25 — ⚠ diferido a humano
  - Afirmação: Grupos por simpatia + 'o pai de hoje pode ter sido o filho ontem' (LE, q. 274-278).
  - Evidência: Grupos por simpatia = q.278; inversão de laços = q.205. q.274-276 (hierarquia) irrelevantes.
  - Verificação: **confirmed** — cite.py: estreitar para q.278 (grupos) + q.205 (inversão de laços).
- **[media]** `wiki/conceitos/evangelizacao-infantojuvenil.md`:39 — ⚠ diferido a humano
  - Afirmação: 'guiar os Espíritos que Deus lhes confiou para a vida terrestre' entre aspas como literal de (ESE, cap. XIV, item 9).
  - Evidência: Locus existe; ideia fiel; mas a frase não é literal (item 9: 'ponde todo o vosso amor em aproximar de Deus essa alma; tal a missão que vos está confiada... Que fizestes do filho confiado à vossa guarda?'). De-quote ou usar a frase literal.
  - Verificação: **confirmed** — qmd/cite.py: 'guiar'/'para a vida terrestre' ausentes no item 9. Paráfrase apresentada como literal.
- **[baixa]** `wiki/conceitos/resignacao.md`:21 — ⚠ diferido a humano
  - Afirmação: 'Bem-aventurados os aflitos, porque serão consolados' (Mt 5:4).
  - Evidência: ESE item 1 = 'os que choram... serão consolados'; item 18 = 'os aflitos... reino dos céus'. A página mescla sujeito do 18 com predicado do 1 — fraseado composto inexistente.
  - Verificação: **confirmed** — cite.py: fusão de dois loci apresentada como literal de Mt 5:4.
- **[baixa]** `wiki/conceitos/vida-espirita.md`:15 — ⚠ diferido a humano
  - Afirmação: Blockquote (LE, q. 224): 'Espírito errante, que aspira a novo destino, que espera.'
  - Evidência: Literal: 'que aspira a novo destino; fica esperando.' Locus correto, texto não-literal.
  - Verificação: **confirmed** — cite.py: 'que espera' vs 'fica esperando'; em blockquote citacional.

### Eixo 3 — Padrão editorial (2)

- **[baixa]** `wiki/conceitos/separacao-e-reencontro.md`:49 — ⚠ diferido a humano
  - Afirmação: Fontes resume range como 'cap. VI, q. 274-285'.
  - Evidência: As afirmações puxam de loci dispersos (cap. IV q.205 + cap. VI q.278,285). Ajustar após corrigir o corpo.
- **[baixa]** `wiki/conceitos/vida-espirita.md`:11 — ⚠ diferido a humano
  - Afirmação: Estrutura fora do template (headings próprios).
  - Evidência: convencoes-frontmatter.md.

### Eixo 4 — Tags e cross-references (5)

- **[baixa]** `wiki/conceitos/resignacao.md`:4 — ✓ auto-corrigido
  - Afirmação: Conceito-virtude com só tema/sofrimento.
  - Evidência: Tags livres 'virtude, moral'; tema/moral cabe.
  - Ação: `add-tag` — Adicionada tag tema/moral.
- **[baixa]** `wiki/conceitos/resignacao.md`:17 — ✓ auto-corrigido
  - Afirmação: 'lei de causa e efeito' sem wikilink.
  - Evidência: Linha 17; página existe.
  - Ação: `add-wikilink` — Envolvida 'lei de causa e efeito' em wikilink na linha 17.
- **[baixa]** `wiki/conceitos/vida-espirita.md`:4 — ✓ auto-corrigido
  - Afirmação: Trata reencarnação/escolha de provas mas só tema/vida-futura.
  - Evidência: Seção 'Escolha das provas' (LE q.258); tema/encarnacao cabe.
  - Ação: `add-tag` — Adicionada tag tema/encarnacao.
- **[baixa]** `wiki/conceitos/vida-espirita.md`:29 — ✓ auto-corrigido
  - Afirmação: 'livre-arbítrio' nomeado sem wikilink.
  - Evidência: Linha 29; página existe.
  - Ação: `add-wikilink` — Envolvido 'livre-arbítrio' em [[wiki/conceitos/livre-arbitrio]] na linha 29.
- **[baixa]** `wiki/conceitos/evangelizacao-infantojuvenil.md`:4 — ✓ auto-corrigido
  - Afirmação: Trata educação moral na família mas só tema/moral.
  - Evidência: Seções sobre dever dos pais/lar/geração espírita; tema/sociedade cabe.
  - Ação: `add-tag` — Adicionada tag tema/sociedade.

## 4. Mudanças auto-aplicadas

- `wiki/conceitos/resignacao.md`:4 — `add-tag`: Adicionada tag tema/moral.
- `wiki/conceitos/resignacao.md`:17 — `add-wikilink`: Envolvida 'lei de causa e efeito' em wikilink na linha 17.
- `wiki/conceitos/vida-espirita.md`:4 — `add-tag`: Adicionada tag tema/encarnacao.
- `wiki/conceitos/vida-espirita.md`:29 — `add-wikilink`: Envolvido 'livre-arbítrio' em [[wiki/conceitos/livre-arbitrio]] na linha 29.
- `wiki/conceitos/evangelizacao-infantojuvenil.md`:4 — `add-tag`: Adicionada tag tema/sociedade.

## 5. Diferidos a decisão humana

> Páginas marcadas `status: rascunho`; itens anotados no ROADMAP.md §11.

- `wiki/conceitos/resignacao.md` (eixo 2, media) — 'Os Espíritos bons nos atraem para o bem...' citado como (LE, Parte 2, cap. I, Introdução).
- `wiki/conceitos/resignacao.md` (eixo 2, baixa) — 'Bem-aventurados os aflitos, porque serão consolados' (Mt 5:4).
- `wiki/conceitos/separacao-e-reencontro.md` (eixo 2, alta) — Blockquote 'Os que se amaram se reencontram após a morte e se reconhecem' atribuído a (LE, q. 274-276).
- `wiki/conceitos/separacao-e-reencontro.md` (eixo 2, alta) — 'acompanhar/proteger os que ficaram, servindo de guia espiritual' (LE, q. 284-285).
- `wiki/conceitos/separacao-e-reencontro.md` (eixo 2, media) — Grupos por simpatia + 'o pai de hoje pode ter sido o filho ontem' (LE, q. 274-278).
- `wiki/conceitos/separacao-e-reencontro.md` (eixo 2, alta) — 'reencarnar juntos para prosseguir relações anteriores' (LE, q. 284-285).
- `wiki/conceitos/separacao-e-reencontro.md` (eixo 3, baixa) — Fontes resume range como 'cap. VI, q. 274-285'.
- `wiki/conceitos/vida-espirita.md` (eixo 2, baixa) — Blockquote (LE, q. 224): 'Espírito errante, que aspira a novo destino, que espera.'
- `wiki/conceitos/vida-espirita.md` (eixo 3, baixa) — Estrutura fora do template (headings próprios).
- `wiki/conceitos/vida-futura.md` (eixo 2, alta) — 'A vida futura é a vida normal do Espírito; a vida corpórea é transitória' como literal de (ESE, cap. II, item 2).
- `wiki/conceitos/vida-futura.md` (eixo 2, alta) — 'A vida corporal é necessária ao aperfeiçoamento... encarnação se reproduza' como literal de (ESE, cap. II, item 5).
- `wiki/conceitos/vida-futura.md` (eixo 2, alta) — 'Aquele que se considera apenas viajante de passagem...' como literal de (ESE, cap. II, item 3).
- `wiki/conceitos/evangelizacao-infantojuvenil.md` (eixo 2, media) — 'guiar os Espíritos que Deus lhes confiou para a vida terrestre' entre aspas como literal de (ESE, cap. XIV, item 9).

## 6. Resumo por página

### `wiki/conceitos/resignacao.md`
Sólida; tag tema/moral + wikilink lei-de-causa-e-efeito aplicados; locus do LE errado (texto verbatim mas é Introdução item VI); bem-aventurança com fraseado composto.

### `wiki/conceitos/separacao-e-reencontro.md`
Tese alinhada, mas 4 citações ao LE com loci que não sustentam (q.274-276 = hierarquia; proteção/guia em q.284-285 quando é q.489; inversão de laços é q.205); blockquote fabricado.

### `wiki/conceitos/vida-espirita.md`
Sólida: 6 citações do LE conferem; tag tema/encarnacao + wikilink livre-arbitrio aplicados; blockquote q.224 não-literal; estrutura.

### `wiki/conceitos/vida-futura.md`
Teses sólidas, mas 3 'citações literais' de ESE cap. II não correspondem ao locus: uma deriva do cap. XXIII item 8 com termos trocados; duas são frases inexistentes no corpus.

### `wiki/conceitos/evangelizacao-infantojuvenil.md`
Sólida, ancorada em Kardec; tag tema/sociedade aplicada; 'citação' de ESE cap. XIV item 9 é paráfrase entre aspas (ideia fiel, forma inventada).
