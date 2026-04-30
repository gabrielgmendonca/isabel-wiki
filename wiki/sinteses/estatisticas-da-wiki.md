---
tipo: sintese
fontes: [meta]
tags: [estatisticas, meta, grafo, vocabulario]
atualizado_em: 2026-04-30
status: ativo
---

# Estatísticas da wiki

## Pergunta motivadora

Como a wiki IsAbel está distribuída entre obras, conceitos e entidades? Quais são os nós centrais do grafo, quais páginas estão isoladas, que termos dominam o vocabulário, e como é o ritmo de ingestão ao longo do tempo? Esta página é **regenerada automaticamente** — serve como painel para orientar expansões, backlinks faltantes e possíveis novos conceitos.

> Gerado em **2026-04-30** por `.claude/skills/stats/scripts/stats_wiki.py`.

## Resumo executivo

- Páginas na wiki: **371**
- Arquivos em `raw/`: **1249**
- Nós no grafo: **368** · Arestas: **3884**
- Componentes fracamente conexos: **1** (maior: 368 nós)
- Páginas órfãs (sem backlinks): **0**
- Vocabulário único (após stopwords): **20848** termos
- Entradas em `log.md`: **113**
- Razão conceitos/questões: **154:9** (17.1)
- Questões únicas do LE citadas: **340/1019** (33.4%)
- Wikilinks não resolvidos (freq ≥ 5): **0** targets

## Cobertura por tipo

| Diretório | Páginas |
|-----------|---------|
| `wiki/obras/` | 47 |
| `wiki/conceitos/` | 154 |
| `wiki/personalidades/` | 126 |
| `wiki/questoes/` | 9 |
| `wiki/aprofundamentos/` | 6 |
| `wiki/sinteses/` | 7 |
| `wiki/divergencias/` | 18 |
| `wiki/trilhas/` | 4 |

### Status

| Status | Páginas |
|--------|---------|
| `ativo` | 314 |
| `rascunho` | 39 |
| `aberta` | 17 |
| `concluída` | 1 |

## Cobertura doutrinária

Referências únicas do Pentateuco efetivamente citadas pela wiki (`(LE, q. N)`, `(ESE, cap. X, item Y)`, etc.). Mede o quanto da codificação já foi ancorado em páginas próprias.

| Obra | Unidade | Citadas | Total | Cobertura |
|------|---------|--------:|------:|----------:|
| LE | questões | 340 | 1019 | 33.4% |
| ESE | capítulos | 28 | 28 | 100.0% |
| Gênese | capítulos | 14 | 18 | 77.8% |
| LM | capítulos da 2ª parte | 26 | 33 | 78.8% |
| C&I | capítulos | 18 | 18 | 100.0% |

Referências `cap./item` únicas: ESE **137**, Gênese **68**, LM **35**, C&I **18**.

### Cobertura do LE por bloco de 100 questões

```
   1– 100  █████████····················   32/100 (32%)
 101– 200  ████████·····················   28/100 (28%)
 201– 300  █████························   19/100 (19%)
 301– 400  ██···························    8/100 (8%)
 401– 500  ███··························   13/100 (13%)
 501– 600  ██████························   20/100 (20%)
 601– 700  █████████████████············   58/100 (58%)
 701– 800  ███████████████··············   52/100 (52%)
 801– 900  ██████████████████···········   62/100 (62%)
 901–1000  ██████████···················   36/100 (36%)
1001–1019  ██████████████████···········   12/19 (63%)
```

## Grafo de conhecimento

### Mais referenciados (grau de entrada)

| # | Página | In |
|---|--------|----|
| 1 | [[wiki/conceitos/reencarnacao]] | 107 |
| 2 | [[wiki/obras/ceu-e-inferno]] | 99 |
| 3 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 93 |
| 4 | [[wiki/conceitos/caridade]] | 89 |
| 5 | [[wiki/conceitos/progresso-espiritual]] | 82 |
| 6 | [[wiki/conceitos/mediunidade]] | 66 |
| 7 | [[wiki/conceitos/perispirito]] | 62 |
| 8 | [[wiki/conceitos/livre-arbitrio]] | 61 |
| 9 | [[wiki/conceitos/prece]] | 61 |
| 10 | [[wiki/personalidades/jesus]] | 59 |
| 11 | [[wiki/conceitos/obsessao]] | 58 |
| 12 | [[wiki/obras/livro-dos-espiritos]] | 56 |
| 13 | [[wiki/conceitos/lei-de-justica-amor-e-caridade]] | 52 |
| 14 | [[wiki/conceitos/lei-de-causa-e-efeito]] | 48 |
| 15 | [[wiki/conceitos/expiacao-e-reparacao]] | 45 |

### Mais conectores (grau de saída)

