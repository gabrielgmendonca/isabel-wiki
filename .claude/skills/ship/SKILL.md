---
name: ship
description: Empacota o ciclo commit→land na wiki IsAbel — revisa diff, propõe mensagem de commit, invoca scripts/land-to-main.sh, trata conflitos por protocolo (rerere para merge=union, união cronológica em personalidades) e roda o lint determinístico ao final. Use com /ship, "leve para main", "ship".
---

# /ship

Gatilhos: `/ship` · "leve para main" · "ship esta branch"

Empacota a sequência stage → commit → land → lint que hoje é manual. **Não** invoca a skill `/lint` (que puxa LLM); roda o script determinístico no final, conforme política do projeto.

## Pré-condições

- Trabalho em curso pode estar staged, unstaged ou já commitado.
- `main` precisa estar checked out em alguma worktree e a branch atual não pode ser `main` (ambos requeridos pelo `land-to-main.sh`). Quando algum dos dois falha, o **Passo 0** abaixo conserta antes do Inventário.

## Passo 0 — Pre-flight de worktree

Rodar antes do Inventário para garantir as duas pré-condições do land script. Em paralelo:

```bash
git rev-parse --abbrev-ref HEAD
git worktree list | grep -q '\[main\]' && echo "main-em-worktree" || echo "main-sem-worktree"
git status --porcelain
```

(Não usar `git worktree list --porcelain` — o wrapper RTK do projeto reformata a saída e quebra o parse de campos `branch refs/heads/...`. O `grep` no formato humano é estável.)

Casos a tratar (em ordem):

1. **Branch atual é `main` e a working tree está limpa e não há nada a integrar** → `git status` vazio + `git rev-list --count origin/main..main` = 0. Reportar "nada a fazer" e parar.
2. **Branch atual é `main` com mudanças (staged/unstaged) ou commits locais não-pushados** → criar branch transitória `ship-pending-<HHMMSS>` (`git checkout -b ship-pending-$(date +%H%M%S)`). Mudanças e commits viajam junto. Avisar o usuário em uma linha qual nome foi usado. A branch é descartável: o land script a deleta no final.
3. **`main` não está checked out em nenhuma worktree** (consequência natural de [2], ou estado herdado) → criar worktree temporária:
   ```bash
   TEMP_MAIN="/tmp/isabel-main-ship-$(date +%H%M%S)"
   git worktree add "$TEMP_MAIN" main
   ```
   Marcar mentalmente que precisa cleanup no Passo 7. Não usar `.claude/worktrees/` para a temp — esse diretório é território de worktrees ativas do harness.
4. **Branch é feature e `main` já está em alguma worktree** → caminho feliz, seguir para Passo 1.

Se o passo 2 disparar, o passo 3 quase sempre dispara junto (criar branch a partir de main deixa main órfã). Tratar os dois sequencialmente.

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
- `git push origin main` ao final — obrigatório, falha o ship se push falhar. Mantém `origin/main` em sincronia para que `claude -w` (que ramifica de `origin/HEAD`) abra worktrees frescas.

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

Não chamar `/lint` (skill LLM). Se o usuário quiser análise complementar, sugerir `/lint` como passo separado.

## Passo 6 — Reindex qmd

Após o land, reindexar para que buscas posteriores enxerguem o que acabou de entrar em `main`:

```bash
qmd update && qmd embed
```

`qmd update` é instantâneo (~1s); `qmd embed` escala com o volume novo (segundos para um ship típico de 3-5 páginas; até ~1min se houve `/ingest` grande no ciclo). Rodar síncrono — sem isso, a próxima checagem de duplicata via qmd (no `/ingest` seguinte) pode mentir.

Se algum dos dois sair com código não-zero, reportar a saída literal e parar — não tentar consertar nem mascarar. O conteúdo já está em `main`, o index só ficou stale.

## Passo 7 — Cleanup do pre-flight

Só roda se o **Passo 0** criou worktree temporária para `main`. Após o land, a worktree atual está em detached HEAD (o script faz `git checkout --detach` antes de apagar a branch transitória) e `main` está apontando para o tip novo dentro da temp. Devolver `main` para a worktree primária:

```bash
git worktree remove "$TEMP_MAIN"
git checkout main
```

`git worktree remove` falha se a temp ficou suja — não deveria acontecer (o land script só toca arquivos via `merge --ff-only`), mas se acontecer, reportar literal e não forçar.

Se o Passo 0 não criou temp, pular este passo inteiro.

## Passo 8 — Reportar

- Hash curto de `main` após o land (`git -C <main-worktree> rev-parse --short HEAD`).
- Resumo do lint: total de errors/warnings/info. Erros novos introduzidos pelo land merecem destaque.
- Se houve conflito resolvido, mencionar quais arquivos.
- Linha curta com o resultado do reindex (ex.: `qmd: 5 docs novos, 12 chunks embedded em 8s`).
- Se o Passo 0 disparou (criação de branch ou temp worktree), uma linha mencionando — útil pra usuário reconstruir o estado mental.

## Regras

- **Nunca** `--no-verify`, `--force`, `reset --hard` ou amend de commit já existente. Se um hook falhar, fixar a causa-raiz e fazer **novo** commit.
- **Nunca** apagar a branch com `git branch -D` (force). O script usa `git branch -d` (verificação de merge) — respeitar.
- **Nunca** invocar `/ship` em modo recursivo (skill chamando skill). Se o usuário quiser combinar com `/ingest` ou `/stats`, esses rodam **antes** do `/ship`.
- Se o usuário pediu `/ship` mas a worktree está em estado inesperado (HEAD detached, mid-rebase de outra sessão, working tree de outra branch suja), parar e reportar — não tentar consertar. **Branch atual em `main` ou `main` órfã** são casos esperados e tratados pelo Passo 0 — não confundir com estado inesperado.
