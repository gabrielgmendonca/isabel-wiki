---
tipo: sintese
fontes: [meta]
tags: [estatisticas, meta, grafo, vocabulario]
atualizado_em: 2026-05-05
status: ativo
---

# Estatísticas da wiki

## Pergunta motivadora

Como a wiki IsAbel está distribuída entre obras, conceitos e entidades? Quais são os nós centrais do grafo, quais páginas estão isoladas, que termos dominam o vocabulário, e como é o ritmo de ingestão ao longo do tempo? Esta página é **regenerada automaticamente** — serve como painel para orientar expansões, backlinks faltantes e possíveis novos conceitos.

> Gerado em **2026-05-05** por `.claude/skills/stats/scripts/stats_wiki.py`.

## Resumo executivo

- Páginas na wiki: **472**
- Arquivos em `raw/`: **1394**
- Nós no grafo: **460** · Arestas: **5378**
- Componentes fracamente conexos: **1** (maior: 460 nós)
- Páginas órfãs (sem backlinks): **0**
- Vocabulário único (após stopwords): **27000** termos
- Entradas em `log.md`: **155**
- Razão conceitos/questões: **178:11** (16.2)
- Questões únicas do LE citadas: **347/1019** (34.1%)
- Wikilinks não resolvidos (freq ≥ 5): **0** targets

## Cobertura por tipo

| Diretório | Páginas |
|-----------|---------|
| `wiki/obras/` | 76 |
| `wiki/conceitos/` | 178 |
| `wiki/personalidades/` | 159 |
| `wiki/questoes/` | 11 |
| `wiki/aprofundamentos/` | 9 |
| `wiki/sinteses/` | 10 |
| `wiki/divergencias/` | 22 |
| `wiki/index.md/` | 1 |
| `wiki/trilhas/` | 6 |

### Status

| Status | Páginas |
|--------|---------|
| `ativo` | 389 |
| `rascunho` | 62 |
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

Referências `cap./item` únicas: ESE **137**, Gênese **68**, LM **37**, C&I **18**.

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
| 1 | [[wiki/conceitos/reencarnacao]] | 127 |
| 2 | [[wiki/obras/ceu-e-inferno]] | 122 |
| 3 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 115 |
| 4 | [[wiki/conceitos/caridade]] | 108 |
| 5 | [[wiki/conceitos/mediunidade]] | 98 |
| 6 | [[wiki/conceitos/perispirito]] | 98 |
| 7 | [[wiki/conceitos/obsessao]] | 94 |
| 8 | [[wiki/conceitos/prece]] | 88 |
| 9 | [[wiki/personalidades/jesus]] | 86 |
| 10 | [[wiki/conceitos/progresso-espiritual]] | 84 |
| 11 | [[wiki/conceitos/livre-arbitrio]] | 78 |
| 12 | [[wiki/obras/livro-dos-espiritos]] | 71 |
| 13 | [[wiki/obras/genese]] | 69 |
| 14 | [[wiki/conceitos/leis-morais/lei-de-causa-e-efeito]] | 68 |
| 15 | [[wiki/conceitos/leis-morais/lei-de-justica-amor-e-caridade]] | 60 |

### Mais conectores (grau de saída)

| # | Página | Out |
|---|--------|-----|
| 1 | [[wiki/obras/revista-espirita]] | 90 |
| 2 | [[wiki/obras/ceu-e-inferno]] | 86 |
| 3 | [[wiki/obras/primeira-epistola-de-pedro]] | 51 |
| 4 | [[wiki/obras/epistola-de-tiago]] | 50 |
| 5 | [[wiki/personalidades/paulo-de-tarso]] | 47 |
| 6 | [[wiki/obras/epistola-aos-romanos]] | 44 |
| 7 | [[wiki/sinteses/parabolas-de-jesus]] | 44 |
| 8 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 42 |
| 9 | [[wiki/personalidades/jesus]] | 42 |
| 10 | [[wiki/obras/epistola-aos-galatas]] | 41 |
| 11 | [[wiki/obras/segunda-epistola-de-pedro]] | 41 |
| 12 | [[wiki/obras/apocalipse]] | 40 |
| 13 | [[wiki/obras/segunda-epistola-aos-corintios]] | 40 |
| 14 | [[wiki/personalidades/allan-kardec]] | 40 |
| 15 | [[wiki/obras/epistola-aos-efesios]] | 39 |

