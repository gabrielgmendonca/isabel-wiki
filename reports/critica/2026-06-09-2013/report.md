# Relatório de crítica profunda — 2026-06-09

## 1. Metadados do run

- **Data:** 2026-06-09
- **Escopo:** `--limit 5`
- **Budget:** ~510k tokens (9 agentes)
- **Modelos:** critica=opus, verificacao=sonnet
- **Páginas devidas / criticadas / puladas:** 5 / 5 / 0
- **Total de achados:** 10 (4 auto, 6 diferidos, 0 descartados)

## 2. Páginas avaliadas

| Página | Tipo | Veredito | Achados | Auto | Diferidos |
|--------|------|----------|---------|------|-----------|
| `wiki/conceitos/espirito.md` | conceito | ⚠ 1 diferido | 1 | 0 | 1 |
| `wiki/conceitos/pluralidade-das-existencias.md` | conceito | ⚠ 2 diferidos | 2 | 0 | 2 |
| `wiki/conceitos/avareza.md` | conceito | ✓ 2 auto · ⚠ 1 diferido | 3 | 2 | 1 |
| `wiki/conceitos/ceu.md` | conceito | ✓ limpa | 0 | 0 | 0 |
| `wiki/conceitos/confianca-em-deus.md` | conceito | ✓ 2 auto · ⚠ 2 diferidos | 4 | 2 | 2 |

## 3. Achados por eixo

### Eixo 2 — Citações (4)

- **[alta]** `wiki/conceitos/pluralidade-das-existencias.md`:25 — ⚠ diferido a humano
  - Afirmação: Afirma 'Pitágoras a ensinou, e antes dele os druidas', atribuindo a (LE, q. 222).
  - Evidência: LE q. 222 (livro-dos-espiritos.md:909-960) traça Pitágoras aos filósofos indianos e egípcios; NÃO menciona druidas. A associação druidas↔reencarnação é de Léon Denis (nível 3), não de Kardec.
  - Verificação: **confirmed** — cite.py retornou o texto integral de q. 222: nenhuma referência a druidas/celtas. A segunda parte da asserção não tem respaldo no locus citado.
- **[alta]** `wiki/conceitos/avareza.md`:17 — ⚠ diferido a humano
  - Afirmação: Apresenta entre aspas, como citação literal, 'A riqueza é um depósito cujo emprego Deus pedirá conta', atribuída a (ESE, cap. XVI, item 7).
  - Evidência: O item 7 ('Utilidade providencial da riqueza') NÃO contém essa frase; o tema depositário/contas é literal no item 13 (Fénelon, l.2647). A formulação entre aspas não é literal em nenhum item do cap. XVI.
  - Verificação: **confirmed** — Item 7 trata da riqueza como prova difícil; a frase não aparece. A ideia literal está no item 13 (Fénelon). Busca qmd não encontrou a formulação no corpus. Erro duplo: número de item errado + formatação como aspas literais quando é paráfrase.
- **[alta]** `wiki/conceitos/confianca-em-deus.md`:21 — ⚠ diferido a humano
  - Afirmação: Atribui a (ESE, cap. XXV, item 3) a frase 'Ter confiança na Providência é não se deixar abater pelas dificuldades da vida, é saber que Deus vela por todas as suas criaturas', como interpretação de Mateus 6:26.
  - Evidência: cite.py ESE cap. XXV item 3 (evangelho-segundo-o-espiritismo.md:4967-4972) retorna texto sobre a LEI DO TRABALHO; cap. XXV intitula-se 'Buscai e achareis' (Mateus 7:7). A frase não aparece em parte alguma do Pentateuco (grep zero ocorrências). Citação fabricada/deturpada.
  - Verificação: **confirmed** — cite.py retorna texto literal sobre a lei do trabalho; a frase atribuída não aparece nesse locus nem em qualquer parte do ESE (grep exaustivo: zero ocorrências). Locus válido estruturalmente, mas o texto-alvo é inexistente. Citação fabricada confirmada.
- **[baixa]** `wiki/conceitos/espirito.md`:13 — ⚠ diferido a humano
  - Afirmação: Apresenta como citação literal entre aspas (LE, q. 76): "...Povoam o Universo, fora do mundo material."
  - Evidência: cite.py LE q. 76 (livro-dos-espiritos.md:422-424) retorna: "Povoam o universo, fora o mundo material." — diverge em duas palavras: 'Universo' vs 'universo'; 'fora do mundo' vs 'fora o mundo'.
  - Verificação: **confirmed** — cite.py confirma as duas divergências; a citação está entre aspas, apresentando-se como transcrição literal. Sem base para refutar.

### Eixo 3 — Padrão editorial (2)

- **[media]** `wiki/conceitos/pluralidade-das-existencias.md`:11 — ⚠ diferido a humano
  - Afirmação: Página tipo conceito usa cabeçalhos próprios em vez da estrutura canônica.
  - Evidência: convencoes-frontmatter.md (Estrutura por tipo): conceitos/ → Definição · Ensino de Kardec · Desdobramentos · Aplicação prática · Divergências · Páginas relacionadas · Fontes. Faltam 'Ensino de Kardec', 'Desdobramentos', 'Aplicação prática', 'Divergências'.
- **[baixa]** `wiki/conceitos/confianca-em-deus.md`:13 — ⚠ diferido a humano
  - Afirmação: Página tipo conceito não segue plenamente a estrutura canônica: faltam 'Desdobramentos' e 'Divergências'.
  - Evidência: Headings presentes: intro, '## Ensino de Kardec', '## Aplicação prática', '## Páginas relacionadas', '## Fontes'. Ausentes 'Desdobramentos' e 'Divergências' (esta opcional sem tensão registrada).

