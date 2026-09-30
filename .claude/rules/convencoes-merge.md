---
paths:
  - "wiki/personalidades/**"
  - "log.md"
  - "wiki/sinteses/catalogo.md"
---

# Convenções de merge (worktrees paralelas)

- **`.gitattributes`**: `log.md`, `wiki/sinteses/catalogo.md`, `ROADMAP.md` → `merge=union` (append-only; conferir a ordem cronológica depois). `wiki/sinteses/estatisticas-da-wiki.md` → `merge=ours` (é só regenerar com `/stats`). `rerere` está ligado.
- **`wiki/personalidades/**` — união cronológica** (sem `merge=union`, é prosa): preservar os dois lados, intercalar por data (ano da obra/palestra), mesclar duplicatas mantendo a versão mais completa, reler o parágrafo e costurar. Frontmatter (`tags:`, `fontes:`): união + dedup + ordem canônica.
- **Após resolver qualquer conflito**, antes de `git add` + `git rebase --continue`: `uv run python .claude/skills/lint/scripts/lint_wiki.py` (o script, não a skill `/lint`).