### Centralidade (PageRank)

| # | Página | PR |
|---|--------|-----|
| 1 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 0.0258 |
| 2 | [[wiki/conceitos/reencarnacao]] | 0.0256 |
| 3 | [[wiki/conceitos/progresso-espiritual]] | 0.0244 |
| 4 | [[wiki/conceitos/livre-arbitrio]] | 0.0176 |
| 5 | [[wiki/obras/ceu-e-inferno]] | 0.0167 |
| 6 | [[wiki/conceitos/perispirito]] | 0.0155 |
| 7 | [[wiki/conceitos/caridade]] | 0.0148 |
| 8 | [[wiki/conceitos/mediunidade]] | 0.0139 |
| 9 | [[wiki/conceitos/leis-morais/lei-de-justica-amor-e-caridade]] | 0.0137 |
| 10 | [[wiki/obras/livro-dos-espiritos]] | 0.0131 |
| 11 | [[wiki/conceitos/obsessao]] | 0.0128 |
| 12 | [[wiki/conceitos/escala-espirita]] | 0.0113 |
| 13 | [[wiki/conceitos/penas-e-gozos-futuros]] | 0.0109 |
| 14 | [[wiki/conceitos/lei-natural]] | 0.0107 |
| 15 | [[wiki/conceitos/morte]] | 0.0107 |

### Páginas órfãs (sem backlinks)

_Nenhuma página órfã._

### Componentes isolados (≤ 2 nós)

_Nenhum._

## Vocabulário

### Top 50 termos

| # | Termo | Ocorrências |
|---|-------|-------------|
| 1 | `kardec` | 2147 |
| 2 | `espírito` | 2082 |
| 3 | `deus` | 2065 |
| 4 | `espíritos` | 1872 |
| 5 | `espírita` | 1715 |
| 6 | `moral` | 1617 |
| 7 | `espiritismo` | 1231 |
| 8 | `vida` | 1110 |
| 9 | `espiritual` | 1100 |
| 10 | `jesus` | 1051 |
| 11 | `cristo` | 936 |
| 12 | `homem` | 922 |
| 13 | `doutrina` | 814 |
| 14 | `morte` | 796 |
| 15 | `médium` | 748 |
| 16 | `leitura` | 739 |
| 17 | `corpo` | 712 |
| 18 | `alma` | 677 |
| 19 | `três` | 665 |
| 20 | `mundo` | 661 |
| 21 | `paulo` | 656 |
| 22 | `terra` | 631 |
| 23 | `amor` | 619 |
| 24 | `caso` | 613 |
| 25 | `caridade` | 573 |
| 26 | `caps` | 568 |
| 27 | `princípio` | 529 |
| 28 | `toda` | 494 |
| 29 | `contra` | 490 |
| 30 | `próprio` | 486 |
| 31 | `andré` | 483 |
| 32 | `obra` | 479 |
| 33 | `obras` | 468 |
| 34 | `prece` | 466 |
| 35 | `item` | 460 |
| 36 | `espíritas` | 448 |
| 37 | `progresso` | 444 |
| 38 | `segundo` | 441 |
| 39 | `mediunidade` | 438 |
| 40 | `dois` | 429 |
| 41 | `prática` | 421 |
| 42 | `anos` | 415 |
| 43 | `antes` | 413 |
| 44 | `luiz` | 395 |
| 45 | `senhor` | 388 |
| 46 | `estudo` | 383 |
| 47 | `justiça` | 374 |
| 48 | `natureza` | 364 |
| 49 | `universal` | 364 |
| 50 | `gênese` | 362 |

### Top 20 bigramas

