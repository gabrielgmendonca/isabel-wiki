---
tipo: sintese
fontes: [meta]
tags: [estatisticas, meta, grafo, vocabulario]
atualizado_em: 2026-04-28
status: ativo
---

# Estatísticas da wiki

## Pergunta motivadora

Como a wiki IsAbel está distribuída entre obras, conceitos e entidades? Quais são os nós centrais do grafo, quais páginas estão isoladas, que termos dominam o vocabulário, e como é o ritmo de ingestão ao longo do tempo? Esta página é **regenerada automaticamente** — serve como painel para orientar expansões, backlinks faltantes e possíveis novos conceitos.

> Gerado em **2026-04-28** por `.claude/skills/stats/scripts/stats_wiki.py`.

## Resumo executivo

- Páginas na wiki: **325**
- Arquivos em `raw/`: **1241**
- Nós no grafo: **322** · Arestas: **3198**
- Componentes fracamente conexos: **1** (maior: 322 nós)
- Páginas órfãs (sem backlinks): **1**
- Vocabulário único (após stopwords): **18086** termos
- Entradas em `log.md`: **95**
- Razão conceitos/questões: **142:9** (15.8)
- Questões únicas do LE citadas: **283/1019** (27.8%)
- Wikilinks não resolvidos (freq ≥ 5): **0** targets

## Cobertura por tipo

| Diretório | Páginas |
|-----------|---------|
| `wiki/obras/` | 39 |
| `wiki/conceitos/` | 142 |
| `wiki/personalidades/` | 104 |
| `wiki/questoes/` | 9 |
| `wiki/aprofundamentos/` | 6 |
| `wiki/sinteses/` | 7 |
| `wiki/divergencias/` | 14 |
| `wiki/trilhas/` | 4 |

### Status

| Status | Páginas |
|--------|---------|
| `ativo` | 270 |
| `rascunho` | 41 |
| `aberta` | 13 |
| `concluída` | 1 |

## Cobertura doutrinária

Referências únicas do Pentateuco efetivamente citadas pela wiki (`(LE, q. N)`, `(ESE, cap. X, item Y)`, etc.). Mede o quanto da codificação já foi ancorado em páginas próprias.

| Obra | Unidade | Citadas | Total | Cobertura |
|------|---------|--------:|------:|----------:|
| LE | questões | 283 | 1019 | 27.8% |
| ESE | capítulos | 28 | 28 | 100.0% |
| Gênese | capítulos | 14 | 18 | 77.8% |
| LM | capítulos da 2ª parte | 26 | 33 | 78.8% |
| C&I | capítulos | 18 | 18 | 100.0% |

Referências `cap./item` únicas: ESE **137**, Gênese **68**, LM **35**, C&I **18**.

### Cobertura do LE por bloco de 100 questões

```
   1– 100  █████████····················   32/100 (32%)
 101– 200  ████████·····················   28/100 (28%)
 201– 300  ████·························   16/100 (16%)
 301– 400  ██···························    7/100 (7%)
 401– 500  ███··························   13/100 (13%)
 501– 600  ██████························   20/100 (20%)
 601– 700  █████████████████············   58/100 (58%)
 701– 800  █████████····················   33/100 (33%)
 801– 900  ████████·····················   29/100 (29%)
 901–1000  ██████████···················   35/100 (35%)
1001–1019  ██████████████████···········   12/19 (63%)
```

## Grafo de conhecimento

### Mais referenciados (grau de entrada)

| # | Página | In |
|---|--------|----|
| 1 | [[wiki/obras/ceu-e-inferno]] | 97 |
| 2 | [[wiki/conceitos/reencarnacao]] | 94 |
| 3 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 90 |
| 4 | [[wiki/conceitos/progresso-espiritual]] | 80 |
| 5 | [[wiki/conceitos/caridade]] | 79 |
| 6 | [[wiki/conceitos/livre-arbitrio]] | 56 |
| 7 | [[wiki/conceitos/mediunidade]] | 55 |
| 8 | [[wiki/conceitos/obsessao]] | 52 |
| 9 | [[wiki/conceitos/prece]] | 51 |
| 10 | [[wiki/personalidades/jesus]] | 51 |
| 11 | [[wiki/conceitos/perispirito]] | 50 |
| 12 | [[wiki/obras/livro-dos-espiritos]] | 47 |
| 13 | [[wiki/conceitos/lei-de-justica-amor-e-caridade]] | 45 |
| 14 | [[wiki/conceitos/expiacao-e-reparacao]] | 42 |
| 15 | [[wiki/conceitos/lei-de-causa-e-efeito]] | 42 |

### Mais conectores (grau de saída)

