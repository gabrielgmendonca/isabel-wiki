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
  collections=["wiki"],            # ou ["raw"], ou ambas
  limit=5,
  minScore=0.5,
  searches=[
    {type: "lex", query: "<termos exatos>"},
    {type: "vec", query: "<paráfrase semântica>"},
  ]
)
```

- `intent` é obrigatório — passa contexto pro ranker e melhora os snippets.
- Combinar `lex` + `vec`. Adicionar `hyde` quando a resposta tiver formato previsível ("a q. X do LE diria…").

### Defaults de triagem (não exaustão)

- `limit: 5` em vez do default 10 do servidor. Aumentar pontualmente quando a busca for genuinamente exaustiva (lint manual, auditoria de cobertura).
- `minScore: 0.5` filtra ruído quando o resultado vier disperso.
- `collections` explícito (`["wiki"]` ou `["raw"]`) — buscar nas duas só quando faz sentido (ex.: checagem de duplicata cobrindo curado e fonte).

### Abrir o documento depois

`mcp__qmd__get` aceita offset por linha em `file.md:100` ou `file.md:100-300`. **Para arquivos em `raw/` com mais de ~1000 linhas (Revista Espírita por ano, Livro dos Médiuns, transcrições longas) preferir sempre `get` com offset a `Read` integral** — ler 200 linhas relevantes em vez de 12K do arquivo todo.

### Pré-resumos para obras monolíticas

Algumas obras nível 1/2 ultrapassam 5K linhas e não dão para fragmentar por natureza (LM, Gênese, ESE). Para essas, há dois artefatos adjacentes ao arquivo monolítico:

- `<obra>.index.md` — índice estrutural (capítulos, range de linhas, primeira sentença). ~100-200 linhas. Gerado deterministicamente por `scripts/generate_obra_index.py`.
- `<obra>.resumo.md` — síntese executiva (~500 palavras: propósito, escopo, aportes, quando recorrer). Gerado uma única vez por subagente Haiku.

**Antes de abrir o arquivo monolítico em `raw/kardec/pentateuco/`, ler o `.index.md` correspondente.** Ele indica o range de linhas do capítulo desejado, que vira `mcp__qmd__get <obra>.md:<inicio>-<fim>`. Para "do que trata esta obra?", o `.resumo.md` resolve sem abrir nem o índice.

Glob para descobrir: `ls raw/kardec/pentateuco/*.index.md raw/kardec/pentateuco/*.resumo.md`.

## Antipadrão

`Bash(grep -r "termo" wiki/)` ou `Read wiki/conceitos/...` no escuro pra descobrir se algo existe. Custa mais tokens, perde matches semânticos, e a auditoria de 1/mai/2026 mostrou que esse reflexo é o motivo de qmd estar sendo usado em só 9% das sessões deste projeto — mesmo nas que fazem 5-8 buscas via Bash. Quando usado, qmd retorna scores 0.88-0.93 e responde a pergunta na primeira chamada.
