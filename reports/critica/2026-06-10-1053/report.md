# Relatório de crítica profunda — 2026-06-10

## 1. Metadados do run

- **Data:** 2026-06-10
- **Escopo:** `--limit 5 (loop, lote 8)`
- **Budget:** ~635k tokens (12 agentes)
- **Modelos:** critica=opus, verificacao=sonnet
- **Páginas devidas / criticadas / puladas:** 5 / 5 / 0
- **Total de achados:** 15 (2 auto, 12 diferidos, 1 descartados)

## 2. Páginas avaliadas

| Página | Tipo | Veredito | Achados | Auto | Diferidos |
|--------|------|----------|---------|------|-----------|
| `wiki/conceitos/harmonia-das-esferas.md` | conceito | ⚠ 1 diferido | 1 | 0 | 1 |
| `wiki/conceitos/morte.md` | conceito | ⚠ 4 dif · ✕ 1 desc | 5 | 0 | 4 |
| `wiki/conceitos/parabola-do-semeador.md` | conceito | ⚠ 2 diferidos | 2 | 0 | 2 |
| `wiki/conceitos/potencias-da-alma.md` | conceito | ✓ 1 auto · ⚠ 3 diferidos | 4 | 1 | 3 |
| `wiki/conceitos/progresso-espiritual.md` | conceito | ✓ 1 auto · ⚠ 2 diferidos | 3 | 1 | 2 |

## 3. Achados por eixo

### Eixo 2 — Citações (7)

- **[alta]** `wiki/conceitos/parabola-do-semeador.md`:33 — ⚠ diferido a humano
  - Afirmação: 'a condenação do egoísmo, da indiferença, do amor das riquezas e da vaidade' entre aspas atribuída a (ESE, cap. XVII, item 6).
  - Evidência: Item 6 trata dos matizes dos espíritas diante do Evangelho; grep no ESE inteiro = zero para a frase. Citação fabricada.
  - Verificação: **confirmed** — cite.py + grep: frase inexistente no ESE. Aspas + 'Kardec observa que' = atribuição literal falsa.
- **[alta]** `wiki/conceitos/potencias-da-alma.md`:21 — ⚠ diferido a humano
  - Afirmação: 'Querendo, o Espírito atua sobre a matéria...' entre aspas atribuída a (LE, q. 459).
  - Evidência: q.459 trata da influência dos Espíritos nos pensamentos. A frase não consta. Tema da ação sobre a matéria é Gênese cap. XIV / RE jun/1868.
  - Verificação: **confirmed** — cite.py: q.459 = influência dos Espíritos; frase não está em q.459 nem encontrada via qmd. Locus incorreto.
- **[alta]** `wiki/conceitos/potencias-da-alma.md`:21 — ⚠ diferido a humano
  - Afirmação: 'A vontade cresce com o adiantamento moral... (LE, q. 635)'.
  - Evidência: q.635 trata de posições sociais. A ideia de força que cresce com a elevação é q.872 ('força moral'), não q.635.
  - Verificação: **confirmed** — cite.py: q.635 ≠ vontade/elevação. Candidato q.872, mas fala de 'força moral', não 'alcance da vontade'.
- **[media]** `wiki/conceitos/morte.md`:39 — ⚠ diferido a humano
  - Afirmação: 'ela é uma porta de entrada na vida, e não como a porta do nada' (C&I, 1ª parte, cap. II).
  - Evidência: Literal: 'a porta da vida, e não como a porta do nada'. 'de entrada' inserido; artigo trocado; abertura suprimida.
  - Verificação: **confirmed** — cite.py C&I cap. II: 3 divergências do original; apresentado como literal.
- **[media]** `wiki/conceitos/potencias-da-alma.md`:25 — ⚠ diferido a humano
  - Afirmação: 'a lei que Deus gravou no coração do homem' entre aspas atribuída a (LE, q. 621).
  - Evidência: q.621 responde só 'Na consciência'. A formulação 'gravou no coração' é de Romanos 2:15/ESE, não do LE.
  - Verificação: **confirmed** — cite.py: q.621 = 'Na consciência'; a frase entre aspas não é o texto de q.621.