### Eixo 4 — Tags e cross-references (4)

- **[baixa]** `wiki/conceitos/avareza.md`:11 — ✓ auto-corrigido
  - Afirmação: 'caridade' em prosa sem wikilink inline (página-conceito existe).
  - Evidência: Linha 11: 'contrária à lei de caridade'; alvo wiki/conceitos/caridade.md existe.
  - Ação: `add-wikilink` — Envolveu 'caridade' em [[wiki/conceitos/caridade|caridade]] na linha 11.
- **[baixa]** `wiki/conceitos/avareza.md`:11 — ✓ auto-corrigido
  - Afirmação: 'egoísmo' em prosa sem wikilink inline (página-conceito existe).
  - Evidência: Linha 11: 'a avareza é forma grave de egoísmo'; alvo wiki/conceitos/egoismo.md existe.
  - Ação: `add-wikilink` — Envolveu 'egoísmo' em [[wiki/conceitos/egoismo|egoísmo]] na linha 11.
- **[baixa]** `wiki/conceitos/confianca-em-deus.md`:11 — ✓ auto-corrigido
  - Afirmação: 'fé raciocinada' citada sem linkar à página-conceito existente.
  - Evidência: Linha 11: 'fé raciocinada aplicada às provas da vida' — existe wiki/conceitos/fe-raciocinada.md.
  - Ação: `add-wikilink` — Envolveu 'fé raciocinada' (linha 11) em wikilink para wiki/conceitos/fe-raciocinada.
- **[baixa]** `wiki/conceitos/confianca-em-deus.md`:17 — ✓ auto-corrigido
  - Afirmação: 'pluralidade das existências' citada sem linkar à página-conceito existente.
  - Evidência: Linha 17: 'a pluralidade das existências encontra razão para confiar' — existe wiki/conceitos/pluralidade-das-existencias.md.
  - Ação: `add-wikilink` — Envolveu 'pluralidade das existências' (linha 17) em wikilink para wiki/conceitos/pluralidade-das-existencias.

## 4. Mudanças auto-aplicadas

- `wiki/conceitos/avareza.md`:11 — `add-wikilink`: Envolveu 'caridade' em [[wiki/conceitos/caridade|caridade]] na linha 11.
- `wiki/conceitos/avareza.md`:11 — `add-wikilink`: Envolveu 'egoísmo' em [[wiki/conceitos/egoismo|egoísmo]] na linha 11.
- `wiki/conceitos/confianca-em-deus.md`:11 — `add-wikilink`: Envolveu 'fé raciocinada' (linha 11) em wikilink para wiki/conceitos/fe-raciocinada.
- `wiki/conceitos/confianca-em-deus.md`:17 — `add-wikilink`: Envolveu 'pluralidade das existências' (linha 17) em wikilink para wiki/conceitos/pluralidade-das-existencias.

## 5. Diferidos a decisão humana

> Páginas marcadas `status: rascunho`; itens anotados no ROADMAP.md §11.

- `wiki/conceitos/espirito.md` (eixo 2, baixa) — Apresenta como citação literal entre aspas (LE, q. 76): "...Povoam o Universo, fora do mundo material."
- `wiki/conceitos/pluralidade-das-existencias.md` (eixo 2, alta) — Afirma 'Pitágoras a ensinou, e antes dele os druidas', atribuindo a (LE, q. 222).
- `wiki/conceitos/pluralidade-das-existencias.md` (eixo 3, media) — Página tipo conceito usa cabeçalhos próprios em vez da estrutura canônica.
- `wiki/conceitos/avareza.md` (eixo 2, alta) — Apresenta entre aspas, como citação literal, 'A riqueza é um depósito cujo emprego Deus pedirá conta', atribuída a (ESE, cap. XVI, item 7).
- `wiki/conceitos/confianca-em-deus.md` (eixo 2, alta) — Atribui a (ESE, cap. XXV, item 3) a frase 'Ter confiança na Providência é não se deixar abater pelas dificuldades da vida, é saber que Deus vela por todas as suas criaturas', como interpretação de Mateus 6:26.
- `wiki/conceitos/confianca-em-deus.md` (eixo 3, baixa) — Página tipo conceito não segue plenamente a estrutura canônica: faltam 'Desdobramentos' e 'Divergências'.

## 6. Resumo por página

### `wiki/conceitos/espirito.md`
Doutrinariamente sólida; único achado é desvio menor de fidelidade na transcrição literal de LE q. 76 (duas palavras), diferido por tocar texto entre aspas.

### `wiki/conceitos/pluralidade-das-existencias.md`
Fiel ao núcleo do LE; frase 'antes dele os druidas' atribuída a (LE, q. 222) sem respaldo no locus (druidas são tese de Léon Denis); estrutura fora do template canônico de conceito.

### `wiki/conceitos/avareza.md`
Fiel ao Pentateuco; 2 wikilinks inline adicionados; frase entre aspas atribuída a (ESE, cap. XVI, item 7) que não a contém — texto literal é de Fénelon no item 13.

### `wiki/conceitos/ceu.md`
Fiel: 8 citações a C&I (1ª parte, cap. III, itens 5-18) conferidas via cite.py; lint zerado; sem divergências.

### `wiki/conceitos/confianca-em-deus.md`
Sólida no conjunto; 2 wikilinks inline adicionados; citação atribuída a (ESE, cap. XXV, item 3) é inexistente na obra (item 3 trata da lei do trabalho) — citação fabricada; estrutura incompleta.
