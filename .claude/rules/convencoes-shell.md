---
paths:
  - ".claude/skills/**"
  - ".claude/hooks/**"
  - "scripts/**"
---

# Shell no macOS — bash 3.2 + BSD coreutils

Hábitos de bash 4/GNU falham **em silêncio** aqui.

- **Não existe**: `mapfile`/`readarray`, `declare -A`, `${var,,}`/`${var^^}`, `[[ -v var ]]`, `globstar` (`wiki/**/*.md` vira `wiki/*/*.md` → usar `find wiki -name '*.md'`).
- **BSD ≠ GNU**: `sed -i '' 's/X/Y/' f` (o `''` é obrigatório); sem `grep -P`, `date -d`, `readlink -f`.
- **`for` + `sed -i` em vários arquivos**: sai 0 mesmo sem mudar nada. Listar alvos com `grep -rl`, contar antes e depois, encadear com `&&`. Acima de ~5 arquivos ou regex não trivial → Python (`uv run python`).
- **Edição em massa em `wiki/**`**: preferir `Edit` por arquivo ou Python — `sed` pula o hook `lint-on-edit`; se usar, rodar o lint completo depois.
