---
tipo: sintese
fontes: [meta]
tags: [estatisticas, meta, grafo, vocabulario]
atualizado_em: 2026-07-25
status: ativo
---

# Estatísticas da wiki

## Pergunta motivadora

Como a wiki IsAbel está distribuída entre obras, conceitos e entidades? Quais são os nós centrais do grafo, quais páginas estão isoladas, que termos dominam o vocabulário, e como é o ritmo de ingestão ao longo do tempo? Esta página é **regenerada automaticamente** — serve como painel para orientar expansões, backlinks faltantes e possíveis novos conceitos.

> Gerado em **2026-07-25** por `.claude/skills/stats/scripts/stats_wiki.py`.

## Resumo executivo

- Páginas na wiki: **1054**
- Arquivos em `raw/`: **2223**
- Nós no grafo: **1041** · Arestas: **8657**
- Componentes fracamente conexos: **1** (maior: 1041 nós)
- Páginas órfãs (sem backlinks): **43**
- Vocabulário único (após stopwords): **47464** termos
- Entradas em `log.md`: **262**
- Razão conceitos/questões: **204:19** (10.7)
- Questões únicas do LE citadas: **437/1019** (42.9%)
- Wikilinks não resolvidos (freq ≥ 5): **0** targets

## Cobertura por tipo

| Diretório | Páginas |
|-----------|---------|
| `wiki/obras/` | 135 |
| `wiki/conceitos/` | 204 |
| `wiki/personalidades/` | 207 |
| `wiki/questoes/` | 19 |
| `wiki/aprofundamentos/` | 17 |
| `wiki/sinteses/` | 19 |
| `wiki/divergencias/` | 23 |
| `wiki/biblia/` | 287 |
| `wiki/index.md/` | 1 |
| `wiki/pentateuco/` | 136 |
| `wiki/trilhas/` | 6 |

### Status

| Status | Páginas |
|--------|---------|
| `ativo` | 882 |
| `rascunho` | 150 |
| `aberta` | 21 |
| `concluída` | 1 |

## Cobertura doutrinária

Referências únicas do Pentateuco efetivamente citadas pela wiki (`(LE, q. N)`, `(ESE, cap. X, item Y)`, etc.). Mede o quanto da codificação já foi ancorado em páginas próprias.

| Obra | Unidade | Citadas | Total | Cobertura |
|------|---------|--------:|------:|----------:|
| LE | questões | 437 | 1019 | 42.9% |
| ESE | capítulos | 28 | 28 | 100.0% |
| Gênese | capítulos | 15 | 18 | 83.3% |
| LM | capítulos da 2ª parte | 27 | 33 | 81.8% |
| C&I | capítulos | 18 | 18 | 100.0% |

Referências `cap./item` únicas: ESE **148**, Gênese **72**, LM **37**, C&I **18**.

### Cobertura do LE por bloco de 100 questões

```
   1– 100  ███████████··················   39/100 (39%)
 101– 200  ████████████·················   41/100 (41%)
 201– 300  ████████████·················   43/100 (43%)
 301– 400  ██████·······················   21/100 (21%)
 401– 500  █████████····················   31/100 (31%)
 501– 600  █████████····················   32/100 (32%)
 601– 700  ██████████████████···········   61/100 (61%)
 701– 800  ███████████████··············   53/100 (53%)
 801– 900  ██████████████████···········   62/100 (62%)
 901–1000  ████████████·················   41/100 (41%)
1001–1019  ████████████████████·········   13/19 (68%)
```

## Grafo de conhecimento

### Mais referenciados (grau de entrada)

| # | Página | In |
|---|--------|----|
| 1 | [[wiki/conceitos/reencarnacao]] | 175 |
| 2 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 161 |
| 3 | [[wiki/personalidades/jesus]] | 140 |
| 4 | [[wiki/obras/ceu-e-inferno]] | 137 |
| 5 | [[wiki/conceitos/perispirito]] | 136 |
| 6 | [[wiki/conceitos/caridade]] | 134 |
| 7 | [[wiki/conceitos/obsessao]] | 126 |
| 8 | [[wiki/conceitos/mediunidade]] | 120 |
| 9 | [[wiki/conceitos/prece]] | 116 |
| 10 | [[wiki/conceitos/livre-arbitrio]] | 114 |
| 11 | [[wiki/obras/livro-dos-espiritos]] | 110 |
| 12 | [[wiki/personalidades/allan-kardec]] | 105 |
| 13 | [[wiki/conceitos/progresso-espiritual]] | 102 |
| 14 | [[wiki/obras/genese]] | 95 |
| 15 | [[wiki/conceitos/leis-morais/lei-de-causa-e-efeito]] | 87 |

### Mais conectores (grau de saída)

