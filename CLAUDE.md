# IsAbel — Wiki Espírita

Idioma: **PT-BR** em todas as páginas geradas.

## 1. Propósito e tom

Base de conhecimento pessoal sobre a Doutrina Espírita codificada por Allan Kardec. Uso: estudos e preparação de palestras em casas espíritas. Tom: estudante kardecista sério — respeitoso, fraterno, didático. Sem ironia, relativismo acadêmico distanciado ou devocionalismo excessivo.

**Princípio de crescimento**: cada pergunta doutrinária é oportunidade de capitalizar conhecimento — transformar resposta efêmera em página citável. Default é arquivar; só não arquivar quando o conteúdo for claramente operacional ou efêmero.

## 2. Hierarquia de autoridade

| Nível | Fontes |
|-------|--------|
| **Primordial** | Ensinamentos morais de Jesus (Evangelhos canônicos), lidos à luz do Pentateuco |
| **1 — Pentateuco** | LE, LM, ESE, C&I, Gênese |
| **2 — Kardec complementar** | OPE, OQE, Revista Espírita, Viagem Espírita em 1862 |
| **3 — Consagrados** | Chico Xavier, Divaldo, Léon Denis, Cairbar, Peralva, Eurípedes, Emmanuel, André Luiz, Joanna de Ângelis, Bezerra; apóstolos seletivamente citados por Kardec |
| **4 — Secundários** | Hammed/Espírito Santo Neto, palestras isoladas — citar com consciência do tier |
| **Fora de escopo** | Umbanda, Candomblé, Ramatís, teosofia, antroposofia, ocultismo, neoespiritismo que relativiza o Pentateuco — **não ingerir sem confirmação explícita** |

Regra de ouro: quando nível 2/3/4 contradiz o nível 1, Kardec prevalece. A divergência é registrada, nunca apagada. Análise completa e tratamento de divergências evangélicas em [[wiki/sinteses/hierarquia-de-autoridade]] (e em `regra-divergencia.md` quando for editar `wiki/**`).

## 3. Citação obrigatória

Toda afirmação doutrinária precisa de citação. Formatos:

- `(LE, q. 150)` · `(LE, Introdução, item IV)` · `(LM, 2ª parte, cap. XX, item 230)`
- `(ESE, cap. XVII, item 4)` · `(C&I, 1ª parte, cap. VI)` · `(Gênese, cap. XI, item 13)`
- `(RE, jan/1858, p. 12)` · `(OPE, "Manifestações dos Espíritos")`
- `(Emmanuel / Chico Xavier, *O Consolador*, q. 123)` · `(Léon Denis, *O Problema do Ser*, cap. IV)`

**Obras psicografadas**: citar como `Autor espiritual / Médium`. Conferir o frontmatter de `raw/mediuns/<médium>/<obra>.md` (campo `Autor espiritual:`) — o médium não é o autor. Não inferir autor a partir do médium.

Toda página termina com `## Fontes`. Detentores de direitos e limites de citação para obras protegidas estão em `convencoes-paginas.md` (carrega ao editar `wiki/**`).

## 4. Workflows e estudo

Skills cobrem `/ingest`, `/lint`, `/slides`, `/stats`, `/glossario` (autocontidos em `.claude/skills/`). Build público exclui `raw/` (`quartz.config.ts` `ignorePatterns`); lint (`check_raw_excluded`) trava regressão. Auto-link de citações e glossário cultural rodam no CI sobre cópia em `/tmp/quartz/content` — source markdown não é alterado.

**Para responder dúvidas doutrinárias**: buscar com `qmd` (coleções `wiki` e `raw`, sempre com `intent`, combinando `lex` + `vec`); citar começando por Jesus/Pentateuco; capitalizar a resposta em página citável (`wiki/sinteses/` para panoramas, `wiki/aprofundamentos/` para estudo sistemático, `wiki/questoes/` para Q&A ancorada em uma única questão/item) e listar em `wiki/sinteses/catalogo.md` + `log.md`. Pular só quando a pergunta for puramente operacional.

## 5. Regras condicionais

`.claude/rules/*.md` são injetadas via hook `PreToolUse` (`.claude/hooks/inject-rules.py`) quando o `paths:` do frontmatter bate com o arquivo de Edit/Write/MultiEdit. Listar com `ls .claude/rules/`. Mover detalhe editorial para uma rule é a forma de manter este CLAUDE.md enxuto.

<!-- rtk-instructions v2 -->
# RTK (Rust Token Killer) - Token-Optimized Commands

## Golden Rule

**Always prefix commands with `rtk`**. If RTK has a dedicated filter, it uses it. If not, it passes through unchanged. This means RTK is always safe to use.

