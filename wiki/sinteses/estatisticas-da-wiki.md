---
tipo: sintese
fontes: [meta]
tags: [estatisticas, meta, grafo, vocabulario]
atualizado_em: 2026-05-07
status: ativo
---

# Estatísticas da wiki

## Pergunta motivadora

Como a wiki IsAbel está distribuída entre obras, conceitos e entidades? Quais são os nós centrais do grafo, quais páginas estão isoladas, que termos dominam o vocabulário, e como é o ritmo de ingestão ao longo do tempo? Esta página é **regenerada automaticamente** — serve como painel para orientar expansões, backlinks faltantes e possíveis novos conceitos.

> Gerado em **2026-05-07** por `.claude/skills/stats/scripts/stats_wiki.py`.

## Resumo executivo

- Páginas na wiki: **522**
- Arquivos em `raw/`: **1409**
- Nós no grafo: **510** · Arestas: **6118**
- Componentes fracamente conexos: **1** (maior: 510 nós)
- Páginas órfãs (sem backlinks): **1**
- Vocabulário único (após stopwords): **29332** termos
- Entradas em `log.md`: **181**
- Razão conceitos/questões: **189:11** (17.2)
- Questões únicas do LE citadas: **347/1019** (34.1%)
- Wikilinks não resolvidos (freq ≥ 5): **0** targets

## Cobertura por tipo

| Diretório | Páginas |
|-----------|---------|
| `wiki/obras/` | 95 |
| `wiki/conceitos/` | 189 |
| `wiki/personalidades/` | 178 |
| `wiki/questoes/` | 11 |
| `wiki/aprofundamentos/` | 9 |
| `wiki/sinteses/` | 11 |
| `wiki/divergencias/` | 22 |
| `wiki/index.md/` | 1 |
| `wiki/trilhas/` | 6 |

### Status

| Status | Páginas |
|--------|---------|
| `ativo` | 444 |
| `rascunho` | 57 |
| `aberta` | 20 |
| `concluída` | 1 |

## Cobertura doutrinária

Referências únicas do Pentateuco efetivamente citadas pela wiki (`(LE, q. N)`, `(ESE, cap. X, item Y)`, etc.). Mede o quanto da codificação já foi ancorado em páginas próprias.

| Obra | Unidade | Citadas | Total | Cobertura |
|------|---------|--------:|------:|----------:|
| LE | questões | 347 | 1019 | 34.1% |
| ESE | capítulos | 28 | 28 | 100.0% |
| Gênese | capítulos | 14 | 18 | 77.8% |
| LM | capítulos da 2ª parte | 27 | 33 | 81.8% |
| C&I | capítulos | 18 | 18 | 100.0% |

Referências `cap./item` únicas: ESE **138**, Gênese **68**, LM **37**, C&I **18**.

### Cobertura do LE por bloco de 100 questões

```
   1– 100  █████████····················   32/100 (32%)
 101– 200  ████████·····················   28/100 (28%)
 201– 300  █████························   19/100 (19%)
 301– 400  ██···························    8/100 (8%)
 401– 500  █████························   17/100 (17%)
 501– 600  ██████························   20/100 (20%)
 601– 700  █████████████████············   58/100 (58%)
 701– 800  ███████████████··············   53/100 (53%)
 801– 900  ██████████████████···········   62/100 (62%)
 901–1000  ███████████··················   38/100 (38%)
1001–1019  ██████████████████···········   12/19 (63%)
```

## Grafo de conhecimento

### Mais referenciados (grau de entrada)

