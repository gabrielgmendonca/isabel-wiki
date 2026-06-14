# Relatório de crítica profunda — 2026-06-10

## 1. Metadados do run

- **Data:** 2026-06-10
- **Escopo:** `--limit 5 (loop, lote 6 — último)`
- **Budget:** ~617k tokens (9 agentes)
- **Modelos:** critica=opus, verificacao=sonnet
- **Páginas devidas / criticadas / puladas:** 5 / 5 / 0
- **Total de achados:** 18 (7 auto, 10 diferidos, 1 descartados)

## 2. Páginas avaliadas

| Página | Tipo | Veredito | Achados | Auto | Diferidos |
|--------|------|----------|---------|------|-----------|
| `wiki/conceitos/principio-vital.md` | conceito | ⚠ 1 diferido | 1 | 0 | 1 |
| `wiki/conceitos/proibicao-de-evocar-os-mortos.md` | conceito | ✓ 1 auto · ⚠ 2 diferidos | 3 | 1 | 2 |
| `wiki/conceitos/psicografia.md` | conceito | ✓ 1 auto · ⚠ 2 dif · ✕ 1 desc | 4 | 1 | 2 |
| `wiki/conceitos/purgatorio.md` | conceito | ✓ 3 auto · ⚠ 1 diferido | 4 | 3 | 1 |
| `wiki/conceitos/raca-adamica.md` | conceito | ✓ 2 auto · ⚠ 4 diferidos | 6 | 2 | 4 |

## 3. Achados por eixo

### Eixo 2 — Citações (5)

- **[alta]** `wiki/conceitos/raca-adamica.md`:23 — ⚠ diferido a humano
  - Afirmação: Blockquote (RE mar/1860) abre com 'Para nós é evidente que as raças primitivas da Terra provêm de origens diferentes' como literal.
  - Evidência: A frase não consta no artigo (grep zero). Só a 2ª metade ('Adão... há 6000 anos') é verbatim.
  - Verificação: **confirmed** — grep 'Para nós'/'raças primitivas'/'evidente' = zero no 03-marco.md. Aspas + [...] criam falsa aparência de citação contínua literal.
- **[media]** `wiki/conceitos/raca-adamica.md`:94 — ✓ auto-corrigido
  - Afirmação: Fontes aponta 'Os pré-adamitas' (mar/1860) para o raw de janeiro.
  - Evidência: O artigo está em revista-espirita/1860/03-marco.md; o link apontava para 01-janeiro.
  - Ação: `replace-text` — Link Edição corrigido de 01-janeiro para 03-marco (typo de locus confirmado pela fonte).
- **[media]** `wiki/conceitos/raca-adamica.md`:70 — ⚠ diferido a humano
  - Afirmação: Blockquote (A Caminho da Luz cap. 3) abre com 'Aqueles seres angustiados e aflitos'.
  - Evidência: Fonte: 'Aqueles seres desolados e aflitos'. Troca de 'desolados' por 'angustiados' dentro de aspas.
  - Verificação: **confirmed** — a-caminho-da-luz.md:120 diz 'desolados'. Resto verbatim. Palavra trocada dentro de citação literal.
- **[baixa]** `wiki/conceitos/proibicao-de-evocar-os-mortos.md`:23 — ⚠ diferido a humano
  - Afirmação: Cita (C&I, 1ª parte, cap. XI, item 4) para dois exemplos (boi do Êxodo + sacerdotes).
  - Evidência: O boi do Êxodo está no item 5; o item 4 = só sacerdotes. Trocar para 'itens 4-5'.
  - Verificação: **confirmed** — cite.py: boi no item 5 (l.2192-2194), sacerdotes no fim do item 4. Locus incompleto, não deturpação.
- **[baixa]** `wiki/conceitos/psicografia.md`:51 — ✕ descartado (verificação refutou)
  - Afirmação: 'critério recomendado por Kardec (LM, 2ª parte, cap. XXIV)' — distinção de Espíritos pelo estilo.
  - Evidência: O cap. XXIV (Da identidade dos Espíritos) de fato recomenda linguagem/estilo como critério.
  - Verificação: **refuted** — Leitura direta do cap. XXIV: §255/§258/§260 recomendam linguagem/estilo como critério de identidade. A afirmação é paráfrase legítima; o achado não se sustenta.

### Eixo 3 — Padrão editorial (3)

