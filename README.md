# isabel-wiki

Wiki espírita mantida com GenAI e curadoria humana — base de conhecimento sobre
a Doutrina Espírita codificada por Allan Kardec, para estudo e preparação de
palestras. Publicada via Quartz no GitHub Pages.

- Propósito, tom e hierarquia de autoridade: [`CLAUDE.md`](CLAUDE.md)
- Roadmap e estado do projeto: [`ROADMAP.md`](ROADMAP.md)

## Setup / Migração

### Subir numa máquina nova (macOS)

O git cobre quase tudo (conteúdo, scripts, skills, configs). O que se perde numa
máquina nova é estado local — esta checklist o reconstrói.

1. **Pré-requisitos**: [Homebrew](https://brew.sh), `git`, `gh`, uma chave SSH
   cadastrada no GitHub e o [Claude Code](https://claude.com/claude-code).
2. **Clone**:
   ```bash
   git clone git@github.com:gabrielgmendonca/isabel-wiki.git
   cd isabel-wiki
   ```
3. **Diagnóstico** — o que ainda falta nesta máquina:
   ```bash
   bash scripts/preflight.sh
   ```
4. **Toolchain**:
   - Python — versão pinada em [`.python-version`](.python-version) (via
     `brew install python@<versão>` ou pyenv) + [`uv`](https://docs.astral.sh/uv/)
     (`brew install uv`).
   - Node — `brew install node@22` (CI usa Node 22; ≥22 serve para build local).
   - `qmd` — `brew install qmd` (busca local; upstream
     [github.com/tobi/qmd](https://github.com/tobi/qmd)).
   - `rtk` — Rust Token Killer (hook de otimização de tokens do Claude Code).
5. **Segredos** — `.env` não está no git:
   ```bash
   cp .env.example .env   # preencha do gerenciador de senhas
   ```
6. **`.claude/settings.local.json`** — não está no git. Copie da máquina antiga
   (contém o hook do RTK e a allowlist de permissões) ou recrie.
7. **Bootstrap** — recria `.venv` e o índice qmd:
   ```bash
   bash scripts/bootstrap.sh             # inclui o embed (custa horas)
   # ou: bash scripts/bootstrap.sh --skip-embed   # se for usar o atalho abaixo
   ```
8. **Registrar o MCP qmd no Claude Code** (escopo local deste projeto):
   ```bash
   claude mcp add qmd -- qmd --index isabel mcp
   ```
   Confira com `claude mcp list`. O registro fica em
   `${CLAUDE_CONFIG_DIR:-~/.claude}/.claude.json` — `CLAUDE_CONFIG_DIR` é uma
   escolha pessoal de máquina; o default do Claude Code é `~/.claude`.
9. **Smoke test**:
   ```bash
   uv run python .claude/skills/lint/scripts/lint_wiki.py   # 0 erros
   bash scripts/serve-local.sh                               # build + serve local
   bash scripts/preflight.sh                                 # tudo verde
   ```

> As convenções de projeto que antes viviam na memória local do Claude Code
> foram consolidadas em docs rastreados (`CLAUDE.md`, `.claude/rules/`,
> `.claude/skills/*/SKILL.md`) — **não** precisam ser migradas à mão.

### O que está / não está no git

| | Onde | Ação na máquina nova |
|---|---|---|
| **No git** | `wiki/`, `raw/` (inclui `*.index.md`/`*.resumo.md`), `scripts/`, `data/*.json`, `.claude/{rules,skills,hooks}` + `settings.json`, `.github/`, `pyproject.toml`, `uv.lock`, configs do Quartz | `git clone` resolve |
| **Fora do git, carregar à mão** | `.env`; `.claude/settings.local.json`; registro do MCP qmd; contextos `qmd` | passos 5, 6, 8 + `bootstrap.sh` |
| **Fora do git, regenerável** | `.venv/` (`uv sync`); índice qmd `~/.cache/qmd/index.sqlite` (~335 MB, embed custa horas); `books_with_links.json` (~47 MB, só p/ re-ingest) | `bootstrap.sh` |

`data/kardec-mapping.json` e os demais `data/*.json` **estão no git** — não
re-crawlear Kardecpedia/FEB.

### Atalho do índice qmd

`scripts/bootstrap.sh` recria o índice do zero — correto, mas `qmd embed` leva
horas. Se quiser pular isso e a máquina antiga ainda existe, copie o índice
pronto **antes** de rodar o bootstrap:

```bash
mkdir -p ~/.cache/qmd
scp maquina-antiga:~/.cache/qmd/index.sqlite ~/.cache/qmd/
bash scripts/bootstrap.sh --skip-embed
```

O `index.sqlite` carrega junto coleções de outros projetos (`kpi-*`) — inócuo
para esta wiki; as coleções `wiki`/`raw` continuam funcionando.
