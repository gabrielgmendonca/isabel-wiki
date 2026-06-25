# Setup / Migração

Como subir a wiki do zero numa máquina nova. O git cobre quase tudo (conteúdo,
scripts, skills, configs); o que se perde numa máquina nova é **estado local** —
esta checklist o reconstrói. Visão geral do projeto: [`../README.md`](../README.md).

## Subir numa máquina nova (macOS)

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
   - Python — versão pinada em [`.python-version`](../.python-version) (via
     `brew install python@<versão>` ou pyenv) + [`uv`](https://docs.astral.sh/uv/)
     (`brew install uv`).
   - `libjpeg` — `brew install jpeg`. Quando o pin do Python é novo demais para
     haver wheel binário do `pillow` (puxado por `torchvision`), o `uv sync`
     compila do fonte e o build exige o libjpeg. O `jpeg` do Homebrew é
     *keg-only*; o `bootstrap.sh` exporta as flags do build automaticamente se a
     formula estiver instalada (logo, basta o `brew install jpeg`).
   - Node — `brew install node` (formula atual ≥ 22, já no PATH; CI usa Node
     22, mas ≥ 22 basta para o build local). Para cravar a paridade exata,
     `brew install node@22` funciona, mas é *keg-only* — siga o caveat impresso
     pelo `brew` (adicionar `/opt/homebrew/opt/node@22/bin` ao PATH), senão
     `node`/`npm` não ficam disponíveis.
   - `qmd` — `npm install -g @tobilu/qmd` (busca local; pacote npm, requer o
     Node acima; upstream [github.com/tobi/qmd](https://github.com/tobi/qmd)).
5. **Segredos** — `.env` não está no git:
   ```bash
   cp .env.example .env   # preencha do gerenciador de senhas
   ```
6. **`.claude/settings.local.json`** — não está no git. Copie da máquina antiga
   (contém a allowlist de permissões) ou recrie.
7. **Bootstrap** — recria `.venv` e o índice qmd:
   ```bash
   bash scripts/bootstrap.sh             # inclui o embed (custa horas)
   # ou: bash scripts/bootstrap.sh --skip-embed   # se for usar o atalho abaixo
   ```
8. **Registrar o MCP qmd no Claude Code** (escopo local deste projeto):
   ```bash
   claude mcp add qmd -- qmd --index isabel mcp
   ```
   Confira com `claude mcp list`. O registro (escopo local) vai para o arquivo
   de config do Claude Code — `~/.claude.json` por padrão, ou
   `$CLAUDE_CONFIG_DIR/.claude.json` se você definir `CLAUDE_CONFIG_DIR`
   (escolha pessoal de máquina; este projeto não exige nenhum valor).
9. **Smoke test**:
   ```bash
   uv run python .claude/skills/lint/scripts/lint_wiki.py   # 0 erros
   bash scripts/serve-local.sh                               # build + serve local
   bash scripts/preflight.sh                                 # tudo verde
   ```

> As convenções de projeto que antes viviam na memória local do Claude Code
> foram consolidadas em docs rastreados (`CLAUDE.md`, `.claude/rules/`,
> `.claude/skills/*/SKILL.md`) — **não** precisam ser migradas à mão.

## O que está / não está no git

| | Onde | Ação na máquina nova |
|---|---|---|
| **No git** | `wiki/`, `raw/` (inclui `*.index.md`/`*.resumo.md`), `scripts/`, `data/*.json`, `.claude/{rules,skills,hooks}` + `settings.json`, `.github/`, `pyproject.toml`, `uv.lock`, configs do Quartz | `git clone` resolve |
| **Fora do git, carregar à mão** | `.env`; `.claude/settings.local.json`; registro do MCP qmd; contextos `qmd` | passos 5, 6, 8 + `bootstrap.sh` |
| **Fora do git, regenerável** | `.venv/` (`uv sync`); índice qmd `~/.cache/qmd/isabel.sqlite` (~270 MB, embed custa horas) | `bootstrap.sh` |
| **Fora do git, não-essencial** | `books_with_links.json` (~47 MB) — entrada de `compile_book.py`, só p/ re-ingestar FEB; o `raw/` resultante já está no git | nenhuma (re-crawlear só se for re-ingestar; `bootstrap.sh` **não** gera este arquivo) |

`data/kardec-mapping.json` e os demais `data/*.json` **estão no git** — não
re-crawlear Kardecpedia/FEB.

## Atalho do índice qmd

`scripts/bootstrap.sh` recria o índice do zero — correto, mas `qmd embed` leva
horas. Se quiser pular isso e a máquina antiga ainda existe, copie o índice
pronto **antes** de rodar o bootstrap:

```bash
mkdir -p ~/.cache/qmd
scp 'maquina-antiga:~/.cache/qmd/isabel.sqlite*' ~/.cache/qmd/
bash scripts/bootstrap.sh --skip-embed
```

O projeto usa o índice **nomeado** `isabel` (`qmd --index isabel`), que mora em
`~/.cache/qmd/isabel.sqlite` e contém só as coleções `wiki`/`raw` desta wiki —
**não** confundir com `~/.cache/qmd/index.sqlite` (índice default do qmd, com
coleções de outros projetos como `kpi-*`). O glob `isabel.sqlite*` também leva
os arquivos `-wal`/`-shm`, caso a máquina antiga não tenha feito checkpoint.
