---
tipo: sintese
fontes: [meta]
tags: [estatisticas, meta, grafo, vocabulario]
atualizado_em: 2026-04-20
status: ativo
---

# Estatísticas da wiki

## Pergunta motivadora

Como a wiki IsAbel está distribuída entre obras, conceitos e entidades? Quais são os nós centrais do grafo, quais páginas estão isoladas, que termos dominam o vocabulário, e como é o ritmo de ingestão ao longo do tempo? Esta página é **regenerada automaticamente** — serve como painel para orientar expansões, backlinks faltantes e possíveis novos conceitos.

> Gerado em **2026-04-20** por `.claude/skills/stats/scripts/stats_wiki.py`.

## Resumo executivo

- Páginas na wiki: **277**
- Arquivos em `raw/`: **1226**
- Nós no grafo: **274** · Arestas: **2264**
- Componentes fracamente conexos: **1** (maior: 274 nós)
- Páginas órfãs (sem backlinks): **3**
- Vocabulário único (após stopwords): **13704** termos
- Entradas em `log.md`: **60**
- Razão conceitos/questões: **129:9** (14.3)
- Questões únicas do LE citadas: **279/1019** (27.4%)
- Wikilinks não resolvidos (freq ≥ 5): **0** targets

## Cobertura por tipo

| Diretório | Páginas |
|-----------|---------|
| `wiki/obras/` | 26 |
| `wiki/conceitos/` | 129 |
| `wiki/personalidades/` | 94 |
| `wiki/questoes/` | 9 |
| `wiki/aprofundamentos/` | 1 |
| `wiki/sinteses/` | 6 |
| `wiki/divergencias/` | 8 |
| `wiki/trilhas/` | 4 |

### Status

| Status | Páginas |
|--------|---------|
| `ativo` | 249 |
| `rascunho` | 20 |
| `aberta` | 7 |
| `concluída` | 1 |

## Cobertura doutrinária

Referências únicas do Pentateuco efetivamente citadas pela wiki (`(LE, q. N)`, `(ESE, cap. X, item Y)`, etc.). Mede o quanto da codificação já foi ancorado em páginas próprias.

| Obra | Unidade | Citadas | Total | Cobertura |
|------|---------|--------:|------:|----------:|
| LE | questões | 279 | 1019 | 27.4% |
| ESE | capítulos | 28 | 28 | 100.0% |
| Gênese | capítulos | 11 | 18 | 61.1% |
| LM | capítulos da 2ª parte | 25 | 33 | 75.8% |
| C&I | capítulos | 18 | 18 | 100.0% |

Referências `cap./item` únicas: ESE **132**, Gênese **52**, LM **31**, C&I **18**.

### Cobertura do LE por bloco de 100 questões

```
   1– 100  █████████····················   32/100 (32%)
 101– 200  ████████·····················   27/100 (27%)
 201– 300  ████·························   16/100 (16%)
 301– 400  ██···························    7/100 (7%)
 401– 500  ███··························   13/100 (13%)
 501– 600  ██████························   20/100 (20%)
 601– 700  █████████████████············   58/100 (58%)
 701– 800  █████████····················   33/100 (33%)
 801– 900  ████████·····················   28/100 (28%)
 901–1000  ██████████···················   34/100 (34%)
1001–1019  █████████████████············   11/19 (58%)
```

## Grafo de conhecimento

### Mais referenciados (grau de entrada)

| # | Página | In |
|---|--------|----|
| 1 | [[wiki/obras/ceu-e-inferno]] | 89 |
| 2 | [[wiki/conceitos/reencarnacao]] | 83 |
| 3 | [[wiki/conceitos/progresso-espiritual]] | 76 |
| 4 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 73 |
| 5 | [[wiki/conceitos/caridade]] | 67 |
| 6 | [[wiki/conceitos/livre-arbitrio]] | 46 |
| 7 | [[wiki/conceitos/prece]] | 37 |
| 8 | [[wiki/conceitos/mediunidade]] | 36 |
| 9 | [[wiki/conceitos/morte]] | 36 |
| 10 | [[wiki/conceitos/obsessao]] | 36 |
| 11 | [[wiki/conceitos/lei-de-justica-amor-e-caridade]] | 35 |
| 12 | [[wiki/conceitos/penas-e-gozos-futuros]] | 34 |
| 13 | [[wiki/conceitos/expiacao-e-reparacao]] | 33 |
| 14 | [[wiki/obras/livro-dos-espiritos]] | 33 |
| 15 | [[wiki/personalidades/jesus]] | 33 |

### Mais conectores (grau de saída)

