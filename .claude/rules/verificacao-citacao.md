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

> **Vai ESCREVER uma aspa literal? Use `insert_quote.py` — nunca digite de memória.** O texto verbatim vem da fonte e é auto-verificado; é a Fase 2 do ROADMAP §12 (fechar a torneira da fabricação na origem).
>
> ```
> uv run python scripts/insert_quote.py LE "q. 358"                                   # blockquote do locus inteiro
> uv run python scripts/insert_quote.py ESE "cap. XVII, item 3" --sentence "interroga"  # só a(s) frase(s) com o trecho
> ```
>
> Emite `> "<verbatim>" (SIGLA, ref)` pronto para colar. `--sentence "<trecho>"` recorta da própria fonte a(s) frase(s) que contêm o trecho (útil para citar um pedaço de um item longo sem digitar nada); `--italic` para o estilo em itálico; `--path P --after "<âncora>"` insere no arquivo após a 1ª linha com a âncora. Se o texto não bater verbatim com a fonte (cobertura <0.95) ou o `--sentence` não casar, **aborta** — não emite aspa fabricada. A aspa do Pentateuco nasce da fonte, não da memória da LLM.

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

## Aspa não bate no locus citado → índice reverso

Se a aspa literal que você quer atribuir a `(SIGLA, ref)` **não aparecer** no texto que o `cite.py` devolve (ou você suspeita do locus), rode o **índice reverso** — dada a aspa, ele acha em que questão/item ela realmente mora (cobertura contígua sobre a obra inteira, robusta a frase quebrada entre linhas, onde `grep` falha):

```
uv run python scripts/reverse_locus.py <SIGLA> "<trecho da aspa>"
```

Devolve o top-N loci por cobertura. Cobertura ~1.0 num locus diferente do citado = **aspa mal-atribuída** (trocar o `ref` pelo achado). Cobertura baixa em todos = **aspa fabricada** (de-quote ou parafrasear). Depois revalidar com `cite.py`. O mesmo motor roda no lint em dois checks: **`check_quote_misattributed`** (`warning`, no hook PostToolUse — uma mal-atribuição nova é apontada já na edição, com a sugestão de troca de locus) e **`check_literal_quote_exists`** (`info`, fora do hook — fabricadas/paráfrases/incertas, alimenta `reports/citacao/triagem-aspas.md`). FP verificado à mão de mal-atribuição entra na allowlist `data/citacao-aspas-aceitas.json` (não silenciar no chute — só com conferência).

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