| # | Página | In |
|---|--------|----|
| 1 | [[wiki/conceitos/reencarnacao]] | 143 |
| 2 | [[wiki/obras/ceu-e-inferno]] | 128 |
| 3 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 125 |
| 4 | [[wiki/conceitos/caridade]] | 115 |
| 5 | [[wiki/conceitos/perispirito]] | 109 |
| 6 | [[wiki/conceitos/obsessao]] | 107 |
| 7 | [[wiki/personalidades/jesus]] | 106 |
| 8 | [[wiki/conceitos/mediunidade]] | 102 |
| 9 | [[wiki/conceitos/prece]] | 98 |
| 10 | [[wiki/conceitos/progresso-espiritual]] | 86 |
| 11 | [[wiki/conceitos/livre-arbitrio]] | 85 |
| 12 | [[wiki/obras/livro-dos-espiritos]] | 79 |
| 13 | [[wiki/obras/genese]] | 75 |
| 14 | [[wiki/conceitos/leis-morais/lei-de-causa-e-efeito]] | 71 |
| 15 | [[wiki/personalidades/allan-kardec]] | 70 |

### Mais conectores (grau de saída)

| # | Página | Out |
|---|--------|-----|
| 1 | [[wiki/obras/revista-espirita]] | 90 |
| 2 | [[wiki/obras/ceu-e-inferno]] | 86 |
| 3 | [[wiki/obras/primeira-epistola-de-pedro]] | 51 |
| 4 | [[wiki/obras/epistola-de-tiago]] | 50 |
| 5 | [[wiki/personalidades/paulo-de-tarso]] | 49 |
| 6 | [[wiki/personalidades/chico-xavier]] | 47 |
| 7 | [[wiki/personalidades/jesus]] | 45 |
| 8 | [[wiki/obras/epistola-aos-romanos]] | 44 |
| 9 | [[wiki/sinteses/parabolas-de-jesus]] | 44 |
| 10 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 42 |
| 11 | [[wiki/obras/segunda-epistola-de-pedro]] | 42 |
| 12 | [[wiki/obras/epistola-aos-galatas]] | 41 |
| 13 | [[wiki/obras/apocalipse]] | 40 |
| 14 | [[wiki/obras/segunda-epistola-aos-corintios]] | 40 |
| 15 | [[wiki/personalidades/allan-kardec]] | 40 |

### Centralidade (PageRank)

| # | Página | PR |
|---|--------|-----|
| 1 | [[wiki/conceitos/reencarnacao]] | 0.0247 |
| 2 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 0.0244 |
| 3 | [[wiki/conceitos/progresso-espiritual]] | 0.0227 |
| 4 | [[wiki/conceitos/livre-arbitrio]] | 0.0165 |
| 5 | [[wiki/obras/ceu-e-inferno]] | 0.0154 |
| 6 | [[wiki/conceitos/perispirito]] | 0.0147 |
| 7 | [[wiki/conceitos/caridade]] | 0.0142 |
| 8 | [[wiki/conceitos/mediunidade]] | 0.0130 |
| 9 | [[wiki/conceitos/obsessao]] | 0.0128 |
| 10 | [[wiki/conceitos/leis-morais/lei-de-justica-amor-e-caridade]] | 0.0128 |
| 11 | [[wiki/obras/livro-dos-espiritos]] | 0.0124 |
| 12 | [[wiki/conceitos/escala-espirita]] | 0.0109 |
| 13 | [[wiki/obras/livro-dos-mediuns]] | 0.0102 |
| 14 | [[wiki/personalidades/jesus]] | 0.0102 |
| 15 | [[wiki/conceitos/lei-natural]] | 0.0100 |

### Páginas órfãs (sem backlinks)

- [[wiki/sinteses/colecao-fonte-viva-emmanuel]]

### Componentes isolados (≤ 2 nós)

_Nenhum._

## Vocabulário

### Top 50 termos

