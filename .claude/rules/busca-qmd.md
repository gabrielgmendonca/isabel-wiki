---
paths:
  - "wiki/**"
  - "raw/**"
bash: true
repetir: true
---

# Busca em wiki/raw — qmd antes de grep

Para achar conteúdo em `wiki/**` ou `raw/**` por significado (conceito, citação, "já existe página?"), usar `mcp__qmd__query` — não `grep -r` nem `Read` exploratório no escuro. `grep`/`find` só para nome de arquivo, string literal exata, frontmatter ou manutenção (renomear referências).

- Sempre `intent`; combinar `lex` + `vec`; `limit: 5`, `minScore: 0.5`, `collections` explícito.
- Arquivo `raw/` longo (>~1000 linhas): `mcp__qmd__get arquivo.md:<ini>-<fim>` em vez de `Read` integral.
- Obra monolítica em `raw/kardec/pentateuco/`: ler antes o `<obra>.index.md` (range de linhas por capítulo); "do que trata a obra?" → `<obra>.resumo.md`.
