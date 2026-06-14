# Relatório de crítica profunda — 2026-06-09

## 1. Metadados do run

- **Data:** 2026-06-09
- **Escopo:** `--limit 5 (loop, lote 2)`
- **Budget:** ~788k tokens (16 agentes)
- **Modelos:** critica=opus, verificacao=sonnet
- **Páginas devidas / criticadas / puladas:** 5 / 5 / 0
- **Total de achados:** 20 (3 auto, 17 diferidos, 0 descartados)

## 2. Páginas avaliadas

| Página | Tipo | Veredito | Achados | Auto | Diferidos |
|--------|------|----------|---------|------|-----------|
| `wiki/conceitos/demonios.md` | conceito | ✓ 1 auto · ⚠ 2 diferidos | 3 | 1 | 2 |
| `wiki/conceitos/desapego-dos-bens-terrenos.md` | conceito | ⚠ 7 diferidos (eixo 2) | 7 | 0 | 7 |
| `wiki/conceitos/desligamento-do-espirito.md` | conceito | ✓ 1 auto · ⚠ 4 diferidos | 5 | 1 | 4 |
| `wiki/conceitos/emigracoes-e-imigracoes-dos-espiritos.md` | conceito | ✓ 1 auto · ⚠ 1 diferido | 2 | 1 | 1 |
| `wiki/conceitos/encarnacao.md` | conceito | ⚠ 3 diferidos | 3 | 0 | 3 |

## 3. Achados por eixo

### Eixo 2 — Citações (13)

- **[alta]** `wiki/conceitos/desapego-dos-bens-terrenos.md`:23 — ⚠ diferido a humano
  - Afirmação: 'Servir a Mamon é subordinar o pensamento...' entre aspas atribuída a (ESE, cap. XVI, item 2).
  - Evidência: Item 2 é a transcrição de Mateus 19:16-24 (mancebo rico), não comentário de Kardec; grep 'subordinar o pensamento' = zero. Frase inexistente no ESE.
  - Verificação: **confirmed** — cite.py exit 2; leitura direta confirma item 2 = Mateus 19; grep literal zero ocorrências. Citação fabricada atribuída a locus sem comentário de Kardec.
- **[alta]** `wiki/conceitos/desapego-dos-bens-terrenos.md`:23 — ⚠ diferido a humano
  - Afirmação: 'Verdadeira propriedade...' atribuída a (ESE, cap. XVI, item 8).
  - Evidência: Conteúdo é do item 9 (Pascal, 'A verdadeira propriedade'); item 8 trata da 'Desigualdade das riquezas'. Frase entre aspas é paráfrase.
  - Verificação: **confirmed** — Leitura direta l.2631-2638: item 8 = desigualdade; item 9 = 'O homem só possui em plena propriedade aquilo que lhe é dado levar deste mundo'. Duplo erro: locus + aspas sobre paráfrase.
- **[alta]** `wiki/conceitos/desapego-dos-bens-terrenos.md`:27 — ⚠ diferido a humano
  - Afirmação: Parábola de Lázaro + 'O rico... condenado a ver a felicidade dos outros enquanto padece' atribuída a (ESE, cap. XVI, item 7).
  - Evidência: Parábola de Lázaro = item 5 (Lucas 16:19-31); item 7 = comentário de Kardec sobre utilidade da riqueza. Frase entre aspas inexistente no ESE inteiro.
  - Verificação: **confirmed** — grep em 5496 linhas: zero para 'condenado a ver', 'felicidade dos outros', 'gozou de todos os bens'. Locus errado (7≠5) + frase inventada entre aspas.
- **[alta]** `wiki/conceitos/desapego-dos-bens-terrenos.md`:31 — ⚠ diferido a humano
  - Afirmação: Parábola dos talentos + 'O homem não é mais que um depositário...' atribuída a (ESE, cap. XVI, item 9).
  - Evidência: Parábola dos talentos = item 6 (Mateus 25); ideia depositário/contas é do item 13 (Fénelon); item 9 é 'A verdadeira propriedade' (Pascal).
  - Verificação: **confirmed** — Leitura direta l.2600-2664: item 9 = Pascal; item 13 = Fénelon ('Sendo o homem o depositário... contas severas lhe serão pedidas'); item 6 = parábola literal. Locus correto: item 13.
- **[alta]** `wiki/conceitos/desapego-dos-bens-terrenos.md`:35 — ⚠ diferido a humano
  - Afirmação: 'O emprego da fortuna é benefício ou malefício...' atribuída a (ESE, cap. XVI, item 10).
  - Evidência: Item 10 (M., Espírito protetor) trata de legitimidade dos bens; frase inexistente no ESE (grep 'benefício ou malefício' = zero). Tema está nos itens 11/13.
  - Verificação: **confirmed** — grep zero ocorrências de 'benefício ou malefício'. Item 10 não a contém; itens 11/13 têm frases próximas mas não a citada. Citação fabricada entre aspas no item errado.
