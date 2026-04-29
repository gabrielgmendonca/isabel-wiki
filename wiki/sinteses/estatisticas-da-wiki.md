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

- Páginas na wiki: **330**
- Arquivos em `raw/`: **1253**
- Nós no grafo: **327** · Arestas: **3366**
- Componentes fracamente conexos: **1** (maior: 327 nós)
- Páginas órfãs (sem backlinks): **1**
- Vocabulário único (após stopwords): **18685** termos
- Entradas em `log.md`: **104**
- Razão conceitos/questões: **142:9** (15.8)
- Questões únicas do LE citadas: **285/1019** (28.0%)
- Wikilinks não resolvidos (freq ≥ 5): **0** targets

## Cobertura por tipo

| Diretório | Páginas |
|-----------|---------|
| `wiki/obras/` | 42 |
| `wiki/conceitos/` | 142 |
| `wiki/personalidades/` | 105 |
| `wiki/questoes/` | 9 |
| `wiki/aprofundamentos/` | 6 |
| `wiki/sinteses/` | 7 |
| `wiki/divergencias/` | 15 |
| `wiki/trilhas/` | 4 |

### Status

| Status | Páginas |
|--------|---------|
| `ativo` | 276 |
| `rascunho` | 39 |
| `aberta` | 14 |
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
| 3 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 92 |
| 4 | [[wiki/conceitos/caridade]] | 83 |
| 5 | [[wiki/conceitos/progresso-espiritual]] | 82 |
| 6 | [[wiki/conceitos/mediunidade]] | 58 |
| 7 | [[wiki/conceitos/livre-arbitrio]] | 57 |
| 8 | [[wiki/personalidades/jesus]] | 55 |
| 9 | [[wiki/conceitos/obsessao]] | 53 |
| 10 | [[wiki/conceitos/prece]] | 53 |
| 11 | [[wiki/conceitos/perispirito]] | 52 |
| 12 | [[wiki/obras/livro-dos-espiritos]] | 50 |
| 13 | [[wiki/conceitos/lei-de-causa-e-efeito]] | 47 |
| 14 | [[wiki/conceitos/lei-de-justica-amor-e-caridade]] | 47 |
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
| 9 | [[wiki/obras/depois-da-morte]] | 37 |
| 10 | [[wiki/obras/evangelho-segundo-lucas]] | 36 |
| 11 | [[wiki/personalidades/jesus]] | 36 |
| 12 | [[wiki/obras/livro-dos-espiritos]] | 35 |
| 13 | [[wiki/obras/epistola-aos-hebreus]] | 34 |
| 14 | [[wiki/trilhas/esde]] | 34 |
| 15 | [[wiki/obras/primeira-epistola-de-joao]] | 33 |

### Centralidade (PageRank)

| # | Página | PR |
|---|--------|-----|
| 1 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 0.0324 |
| 2 | [[wiki/conceitos/progresso-espiritual]] | 0.0322 |
| 3 | [[wiki/conceitos/reencarnacao]] | 0.0288 |
| 4 | [[wiki/conceitos/livre-arbitrio]] | 0.0221 |
| 5 | [[wiki/obras/ceu-e-inferno]] | 0.0183 |
| 6 | [[wiki/conceitos/caridade]] | 0.0177 |
| 7 | [[wiki/conceitos/lei-de-justica-amor-e-caridade]] | 0.0176 |
| 8 | [[wiki/conceitos/lei-natural]] | 0.0175 |
| 9 | [[wiki/obras/livro-dos-espiritos]] | 0.0157 |
| 10 | [[wiki/conceitos/perispirito]] | 0.0138 |
| 11 | [[wiki/conceitos/mediunidade]] | 0.0135 |
| 12 | [[wiki/conceitos/morte]] | 0.0130 |
| 13 | [[wiki/conceitos/penas-e-gozos-futuros]] | 0.0128 |
| 14 | [[wiki/conceitos/vida-espirita]] | 0.0121 |
| 15 | [[wiki/conceitos/obsessao]] | 0.0120 |

### Páginas órfãs (sem backlinks)

- [[wiki/obras/revista-espirita]]

### Componentes isolados (≤ 2 nós)

_Nenhum._

## Vocabulário

### Top 50 termos