- **[baixa]** `wiki/conceitos/morte.md`:66 — ✕ descartado (verificação refutou)
  - Afirmação: Ref de Joanna de Ângelis ao diálogo de Sócrates dá '(ESE, Introdução)'.
  - Evidência: O agente alegou que o locus real seria ESE cap. I item XI.
  - Verificação: **refuted** — As Máximas de Sócrates e Platão (itens I-XXI) ESTÃO na Introdução do ESE (seção IV), não no cap. I. A ref de Joanna está correta; o erro era do achado.
- **[baixa]** `wiki/conceitos/progresso-espiritual.md`:19 — ⚠ diferido a humano
  - Afirmação: 'uns avançaram mais depressa no livre exercício da vontade (LE, q. 115)'.
  - Evidência: q.115: o avanço mais rápido decorre da aceitação submissa das provas, não do 'livre exercício da vontade' (mais próximo de q.119).
  - Verificação: **confirmed** — cite.py: q.115 = aceitação submissa; 'livre exercício da vontade' não consta. Erro de ênfase doutrinária.

### Eixo 3 — Padrão editorial (5)

- **[media]** `wiki/conceitos/morte.md`:66 — ⚠ diferido a humano
  - Afirmação: 'reafirma o ancoramento kardequista'.
  - Evidência: 'kardequista' é forma proibida (data/terminologia.json derivados-de-kardec, auto_fix=false). Sentido é 'ancorado em Kardec' → 'de Kardec'. Correção contextual.
- **[baixa]** `wiki/conceitos/harmonia-das-esferas.md`:23 — ⚠ diferido a humano
  - Afirmação: 'harpa cósmica' e 'degraus harmônicos' entre aspas sugerem literal de Léon Denis.
  - Evidência: Fonte: 'imensa harpa cujos planetas representam as cordas' e '320 degraus ou ondas harmônicas'. As formulações entre aspas são cunhagem da página. De-quote ou citar literal.
- **[baixa]** `wiki/conceitos/morte.md`:39 — ⚠ diferido a humano
  - Afirmação: 'não se aprende diante da morte'.
  - Evidência: O cap. é 'Da apreensão diante da morte'; verbo correto 'apreende'. 'aprende' inverte o sentido.
- **[baixa]** `wiki/conceitos/parabola-do-semeador.md`:35 — ⚠ diferido a humano
  - Afirmação: Estrutura com seções extras ('Texto da parábola', 'Na palestra de Carlos Mendonça'); sem 'Desdobramentos'.
  - Evidência: convencoes-frontmatter.md.
- **[baixa]** `wiki/conceitos/progresso-espiritual.md`:11 — ⚠ diferido a humano
  - Afirmação: Estrutura com cabeçalhos próprios; sem 'Ensino de Kardec'/'Aplicação prática'/'Divergências'.
  - Evidência: convencoes-frontmatter.md.

### Eixo 4 — Tags e cross-references (3)

- **[baixa]** `wiki/conceitos/morte.md`:4 — ⚠ diferido a humano
  - Afirmação: Só tema/vida-futura; desenvolve o mecanismo perispiritual da separação.
  - Evidência: Seções 'Separação alma-corpo' e 'Mecanismo fluídico'. Avaliar tema/encarnacao.