| # | Página | Out |
|---|--------|-----|
| 1 | [[wiki/obras/ceu-e-inferno]] | 85 |
| 2 | [[wiki/obras/revista-espirita]] | 59 |
| 3 | [[wiki/obras/primeira-epistola-de-pedro]] | 51 |
| 4 | [[wiki/obras/epistola-de-tiago]] | 50 |
| 5 | [[wiki/obras/epistola-aos-romanos]] | 44 |
| 6 | [[wiki/sinteses/parabolas-de-jesus]] | 44 |
| 7 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 42 |
| 8 | [[wiki/personalidades/paulo-de-tarso]] | 42 |
| 9 | [[wiki/obras/epistola-aos-galatas]] | 41 |
| 10 | [[wiki/obras/segunda-epistola-aos-corintios]] | 40 |
| 11 | [[wiki/obras/epistola-aos-efesios]] | 39 |
| 12 | [[wiki/personalidades/jesus]] | 39 |
| 13 | [[wiki/obras/depois-da-morte]] | 37 |
| 14 | [[wiki/obras/evangelho-segundo-lucas]] | 36 |
| 15 | [[wiki/obras/livro-dos-espiritos]] | 35 |

### Centralidade (PageRank)

| # | Página | PR |
|---|--------|-----|
| 1 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 0.0293 |
| 2 | [[wiki/conceitos/progresso-espiritual]] | 0.0292 |
| 3 | [[wiki/conceitos/reencarnacao]] | 0.0287 |
| 4 | [[wiki/conceitos/livre-arbitrio]] | 0.0196 |
| 5 | [[wiki/obras/ceu-e-inferno]] | 0.0174 |
| 6 | [[wiki/conceitos/caridade]] | 0.0164 |
| 7 | [[wiki/conceitos/lei-de-justica-amor-e-caridade]] | 0.0155 |
| 8 | [[wiki/obras/livro-dos-espiritos]] | 0.0148 |
| 9 | [[wiki/conceitos/perispirito]] | 0.0141 |
| 10 | [[wiki/conceitos/mediunidade]] | 0.0136 |
| 11 | [[wiki/conceitos/lei-natural]] | 0.0126 |
| 12 | [[wiki/conceitos/morte]] | 0.0124 |
| 13 | [[wiki/conceitos/escala-espirita]] | 0.0124 |
| 14 | [[wiki/conceitos/obsessao]] | 0.0121 |
| 15 | [[wiki/conceitos/penas-e-gozos-futuros]] | 0.0121 |

### Páginas órfãs (sem backlinks)

_Nenhuma página órfã._

### Componentes isolados (≤ 2 nós)

_Nenhum._

## Vocabulário

### Top 50 termos

| # | Termo | Ocorrências |
|---|-------|-------------|
| 1 | `deus` | 1635 |
| 2 | `espírito` | 1534 |
| 3 | `kardec` | 1405 |
| 4 | `espíritos` | 1294 |
| 5 | `moral` | 1138 |
| 6 | `espírita` | 1002 |
| 7 | `vida` | 819 |
| 8 | `jesus` | 777 |
| 9 | `espiritual` | 733 |
| 10 | `homem` | 719 |
| 11 | `cristo` | 718 |
| 12 | `espiritismo` | 558 |
| 13 | `corpo` | 514 |
| 14 | `paulo` | 501 |
| 15 | `morte` | 485 |
| 16 | `leitura` | 467 |
| 17 | `amor` | 466 |
| 18 | `alma` | 465 |
| 19 | `doutrina` | 456 |
| 20 | `caridade` | 451 |
| 21 | `mundo` | 418 |
| 22 | `terra` | 401 |
| 23 | `três` | 394 |
| 24 | `caps` | 381 |
| 25 | `progresso` | 354 |
| 26 | `obras` | 351 |
| 27 | `item` | 345 |
| 28 | `princípio` | 344 |
| 29 | `toda` | 334 |
| 30 | `médium` | 330 |
| 31 | `prece` | 328 |
| 32 | `prática` | 325 |
| 33 | `segundo` | 314 |
| 34 | `próprio` | 307 |
| 35 | `justiça` | 306 |
| 36 | `contra` | 300 |
| 37 | `obra` | 295 |
| 38 | `natureza` | 294 |
| 39 | `antes` | 279 |
| 40 | `caso` | 278 |
| 41 | `tudo` | 266 |
| 42 | `estado` | 259 |
| 43 | `andré` | 259 |
| 44 | `ensino` | 259 |
| 45 | `casa` | 254 |
| 46 | `evangelho` | 252 |
| 47 | `senhor` | 250 |
| 48 | `sempre` | 247 |
| 49 | `filho` | 247 |
| 50 | `passagem` | 246 |

### Top 20 bigramas

| # | Bigrama | Ocorrências |
|---|---------|-------------|
| 1 | `andré luiz` | 191 |
| 2 | `leitura espírita` | 186 |
| 3 | `aplicação prática` | 142 |
| 4 | `livre arbítrio` | 134 |
| 5 | `ensino kardec` | 129 |
| 6 | `doutrina espírita` | 104 |
| 7 | `mundo espiritual` | 101 |
| 8 | `chico xavier` | 92 |
| 9 | `jesus cristo` | 87 |
| 10 | `vida futura` | 76 |
| 11 | `após morte` | 75 |
| 12 | `estudo espírita` | 74 |
| 13 | `espírito verdade` | 62 |
| 14 | `livro espíritos` | 61 |
| 15 | `plano espiritual` | 59 |
| 16 | `causa efeito` | 59 |
| 17 | `caridade salvação` | 59 |
| 18 | `justiça divina` | 57 |
| 19 | `léon denis` | 57 |
| 20 | `pluralidade existências` | 56 |

