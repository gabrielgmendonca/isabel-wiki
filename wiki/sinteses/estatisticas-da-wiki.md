---
tipo: sintese
fontes: [meta]
tags: [estatisticas, meta, grafo, vocabulario]
atualizado_em: 2026-05-04
status: ativo
---

# Estatísticas da wiki

## Pergunta motivadora

Como a wiki IsAbel está distribuída entre obras, conceitos e entidades? Quais são os nós centrais do grafo, quais páginas estão isoladas, que termos dominam o vocabulário, e como é o ritmo de ingestão ao longo do tempo? Esta página é **regenerada automaticamente** — serve como painel para orientar expansões, backlinks faltantes e possíveis novos conceitos.

> Gerado em **2026-05-04** por `.claude/skills/stats/scripts/stats_wiki.py`.

## Resumo executivo

- Páginas na wiki: **452**
- Arquivos em `raw/`: **1387**
- Nós no grafo: **449** · Arestas: **5162**
- Componentes fracamente conexos: **1** (maior: 449 nós)
- Páginas órfãs (sem backlinks): **1**
- Vocabulário único (após stopwords): **26447** termos
- Entradas em `log.md`: **144**
- Razão conceitos/questões: **176:9** (19.6)
- Questões únicas do LE citadas: **347/1019** (34.1%)
- Wikilinks não resolvidos (freq ≥ 5): **0** targets

## Cobertura por tipo

| Diretório | Páginas |
|-----------|---------|
| `wiki/obras/` | 68 |
| `wiki/conceitos/` | 176 |
| `wiki/personalidades/` | 158 |
| `wiki/questoes/` | 9 |
| `wiki/aprofundamentos/` | 7 |
| `wiki/sinteses/` | 9 |
| `wiki/divergencias/` | 21 |
| `wiki/trilhas/` | 4 |

### Status

| Status | Páginas |
|--------|---------|
| `ativo` | 366 |
| `rascunho` | 65 |
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

Referências `cap./item` únicas: ESE **136**, Gênese **68**, LM **37**, C&I **18**.

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
| 1 | [[wiki/conceitos/reencarnacao]] | 125 |
| 2 | [[wiki/obras/ceu-e-inferno]] | 122 |
| 3 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 107 |
| 4 | [[wiki/conceitos/caridade]] | 102 |
| 5 | [[wiki/conceitos/perispirito]] | 96 |
| 6 | [[wiki/conceitos/mediunidade]] | 94 |
| 7 | [[wiki/conceitos/obsessao]] | 92 |
| 8 | [[wiki/conceitos/progresso-espiritual]] | 83 |
| 9 | [[wiki/conceitos/prece]] | 78 |
| 10 | [[wiki/personalidades/jesus]] | 78 |
| 11 | [[wiki/conceitos/livre-arbitrio]] | 72 |
| 12 | [[wiki/obras/livro-dos-espiritos]] | 67 |
| 13 | [[wiki/conceitos/leis-morais/lei-de-causa-e-efeito]] | 65 |
| 14 | [[wiki/obras/genese]] | 63 |
| 15 | [[wiki/personalidades/allan-kardec]] | 57 |

### Mais conectores (grau de saída)

| # | Página | Out |
|---|--------|-----|
| 1 | [[wiki/obras/revista-espirita]] | 90 |
| 2 | [[wiki/obras/ceu-e-inferno]] | 86 |
| 3 | [[wiki/obras/primeira-epistola-de-pedro]] | 51 |
| 4 | [[wiki/obras/epistola-de-tiago]] | 50 |
| 5 | [[wiki/personalidades/paulo-de-tarso]] | 45 |
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
| 1 | [[wiki/conceitos/reencarnacao]] | 0.0260 |
| 2 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 0.0258 |
| 3 | [[wiki/conceitos/progresso-espiritual]] | 0.0246 |
| 4 | [[wiki/conceitos/livre-arbitrio]] | 0.0176 |
| 5 | [[wiki/obras/ceu-e-inferno]] | 0.0170 |
| 6 | [[wiki/conceitos/perispirito]] | 0.0156 |
| 7 | [[wiki/conceitos/caridade]] | 0.0148 |
| 8 | [[wiki/conceitos/mediunidade]] | 0.0141 |
| 9 | [[wiki/conceitos/leis-morais/lei-de-justica-amor-e-caridade]] | 0.0135 |
| 10 | [[wiki/obras/livro-dos-espiritos]] | 0.0131 |
| 11 | [[wiki/conceitos/obsessao]] | 0.0130 |
| 12 | [[wiki/conceitos/escala-espirita]] | 0.0115 |
| 13 | [[wiki/conceitos/penas-e-gozos-futuros]] | 0.0110 |
| 14 | [[wiki/conceitos/morte]] | 0.0109 |
| 15 | [[wiki/conceitos/lei-natural]] | 0.0107 |

### Páginas órfãs (sem backlinks)

- [[wiki/aprofundamentos/dor-rigidez]]

### Componentes isolados (≤ 2 nós)

_Nenhum._

## Vocabulário

### Top 50 termos

