---
tipo: sintese
fontes: [meta]
tags: [estatisticas, meta, grafo, vocabulario]
atualizado_em: 2026-04-19
status: ativo
---

# Estatísticas da wiki

## Pergunta motivadora

Como a wiki IsAbel está distribuída entre obras, conceitos e entidades? Quais são os nós centrais do grafo, quais páginas estão isoladas, que termos dominam o vocabulário, e como é o ritmo de ingestão ao longo do tempo? Esta página é **regenerada automaticamente** — serve como painel para orientar expansões, backlinks faltantes e possíveis novos conceitos.

> Gerado em **2026-04-19** por `.claude/skills/stats/scripts/stats_wiki.py`.

## Resumo executivo

- Páginas na wiki: **251**
- Arquivos em `raw/`: **1225**
- Nós no grafo: **250** · Arestas: **1914**
- Componentes fracamente conexos: **1** (maior: 250 nós)
- Páginas órfãs (sem backlinks): **0**
- Vocabulário único (após stopwords): **12419** termos
- Entradas em `log.md`: **52**
- Razão conceitos/questões: **119:6** (19.8)
- Questões únicas do LE citadas: **239/1019** (23.5%)
- Wikilinks não resolvidos (freq ≥ 5): **0** targets

## Cobertura por tipo

| Diretório | Páginas |
|-----------|---------|
| `wiki/obras/` | 24 |
| `wiki/conceitos/` | 119 |
| `wiki/personalidades/` | 92 |
| `wiki/questoes/` | 6 |
| `wiki/aprofundamentos/` | 1 |
| `wiki/sinteses/` | 3 |
| `wiki/divergencias/` | 6 |

### Status

| Status | Páginas |
|--------|---------|
| `ativo` | 233 |
| `rascunho` | 12 |
| `aberta` | 5 |
| `concluída` | 1 |

## Cobertura doutrinária

Referências únicas do Pentateuco efetivamente citadas pela wiki (`(LE, q. N)`, `(ESE, cap. X, item Y)`, etc.). Mede o quanto da codificação já foi ancorado em páginas próprias.

| Obra | Unidade | Citadas | Total | Cobertura |
|------|---------|--------:|------:|----------:|
| LE | questões | 239 | 1019 | 23.5% |
| ESE | capítulos | 28 | 28 | 100.0% |
| Gênese | capítulos | 11 | 18 | 61.1% |
| LM | capítulos da 2ª parte | 24 | 33 | 72.7% |
| C&I | capítulos | 18 | 18 | 100.0% |

Referências `cap./item` únicas: ESE **104**, Gênese **52**, LM **30**, C&I **18**.

### Cobertura do LE por bloco de 100 questões

```
   1– 100  █████████·····················   30/100 (30%)
 101– 200  ████████·····················   27/100 (27%)
 201– 300  ████·························   16/100 (16%)
 301– 400  ██···························    7/100 (7%)
 401– 500  ███··························   13/100 (13%)
 501– 600  ██████························   20/100 (20%)
 601– 700  ████████·····················   29/100 (29%)
 701– 800  ███████······················   26/100 (26%)
 801– 900  ████████·····················   27/100 (27%)
 901–1000  █████████····················   33/100 (33%)
1001–1019  █████████████████············   11/19 (58%)
```

## Grafo de conhecimento

### Mais referenciados (grau de entrada)

| # | Página | In |
|---|--------|----|
| 1 | [[wiki/obras/ceu-e-inferno]] | 87 |
| 2 | [[wiki/conceitos/reencarnacao]] | 80 |
| 3 | [[wiki/conceitos/progresso-espiritual]] | 74 |
| 4 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 57 |
| 5 | [[wiki/conceitos/caridade]] | 56 |
| 6 | [[wiki/conceitos/livre-arbitrio]] | 43 |
| 7 | [[wiki/conceitos/morte]] | 35 |
| 8 | [[wiki/conceitos/penas-e-gozos-futuros]] | 34 |
| 9 | [[wiki/conceitos/prece]] | 34 |
| 10 | [[wiki/conceitos/obsessao]] | 33 |
| 11 | [[wiki/conceitos/expiacao-e-reparacao]] | 32 |
| 12 | [[wiki/conceitos/mediunidade]] | 31 |
| 13 | [[wiki/conceitos/perispirito]] | 29 |
| 14 | [[wiki/personalidades/jesus]] | 28 |
| 15 | [[wiki/conceitos/lei-de-justica-amor-e-caridade]] | 27 |

### Mais conectores (grau de saída)

