# Relatório de crítica profunda — 2026-06-09

## 1. Metadados do run

- **Data:** 2026-06-09
- **Escopo:** `--limit 5 (DRY-RUN — nenhuma página mutada)`
- **Budget:** verifyDepth=1; ~582k tokens; 10 agentes; 223s
- **Modelos:** critica=opus, verificacao=sonnet
- **Páginas devidas / criticadas / puladas:** 5 / 5 / 0
- **Total de achados:** 14 (2 auto, 12 diferidos, 0 descartados)

## 2. Páginas avaliadas

| Página | Tipo | Veredito | Achados | Auto | Diferidos |
|--------|------|----------|---------|------|-----------|
| `wiki/conceitos/espirito.md` | conceito | requer revisão humana | 2 | 0 | 2 |
| `wiki/conceitos/pluralidade-das-existencias.md` | conceito | requer revisão humana | 2 | 0 | 2 |
| `wiki/conceitos/avareza.md` | conceito | requer revisão humana | 2 | 0 | 2 |
| `wiki/conceitos/ceu.md` | conceito | requer revisão humana | 4 | 1 | 3 |
| `wiki/conceitos/confianca-em-deus.md` | conceito | requer revisão humana | 4 | 1 | 3 |

## 3. Achados por eixo

### Eixo 2 — Citações (5)