| # | Bigrama | Ocorrências |
|---|---------|-------------|
| 1 | `andré luiz` | 395 |
| 2 | `leitura espírita` | 285 |
| 3 | `livre arbítrio` | 193 |
| 4 | `aplicação prática` | 171 |
| 5 | `doutrina espírita` | 160 |
| 6 | `chico xavier` | 160 |
| 7 | `ensino kardec` | 142 |
| 8 | `jesus cristo` | 119 |
| 9 | `revista espírita` | 107 |
| 10 | `mundo espiritual` | 106 |
| 11 | `estudo espírita` | 104 |
| 12 | `após morte` | 102 |
| 13 | `vida futura` | 98 |
| 14 | `espírito verdade` | 98 |
| 15 | `plano espiritual` | 93 |
| 16 | `causa efeito` | 89 |
| 17 | `allan kardec` | 84 |
| 18 | `texto integral` | 82 |
| 19 | `chave espírita` | 79 |
| 20 | `caridade salvação` | 78 |

## Atividade no tempo

Período coberto: **2026-04** → **2026-05** (2 meses).

### Sparkline por tipo

```
aprofundamento ▁█  total=1
estudo     █▂  total=14
glossario  ██  total=2
ingest     █▄  total=79
lint       █▂  total=42
refactor   █▂  total=15
setup      █▁  total=2
```

### Tabela mensal

| Mês | aprofundamento | estudo | glossario | ingest | lint | refactor | setup | Total |
|-----|---|---|---|---|---|---|---|-------|
| 2026-04 | 0 | 12 | 1 | 52 | 36 | 12 | 2 | 115 |
| 2026-05 | 1 | 2 | 1 | 27 | 6 | 3 | 0 | 40 |

### Dias mais ativos

| Data | Entradas |
|------|----------|
| 2026-04-07 | 15 |
| 2026-04-15 | 13 |
| 2026-04-29 | 12 |
| 2026-05-01 | 11 |
| 2026-04-26 | 10 |
| 2026-04-19 | 10 |
| 2026-04-06 | 10 |
| 2026-04-28 | 9 |
| 2026-05-04 | 8 |
| 2026-05-02 | 8 |

## Tamanho das páginas

```
<200        101  █████████████████
200-500     173  ██████████████████████████████
500-1000    118  ████████████████████
1000-2000    43  ███████
>2000        25  ████
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

- **Termos frequentes sem página própria**: `kardec` (2147), `espírito` (2082), `espíritos` (1872), `espírita` (1715), `moral` (1617), `espiritismo` (1231), `vida` (1110), `espiritual` (1100) — candidatos a novos conceitos ou sinônimos a padronizar.
- **3 blocos de 100 questões do LE com <20% de cobertura**: 201–300 (19/100), 301–400 (8/100), 401–500 (17/100). Priorizar extração de questões-chave desses intervalos para `wiki/questoes/`.

## Páginas referenciadas

- [[index]]
- `log.md`

## Fontes

- Script gerador: `.claude/skills/stats/scripts/stats_wiki.py` (execução em 2026-05-05).
- Corpus analisado: `wiki/**/*.md`, `log.md`, `raw/**/*.md`.
- Dependências: `networkx` (grafo, PageRank), `nltk` (stopwords PT-BR).
- Filtros: meta-páginas (`tipo: sintese` + tag `meta`) são excluídas de grafo, vocabulário, tamanho, cobertura doutrinária e wikilinks quebrados; seções-template (`## Fontes`, `## Páginas relacionadas`, `## Páginas referenciadas`, `## Conceitos relacionados`) são removidas antes da tokenização.
- Cobertura doutrinária: regex sobre citações inline `(LE, q. N)`, `(ESE, cap. X, item Y)`, `(Gênese, cap. X, item Y)`, `(LM, Nª parte, cap. X)`, `(C&I, Nª parte, cap. X)`. Totais canônicos: LE=1019q; ESE=28c; Gênese=18c; LM=33c (2ª parte); C&I=18c (11 + 7).