- **[media]** `wiki/conceitos/raca-adamica.md`:59 — ⚠ diferido a humano
  - Afirmação: 'Desenvolvimento por Emmanuel' (origem em Capela; raça adâmica = raças brancas) vai além de Kardec, sem seção Divergências.
  - Evidência: Gênese cap. XI item 39 distingue raças sem racializar a raça adâmica nem nomear o mundo de origem. Aprofundamento nível 3 não fixado por Kardec — avaliar callout/Divergências. slug: raca-adamica-identificacao-capela-emmanuel.
- **[baixa]** `wiki/conceitos/proibicao-de-evocar-os-mortos.md`:13 — ⚠ diferido a humano
  - Afirmação: Sem heading 'Definição'; seção 'Na Viagem Espírita em 1862' no lugar de Desdobramentos/Divergências.
  - Evidência: convencoes-frontmatter.md.
- **[baixa]** `wiki/conceitos/psicografia.md`:47 — ⚠ diferido a humano
  - Afirmação: 'Casos notáveis' no lugar de 'Desdobramentos'.
  - Evidência: convencoes-frontmatter.md.

### Eixo 4 — Tags e cross-references (10)

- **[baixa]** `wiki/conceitos/principio-vital.md`:19 — ⚠ diferido a humano
  - Afirmação: Prosa e tag pressupõem [[wiki/conceitos/fluido-vital]], que não existe.
  - Evidência: data/terminologia.json registra o slug; o arquivo está ausente. Criar a página (distinção princípio vital vs. fluido vital) ou remover o slug órfão.
- **[baixa]** `wiki/conceitos/proibicao-de-evocar-os-mortos.md`:4 — ✓ auto-corrigido
  - Afirmação: Trata extensamente de comunicação mediúnica mas só tinha tema/espiritos.
  - Evidência: Seções sobre evocação espírita vs. necromancia; material p/ palestras sobre mediunidade.
  - Ação: `add-tag` — Adicionada tag tema/mediunidade ao frontmatter.
- **[baixa]** `wiki/conceitos/psicografia.md`:41 — ✓ auto-corrigido
  - Afirmação: 'pneumatografia' em negrito sem wikilink (página existe).
  - Evidência: Linha 41; alvo wiki/conceitos/pneumatografia.md existe.
  - Ação: `add-wikilink` — Inseriu [[wiki/conceitos/pneumatografia|pneumatografia]] na linha 41.
- **[baixa]** `wiki/conceitos/psicografia.md`:4 — ⚠ diferido a humano
  - Afirmação: 'Casos notáveis' (Divaldo/Chico) mas só autor/kardec.
  - Evidência: Avaliar autor/divaldo-franco + autor/chico-xavier.
- **[baixa]** `wiki/conceitos/purgatorio.md`:4 — ✓ auto-corrigido
  - Afirmação: Só tema/vida-futura; 'Aplicação prática' gira sobre o sentido do sofrimento.
  - Evidência: Linha 51: 'palestras sobre o sentido do sofrimento'.
  - Ação: `add-tag` — Adicionada tag tema/sofrimento.
- **[baixa]** `wiki/conceitos/purgatorio.md`:4 — ✓ auto-corrigido
  - Afirmação: Discute livre-arbítrio/responsabilidade ('artífice de seu futuro').
  - Evidência: Linha 53 (C&I, 1ª parte, cap. V, item 6).
  - Ação: `add-tag` — Adicionada tag tema/livre-arbitrio.
- **[baixa]** `wiki/conceitos/purgatorio.md`:11 — ✓ auto-corrigido
  - Afirmação: 'mundo de expiação e provas' (forma canônica) sem wikilink.
  - Evidência: Linha 11; página wiki/conceitos/mundos-de-expiacao-e-provas existe.
  - Ação: `add-wikilink` — Envolvido 'mundo de expiação e provas' em wikilink para wiki/conceitos/mundos-de-expiacao-e-provas.
- **[baixa]** `wiki/conceitos/purgatorio.md`:11 — ⚠ diferido a humano
  - Afirmação: 'expiação' central na prosa/tag mas sem link a wiki/conceitos/expiacao.
  - Evidência: A página wiki/conceitos/expiacao existe. Adicionar em Páginas relacionadas.
- **[baixa]** `wiki/conceitos/raca-adamica.md`:4 — ✓ auto-corrigido
  - Afirmação: Só tema/historia-doutrina; conteúdo trata natureza/migração dos Espíritos.
  - Evidência: Seções sobre anjos decaídos, Espíritos exilados, escala (RE jan/1862, A Caminho da Luz cap. 3).
  - Ação: `add-tag` — Adicionado tema/espiritos ao frontmatter.
- **[baixa]** `wiki/conceitos/raca-adamica.md`:27 — ⚠ diferido a humano
  - Afirmação: 'anjos decaídos' central sem wikilink a [[wiki/conceitos/anjos]].
  - Evidência: Termo só em títulos/quotes; exige tocar prosa.

