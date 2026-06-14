# Relatório de crítica profunda — 2026-06-10

## 1. Metadados do run

- **Data:** 2026-06-10
- **Escopo:** `--limit 5 (loop, lote 9)`
- **Budget:** ~968k tokens (14 agentes)
- **Modelos:** critica=opus, verificacao=sonnet
- **Páginas devidas / criticadas / puladas:** 5 / 5 / 0
- **Total de achados:** 18 (5 auto, 12 diferidos, 1 descartados)

## 2. Páginas avaliadas

| Página | Tipo | Veredito | Achados | Auto | Diferidos |
|--------|------|----------|---------|------|-----------|
| `wiki/conceitos/verdadeiro-espirita.md` | conceito | ✓ 1 auto · ⚠ 3 dif · ✕ 1 desc | 5 | 1 | 3 |
| `wiki/conceitos/parabola-da-dracma-perdida.md` | conceito | ⚠ 2 diferidos | 2 | 0 | 2 |
| `wiki/conceitos/parabola-da-ovelha-perdida.md` | conceito | ✓ 2 auto · ⚠ 3 diferidos | 5 | 2 | 3 |
| `wiki/conceitos/parabola-da-rede.md` | conceito | ✓ 2 auto · ⚠ 2 diferidos | 4 | 2 | 2 |
| `wiki/conceitos/parabola-da-semente-que-cresce-por-si.md` | conceito | ⚠ 2 diferidos | 2 | 0 | 2 |

## 3. Achados por eixo

### Eixo 2 — Citações (9)

- **[alta]** `wiki/conceitos/verdadeiro-espirita.md`:53 — ⚠ diferido a humano
  - Afirmação: 'dá de si mesmo o mais formal desmentido' atribuída a (ESE, cap. XV, item 10).
  - Evidência: A frase 'o mais formal desmentido' é do cap. XXI item 10 (falsos profetas da erraticidade). Cap. XV item 10 trata de 'verdadeiro espírita = verdadeiro cristão'.
  - Verificação: **confirmed** — cite.py: locus E aplicação errados; reancorar em cap. XV item 10 (que sustenta a tese).
- **[alta]** `wiki/conceitos/verdadeiro-espirita.md`:53 — ⚠ diferido a humano
  - Afirmação: 'Fiz o bem que podia? Sacrifiquei algum interesse...' como literal de (LE, Conclusão, item III).
  - Evidência: Conclusão item III = polêmica contra materialismo. Autoexame é q.919, mas a frase não é literal nem lá.
  - Verificação: **confirmed** — cite.py: locus errado + paráfrase apresentada como literal; reapontar para q.919 e de-quote.
- **[alta]** `wiki/conceitos/parabola-da-dracma-perdida.md`:21 — ⚠ diferido a humano
  - Afirmação: Kardec trata as 3 parábolas de Lucas 15 no ESE cap. XI.
  - Evidência: Cap. XI = lei de amor (servo impiedoso, instruções dos Espíritos). grep 'dracma'/'ovelha perdida'/'Lucas 15' no ESE = 0. CLUSTER: replicado em ovelha-perdida e filho-prodigo.
  - Verificação: **confirmed** — cite.py + grep: ESE não comenta as parábolas de Lucas 15. Reescrever como leitura do estudante; corrigir o cluster.
- **[alta]** `wiki/conceitos/parabola-da-ovelha-perdida.md`:21 — ⚠ diferido a humano
  - Afirmação: Festejo pelo arrependido atribuído a (ESE, cap. XI, item 10).
  - Evidência: Item 10 = ditado de Sanson ('Amai bastante para serdes amados'). Locus real do bom Pastor/festejo: LE q.1009 (Lamennais).
  - Verificação: **confirmed** — cite.py: item 10 não trata a ovelha; substituir por (LE, q. 1009), já citado na própria página.
- **[alta]** `wiki/conceitos/parabola-da-ovelha-perdida.md`:21 — ⚠ diferido a humano
  - Afirmação: Kardec discute a parábola no cap. XVIII (cuidado com os 'pequeninos').
  - Evidência: Cap. XVIII = festim de bodas. Tema dos pequeninos (Mt 18) está no cap. VIII, não XVIII.
  - Verificação: **confirmed** — cite.py: cap. XVIII não trata a ovelha nem os pequeninos. Remover a atribuição.
- **[alta]** `wiki/conceitos/parabola-da-semente-que-cresce-por-si.md`:27 — ⚠ diferido a humano
  - Afirmação: Autopropagação do Espiritismo citando '(cf. ESE, cap. XVIII, item 2 — sobre o grão de mostarda e o fermento)'.
  - Evidência: Cap. XVIII item 2 = festim de bodas/hebreus. ESE não comenta mostarda/fermento (grep). Tese da autopropagação está na Introdução item VI. CLUSTER: parabola-do-grao-de-mostarda atribui a cap. XVIII item 5 (= porta estreita).
  - Verificação: **confirmed** — cite.py + grep: locus válido mas não sustenta; descritor 'grão de mostarda e fermento' é falso. Reancorar na Introdução item VI; corrigir o par.