| # | Termo | Ocorrências |
|---|-------|-------------|
| 1 | `kardec` | 2098 |
| 2 | `espírito` | 2022 |
| 3 | `deus` | 1965 |
| 4 | `espíritos` | 1850 |
| 5 | `espírita` | 1662 |
| 6 | `moral` | 1544 |
| 7 | `espiritismo` | 1198 |
| 8 | `vida` | 1060 |
| 9 | `espiritual` | 1059 |
| 10 | `jesus` | 945 |
| 11 | `cristo` | 891 |
| 12 | `homem` | 881 |
| 13 | `doutrina` | 792 |
| 14 | `morte` | 791 |
| 15 | `médium` | 735 |
| 16 | `leitura` | 698 |
| 17 | `corpo` | 696 |
| 18 | `alma` | 657 |
| 19 | `mundo` | 647 |
| 20 | `três` | 638 |
| 21 | `terra` | 620 |
| 22 | `paulo` | 613 |
| 23 | `caso` | 601 |
| 24 | `amor` | 589 |
| 25 | `caridade` | 533 |
| 26 | `caps` | 521 |
| 27 | `princípio` | 510 |
| 28 | `andré` | 479 |
| 29 | `contra` | 469 |
| 30 | `toda` | 466 |
| 31 | `obras` | 463 |
| 32 | `próprio` | 462 |
| 33 | `espíritas` | 442 |
| 34 | `obra` | 441 |
| 35 | `item` | 437 |
| 36 | `progresso` | 435 |
| 37 | `prece` | 435 |
| 38 | `segundo` | 430 |
| 39 | `mediunidade` | 426 |
| 40 | `dois` | 412 |
| 41 | `anos` | 405 |
| 42 | `prática` | 400 |
| 43 | `antes` | 395 |
| 44 | `luiz` | 391 |
| 45 | `estudo` | 366 |
| 46 | `justiça` | 361 |
| 47 | `natureza` | 360 |
| 48 | `universal` | 360 |
| 49 | `comunicação` | 358 |
| 50 | `médiuns` | 355 |

### Top 20 bigramas

| # | Bigrama | Ocorrências |
|---|---------|-------------|
| 1 | `andré luiz` | 391 |
| 2 | `leitura espírita` | 275 |
| 3 | `livre arbítrio` | 174 |
| 4 | `aplicação prática` | 169 |
| 5 | `doutrina espírita` | 153 |
| 6 | `chico xavier` | 145 |
| 7 | `ensino kardec` | 140 |
| 8 | `jesus cristo` | 113 |
| 9 | `revista espírita` | 107 |
| 10 | `mundo espiritual` | 106 |
| 11 | `após morte` | 100 |
| 12 | `vida futura` | 98 |
| 13 | `estudo espírita` | 96 |
| 14 | `espírito verdade` | 93 |
| 15 | `plano espiritual` | 91 |
| 16 | `allan kardec` | 84 |
| 17 | `causa efeito` | 81 |
| 18 | `caridade salvação` | 75 |
| 19 | `texto integral` | 75 |
| 20 | `pluralidade existências` | 74 |

## Atividade no tempo

Período coberto: **2026-04** → **2026-05** (2 meses).

### Sparkline por tipo

```
estudo     █▁  total=13
glossario  ██  total=2
ingest     █▃  total=72
lint       █▂  total=42
refactor   █▁  total=13
setup      █▁  total=2
```

### Tabela mensal

| Mês | estudo | glossario | ingest | lint | refactor | setup | Total |
|-----|---|---|---|---|---|---|-------|
| 2026-04 | 12 | 1 | 52 | 36 | 12 | 2 | 115 |
| 2026-05 | 1 | 1 | 20 | 6 | 1 | 0 | 29 |

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
| 2026-05-02 | 8 |
| 2026-04-27 | 8 |

## Tamanho das páginas

```
<200        104  ██████████████████
200-500     167  ██████████████████████████████
500-1000    115  ████████████████████
1000-2000    38  ██████
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

- **1 páginas órfãs** (grau de entrada = 0) — considerar adicionar backlinks a partir de conceitos/obras relacionados.
- **Termos frequentes sem página própria**: `kardec` (2098), `espírito` (2022), `espíritos` (1850), `espírita` (1662), `moral` (1544), `espiritismo` (1198), `vida` (1060), `espiritual` (1059) — candidatos a novos conceitos ou sinônimos a padronizar.
- **3 blocos de 100 questões do LE com <20% de cobertura**: 201–300 (19/100), 301–400 (8/100), 401–500 (17/100). Priorizar extração de questões-chave desses intervalos para `wiki/questoes/`.

## Páginas referenciadas

- [[index]]
- `log.md`

## Fontes

- Script gerador: `.claude/skills/stats/scripts/stats_wiki.py` (execução em 2026-05-04).
- Corpus analisado: `wiki/**/*.md`, `log.md`, `raw/**/*.md`.
- Dependências: `networkx` (grafo, PageRank), `nltk` (stopwords PT-BR).
- Filtros: meta-páginas (`tipo: sintese` + tag `meta`) são excluídas de grafo, vocabulário, tamanho, cobertura doutrinária e wikilinks quebrados; seções-template (`## Fontes`, `## Páginas relacionadas`, `## Páginas referenciadas`, `## Conceitos relacionados`) são removidas antes da tokenização.
- Cobertura doutrinária: regex sobre citações inline `(LE, q. N)`, `(ESE, cap. X, item Y)`, `(Gênese, cap. X, item Y)`, `(LM, Nª parte, cap. X)`, `(C&I, Nª parte, cap. X)`. Totais canônicos: LE=1019q; ESE=28c; Gênese=18c; LM=33c (2ª parte); C&I=18c (11 + 7).
