---
tipo: sintese
fontes: [meta]
tags: [estatisticas, meta, grafo, vocabulario]
atualizado_em: 2026-05-26
status: ativo
---

# Estatísticas da wiki

## Pergunta motivadora

Como a wiki IsAbel está distribuída entre obras, conceitos e entidades? Quais são os nós centrais do grafo, quais páginas estão isoladas, que termos dominam o vocabulário, e como é o ritmo de ingestão ao longo do tempo? Esta página é **regenerada automaticamente** — serve como painel para orientar expansões, backlinks faltantes e possíveis novos conceitos.

> Gerado em **2026-05-26** por `.claude/skills/stats/scripts/stats_wiki.py`.

## Resumo executivo

- Páginas na wiki: **885**
- Arquivos em `raw/`: **1853**
- Nós no grafo: **872** · Arestas: **7922**
- Componentes fracamente conexos: **1** (maior: 872 nós)
- Páginas órfãs (sem backlinks): **45**
- Vocabulário único (após stopwords): **35747** termos
- Entradas em `log.md`: **223**
- Razão conceitos/questões: **200:15** (13.3)
- Questões únicas do LE citadas: **385/1019** (37.8%)
- Wikilinks não resolvidos (freq ≥ 5): **0** targets

## Cobertura por tipo

| Diretório | Páginas |
|-----------|---------|
| `wiki/obras/` | 122 |
| `wiki/conceitos/` | 200 |
| `wiki/personalidades/` | 203 |
| `wiki/questoes/` | 15 |
| `wiki/aprofundamentos/` | 13 |
| `wiki/sinteses/` | 16 |
| `wiki/divergencias/` | 22 |
| `wiki/biblia/` | 287 |
| `wiki/index.md/` | 1 |
| `wiki/trilhas/` | 6 |

### Status

| Status | Páginas |
|--------|---------|
| `ativo` | 785 |
| `rascunho` | 79 |
| `aberta` | 20 |
| `concluída` | 1 |

## Cobertura doutrinária

Referências únicas do Pentateuco efetivamente citadas pela wiki (`(LE, q. N)`, `(ESE, cap. X, item Y)`, etc.). Mede o quanto da codificação já foi ancorado em páginas próprias.

| Obra | Unidade | Citadas | Total | Cobertura |
|------|---------|--------:|------:|----------:|
| LE | questões | 385 | 1019 | 37.8% |
| ESE | capítulos | 28 | 28 | 100.0% |
| Gênese | capítulos | 15 | 18 | 83.3% |
| LM | capítulos da 2ª parte | 28 | 33 | 84.8% |
| C&I | capítulos | 18 | 18 | 100.0% |

Referências `cap./item` únicas: ESE **143**, Gênese **71**, LM **38**, C&I **18**.

### Cobertura do LE por bloco de 100 questões

