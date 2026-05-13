---
tipo: sintese
fontes: [meta]
tags: [estatisticas, meta, grafo, vocabulario]
atualizado_em: 2026-05-12
status: ativo
---

# Estatísticas da wiki

## Pergunta motivadora

Como a wiki IsAbel está distribuída entre obras, conceitos e entidades? Quais são os nós centrais do grafo, quais páginas estão isoladas, que termos dominam o vocabulário, e como é o ritmo de ingestão ao longo do tempo? Esta página é **regenerada automaticamente** — serve como painel para orientar expansões, backlinks faltantes e possíveis novos conceitos.

> Gerado em **2026-05-12** por `.claude/skills/stats/scripts/stats_wiki.py`.

## Resumo executivo

- Páginas na wiki: **539**
- Arquivos em `raw/`: **1414**
- Nós no grafo: **527** · Arestas: **6502**
- Componentes fracamente conexos: **1** (maior: 527 nós)
- Páginas órfãs (sem backlinks): **5**
- Vocabulário único (após stopwords): **30120** termos
- Entradas em `log.md`: **193**
- Razão conceitos/questões: **192:14** (13.7)
- Questões únicas do LE citadas: **356/1019** (34.9%)
- Wikilinks não resolvidos (freq ≥ 5): **0** targets

## Cobertura por tipo

| Diretório | Páginas |
|-----------|---------|
| `wiki/obras/` | 100 |
| `wiki/conceitos/` | 192 |
| `wiki/personalidades/` | 180 |
| `wiki/questoes/` | 14 |
| `wiki/aprofundamentos/` | 11 |
| `wiki/sinteses/` | 13 |
| `wiki/divergencias/` | 22 |
| `wiki/index.md/` | 1 |
| `wiki/trilhas/` | 6 |

### Status

| Status | Páginas |
|--------|---------|
| `ativo` | 459 |
| `rascunho` | 59 |
| `aberta` | 20 |
| `concluída` | 1 |

## Cobertura doutrinária

Referências únicas do Pentateuco efetivamente citadas pela wiki (`(LE, q. N)`, `(ESE, cap. X, item Y)`, etc.). Mede o quanto da codificação já foi ancorado em páginas próprias.

| Obra | Unidade | Citadas | Total | Cobertura |
|------|---------|--------:|------:|----------:|
| LE | questões | 356 | 1019 | 34.9% |
| ESE | capítulos | 28 | 28 | 100.0% |
| Gênese | capítulos | 14 | 18 | 77.8% |
| LM | capítulos da 2ª parte | 27 | 33 | 81.8% |
| C&I | capítulos | 18 | 18 | 100.0% |

Referências `cap./item` únicas: ESE **140**, Gênese **68**, LM **37**, C&I **18**.

### Cobertura do LE por bloco de 100 questões

