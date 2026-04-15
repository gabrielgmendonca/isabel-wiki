---
name: stats
description: Gera página de estatísticas da wiki IsAbel — roda script Python que compila métricas de grafo (networkx), vocabulário, atividade temporal e cobertura, e escreve `wiki/sinteses/estatisticas-da-wiki.md`. Use com /stats, "gerar estatísticas", "atualizar estatísticas".
---

# /stats

Gatilhos: `/stats` · "gerar estatísticas" · "atualizar estatísticas da wiki"

## Passo 1 — Rodar script

Da raiz do projeto:

```bash
uv run python .claude/skills/stats/scripts/stats_wiki.py
```

O script sobrescreve `wiki/sinteses/estatisticas-da-wiki.md` com um painel determinístico contendo:

- Totais e cobertura por tipo / status.
- Grafo: top por grau de entrada, saída e PageRank; órfãos; componentes isolados.
- Vocabulário: top 50 palavras (stopwords PT-BR via `nltk`) + top 20 bigramas.
- Atividade mensal a partir de `log.md` (sparkline ASCII).
- Tamanho das páginas (histograma textual, extremos).
- Sugestões automáticas (órfãs, termos sem página, componentes isolados).

## Passo 2 — Atualizar índice e log

Se esta é a primeira execução e a página ainda não está em `index.md`:

1. Adicionar `- [[wiki/sinteses/estatisticas-da-wiki]] — painel estatístico gerado automaticamente` na seção Sínteses.
2. Adicionar entrada em `log.md`: `## [YYYY-MM-DD] setup | Página de estatísticas da wiki`.

Em regenerações subsequentes, apenas rodar o script.

## Passo 3 — Lint de sanidade (opcional)

```bash
uv run python .claude/skills/lint/scripts/lint_wiki.py
```

Verifica que a página gerada passa nos checks da wiki.
