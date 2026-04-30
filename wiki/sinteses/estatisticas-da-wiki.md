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

- Páginas na wiki: **352**
- Arquivos em `raw/`: **1253**
- Nós no grafo: **349** · Arestas: **3626**
- Componentes fracamente conexos: **1** (maior: 349 nós)
- Páginas órfãs (sem backlinks): **0**
- Vocabulário único (após stopwords): **19806** termos
- Entradas em `log.md`: **108**
- Razão conceitos/questões: **147:9** (16.3)
- Questões únicas do LE citadas: **285/1019** (28.0%)
- Wikilinks não resolvidos (freq ≥ 5): **0** targets

## Cobertura por tipo

| Diretório | Páginas |
|-----------|---------|
| `wiki/obras/` | 45 |
| `wiki/conceitos/` | 147 |
| `wiki/personalidades/` | 117 |
| `wiki/questoes/` | 9 |
| `wiki/aprofundamentos/` | 6 |
| `wiki/sinteses/` | 7 |
| `wiki/divergencias/` | 17 |
| `wiki/trilhas/` | 4 |

### Status

| Status | Páginas |
|--------|---------|
| `ativo` | 296 |
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
| 1 | [[wiki/conceitos/reencarnacao]] | 103 |
| 2 | [[wiki/obras/ceu-e-inferno]] | 98 |
| 3 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 93 |
| 4 | [[wiki/conceitos/caridade]] | 86 |
| 5 | [[wiki/conceitos/progresso-espiritual]] | 82 |
| 6 | [[wiki/conceitos/mediunidade]] | 64 |
| 7 | [[wiki/conceitos/livre-arbitrio]] | 60 |
| 8 | [[wiki/conceitos/obsessao]] | 57 |
| 9 | [[wiki/conceitos/perispirito]] | 56 |
| 10 | [[wiki/conceitos/prece]] | 56 |
| 11 | [[wiki/personalidades/jesus]] | 56 |
| 12 | [[wiki/obras/livro-dos-espiritos]] | 53 |
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
| 7 | [[wiki/obras/revista-espirita]] | 42 |
| 8 | [[wiki/obras/epistola-aos-galatas]] | 41 |
| 9 | [[wiki/obras/segunda-epistola-aos-corintios]] | 40 |
| 10 | [[wiki/obras/epistola-aos-efesios]] | 39 |
| 11 | [[wiki/obras/depois-da-morte]] | 37 |
| 12 | [[wiki/personalidades/paulo-de-tarso]] | 37 |
| 13 | [[wiki/obras/evangelho-segundo-lucas]] | 36 |
| 14 | [[wiki/personalidades/jesus]] | 36 |
| 15 | [[wiki/obras/livro-dos-espiritos]] | 35 |

### Centralidade (PageRank)

| # | Página | PR |
|---|--------|-----|
| 1 | [[wiki/conceitos/progresso-espiritual]] | 0.0306 |
| 2 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 0.0302 |
| 3 | [[wiki/conceitos/reencarnacao]] | 0.0285 |
| 4 | [[wiki/conceitos/livre-arbitrio]] | 0.0214 |
| 5 | [[wiki/obras/ceu-e-inferno]] | 0.0175 |
| 6 | [[wiki/conceitos/caridade]] | 0.0167 |
| 7 | [[wiki/conceitos/lei-de-justica-amor-e-caridade]] | 0.0157 |
| 8 | [[wiki/obras/livro-dos-espiritos]] | 0.0151 |
| 9 | [[wiki/conceitos/lei-natural]] | 0.0149 |
| 10 | [[wiki/conceitos/perispirito]] | 0.0140 |
| 11 | [[wiki/conceitos/mediunidade]] | 0.0138 |
| 12 | [[wiki/conceitos/morte]] | 0.0126 |
| 13 | [[wiki/conceitos/obsessao]] | 0.0122 |
| 14 | [[wiki/conceitos/penas-e-gozos-futuros]] | 0.0122 |
| 15 | [[wiki/conceitos/escala-espirita]] | 0.0122 |

### Páginas órfãs (sem backlinks)

_Nenhuma página órfã._

