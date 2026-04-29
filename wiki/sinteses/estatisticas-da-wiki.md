---
tipo: sintese
fontes: [meta]
tags: [estatisticas, meta, grafo, vocabulario]
atualizado_em: 2026-04-29
status: ativo
---

# Estatísticas da wiki

## Pergunta motivadora

Como a wiki IsAbel está distribuída entre obras, conceitos e entidades? Quais são os nós centrais do grafo, quais páginas estão isoladas, que termos dominam o vocabulário, e como é o ritmo de ingestão ao longo do tempo? Esta página é **regenerada automaticamente** — serve como painel para orientar expansões, backlinks faltantes e possíveis novos conceitos.

> Gerado em **2026-04-29** por `.claude/skills/stats/scripts/stats_wiki.py`.

## Resumo executivo

- Páginas na wiki: **328**
- Arquivos em `raw/`: **1253**
- Nós no grafo: **325** · Arestas: **3286**
- Componentes fracamente conexos: **1** (maior: 325 nós)
- Páginas órfãs (sem backlinks): **2**
- Vocabulário único (após stopwords): **18326** termos
- Entradas em `log.md`: **99**
- Razão conceitos/questões: **142:9** (15.8)
- Questões únicas do LE citadas: **283/1019** (27.8%)
- Wikilinks não resolvidos (freq ≥ 5): **0** targets

## Cobertura por tipo

| Diretório | Páginas |
|-----------|---------|
| `wiki/obras/` | 41 |
| `wiki/conceitos/` | 142 |
| `wiki/personalidades/` | 105 |
| `wiki/questoes/` | 9 |
| `wiki/aprofundamentos/` | 6 |
| `wiki/sinteses/` | 7 |
| `wiki/divergencias/` | 14 |
| `wiki/trilhas/` | 4 |

### Status

| Status | Páginas |
|--------|---------|
| `ativo` | 273 |
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
| 2 | [[wiki/conceitos/reencarnacao]] | 96 |
| 3 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 90 |
| 4 | [[wiki/conceitos/progresso-espiritual]] | 82 |
| 5 | [[wiki/conceitos/caridade]] | 81 |
| 6 | [[wiki/conceitos/livre-arbitrio]] | 57 |
| 7 | [[wiki/conceitos/mediunidade]] | 57 |
| 8 | [[wiki/conceitos/obsessao]] | 53 |
| 9 | [[wiki/conceitos/prece]] | 53 |
| 10 | [[wiki/personalidades/jesus]] | 53 |
| 11 | [[wiki/conceitos/perispirito]] | 52 |
| 12 | [[wiki/obras/livro-dos-espiritos]] | 47 |
| 13 | [[wiki/conceitos/lei-de-justica-amor-e-caridade]] | 46 |
| 14 | [[wiki/conceitos/lei-de-causa-e-efeito]] | 44 |
| 15 | [[wiki/conceitos/expiacao-e-reparacao]] | 43 |

### Mais conectores (grau de saída)

| # | Página | Out |
|---|--------|-----|
| 1 | [[wiki/obras/ceu-e-inferno]] | 85 |
| 2 | [[wiki/obras/primeira-epistola-de-pedro]] | 51 |
| 3 | [[wiki/obras/epistola-de-tiago]] | 50 |
| 4 | [[wiki/obras/epistola-aos-romanos]] | 44 |
| 5 | [[wiki/sinteses/parabolas-de-jesus]] | 44 |
| 6 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 42 |
| 7 | [[wiki/obras/segunda-epistola-aos-corintios]] | 40 |
| 8 | [[wiki/obras/depois-da-morte]] | 37 |
| 9 | [[wiki/obras/evangelho-segundo-lucas]] | 36 |
| 10 | [[wiki/personalidades/jesus]] | 36 |
| 11 | [[wiki/obras/livro-dos-espiritos]] | 35 |
| 12 | [[wiki/obras/epistola-aos-hebreus]] | 34 |
| 13 | [[wiki/trilhas/esde]] | 34 |
| 14 | [[wiki/obras/primeira-epistola-de-joao]] | 33 |
| 15 | [[wiki/obras/espiritismo-mais-simples-expressao]] | 29 |

### Centralidade (PageRank)