```
   1– 100  ██████████···················   35/100 (35%)
 101– 200  ████████████·················   41/100 (41%)
 201– 300  ████████·····················   29/100 (29%)
 301– 400  ████·························   16/100 (16%)
 401– 500  ██████·······················   21/100 (21%)
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
| 1 | [[wiki/conceitos/reencarnacao]] | 166 |
| 2 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 154 |
| 3 | [[wiki/obras/ceu-e-inferno]] | 133 |
| 4 | [[wiki/personalidades/jesus]] | 130 |
| 5 | [[wiki/conceitos/perispirito]] | 129 |
| 6 | [[wiki/conceitos/caridade]] | 127 |
| 7 | [[wiki/conceitos/obsessao]] | 117 |
| 8 | [[wiki/conceitos/mediunidade]] | 114 |
| 9 | [[wiki/conceitos/prece]] | 107 |
| 10 | [[wiki/obras/livro-dos-espiritos]] | 102 |
| 11 | [[wiki/personalidades/allan-kardec]] | 97 |
| 12 | [[wiki/conceitos/livre-arbitrio]] | 96 |
| 13 | [[wiki/conceitos/progresso-espiritual]] | 94 |
| 14 | [[wiki/obras/genese]] | 91 |
| 15 | [[wiki/obras/livro-dos-mediuns]] | 84 |

### Mais conectores (grau de saída)

| # | Página | Out |
|---|--------|-----|
| 1 | [[wiki/obras/revista-espirita]] | 90 |
| 2 | [[wiki/obras/ceu-e-inferno]] | 86 |
| 3 | [[wiki/obras/apocalipse]] | 62 |
| 4 | [[wiki/personalidades/chico-xavier]] | 62 |
| 5 | [[wiki/obras/epistola-aos-romanos]] | 60 |
| 6 | [[wiki/obras/evangelho-segundo-lucas]] | 60 |
| 7 | [[wiki/obras/evangelho-segundo-mateus]] | 59 |
| 8 | [[wiki/personalidades/paulo-de-tarso]] | 58 |
| 9 | [[wiki/obras/primeira-epistola-de-pedro]] | 56 |
| 10 | [[wiki/obras/epistola-de-tiago]] | 55 |
| 11 | [[wiki/obras/segunda-epistola-aos-corintios]] | 53 |
| 12 | [[wiki/obras/epistola-aos-galatas]] | 47 |
| 13 | [[wiki/obras/epistola-aos-hebreus]] | 47 |
| 14 | [[wiki/personalidades/divaldo-franco]] | 46 |
| 15 | [[wiki/obras/atos-dos-apostolos]] | 45 |

### Centralidade (PageRank)

| # | Página | PR |
|---|--------|-----|
| 1 | [[wiki/conceitos/reencarnacao]] | 0.0215 |
| 2 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 0.0206 |
| 3 | [[wiki/conceitos/progresso-espiritual]] | 0.0184 |
| 4 | [[wiki/conceitos/livre-arbitrio]] | 0.0136 |
| 5 | [[wiki/obras/ceu-e-inferno]] | 0.0129 |
| 6 | [[wiki/conceitos/perispirito]] | 0.0127 |
| 7 | [[wiki/conceitos/caridade]] | 0.0116 |
| 8 | [[wiki/conceitos/obsessao]] | 0.0114 |
| 9 | [[wiki/conceitos/mediunidade]] | 0.0110 |
| 10 | [[wiki/obras/livro-dos-espiritos]] | 0.0107 |
| 11 | [[wiki/conceitos/leis-morais/lei-de-justica-amor-e-caridade]] | 0.0103 |
| 12 | [[wiki/personalidades/jesus]] | 0.0101 |
| 13 | [[wiki/personalidades/allan-kardec]] | 0.0098 |
| 14 | [[wiki/conceitos/escala-espirita]] | 0.0091 |
| 15 | [[wiki/obras/livro-dos-mediuns]] | 0.0087 |

### Páginas órfãs (sem backlinks)

- [[wiki/aprofundamentos/silencio-interior-o-ser-consciente]]
- [[wiki/biblia/1-corintios/index]]
- [[wiki/biblia/1-joao/index]]
- [[wiki/biblia/1-pedro/index]]
- [[wiki/biblia/1-tessalonicenses/index]]
- [[wiki/biblia/1-timoteo/index]]
- [[wiki/biblia/2-corintios/index]]
- [[wiki/biblia/2-joao/index]]
- [[wiki/biblia/2-pedro/index]]
- [[wiki/biblia/2-tessalonicenses/index]]
- [[wiki/biblia/2-timoteo/index]]
- [[wiki/biblia/3-joao/index]]
- [[wiki/biblia/apocalipse/index]]
- [[wiki/biblia/atos/index]]
- [[wiki/biblia/colossenses/index]]
- [[wiki/biblia/efesios/index]]
- [[wiki/biblia/filemom/index]]
- [[wiki/biblia/filipenses/index]]
- [[wiki/biblia/galatas/index]]
- [[wiki/biblia/hebreus/index]]
- [[wiki/biblia/joao/index]]
- [[wiki/biblia/judas/index]]
- [[wiki/biblia/lucas/index]]
- [[wiki/biblia/marcos/index]]
- [[wiki/biblia/mateus/index]]
- [[wiki/biblia/romanos/index]]
- [[wiki/biblia/tiago/index]]
- [[wiki/biblia/tito/index]]
- [[wiki/conceitos/sonhos]]
- [[wiki/personalidades/arthur-conan-doyle]]
- … e mais 15 páginas.

### Componentes isolados (≤ 2 nós)

_Nenhum._

## Vocabulário

### Top 50 termos

| # | Termo | Ocorrências |
|---|-------|-------------|
| 1 | `deus` | 3855 |
| 2 | `espírito` | 3042 |
| 3 | `kardec` | 2699 |
| 4 | `jesus` | 2514 |
| 5 | `espírita` | 2209 |
| 6 | `espíritos` | 2185 |
| 7 | `moral` | 2078 |
| 8 | `vida` | 1729 |
| 9 | `cristo` | 1697 |
| 10 | `homem` | 1574 |
| 11 | `espiritual` | 1556 |
| 12 | `espiritismo` | 1410 |
| 13 | `senhor` | 1238 |
| 14 | `morte` | 1223 |
| 15 | `amor` | 1177 |
| 16 | `doutrina` | 1126 |
| 17 | `mundo` | 1116 |
| 18 | `terra` | 1100 |
| 19 | `corpo` | 1088 |
| 20 | `disse` | 1066 |
| 21 | `leitura` | 1008 |
| 22 | `três` | 1001 |
| 23 | `alma` | 976 |
| 24 | `paulo` | 974 |
| 25 | `obra` | 938 |
| 26 | `toda` | 903 |
| 27 | `médium` | 892 |
| 28 | `pois` | 883 |
| 29 | `caps` | 825 |
| 30 | `contra` | 814 |
| 31 | `filho` | 797 |
| 32 | `obras` | 760 |
| 33 | `segundo` | 746 |
| 34 | `caridade` | 743 |
| 35 | `caso` | 741 |
| 36 | `antes` | 740 |
| 37 | `dois` | 736 |
| 38 | `princípio` | 724 |
| 39 | `homens` | 720 |
| 40 | `verdade` | 702 |
| 41 | `coisas` | 697 |
| 42 | `casa` | 695 |
| 43 | `anos` | 678 |
| 44 | `tudo` | 676 |
| 45 | `próprio` | 663 |
| 46 | `onde` | 646 |
| 47 | `prece` | 626 |
| 48 | `item` | 625 |
| 49 | `todo` | 621 |
| 50 | `andré` | 611 |

### Top 20 bigramas

| # | Bigrama | Ocorrências |
|---|---------|-------------|
| 1 | `andré luiz` | 496 |
| 2 | `jesus cristo` | 367 |
| 3 | `leitura espírita` | 327 |
| 4 | `chico xavier` | 287 |
| 5 | `livre arbítrio` | 236 |
| 6 | `doutrina espírita` | 219 |
| 7 | `aplicação prática` | 198 |
| 8 | `senhor jesus` | 177 |
| 9 | `espírito santo` | 168 |
| 10 | `ensino kardec` | 163 |
| 11 | `plano espiritual` | 157 |
| 12 | `texto integral` | 156 |
| 13 | `allan kardec` | 144 |
| 14 | `estudo espírita` | 129 |
| 15 | `revista espírita` | 127 |
| 16 | `após morte` | 125 |
| 17 | `dados bibliográficos` | 121 |
| 18 | `emmanuel chico` | 120 |
| 19 | `cristo jesus` | 118 |
| 20 | `reino deus` | 117 |

## Atividade no tempo

Período coberto: **2026-04** → **2026-05** (2 meses).

### Sparkline por tipo

```
aprofundamento ▁█  total=1
estudo     ▇█  total=25
glossario  ▄█  total=3
ingest     ▆█  total=123
lint       █▃  total=50
refactor   █▅  total=19
setup      █▁  total=2
```

### Tabela mensal

| Mês | aprofundamento | estudo | glossario | ingest | lint | refactor | setup | Total |
|-----|---|---|---|---|---|---|---|-------|
| 2026-04 | 0 | 12 | 1 | 52 | 36 | 12 | 2 | 115 |
| 2026-05 | 1 | 13 | 2 | 71 | 14 | 7 | 0 | 108 |

### Dias mais ativos

| Data | Entradas |
|------|----------|
| 2026-05-05 | 15 |
| 2026-04-07 | 15 |
| 2026-04-15 | 13 |
| 2026-05-07 | 12 |
| 2026-04-29 | 12 |
| 2026-05-01 | 11 |
| 2026-04-26 | 10 |
| 2026-04-19 | 10 |
| 2026-04-06 | 10 |
| 2026-05-06 | 9 |

## Tamanho das páginas

```
<200        233  ███████████████████
200-500     358  ██████████████████████████████
500-1000    170  ██████████████
1000-2000    79  ██████
>2000        32  ██
```

### Maiores

- [[wiki/obras/apocalipse]] — 4805 palavras
- [[wiki/obras/revista-espirita-1866]] — 4069 palavras
- [[wiki/obras/segunda-epistola-a-timoteo]] — 3979 palavras
- [[wiki/obras/revista-espirita-1868]] — 3794 palavras
- [[wiki/obras/epistola-aos-galatas]] — 3603 palavras
- [[wiki/obras/primeira-epistola-de-pedro]] — 3564 palavras
- [[wiki/obras/revista-espirita-1865]] — 3559 palavras
- [[wiki/obras/revista-espirita-1867]] — 3519 palavras
- [[wiki/obras/revista-espirita-1863]] — 3227 palavras
- [[wiki/obras/revista-espirita-1864]] — 3220 palavras

### Menores (candidatas a expansão)

- [[wiki/biblia/1-corintios/index]] — 15 palavras
- [[wiki/biblia/1-joao/index]] — 15 palavras
- [[wiki/biblia/1-pedro/index]] — 15 palavras
- [[wiki/biblia/1-tessalonicenses/index]] — 15 palavras
- [[wiki/biblia/1-timoteo/index]] — 15 palavras
- [[wiki/biblia/2-corintios/index]] — 15 palavras
- [[wiki/biblia/2-joao/index]] — 15 palavras
- [[wiki/biblia/2-pedro/index]] — 15 palavras
- [[wiki/biblia/2-tessalonicenses/index]] — 15 palavras
- [[wiki/biblia/2-timoteo/index]] — 15 palavras

## Referências não resolvidas

Wikilinks `[[...]]` cujo target não existe na árvore — candidatos a páginas novas (quando frequentes) ou erros de digitação (quando raros).

_Nenhum wikilink quebrado._

## Sugestões automáticas

- **45 páginas órfãs** (grau de entrada = 0) — considerar adicionar backlinks a partir de conceitos/obras relacionados.
- **Termos frequentes sem página própria**: `espírito` (3042), `kardec` (2699), `espírita` (2209), `espíritos` (2185), `moral` (2078), `vida` (1729), `cristo` (1697), `homem` (1574) — candidatos a novos conceitos ou sinônimos a padronizar.
- **1 blocos de 100 questões do LE com <20% de cobertura**: 301–400 (16/100). Priorizar extração de questões-chave desses intervalos para `wiki/questoes/`.

## Páginas referenciadas

- [[index]]
- `log.md`

## Fontes

- Script gerador: `.claude/skills/stats/scripts/stats_wiki.py` (execução em 2026-05-26).
- Corpus analisado: `wiki/**/*.md`, `log.md`, `raw/**/*.md`.
- Dependências: `networkx` (grafo, PageRank), `nltk` (stopwords PT-BR).
- Filtros: meta-páginas (`tipo: sintese` + tag `meta`) são excluídas de grafo, vocabulário, tamanho, cobertura doutrinária e wikilinks quebrados; seções-template (`## Fontes`, `## Páginas relacionadas`, `## Páginas referenciadas`, `## Conceitos relacionados`) são removidas antes da tokenização.
- Cobertura doutrinária: regex sobre citações inline `(LE, q. N)`, `(ESE, cap. X, item Y)`, `(Gênese, cap. X, item Y)`, `(LM, Nª parte, cap. X)`, `(C&I, Nª parte, cap. X)`. Totais canônicos: LE=1019q; ESE=28c; Gênese=18c; LM=33c (2ª parte); C&I=18c (11 + 7).
