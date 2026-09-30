---
paths:
  - "wiki/**"
---

# Verificação de citação — Pentateuco

- **Antes de afirmar** `(LE, q. N)`, `(ESE, cap. X, item Y)` etc.: `uv run python scripts/cite.py <SIGLA> "<ref>"` e conferir o texto literal. Não parafrasear de memória. (`q. 150b` devolve só o subitem; C&I 2ª parte devolve o capítulo inteiro.)
- **Aspa literal: nunca digitar de memória** — gerar com `insert_quote.py`, que aborta se não bater com a fonte:
  ```
  uv run python scripts/insert_quote.py LE "q. 358"
  uv run python scripts/insert_quote.py ESE "cap. XVII, item 3" --sentence "interroga"   # só a(s) frase(s)
  ```
  (`--italic`; `--path P --after "<âncora>"` insere direto no arquivo.)
- **Aspa não aparece no locus citado** → `uv run python scripts/reverse_locus.py <SIGLA> "<trecho>"`. Cobertura ~1.0 em outro locus = mal-atribuída (trocar a ref); baixa em todos = fabricada (tirar as aspas ou parafrasear). Revalidar com `cite.py`. Allowlist `data/citacao-aspas-aceitas.json` só após conferência manual.
- **Locus rejeitado** ("fora do range"/"inexistente") → não ajustar no chute; achar o locus com `mcp__qmd__query` em `raw` e revalidar.
- Fora do escopo do `cite.py` (RE, Denis, psicografias): localizar a passagem via qmd (`lex` + `vec`) e citar com cuidado. Paráfrase com locus válido ainda exige conferir que o trecho sustenta a afirmação.