| # | Página | PR |
|---|--------|-----|
| 1 | [[wiki/conceitos/progresso-espiritual]] | 0.0324 |
| 2 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 0.0324 |
| 3 | [[wiki/conceitos/reencarnacao]] | 0.0295 |
| 4 | [[wiki/conceitos/livre-arbitrio]] | 0.0229 |
| 5 | [[wiki/conceitos/lei-de-justica-amor-e-caridade]] | 0.0183 |
| 6 | [[wiki/conceitos/lei-natural]] | 0.0183 |
| 7 | [[wiki/obras/ceu-e-inferno]] | 0.0181 |
| 8 | [[wiki/conceitos/caridade]] | 0.0176 |
| 9 | [[wiki/obras/livro-dos-espiritos]] | 0.0154 |
| 10 | [[wiki/conceitos/perispirito]] | 0.0138 |
| 11 | [[wiki/conceitos/mediunidade]] | 0.0137 |
| 12 | [[wiki/conceitos/penas-e-gozos-futuros]] | 0.0134 |
| 13 | [[wiki/conceitos/morte]] | 0.0132 |
| 14 | [[wiki/conceitos/vida-espirita]] | 0.0123 |
| 15 | [[wiki/conceitos/obsessao]] | 0.0122 |

### Páginas órfãs (sem backlinks)

- [[wiki/aprofundamentos/missao-de-kardec]]
- [[wiki/obras/revista-espirita]]

### Componentes isolados (≤ 2 nós)

_Nenhum._

## Vocabulário

### Top 50 termos

| # | Termo | Ocorrências |
|---|-------|-------------|
| 1 | `deus` | 1319 |
| 2 | `espírito` | 1157 |
| 3 | `kardec` | 1144 |
| 4 | `espíritos` | 1057 |
| 5 | `moral` | 934 |
| 6 | `espírita` | 767 |
| 7 | `vida` | 700 |
| 8 | `espiritual` | 639 |
| 9 | `jesus` | 627 |
| 10 | `homem` | 510 |
| 11 | `espiritismo` | 445 |
| 12 | `cristo` | 431 |
| 13 | `morte` | 425 |
| 14 | `corpo` | 421 |
| 15 | `alma` | 409 |
| 16 | `caridade` | 406 |
| 17 | `amor` | 387 |
| 18 | `doutrina` | 358 |
| 19 | `mundo` | 358 |
| 20 | `leitura` | 356 |
| 21 | `caps` | 345 |
| 22 | `paulo` | 327 |
| 23 | `terra` | 326 |
| 24 | `item` | 310 |
| 25 | `progresso` | 291 |
| 26 | `três` | 287 |
| 27 | `prece` | 284 |
| 28 | `prática` | 284 |
| 29 | `princípio` | 279 |
| 30 | `toda` | 265 |
| 31 | `justiça` | 263 |
| 32 | `obras` | 260 |
| 33 | `segundo` | 252 |
| 34 | `natureza` | 246 |
| 35 | `andré` | 246 |
| 36 | `médium` | 245 |
| 37 | `obra` | 244 |
| 38 | `parábola` | 240 |
| 39 | `próprio` | 239 |
| 40 | `ensino` | 234 |
| 41 | `sofrimento` | 226 |
| 42 | `contra` | 215 |
| 43 | `estado` | 206 |
| 44 | `arrependimento` | 204 |
| 45 | `evangelho` | 204 |
| 46 | `casa` | 203 |
| 47 | `filho` | 202 |
| 48 | `sempre` | 200 |
| 49 | `expiação` | 199 |
| 50 | `passagem` | 198 |

### Top 20 bigramas

| # | Bigrama | Ocorrências |
|---|---------|-------------|
| 1 | `andré luiz` | 179 |
| 2 | `leitura espírita` | 149 |
| 3 | `aplicação prática` | 126 |
| 4 | `ensino kardec` | 118 |
| 5 | `livre arbítrio` | 109 |
| 6 | `mundo espiritual` | 99 |
| 7 | `chico xavier` | 88 |
| 8 | `doutrina espírita` | 85 |
| 9 | `vida futura` | 75 |
| 10 | `após morte` | 71 |
| 11 | `espírito verdade` | 62 |
| 12 | `estudo espírita` | 59 |
| 13 | `plano espiritual` | 56 |
| 14 | `léon denis` | 56 |
| 15 | `situação mundo` | 56 |
| 16 | `lições principais` | 56 |
| 17 | `caridade salvação` | 55 |
| 18 | `justiça divina` | 53 |
| 19 | `pluralidade existências` | 52 |
| 20 | `causa efeito` | 52 |