| # | Página | Out |
|---|--------|-----|
| 1 | [[wiki/obras/revista-espirita]] | 90 |
| 2 | [[wiki/obras/ceu-e-inferno]] | 86 |
| 3 | [[wiki/personalidades/chico-xavier]] | 63 |
| 4 | [[wiki/obras/apocalipse]] | 62 |
| 5 | [[wiki/obras/epistola-aos-romanos]] | 60 |
| 6 | [[wiki/obras/evangelho-segundo-lucas]] | 60 |
| 7 | [[wiki/obras/evangelho-segundo-mateus]] | 60 |
| 8 | [[wiki/personalidades/paulo-de-tarso]] | 58 |
| 9 | [[wiki/obras/primeira-epistola-de-pedro]] | 56 |
| 10 | [[wiki/obras/epistola-de-tiago]] | 55 |
| 11 | [[wiki/obras/segunda-epistola-aos-corintios]] | 53 |
| 12 | [[wiki/personalidades/divaldo-franco]] | 52 |
| 13 | [[wiki/sinteses/parabolas-de-jesus]] | 48 |
| 14 | [[wiki/obras/epistola-aos-galatas]] | 47 |
| 15 | [[wiki/obras/epistola-aos-hebreus]] | 47 |

### Centralidade (PageRank)

| # | Página | PR |
|---|--------|-----|
| 1 | [[wiki/conceitos/reencarnacao]] | 0.0203 |
| 2 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 0.0191 |
| 3 | [[wiki/conceitos/progresso-espiritual]] | 0.0172 |
| 4 | [[wiki/conceitos/livre-arbitrio]] | 0.0130 |
| 5 | [[wiki/conceitos/perispirito]] | 0.0117 |
| 6 | [[wiki/obras/ceu-e-inferno]] | 0.0117 |
| 7 | [[wiki/conceitos/obsessao]] | 0.0116 |
| 8 | [[wiki/conceitos/caridade]] | 0.0112 |
| 9 | [[wiki/conceitos/mediunidade]] | 0.0105 |
| 10 | [[wiki/obras/livro-dos-espiritos]] | 0.0100 |
| 11 | [[wiki/personalidades/jesus]] | 0.0100 |
| 12 | [[wiki/conceitos/leis-morais/lei-de-justica-amor-e-caridade]] | 0.0096 |
| 13 | [[wiki/personalidades/allan-kardec]] | 0.0093 |
| 14 | [[wiki/conceitos/prece]] | 0.0088 |
| 15 | [[wiki/conceitos/escala-espirita]] | 0.0085 |

### Páginas órfãs (sem backlinks)

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
- [[wiki/pentateuco/index]]
- [[wiki/personalidades/arthur-conan-doyle]]
- [[wiki/personalidades/deolindo-amorim]]
- … e mais 13 páginas.

### Componentes isolados (≤ 2 nós)

_Nenhum._

## Vocabulário

### Top 50 termos

| # | Termo | Ocorrências |
|---|-------|-------------|
| 1 | `deus` | 6461 |
| 2 | `espírito` | 5949 |
| 3 | `espíritos` | 5487 |
| 4 | `kardec` | 3572 |
| 5 | `vida` | 3375 |
| 6 | `homem` | 3356 |
| 7 | `jesus` | 3196 |
| 8 | `moral` | 2691 |
| 9 | `espírita` | 2582 |
| 10 | `item` | 2500 |
| 11 | `terra` | 2370 |
| 12 | `mundo` | 2154 |
| 13 | `pois` | 2135 |
| 14 | `corpo` | 2088 |
| 15 | `espiritual` | 2032 |
| 16 | `espiritismo` | 2010 |
| 17 | `cristo` | 1936 |
| 18 | `morte` | 1901 |
| 19 | `alma` | 1898 |
| 20 | `homens` | 1765 |
| 21 | `toda` | 1697 |
| 22 | `sempre` | 1694 |
| 23 | `senhor` | 1596 |
| 24 | `tudo` | 1583 |
| 25 | `amor` | 1566 |
| 26 | `doutrina` | 1511 |
| 27 | `médium` | 1476 |
| 28 | `disse` | 1454 |
| 29 | `coisas` | 1430 |
| 30 | `tempo` | 1369 |
| 31 | `então` | 1350 |
| 32 | `onde` | 1289 |
| 33 | `natureza` | 1255 |
| 34 | `obra` | 1249 |
| 35 | `princípio` | 1217 |
| 36 | `antes` | 1209 |
| 37 | `segundo` | 1205 |
| 38 | `nada` | 1203 |
| 39 | `contra` | 1166 |
| 40 | `caridade` | 1153 |
| 41 | `três` | 1152 |
| 42 | `todo` | 1143 |
| 43 | `estado` | 1142 |
| 44 | `leitura` | 1121 |
| 45 | `verdade` | 1101 |
| 46 | `próprio` | 1080 |
| 47 | `caso` | 1071 |
| 48 | `causa` | 1057 |
| 49 | `menos` | 1046 |
| 50 | `grande` | 1046 |

### Top 20 bigramas

