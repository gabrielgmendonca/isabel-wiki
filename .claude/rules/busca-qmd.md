---
paths:
  - "wiki/**"
  - "raw/**"
---

# Busca em wiki/raw — preferir qmd

Para localizar conteúdo dentro de `wiki/**` ou `raw/**`, usar **`mcp__qmd__query`** antes de `grep`/`find`/`rg` ou `Read` exploratório.

## Quando qmd ganha

- Procurar conceito, citação ou trecho por significado (`vec`/`hyde`).
- Checar se já existe página antes de criar duplicata (`lex` + `vec`).
- Recuperar capítulo/questão pelo tema, não pelo nome de arquivo.
- Encontrar trechos onde a forma exata da palavra varia (acento, conjugação, sinônimo).

## Quando grep/find/rg ainda fazem sentido

- Listar arquivos por nome ou extensão (não por conteúdo).
- Contar ocorrências de string literal exata em todo o repo.
- Inspecionar frontmatter ou estrutura de diretório.
- Operações de manutenção (renomear referências, achar links quebrados).

## Como invocar

```
mcp__qmd__query(
  intent="<descrição curta da intenção>",
  collection="wiki" | "raw",
  searches=[
    {type: "lex", query: "<termos exatos>"},
    {type: "vec", query: "<paráfrase semântica>"},
  ]
)
```

- `intent` é obrigatório — passa contexto pro ranker e melhora os snippets.
- Combinar `lex` + `vec`. Adicionar `hyde` quando a resposta tiver formato previsível ("a q. X do LE diria…").
- `minScore: 0.5` filtra ruído quando o resultado vier disperso.
- Para abrir o documento depois, `mcp__qmd__get` aceita `file.md:100` para offset por linha.

## Antipadrão

`Bash(grep -r "termo" wiki/)` ou `Read wiki/conceitos/...` no escuro pra descobrir se algo existe. Custa mais tokens, perde matches semânticos, e a auditoria de 1/mai/2026 mostrou que esse reflexo é o motivo de qmd estar sendo usado em só 9% das sessões deste projeto — mesmo nas que fazem 5-8 buscas via Bash. Quando usado, qmd retorna scores 0.88-0.93 e responde a pergunta na primeira chamada.
