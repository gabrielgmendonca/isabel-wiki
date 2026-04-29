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

- Páginas na wiki: **336**
- Arquivos em `raw/`: **1249**
- Nós no grafo: **333** · Arestas: **3466**
- Componentes fracamente conexos: **1** (maior: 333 nós)
- Páginas órfãs (sem backlinks): **1**
- Vocabulário único (após stopwords): **19007** termos
- Entradas em `log.md`: **105**
- Razão conceitos/questões: **144:9** (16.0)
- Questões únicas do LE citadas: **285/1019** (28.0%)
- Wikilinks não resolvidos (freq ≥ 5): **0** targets

## Cobertura por tipo

| Diretório | Páginas |
|-----------|---------|
| `wiki/obras/` | 43 |
| `wiki/conceitos/` | 144 |
| `wiki/personalidades/` | 106 |
| `wiki/questoes/` | 9 |
| `wiki/aprofundamentos/` | 6 |
| `wiki/sinteses/` | 7 |
| `wiki/divergencias/` | 17 |
| `wiki/trilhas/` | 4 |

### Status

| Status | Páginas |
|--------|---------|
| `ativo` | 280 |
| `rascunho` | 39 |
| `aberta` | 16 |
| `concluída` | 1 |

## Cobertura doutrinária

Referências únicas do Pentateuco efetivamente citadas pela wiki (`(LE, q. N)`, `(ESE, cap. X, item Y)`, etc.). Mede o quanto da codificação já foi ancorado em páginas próprias.

| Obra | Unidade | Citadas | Total | Cobertura |
|------|---------|--------:|------:|----------:|
| LE | questões | 285 | 1019 | 28.0% |
| ESE | capítulos | 28 | 28 | 100.0% |
| Gênese | capítulos | 14 | 18 | 77.8% |
| LM | capítulos da 2ª parte | 26 | 33 | 78.8% |
| C&I | capítulos | 18 | 18 | 100.0% |

Referências `cap./item` únicas: ESE **137**, Gênese **68**, LM **35**, C&I **18**.

### Cobertura do LE por bloco de 100 questões

