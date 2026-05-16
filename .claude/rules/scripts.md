---
paths:
  - ".claude/skills/**"
  - "scripts/**"
---

# Scripts e automação

## Onde mora um script

- Script auxiliar de uma skill → `.claude/skills/<skill>/scripts/<arquivo>.py` (padrão Claude Code; não jogar em `scripts/` na raiz).
- Script de pipeline/curadoria da wiki, reusado fora de uma skill → `scripts/` na raiz.

## Como rodar

Para rodar scripts Python locais nesta wiki, sempre prefixar com `uv run python`:

```bash
uv run python .claude/skills/<skill>/scripts/<script>.py
```

Não usar `python` (macOS sem alias) nem `python3` direto (não usa o ambiente do projeto).

**No CI** (GitHub Actions, `.github/workflows/*`), o runner não tem `uv` — workflows usam `python3` e isso é correto. Não alterar comandos no CI.

Quando criar nova skill que invoque script Python, escrever os exemplos com `uv run python`. Não duplicar a regra dentro do `SKILL.md` — esta rule já está documentada em CLAUDE.md §5 e injetada automaticamente quando se edita arquivos em `.claude/skills/**`.

## Dependência madura > conversor caseiro

Para domínios bem cobertos por bibliotecas estabelecidas — HTML→Markdown, MD→HTML, parsing de YAML/TOML, slugify, datas — preferir **adicionar a dependência** (`uv add <pkg>`) a escrever um wrapper ad hoc (ex.: conversor manual em BeautifulSoup). Antes de propor um parser/conversor custom de ~30+ linhas, verificar se há lib bem mantida no PyPI e propor `uv add` no plano. Não vale para lógica de negócio específica do projeto.

## Lint determinístico em fluxos automáticos

Em automação — skills wrapper (`/ship`), hooks `PostToolUse`, loops (`/autolint`) — invocar o script determinístico `.claude/skills/lint/scripts/lint_wiki.py`, **não** a skill `/lint` (que puxa LLM para análise editorial). O script já cobre os checks estruturais (frontmatter, wikilinks, taxonomia, direitos); LLM em loop/hook é caro e o ganho é marginal. A skill `/lint` permanece para uso interativo dirigido pelo usuário. Mesmo num `/autolint` que corrija via LLM, a fase de detecção e re-validação roda no script.