| # | Termo | Ocorrências |
|---|-------|-------------|
| 1 | `deus` | 1355 |
| 2 | `espírito` | 1224 |
| 3 | `kardec` | 1157 |
| 4 | `espíritos` | 1069 |
| 5 | `moral` | 991 |
| 6 | `espírita` | 802 |
| 7 | `vida` | 715 |
| 8 | `espiritual` | 661 |
| 9 | `jesus` | 646 |
| 10 | `homem` | 544 |
| 11 | `cristo` | 536 |
| 12 | `espiritismo` | 449 |
| 13 | `morte` | 426 |
| 14 | `corpo` | 424 |
| 15 | `amor` | 420 |
| 16 | `caridade` | 417 |
| 17 | `alma` | 409 |
| 18 | `paulo` | 402 |
| 19 | `leitura` | 389 |
| 20 | `doutrina` | 371 |
| 21 | `mundo` | 362 |
| 22 | `caps` | 356 |
| 23 | `terra` | 327 |
| 24 | `item` | 315 |
| 25 | `três` | 300 |
| 26 | `obras` | 297 |
| 27 | `progresso` | 295 |
| 28 | `princípio` | 289 |
| 29 | `prática` | 287 |
| 30 | `prece` | 284 |
| 31 | `toda` | 277 |
| 32 | `justiça` | 267 |
| 33 | `segundo` | 262 |
| 34 | `próprio` | 256 |
| 35 | `natureza` | 249 |
| 36 | `obra` | 248 |
| 37 | `andré` | 247 |
| 38 | `médium` | 245 |
| 39 | `parábola` | 242 |
| 40 | `ensino` | 234 |
| 41 | `contra` | 230 |
| 42 | `sofrimento` | 226 |
| 43 | `evangelho` | 224 |
| 44 | `filho` | 212 |
| 45 | `estado` | 207 |
| 46 | `expiação` | 206 |
| 47 | `arrependimento` | 206 |
| 48 | `casa` | 206 |
| 49 | `passagem` | 205 |
| 50 | `sempre` | 201 |

### Top 20 bigramas

| # | Bigrama | Ocorrências |
|---|---------|-------------|
| 1 | `andré luiz` | 179 |
| 2 | `leitura espírita` | 157 |
| 3 | `aplicação prática` | 126 |
| 4 | `ensino kardec` | 118 |
| 5 | `livre arbítrio` | 110 |
| 6 | `mundo espiritual` | 99 |
| 7 | `chico xavier` | 89 |
| 8 | `doutrina espírita` | 86 |
| 9 | `vida futura` | 75 |
| 10 | `após morte` | 71 |
| 11 | `espírito verdade` | 62 |
| 12 | `jesus cristo` | 62 |
| 13 | `estudo espírita` | 62 |
| 14 | `causa efeito` | 58 |
| 15 | `justiça divina` | 56 |
| 16 | `plano espiritual` | 56 |
| 17 | `léon denis` | 56 |
| 18 | `caridade salvação` | 56 |
| 19 | `situação mundo` | 56 |
| 20 | `lições principais` | 56 |

## Atividade no tempo

Período coberto: **2026-04** → **2026-04** (1 meses).

### Sparkline por tipo

```
estudo     █  total=12
glossario  █  total=1
ingest     █  total=46
lint       █  total=32
refactor   █  total=11
setup      █  total=2
```

### Tabela mensal

| Mês | estudo | glossario | ingest | lint | refactor | setup | Total |
|-----|---|---|---|---|---|---|-------|
| 2026-04 | 12 | 1 | 46 | 32 | 11 | 2 | 104 |

### Dias mais ativos

| Data | Entradas |
|------|----------|
| 2026-04-07 | 15 |
| 2026-04-15 | 13 |
| 2026-04-26 | 10 |
| 2026-04-19 | 10 |
| 2026-04-06 | 10 |
| 2026-04-28 | 9 |
| 2026-04-29 | 8 |
| 2026-04-27 | 8 |
| 2026-04-21 | 6 |
| 2026-04-16 | 6 |

## Tamanho das páginas

```
<200        118  ██████████████████████████████
200-500     116  █████████████████████████████
500-1000     59  ███████████████
1000-2000    26  ██████
>2000         8  ██
```

### Maiores

- [[wiki/obras/epistola-aos-galatas]] — 3603 palavras
- [[wiki/obras/primeira-epistola-de-pedro]] — 3564 palavras
- [[wiki/obras/primeira-epistola-de-joao]] — 2981 palavras
- [[wiki/obras/epistola-aos-romanos]] — 2305 palavras
- [[wiki/obras/epistola-de-tiago]] — 2295 palavras
- [[wiki/obras/epistola-aos-hebreus]] — 2278 palavras
- [[wiki/aprofundamentos/expiacao-e-arrependimento]] — 2238 palavras
- [[wiki/obras/segunda-epistola-aos-corintios]] — 2129 palavras
- [[wiki/obras/obreiros-da-vida-eterna]] — 1883 palavras
- [[wiki/obras/missionarios-da-luz]] — 1773 palavras

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
- **Termos frequentes sem página própria**: `espírito` (1224), `kardec` (1157), `espíritos` (1069), `moral` (991), `espírita` (802), `vida` (715), `espiritual` (661), `homem` (544) — candidatos a novos conceitos ou sinônimos a padronizar.
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