### Componentes isolados (≤ 2 nós)

_Nenhum._

## Vocabulário

### Top 50 termos

| # | Termo | Ocorrências |
|---|-------|-------------|
| 1 | `deus` | 1465 |
| 2 | `espírito` | 1349 |
| 3 | `kardec` | 1272 |
| 4 | `espíritos` | 1183 |
| 5 | `moral` | 1068 |
| 6 | `espírita` | 900 |
| 7 | `vida` | 762 |
| 8 | `espiritual` | 693 |
| 9 | `jesus` | 666 |
| 10 | `homem` | 627 |
| 11 | `cristo` | 602 |
| 12 | `espiritismo` | 486 |
| 13 | `amor` | 453 |
| 14 | `corpo` | 449 |
| 15 | `paulo` | 448 |
| 16 | `morte` | 443 |
| 17 | `caridade` | 434 |
| 18 | `leitura` | 427 |
| 19 | `alma` | 422 |
| 20 | `doutrina` | 415 |
| 21 | `mundo` | 393 |
| 22 | `caps` | 365 |
| 23 | `três` | 358 |
| 24 | `terra` | 344 |
| 25 | `obras` | 338 |
| 26 | `item` | 331 |
| 27 | `progresso` | 310 |
| 28 | `toda` | 306 |
| 29 | `princípio` | 304 |
| 30 | `prática` | 297 |
| 31 | `prece` | 296 |
| 32 | `justiça` | 295 |
| 33 | `segundo` | 293 |
| 34 | `médium` | 290 |
| 35 | `próprio` | 287 |
| 36 | `contra` | 275 |
| 37 | `obra` | 274 |
| 38 | `natureza` | 261 |
| 39 | `andré` | 250 |
| 40 | `antes` | 246 |
| 41 | `ensino` | 243 |
| 42 | `parábola` | 243 |
| 43 | `evangelho` | 239 |
| 44 | `sofrimento` | 229 |
| 45 | `estado` | 227 |
| 46 | `passagem` | 226 |
| 47 | `mundos` | 223 |
| 48 | `senhor` | 220 |
| 49 | `filho` | 220 |
| 50 | `dois` | 219 |

### Top 20 bigramas

| # | Bigrama | Ocorrências |
|---|---------|-------------|
| 1 | `andré luiz` | 182 |
| 2 | `leitura espírita` | 173 |
| 3 | `aplicação prática` | 132 |
| 4 | `ensino kardec` | 123 |
| 5 | `livre arbítrio` | 120 |
| 6 | `mundo espiritual` | 101 |
| 7 | `doutrina espírita` | 92 |
| 8 | `chico xavier` | 89 |
| 9 | `após morte` | 75 |
| 10 | `vida futura` | 75 |
| 11 | `jesus cristo` | 67 |
| 12 | `estudo espírita` | 64 |
| 13 | `espírito verdade` | 62 |
| 14 | `caridade salvação` | 59 |
| 15 | `plano espiritual` | 58 |
| 16 | `causa efeito` | 58 |
| 17 | `justiça divina` | 57 |
| 18 | `léon denis` | 56 |
| 19 | `situação mundo` | 56 |
| 20 | `lições principais` | 56 |

## Atividade no tempo

Período coberto: **2026-04** → **2026-04** (1 meses).

### Sparkline por tipo

```
estudo     █  total=12
glossario  █  total=1
ingest     █  total=49
lint       █  total=33
refactor   █  total=11
setup      █  total=2
```

### Tabela mensal

| Mês | estudo | glossario | ingest | lint | refactor | setup | Total |
|-----|---|---|---|---|---|---|-------|
| 2026-04 | 12 | 1 | 49 | 33 | 11 | 2 | 108 |

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
<200        114  █████████████████████████
200-500     133  ██████████████████████████████
500-1000     64  ██████████████
1000-2000    29  ██████
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

- **Termos frequentes sem página própria**: `espírito` (1349), `kardec` (1272), `espíritos` (1183), `moral` (1068), `espírita` (900), `vida` (762), `espiritual` (693), `homem` (627) — candidatos a novos conceitos ou sinônimos a padronizar.
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