- **[alta]** `wiki/conceitos/encarnacao.md`:32 — ⚠ diferido a humano
  - Afirmação: Necessidade/progresso/expiação atribuída a (ESE, cap. IV, itens 16-18).
  - Evidência: Itens 16-18 tratam de ressurreição/reencarnação e laços de família; o conteúdo (necessidade da encarnação) está no item 25 ('Necessidade da encarnação', S. Luís).
  - Verificação: **confirmed** — cite.py: itens 16-18 não tratam de necessidade/progresso. Item 25 é o locus correto. Não é paráfrase legítima — locus citado não contém o conteúdo.
- **[media]** `wiki/conceitos/demonios.md`:51 — ✓ auto-corrigido
  - Afirmação: Blockquote 'E em nome de Jesus Cristo...' atribuído a (C&I, 1ª parte, cap. IX, item 19).
  - Evidência: cite.py: a frase é verbatim do item 15 (ceu-e-inferno.md:1919-1944); o item 19 não a contém.
  - Ação: `replace-text` — Locus corrigido de 'cap. IX, item 19' para 'cap. IX, item 15' (typo confirmado por cite.py). Prosa da linha 49 (item 19) permanece correta.
- **[media]** `wiki/conceitos/desapego-dos-bens-terrenos.md`:39 — ⚠ diferido a humano
  - Afirmação: 'A miséria e a riqueza são provas igualmente difíceis' (LE, q. 814).
  - Evidência: q. 814: 'Para experimentá-los de modos diferentes... provas escolhidas pelos próprios Espíritos'. Aspas sobre paráfrase; 'igualmente difíceis' contradiz ESE cap. XVI item 7 (riqueza mais perigosa).
  - Verificação: **confirmed** — cite.py q.814 não diz 'igualmente difíceis'; ESE item 7 diz riqueza 'mais perigosa do que a miséria'. Sentido distorcido, não resumido.
- **[media]** `wiki/conceitos/desapego-dos-bens-terrenos.md`:39 — ⚠ diferido a humano
  - Afirmação: 'A desigualdade de riquezas é consequência da diversidade de inteligências e aptidões dos Espíritos' (LE, q. 806).
  - Evidência: q. 806: 'É lei da natureza a desigualdade das condições sociais? Não; é obra do homem'. O argumento por inteligência/aptidão é do ESE cap. XVI item 8.
  - Verificação: **confirmed** — cite.py q.806 trata de 'condições sociais' (obra do homem), não de riquezas por inteligência. Locus correto: ESE cap. XVI item 8.
- **[media]** `wiki/conceitos/desligamento-do-espirito.md`:21 — ✓ auto-corrigido
  - Afirmação: Variação do desprendimento pelo grau moral atribuída a (LE, q. 155; C&I, 1ª parte, cap. I).
  - Evidência: C&I 1ª parte cap. I é 'O futuro e o nada'; a afirmação é sustentada por C&I 2ª parte cap. I 'A passagem' itens 8-13.
  - Ação: `replace-text` — (C&I, 1ª parte, cap. I) → (C&I, 2ª parte, cap. I); novo locus sustenta literalmente a afirmação.
- **[media]** `wiki/conceitos/desligamento-do-espirito.md`:29 — ⚠ diferido a humano
  - Afirmação: Morte violenta → desligamento mais difícil atribuído também a (LM, 2ª parte, cap. I).
  - Evidência: LM 2ª parte cap. I é 'Da ação dos Espíritos sobre a matéria', não trata de morte violenta. Sustentado por LE q. 161-162 e C&I 2ª parte cap. I item 12.
  - Verificação: **confirmed** — LM 2ª parte cap. I (livro-dos-mediuns.md:1316-1507) lido integralmente: nenhuma referência a morte violenta. Remover ou trocar por C&I 2ª parte cap. I item 12.
- **[media]** `wiki/conceitos/desligamento-do-espirito.md`:17 — ⚠ diferido a humano
  - Afirmação: Frase entre aspas como literal de LE q. 155: 'por um desprendimento que se efetua mais ou menos lentamente, segundo os indivíduos e as circunstâncias'.
  - Evidência: Texto literal de q. 155: 'se opera gradualmente e com uma lentidão muito variável conforme os indivíduos'. 'e as circunstâncias' é acréscimo inexistente.
  - Verificação: **confirmed** — cite.py q.155 difere em redação; 'e as circunstâncias' não consta. Locus válido, mas aspas configuram citação direta falsa.
