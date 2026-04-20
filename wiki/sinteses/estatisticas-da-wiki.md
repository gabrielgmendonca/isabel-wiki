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

- Páginas na wiki: **258**
- Arquivos em `raw/`: **1226**
- Nós no grafo: **257** · Arestas: **2009**
- Componentes fracamente conexos: **1** (maior: 257 nós)
- Páginas órfãs (sem backlinks): **0**
- Vocabulário único (após stopwords): **12915** termos
- Entradas em `log.md`: **58**
- Razão conceitos/questões: **120:9** (13.3)
- Questões únicas do LE citadas: **278/1019** (27.3%)
- Wikilinks não resolvidos (freq ≥ 5): **0** targets

## Cobertura por tipo

| Diretório | Páginas |
|-----------|---------|
| `wiki/obras/` | 25 |
| `wiki/conceitos/` | 120 |
| `wiki/personalidades/` | 94 |
| `wiki/questoes/` | 9 |
| `wiki/aprofundamentos/` | 1 |
| `wiki/sinteses/` | 3 |
| `wiki/divergencias/` | 6 |

### Status

| Status | Páginas |
|--------|---------|
| `ativo` | 236 |
| `rascunho` | 16 |
| `aberta` | 5 |
| `concluída` | 1 |

## Cobertura doutrinária

Referências únicas do Pentateuco efetivamente citadas pela wiki (`(LE, q. N)`, `(ESE, cap. X, item Y)`, etc.). Mede o quanto da codificação já foi ancorado em páginas próprias.

| Obra | Unidade | Citadas | Total | Cobertura |
|------|---------|--------:|------:|----------:|
| LE | questões | 278 | 1019 | 27.3% |
| ESE | capítulos | 28 | 28 | 100.0% |
| Gênese | capítulos | 11 | 18 | 61.1% |
| LM | capítulos da 2ª parte | 24 | 33 | 72.7% |
| C&I | capítulos | 18 | 18 | 100.0% |

Referências `cap./item` únicas: ESE **107**, Gênese **52**, LM **30**, C&I **18**.

### Cobertura do LE por bloco de 100 questões

```
   1– 100  █████████····················   32/100 (32%)
 101– 200  ████████·····················   27/100 (27%)
 201– 300  ████·························   16/100 (16%)
 301– 400  ██···························    7/100 (7%)
 401– 500  ███··························   13/100 (13%)
 501– 600  ██████························   20/100 (20%)
 601– 700  █████████████████············   58/100 (58%)
 701– 800  █████████····················   33/100 (33%)
 801– 900  ████████·····················   27/100 (27%)
 901–1000  ██████████···················   34/100 (34%)
1001–1019  █████████████████············   11/19 (58%)
```

## Grafo de conhecimento

### Mais referenciados (grau de entrada)

| # | Página | In |
|---|--------|----|
| 1 | [[wiki/obras/ceu-e-inferno]] | 87 |
| 2 | [[wiki/conceitos/reencarnacao]] | 80 |
| 3 | [[wiki/conceitos/progresso-espiritual]] | 75 |
| 4 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 59 |
| 5 | [[wiki/conceitos/caridade]] | 58 |
| 6 | [[wiki/conceitos/livre-arbitrio]] | 45 |
| 7 | [[wiki/conceitos/morte]] | 35 |
| 8 | [[wiki/conceitos/penas-e-gozos-futuros]] | 34 |
| 9 | [[wiki/conceitos/prece]] | 34 |
| 10 | [[wiki/conceitos/obsessao]] | 33 |
| 11 | [[wiki/conceitos/expiacao-e-reparacao]] | 32 |
| 12 | [[wiki/conceitos/mediunidade]] | 32 |
| 13 | [[wiki/personalidades/jesus]] | 30 |
| 14 | [[wiki/conceitos/lei-de-justica-amor-e-caridade]] | 29 |
| 15 | [[wiki/conceitos/perispirito]] | 29 |

### Mais conectores (grau de saída)