```
   1– 100  █████████····················   32/100 (32%)
 101– 200  ████████·····················   28/100 (28%)
 201– 300  █████························   17/100 (17%)
 301– 400  ██···························    8/100 (8%)
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
| 1 | [[wiki/obras/ceu-e-inferno]] | 98 |
| 2 | [[wiki/conceitos/reencarnacao]] | 97 |
| 3 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 93 |
| 4 | [[wiki/conceitos/caridade]] | 85 |
| 5 | [[wiki/conceitos/progresso-espiritual]] | 82 |
| 6 | [[wiki/conceitos/livre-arbitrio]] | 59 |
| 7 | [[wiki/conceitos/mediunidade]] | 59 |
| 8 | [[wiki/personalidades/jesus]] | 56 |
| 9 | [[wiki/conceitos/obsessao]] | 55 |
| 10 | [[wiki/conceitos/prece]] | 55 |
| 11 | [[wiki/obras/livro-dos-espiritos]] | 53 |
| 12 | [[wiki/conceitos/perispirito]] | 52 |
| 13 | [[wiki/conceitos/lei-de-justica-amor-e-caridade]] | 51 |
| 14 | [[wiki/conceitos/lei-de-causa-e-efeito]] | 47 |
| 15 | [[wiki/conceitos/expiacao-e-reparacao]] | 45 |

### Mais conectores (grau de saída)

| # | Página | Out |
|---|--------|-----|
| 1 | [[wiki/obras/ceu-e-inferno]] | 85 |
| 2 | [[wiki/obras/primeira-epistola-de-pedro]] | 51 |
| 3 | [[wiki/obras/epistola-de-tiago]] | 50 |
| 4 | [[wiki/obras/epistola-aos-romanos]] | 44 |
| 5 | [[wiki/sinteses/parabolas-de-jesus]] | 44 |
| 6 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 42 |
| 7 | [[wiki/obras/epistola-aos-galatas]] | 41 |
| 8 | [[wiki/obras/segunda-epistola-aos-corintios]] | 40 |
| 9 | [[wiki/obras/epistola-aos-efesios]] | 39 |
| 10 | [[wiki/obras/depois-da-morte]] | 37 |
| 11 | [[wiki/personalidades/paulo-de-tarso]] | 37 |
| 12 | [[wiki/obras/evangelho-segundo-lucas]] | 36 |
| 13 | [[wiki/personalidades/jesus]] | 36 |
| 14 | [[wiki/obras/livro-dos-espiritos]] | 35 |
| 15 | [[wiki/obras/epistola-aos-hebreus]] | 34 |

### Centralidade (PageRank)

| # | Página | PR |
|---|--------|-----|
| 1 | [[wiki/conceitos/progresso-espiritual]] | 0.0313 |
| 2 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 0.0309 |
| 3 | [[wiki/conceitos/reencarnacao]] | 0.0284 |
| 4 | [[wiki/conceitos/livre-arbitrio]] | 0.0218 |
| 5 | [[wiki/obras/ceu-e-inferno]] | 0.0180 |
| 6 | [[wiki/conceitos/caridade]] | 0.0171 |
| 7 | [[wiki/conceitos/lei-de-justica-amor-e-caridade]] | 0.0161 |
| 8 | [[wiki/obras/livro-dos-espiritos]] | 0.0159 |
| 9 | [[wiki/conceitos/lei-natural]] | 0.0153 |
| 10 | [[wiki/conceitos/perispirito]] | 0.0136 |
| 11 | [[wiki/conceitos/mediunidade]] | 0.0136 |
| 12 | [[wiki/conceitos/morte]] | 0.0129 |
| 13 | [[wiki/conceitos/penas-e-gozos-futuros]] | 0.0126 |
| 14 | [[wiki/conceitos/obsessao]] | 0.0123 |
| 15 | [[wiki/conceitos/vida-espirita]] | 0.0121 |

### Páginas órfãs (sem backlinks)

- [[wiki/obras/revista-espirita]]

### Componentes isolados (≤ 2 nós)

_Nenhum._

## Vocabulário

### Top 50 termos

| # | Termo | Ocorrências |
|---|-------|-------------|
| 1 | `deus` | 1440 |
| 2 | `espírito` | 1263 |
| 3 | `kardec` | 1180 |
| 4 | `espíritos` | 1092 |
| 5 | `moral` | 1044 |
| 6 | `espírita` | 838 |
| 7 | `vida` | 732 |
| 8 | `espiritual` | 675 |
| 9 | `jesus` | 664 |
| 10 | `homem` | 624 |
| 11 | `cristo` | 599 |
| 12 | `espiritismo` | 464 |
| 13 | `amor` | 452 |
| 14 | `paulo` | 444 |
| 15 | `corpo` | 435 |
| 16 | `morte` | 431 |
| 17 | `caridade` | 430 |
| 18 | `leitura` | 424 |
| 19 | `alma` | 410 |
| 20 | `doutrina` | 383 |
| 21 | `mundo` | 377 |
| 22 | `caps` | 364 |
| 23 | `terra` | 332 |
| 24 | `item` | 328 |
| 25 | `três` | 316 |
| 26 | `obras` | 314 |
| 27 | `progresso` | 307 |
| 28 | `toda` | 298 |
| 29 | `princípio` | 296 |
| 30 | `justiça` | 294 |
| 31 | `prece` | 292 |
| 32 | `prática` | 292 |
| 33 | `segundo` | 283 |
| 34 | `próprio` | 269 |
| 35 | `contra` | 265 |
| 36 | `obra` | 256 |
| 37 | `natureza` | 251 |
| 38 | `andré` | 250 |
| 39 | `médium` | 248 |
| 40 | `parábola` | 243 |
| 41 | `ensino` | 236 |
| 42 | `evangelho` | 234 |
| 43 | `antes` | 231 |
| 44 | `passagem` | 226 |
| 45 | `sofrimento` | 226 |
| 46 | `estado` | 219 |
| 47 | `senhor` | 214 |
| 48 | `filho` | 213 |
| 49 | `sempre` | 209 |
| 50 | `casa` | 207 |

### Top 20 bigramas

| # | Bigrama | Ocorrências |
|---|---------|-------------|
| 1 | `andré luiz` | 182 |
| 2 | `leitura espírita` | 173 |
| 3 | `aplicação prática` | 128 |
| 4 | `ensino kardec` | 120 |
| 5 | `livre arbítrio` | 117 |
| 6 | `mundo espiritual` | 99 |
| 7 | `doutrina espírita` | 89 |
| 8 | `chico xavier` | 89 |
| 9 | `vida futura` | 75 |
| 10 | `após morte` | 72 |
| 11 | `jesus cristo` | 67 |
| 12 | `estudo espírita` | 64 |
| 13 | `espírito verdade` | 62 |
| 14 | `caridade salvação` | 59 |
| 15 | `causa efeito` | 58 |
| 16 | `justiça divina` | 57 |
| 17 | `plano espiritual` | 57 |
| 18 | `léon denis` | 56 |
| 19 | `situação mundo` | 56 |
| 20 | `lições principais` | 56 |

## Atividade no tempo

Período coberto: **2026-04** → **2026-04** (1 meses).

### Sparkline por tipo

```
estudo     █  total=12
glossario  █  total=1
ingest     █  total=47
lint       █  total=32
refactor   █  total=11
setup      █  total=2
```

### Tabela mensal

| Mês | estudo | glossario | ingest | lint | refactor | setup | Total |
|-----|---|---|---|---|---|---|-------|
| 2026-04 | 12 | 1 | 47 | 32 | 11 | 2 | 105 |

### Dias mais ativos

| Data | Entradas |
|------|----------|
| 2026-04-07 | 15 |
| 2026-04-15 | 13 |
| 2026-04-26 | 10 |
| 2026-04-19 | 10 |
| 2026-04-06 | 10 |
| 2026-04-29 | 9 |
| 2026-04-28 | 9 |
| 2026-04-27 | 8 |
| 2026-04-21 | 6 |
| 2026-04-16 | 6 |

## Tamanho das páginas

```
<200        117  ██████████████████████████████
200-500     117  ██████████████████████████████
500-1000     63  ████████████████
1000-2000    27  ██████
>2000         9  ██
```

### Maiores

- [[wiki/obras/epistola-aos-galatas]] — 3603 palavras
- [[wiki/obras/primeira-epistola-de-pedro]] — 3564 palavras
- [[wiki/obras/primeira-epistola-de-joao]] — 2981 palavras
- [[wiki/obras/epistola-aos-efesios]] — 2538 palavras
- [[wiki/obras/epistola-aos-romanos]] — 2305 palavras
- [[wiki/obras/epistola-de-tiago]] — 2295 palavras
- [[wiki/obras/epistola-aos-hebreus]] — 2278 palavras
- [[wiki/aprofundamentos/expiacao-e-arrependimento]] — 2238 palavras
- [[wiki/obras/segunda-epistola-aos-corintios]] — 2129 palavras
- [[wiki/obras/obreiros-da-vida-eterna]] — 1883 palavras

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

- **1 páginas órfãs** (grau de entrada = 0) — considerar adicionar backlinks a partir de conceitos/obras relacionados.
- **Termos frequentes sem página própria**: `espírito` (1263), `kardec` (1180), `espíritos` (1092), `moral` (1044), `espírita` (838), `vida` (732), `espiritual` (675), `homem` (624) — candidatos a novos conceitos ou sinônimos a padronizar.
- **3 blocos de 100 questões do LE com <20% de cobertura**: 201–300 (17/100), 301–400 (8/100), 401–500 (13/100). Priorizar extração de questões-chave desses intervalos para `wiki/questoes/`.

## Páginas referenciadas

- [[index]]
- `log.md`

## Fontes

- Script gerador: `.claude/skills/stats/scripts/stats_wiki.py` (execução em 2026-04-29).
- Corpus analisado: `wiki/**/*.md`, `log.md`, `raw/**/*.md`.
- Dependências: `networkx` (grafo, PageRank), `nltk` (stopwords PT-BR).
- Filtros: meta-páginas (`tipo: sintese` + tag `meta`) são excluídas de grafo, vocabulário, tamanho, cobertura doutrinária e wikilinks quebrados; seções-template (`## Fontes`, `## Páginas relacionadas`, `## Páginas referenciadas`, `## Conceitos relacionados`) são removidas antes da tokenização.
- Cobertura doutrinária: regex sobre citações inline `(LE, q. N)`, `(ESE, cap. X, item Y)`, `(Gênese, cap. X, item Y)`, `(LM, Nª parte, cap. X)`, `(C&I, Nª parte, cap. X)`. Totais canônicos: LE=1019q; ESE=28c; Gênese=18c; LM=33c (2ª parte); C&I=18c (11 + 7).
