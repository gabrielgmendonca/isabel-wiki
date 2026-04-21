---
tipo: sintese
fontes: [meta]
tags: [estatisticas, meta, grafo, vocabulario]
atualizado_em: 2026-04-21
status: ativo
---

# Estatísticas da wiki

## Pergunta motivadora

Como a wiki IsAbel está distribuída entre obras, conceitos e entidades? Quais são os nós centrais do grafo, quais páginas estão isoladas, que termos dominam o vocabulário, e como é o ritmo de ingestão ao longo do tempo? Esta página é **regenerada automaticamente** — serve como painel para orientar expansões, backlinks faltantes e possíveis novos conceitos.

> Gerado em **2026-04-21** por `.claude/skills/stats/scripts/stats_wiki.py`.

## Resumo executivo

- Páginas na wiki: **284**
- Arquivos em `raw/`: **1226**
- Nós no grafo: **281** · Arestas: **2451**
- Componentes fracamente conexos: **1** (maior: 281 nós)
- Páginas órfãs (sem backlinks): **2**
- Vocabulário único (após stopwords): **14411** termos
- Entradas em `log.md`: **69**
- Razão conceitos/questões: **129:9** (14.3)
- Questões únicas do LE citadas: **279/1019** (27.4%)
- Wikilinks não resolvidos (freq ≥ 5): **0** targets

## Cobertura por tipo

| Diretório | Páginas |
|-----------|---------|
| `wiki/obras/` | 28 |
| `wiki/conceitos/` | 129 |
| `wiki/personalidades/` | 95 |
| `wiki/questoes/` | 9 |
| `wiki/aprofundamentos/` | 1 |
| `wiki/sinteses/` | 6 |
| `wiki/divergencias/` | 12 |
| `wiki/trilhas/` | 4 |

### Status

| Status | Páginas |
|--------|---------|
| `ativo` | 252 |
| `rascunho` | 20 |
| `aberta` | 11 |
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
| 1 | [[wiki/obras/ceu-e-inferno]] | 92 |
| 2 | [[wiki/conceitos/reencarnacao]] | 85 |
| 3 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 80 |
| 4 | [[wiki/conceitos/progresso-espiritual]] | 78 |
| 5 | [[wiki/conceitos/caridade]] | 70 |
| 6 | [[wiki/conceitos/livre-arbitrio]] | 50 |
| 7 | [[wiki/obras/livro-dos-espiritos]] | 40 |
| 8 | [[wiki/conceitos/lei-de-justica-amor-e-caridade]] | 39 |
| 9 | [[wiki/conceitos/mediunidade]] | 37 |
| 10 | [[wiki/conceitos/prece]] | 37 |
| 11 | [[wiki/conceitos/morte]] | 36 |
| 12 | [[wiki/conceitos/obsessao]] | 36 |
| 13 | [[wiki/personalidades/jesus]] | 36 |
| 14 | [[wiki/conceitos/penas-e-gozos-futuros]] | 35 |
| 15 | [[wiki/conceitos/expiacao-e-reparacao]] | 33 |

### Mais conectores (grau de saída)

| # | Página | Out |
|---|--------|-----|
| 1 | [[wiki/obras/ceu-e-inferno]] | 85 |
| 2 | [[wiki/obras/epistola-aos-romanos]] | 44 |
| 3 | [[wiki/sinteses/parabolas-de-jesus]] | 43 |
| 4 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 40 |
| 5 | [[wiki/obras/depois-da-morte]] | 37 |
| 6 | [[wiki/obras/evangelho-segundo-lucas]] | 36 |
| 7 | [[wiki/personalidades/jesus]] | 36 |
| 8 | [[wiki/obras/livro-dos-espiritos]] | 35 |
| 9 | [[wiki/obras/epistola-aos-hebreus]] | 34 |
| 10 | [[wiki/trilhas/esde]] | 34 |
| 11 | [[wiki/obras/evangelho-segundo-mateus]] | 29 |
| 12 | [[wiki/obras/o-que-e-o-espiritismo]] | 28 |
| 13 | [[wiki/obras/primeira-epistola-aos-corintios]] | 27 |
| 14 | [[wiki/aprofundamentos/expiacao-e-arrependimento]] | 25 |
| 15 | [[wiki/obras/obras-postumas]] | 24 |