| # | Página | Out |
|---|--------|-----|
| 1 | [[wiki/obras/ceu-e-inferno]] | 85 |
| 2 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 40 |
| 3 | [[wiki/obras/depois-da-morte]] | 37 |
| 4 | [[wiki/obras/evangelho-segundo-lucas]] | 36 |
| 5 | [[wiki/personalidades/jesus]] | 36 |
| 6 | [[wiki/obras/livro-dos-espiritos]] | 35 |
| 7 | [[wiki/obras/evangelho-segundo-mateus]] | 29 |
| 8 | [[wiki/obras/o-que-e-o-espiritismo]] | 28 |
| 9 | [[wiki/aprofundamentos/expiacao-e-arrependimento]] | 25 |
| 10 | [[wiki/obras/obras-postumas]] | 24 |
| 11 | [[wiki/obras/evangelho-segundo-marcos]] | 20 |
| 12 | [[wiki/obras/o-problema-do-ser-e-do-destino]] | 20 |
| 13 | [[wiki/obras/as-dores-da-alma]] | 19 |
| 14 | [[wiki/obras/genese]] | 18 |
| 15 | [[wiki/obras/viagem-espirita-em-1862]] | 18 |

### Centralidade (PageRank)

| # | Página | PR |
|---|--------|-----|
| 1 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 0.0416 |
| 2 | [[wiki/conceitos/progresso-espiritual]] | 0.0406 |
| 3 | [[wiki/conceitos/reencarnacao]] | 0.0333 |
| 4 | [[wiki/conceitos/livre-arbitrio]] | 0.0267 |
| 5 | [[wiki/conceitos/lei-natural]] | 0.0217 |
| 6 | [[wiki/conceitos/caridade]] | 0.0205 |
| 7 | [[wiki/obras/ceu-e-inferno]] | 0.0204 |
| 8 | [[wiki/conceitos/lei-de-justica-amor-e-caridade]] | 0.0198 |
| 9 | [[wiki/obras/livro-dos-espiritos]] | 0.0175 |
| 10 | [[wiki/conceitos/vida-espirita]] | 0.0165 |
| 11 | [[wiki/conceitos/morte]] | 0.0154 |
| 12 | [[wiki/conceitos/perfeicao-moral]] | 0.0154 |
| 13 | [[wiki/conceitos/penas-e-gozos-futuros]] | 0.0150 |
| 14 | [[wiki/conceitos/mediunidade]] | 0.0134 |
| 15 | [[wiki/conceitos/perispirito]] | 0.0132 |

### Páginas órfãs (sem backlinks)

_Nenhuma página órfã._

### Componentes isolados (≤ 2 nós)

_Nenhum._

## Vocabulário

### Top 50 termos

| # | Termo | Ocorrências |
|---|-------|-------------|
| 1 | `kardec` | 693 |
| 2 | `espírito` | 671 |
| 3 | `deus` | 669 |
| 4 | `espíritos` | 663 |
| 5 | `moral` | 468 |
| 6 | `vida` | 451 |
| 7 | `jesus` | 406 |
| 8 | `espírita` | 386 |
| 9 | `espiritual` | 365 |
| 10 | `homem` | 317 |
| 11 | `morte` | 307 |
| 12 | `espiritismo` | 305 |
| 13 | `alma` | 286 |
| 14 | `mundo` | 243 |
| 15 | `caridade` | 232 |
| 16 | `parábola` | 225 |
| 17 | `corpo` | 212 |
| 18 | `progresso` | 206 |
| 19 | `ensino` | 188 |
| 20 | `terra` | 182 |
| 21 | `prática` | 181 |
| 22 | `doutrina` | 179 |
| 23 | `expiação` | 170 |
| 24 | `arrependimento` | 168 |
| 25 | `natureza` | 164 |
| 26 | `denis` | 155 |
| 27 | `mundos` | 153 |
| 28 | `caps` | 148 |
| 29 | `sempre` | 147 |
| 30 | `princípio` | 147 |
| 31 | `prece` | 144 |
| 32 | `provas` | 142 |
| 33 | `sofrimento` | 142 |
| 34 | `justiça` | 142 |
| 35 | `mateus` | 134 |
| 36 | `toda` | 133 |
| 37 | `estado` | 131 |
| 38 | `segundo` | 130 |
| 39 | `três` | 129 |
| 40 | `reparação` | 126 |
| 41 | `orgulho` | 125 |
| 42 | `tudo` | 122 |
| 43 | `amor` | 121 |
| 44 | `filho` | 120 |
| 45 | `matéria` | 119 |
| 46 | `médium` | 118 |
| 47 | `homens` | 117 |
| 48 | `evangelho` | 116 |
| 49 | `espíritas` | 115 |
| 50 | `divina` | 113 |