- **[alta]** `wiki/conceitos/pluralidade-das-existencias.md`:25 — ⚠ diferido a humano
  - Afirmação: A página atribui a LE q. 222 a afirmação de que "Pitágoras a ensinou, e antes dele os druidas" o princípio da pluralidade das existências.
  - Evidência: LE q. 222 (raw/kardec/pentateuco/livro-dos-espiritos.md:909): "Pitágoras, como se sabe, não foi o autor do sistema da metempsicose; ele o colheu dos filósofos indianos e dos egípcios, que o tinham desde tempos imemoriais." Kardec nomeia indianos e egípcios, NUNCA druidas. A string "druida(s)" não ocorre em nenhum arquivo do Pentateuco (raw/kardec/pentateuco/*.md) — só aparece em Léon Denis e outros autores complementares.
  - Verificação: **confirmed** — cite.py para LE q. 222 retornou o texto literal completo (raw/kardec/pentateuco/livro-dos-espiritos.md:909-960): Kardec nomeia "filósofos indianos e dos egípcios" como predecessores de Pitágoras — druidas não aparecem em nenhum ponto do longo comentário de q. 222. Grep confirmou zero ocorrências de "druida" em todo o arquivo fonte do LE. A afirmação da página (linha 25) — "Pitágoras a ensinou, e antes dele os druidas (LE, q. 222)" — não encontra sustentação no locus citado. O locus é válido (q. 222 existe), mas o argumento que a página extrai dele é incompatível com o texto literal: a citação não sustenta a afirmação sobre druidas.
- **[alta]** `wiki/conceitos/confianca-em-deus.md`:21 — ⚠ diferido a humano
  - Afirmação: A página apresenta como citação literal de Kardec, atribuída a (ESE, cap. XXV, item 3): 'Ter confiança na Providência é não se deixar abater pelas dificuldades da vida, é saber que Deus vela por todas as suas criaturas'.
  - Evidência: cite.py ESE 'cap. XXV, item 3' (linhas 4967-4972) trata do TRABALHO, não da Providência: 'Se Deus houvesse isentado do trabalho do corpo o homem, seus membros se teriam atrofiado... Procura e acharás; trabalha e produzirás.' A frase entre aspas na página NÃO aparece em lugar nenhum do cap. XXV (linhas 4931-5107). A passagem real sobre a Providência está no item 7 (linha ~5040): 'Não se deve, portanto, ver, nessas palavras, mais do que uma poética alegoria da Providência, que nunca deixa ao abandono os que nela confiam, querendo, todavia, que esses, por seu lado, trabalhem.' Logo: (a) o locus está errado (item 3 → item 7) E (b) o texto entre aspas é paráfrase apresentada como citação literal — não é texto de Kardec. Não auto-corrigível: nenhum locus sustenta a frase entre aspas como está.
  - Verificação: **confirmed** — cite.py confirms both defects. (1) ESE cap. XXV, item 3 (lines 4967-4972) treats the law of work ("Se Deus houvesse isentado do trabalho do corpo o homem... Procura e acharás; trabalha e produzirás") — not Providence. (2) The phrase between quotation marks on the page ("Ter confiança na Providência é não se deixar abater pelas dificuldades da vida, é saber que Deus vela por todas as suas criaturas") is absent from the entire ESE raw file (grep returned no output). (3) The real Providence passage is item 7 (lines 5023-5047): "Não se deve, portanto, ver, nessas palavras, mais do que uma poética alegoria da Providência, que nunca deixa ao abandono os que nela confiam, querendo, todavia, que esses, por seu lado, trabalhem." The finding is fully sustained: wrong locus (item 3 → item 7) AND fabricated literal quote — the wiki page presents a paraphrase as a transcription of Kardec.
- **[media]** `wiki/conceitos/avareza.md`:17 — ⚠ diferido a humano
  - Afirmação: A página atribui a frase entre aspas "A riqueza é um depósito cujo emprego Deus pedirá conta" ao locus (ESE, cap. XVI, item 7), apresentando-a como citação literal de Kardec.
  - Evidência: cite.py ESE "cap. XVI": o item 7 ('Utilidade providencial da riqueza. Provas da riqueza e da miséria', linhas 2600-2664) trata da utilidade providencial da riqueza e NÃO contém a formulação 'depósito / Deus pedirá conta'. A frase entre aspas tampouco aparece literalmente em lugar algum do capítulo — é paráfrase. O ensino do homem como depositário a quem 'contas severas serão pedidas do emprego' está em ESE cap. XVI item 13 (Fénelon: 'Sendo o homem o depositário, o administrador dos bens que Deus lhe pôs nas mãos, contas severas lhe serão pedidas do emprego que lhes haja ele dado') e item 14 (Lacordaire: 'Sois depositários e não proprietários... tereis de prestar contas ao Senhor'). O item 11 traz 'Que fizeste, ecônomo infiel, dos bens que te confiei?'.
  - Verificação: **confirmed** — cite.py confirmou: ESE cap. XVI, item 7 (linhas 2624-2630) trata da "Utilidade providencial da riqueza. Provas da riqueza e da miséria" — Kardec argumenta que a riqueza é instrumento de progresso moral e prova; não contém a formulação "depósito / Deus pedirá conta" em lugar algum. A frase entre aspas da página ("A riqueza é um depósito cujo emprego Deus pedirá conta") é uma paráfrase sintética que não aparece verbatim em nenhum item do capítulo. O ensinamento real do homem como "depositário" a quem "contas severas serão pedidas do emprego" está nas Instruções dos Espíritos: item 13 (Fénelon, linha 2647): "Sendo o homem o depositário, o administrador dos bens que Deus lhe pôs nas mãos, contas severas lhe serão pedidas do emprego..." e item 14 (Lacordaire, linhas 2649-2660): "Sois depositários e não proprietários... tendes de justificar o emprego que lhes derdes". O achado se sustenta integralmente: (a) o locus citado (item 7) está errado — versa sobre outro tema; (b) a frase aparece entre aspas como se fosse citação literal de Kardec, quando é paráfrase de instruções de Espíritos nos itens 13-14; (c) não é paráfrase legítima (locus válido com sentido preservado), pois o locus apontado (item 7) trata de assunto diferente.
- **[media]** `wiki/conceitos/confianca-em-deus.md`:21 — ⚠ diferido a humano
  - Afirmação: A página apresenta como fala literal de Jesus (entre aspas) 'Olhai as aves do céu, que não semeiam nem colhem; contudo, vosso Pai celestial as alimenta' citando (S. Mateus, 6:26).
  - Evidência: No texto-fonte do ESE (cap. XXV, linha ~5009), a passagem é renderizada como 'Observai os pássaros do céu: não semeiam, não ceifam, nada guardam em celeiros; mas, vosso Pai celestial os alimenta', com a citação bíblica '(S. Mateus, 6:19 a 21 e 25 a 34.)'. A redação da página ('aves do céu... nem colhem... as alimenta') difere da redação do ESE e mistura aspeamento literal com locus pontual 6:26.
  - Verificação: **confirmed** — cite.py confirm: ESE cap. XXV, item 6 renders the passage as "Observai os pássaros do céu: não semeiam, não ceifam, nada guardam em celeiros; mas, vosso Pai celestial os alimenta" with locus (S. Mateus, 6:19 a 21 e 25 a 34.). The page presents as literal quoted speech "Olhai as aves do céu, que não semeiam nem colhem; contudo, vosso Pai celestial as alimenta" with locus (S. Mateus, 6:26). Three concrete divergences: (1) different Portuguese translation ("Olhai/aves/colhem" vs. "Observai/pássaros/ceifam"); (2) single-verse locus 6:26 vs. ESE's range 6:19-21 and 25-34; (3) the page does not signal it is quoting from a Bible translation independent of the ESE — the aspeamento presents it as if it were the canonical rendering. Paráfrase legítima defense does not apply because the page uses quotation marks implying literal transcription, and in the ESE context the correct attribution locus is the range, not 6:26 alone. The finding stands.
- **[baixa]** `wiki/conceitos/avareza.md`:22 — ⚠ diferido a humano
  - Afirmação: A página cita a parábola do rico insensato com a passagem entre aspas 'Insensato! esta noite te pedirão a tua alma' e o intervalo (S. Lucas, 12:16-21).
  - Evidência: Em ESE cap. XVI item 3 ('Preservar-se da avareza'), o texto é 'Que insensato és! Esta noite mesmo tomar-te-ão a alma' e o intervalo impresso por Kardec é S. LUCAS, 12:13 a 21 (não 12:16-21). A frase entre aspas na página é paráfrase, não transcrição literal.
  - Verificação: **confirmed** — cite.py falhou para "cap. XVI, item 3" por limitação de parsing do script, mas a leitura direta de raw/kardec/pentateuco/evangelho-segundo-o-espiritismo.md linha 2607-2611 confirma dois erros na página:

1. TEXTO LITERAL em ESE cap. XVI, item 3 (linha 2609): "Que insensato és! Esta noite mesmo tomar-te-ão a alma" — a página cita "Insensato! esta noite te pedirão a tua alma", que é paráfrase de tradução diferente, não o texto kardecista.

2. REFERÊNCIA BÍBLICA: Kardec imprime explicitamente "(S. LUCAS, 12:13 a 21)" (linha 2611). A página cita "S. Lucas, 12:16–21" — o versículo inicial está errado (13, não 16). O rico insensato interpela alguém a dividir a herança em 12:13, antes do versículo 16 da parábola; Kardec inclui esse contexto na citação.

Ambos os sub-achados do eixo 2 se sustentam: locus válido (ESE cap. XVI, item 3 "Preservar-se da avareza"), mas (a) a frase entre aspas é paráfrase e não transcrição literal kardecista, e (b) o intervalo bíblico na página está truncado no início.

### Eixo 3 — Padrão editorial (3)

- **[media]** `wiki/conceitos/pluralidade-das-existencias.md`:11 — ⚠ diferido a humano
  - Afirmação: Página tipo: conceito não segue a estrutura canônica de conceitos/ fixada em convencoes-frontmatter.md.
  - Evidência: Headings atuais: Definição · Relação com "reencarnação" · Antiguidade do princípio · Considerações adicionais (Cap. V) · Páginas relacionadas · Fontes. A convenção pede: Definição curta · Ensino de Kardec · Desdobramentos · Aplicação prática · Divergências · Páginas relacionadas · Fontes. Faltam, em particular, "Ensino de Kardec", "Aplicação prática" e "Divergências".
- **[baixa]** `wiki/conceitos/espirito.md`:17 — ⚠ diferido a humano
  - Afirmação: A página usa seções próprias (Definição · Origem e natureza · Envoltório: perispírito · Destino e progresso · No Livro dos Médiuns · Páginas relacionadas · Fontes) em vez do template canônico de conceito.
  - Evidência: convencoes-frontmatter.md fixa para conceitos/: 'Definição curta · Ensino de Kardec · Desdobramentos · Aplicação prática · Divergências · Páginas relacionadas · Fontes'. A página não traz 'Ensino de Kardec', 'Desdobramentos', 'Aplicação prática' nem 'Divergências'; usa headings temáticos próprios.
- **[baixa]** `wiki/conceitos/ceu.md`:13 — ⚠ diferido a humano
  - Afirmação: Estrutura de tipo:conceito incompleta — faltam as seções nominais 'Desdobramentos' e 'Divergências' previstas em convencoes-frontmatter.md.
  - Evidência: A página tem: intro (Definição) · ## Ensino de Kardec · ## Aplicação prática · ## Páginas relacionadas · ## Fontes. O conteúdo de 'Desdobramentos' está dobrado dentro de 'Ensino de Kardec'; não há seção '## Divergências' (não há divergência real a registrar, pois a fonte é o próprio Pentateuco C&I).

### Eixo 4 — Tags e cross-references (6)

- **[baixa]** `wiki/conceitos/espirito.md`:4 — ⚠ diferido a humano
  - Afirmação: A página carrega apenas um tema/* (tema/espiritos).
  - Evidência: tags: [..., tema/espiritos]. A convenção (convencoes-tags.md) permite 1-3 tema/*; o conteúdo trata fortemente de individualização do princípio inteligente e do perispírito, podendo tocar tema/encarnacao (perispírito/corpo).
- **[baixa]** `wiki/conceitos/ceu.md`:21 — ✓ auto-corrigido
  - Afirmação: A prosa menciona 'livre-arbítrio' (linha 21) sem linkar para a página-conceito existente wiki/conceitos/livre-arbitrio.md.
  - Evidência: Linha 21: 'Os Espíritos são criados simples e ignorantes, com aptidão para progredir em virtude de seu livre-arbítrio.' — fora de blockquote; página wiki/conceitos/livre-arbitrio.md existe.
  - Ação: `add-wikilink` — DRY-RUN — adicionaria wikilink [[wiki/conceitos/livre-arbitrio|livre-arbítrio]] na linha 21 (conceito existente nomeado em prosa). critica_apply rodou em modo dry-run (changed:false).
- **[baixa]** `wiki/conceitos/ceu.md`:37 — ⚠ diferido a humano
  - Afirmação: A seção 'Mundos superiores como etapas' (linhas 35-37) e a linha 45 discutem os mundos felizes/paraísos sem linkar para a página-conceito existente wiki/conceitos/mundos-felizes.md.
  - Evidência: Linha 41 (blockquote, não-linkável): 'os mundos felizes são as últimas estações que a ele conduzem'. Linha 37 (prosa): 'Esses mundos são "verdadeiros paraísos" e representam etapas no caminho do progresso'. A página linka pluralidade-dos-mundos-habitados em Páginas relacionadas, mas o texto fala de 'mundos superiores' (descritor relativo, ESE cap. III item 8), não nomeia literalmente a categoria canônica 'mundos felizes' em prosa fora de blockquote.
- **[baixa]** `wiki/conceitos/ceu.md`:4 — ⚠ diferido a humano
  - Afirmação: A página tem apenas um tema/* (tema/vida-futura), mas o conteúdo atravessa fortemente o eixo da encarnação/progresso (seções 'Progresso pelo trabalho e pela encarnação' e 'Mundos superiores como etapas').
  - Evidência: Frontmatter linha 4: tags incluem tema/vida-futura como único tema/*. Linhas 29-37 desenvolvem reencarnação, duplo progresso moral/intelectual e mundos superiores — eixo tema/encarnacao.
- **[baixa]** `wiki/conceitos/confianca-em-deus.md`:11 — ✓ auto-corrigido
  - Afirmação: A prosa nomeia 'fé raciocinada' (linha 11), conceito que já tem página própria existente (wiki/conceitos/fe-raciocinada.md), mas não a linka.
  - Evidência: Linha 11: '...a confiança em Deus não é resignação passiva, mas fé raciocinada aplicada às provas da vida.' — fe-raciocinada.md existe em wiki/conceitos/.
  - Ação: `add-wikilink` — DRY-RUN — adicionar wikilink em 'fé raciocinada' (linha 11) apontando para wiki/conceitos/fe-raciocinada: critica_apply.py add-wikilink --path wiki/conceitos/confianca-em-deus.md --line 11 --text "fé raciocinada" --target "wiki/conceitos/fe-raciocinada"
- **[baixa]** `wiki/conceitos/confianca-em-deus.md`:4 — ⚠ diferido a humano
  - Afirmação: A página tem apenas tema/deus, mas dedica seção própria ('Confiança e prece') à prece como expressão da confiança, com citação (ESE, cap. XXVII).
  - Evidência: Seção linhas 23-25 trata da prece (ESE cap. XXVII — 'Pedi e obtereis'); a convenção tema/* admite 1-3 eixos e tema/prece-caridade cobre 'adoração, prece, caridade prática'.

## 4. Mudanças auto-aplicadas

- `wiki/conceitos/ceu.md`:21 — `add-wikilink`: DRY-RUN — adicionaria wikilink [[wiki/conceitos/livre-arbitrio|livre-arbítrio]] na linha 21 (conceito existente nomeado em prosa). critica_apply rodou em modo dry-run (changed:false).
- `wiki/conceitos/confianca-em-deus.md`:11 — `add-wikilink`: DRY-RUN — adicionar wikilink em 'fé raciocinada' (linha 11) apontando para wiki/conceitos/fe-raciocinada: critica_apply.py add-wikilink --path wiki/conceitos/confianca-em-deus.md --line 11 --text "fé raciocinada" --target "wiki/conceitos/fe-raciocinada"

## 5. Diferidos a decisão humana

> Páginas marcadas `status: rascunho`; itens anotados no ROADMAP.md §11.

- `wiki/conceitos/espirito.md` (eixo 3, baixa) — A página usa seções próprias (Definição · Origem e natureza · Envoltório: perispírito · Destino e progresso · No Livro dos Médiuns · Páginas relacionadas · Fontes) em vez do template canônico de conceito.
- `wiki/conceitos/espirito.md` (eixo 4, baixa) — A página carrega apenas um tema/* (tema/espiritos).
- `wiki/conceitos/pluralidade-das-existencias.md` (eixo 2, alta) — A página atribui a LE q. 222 a afirmação de que "Pitágoras a ensinou, e antes dele os druidas" o princípio da pluralidade das existências.
- `wiki/conceitos/pluralidade-das-existencias.md` (eixo 3, media) — Página tipo: conceito não segue a estrutura canônica de conceitos/ fixada em convencoes-frontmatter.md.
- `wiki/conceitos/avareza.md` (eixo 2, media) — A página atribui a frase entre aspas "A riqueza é um depósito cujo emprego Deus pedirá conta" ao locus (ESE, cap. XVI, item 7), apresentando-a como citação literal de Kardec.
- `wiki/conceitos/avareza.md` (eixo 2, baixa) — A página cita a parábola do rico insensato com a passagem entre aspas 'Insensato! esta noite te pedirão a tua alma' e o intervalo (S. Lucas, 12:16-21).
- `wiki/conceitos/ceu.md` (eixo 4, baixa) — A seção 'Mundos superiores como etapas' (linhas 35-37) e a linha 45 discutem os mundos felizes/paraísos sem linkar para a página-conceito existente wiki/conceitos/mundos-felizes.md.
- `wiki/conceitos/ceu.md` (eixo 3, baixa) — Estrutura de tipo:conceito incompleta — faltam as seções nominais 'Desdobramentos' e 'Divergências' previstas em convencoes-frontmatter.md.
- `wiki/conceitos/ceu.md` (eixo 4, baixa) — A página tem apenas um tema/* (tema/vida-futura), mas o conteúdo atravessa fortemente o eixo da encarnação/progresso (seções 'Progresso pelo trabalho e pela encarnação' e 'Mundos superiores como etapas').
- `wiki/conceitos/confianca-em-deus.md` (eixo 2, alta) — A página apresenta como citação literal de Kardec, atribuída a (ESE, cap. XXV, item 3): 'Ter confiança na Providência é não se deixar abater pelas dificuldades da vida, é saber que Deus vela por todas as suas criaturas'.
- `wiki/conceitos/confianca-em-deus.md` (eixo 2, media) — A página apresenta como fala literal de Jesus (entre aspas) 'Olhai as aves do céu, que não semeiam nem colhem; contudo, vosso Pai celestial as alimenta' citando (S. Mateus, 6:26).
- `wiki/conceitos/confianca-em-deus.md` (eixo 4, baixa) — A página tem apenas tema/deus, mas dedica seção própria ('Confiança e prece') à prece como expressão da confiança, com citação (ESE, cap. XXVII).

## 6. Resumo por página

### `wiki/conceitos/espirito.md`
Página doutrinariamente sólida: todas as citações ao Pentateuco (LE q.76/79/82/115/118) e ao LM (itens 1-2-3, 74, 133) foram verificadas literalmente e sustentam as afirmações; lint limpo; único ponto a rever é o desvio editorial das seções em relação ao template canônico de conceito.

### `wiki/conceitos/pluralidade-das-existencias.md`
Página doutrinariamente quase sólida (lint 100% limpo, citação estrutural de q.166-222 e Caps. IV-V correta), mas contém uma deturpação de citação: atribui a LE q. 222 a menção aos \"druidas\", quando Kardec nomeia indianos e egípcios e druidas não ocorrem em todo o Pentateuco.

### `wiki/conceitos/avareza.md`
A página de avareza é doutrinariamente sólida e bem ancorada no ensino de Kardec (depósito dos bens, desapego sem miséria, lei de caridade), mas tem duas imprecisões de citação no eixo 2: o locus (ESE, cap. XVI, item 7) não sustenta a frase entre aspas sobre 'depósito de que Deus pedirá conta' (que pertence aos itens 13-14, e ainda assim é paráfrase, não literal), e a transcrição da parábola do rico insensato é parafraseada com intervalo de versículos divergente — ambas diferidas por mudarem atribuição/precisão de citações apresentadas como literais.

### `wiki/conceitos/ceu.md`
Página doutrinariamente sólida: todas as citações a C&I 1ª parte cap. III conferem com o texto literal (verificadas via cite.py), sem divergências a registrar; ajustes apenas de cross-reference.

### `wiki/conceitos/confianca-em-deus.md`
Página doutrinariamente sólida no enquadramento (confiança = fé raciocinada, não fatalismo nem superstição), mas contém uma citação deturpada de alta gravidade: a frase entre aspas atribuída a (ESE, cap. XXV, item 3) não é texto literal de Kardec e o locus está errado (a passagem real sobre a Providência está no item 7) — exige correção humana.