- **[baixa]** `wiki/conceitos/potencias-da-alma.md`:4 — ✓ auto-corrigido
  - Afirmação: Trata vontade/consciência/livre-arbítrio mas só tema/encarnacao.
  - Evidência: Seção 'Livre-arbítrio' + LE q.843-872. tema/livre-arbitrio cabe.
  - Ação: `add-tag` — Adicionada tag tema/livre-arbitrio (passa de 1 para 2 tema/*).
- **[baixa]** `wiki/conceitos/progresso-espiritual.md`:4 — ✓ auto-corrigido
  - Afirmação: Progresso como motivo da encarnação / progressão dos mundos, mas só tema/historia-doutrina.
  - Evidência: Linhas 13,33 (ESE cap. III itens 3-5).
  - Ação: `add-tag` — Adicionada tag tema/encarnacao (aditiva).

## 4. Mudanças auto-aplicadas

- `wiki/conceitos/potencias-da-alma.md`:4 — `add-tag`: Adicionada tag tema/livre-arbitrio (passa de 1 para 2 tema/*).
- `wiki/conceitos/progresso-espiritual.md`:4 — `add-tag`: Adicionada tag tema/encarnacao (aditiva).

## 5. Diferidos a decisão humana

> Páginas marcadas `status: rascunho`; itens anotados no ROADMAP.md §11.

- `wiki/conceitos/harmonia-das-esferas.md` (eixo 3, baixa) — 'harpa cósmica' e 'degraus harmônicos' entre aspas sugerem literal de Léon Denis.
- `wiki/conceitos/morte.md` (eixo 2, media) — 'ela é uma porta de entrada na vida, e não como a porta do nada' (C&I, 1ª parte, cap. II).
- `wiki/conceitos/morte.md` (eixo 3, baixa) — 'não se aprende diante da morte'.
- `wiki/conceitos/morte.md` (eixo 3, media) — 'reafirma o ancoramento kardequista'.
- `wiki/conceitos/morte.md` (eixo 4, baixa) — Só tema/vida-futura; desenvolve o mecanismo perispiritual da separação.
- `wiki/conceitos/parabola-do-semeador.md` (eixo 2, alta) — 'a condenação do egoísmo, da indiferença, do amor das riquezas e da vaidade' entre aspas atribuída a (ESE, cap. XVII, item 6).
- `wiki/conceitos/parabola-do-semeador.md` (eixo 3, baixa) — Estrutura com seções extras ('Texto da parábola', 'Na palestra de Carlos Mendonça'); sem 'Desdobramentos'.
- `wiki/conceitos/potencias-da-alma.md` (eixo 2, alta) — 'Querendo, o Espírito atua sobre a matéria...' entre aspas atribuída a (LE, q. 459).
- `wiki/conceitos/potencias-da-alma.md` (eixo 2, alta) — 'A vontade cresce com o adiantamento moral... (LE, q. 635)'.
- `wiki/conceitos/potencias-da-alma.md` (eixo 2, media) — 'a lei que Deus gravou no coração do homem' entre aspas atribuída a (LE, q. 621).
- `wiki/conceitos/progresso-espiritual.md` (eixo 2, baixa) — 'uns avançaram mais depressa no livre exercício da vontade (LE, q. 115)'.
- `wiki/conceitos/progresso-espiritual.md` (eixo 3, baixa) — Estrutura com cabeçalhos próprios; sem 'Ensino de Kardec'/'Aplicação prática'/'Divergências'.

## 6. Resumo por página

### `wiki/conceitos/harmonia-das-esferas.md`
Sólida: 5 citações de Léon Denis e 3 do Pentateuco conferem; lint limpo. Único ponto: aspas em 2 paráfrases de Léon Denis.

### `wiki/conceitos/morte.md`
Citações do Pentateuco conferem; quote de C&I cap. II 'porta de entrada' não-literal; typo 'aprende'→'apreende'; 'kardequista' proibido; ref de Joanna DESCARTADA (correta).

### `wiki/conceitos/parabola-do-semeador.md`
Interpretação dos 4 terrenos sólida, mas frase 'condenação do egoísmo...' atribuída ao ESE cap. XVII item 6 é fabricada (grep zero); estrutura.

### `wiki/conceitos/potencias-da-alma.md`
Estrutura/Léon Denis sólidos; tag tema/livre-arbitrio aplicada; 3 citações ao LE (q.459/635/621) com loci que não sustentam a afirmação.

### `wiki/conceitos/progresso-espiritual.md`
Sólida: 7 citações do Pentateuco conferem; tag tema/encarnacao aplicada; 'livre exercício da vontade' ancorado em q.115 (que fala de aceitação submissa); estrutura.