- **[media]** `wiki/conceitos/parabola-da-rede.md`:21 — ⚠ diferido a humano
  - Afirmação: 'Kardec a trata em paralelo à parábola do joio e do trigo (ESE, cap. XVIII)'.
  - Evidência: Cap. XVIII = festim de bodas + casa sobre a rocha. ESE não trata o joio (só alusão no cap. XII). CLUSTER: mesmo erro em parabola-do-joio-e-do-trigo (cap. XVIII item 7 = casa sobre a rocha).
  - Verificação: **confirmed** — cite.py + grep: cap. XVIII não trata o joio. Ancorar a triagem em ESE cap. III item 13 + Gênese cap. XVIII (já citados).
- **[baixa]** `wiki/conceitos/verdadeiro-espirita.md`:24 — ✕ descartado (verificação refutou)
  - Afirmação: Citações da Viagem 1862 rotuladas 'Discurso I' sem numeração na fonte.
  - Evidência: O agente alegou ausência de numeração interna.
  - Verificação: **refuted** — O raw TEM **I**, **II**, **III** após o heading dos Discursos. 'Discurso I' é válido e o conteúdo é fiel. Só o subtítulo 'Questões pessoais e adversários' é adição editorial (detalhe bibliográfico, não eixo 2).
- **[baixa]** `wiki/conceitos/parabola-da-rede.md`:28 — ⚠ diferido a humano
  - Afirmação: 'anjos ceifeiros' como organizadores da triagem com (C&I, 1ª parte) genérico.
  - Evidência: Citação sem cap./item. 'ceifeiro' não aparece em C&I. Anjos = Espíritos adiantados é C&I 1ª parte cap. VIII item 13, mas não trata de ceifeiros.
  - Verificação: **confirmed** — cite.py: citação genérica demais para a afirmação interpretativa; precisar o locus ou substituir.

### Eixo 3 — Padrão editorial (1)

- **[media]** `wiki/conceitos/parabola-da-ovelha-perdida.md`:46 — ⚠ diferido a humano
  - Afirmação: Fontes lista 'caps. XI, XVIII'.
  - Evidência: Herda a imprecisão. Ajustar (remover cap. XVIII).

### Eixo 4 — Tags e cross-references (8)

- **[baixa]** `wiki/conceitos/verdadeiro-espirita.md`:43 — ✓ auto-corrigido
  - Afirmação: 'homem de bem' em negrito sem wikilink.
  - Evidência: Linha 43; página existe.
  - Ação: `add-wikilink` — Envolvido 'homem de bem' em [[wiki/conceitos/homem-de-bem|homem de bem]] (mantido o negrito).
- **[baixa]** `wiki/conceitos/verdadeiro-espirita.md`:4 — ⚠ diferido a humano
  - Afirmação: Só tema/moral; núcleo é a caridade prática.
  - Evidência: Avaliar tema/prece-caridade.
- **[baixa]** `wiki/conceitos/parabola-da-dracma-perdida.md`:4 — ⚠ diferido a humano
  - Afirmação: Só tema/jesus; Ensino de Kardec domina reencarnação/misericórdia eterna.
  - Evidência: LE q.1009; C&I cap. VII. Avaliar tema/vida-futura.
- **[baixa]** `wiki/conceitos/parabola-da-ovelha-perdida.md`:21 — ✓ auto-corrigido
  - Afirmação: 'arrependimento' sem wikilink.
  - Evidência: Linha 21; página existe.
  - Ação: `add-wikilink` — Envolveu 'arrependimento' em [[wiki/conceitos/arrependimento|arrependimento]].
- **[baixa]** `wiki/conceitos/parabola-da-ovelha-perdida.md`:23 — ✓ auto-corrigido
  - Afirmação: 'Pastor' sem wikilink ao conceito-irmão.
  - Evidência: Linha 23; wiki/conceitos/parabola-do-bom-pastor.md existe.
  - Ação: `add-wikilink` — Envolveu 'Pastor' em [[wiki/conceitos/parabola-do-bom-pastor|Pastor]].
- **[baixa]** `wiki/conceitos/parabola-da-rede.md`:4 — ✓ auto-corrigido
  - Afirmação: Transição planetária/realocação de Espíritos mas só tema/jesus.
  - Evidência: Seções sobre Terra passando a regenerador. Avaliar tema/vida-futura.
  - Ação: `add-tag` — Adicionada tag tema/vida-futura.
- **[baixa]** `wiki/conceitos/parabola-da-rede.md`:23 — ✓ auto-corrigido
  - Afirmação: 'transição planetária' nomeada sem wikilink na prosa.
  - Evidência: Linha 23; wiki/conceitos/transicao-planetaria existe.
  - Ação: `add-wikilink` — Envolveu 'transição planetária' em [[wiki/conceitos/transicao-planetaria]] na linha 23.
- **[baixa]** `wiki/conceitos/parabola-da-semente-que-cresce-por-si.md`:25 — ⚠ diferido a humano
  - Afirmação: 'lei do progresso'/'Progresso do Espírito' sem wikilink a progresso-espiritual.
  - Evidência: Página existe; a irmã grao-de-mostarda já linka. Adicionar em Páginas relacionadas.