### Top 20 bigramas

| # | Bigrama | Ocorrências |
|---|---------|-------------|
| 1 | `mundo espiritual` | 100 |
| 2 | `aplicação prática` | 100 |
| 3 | `ensino kardec` | 97 |
| 4 | `livre arbítrio` | 71 |
| 5 | `vida futura` | 63 |
| 6 | `após morte` | 59 |
| 7 | `situação mundo` | 58 |
| 8 | `lições principais` | 58 |
| 9 | `doutrina espírita` | 49 |
| 10 | `léon denis` | 48 |
| 11 | `justiça divina` | 45 |
| 12 | `livro espíritos` | 42 |
| 13 | `dores alma` | 40 |
| 14 | `leitura espírita` | 38 |
| 15 | `chico xavier` | 32 |
| 16 | `segundo espiritismo` | 32 |
| 17 | `viagem espírita` | 32 |
| 18 | `allan kardec` | 32 |
| 19 | `evangelho segundo` | 31 |
| 20 | `kardec kardec` | 30 |

## Atividade no tempo

Período coberto: **2026-04** → **2026-04** (1 meses).

### Sparkline por tipo

```
ingest     █  total=29
lint       █  total=17
query      █  total=6
refactor   █  total=4
setup      █  total=2
```

### Tabela mensal

| Mês | ingest | lint | query | refactor | setup | Total |
|-----|---|---|---|---|---|-------|
| 2026-04 | 29 | 17 | 6 | 4 | 2 | 58 |

### Dias mais ativos

| Data | Entradas |
|------|----------|
| 2026-04-07 | 15 |
| 2026-04-15 | 13 |
| 2026-04-06 | 10 |
| 2026-04-19 | 9 |
| 2026-04-16 | 6 |
| 2026-04-05 | 2 |
| 2026-04-08 | 2 |
| 2026-04-18 | 1 |

## Tamanho das páginas

```
<200        130  ██████████████████████████████
200-500      93  █████████████████████
500-1000     25  █████
1000-2000     8  █
>2000         1  
```

### Maiores

- [[wiki/aprofundamentos/expiacao-e-arrependimento]] — 2238 palavras
- [[wiki/obras/atos-dos-apostolos]] — 1535 palavras
- [[wiki/sinteses/hierarquia-de-autoridade]] — 1490 palavras
- [[wiki/obras/as-dores-da-alma]] — 1402 palavras
- [[wiki/obras/evangelho-segundo-marcos]] — 1182 palavras
- [[wiki/obras/cristianismo-e-espiritismo]] — 1118 palavras
- [[wiki/obras/evangelho-segundo-lucas]] — 1116 palavras
- [[wiki/obras/evangelho-segundo-mateus]] — 1073 palavras
- [[wiki/obras/quando-o-invisivel-se-torna-inevitavel]] — 1061 palavras
- [[wiki/obras/evangelho-segundo-joao]] — 958 palavras

### Menores (candidatas a expansão)

- [[wiki/personalidades/carlos-mendonca]] — 51 palavras
- [[wiki/personalidades/chico-xavier]] — 71 palavras
- [[wiki/conceitos/pluralidade-das-existencias]] — 82 palavras
- [[wiki/personalidades/joseph-bre]] — 90 palavras
- [[wiki/conceitos/lei-de-conservacao]] — 92 palavras
- [[wiki/personalidades/espiritos-reveladores]] — 92 palavras
- [[wiki/personalidades/vinicius]] — 94 palavras
- [[wiki/personalidades/eric-stanislas]] — 96 palavras
- [[wiki/personalidades/erasto]] — 97 palavras
- [[wiki/personalidades/marques-de-saint-paul]] — 98 palavras

## Referências não resolvidas

Wikilinks `[[...]]` cujo target não existe na árvore — candidatos a páginas novas (quando frequentes) ou erros de digitação (quando raros).

_Nenhum wikilink quebrado._

## Sugestões automáticas

- **Termos frequentes sem página própria**: `kardec` (693), `espírito` (671), `espíritos` (663), `moral` (468), `vida` (451), `espírita` (386), `espiritual` (365), `homem` (317) — candidatos a novos conceitos ou sinônimos a padronizar.
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
