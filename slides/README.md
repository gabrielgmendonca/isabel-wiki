# Slides — palestras espíritas

Apresentações Marp geradas a partir de páginas da wiki, no padrão socrático Q&A.

## Estrutura

```
slides/
  themes/
    isabel.css                # tema customizado
    preview.md                # deck de demonstração do tema (versionado)
    assets/                   # fixture sintético usado só pelo preview
  <tema>/
    deck.md                   # Marp markdown (versionado)
    assets/                   # imagens + creditos.json (versionados)
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

Requer Node no PATH (Marp roda via `npx -y @marp-team/marp-cli@latest`). Para PPTX/PDF
é preciso `CHROME_PATH` apontando para um Chrome — em geral o Chrome for Testing do
puppeteer, em `~/.cache/puppeteer/chrome/*/chrome-mac-*/`.

## Preview do tema

`slides/themes/preview.md` é um deck de demonstração: um slide por classe (capa,
`.pergunta`, `.quote`, `.section`, split background, síntese) mais um espécime
tipográfico e um checklist. O cabeçalho de cada slide diz o que aquele slide testa.

Serve para inspecionar o `isabel.css` **sem gastar uma palestra real** — rodar sempre
que se mexer no tema e comparar o PDF:

```bash
uv run python .claude/skills/slides/scripts/build_deck.py slides/themes/preview.md --formats pdf
open slides/themes/build/preview.pdf
```

A imagem em `themes/assets/` é um fixture sintético (gradiente na paleta do tema), não
arte real — decks de palestra tomam arte em domínio público pela cascata de
`convencoes-imagens.md`.

## Slide que transborda

O `/lint` estima, sem renderizar nada, se algum slide estoura a caixa de 1080 × 560 px
e colide com o rodapé:

```bash
uv run python .claude/skills/lint/scripts/lint_wiki.py --check slide_overflow
```

É estimativa (severidade `info`) — o veredito continua sendo olhar o PDF. Conserto
típico: dividir a síntese em dois slides ou encurtar bullets. Um slide que transborda
de propósito declara `<!-- lint: overflow-esperado -->`.

## Convenções

Ver `.claude/rules/convencoes-slides.md`.

## Fora do Quartz

Esta pasta não é publicada pela wiki. Slides são produção pessoal, não fonte doutrinária.