| # | Página | Out |
|---|--------|-----|
| 1 | [[wiki/obras/ceu-e-inferno]] | 85 |
| 2 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 40 |
| 3 | [[wiki/obras/depois-da-morte]] | 37 |
| 4 | [[wiki/obras/evangelho-segundo-lucas]] | 36 |
| 5 | [[wiki/obras/livro-dos-espiritos]] | 35 |
| 6 | [[wiki/personalidades/jesus]] | 34 |
| 7 | [[wiki/obras/evangelho-segundo-mateus]] | 29 |
| 8 | [[wiki/obras/o-que-e-o-espiritismo]] | 28 |
| 9 | [[wiki/aprofundamentos/expiacao-e-arrependimento]] | 25 |
| 10 | [[wiki/obras/obras-postumas]] | 24 |
| 11 | [[wiki/obras/evangelho-segundo-marcos]] | 20 |
| 12 | [[wiki/obras/o-problema-do-ser-e-do-destino]] | 20 |
| 13 | [[wiki/obras/genese]] | 18 |
| 14 | [[wiki/obras/viagem-espirita-em-1862]] | 18 |
| 15 | [[wiki/obras/atos-dos-apostolos]] | 17 |

### Centralidade (PageRank)

| # | Página | PR |
|---|--------|-----|
| 1 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 0.0419 |
| 2 | [[wiki/conceitos/progresso-espiritual]] | 0.0408 |
| 3 | [[wiki/conceitos/reencarnacao]] | 0.0344 |
| 4 | [[wiki/conceitos/livre-arbitrio]] | 0.0271 |
| 5 | [[wiki/conceitos/lei-natural]] | 0.0250 |
| 6 | [[wiki/conceitos/lei-de-justica-amor-e-caridade]] | 0.0217 |
| 7 | [[wiki/obras/ceu-e-inferno]] | 0.0210 |
| 8 | [[wiki/conceitos/caridade]] | 0.0201 |
| 9 | [[wiki/obras/livro-dos-espiritos]] | 0.0173 |
| 10 | [[wiki/conceitos/vida-espirita]] | 0.0168 |
| 11 | [[wiki/conceitos/morte]] | 0.0158 |
| 12 | [[wiki/conceitos/penas-e-gozos-futuros]] | 0.0153 |
| 13 | [[wiki/conceitos/perfeicao-moral]] | 0.0152 |
| 14 | [[wiki/conceitos/mediunidade]] | 0.0135 |
| 15 | [[wiki/conceitos/perispirito]] | 0.0135 |

### Páginas órfãs (sem backlinks)

_Nenhuma página órfã._

### Componentes isolados (≤ 2 nós)

_Nenhum._

## Vocabulário

### Top 50 termos

| # | Termo | Ocorrências |
|---|-------|-------------|
| 1 | `kardec` | 656 |
| 2 | `espírito` | 643 |
| 3 | `espíritos` | 630 |
| 4 | `deus` | 603 |
| 5 | `moral` | 433 |
| 6 | `vida` | 431 |
| 7 | `jesus` | 375 |
| 8 | `espírita` | 368 |
| 9 | `espiritual` | 350 |
| 10 | `morte` | 303 |
| 11 | `espiritismo` | 289 |
| 12 | `homem` | 283 |
| 13 | `mundo` | 239 |
| 14 | `alma` | 239 |
| 15 | `parábola` | 224 |
| 16 | `corpo` | 207 |
| 17 | `caridade` | 199 |
| 18 | `progresso` | 193 |
| 19 | `ensino` | 184 |
| 20 | `terra` | 174 |
| 21 | `prática` | 171 |
| 22 | `expiação` | 168 |
| 23 | `arrependimento` | 166 |
| 24 | `doutrina` | 166 |
| 25 | `denis` | 153 |
| 26 | `mundos` | 152 |
| 27 | `caps` | 148 |
| 28 | `provas` | 141 |
| 29 | `natureza` | 140 |
| 30 | `sofrimento` | 140 |
| 31 | `justiça` | 138 |
| 32 | `prece` | 137 |
| 33 | `princípio` | 136 |
| 34 | `sempre` | 134 |
| 35 | `mateus` | 132 |
| 36 | `estado` | 128 |
| 37 | `toda` | 125 |
| 38 | `reparação` | 123 |
| 39 | `três` | 122 |
| 40 | `segundo` | 121 |
| 41 | `filho` | 120 |
| 42 | `matéria` | 115 |
| 43 | `médium` | 115 |
| 44 | `tudo` | 113 |
| 45 | `evangelho` | 112 |
| 46 | `após` | 111 |
| 47 | `amor` | 111 |
| 48 | `leis` | 111 |
| 49 | `espíritas` | 110 |
| 50 | `orgulho` | 107 |

### Top 20 bigramas

| # | Bigrama | Ocorrências |
|---|---------|-------------|
| 1 | `mundo espiritual` | 100 |
| 2 | `ensino kardec` | 96 |
| 3 | `aplicação prática` | 95 |
| 4 | `livre arbítrio` | 68 |
| 5 | `vida futura` | 63 |
| 6 | `após morte` | 59 |
| 7 | `situação mundo` | 58 |
| 8 | `lições principais` | 58 |
| 9 | `léon denis` | 48 |
| 10 | `justiça divina` | 45 |
| 11 | `doutrina espírita` | 45 |
| 12 | `leitura espírita` | 37 |
| 13 | `chico xavier` | 32 |
| 14 | `allan kardec` | 32 |
| 15 | `livro espíritos` | 31 |
| 16 | `joão batista` | 30 |
| 17 | `segundo espiritismo` | 29 |
| 18 | `kardec kardec` | 29 |
| 19 | `causa efeito` | 29 |
| 20 | `viagem espírita` | 29 |

