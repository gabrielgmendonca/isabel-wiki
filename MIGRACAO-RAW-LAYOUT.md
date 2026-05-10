# Migração do layout de `raw/`

Plano transitório para zerar o legado de slugs/hierarquia em `raw/`. Quando todos os warnings de `check_raw_layout` forem resolvidos, este arquivo pode ser removido (ou virar nota histórica no `ROADMAP.md`).

## Esquema canônico (referência)

- Slugs kebab-case ASCII puros: `^[a-z0-9]+(-[a-z0-9]+)*$` — sem `_`, sem espaços, sem maiúsculas, sem diacríticos, sem sufixos artefato (`_compress`, `-min`, `pdf`, `c3a[0-9a-f]`).
- `raw/mediuns/<medium>/<autor-espiritual>/<obra>` (sempre 3 níveis).
- `<slug>.pdf` no nível pai + `<slug>/<slug>.md` + `<slug>/_meta.json` + `<slug>/assets/_page_*.jpeg`.
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
| `raw/autores/leon-denis` | pendente | PDFs com `Snake_Case` e `Title Case`; sufixos `-min` e `_` URL-encoded. |
| `raw/mediuns/chico-xavier` | pendente | 28 obras soltas no nível do médium. Mapping `OBRA_TO_SPIRIT` distribui entre Emmanuel/André Luiz/Humberto-de-Campos. Revisar mapping antes de aplicar. |
| `raw/mediuns/divaldo-franco` | pendente | 19 obras + diretórios bagunçados. `__default__` envia para `joanna-de-angelis/`. Casos `c3a0`/`c3a2` (UTF-8 escapado) tratados via `_decode_url_encoded`. |
| `raw/mediuns/francisco-neto` | pendente | 1 obra (`AS-DORES-DA-ALMA`) → `francisco-neto/diversos/`. |
| `raw/autores/cairbar-schutel`, `euripedes-barsanulfo`, `martins-peralva` | sem ação | Apenas `.gitkeep`, nada para migrar. |

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

## Próximos refinos opcionais (após zerar legado)

- Promover severidade de `check_raw_layout` de `warning` para `error`.
- Hookar o check em `PostToolUse` para arquivos novos em `raw/` (similar ao que `lint-on-edit.py` faz para `wiki/**`).
- Estender `OBRA_TO_SPIRIT` para Hammed/Francisco-Neto se mais obras chegarem.