| # | Página | Out |
|---|--------|-----|
| 1 | [[wiki/obras/ceu-e-inferno]] | 85 |
| 2 | [[wiki/obras/primeira-epistola-de-pedro]] | 51 |
| 3 | [[wiki/obras/epistola-de-tiago]] | 50 |
| 4 | [[wiki/obras/epistola-aos-romanos]] | 44 |
| 5 | [[wiki/sinteses/parabolas-de-jesus]] | 44 |
| 6 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 42 |
| 7 | [[wiki/obras/depois-da-morte]] | 37 |
| 8 | [[wiki/obras/evangelho-segundo-lucas]] | 36 |
| 9 | [[wiki/personalidades/jesus]] | 36 |
| 10 | [[wiki/obras/livro-dos-espiritos]] | 35 |
| 11 | [[wiki/obras/epistola-aos-hebreus]] | 34 |
| 12 | [[wiki/trilhas/esde]] | 34 |
| 13 | [[wiki/obras/primeira-epistola-de-joao]] | 33 |
| 14 | [[wiki/obras/espiritismo-mais-simples-expressao]] | 29 |
| 15 | [[wiki/obras/evangelho-segundo-mateus]] | 29 |

### Centralidade (PageRank)

| # | Página | PR |
|---|--------|-----|
| 1 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 0.0331 |
| 2 | [[wiki/conceitos/progresso-espiritual]] | 0.0330 |
| 3 | [[wiki/conceitos/reencarnacao]] | 0.0297 |
| 4 | [[wiki/conceitos/livre-arbitrio]] | 0.0229 |
| 5 | [[wiki/conceitos/lei-natural]] | 0.0185 |
| 6 | [[wiki/conceitos/lei-de-justica-amor-e-caridade]] | 0.0183 |
| 7 | [[wiki/obras/ceu-e-inferno]] | 0.0183 |
| 8 | [[wiki/conceitos/caridade]] | 0.0180 |
| 9 | [[wiki/obras/livro-dos-espiritos]] | 0.0154 |
| 10 | [[wiki/conceitos/perispirito]] | 0.0139 |
| 11 | [[wiki/conceitos/mediunidade]] | 0.0137 |
| 12 | [[wiki/conceitos/penas-e-gozos-futuros]] | 0.0134 |
| 13 | [[wiki/conceitos/morte]] | 0.0132 |
| 14 | [[wiki/conceitos/vida-espirita]] | 0.0124 |
| 15 | [[wiki/conceitos/obsessao]] | 0.0122 |

### Páginas órfãs (sem backlinks)

- [[wiki/aprofundamentos/missao-de-kardec]]

### Componentes isolados (≤ 2 nós)

_Nenhum._

## Vocabulário

### Top 50 termos

| # | Termo | Ocorrências |
|---|-------|-------------|
| 1 | `deus` | 1274 |
| 2 | `espírito` | 1122 |
| 3 | `kardec` | 1119 |
| 4 | `espíritos` | 1034 |
| 5 | `moral` | 899 |
| 6 | `espírita` | 729 |
| 7 | `vida` | 686 |
| 8 | `espiritual` | 622 |
| 9 | `jesus` | 613 |
| 10 | `homem` | 501 |
| 11 | `espiritismo` | 436 |
| 12 | `morte` | 416 |
| 13 | `alma` | 406 |
| 14 | `cristo` | 399 |
| 15 | `corpo` | 398 |
| 16 | `caridade` | 391 |
| 17 | `amor` | 379 |
| 18 | `mundo` | 354 |
| 19 | `doutrina` | 350 |
| 20 | `leitura` | 348 |
| 21 | `caps` | 334 |
| 22 | `terra` | 325 |
| 23 | `item` | 302 |
| 24 | `progresso` | 282 |
| 25 | `paulo` | 282 |
| 26 | `prática` | 279 |
| 27 | `prece` | 277 |
| 28 | `três` | 276 |
| 29 | `princípio` | 266 |
| 30 | `justiça` | 259 |
| 31 | `toda` | 254 |
| 32 | `obras` | 252 |
| 33 | `natureza` | 246 |
| 34 | `obra` | 241 |
| 35 | `andré` | 241 |
| 36 | `parábola` | 239 |
| 37 | `segundo` | 234 |
| 38 | `médium` | 232 |
| 39 | `ensino` | 232 |
| 40 | `próprio` | 228 |
| 41 | `sofrimento` | 217 |
| 42 | `contra` | 213 |
| 43 | `estado` | 202 |
| 44 | `evangelho` | 201 |
| 45 | `expiação` | 198 |
| 46 | `sempre` | 198 |
| 47 | `arrependimento` | 197 |
| 48 | `mundos` | 195 |
| 49 | `passagem` | 192 |
| 50 | `filho` | 191 |

### Top 20 bigramas

| # | Bigrama | Ocorrências |
|---|---------|-------------|
| 1 | `andré luiz` | 174 |
| 2 | `leitura espírita` | 145 |
| 3 | `aplicação prática` | 126 |
| 4 | `ensino kardec` | 118 |
| 5 | `livre arbítrio` | 109 |
| 6 | `mundo espiritual` | 99 |
| 7 | `chico xavier` | 87 |
| 8 | `doutrina espírita` | 82 |
| 9 | `vida futura` | 74 |
| 10 | `após morte` | 71 |
| 11 | `espírito verdade` | 61 |
| 12 | `plano espiritual` | 56 |
| 13 | `léon denis` | 56 |
| 14 | `situação mundo` | 56 |
| 15 | `lições principais` | 56 |
| 16 | `caridade salvação` | 55 |
| 17 | `estudo espírita` | 54 |
| 18 | `justiça divina` | 53 |
| 19 | `pluralidade existências` | 52 |
| 20 | `livro espíritos` | 49 |

