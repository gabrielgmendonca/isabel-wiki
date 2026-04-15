---
name: slides
description: Gera apresentação Marp (PPTX + PDF) a partir de uma página da wiki IsAbel, no padrão socrático Q&A das palestras de Gabriel. Use com /slides <página-wiki>, "gerar slides de X", "fazer deck para palestra sobre X".
---

# /slides

Gatilhos: `/slides <página>` · "fazer slides de X" · "deck para palestra sobre X"

Convenções obrigatórias: ler `.claude/rules/convencoes-slides.md` antes de propor outline.

## Passo 1 — Validar input

Confirmar que o argumento é uma página existente em `wiki/`. Se vier só um tema (ex: `/slides livre-arbítrio`), procurar o arquivo correspondente em `wiki/conceitos/`, `wiki/sinteses/`, `wiki/questoes/`. Se ambíguo, perguntar.

## Passo 2 — Scaffold determinístico

Rodar:

```bash
uv run python .claude/skills/slides/scripts/scaffold_deck.py <caminho-wiki> [--out slides/<slug>/deck.md]
```

O script extrai título, frontmatter, blockquotes com citação e seção `## Fontes`, e emite um `deck.md` Marp com a estrutura esquelética:

1. Capa (título + fontes + autor + data)
2. Para cada blockquote com citação detectada: par Q-slide (heading da seção) + A-slide (citação literal entre aspas, com referência)
3. Slide vazio antes do encerramento
4. `## Fontes` no último slide com `<!-- _class: source -->`

Reportar caminho do `deck.md` criado.

## Passo 3 — Buscar material complementar via qmd

Para enriquecer o esqueleto, consultar qmd:

- `query` na collection `wiki` por questões do Pentateuco relacionadas (filtrar por `wiki/questoes/`)
- `query` por parábola que ilustre o tema (`wiki/parabolas/` se existir, senão `wiki/conceitos/` com tag pertinente)
- Se a página tem `[[wikilinks]]` para parábolas/personalidades, priorizar essas

## Passo 4 — Apresentar outline ao usuário

Antes de editar o `deck.md`, listar:

- **Capa proposta** (título, fonte, autor, data)
- **Pergunta de abertura** (1 frase, retórica)
- **3-5 pares Q&A** já no esqueleto + sugestões de adicionais
- **Parábola sugerida** (qual, de qual fonte) — perguntar se concorda
- **Síntese final** (volta à pergunta de abertura)

Aguardar validação. Não construir antes de o usuário confirmar.

## Passo 5 — Refinar o deck.md

Editar `slides/<slug>/deck.md` com base no outline aprovado:

- Reescrever perguntas em tom socrático (curtas, diretas, retóricas)
- Garantir respostas literais entre aspas com citação no formato CLAUDE.md §3
- Inserir 1 slide em branco entre blocos temáticos (`---\n\n<!-- _class: blank -->\n`)
- Adicionar parábola (2-4 slides)
- Síntese final retomando a pergunta de abertura
- `## Fontes` no padrão wiki

## Passo 6 — Build PPTX + PDF

```bash
uv run python .claude/skills/slides/scripts/build_deck.py slides/<slug>/deck.md
```

O script chama `npx -y @marp-team/marp-cli@latest` duas vezes (PPTX + PDF) e escreve em `slides/<slug>/build/`. Requer Node disponível no PATH.

Flag `--no-build` no Passo 2 pula o build (útil quando Node ausente).

## Passo 7 — Reportar

Listar:
- Caminho do `deck.md` (versionado)
- Caminhos de `build/deck.pptx` e `build/deck.pdf` (gitignored)
- Sugestão: abrir o PPTX no Keynote para ajustes finais (imagens de fundo, transições)

## Regras

- **Citação obrigatória** em toda afirmação doutrinária (CLAUDE.md §3).
- **Hierarquia de autoridade** respeitada (CLAUDE.md §2): Pentateuco prevalece.
- **Não publicar na wiki**: `slides/` fica fora do build do Quartz.
- **Não tocar `wiki/`** durante a geração — slides são derivados, não fontes.
- O usuário valida o outline antes do build.