- **[media]** `wiki/conceitos/encarnacao.md`:34 — ⚠ diferido a humano
  - Afirmação: 'Limites da encarnação... não é eterna nem ilimitada em número' ancorado genericamente em (ESE, cap. IV).
  - Evidência: Item 24 'Limites da encarnação': 'carece de limites precisamente traçados'. Item 25: a reencarnação pode prolongar-se indefinidamente. 'não ilimitada em número' contradiz o texto.
  - Verificação: **confirmed** — cite.py: item 24 = sem limites fixos; item 25 = pode prolongar-se indefinidamente. A página afirma o oposto. Só 'não é eterna' é sustentado (estado transitório).

### Eixo 3 — Padrão editorial (3)

- **[baixa]** `wiki/conceitos/demonios.md`:35 — ⚠ diferido a humano
  - Afirmação: Falta seção '## Divergências' do template de conceito.
  - Evidência: convencoes-frontmatter.md. Página trata a tensão Igreja×Espiritismo dentro de '## Ensino de Kardec'.
- **[baixa]** `wiki/conceitos/desligamento-do-espirito.md`:46 — ⚠ diferido a humano
  - Afirmação: Fontes lista C&I '1ª parte, cap. I' que deixou de ser usada após o auto-fix.
  - Evidência: Após corrigir o corpo para 2ª parte cap. I, '1ª parte, cap. I' (O futuro e o nada) não corresponde a nenhuma citação do corpo.
- **[baixa]** `wiki/conceitos/encarnacao.md`:11 — ⚠ diferido a humano
  - Afirmação: Estrutura de seções fora do template de conceito.
  - Evidência: Usa Definição · Objetivo · Necessidade universal · Diferenças... sem 'Ensino de Kardec', 'Aplicação prática', 'Divergências'. convencoes-frontmatter.md.

### Eixo 4 — Tags e cross-references (4)