## Atividade no tempo

Período coberto: **2026-04** → **2026-04** (1 meses).

### Sparkline por tipo

```
estudo     █  total=10
ingest     █  total=43
lint       █  total=30
refactor   █  total=10
setup      █  total=2
```

### Tabela mensal

| Mês | estudo | ingest | lint | refactor | setup | Total |
|-----|---|---|---|---|---|-------|
| 2026-04 | 10 | 43 | 30 | 10 | 2 | 95 |

### Dias mais ativos

| Data | Entradas |
|------|----------|
| 2026-04-07 | 15 |
| 2026-04-15 | 13 |
| 2026-04-26 | 10 |
| 2026-04-19 | 10 |
| 2026-04-06 | 10 |
| 2026-04-28 | 8 |
| 2026-04-27 | 8 |
| 2026-04-21 | 6 |
| 2026-04-16 | 6 |
| 2026-04-20 | 4 |

## Tamanho das páginas

```
<200        120  ██████████████████████████████
200-500     116  █████████████████████████████
500-1000     55  █████████████
1000-2000    25  ██████
>2000         6  █
```

### Maiores

- [[wiki/obras/primeira-epistola-de-pedro]] — 3564 palavras
- [[wiki/obras/primeira-epistola-de-joao]] — 2981 palavras
- [[wiki/obras/epistola-aos-romanos]] — 2305 palavras
- [[wiki/obras/epistola-de-tiago]] — 2295 palavras
- [[wiki/obras/epistola-aos-hebreus]] — 2278 palavras
- [[wiki/aprofundamentos/expiacao-e-arrependimento]] — 2238 palavras
- [[wiki/obras/obreiros-da-vida-eterna]] — 1883 palavras
- [[wiki/obras/missionarios-da-luz]] — 1773 palavras
- [[wiki/obras/os-mensageiros]] — 1696 palavras
- [[wiki/obras/primeira-epistola-aos-corintios]] — 1661 palavras

### Menores (candidatas a expansão)

- [[wiki/conceitos/pluralidade-das-existencias]] — 82 palavras
- [[wiki/trilhas/esde]] — 87 palavras
- [[wiki/conceitos/lei-de-conservacao]] — 92 palavras
- [[wiki/personalidades/vinicius]] — 94 palavras
- [[wiki/personalidades/erasto]] — 97 palavras
- [[wiki/personalidades/marques-de-saint-paul]] — 98 palavras
- [[wiki/personalidades/sra-helene-michel]] — 98 palavras
- [[wiki/conceitos/vida-espirita]] — 99 palavras
- [[wiki/personalidades/arrependimento-de-um-dissoluto]] — 100 palavras
- [[wiki/personalidades/francisco-do-espirito-santo-neto]] — 101 palavras

## Referências não resolvidas

Wikilinks `[[...]]` cujo target não existe na árvore — candidatos a páginas novas (quando frequentes) ou erros de digitação (quando raros).

Total: **1** targets distintos, **1** ocorrências. Freq ≥ 5: **0**.

### Mais referenciados (freq ≥ 3)

| # | Target | Ocorrências |
|---|--------|------------:|
| — | _nenhum com freq ≥ 3_ | — |

## Sugestões automáticas

- **1 páginas órfãs** (grau de entrada = 0) — considerar adicionar backlinks a partir de conceitos/obras relacionados.
- **Termos frequentes sem página própria**: `espírito` (1122), `kardec` (1119), `espíritos` (1034), `moral` (899), `espírita` (729), `vida` (686), `espiritual` (622), `homem` (501) — candidatos a novos conceitos ou sinônimos a padronizar.
- **3 blocos de 100 questões do LE com <20% de cobertura**: 201–300 (16/100), 301–400 (7/100), 401–500 (13/100). Priorizar extração de questões-chave desses intervalos para `wiki/questoes/`.

## Páginas referenciadas

- [[index]]
- `log.md`

## Fontes

- Script gerador: `.claude/skills/stats/scripts/stats_wiki.py` (execução em 2026-04-28).
- Corpus analisado: `wiki/**/*.md`, `log.md`, `raw/**/*.md`.
- Dependências: `networkx` (grafo, PageRank), `nltk` (stopwords PT-BR).
- Filtros: meta-páginas (`tipo: sintese` + tag `meta`) são excluídas de grafo, vocabulário, tamanho, cobertura doutrinária e wikilinks quebrados; seções-template (`## Fontes`, `## Páginas relacionadas`, `## Páginas referenciadas`, `## Conceitos relacionados`) são removidas antes da tokenização.
- Cobertura doutrinária: regex sobre citações inline `(LE, q. N)`, `(ESE, cap. X, item Y)`, `(Gênese, cap. X, item Y)`, `(LM, Nª parte, cap. X)`, `(C&I, Nª parte, cap. X)`. Totais canônicos: LE=1019q; ESE=28c; Gênese=18c; LM=33c (2ª parte); C&I=18c (11 + 7).
