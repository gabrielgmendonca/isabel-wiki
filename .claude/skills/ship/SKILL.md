---
name: ship
description: Empacota o ciclo commit→land na wiki IsAbel — revisa diff, propõe mensagem de commit, invoca scripts/land-to-main.sh, trata conflitos por protocolo (rerere para merge=union, união cronológica em personalidades) e roda o lint determinístico ao final. Use com /ship, "leve para main", "ship".
---

# /ship

Gatilhos: `/ship` · "leve para main" · "ship esta branch"

Empacota a sequência stage → commit → land → lint que hoje é manual. **Não** invoca a skill `/lint` (que puxa LLM); roda o script determinístico no final, conforme política do projeto.

## Pré-condições

- Não estar em `main` (o script aborta nesse caso).
- `main` está checked out em alguma worktree (o script localiza via `git worktree list`).
- Trabalho em curso pode estar staged, unstaged ou já commitado.

## Passo 1 — Inventário

Em paralelo:

```bash
git status
git diff
git diff --cached
git rev-list --count main..HEAD
git log --oneline main..HEAD
```

Determinar o estado:

- **Já commitado, nada pendente** → pular para Passo 3.
- **Tem mudanças (staged ou não)** → seguir para Passo 2.
- **Sem commits novos sobre `main` e sem mudanças** → reportar "nada a fazer" e parar.

## Passo 2 — Commit

Analisar o diff e propor **uma** mensagem de commit coerente (1ª linha ≤ 72 chars, foco no "porquê" mais do que no "o quê"; PT-BR; sem prefixos convencionais — seguir estilo do `git log` recente). Apresentar a mensagem ao usuário.

Em modo auto, prosseguir; em modo manual, esperar OK explícito antes de commitar.

Stage seletivo — listar arquivos por nome em `git add`, nunca `git add -A` ou `git add .` (evita arrastar `.env`, artefatos etc.). Se houver arquivos suspeitos (qualquer coisa fora de `wiki/`, `raw/`, `scripts/`, `.claude/`, configs conhecidas), perguntar antes.

Commit com HEREDOC para preservar quebras:

```bash
git commit -m "$(cat <<'EOF'
<mensagem>

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

Se houver múltiplas unidades lógicas distintas no diff, propor **um commit por unidade** em vez de um único commit balaio. Confirmar com o usuário antes de commitar a sequência.

## Passo 3 — Land

```bash
./scripts/land-to-main.sh
```

Comportamento esperado:
- Verifica que a worktree atual está limpa e ahead de `main`.
- Localiza a worktree onde `main` está checked out.
- Faz `rebase` da branch atual sobre `main` com `rerere.enabled=true`.
- Fast-forward de `main` para o novo HEAD na worktree de `main`.
- Apaga a branch local (default; `--keep-branch` para evitar).

Se sair com código 0 → seguir para Passo 5.

Se sair com código 2 → conflito de rebase, ir para Passo 4. O script já abortou o rebase para deixar o estado limpo; vamos refazer manualmente.

Outros códigos → reportar erro literal e parar.

## Passo 4 — Conflito (refazer rebase manual)

```bash
git rebase main
```

Para cada arquivo em conflito (`git diff --name-only --diff-filter=U`), aplicar protocolo conforme tipo. As regras detalhadas estão em `.claude/rules/convencoes-merge.md`, que carrega automaticamente quando se edita `wiki/personalidades/**`, `log.md` ou `wiki/sinteses/catalogo.md`. Sumário:

- **`log.md`, `wiki/sinteses/catalogo.md`, `ROADMAP.md`** — não devem aparecer em conflito (driver `merge=union` resolve sozinho). Se aparecerem, é sinal de que `.gitattributes` regrediu — investigar antes de mexer.
- **`wiki/sinteses/estatisticas-da-wiki.md`** — `merge=ours` resolve. Se aparecer, idem acima. Se precisar regenerar de qualquer forma, rodar `/stats`.
- **`wiki/personalidades/<slug>.md`** — aplicar **união cronológica**: preservar ambos os lados, ordenar por data quando há marcador, deduplicar entradas, reler parágrafos para garantir costura.
- **Outras páginas da wiki** — resolver na mão, preservando o sentido doutrinário. Em dúvida, perguntar ao usuário (não chutar resolução em `wiki/conceitos/` ou `wiki/divergencias/`).

Após resolver **todos** os conflitos, rodar o lint determinístico (regra (c) de `convencoes-merge.md`):

```bash
uv run python .claude/skills/lint/scripts/lint_wiki.py
```

Se o lint reportar `errors > 0`, corrigir antes de continuar (link quebrado introduzido pela resolução é o caso mais comum). Avisos podem ficar para depois.

```bash
git add <arquivos resolvidos>
git rebase --continue
```

Repetir se houver novos conflitos no próximo commit do rebase. Quando o rebase concluir, rodar `./scripts/land-to-main.sh` de novo — agora vai cair no fast-forward direto.

## Passo 5 — Lint final

Rodar o script determinístico (não a skill):

```bash
uv run python .claude/skills/lint/scripts/lint_wiki.py
```

Reportar ao usuário:
- Hash curto de `main` após o land (`git -C <main-worktree> rev-parse --short HEAD`).
- Resumo do lint: total de errors/warnings/info. Erros novos introduzidos pelo land merecem destaque.
- Se houve conflito resolvido, mencionar quais arquivos.

Não chamar `/lint` (skill LLM). Se o usuário quiser análise complementar, sugerir `/lint` como passo separado.

## Regras

- **Nunca** `--no-verify`, `--force`, `reset --hard` ou amend de commit já existente. Se um hook falhar, fixar a causa-raiz e fazer **novo** commit.
- **Nunca** apagar a branch com `git branch -D` (force). O script usa `git branch -d` (verificação de merge) — respeitar.
- **Nunca** invocar `/ship` em modo recursivo (skill chamando skill). Se o usuário quiser combinar com `/ingest` ou `/stats`, esses rodam **antes** do `/ship`.
- Se o usuário pediu `/ship` mas a worktree está em estado inesperado (HEAD detached, branch já em main, mid-rebase de outra sessão), parar e reportar — não tentar consertar.
