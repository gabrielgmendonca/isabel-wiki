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

- Páginas na wiki: **482**
- Arquivos em `raw/`: **1396**
- Nós no grafo: **470** · Arestas: **5538**
- Componentes fracamente conexos: **1** (maior: 470 nós)
- Páginas órfãs (sem backlinks): **1**
- Vocabulário único (após stopwords): **27438** termos
- Entradas em `log.md`: **162**
- Razão conceitos/questões: **180:11** (16.4)
- Questões únicas do LE citadas: **347/1019** (34.1%)
- Wikilinks não resolvidos (freq ≥ 5): **0** targets

## Cobertura por tipo

| Diretório | Páginas |
|-----------|---------|
| `wiki/obras/` | 81 |
| `wiki/conceitos/` | 180 |
| `wiki/personalidades/` | 161 |
| `wiki/questoes/` | 11 |
| `wiki/aprofundamentos/` | 9 |
| `wiki/sinteses/` | 11 |
| `wiki/divergencias/` | 22 |
| `wiki/index.md/` | 1 |
| `wiki/trilhas/` | 6 |

### Status

| Status | Páginas |
|--------|---------|
| `ativo` | 404 |
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
| 1 | [[wiki/conceitos/reencarnacao]] | 129 |
| 2 | [[wiki/obras/ceu-e-inferno]] | 122 |
| 3 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 119 |
| 4 | [[wiki/conceitos/caridade]] | 111 |
| 5 | [[wiki/conceitos/mediunidade]] | 100 |
| 6 | [[wiki/conceitos/obsessao]] | 99 |
| 7 | [[wiki/conceitos/perispirito]] | 99 |
| 8 | [[wiki/conceitos/prece]] | 91 |
| 9 | [[wiki/personalidades/jesus]] | 91 |
| 10 | [[wiki/conceitos/progresso-espiritual]] | 84 |
| 11 | [[wiki/conceitos/livre-arbitrio]] | 80 |
| 12 | [[wiki/obras/livro-dos-espiritos]] | 76 |
| 13 | [[wiki/obras/genese]] | 71 |
| 14 | [[wiki/conceitos/leis-morais/lei-de-causa-e-efeito]] | 69 |
| 15 | [[wiki/obras/livro-dos-mediuns]] | 62 |

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
| 1 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 0.0257 |
| 2 | [[wiki/conceitos/reencarnacao]] | 0.0254 |
| 3 | [[wiki/conceitos/progresso-espiritual]] | 0.0240 |
| 4 | [[wiki/conceitos/livre-arbitrio]] | 0.0174 |
| 5 | [[wiki/obras/ceu-e-inferno]] | 0.0163 |
| 6 | [[wiki/conceitos/perispirito]] | 0.0153 |
| 7 | [[wiki/conceitos/caridade]] | 0.0148 |
| 8 | [[wiki/conceitos/mediunidade]] | 0.0138 |
| 9 | [[wiki/conceitos/leis-morais/lei-de-justica-amor-e-caridade]] | 0.0136 |
| 10 | [[wiki/conceitos/obsessao]] | 0.0133 |
| 11 | [[wiki/obras/livro-dos-espiritos]] | 0.0131 |
| 12 | [[wiki/conceitos/escala-espirita]] | 0.0112 |
| 13 | [[wiki/conceitos/penas-e-gozos-futuros]] | 0.0107 |
| 14 | [[wiki/obras/livro-dos-mediuns]] | 0.0107 |
| 15 | [[wiki/conceitos/lei-natural]] | 0.0106 |

### Páginas órfãs (sem backlinks)

- [[wiki/sinteses/colecao-fonte-viva-emmanuel]]

### Componentes isolados (≤ 2 nós)

_Nenhum._

## Vocabulário

### Top 50 termos