## Atividade no tempo

Período coberto: **2026-04** → **2026-04** (1 meses).

### Sparkline por tipo

```
estudo     █  total=11
ingest     █  total=45
lint       █  total=31
refactor   █  total=10
setup      █  total=2
```

### Tabela mensal

| Mês | estudo | ingest | lint | refactor | setup | Total |
|-----|---|---|---|---|---|-------|
| 2026-04 | 11 | 45 | 31 | 10 | 2 | 99 |

### Dias mais ativos

| Data | Entradas |
|------|----------|
| 2026-04-07 | 15 |
| 2026-04-15 | 13 |
| 2026-04-26 | 10 |
| 2026-04-19 | 10 |
| 2026-04-06 | 10 |
| 2026-04-28 | 9 |
| 2026-04-27 | 8 |
| 2026-04-21 | 6 |
| 2026-04-16 | 6 |
| 2026-04-20 | 4 |

## Tamanho das páginas

```
<200        120  ██████████████████████████████
200-500     114  ████████████████████████████
500-1000     59  ██████████████
1000-2000    25  ██████
>2000         7  █
```

### Maiores

- [[wiki/obras/primeira-epistola-de-pedro]] — 3564 palavras
- [[wiki/obras/primeira-epistola-de-joao]] — 2981 palavras
- [[wiki/obras/epistola-aos-romanos]] — 2305 palavras
- [[wiki/obras/epistola-de-tiago]] — 2295 palavras
- [[wiki/obras/epistola-aos-hebreus]] — 2278 palavras
- [[wiki/aprofundamentos/expiacao-e-arrependimento]] — 2238 palavras
- [[wiki/obras/segunda-epistola-aos-corintios]] — 2129 palavras
- [[wiki/obras/obreiros-da-vida-eterna]] — 1883 palavras
- [[wiki/obras/missionarios-da-luz]] — 1773 palavras
- [[wiki/obras/os-mensageiros]] — 1696 palavras

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

_Nenhum wikilink quebrado._

## Sugestões automáticas

- **2 páginas órfãs** (grau de entrada = 0) — considerar adicionar backlinks a partir de conceitos/obras relacionados.
- **Termos frequentes sem página própria**: `espírito` (1157), `kardec` (1144), `espíritos` (1057), `moral` (934), `espírita` (767), `vida` (700), `espiritual` (639), `homem` (510) — candidatos a novos conceitos ou sinônimos a padronizar.
- **3 blocos de 100 questões do LE com <20% de cobertura**: 201–300 (16/100), 301–400 (7/100), 401–500 (13/100). Priorizar extração de questões-chave desses intervalos para `wiki/questoes/`.

## Páginas referenciadas

- [[index]]
- `log.md`

## Fontes

- Script gerador: `.claude/skills/stats/scripts/stats_wiki.py` (execução em 2026-04-29).
- Corpus analisado: `wiki/**/*.md`, `log.md`, `raw/**/*.md`.
- Dependências: `networkx` (grafo, PageRank), `nltk` (stopwords PT-BR).
- Filtros: meta-páginas (`tipo: sintese` + tag `meta`) são excluídas de grafo, vocabulário, tamanho, cobertura doutrinária e wikilinks quebrados; seções-template (`## Fontes`, `## Páginas relacionadas`, `## Páginas referenciadas`, `## Conceitos relacionados`) são removidas antes da tokenização.
- Cobertura doutrinária: regex sobre citações inline `(LE, q. N)`, `(ESE, cap. X, item Y)`, `(Gênese, cap. X, item Y)`, `(LM, Nª parte, cap. X)`, `(C&I, Nª parte, cap. X)`. Totais canônicos: LE=1019q; ESE=28c; Gênese=18c; LM=33c (2ª parte); C&I=18c (11 + 7).
