# Slides — palestras espíritas

Apresentações Marp geradas a partir de páginas da wiki, no padrão socrático Q&A.

## Estrutura

```
slides/
  themes/isabel.css           # tema customizado
  <tema>/
    deck.md                   # Marp markdown (versionado)
    build/                    # PPTX + PDF (gitignored)
```

## Workflow

Use a skill `/slides <página-wiki>` para gerar e construir um deck.

Manualmente:

```bash
# 1. Scaffold a partir de uma página wiki
uv run python .claude/skills/slides/scripts/scaffold_deck.py wiki/conceitos/leis-morais/lei-do-trabalho.md

# 2. Editar slides/lei-do-trabalho/deck.md à mão (refinar perguntas, adicionar parábola)

# 3. Build PPTX + PDF
uv run python .claude/skills/slides/scripts/build_deck.py slides/lei-do-trabalho/deck.md
```

Requer Node no PATH (Marp roda via `npx -y @marp-team/marp-cli@latest`).

## Convenções

Ver `.claude/rules/convencoes-slides.md`.

## Fora do Quartz

Esta pasta não é publicada pela wiki. Slides são produção pessoal, não fonte doutrinária.
