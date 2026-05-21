---
paths:
  - ".claude/skills/**"
  - ".claude/hooks/**"
  - "scripts/**"
---

# Shell gotchas — bash 3.2 e substituições multi-arquivo

macOS default é **bash 3.2.57** e **BSD** sed/awk/find. Hábitos de bash 4+ ou GNU coreutils falham silenciosamente. Esta rule também é injetada antes de cada Bash que contém `sed -i`, `mapfile` ou `readarray` (`.claude/hooks/inject-rules.py` — gate por regex no comando).

## (a) Bash 3.2 baseline — não usar

- `mapfile`/`readarray` (bash 4) → `while IFS= read -r line; do …; done < file`.
- `declare -A` / array associativo (bash 4) → array indexado + função de lookup, ou Python.
- `${var,,}` / `${var^^}` (bash 4) → `tr '[:upper:]' '[:lower:]'`.
- `[[ -v var ]]` (bash 4.2) → `[[ -n "${var+x}" ]]`.
- `globstar` (`**/`) não está ligado por default — `wiki/**/*.md` em bash 3.2 expande como `wiki/*/*.md` (uma pasta só). Use `find wiki -name '*.md'`.

Quando precisar dessas features, escrever em Python (`uv run python`) — ver `scripts.md`.

## (b) BSD vs GNU — `sed -i` é a armadilha mais comum

```bash
# ERRADO no macOS — sintaxe GNU; BSD interpreta '' como sufixo de backup e quebra
sed -i 's/X/Y/g' file.md

# CERTO no macOS — BSD exige string vazia explícita
sed -i '' 's/X/Y/g' file.md
```

Outras divergências silenciosas: `grep -P` (PCRE só em GNU), `date -d` (GNU) vs `date -j -f` (BSD), `readlink -f` (GNU), `xargs --no-run-if-empty` (GNU) vs `xargs` BSD (que já não roda comando vazio). Para script portável ou regex não-trivial, **Python**.

## (c) `for`+`sed` multi-arquivo: proibido sem verificação

O padrão clássico falha silencioso:

```bash
# ANTIPADRÃO — exit 0 mesmo quando nada mudou
for f in wiki/**/*.md; do sed -i '' 's/X/Y/g' "$f"; done
```

Modos de falha que esse loop esconde:

1. Glob não expandiu (sem `globstar` em bash 3.2, `wiki/**/*.md` vira um arquivo literal ou `wiki/*/*.md`).
2. Nenhum arquivo continha `X` — `sed` retorna 0, loop reporta sucesso, nada mudou.
3. `X` continha caractere de regex (`.`, `/`, `&`, `[`) e bateu em mais coisa que o esperado.
4. Substituição truncou newline ou multi-byte (UTF-8 + locale `C`).

Quando for inevitável fazer em Bash (script único, baixo risco), aplicar este protocolo:

1. **Listar alvos explicitamente** — `find wiki -name '*.md'` ou `grep -rl <padrão>`, nunca confiar em glob de bash 3.2.
2. **`grep -l` antes** — confirmar que o padrão existe e contar os arquivos esperados.
3. **`grep -l` ou `diff` depois** — confirmar que a substituição materializou na contagem prevista. Anotar antes/depois.
4. **Não silenciar exit** — `set -e` no script; em one-liner, encadear com `&&` e não com `;`.

```bash
# CERTO — explícito, verificado, falha alta
antes=$(grep -rl 'X' wiki/ --include='*.md')
echo "$antes" | wc -l                                   # ex.: 12
for f in $antes; do sed -i '' 's/X/Y/g' "$f"; done
grep -rl 'X' wiki/ --include='*.md' | head              # esperado: vazio
grep -rl 'Y' wiki/ --include='*.md' | wc -l             # esperado: ≥ 12
```

Acima de ~5 arquivos ou com regex não-trivial, **Python**: `pathlib.Path.read_text/write_text`, regex compilado, exceções por arquivo. Custo de ~10 linhas; benefício é vê-lo falhar.

## (d) Bulk-edit em `wiki/**`: prefira Edit por arquivo

A wiki tem hook `PostToolUse` (`lint-on-edit.py`) que roda `lint_wiki.py --file` após cada `Edit`/`Write`/`MultiEdit` em `wiki/**/*.md`. Substituição em massa via `sed` **pula** esse hook — drift de frontmatter, tag fora da taxonomia ou wikilink quebrado passa despercebido até o `/lint` global.

Para mudar texto em N páginas, default: loop em Python ou sequência de `Edit` por arquivo (dispara o hook). `sed -i` só quando a mudança é trivialmente reversível e o `/lint` completo será rodado depois (via `/ship` ou manualmente).