| # | Página | Out |
|---|--------|-----|
| 1 | [[wiki/obras/ceu-e-inferno]] | 85 |
| 2 | [[wiki/sinteses/parabolas-de-jesus]] | 43 |
| 3 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 40 |
| 4 | [[wiki/obras/depois-da-morte]] | 37 |
| 5 | [[wiki/obras/evangelho-segundo-lucas]] | 36 |
| 6 | [[wiki/personalidades/jesus]] | 36 |
| 7 | [[wiki/obras/livro-dos-espiritos]] | 35 |
| 8 | [[wiki/trilhas/esde]] | 34 |
| 9 | [[wiki/obras/evangelho-segundo-mateus]] | 29 |
| 10 | [[wiki/obras/o-que-e-o-espiritismo]] | 28 |
| 11 | [[wiki/obras/primeira-epistola-aos-corintios]] | 27 |
| 12 | [[wiki/aprofundamentos/expiacao-e-arrependimento]] | 25 |
| 13 | [[wiki/obras/obras-postumas]] | 24 |
| 14 | [[wiki/obras/evangelho-segundo-marcos]] | 20 |
| 15 | [[wiki/obras/o-problema-do-ser-e-do-destino]] | 20 |

### Centralidade (PageRank)

| # | Página | PR |
|---|--------|-----|
| 1 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 0.0417 |
| 2 | [[wiki/conceitos/progresso-espiritual]] | 0.0399 |
| 3 | [[wiki/conceitos/reencarnacao]] | 0.0320 |
| 4 | [[wiki/conceitos/livre-arbitrio]] | 0.0262 |
| 5 | [[wiki/conceitos/lei-natural]] | 0.0217 |
| 6 | [[wiki/conceitos/caridade]] | 0.0208 |
| 7 | [[wiki/conceitos/lei-de-justica-amor-e-caridade]] | 0.0200 |
| 8 | [[wiki/obras/ceu-e-inferno]] | 0.0196 |
| 9 | [[wiki/obras/livro-dos-espiritos]] | 0.0176 |
| 10 | [[wiki/conceitos/vida-espirita]] | 0.0161 |
| 11 | [[wiki/conceitos/perfeicao-moral]] | 0.0155 |
| 12 | [[wiki/conceitos/morte]] | 0.0150 |
| 13 | [[wiki/conceitos/penas-e-gozos-futuros]] | 0.0146 |
| 14 | [[wiki/conceitos/mediunidade]] | 0.0134 |
| 15 | [[wiki/conceitos/perispirito]] | 0.0130 |

### Páginas órfãs (sem backlinks)

- [[wiki/conceitos/bem-aventuranca-dos-puros-de-coracao]]
- [[wiki/trilhas/palestras]]
- [[wiki/trilhas/primeiros-passos]]

### Componentes isolados (≤ 2 nós)

_Nenhum._

## Vocabulário

### Top 50 termos

| # | Termo | Ocorrências |
|---|-------|-------------|
| 1 | `kardec` | 800 |
| 2 | `deus` | 765 |
| 3 | `espírito` | 749 |
| 4 | `espíritos` | 712 |
| 5 | `moral` | 518 |
| 6 | `vida` | 485 |
| 7 | `jesus` | 457 |
| 8 | `espírita` | 442 |
| 9 | `espiritual` | 393 |
| 10 | `homem` | 359 |
| 11 | `espiritismo` | 326 |
| 12 | `morte` | 314 |
| 13 | `alma` | 298 |
| 14 | `caridade` | 284 |
| 15 | `mundo` | 272 |
| 16 | `corpo` | 267 |
| 17 | `parábola` | 229 |
| 18 | `progresso` | 223 |
| 19 | `terra` | 212 |
| 20 | `ensino` | 203 |
| 21 | `prática` | 202 |
| 22 | `doutrina` | 201 |
| 23 | `justiça` | 195 |
| 24 | `mateus` | 179 |
| 25 | `natureza` | 173 |
| 26 | `expiação` | 171 |
| 27 | `arrependimento` | 169 |
| 28 | `princípio` | 166 |
| 29 | `prece` | 163 |
| 30 | `amor` | 160 |
| 31 | `denis` | 159 |
| 32 | `caps` | 159 |
| 33 | `mundos` | 156 |
| 34 | `toda` | 154 |
| 35 | `sofrimento` | 154 |
| 36 | `orgulho` | 154 |
| 37 | `sempre` | 153 |
| 38 | `provas` | 151 |
| 39 | `três` | 145 |
| 40 | `estado` | 144 |
| 41 | `item` | 141 |
| 42 | `tudo` | 138 |
| 43 | `segundo` | 136 |
| 44 | `homens` | 133 |
| 45 | `evangelho` | 132 |
| 46 | `paulo` | 130 |
| 47 | `causa` | 129 |
| 48 | `reparação` | 127 |
| 49 | `divina` | 127 |
| 50 | `médium` | 127 |

### Top 20 bigramas

| # | Bigrama | Ocorrências |
|---|---------|-------------|
| 1 | `aplicação prática` | 109 |
| 2 | `ensino kardec` | 107 |
| 3 | `mundo espiritual` | 100 |
| 4 | `vida futura` | 74 |
| 5 | `livre arbítrio` | 72 |
| 6 | `após morte` | 60 |
| 7 | `situação mundo` | 58 |
| 8 | `lições principais` | 58 |
| 9 | `doutrina espírita` | 54 |
| 10 | `léon denis` | 50 |
| 11 | `justiça divina` | 49 |
| 12 | `leitura espírita` | 47 |
| 13 | `livro espíritos` | 47 |
| 14 | `dores alma` | 40 |
| 15 | `reino céus` | 39 |
| 16 | `segundo espiritismo` | 35 |
| 17 | `viagem espírita` | 35 |
| 18 | `pluralidade existências` | 34 |
| 19 | `causa efeito` | 34 |
| 20 | `evangelho segundo` | 34 |