| # | Bigrama | Ocorrências |
|---|---------|-------------|
| 1 | `andré luiz` | 523 |
| 2 | `livre arbítrio` | 394 |
| 3 | `jesus cristo` | 379 |
| 4 | `muitas vezes` | 355 |
| 5 | `leitura espírita` | 334 |
| 6 | `chico xavier` | 326 |
| 7 | `doutrina espírita` | 265 |
| 8 | `bons espíritos` | 250 |
| 9 | `após morte` | 211 |
| 10 | `vida futura` | 206 |
| 11 | `aplicação prática` | 203 |
| 12 | `alguma coisa` | 188 |
| 13 | `ponto vista` | 183 |
| 14 | `livro espíritos` | 179 |
| 15 | `espírito santo` | 178 |
| 16 | `senhor jesus` | 178 |
| 17 | `ensino kardec` | 176 |
| 18 | `texto integral` | 175 |
| 19 | `reino céus` | 168 |
| 20 | `plano espiritual` | 167 |

## Atividade no tempo

Período coberto: **2026-04** → **2026-07** (4 meses).

### Sparkline por tipo

```
aprofundamento ▁█▁█  total=2
autocritica ▁▁█▁  total=10
conceito   ▁▁▁█  total=1
critica    ▁▂█▁  total=5
estudo     ▆█▁▁  total=29
glossario  ▄█▁▁  total=3
ingest     ▅█▁▁  total=135
lint       █▃▁▁  total=52
refactor   █▅▁▁  total=22
setup      █▁▁▁  total=2
síntese    ▁▁▁█  total=1
```

### Tabela mensal

| Mês | aprofundamento | autocritica | conceito | critica | estudo | glossario | ingest | lint | refactor | setup | síntese | Total |
|-----|---|---|---|---|---|---|---|---|---|---|---|-------|
| 2026-04 | 0 | 0 | 0 | 0 | 12 | 1 | 52 | 36 | 12 | 2 | 0 | 115 |
| 2026-05 | 1 | 0 | 0 | 1 | 16 | 2 | 79 | 14 | 8 | 0 | 0 | 121 |
| 2026-06 | 0 | 10 | 0 | 4 | 0 | 0 | 3 | 2 | 1 | 0 | 0 | 20 |
| 2026-07 | 1 | 0 | 1 | 0 | 1 | 0 | 1 | 0 | 1 | 0 | 1 | 6 |

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
<200        240  ███████████████████
200-500     373  ██████████████████████████████
500-1000    207  ████████████████
1000-2000   133  ██████████
>2000        88  ███████
```

### Maiores

- [[wiki/pentateuco/ceu-e-inferno/parte-2-cap-ii]] — 10121 palavras
- [[wiki/pentateuco/evangelho-segundo-o-espiritismo/cap-xxviii]] — 7711 palavras
- [[wiki/pentateuco/livro-dos-espiritos/parte-4-cap-ii]] — 7153 palavras
- [[wiki/pentateuco/ceu-e-inferno/parte-2-cap-viii]] — 7072 palavras
- [[wiki/pentateuco/genese/cap-xv]] — 7010 palavras
- [[wiki/pentateuco/genese/cap-i]] — 6112 palavras
- [[wiki/pentateuco/genese/cap-vi]] — 5483 palavras
- [[wiki/pentateuco/livro-dos-espiritos/parte-2-cap-vi]] — 5270 palavras
- [[wiki/pentateuco/genese/cap-xiv]] — 5171 palavras
- [[wiki/obras/apocalipse]] — 4803 palavras

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

Total: **1** targets distintos, **4** ocorrências. Freq ≥ 5: **0**.

### Mais referenciados (freq ≥ 3)

| # | Target | Ocorrências |
|---|--------|------------:|
| 1 | `1` | 4 |

## Sugestões automáticas

- **43 páginas órfãs** (grau de entrada = 0) — considerar adicionar backlinks a partir de conceitos/obras relacionados.
- **Termos frequentes sem página própria**: `espírito` (5949), `espíritos` (5487), `kardec` (3572), `vida` (3375), `homem` (3356), `moral` (2691), `espírita` (2582), `item` (2500) — candidatos a novos conceitos ou sinônimos a padronizar.

## Páginas referenciadas

- [[index]]
- `log.md`

## Fontes

- Script gerador: `.claude/skills/stats/scripts/stats_wiki.py` (execução em 2026-07-25).
- Corpus analisado: `wiki/**/*.md`, `log.md`, `raw/**/*.md`.
- Dependências: `networkx` (grafo, PageRank), `nltk` (stopwords PT-BR).
- Filtros: meta-páginas (`tipo: sintese` + tag `meta`) são excluídas de grafo, vocabulário, tamanho, cobertura doutrinária e wikilinks quebrados; seções-template (`## Fontes`, `## Páginas relacionadas`, `## Páginas referenciadas`, `## Conceitos relacionados`) são removidas antes da tokenização.
- Cobertura doutrinária: regex sobre citações inline `(LE, q. N)`, `(ESE, cap. X, item Y)`, `(Gênese, cap. X, item Y)`, `(LM, Nª parte, cap. X)`, `(C&I, Nª parte, cap. X)`. Totais canônicos: LE=1019q; ESE=28c; Gênese=18c; LM=33c (2ª parte); C&I=18c (11 + 7).