- **[baixa]** `wiki/conceitos/demonios.md`:4 — ⚠ diferido a humano
  - Afirmação: Só tema/espiritos; conteúdo de céu/inferno/penas atravessa tema/vida-futura.
  - Evidência: Prosa trata inferno, fogo eterno, penas eternas; convencoes-tags.md permite 1-3 tema/*.
- **[baixa]** `wiki/conceitos/desligamento-do-espirito.md`:4 — ⚠ diferido a humano
  - Afirmação: Só tema/vida-futura; trata perispírito/laço perispiritual (tema/encarnacao).
  - Evidência: Corpo desenvolve o perispírito como laço; convenção permite 1-3 tema/*.
- **[baixa]** `wiki/conceitos/emigracoes-e-imigracoes-dos-espiritos.md`:31 — ✓ auto-corrigido
  - Afirmação: Primeira menção de 'raça adâmica' sem wikilink (página existe).
  - Evidência: Linha 31: '(Gênese, cap. XI, item 38)'; alvo wiki/conceitos/raca-adamica.md existe.
  - Ação: `add-wikilink` — Envolvida a primeira ocorrência de 'raça adâmica' (linha 31) em [[wiki/conceitos/raca-adamica|raça adâmica]].
- **[baixa]** `wiki/conceitos/emigracoes-e-imigracoes-dos-espiritos.md`:4 — ⚠ diferido a humano
  - Afirmação: Só tema/espiritos; conteúdo atravessa tema/encarnacao e tema/vida-futura.
  - Evidência: Reencarnação 'sustenta todo o fluxo migratório'; progressão planetária dos Espíritos. Convenção permite 1-3 tema/*.

## 4. Mudanças auto-aplicadas

- `wiki/conceitos/demonios.md`:51 — `replace-text`: Locus corrigido de 'cap. IX, item 19' para 'cap. IX, item 15' (typo confirmado por cite.py). Prosa da linha 49 (item 19) permanece correta.
- `wiki/conceitos/desligamento-do-espirito.md`:21 — `replace-text`: (C&I, 1ª parte, cap. I) → (C&I, 2ª parte, cap. I); novo locus sustenta literalmente a afirmação.
- `wiki/conceitos/emigracoes-e-imigracoes-dos-espiritos.md`:31 — `add-wikilink`: Envolvida a primeira ocorrência de 'raça adâmica' (linha 31) em [[wiki/conceitos/raca-adamica|raça adâmica]].

## 5. Diferidos a decisão humana

> Páginas marcadas `status: rascunho`; itens anotados no ROADMAP.md §11.

- `wiki/conceitos/demonios.md` (eixo 3, baixa) — Falta seção '## Divergências' do template de conceito.
- `wiki/conceitos/demonios.md` (eixo 4, baixa) — Só tema/espiritos; conteúdo de céu/inferno/penas atravessa tema/vida-futura.
- `wiki/conceitos/desapego-dos-bens-terrenos.md` (eixo 2, alta) — 'Servir a Mamon é subordinar o pensamento...' entre aspas atribuída a (ESE, cap. XVI, item 2).
- `wiki/conceitos/desapego-dos-bens-terrenos.md` (eixo 2, alta) — 'Verdadeira propriedade...' atribuída a (ESE, cap. XVI, item 8).
- `wiki/conceitos/desapego-dos-bens-terrenos.md` (eixo 2, alta) — Parábola de Lázaro + 'O rico... condenado a ver a felicidade dos outros enquanto padece' atribuída a (ESE, cap. XVI, item 7).
- `wiki/conceitos/desapego-dos-bens-terrenos.md` (eixo 2, alta) — Parábola dos talentos + 'O homem não é mais que um depositário...' atribuída a (ESE, cap. XVI, item 9).
- `wiki/conceitos/desapego-dos-bens-terrenos.md` (eixo 2, alta) — 'O emprego da fortuna é benefício ou malefício...' atribuída a (ESE, cap. XVI, item 10).
- `wiki/conceitos/desapego-dos-bens-terrenos.md` (eixo 2, media) — 'A miséria e a riqueza são provas igualmente difíceis' (LE, q. 814).
- `wiki/conceitos/desapego-dos-bens-terrenos.md` (eixo 2, media) — 'A desigualdade de riquezas é consequência da diversidade de inteligências e aptidões dos Espíritos' (LE, q. 806).
- `wiki/conceitos/desligamento-do-espirito.md` (eixo 2, media) — Morte violenta → desligamento mais difícil atribuído também a (LM, 2ª parte, cap. I).
- `wiki/conceitos/desligamento-do-espirito.md` (eixo 2, media) — Frase entre aspas como literal de LE q. 155: 'por um desprendimento que se efetua mais ou menos lentamente, segundo os indivíduos e as circunstâncias'.
- `wiki/conceitos/desligamento-do-espirito.md` (eixo 3, baixa) — Fontes lista C&I '1ª parte, cap. I' que deixou de ser usada após o auto-fix.
- `wiki/conceitos/desligamento-do-espirito.md` (eixo 4, baixa) — Só tema/vida-futura; trata perispírito/laço perispiritual (tema/encarnacao).
- `wiki/conceitos/emigracoes-e-imigracoes-dos-espiritos.md` (eixo 4, baixa) — Só tema/espiritos; conteúdo atravessa tema/encarnacao e tema/vida-futura.
- `wiki/conceitos/encarnacao.md` (eixo 2, alta) — Necessidade/progresso/expiação atribuída a (ESE, cap. IV, itens 16-18).
- `wiki/conceitos/encarnacao.md` (eixo 2, media) — 'Limites da encarnação... não é eterna nem ilimitada em número' ancorado genericamente em (ESE, cap. IV).
- `wiki/conceitos/encarnacao.md` (eixo 3, baixa) — Estrutura de seções fora do template de conceito.

## 6. Resumo por página

### `wiki/conceitos/demonios.md`
Sólida; apresenta fielmente a refutação de Kardec à doutrina dos demônios (C&I cap. IX-X). Locus de blockquote corrigido (IX item 19→15). Diferidos editoriais (seção Divergências; segunda tag).

### `wiki/conceitos/desapego-dos-bens-terrenos.md`
Estruturalmente sã, mas problema sistemático de eixo 2: quase todas as 'citações' da seção Ensino de Kardec são paráfrases entre aspas como texto literal, vários loci errados. Precisa revisão humana.

### `wiki/conceitos/desligamento-do-espirito.md`
Fiel no conteúdo; locus C&I corrigido (1ª→2ª parte). Diferidos: LM 2ª parte cap. I não sustenta morte violenta; aspas não-literais em LE q. 155; Fontes desatualizadas; segunda tag.

### `wiki/conceitos/emigracoes-e-imigracoes-dos-espiritos.md`
Sólida: 5 citações ao Gênese cap. XI conferem; Emmanuel enquadrado como aprofundamento. Wikilink de raça adâmica adicionado; diferido apenas segunda tag (ambíguo).

### `wiki/conceitos/encarnacao.md`
Fiel ao Pentateuco (q. 132/133/223), mas a seção 'No ESE' cita itens 16-18 do cap. IV para conteúdo que vive nos itens 24-25; afirmação 'não ilimitada em número' contradiz item 25.