**Important**: Even in command chains with `&&`, use `rtk`:
```bash
# ❌ Wrong
git add . && git commit -m "msg" && git push

# ✅ Correct
rtk git add . && rtk git commit -m "msg" && rtk git push
```

## RTK Commands by Workflow

### Build & Compile (80-90% savings)
```bash
rtk cargo build         # Cargo build output
rtk cargo check         # Cargo check output
rtk cargo clippy        # Clippy warnings grouped by file (80%)
rtk tsc                 # TypeScript errors grouped by file/code (83%)
rtk lint                # ESLint/Biome violations grouped (84%)
rtk prettier --check    # Files needing format only (70%)
rtk next build          # Next.js build with route metrics (87%)
```

### Test (60-99% savings)
```bash
rtk cargo test          # Cargo test failures only (90%)
rtk go test             # Go test failures only (90%)
rtk jest                # Jest failures only (99.5%)
rtk vitest              # Vitest failures only (99.5%)
rtk playwright test     # Playwright failures only (94%)
rtk pytest              # Python test failures only (90%)
rtk rake test           # Ruby test failures only (90%)
rtk rspec               # RSpec test failures only (60%)
rtk test <cmd>          # Generic test wrapper - failures only
```

### Git (59-80% savings)
```bash
rtk git status          # Compact status
rtk git log             # Compact log (works with all git flags)
rtk git diff            # Compact diff (80%)
rtk git show            # Compact show (80%)
rtk git add             # Ultra-compact confirmations (59%)
rtk git commit          # Ultra-compact confirmations (59%)
rtk git push            # Ultra-compact confirmations
rtk git pull            # Ultra-compact confirmations
rtk git branch          # Compact branch list
rtk git fetch           # Compact fetch
rtk git stash           # Compact stash
rtk git worktree        # Compact worktree
```

Note: Git passthrough works for ALL subcommands, even those not explicitly listed.

### GitHub (26-87% savings)
```bash
rtk gh pr view <num>    # Compact PR view (87%)
rtk gh pr checks        # Compact PR checks (79%)
rtk gh run list         # Compact workflow runs (82%)
rtk gh issue list       # Compact issue list (80%)
rtk gh api              # Compact API responses (26%)
```

### JavaScript/TypeScript Tooling (70-90% savings)
```bash
rtk pnpm list           # Compact dependency tree (70%)
rtk pnpm outdated       # Compact outdated packages (80%)
rtk pnpm install        # Compact install output (90%)
rtk npm run <script>    # Compact npm script output
rtk npx <cmd>           # Compact npx command output
rtk prisma              # Prisma without ASCII art (88%)
```

### Files & Search (60-75% savings)
```bash
rtk ls <path>           # Tree format, compact (65%)
rtk read <file>         # Code reading with filtering (60%)
rtk grep <pattern>      # Search grouped by file (75%)
rtk find <pattern>      # Find grouped by directory (70%)
```

### Analysis & Debug (70-90% savings)
```bash
rtk err <cmd>           # Filter errors only from any command
rtk log <file>          # Deduplicated logs with counts
rtk json <file>         # JSON structure without values
rtk deps                # Dependency overview
rtk env                 # Environment variables compact
rtk summary <cmd>       # Smart summary of command output
rtk diff                # Ultra-compact diffs
```

### Infrastructure (85% savings)
```bash
rtk docker ps           # Compact container list
rtk docker images       # Compact image list
rtk docker logs <c>     # Deduplicated logs
rtk kubectl get         # Compact resource list
rtk kubectl logs        # Deduplicated pod logs
```

### Network (65-70% savings)
```bash
rtk curl <url>          # Compact HTTP responses (70%)
rtk wget <url>          # Compact download output (65%)
```

### Meta Commands
```bash
rtk gain                # View token savings statistics
rtk gain --history      # View command history with savings
rtk discover            # Analyze Claude Code sessions for missed RTK usage
rtk proxy <cmd>         # Run command without filtering (for debugging)
rtk init                # Add RTK instructions to CLAUDE.md
rtk init --global       # Add RTK to ~/.claude/CLAUDE.md
```

## Token Savings Overview

| Category | Commands | Typical Savings |
|----------|----------|-----------------|
| Tests | vitest, playwright, cargo test | 90-99% |
| Build | next, tsc, lint, prettier | 70-87% |
| Git | status, log, diff, add, commit | 59-80% |
| GitHub | gh pr, gh run, gh issue | 26-87% |
| Package Managers | pnpm, npm, npx | 70-90% |
| Files | ls, read, grep, find | 60-75% |
| Infrastructure | docker, kubectl | 85% |
| Network | curl, wget | 65-70% |

Overall average: **60-90% token reduction** on common development operations.
<!-- /rtk-instructions -->