### Centralidade (PageRank)

| # | Página | PR |
|---|--------|-----|
| 1 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 0.0394 |
| 2 | [[wiki/conceitos/progresso-espiritual]] | 0.0375 |
| 3 | [[wiki/conceitos/reencarnacao]] | 0.0308 |
| 4 | [[wiki/conceitos/livre-arbitrio]] | 0.0247 |
| 5 | [[wiki/conceitos/lei-natural]] | 0.0222 |
| 6 | [[wiki/conceitos/caridade]] | 0.0204 |
| 7 | [[wiki/conceitos/lei-de-justica-amor-e-caridade]] | 0.0199 |
| 8 | [[wiki/obras/ceu-e-inferno]] | 0.0198 |
| 9 | [[wiki/obras/livro-dos-espiritos]] | 0.0182 |
| 10 | [[wiki/conceitos/perfeicao-moral]] | 0.0147 |
| 11 | [[wiki/conceitos/morte]] | 0.0143 |
| 12 | [[wiki/conceitos/penas-e-gozos-futuros]] | 0.0143 |
| 13 | [[wiki/conceitos/vida-espirita]] | 0.0138 |
| 14 | [[wiki/conceitos/mediunidade]] | 0.0130 |
| 15 | [[wiki/conceitos/perispirito]] | 0.0125 |

### Páginas órfãs (sem backlinks)

- [[wiki/trilhas/palestras]]
- [[wiki/trilhas/primeiros-passos]]

### Componentes isolados (≤ 2 nós)

_Nenhum._

## Vocabulário

### Top 50 termos

| # | Termo | Ocorrências |
|---|-------|-------------|
| 1 | `deus` | 925 |
| 2 | `espírito` | 867 |
| 3 | `kardec` | 860 |
| 4 | `espíritos` | 782 |
| 5 | `moral` | 609 |
| 6 | `espírita` | 534 |
| 7 | `vida` | 526 |
| 8 | `jesus` | 501 |
| 9 | `homem` | 427 |
| 10 | `espiritual` | 404 |
| 11 | `espiritismo` | 361 |
| 12 | `morte` | 354 |
| 13 | `alma` | 319 |
| 14 | `caridade` | 301 |
| 15 | `mundo` | 286 |
| 16 | `corpo` | 283 |
| 17 | `progresso` | 249 |
| 18 | `terra` | 236 |
| 19 | `parábola` | 229 |
| 20 | `doutrina` | 226 |
| 21 | `justiça` | 224 |
| 22 | `ensino` | 212 |
| 23 | `prática` | 209 |
| 24 | `paulo` | 203 |
| 25 | `amor` | 198 |
| 26 | `natureza` | 190 |
| 27 | `arrependimento` | 185 |
| 28 | `cristo` | 185 |
| 29 | `princípio` | 183 |
| 30 | `leitura` | 183 |
| 31 | `caps` | 180 |
| 32 | `mateus` | 179 |
| 33 | `sofrimento` | 177 |
| 34 | `expiação` | 176 |
| 35 | `provas` | 175 |
| 36 | `toda` | 174 |
| 37 | `segundo` | 174 |
| 38 | `sempre` | 167 |
| 39 | `item` | 165 |
| 40 | `três` | 164 |
| 41 | `denis` | 164 |
| 42 | `prece` | 163 |
| 43 | `estado` | 161 |
| 44 | `mundos` | 156 |
| 45 | `tudo` | 154 |
| 46 | `orgulho` | 154 |
| 47 | `divina` | 151 |
| 48 | `homens` | 148 |
| 49 | `obras` | 148 |
| 50 | `filho` | 141 |

### Top 20 bigramas

| # | Bigrama | Ocorrências |
|---|---------|-------------|
| 1 | `aplicação prática` | 109 |
| 2 | `ensino kardec` | 107 |
| 3 | `mundo espiritual` | 100 |
| 4 | `livre arbítrio` | 99 |
| 5 | `leitura espírita` | 86 |
| 6 | `vida futura` | 74 |
| 7 | `após morte` | 67 |
| 8 | `doutrina espírita` | 65 |
| 9 | `situação mundo` | 58 |
| 10 | `lições principais` | 58 |
| 11 | `pluralidade existências` | 51 |
| 12 | `léon denis` | 51 |
| 13 | `justiça divina` | 50 |
| 14 | `livro espíritos` | 47 |
| 15 | `dores alma` | 40 |
| 16 | `reino céus` | 39 |
| 17 | `viagem espírita` | 36 |
| 18 | `joão batista` | 36 |
| 19 | `segundo espiritismo` | 35 |
| 20 | `chico xavier` | 34 |