| # | Termo | Ocorrências |
|---|-------|-------------|
| 1 | `kardec` | 2277 |
| 2 | `espírito` | 2259 |
| 3 | `deus` | 2190 |
| 4 | `espíritos` | 1923 |
| 5 | `espírita` | 1848 |
| 6 | `moral` | 1718 |
| 7 | `espiritual` | 1293 |
| 8 | `espiritismo` | 1279 |
| 9 | `vida` | 1258 |
| 10 | `jesus` | 1237 |
| 11 | `cristo` | 992 |
| 12 | `homem` | 987 |
| 13 | `morte` | 921 |
| 14 | `doutrina` | 856 |
| 15 | `amor` | 842 |
| 16 | `leitura` | 825 |
| 17 | `corpo` | 785 |
| 18 | `médium` | 785 |
| 19 | `alma` | 747 |
| 20 | `três` | 743 |
| 21 | `paulo` | 709 |
| 22 | `mundo` | 707 |
| 23 | `terra` | 681 |
| 24 | `caps` | 681 |
| 25 | `caso` | 634 |
| 26 | `obra` | 624 |
| 27 | `caridade` | 605 |
| 28 | `princípio` | 555 |
| 29 | `próprio` | 538 |
| 30 | `toda` | 533 |
| 31 | `contra` | 528 |
| 32 | `item` | 527 |
| 33 | `anos` | 523 |
| 34 | `prece` | 517 |
| 35 | `dois` | 515 |
| 36 | `andré` | 498 |
| 37 | `obras` | 490 |
| 38 | `segundo` | 469 |
| 39 | `antes` | 461 |
| 40 | `mediunidade` | 458 |
| 41 | `espíritas` | 457 |
| 42 | `progresso` | 456 |
| 43 | `prática` | 447 |
| 44 | `chave` | 424 |
| 45 | `reencarnação` | 422 |
| 46 | `senhor` | 411 |
| 47 | `luiz` | 407 |
| 48 | `própria` | 406 |
| 49 | `primeira` | 392 |
| 50 | `estudo` | 391 |

### Top 20 bigramas

| # | Bigrama | Ocorrências |
|---|---------|-------------|
| 1 | `andré luiz` | 407 |
| 2 | `leitura espírita` | 301 |
| 3 | `chico xavier` | 218 |
| 4 | `livre arbítrio` | 212 |
| 5 | `aplicação prática` | 185 |
| 6 | `doutrina espírita` | 175 |
| 7 | `ensino kardec` | 151 |
| 8 | `plano espiritual` | 124 |
| 9 | `jesus cristo` | 121 |
| 10 | `após morte` | 113 |
| 11 | `revista espírita` | 113 |
| 12 | `mundo espiritual` | 108 |
| 13 | `estudo espírita` | 104 |
| 14 | `vida futura` | 102 |
| 15 | `texto integral` | 101 |
| 16 | `emmanuel chico` | 100 |
| 17 | `causa efeito` | 99 |
| 18 | `allan kardec` | 99 |
| 19 | `espírito verdade` | 99 |
| 20 | `dados bibliográficos` | 94 |

## Atividade no tempo

Período coberto: **2026-04** → **2026-05** (2 meses).

### Sparkline por tipo

```
aprofundamento ▁█  total=1
estudo     █▂  total=15
glossario  ▄█  total=3
ingest     █▇  total=98
lint       █▂  total=45
refactor   █▃  total=17
setup      █▁  total=2
```

### Tabela mensal

| Mês | aprofundamento | estudo | glossario | ingest | lint | refactor | setup | Total |
|-----|---|---|---|---|---|---|---|-------|
| 2026-04 | 0 | 12 | 1 | 52 | 36 | 12 | 2 | 115 |
| 2026-05 | 1 | 3 | 2 | 46 | 9 | 5 | 0 | 66 |

### Dias mais ativos

| Data | Entradas |
|------|----------|
| 2026-05-05 | 15 |
| 2026-04-07 | 15 |
| 2026-04-15 | 13 |
| 2026-04-29 | 12 |
| 2026-05-01 | 11 |
| 2026-04-26 | 10 |
| 2026-04-19 | 10 |
| 2026-04-06 | 10 |
| 2026-05-06 | 9 |
| 2026-04-28 | 9 |

