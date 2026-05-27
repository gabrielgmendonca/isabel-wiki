---
paths:
  - "wiki/**"
---

# Verificação de citação — Pentateuco

Antes de afirmar uma citação do Pentateuco (`(LE, q. N)`, `(LM, item N)`, `(ESE, cap. X, item Y)`, `(C&I, Nª parte, cap. Y)`, `(Gênese, cap. X, item Y)`), rodar:

```
uv run python scripts/cite.py <SIGLA> "<ref>"
```

e copiar o texto literal. Não inferir paráfrase de questão/item — o texto kardecista tem formulações específicas que importam doutrinariamente, e citação imprecisa em página da wiki é o tipo de erro que `/lint` não pega (a estrutura está certa, o conteúdo está errado).

## Quando usar

- Sempre que vai escrever ou editar uma citação canônica em `wiki/**`.
- Quando a citação vier de memória ou conhecimento prévio — validar antes de afirmar.
- Quando o usuário cita uma questão/item em conversa e a resposta vai virar página: ancorar no texto literal.

## Como o script se comporta

- `resolve_locus` valida primeiro: se a referência não existe na obra (ex.: `q. 99999`, `cap. XLII`), aborta com exit code 2 e indica o `.index.md` da obra para conferência.
- Em locus válido, devolve cabeçalho com `path:linhas` + texto literal (pergunta + respostas + subitens + comentário de Kardec até a próxima questão ou heading).
- Subitens isolados: `q. 150b` retorna só o subitem b.

## Quando o script não cobre

- **Revista Espírita, Léon Denis, Chico Xavier e demais obras complementares**: fora do escopo v1. Citar com cuidado mas sem validador automático. Para essas, `mcp__qmd__query` com `lex` + `vec` recupera a passagem.
- **C&I 2ª parte (Exemplos)**: relatos nominais sem numeração — o script faz dump do capítulo inteiro com aviso.
- **Citações que parafraseiam a passagem** (em vez de citar literal): `cite.py` confirma o locus, mas não verifica que o argumento da frase corresponde ao texto. Para isso, complementar com `mcp__qmd__query` (vec) para conferir que o trecho corresponde semanticamente ao que você está afirmando.

## Em locus inválido

Se `cite.py` rejeitar com "fora do range" ou "inexistente", **não** ajustar a citação no chute. Buscar com `mcp__qmd__query` qual é o locus correto:

```python
mcp__qmd__query(
  intent="achar onde Kardec trata de <tema>",
  collections=["raw"],
  searches=[
    {type: "vec", query: "<paráfrase do tema>"},
    {type: "lex", query: "<termo exato>"},
  ],
)
```

Depois revalidar com `cite.py`.
