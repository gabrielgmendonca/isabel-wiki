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

- Páginas na wiki: **246**
- Arquivos em `raw/`: **1225**
- Nós no grafo: **245** · Arestas: **1873**
- Componentes fracamente conexos: **1** (maior: 245 nós)
- Páginas órfãs (sem backlinks): **0**
- Vocabulário único (após stopwords): **12159** termos
- Entradas em `log.md`: **50**
- Razão conceitos/questões: **119:1** (119.0)
- Questões únicas do LE citadas: **215/1019** (21.1%)
- Wikilinks não resolvidos (freq ≥ 5): **0** targets

## Cobertura por tipo

| Diretório | Páginas |
|-----------|---------|
| `wiki/obras/` | 24 |
| `wiki/conceitos/` | 119 |
| `wiki/personalidades/` | 92 |
| `wiki/questoes/` | 1 |
| `wiki/aprofundamentos/` | 1 |
| `wiki/sinteses/` | 3 |
| `wiki/divergencias/` | 6 |

### Status

| Status | Páginas |
|--------|---------|
| `ativo` | 228 |
| `rascunho` | 12 |
| `aberta` | 5 |
| `concluída` | 1 |

## Cobertura doutrinária

Referências únicas do Pentateuco efetivamente citadas pela wiki (`(LE, q. N)`, `(ESE, cap. X, item Y)`, etc.). Mede o quanto da codificação já foi ancorado em páginas próprias.

| Obra | Unidade | Citadas | Total | Cobertura |
|------|---------|--------:|------:|----------:|
| LE | questões | 215 | 1019 | 21.1% |
| ESE | capítulos | 28 | 28 | 100.0% |
| Gênese | capítulos | 10 | 18 | 55.6% |
| LM | capítulos da 2ª parte | 24 | 33 | 72.7% |
| C&I | capítulos | 18 | 18 | 100.0% |

Referências `cap./item` únicas: ESE **103**, Gênese **50**, LM **30**, C&I **18**.

### Cobertura do LE por bloco de 100 questões

```
   1– 100  █████████·····················   30/100 (30%)
 101– 200  ███████······················   26/100 (26%)
 201– 300  ████·························   16/100 (16%)
 301– 400  █····························    5/100 (5%)
 401– 500  ███··························   12/100 (12%)
 501– 600  ·····························    2/100 (2%)
 601– 700  ████████·····················   28/100 (28%)
 701– 800  ███████······················   25/100 (25%)
 801– 900  ████████·····················   27/100 (27%)
 901–1000  █████████····················   33/100 (33%)
1001–1019  █████████████████············   11/19 (58%)
```

## Grafo de conhecimento

### Mais referenciados (grau de entrada)

| # | Página | In |
|---|--------|----|
| 1 | [[wiki/obras/ceu-e-inferno]] | 87 |
| 2 | [[wiki/conceitos/reencarnacao]] | 78 |
| 3 | [[wiki/conceitos/progresso-espiritual]] | 73 |
| 4 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 57 |
| 5 | [[wiki/conceitos/caridade]] | 56 |
| 6 | [[wiki/conceitos/livre-arbitrio]] | 39 |
| 7 | [[wiki/conceitos/morte]] | 34 |
| 8 | [[wiki/conceitos/penas-e-gozos-futuros]] | 34 |
| 9 | [[wiki/conceitos/prece]] | 33 |
| 10 | [[wiki/conceitos/obsessao]] | 32 |
| 11 | [[wiki/conceitos/expiacao-e-reparacao]] | 31 |
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
| 1 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 0.0423 |
| 2 | [[wiki/conceitos/progresso-espiritual]] | 0.0410 |
| 3 | [[wiki/conceitos/reencarnacao]] | 0.0342 |
| 4 | [[wiki/conceitos/livre-arbitrio]] | 0.0268 |
| 5 | [[wiki/conceitos/lei-natural]] | 0.0257 |
| 6 | [[wiki/conceitos/lei-de-justica-amor-e-caridade]] | 0.0225 |
| 7 | [[wiki/obras/ceu-e-inferno]] | 0.0212 |
| 8 | [[wiki/conceitos/caridade]] | 0.0204 |
| 9 | [[wiki/obras/livro-dos-espiritos]] | 0.0168 |
| 10 | [[wiki/conceitos/vida-espirita]] | 0.0167 |
| 11 | [[wiki/conceitos/perfeicao-moral]] | 0.0156 |
| 12 | [[wiki/conceitos/morte]] | 0.0156 |
| 13 | [[wiki/conceitos/penas-e-gozos-futuros]] | 0.0153 |
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
| 1 | `kardec` | 642 |
| 2 | `espírito` | 625 |
| 3 | `deus` | 591 |
| 4 | `espíritos` | 568 |
| 5 | `vida` | 419 |
| 6 | `moral` | 415 |
| 7 | `jesus` | 375 |
| 8 | `espírita` | 366 |
| 9 | `espiritual` | 345 |
| 10 | `morte` | 290 |
| 11 | `espiritismo` | 283 |
| 12 | `homem` | 250 |
| 13 | `mundo` | 234 |
| 14 | `parábola` | 224 |
| 15 | `alma` | 223 |
| 16 | `caridade` | 199 |
| 17 | `corpo` | 198 |
| 18 | `progresso` | 188 |
| 19 | `ensino` | 183 |
| 20 | `terra` | 174 |
| 21 | `arrependimento` | 166 |
| 22 | `prática` | 166 |
| 23 | `expiação` | 164 |
| 24 | `mundos` | 151 |
| 25 | `doutrina` | 150 |
| 26 | `denis` | 150 |
| 27 | `caps` | 146 |
| 28 | `sofrimento` | 137 |
| 29 | `justiça` | 136 |
| 30 | `prece` | 135 |
| 31 | `provas` | 134 |
| 32 | `mateus` | 132 |
| 33 | `natureza` | 129 |
| 34 | `sempre` | 124 |
| 35 | `estado` | 122 |
| 36 | `reparação` | 121 |
| 37 | `toda` | 119 |
| 38 | `segundo` | 117 |
| 39 | `princípio` | 115 |
| 40 | `médium` | 115 |
| 41 | `três` | 114 |
| 42 | `tudo` | 112 |
| 43 | `amor` | 110 |
| 44 | `evangelho` | 109 |
| 45 | `matéria` | 108 |
| 46 | `espíritas` | 108 |
| 47 | `após` | 107 |
| 48 | `orgulho` | 106 |
| 49 | `perispírito` | 106 |
| 50 | `homens` | 105 |

