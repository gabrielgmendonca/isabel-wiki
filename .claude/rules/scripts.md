---
paths:
  - ".claude/skills/**"
---

# Scripts Python das skills

Para rodar scripts Python locais nesta wiki, sempre prefixar com `uv run python`:

```bash
uv run python .claude/skills/<skill>/scripts/<script>.py
```

Não usar `python` (macOS sem alias) nem `python3` direto (não usa o ambiente do projeto).

**No CI** (GitHub Actions, `.github/workflows/*`), o runner não tem `uv` — workflows usam `python3` e isso é correto. Não alterar comandos no CI.

Quando criar nova skill que invoque script Python, escrever os exemplos com `uv run python`. Não duplicar a regra dentro do `SKILL.md` — esta rule já está documentada em CLAUDE.md §5 e injetada automaticamente quando se edita arquivos em `.claude/skills/**`.