## Atividade no tempo

Período coberto: **2026-04** → **2026-04** (1 meses).

### Sparkline por tipo

```
ingest     █  total=26
lint       █  total=14
query      █  total=6
refactor   █  total=4
setup      █  total=2
```

### Tabela mensal

| Mês | ingest | lint | query | refactor | setup | Total |
|-----|---|---|---|---|---|-------|
| 2026-04 | 26 | 14 | 6 | 4 | 2 | 52 |

### Dias mais ativos

| Data | Entradas |
|------|----------|
| 2026-04-07 | 15 |
| 2026-04-15 | 13 |
| 2026-04-06 | 10 |
| 2026-04-16 | 6 |
| 2026-04-19 | 3 |
| 2026-04-05 | 2 |
| 2026-04-08 | 2 |
| 2026-04-18 | 1 |

## Tamanho das páginas

```
<200        134  ██████████████████████████████
200-500      84  ██████████████████
500-1000     24  █████
1000-2000     7  █
>2000         1  
```

### Maiores

- [[wiki/aprofundamentos/expiacao-e-arrependimento]] — 2238 palavras
- [[wiki/obras/atos-dos-apostolos]] — 1535 palavras
- [[wiki/sinteses/hierarquia-de-autoridade]] — 1490 palavras
- [[wiki/obras/evangelho-segundo-marcos]] — 1182 palavras
- [[wiki/obras/cristianismo-e-espiritismo]] — 1118 palavras
- [[wiki/obras/evangelho-segundo-lucas]] — 1116 palavras
- [[wiki/obras/evangelho-segundo-mateus]] — 1073 palavras
- [[wiki/obras/quando-o-invisivel-se-torna-inevitavel]] — 1061 palavras
- [[wiki/obras/evangelho-segundo-joao]] — 958 palavras
- [[wiki/obras/conquista-da-saude-psicologica]] — 895 palavras

### Menores (candidatas a expansão)

- [[wiki/personalidades/carlos-mendonca]] — 51 palavras
- [[wiki/personalidades/chico-xavier]] — 71 palavras
- [[wiki/conceitos/lei-do-trabalho]] — 82 palavras
- [[wiki/conceitos/pluralidade-das-existencias]] — 82 palavras
- [[wiki/conceitos/lei-de-adoracao]] — 84 palavras
- [[wiki/conceitos/lei-de-reproducao]] — 88 palavras
- [[wiki/personalidades/joseph-bre]] — 90 palavras
- [[wiki/conceitos/lei-de-conservacao]] — 92 palavras
- [[wiki/personalidades/espiritos-reveladores]] — 92 palavras
- [[wiki/conceitos/lei-de-sociedade]] — 93 palavras

## Referências não resolvidas

Wikilinks `[[...]]` cujo target não existe na árvore — candidatos a páginas novas (quando frequentes) ou erros de digitação (quando raros).

_Nenhum wikilink quebrado._

## Sugestões automáticas

- **Termos frequentes sem página própria**: `kardec` (656), `espírito` (643), `espíritos` (630), `moral` (433), `vida` (431), `espírita` (368), `espiritual` (350), `espiritismo` (289) — candidatos a novos conceitos ou sinônimos a padronizar.
- **3 blocos de 100 questões do LE com <20% de cobertura**: 201–300 (16/100), 301–400 (7/100), 401–500 (13/100). Priorizar extração de questões-chave desses intervalos para `wiki/questoes/`.

## Páginas referenciadas

- [[index]]
- `log.md`

## Fontes

- Script gerador: `.claude/skills/stats/scripts/stats_wiki.py` (execução em 2026-04-19).
- Corpus analisado: `wiki/**/*.md`, `log.md`, `raw/**/*.md`.
- Dependências: `networkx` (grafo, PageRank), `nltk` (stopwords PT-BR).
- Filtros: meta-páginas (`tipo: sintese` + tag `meta`) são excluídas de grafo, vocabulário, tamanho, cobertura doutrinária e wikilinks quebrados; seções-template (`## Fontes`, `## Páginas relacionadas`, `## Páginas referenciadas`, `## Conceitos relacionados`) são removidas antes da tokenização.
- Cobertura doutrinária: regex sobre citações inline `(LE, q. N)`, `(ESE, cap. X, item Y)`, `(Gênese, cap. X, item Y)`, `(LM, Nª parte, cap. X)`, `(C&I, Nª parte, cap. X)`. Totais canônicos: LE=1019q; ESE=28c; Gênese=18c; LM=33c (2ª parte); C&I=18c (11 + 7).