## 4. Mudanças auto-aplicadas

- `wiki/conceitos/proibicao-de-evocar-os-mortos.md`:4 — `add-tag`: Adicionada tag tema/mediunidade ao frontmatter.
- `wiki/conceitos/psicografia.md`:41 — `add-wikilink`: Inseriu [[wiki/conceitos/pneumatografia|pneumatografia]] na linha 41.
- `wiki/conceitos/purgatorio.md`:4 — `add-tag`: Adicionada tag tema/sofrimento.
- `wiki/conceitos/purgatorio.md`:4 — `add-tag`: Adicionada tag tema/livre-arbitrio.
- `wiki/conceitos/purgatorio.md`:11 — `add-wikilink`: Envolvido 'mundo de expiação e provas' em wikilink para wiki/conceitos/mundos-de-expiacao-e-provas.
- `wiki/conceitos/raca-adamica.md`:94 — `replace-text`: Link Edição corrigido de 01-janeiro para 03-marco (typo de locus confirmado pela fonte).
- `wiki/conceitos/raca-adamica.md`:4 — `add-tag`: Adicionado tema/espiritos ao frontmatter.

## 5. Diferidos a decisão humana

> Páginas marcadas `status: rascunho`; itens anotados no ROADMAP.md §11.

- `wiki/conceitos/principio-vital.md` (eixo 4, baixa) — Prosa e tag pressupõem [[wiki/conceitos/fluido-vital]], que não existe.
- `wiki/conceitos/proibicao-de-evocar-os-mortos.md` (eixo 2, baixa) — Cita (C&I, 1ª parte, cap. XI, item 4) para dois exemplos (boi do Êxodo + sacerdotes).
- `wiki/conceitos/proibicao-de-evocar-os-mortos.md` (eixo 3, baixa) — Sem heading 'Definição'; seção 'Na Viagem Espírita em 1862' no lugar de Desdobramentos/Divergências.
- `wiki/conceitos/psicografia.md` (eixo 4, baixa) — 'Casos notáveis' (Divaldo/Chico) mas só autor/kardec.
- `wiki/conceitos/psicografia.md` (eixo 3, baixa) — 'Casos notáveis' no lugar de 'Desdobramentos'.
- `wiki/conceitos/purgatorio.md` (eixo 4, baixa) — 'expiação' central na prosa/tag mas sem link a wiki/conceitos/expiacao.
- `wiki/conceitos/raca-adamica.md` (eixo 2, alta) — Blockquote (RE mar/1860) abre com 'Para nós é evidente que as raças primitivas da Terra provêm de origens diferentes' como literal.
- `wiki/conceitos/raca-adamica.md` (eixo 2, media) — Blockquote (A Caminho da Luz cap. 3) abre com 'Aqueles seres angustiados e aflitos'.
- `wiki/conceitos/raca-adamica.md` (eixo 3, media) — 'Desenvolvimento por Emmanuel' (origem em Capela; raça adâmica = raças brancas) vai além de Kardec, sem seção Divergências.
- `wiki/conceitos/raca-adamica.md` (eixo 4, baixa) — 'anjos decaídos' central sem wikilink a [[wiki/conceitos/anjos]].

## 6. Resumo por página

### `wiki/conceitos/principio-vital.md`
Sólida: 14 citações ao Pentateuco conferem; lint zerado. Único ponto: a página-conceito 'fluido-vital' que a prosa e a tag pressupõem não existe.

### `wiki/conceitos/proibicao-de-evocar-os-mortos.md`
Fiel a C&I cap. XI; tag tema/mediunidade aplicada; locus item 4 deveria ser 4-5 (boi do Êxodo está no item 5); estrutura.

### `wiki/conceitos/psicografia.md`
Sólida; wikilink pneumatografia aplicado; eixo-2 sobre LM cap. XXIV DESCARTADO (citação sustenta a afirmação); autor tags e estrutura.

### `wiki/conceitos/purgatorio.md`
Fiel a C&I 1ª parte cap. V; tags tema/sofrimento + tema/livre-arbitrio + wikilink mundos-de-expiacao aplicados; falta link a expiacao.

### `wiki/conceitos/raca-adamica.md`
Sólida e bem fundamentada; link raw RE corrigido (jan→mar) + tag tema/espiritos; 2 blockquotes não-literais (RE mar/1860 frase inexistente; Emmanuel 'angustiados'→'desolados'); desenvolvimento de Emmanuel (Capela, racialização) tensiona Gênese cap. XI item 39.