## Atividade no tempo

Período coberto: **2026-04** → **2026-04** (1 meses).

### Sparkline por tipo

```
estudo     █  total=12
glossario  █  total=1
ingest     █  total=51
lint       █  total=35
refactor   █  total=12
setup      █  total=2
```

### Tabela mensal

| Mês | estudo | glossario | ingest | lint | refactor | setup | Total |
|-----|---|---|---|---|---|---|-------|
| 2026-04 | 12 | 1 | 51 | 35 | 12 | 2 | 113 |

### Dias mais ativos

| Data | Entradas |
|------|----------|
| 2026-04-07 | 15 |
| 2026-04-15 | 13 |
| 2026-04-29 | 12 |
| 2026-04-26 | 10 |
| 2026-04-19 | 10 |
| 2026-04-06 | 10 |
| 2026-04-28 | 9 |
| 2026-04-27 | 8 |
| 2026-04-21 | 6 |
| 2026-04-16 | 6 |

## Tamanho das páginas

```
<200        107  ██████████████████████
200-500     145  ██████████████████████████████
500-1000     74  ███████████████
1000-2000    31  ██████
>2000        11  ██
```

### Maiores

- [[wiki/obras/epistola-aos-galatas]] — 3603 palavras
- [[wiki/obras/primeira-epistola-de-pedro]] — 3564 palavras
- [[wiki/obras/primeira-epistola-de-joao]] — 2981 palavras
- [[wiki/obras/epistola-aos-filipenses]] — 2753 palavras
- [[wiki/obras/epistola-aos-efesios]] — 2538 palavras
- [[wiki/obras/revista-espirita-1860]] — 2508 palavras
- [[wiki/obras/epistola-aos-romanos]] — 2305 palavras
- [[wiki/obras/epistola-de-tiago]] — 2295 palavras
- [[wiki/obras/epistola-aos-hebreus]] — 2278 palavras
- [[wiki/aprofundamentos/expiacao-e-arrependimento]] — 2238 palavras

### Menores (candidatas a expansão)

- [[wiki/conceitos/pluralidade-das-existencias]] — 82 palavras
- [[wiki/trilhas/esde]] — 87 palavras
- [[wiki/personalidades/vinicius]] — 94 palavras
- [[wiki/personalidades/erasto]] — 97 palavras
- [[wiki/personalidades/marques-de-saint-paul]] — 98 palavras
- [[wiki/personalidades/sra-helene-michel]] — 98 palavras
- [[wiki/conceitos/vida-espirita]] — 99 palavras
- [[wiki/personalidades/arrependimento-de-um-dissoluto]] — 100 palavras
- [[wiki/personalidades/francisco-do-espirito-santo-neto]] — 101 palavras
- [[wiki/personalidades/mae-e-seu-filho]] — 102 palavras

## Referências não resolvidas

Wikilinks `[[...]]` cujo target não existe na árvore — candidatos a páginas novas (quando frequentes) ou erros de digitação (quando raros).

_Nenhum wikilink quebrado._

## Sugestões automáticas

- **Termos frequentes sem página própria**: `espírito` (1534), `kardec` (1405), `espíritos` (1294), `moral` (1138), `espírita` (1002), `vida` (819), `espiritual` (733), `homem` (719) — candidatos a novos conceitos ou sinônimos a padronizar.
- **3 blocos de 100 questões do LE com <20% de cobertura**: 201–300 (19/100), 301–400 (8/100), 401–500 (13/100). Priorizar extração de questões-chave desses intervalos para `wiki/questoes/`.

## Páginas referenciadas

- [[index]]
- `log.md`

## Fontes

- Script gerador: `.claude/skills/stats/scripts/stats_wiki.py` (execução em 2026-04-30).
- Corpus analisado: `wiki/**/*.md`, `log.md`, `raw/**/*.md`.
- Dependências: `networkx` (grafo, PageRank), `nltk` (stopwords PT-BR).
- Filtros: meta-páginas (`tipo: sintese` + tag `meta`) são excluídas de grafo, vocabulário, tamanho, cobertura doutrinária e wikilinks quebrados; seções-template (`## Fontes`, `## Páginas relacionadas`, `## Páginas referenciadas`, `## Conceitos relacionados`) são removidas antes da tokenização.
- Cobertura doutrinária: regex sobre citações inline `(LE, q. N)`, `(ESE, cap. X, item Y)`, `(Gênese, cap. X, item Y)`, `(LM, Nª parte, cap. X)`, `(C&I, Nª parte, cap. X)`. Totais canônicos: LE=1019q; ESE=28c; Gênese=18c; LM=33c (2ª parte); C&I=18c (11 + 7).
