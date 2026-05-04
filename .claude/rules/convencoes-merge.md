---
paths:
  - "wiki/personalidades/**"
  - "log.md"
  - "wiki/sinteses/catalogo.md"
---

# Convenções de merge

Esta wiki é editada em paralelo a partir de várias worktrees (`main` + `.claude/worktrees/*`). O comportamento abaixo já existe na prática há 5+ sessões; esta rule codifica para evitar re-derivação a cada conflito.

## (a) Drivers de merge declarados em `.gitattributes`

| Padrão | Driver | Motivo |
|---|---|---|
| `log.md` | `merge=union` | Append-only por convenção; concatena os dois lados em vez de gerar conflito. Pode embaralhar a ordem cronológica — revisar quando importar. |
| `wiki/sinteses/catalogo.md` | `merge=union` | Idem — só ganha entradas. |
| `ROADMAP.md` | `merge=union` | Idem. |
| `wiki/sinteses/estatisticas-da-wiki.md` | `merge=ours` | Gerado pelo `/stats`; conflito é ruído, basta regenerar. Driver `ours` precisa de `git config merge.ours.driver true` por clone (já feito neste). |

`rerere.enabled=true` está ligado no repo — resoluções repetidas (especialmente em catalogo/log) são reaproveitadas automaticamente em rebases subsequentes.

## (b) União cronológica em páginas de personalidade

Páginas em `wiki/personalidades/**` **não** têm `merge=union` — a estrutura é prosa e seções, não lista append-only, e a união cega quebraria parágrafos. Quando duas worktrees acrescentam material à mesma página (típico: ambas adicionam obra em `## Obras associadas`, ou ambas enriquecem o mesmo período da biografia), aplicar **união cronológica**:

1. **Preservar ambos os lados** do conflito — nunca descartar adições.
2. **Ordenar por data** quando há marcador (ano de obra, data de palestra). Se o lado A adicionou uma obra de 1958 e o lado B uma de 1962, intercalar na ordem cronológica da seção.
3. **Conferir duplicatas** — uma mesma obra pode ter sido adicionada nos dois lados com formulações diferentes. Mesclar em uma única entrada (tomar a versão mais completa).
4. **Reler o parágrafo** após resolver — adições paralelas no mesmo período biográfico podem precisar de uma frase de costura.

Conflitos em frontmatter de personalidade (campo `tags:` ou `fontes:` crescendo dos dois lados) seguem a mesma lógica: união dos valores, dedup, ordenação canônica.

## (c) Lint antes de continuar o rebase

Após resolver conflito manualmente em qualquer arquivo coberto por esta rule (ou em qualquer página da wiki), **sempre** rodar:

```bash
uv run python .claude/skills/lint/scripts/lint_wiki.py
```

Antes de `git add` + `git rebase --continue`. O lint pega wikilink quebrado introduzido pela resolução, frontmatter mal-formatado e tag fora dos namespaces canônicos. Resolução manual é a janela mais comum de drift.

Não invocar a skill `/lint` aqui — em automação use sempre o script Python determinístico (regra geral do projeto: ver `feedback_lint_deterministico_em_automacao` na auto-memória).