```
   1– 100  █████████····················   32/100 (32%)
 101– 200  ████████·····················   29/100 (29%)
 201– 300  █████························   19/100 (19%)
 301– 400  ████·························   16/100 (16%)
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
| 1 | [[wiki/conceitos/reencarnacao]] | 149 |
| 2 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 135 |
| 3 | [[wiki/obras/ceu-e-inferno]] | 131 |
| 4 | [[wiki/conceitos/perispirito]] | 116 |
| 5 | [[wiki/conceitos/caridade]] | 115 |
| 6 | [[wiki/personalidades/jesus]] | 113 |
| 7 | [[wiki/conceitos/obsessao]] | 110 |
| 8 | [[wiki/conceitos/mediunidade]] | 105 |
| 9 | [[wiki/conceitos/prece]] | 100 |
| 10 | [[wiki/conceitos/progresso-espiritual]] | 89 |
| 11 | [[wiki/obras/livro-dos-espiritos]] | 89 |
| 12 | [[wiki/conceitos/livre-arbitrio]] | 86 |
| 13 | [[wiki/obras/genese]] | 79 |
| 14 | [[wiki/conceitos/leis-morais/lei-de-causa-e-efeito]] | 78 |
| 15 | [[wiki/personalidades/allan-kardec]] | 75 |

### Mais conectores (grau de saída)

| # | Página | Out |
|---|--------|-----|
| 1 | [[wiki/obras/revista-espirita]] | 90 |
| 2 | [[wiki/obras/ceu-e-inferno]] | 86 |
| 3 | [[wiki/personalidades/chico-xavier]] | 53 |
| 4 | [[wiki/obras/primeira-epistola-de-pedro]] | 51 |
| 5 | [[wiki/obras/epistola-de-tiago]] | 50 |
| 6 | [[wiki/personalidades/paulo-de-tarso]] | 49 |
| 7 | [[wiki/personalidades/divaldo-franco]] | 46 |
| 8 | [[wiki/personalidades/jesus]] | 45 |
| 9 | [[wiki/obras/epistola-aos-romanos]] | 44 |
| 10 | [[wiki/sinteses/parabolas-de-jesus]] | 44 |
| 11 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 42 |
| 12 | [[wiki/obras/segunda-epistola-de-pedro]] | 42 |
| 13 | [[wiki/obras/epistola-aos-galatas]] | 41 |
| 14 | [[wiki/personalidades/joanna-de-angelis]] | 41 |
| 15 | [[wiki/sinteses/serie-psicologica-joanna-de-angelis]] | 41 |

### Centralidade (PageRank)

| # | Página | PR |
|---|--------|-----|
| 1 | [[wiki/conceitos/reencarnacao]] | 0.0244 |
| 2 | [[wiki/obras/evangelho-segundo-o-espiritismo]] | 0.0243 |
| 3 | [[wiki/conceitos/progresso-espiritual]] | 0.0224 |
| 4 | [[wiki/conceitos/livre-arbitrio]] | 0.0162 |
| 5 | [[wiki/obras/ceu-e-inferno]] | 0.0151 |
| 6 | [[wiki/conceitos/perispirito]] | 0.0146 |
| 7 | [[wiki/conceitos/caridade]] | 0.0139 |
| 8 | [[wiki/conceitos/mediunidade]] | 0.0129 |
| 9 | [[wiki/conceitos/leis-morais/lei-de-justica-amor-e-caridade]] | 0.0127 |
| 10 | [[wiki/conceitos/obsessao]] | 0.0127 |
| 11 | [[wiki/obras/livro-dos-espiritos]] | 0.0125 |
| 12 | [[wiki/conceitos/escala-espirita]] | 0.0108 |
| 13 | [[wiki/personalidades/jesus]] | 0.0103 |
| 14 | [[wiki/obras/livro-dos-mediuns]] | 0.0103 |
| 15 | [[wiki/conceitos/lei-natural]] | 0.0098 |

### Páginas órfãs (sem backlinks)

- [[wiki/questoes/esquecimento-do-passado]]
- [[wiki/questoes/obediencia-e-resignacao]]
- [[wiki/questoes/objetivo-da-encarnacao]]
- [[wiki/sinteses/colecao-fonte-viva-emmanuel]]
- [[wiki/sinteses/psicopatologias-na-doutrina-espirita]]

### Componentes isolados (≤ 2 nós)

_Nenhum._

## Vocabulário

### Top 50 termos

| # | Termo | Ocorrências |
|---|-------|-------------|
| 1 | `kardec` | 2388 |
| 2 | `espírito` | 2372 |
| 3 | `deus` | 2267 |
| 4 | `espíritos` | 1968 |
| 5 | `espírita` | 1941 |
| 6 | `moral` | 1797 |
| 7 | `vida` | 1378 |
| 8 | `espiritual` | 1369 |
| 9 | `jesus` | 1324 |
| 10 | `espiritismo` | 1316 |
| 11 | `homem` | 1044 |
| 12 | `cristo` | 1013 |
| 13 | `morte` | 963 |
| 14 | `doutrina` | 909 |
| 15 | `amor` | 907 |
| 16 | `leitura` | 882 |
| 17 | `corpo` | 819 |
| 18 | `médium` | 801 |
| 19 | `três` | 793 |
| 20 | `alma` | 781 |
| 21 | `mundo` | 740 |
| 22 | `paulo` | 720 |
| 23 | `caps` | 717 |
| 24 | `terra` | 711 |
| 25 | `obra` | 698 |
| 26 | `caso` | 661 |
| 27 | `caridade` | 631 |
| 28 | `princípio` | 584 |
| 29 | `item` | 559 |
| 30 | `próprio` | 553 |
| 31 | `toda` | 551 |
| 32 | `dois` | 547 |
| 33 | `contra` | 547 |
| 34 | `anos` | 545 |
| 35 | `andré` | 539 |
| 36 | `prece` | 537 |
| 37 | `obras` | 497 |
| 38 | `segundo` | 480 |
| 39 | `antes` | 480 |
| 40 | `progresso` | 478 |
| 41 | `mediunidade` | 469 |
| 42 | `espíritas` | 468 |
| 43 | `tese` | 463 |
| 44 | `prática` | 461 |
| 45 | `luiz` | 450 |
| 46 | `chave` | 446 |
| 47 | `reencarnação` | 437 |
| 48 | `própria` | 429 |
| 49 | `estado` | 419 |
| 50 | `senhor` | 417 |

### Top 20 bigramas

| # | Bigrama | Ocorrências |
|---|---------|-------------|
| 1 | `andré luiz` | 448 |
| 2 | `leitura espírita` | 306 |
| 3 | `chico xavier` | 235 |
| 4 | `livre arbítrio` | 216 |
| 5 | `aplicação prática` | 188 |
| 6 | `doutrina espírita` | 185 |
| 7 | `ensino kardec` | 154 |
| 8 | `plano espiritual` | 133 |
| 9 | `jesus cristo` | 121 |
| 10 | `revista espírita` | 116 |
| 11 | `após morte` | 114 |
| 12 | `mundo espiritual` | 111 |
| 13 | `joanna ângelis` | 109 |
| 14 | `allan kardec` | 108 |
| 15 | `emmanuel chico` | 107 |
| 16 | `texto integral` | 106 |
| 17 | `causa efeito` | 105 |
| 18 | `estudo espírita` | 104 |
| 19 | `vida futura` | 102 |
| 20 | `espírito verdade` | 99 |

## Atividade no tempo

Período coberto: **2026-04** → **2026-05** (2 meses).

### Sparkline por tipo

```
aprofundamento ▁█  total=1
estudo     █▅  total=20
glossario  ▄█  total=3
ingest     █▇  total=103
lint       █▃  total=47
refactor   █▃  total=17
setup      █▁  total=2
```

### Tabela mensal

| Mês | aprofundamento | estudo | glossario | ingest | lint | refactor | setup | Total |
|-----|---|---|---|---|---|---|---|-------|
| 2026-04 | 0 | 12 | 1 | 52 | 36 | 12 | 2 | 115 |
| 2026-05 | 1 | 8 | 2 | 51 | 11 | 5 | 0 | 78 |

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
<200        105  ████████████████
200-500     187  ██████████████████████████████
500-1000    143  ██████████████████████
1000-2000    65  ██████████
>2000        27  ████
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

- **5 páginas órfãs** (grau de entrada = 0) — considerar adicionar backlinks a partir de conceitos/obras relacionados.
- **Termos frequentes sem página própria**: `kardec` (2388), `espírito` (2372), `espíritos` (1968), `espírita` (1941), `moral` (1797), `vida` (1378), `espiritual` (1369), `espiritismo` (1316) — candidatos a novos conceitos ou sinônimos a padronizar.
- **3 blocos de 100 questões do LE com <20% de cobertura**: 201–300 (19/100), 301–400 (16/100), 401–500 (17/100). Priorizar extração de questões-chave desses intervalos para `wiki/questoes/`.

## Páginas referenciadas

- [[index]]
- `log.md`

## Fontes

- Script gerador: `.claude/skills/stats/scripts/stats_wiki.py` (execução em 2026-05-12).
- Corpus analisado: `wiki/**/*.md`, `log.md`, `raw/**/*.md`.
- Dependências: `networkx` (grafo, PageRank), `nltk` (stopwords PT-BR).
- Filtros: meta-páginas (`tipo: sintese` + tag `meta`) são excluídas de grafo, vocabulário, tamanho, cobertura doutrinária e wikilinks quebrados; seções-template (`## Fontes`, `## Páginas relacionadas`, `## Páginas referenciadas`, `## Conceitos relacionados`) são removidas antes da tokenização.
- Cobertura doutrinária: regex sobre citações inline `(LE, q. N)`, `(ESE, cap. X, item Y)`, `(Gênese, cap. X, item Y)`, `(LM, Nª parte, cap. X)`, `(C&I, Nª parte, cap. X)`. Totais canônicos: LE=1019q; ESE=28c; Gênese=18c; LM=33c (2ª parte); C&I=18c (11 + 7).