## Atividade no tempo

Período coberto: **2026-04** → **2026-04** (1 meses).

### Sparkline por tipo

```
ingest     █  total=29
lint       █  total=17
query      █  total=6
refactor   █  total=6
setup      █  total=2
```

### Tabela mensal

| Mês | ingest | lint | query | refactor | setup | Total |
|-----|---|---|---|---|---|-------|
| 2026-04 | 29 | 17 | 6 | 6 | 2 | 60 |

### Dias mais ativos

| Data | Entradas |
|------|----------|
| 2026-04-07 | 15 |
| 2026-04-15 | 13 |
| 2026-04-19 | 10 |
| 2026-04-06 | 10 |
| 2026-04-16 | 6 |
| 2026-04-05 | 2 |
| 2026-04-08 | 2 |
| 2026-04-20 | 1 |
| 2026-04-18 | 1 |

## Tamanho das páginas

```
<200        134  ██████████████████████████████
200-500     100  ██████████████████████
500-1000     30  ██████
1000-2000     9  ██
>2000         1  
```

### Maiores

- [[wiki/aprofundamentos/expiacao-e-arrependimento]] — 2238 palavras
- [[wiki/obras/primeira-epistola-aos-corintios]] — 1661 palavras
- [[wiki/obras/atos-dos-apostolos]] — 1535 palavras
- [[wiki/sinteses/hierarquia-de-autoridade]] — 1490 palavras
- [[wiki/obras/as-dores-da-alma]] — 1402 palavras
- [[wiki/obras/evangelho-segundo-marcos]] — 1182 palavras
- [[wiki/obras/cristianismo-e-espiritismo]] — 1118 palavras
- [[wiki/obras/evangelho-segundo-lucas]] — 1116 palavras
- [[wiki/obras/evangelho-segundo-mateus]] — 1073 palavras
- [[wiki/obras/quando-o-invisivel-se-torna-inevitavel]] — 1061 palavras

### Menores (candidatas a expansão)

- [[wiki/personalidades/carlos-mendonca]] — 51 palavras
- [[wiki/personalidades/chico-xavier]] — 71 palavras
- [[wiki/conceitos/pluralidade-das-existencias]] — 82 palavras
- [[wiki/trilhas/esde]] — 87 palavras
- [[wiki/personalidades/joseph-bre]] — 90 palavras
- [[wiki/conceitos/lei-de-conservacao]] — 92 palavras
- [[wiki/personalidades/espiritos-reveladores]] — 92 palavras
- [[wiki/personalidades/vinicius]] — 94 palavras
- [[wiki/personalidades/eric-stanislas]] — 96 palavras
- [[wiki/personalidades/erasto]] — 97 palavras

## Referências não resolvidas

Wikilinks `[[...]]` cujo target não existe na árvore — candidatos a páginas novas (quando frequentes) ou erros de digitação (quando raros).

Total: **37** targets distintos, **37** ocorrências. Freq ≥ 5: **0**.

### Mais referenciados (freq ≥ 3)

| # | Target | Ocorrências |
|---|--------|------------:|
| — | _nenhum com freq ≥ 3_ | — |

## Sugestões automáticas

- **3 páginas órfãs** (grau de entrada = 0) — considerar adicionar backlinks a partir de conceitos/obras relacionados.
- **Termos frequentes sem página própria**: `kardec` (800), `espírito` (749), `espíritos` (712), `moral` (518), `vida` (485), `espírita` (442), `espiritual` (393), `homem` (359) — candidatos a novos conceitos ou sinônimos a padronizar.
- **3 blocos de 100 questões do LE com <20% de cobertura**: 201–300 (16/100), 301–400 (7/100), 401–500 (13/100). Priorizar extração de questões-chave desses intervalos para `wiki/questoes/`.

## Páginas referenciadas

- [[index]]
- `log.md`

## Fontes

- Script gerador: `.claude/skills/stats/scripts/stats_wiki.py` (execução em 2026-04-20).
- Corpus analisado: `wiki/**/*.md`, `log.md`, `raw/**/*.md`.
- Dependências: `networkx` (grafo, PageRank), `nltk` (stopwords PT-BR).
- Filtros: meta-páginas (`tipo: sintese` + tag `meta`) são excluídas de grafo, vocabulário, tamanho, cobertura doutrinária e wikilinks quebrados; seções-template (`## Fontes`, `## Páginas relacionadas`, `## Páginas referenciadas`, `## Conceitos relacionados`) são removidas antes da tokenização.
- Cobertura doutrinária: regex sobre citações inline `(LE, q. N)`, `(ESE, cap. X, item Y)`, `(Gênese, cap. X, item Y)`, `(LM, Nª parte, cap. X)`, `(C&I, Nª parte, cap. X)`. Totais canônicos: LE=1019q; ESE=28c; Gênese=18c; LM=33c (2ª parte); C&I=18c (11 + 7).