## Atividade no tempo

Período coberto: **2026-04** → **2026-04** (1 meses).

### Sparkline por tipo

```
ingest     █  total=32
lint       █  total=21
query      █  total=6
refactor   █  total=8
setup      █  total=2
```

### Tabela mensal

| Mês | ingest | lint | query | refactor | setup | Total |
|-----|---|---|---|---|---|-------|
| 2026-04 | 32 | 21 | 6 | 8 | 2 | 69 |

### Dias mais ativos

| Data | Entradas |
|------|----------|
| 2026-04-07 | 15 |
| 2026-04-15 | 13 |
| 2026-04-19 | 10 |
| 2026-04-06 | 10 |
| 2026-04-21 | 6 |
| 2026-04-16 | 6 |
| 2026-04-20 | 4 |
| 2026-04-05 | 2 |
| 2026-04-08 | 2 |
| 2026-04-18 | 1 |

## Tamanho das páginas

```
<200        128  ██████████████████████████████
200-500     104  ████████████████████████
500-1000     37  ████████
1000-2000     9  ██
>2000         3  
```

### Maiores

- [[wiki/obras/epistola-aos-romanos]] — 2305 palavras
- [[wiki/obras/epistola-aos-hebreus]] — 2278 palavras
- [[wiki/aprofundamentos/expiacao-e-arrependimento]] — 2238 palavras
- [[wiki/obras/primeira-epistola-aos-corintios]] — 1661 palavras
- [[wiki/obras/atos-dos-apostolos]] — 1535 palavras
- [[wiki/sinteses/hierarquia-de-autoridade]] — 1490 palavras
- [[wiki/obras/as-dores-da-alma]] — 1402 palavras
- [[wiki/obras/evangelho-segundo-marcos]] — 1182 palavras
- [[wiki/obras/cristianismo-e-espiritismo]] — 1118 palavras
- [[wiki/obras/evangelho-segundo-lucas]] — 1116 palavras

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

_Nenhum wikilink quebrado._

## Sugestões automáticas

- **2 páginas órfãs** (grau de entrada = 0) — considerar adicionar backlinks a partir de conceitos/obras relacionados.
- **Termos frequentes sem página própria**: `espírito` (867), `kardec` (860), `espíritos` (782), `moral` (609), `espírita` (534), `vida` (526), `homem` (427), `espiritual` (404) — candidatos a novos conceitos ou sinônimos a padronizar.
- **3 blocos de 100 questões do LE com <20% de cobertura**: 201–300 (16/100), 301–400 (7/100), 401–500 (13/100). Priorizar extração de questões-chave desses intervalos para `wiki/questoes/`.

## Páginas referenciadas

- [[index]]
- `log.md`

## Fontes

- Script gerador: `.claude/skills/stats/scripts/stats_wiki.py` (execução em 2026-04-21).
- Corpus analisado: `wiki/**/*.md`, `log.md`, `raw/**/*.md`.
- Dependências: `networkx` (grafo, PageRank), `nltk` (stopwords PT-BR).
- Filtros: meta-páginas (`tipo: sintese` + tag `meta`) são excluídas de grafo, vocabulário, tamanho, cobertura doutrinária e wikilinks quebrados; seções-template (`## Fontes`, `## Páginas relacionadas`, `## Páginas referenciadas`, `## Conceitos relacionados`) são removidas antes da tokenização.
- Cobertura doutrinária: regex sobre citações inline `(LE, q. N)`, `(ESE, cap. X, item Y)`, `(Gênese, cap. X, item Y)`, `(LM, Nª parte, cap. X)`, `(C&I, Nª parte, cap. X)`. Totais canônicos: LE=1019q; ESE=28c; Gênese=18c; LM=33c (2ª parte); C&I=18c (11 + 7).