## Tamanho das páginas

```
<200        105  ████████████████
200-500     187  ██████████████████████████████
500-1000    135  █████████████████████
1000-2000    57  █████████
>2000        26  ████
```

### Maiores

- [[wiki/obras/apocalipse]] — 4805 palavras
- [[wiki/obras/revista-espirita-1866]] — 4069 palavras
- [[wiki/obras/revista-espirita-1868]] — 3794 palavras
- [[wiki/obras/epistola-aos-galatas]] — 3603 palavras
- [[wiki/obras/primeira-epistola-de-pedro]] — 3564 palavras
- [[wiki/obras/revista-espirita-1865]] — 3559 palavras
- [[wiki/obras/revista-espirita-1867]] — 3519 palavras
- [[wiki/obras/revista-espirita-1863]] — 3227 palavras
- [[wiki/obras/revista-espirita-1864]] — 3220 palavras
- [[wiki/obras/primeira-epistola-de-joao]] — 2981 palavras

### Menores (candidatas a expansão)

- [[wiki/conceitos/pluralidade-das-existencias]] — 82 palavras
- [[wiki/trilhas/esde]] — 87 palavras
- [[wiki/personalidades/vinicius]] — 94 palavras
- [[wiki/personalidades/marques-de-saint-paul]] — 98 palavras
- [[wiki/personalidades/sra-helene-michel]] — 98 palavras
- [[wiki/conceitos/vida-espirita]] — 99 palavras
- [[wiki/personalidades/arrependimento-de-um-dissoluto]] — 100 palavras
- [[wiki/personalidades/francisco-do-espirito-santo-neto]] — 101 palavras
- [[wiki/personalidades/mae-e-seu-filho]] — 102 palavras
- [[wiki/personalidades/o-castigo]] — 102 palavras

## Referências não resolvidas

Wikilinks `[[...]]` cujo target não existe na árvore — candidatos a páginas novas (quando frequentes) ou erros de digitação (quando raros).

_Nenhum wikilink quebrado._

## Sugestões automáticas

- **1 páginas órfãs** (grau de entrada = 0) — considerar adicionar backlinks a partir de conceitos/obras relacionados.
- **Termos frequentes sem página própria**: `kardec` (2277), `espírito` (2259), `espíritos` (1923), `espírita` (1848), `moral` (1718), `espiritual` (1293), `espiritismo` (1279), `vida` (1258) — candidatos a novos conceitos ou sinônimos a padronizar.
- **3 blocos de 100 questões do LE com <20% de cobertura**: 201–300 (19/100), 301–400 (8/100), 401–500 (17/100). Priorizar extração de questões-chave desses intervalos para `wiki/questoes/`.

## Páginas referenciadas

- [[index]]
- `log.md`

## Fontes

- Script gerador: `.claude/skills/stats/scripts/stats_wiki.py` (execução em 2026-05-07).
- Corpus analisado: `wiki/**/*.md`, `log.md`, `raw/**/*.md`.
- Dependências: `networkx` (grafo, PageRank), `nltk` (stopwords PT-BR).
- Filtros: meta-páginas (`tipo: sintese` + tag `meta`) são excluídas de grafo, vocabulário, tamanho, cobertura doutrinária e wikilinks quebrados; seções-template (`## Fontes`, `## Páginas relacionadas`, `## Páginas referenciadas`, `## Conceitos relacionados`) são removidas antes da tokenização.
- Cobertura doutrinária: regex sobre citações inline `(LE, q. N)`, `(ESE, cap. X, item Y)`, `(Gênese, cap. X, item Y)`, `(LM, Nª parte, cap. X)`, `(C&I, Nª parte, cap. X)`. Totais canônicos: LE=1019q; ESE=28c; Gênese=18c; LM=33c (2ª parte); C&I=18c (11 + 7).