## 4. Mudanças auto-aplicadas

- `wiki/conceitos/verdadeiro-espirita.md`:43 — `add-wikilink`: Envolvido 'homem de bem' em [[wiki/conceitos/homem-de-bem|homem de bem]] (mantido o negrito).
- `wiki/conceitos/parabola-da-ovelha-perdida.md`:21 — `add-wikilink`: Envolveu 'arrependimento' em [[wiki/conceitos/arrependimento|arrependimento]].
- `wiki/conceitos/parabola-da-ovelha-perdida.md`:23 — `add-wikilink`: Envolveu 'Pastor' em [[wiki/conceitos/parabola-do-bom-pastor|Pastor]].
- `wiki/conceitos/parabola-da-rede.md`:4 — `add-tag`: Adicionada tag tema/vida-futura.
- `wiki/conceitos/parabola-da-rede.md`:23 — `add-wikilink`: Envolveu 'transição planetária' em [[wiki/conceitos/transicao-planetaria]] na linha 23.

## 5. Diferidos a decisão humana

> Páginas marcadas `status: rascunho`; itens anotados no ROADMAP.md §11.

- `wiki/conceitos/verdadeiro-espirita.md` (eixo 2, alta) — 'dá de si mesmo o mais formal desmentido' atribuída a (ESE, cap. XV, item 10).
- `wiki/conceitos/verdadeiro-espirita.md` (eixo 2, alta) — 'Fiz o bem que podia? Sacrifiquei algum interesse...' como literal de (LE, Conclusão, item III).
- `wiki/conceitos/verdadeiro-espirita.md` (eixo 4, baixa) — Só tema/moral; núcleo é a caridade prática.
- `wiki/conceitos/parabola-da-dracma-perdida.md` (eixo 2, alta) — Kardec trata as 3 parábolas de Lucas 15 no ESE cap. XI.
- `wiki/conceitos/parabola-da-dracma-perdida.md` (eixo 4, baixa) — Só tema/jesus; Ensino de Kardec domina reencarnação/misericórdia eterna.
- `wiki/conceitos/parabola-da-ovelha-perdida.md` (eixo 2, alta) — Festejo pelo arrependido atribuído a (ESE, cap. XI, item 10).
- `wiki/conceitos/parabola-da-ovelha-perdida.md` (eixo 2, alta) — Kardec discute a parábola no cap. XVIII (cuidado com os 'pequeninos').
- `wiki/conceitos/parabola-da-ovelha-perdida.md` (eixo 3, media) — Fontes lista 'caps. XI, XVIII'.
- `wiki/conceitos/parabola-da-rede.md` (eixo 2, media) — 'Kardec a trata em paralelo à parábola do joio e do trigo (ESE, cap. XVIII)'.
- `wiki/conceitos/parabola-da-rede.md` (eixo 2, baixa) — 'anjos ceifeiros' como organizadores da triagem com (C&I, 1ª parte) genérico.
- `wiki/conceitos/parabola-da-semente-que-cresce-por-si.md` (eixo 2, alta) — Autopropagação do Espiritismo citando '(cf. ESE, cap. XVIII, item 2 — sobre o grão de mostarda e o fermento)'.
- `wiki/conceitos/parabola-da-semente-que-cresce-por-si.md` (eixo 4, baixa) — 'lei do progresso'/'Progresso do Espírito' sem wikilink a progresso-espiritual.

## 6. Resumo por página

### `wiki/conceitos/verdadeiro-espirita.md`
Núcleo sólido (Viagem 1862 + ESE cap. XVII); wikilink homem-de-bem aplicado; 2 citações da 'Aplicação prática' com locus/quote errados ('o mais formal desmentido' = cap. XXI não XV; 'Fiz o bem que podia' não-literal); 'Discurso I' DESCARTADO (correto).

### `wiki/conceitos/parabola-da-dracma-perdida.md`
LE q.1009 e C&I cap. VII conferem, mas a tese de que Kardec trata as 3 parábolas de Lucas 15 no ESE cap. XI é falsa (cluster); tag opcional.

### `wiki/conceitos/parabola-da-ovelha-perdida.md`
Misericórdia bem ancorada (LE q.1009, C&I cap. VII); wikilinks arrependimento/Pastor; mas ESE cap. XI item 10 (= Sanson) e cap. XVIII (= festim) não tratam a ovelha perdida.

### `wiki/conceitos/parabola-da-rede.md`
Triagem bem ancorada (ESE cap. III item 13 + Gênese cap. XVIII); tag tema/vida-futura + wikilink transicao-planetaria; joio/trigo atribuído a ESE cap. XVIII (= festim); 'anjos ceifeiros' com C&I genérico.

### `wiki/conceitos/parabola-da-semente-que-cresce-por-si.md`
Leitura espírita sólida (Mc 4:26-29, LE q.776-800), mas autopropagação + 'grão de mostarda e fermento' atribuídos a ESE cap. XVIII item 2 (= festim); tese está na Introdução item VI.
