# Migração do layout de `raw/`

Plano transitório para zerar o legado de slugs/hierarquia em `raw/`. **Concluído em 2026-05-10** — `check_raw_layout` zera; este arquivo pode ser removido ou virar nota histórica no `ROADMAP.md`. Mantido enquanto os refinos opcionais (severidade `error`, hook PostToolUse) não forem promovidos.

## Esquema canônico (referência)

- Slugs kebab-case ASCII puros: `^[a-z0-9]+(-[a-z0-9]+)*$` — sem `_`, sem espaços, sem maiúsculas, sem diacríticos, sem sufixos artefato (`_compress`, `-min`, `pdf`, `c3a[0-9a-f]`).
- `raw/mediuns/<medium>/<autor-espiritual>/<obra>` (sempre 3 níveis).
- `<slug>.pdf` no nível pai + `<slug>/<slug>.md` + `<slug>/<slug>_meta.json` + `<slug>/assets/_page_*.jpeg`. O sufixo `_meta` no `.json` é o nome produzido pelo extrator (marker-pdf, etc.) e fica preservado — o lint reconhece `<slug>_meta` como par válido do `<slug>.md`.
- `<TÍTULO>.md` + `summary-<TÍTULO>.md` em palestras ficam lado a lado (ver `.claude/rules/convencoes-palestras.md`).

## Ferramentas

- **Detectar**: `uv run python .claude/skills/lint/scripts/lint_wiki.py --check raw_layout`
- **Migrar (dry-run)**: `uv run python scripts/normalize_raw_layout.py --dry-run [--scope raw/<subdir>]`
- **Migrar (apply)**: `uv run python scripts/normalize_raw_layout.py --apply --scope raw/<subdir>`
- **Exceções manuais**: `raw/.normalize-exceptions.txt` (paths a pular, um por linha).

## Estado

| Escopo | Status | Notas |
|---|---|---|
| `raw/palestras` | concluído | 19 renames aplicados em 2026-05-09. Pares `<TÍTULO>` + `summary-` preservados. |
| `raw/mediuns/francisco-neto` | concluído | 2026-05-10 — 4 renames: `AS-DORES-DA-ALMA` → `diversos/as-dores-da-alma`. |
| `raw/mediuns/chico-xavier` | concluído | 2026-05-10 — 28 obras distribuídas: emmanuel/ (12), andre-luiz/ (15), humberto-de-campos/ (1 — Boa Nova). 114 wikilinks atualizados. |
| `raw/autores/leon-denis` | concluído | 2026-05-10 — 174 renames (4 obras + 170 imagens em `assets/`). Sufixo `-min` removido. 4 wikilinks atualizados. |
| `raw/mediuns/divaldo-franco` | concluído | 2026-05-10 — 175 renames + 8 obras novas incorporadas no layout canônico. `c3a0`/`c3a2` decodificados. 73 wikilinks atualizados. |
| `raw/autores/cairbar-schutel`, `euripedes-barsanulfo`, `martins-peralva` | sem ação | Apenas `.gitkeep`, nada para migrar. |

**Estado final (2026-05-10):** `check_raw_layout` retorna 0 achados em todo o `raw/`. Migração completa.

## Workflow recomendado por escopo

1. Rodar dry-run com `--scope raw/<subdir>`.
2. Conferir saída — particularmente a inferência de autor espiritual em médiuns. Para casos onde o normalizador joga em `diversos/` mas o autor é conhecido, adicionar entrada em `OBRA_TO_SPIRIT` em `scripts/normalize_raw_layout.py`.
3. `--apply --scope raw/<subdir>`.
4. `git status` para revisar renames.
5. **Diretórios bagunçados em mediuns** (caso Divaldo): rodar `--apply --scope` uma segunda vez. A primeira passada move os diretórios; a segunda canonicaliza arquivos dentro.
6. Re-rodar lint: `uv run python .claude/skills/lint/scripts/lint_wiki.py --check raw_layout` — confirmar que warnings caíram para zero no escopo.
7. Commitar (`/ship` ou commit manual).

## Casos que exigem atenção humana

- **Inferência de autor espiritual ambígua** em obras de Chico Xavier não cobertas pelo mapping. Auditar o resultado em `mediuns/chico-xavier/` após dry-run.
- **PDFs sem extrato** (`pdf_without_extract`): decidir se vale extrair ou se o PDF é arquivado bruto.
- **Imagens fora de `assets/`** (`images_not_in_assets`): 17 ocorrências; o normalizador move automaticamente.
- **`raw/mediuns/divaldo-franco/jesus-e-o-evangelho-c3a0-luz-...`**: nome com UTF-8 escapado; o normalizador agora decodifica para "à"/"â". Conferir resultado.
- **Split state após apply** (caso `momentos-de-felicidade` em divaldo-franco, 2026-05-10): o normalizador moveu o `.pdf` para `joanna-de-angelis/` mas deixou o diretório `<obra>/` com `.md`+`_meta.json` no nível anterior. Resolução manual via `git mv <obra> joanna-de-angelis/<obra>`. Caso reapareça em outros médiuns, vale investigar o `infer_spirit_author` para garantir que diretório e PDF tomem a mesma decisão.

## Próximos refinos opcionais (após zerar legado)

- Promover severidade de `check_raw_layout` de `warning` para `error`.
- Hookar o check em `PostToolUse` para arquivos novos em `raw/` (similar ao que `lint-on-edit.py` faz para `wiki/**`).
- Estender `OBRA_TO_SPIRIT` para Hammed/Francisco-Neto se mais obras chegarem.
