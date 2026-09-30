---
paths:
  - ".claude/skills/dreno/**"
  - "scripts/loop-diario.sh"
  - "scripts/com.isabel.loop-diario.plist"
---

# Invariantes do /dreno e do loop diário

- **Promover não bumpa `atualizado_em`.** Bumpar devolve a página à fila do Opus como `atualizado-apos-critica` → diferida de novo → rascunho de novo: moto-perpétuo. Travado em `tests/test_dreno.py`.
- **Slug ambíguo nunca promove** (bucket F), vale para `[ ]` **e** `[x]` do §11. Contar só `abertos`/`fechados` não basta: um `[x]` ambíguo somaria `fechados` em todas as homônimas e promoveria todas. Travado em `tests/test_dreno.py`.
- **Nada automescla.** Os dois níveis do loop entregam PR e esperam revisão humana. O auto-merge do nível 0 foi removido (2026-07-14): o guarda falhava aberto, e promover apaga do site o aviso `DraftNotice`. Só religar com o verificador descrito no ROADMAP §5 (Python sobre `git diff --cached --name-status`; todo arquivo `M` + `wiki/**/*.md`; única diferença a chave `status:`).
- O loop **nunca toca no working tree**: opera na worktree dedicada resetada a `origin/main`.