| # | Termo | Ocorrências |
|---|-------|-------------|
| 1 | `kardec` | 2191 |
| 2 | `espírito` | 2103 |
| 3 | `deus` | 2087 |
| 4 | `espíritos` | 1878 |
| 5 | `espírita` | 1759 |
| 6 | `moral` | 1652 |
| 7 | `espiritismo` | 1259 |
| 8 | `vida` | 1157 |
| 9 | `espiritual` | 1129 |
| 10 | `jesus` | 1089 |
| 11 | `homem` | 956 |
| 12 | `cristo` | 953 |
| 13 | `doutrina` | 831 |
| 14 | `morte` | 812 |
| 15 | `leitura` | 766 |
| 16 | `médium` | 758 |
| 17 | `corpo` | 729 |
| 18 | `alma` | 701 |
| 19 | `três` | 684 |
| 20 | `mundo` | 672 |
| 21 | `paulo` | 671 |
| 22 | `amor` | 658 |
| 23 | `terra` | 636 |
| 24 | `caps` | 632 |
| 25 | `caso` | 613 |
| 26 | `caridade` | 594 |
| 27 | `princípio` | 539 |
| 28 | `obra` | 523 |
| 29 | `toda` | 506 |
| 30 | `próprio` | 501 |
| 31 | `contra` | 497 |
| 32 | `andré` | 488 |
| 33 | `obras` | 484 |
| 34 | `prece` | 478 |
| 35 | `item` | 461 |
| 36 | `espíritas` | 456 |
| 37 | `progresso` | 449 |
| 38 | `segundo` | 448 |
| 39 | `mediunidade` | 445 |
| 40 | `anos` | 434 |
| 41 | `dois` | 433 |
| 42 | `prática` | 430 |
| 43 | `antes` | 422 |
| 44 | `luiz` | 400 |
| 45 | `senhor` | 392 |
| 46 | `estudo` | 388 |
| 47 | `justiça` | 380 |
| 48 | `tudo` | 374 |
| 49 | `chave` | 371 |
| 50 | `própria` | 369 |

### Top 20 bigramas

| # | Bigrama | Ocorrências |
|---|---------|-------------|
| 1 | `andré luiz` | 400 |
| 2 | `leitura espírita` | 289 |
| 3 | `livre arbítrio` | 201 |
| 4 | `aplicação prática` | 175 |
| 5 | `doutrina espírita` | 168 |
| 6 | `chico xavier` | 168 |
| 7 | `ensino kardec` | 142 |
| 8 | `jesus cristo` | 119 |
| 9 | `revista espírita` | 109 |
| 10 | `mundo espiritual` | 106 |
| 11 | `estudo espírita` | 104 |
| 12 | `após morte` | 103 |
| 13 | `vida futura` | 98 |
| 14 | `espírito verdade` | 98 |
| 15 | `plano espiritual` | 93 |
| 16 | `causa efeito` | 91 |
| 17 | `allan kardec` | 89 |
| 18 | `texto integral` | 87 |
| 19 | `chave espírita` | 81 |
| 20 | `dados bibliográficos` | 80 |

## Atividade no tempo

Período coberto: **2026-04** → **2026-05** (2 meses).

### Sparkline por tipo

```
aprofundamento ▁█  total=1
estudo     █▂  total=15
glossario  ██  total=2
ingest     █▅  total=84
lint       █▂  total=43
refactor   █▂  total=15
setup      █▁  total=2
```

### Tabela mensal

| Mês | aprofundamento | estudo | glossario | ingest | lint | refactor | setup | Total |
|-----|---|---|---|---|---|---|---|-------|
| 2026-04 | 0 | 12 | 1 | 52 | 36 | 12 | 2 | 115 |
| 2026-05 | 1 | 3 | 1 | 32 | 7 | 3 | 0 | 47 |

### Dias mais ativos

| Data | Entradas |
|------|----------|
| 2026-04-07 | 15 |
| 2026-05-05 | 13 |
| 2026-04-15 | 13 |
| 2026-04-29 | 12 |
| 2026-05-01 | 11 |
| 2026-04-26 | 10 |
| 2026-04-19 | 10 |
| 2026-04-06 | 10 |
| 2026-04-28 | 9 |
| 2026-05-04 | 8 |

## Tamanho das páginas

```
<200        100  █████████████████
200-500     175  ██████████████████████████████
500-1000    125  █████████████████████
1000-2000    45  ███████
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
- **Termos frequentes sem página própria**: `kardec` (2191), `espírito` (2103), `espíritos` (1878), `espírita` (1759), `moral` (1652), `espiritismo` (1259), `vida` (1157), `espiritual` (1129) — candidatos a novos conceitos ou sinônimos a padronizar.
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