### Top 20 bigramas

| # | Bigrama | Ocorrências |
|---|---------|-------------|
| 1 | `mundo espiritual` | 100 |
| 2 | `ensino kardec` | 96 |
| 3 | `aplicação prática` | 90 |
| 4 | `vida futura` | 58 |
| 5 | `situação mundo` | 58 |
| 6 | `lições principais` | 58 |
| 7 | `após morte` | 55 |
| 8 | `livre arbítrio` | 52 |
| 9 | `léon denis` | 45 |
| 10 | `doutrina espírita` | 44 |
| 11 | `justiça divina` | 43 |
| 12 | `leitura espírita` | 37 |
| 13 | `chico xavier` | 32 |
| 14 | `allan kardec` | 32 |
| 15 | `joão batista` | 30 |
| 16 | `kardec kardec` | 29 |
| 17 | `causa efeito` | 29 |
| 18 | `viagem espírita` | 29 |
| 19 | `temas centrais` | 29 |
| 20 | `pluralidade existências` | 28 |

## Atividade no tempo

Período coberto: **2026-04** → **2026-04** (1 meses).

### Sparkline por tipo

```
ingest     █  total=25
lint       █  total=14
query      █  total=6
refactor   █  total=3
setup      █  total=2
```

### Tabela mensal

| Mês | ingest | lint | query | refactor | setup | Total |
|-----|---|---|---|---|---|-------|
| 2026-04 | 25 | 14 | 6 | 3 | 2 | 50 |

### Dias mais ativos

| Data | Entradas |
|------|----------|
| 2026-04-07 | 15 |
| 2026-04-15 | 13 |
| 2026-04-06 | 10 |
| 2026-04-16 | 6 |
| 2026-04-05 | 2 |
| 2026-04-08 | 2 |
| 2026-04-18 | 1 |
| 2026-04-19 | 1 |

## Tamanho das páginas

```
<200        134  ██████████████████████████████
200-500      82  ██████████████████
500-1000     21  ████
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

- **Termos frequentes sem página própria**: `kardec` (642), `espírito` (625), `espíritos` (568), `vida` (419), `moral` (415), `espírita` (366), `espiritual` (345), `espiritismo` (283) — candidatos a novos conceitos ou sinônimos a padronizar.
- **4 blocos de 100 questões do LE com <20% de cobertura**: 201–300 (16/100), 301–400 (5/100), 401–500 (12/100), 501–600 (2/100). Priorizar extração de questões-chave desses intervalos para `wiki/questoes/`.
- **Razão conceitos/questões muito alta** (119:1 = 119.0). `wiki/questoes/` está sub-representada; ver item §3 do ROADMAP.

## Páginas referenciadas

- [[index]]
- `log.md`

## Fontes

- Script gerador: `.claude/skills/stats/scripts/stats_wiki.py` (execução em 2026-04-19).
- Corpus analisado: `wiki/**/*.md`, `log.md`, `raw/**/*.md`.
- Dependências: `networkx` (grafo, PageRank), `nltk` (stopwords PT-BR).
- Filtros: meta-páginas (`tipo: sintese` + tag `meta`) são excluídas de grafo, vocabulário, tamanho, cobertura doutrinária e wikilinks quebrados; seções-template (`## Fontes`, `## Páginas relacionadas`, `## Páginas referenciadas`, `## Conceitos relacionados`) são removidas antes da tokenização.
- Cobertura doutrinária: regex sobre citações inline `(LE, q. N)`, `(ESE, cap. X, item Y)`, `(Gênese, cap. X, item Y)`, `(LM, Nª parte, cap. X)`, `(C&I, Nª parte, cap. X)`. Totais canônicos: LE=1019q; ESE=28c; Gênese=18c; LM=33c (2ª parte); C&I=18c (11 + 7).
