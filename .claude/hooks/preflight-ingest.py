#!/usr/bin/env python3
"""PreToolUse hook: pre-flight de branch antes de Write/Edit/MultiEdit em wiki/**.

Bloqueia (deny) quando o estado da árvore tornaria o trabalho perdido ou
ruidoso para mesclar:

- branch é `main` — toda página nova ou alterada em `wiki/**` deve viver numa
  feature branch / worktree, não direto em `main`.
- branch atrás de `main` — `git rev-list --count HEAD..main` > 0; mesclar
  agora vai gerar conflitos com regenerações já em `main`.

Equivalente determinístico do Passo 0 do `/ingest` (cwd-worktree + alinhamento
de branch). A checagem de existência de `raw/<caminho>` continua no SKILL —
o hook não sabe o caminho de origem no momento do Write.

Falhas de git (não é repo, sem ref `main`, etc.) são silenciosas: o hook
não bloqueia o que não consegue verificar.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def _git(cwd: str, *args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", cwd, *args],
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(f"preflight-ingest: git {' '.join(args)} falhou: {exc}", file=sys.stderr)
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def _deny(reason: str) -> None:
    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": reason,
            }
        },
        sys.stdout,
    )


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        print(f"preflight-ingest: invalid event JSON on stdin: {exc}", file=sys.stderr)
        return 0

    if event.get("tool_name") not in ("Edit", "Write", "MultiEdit"):
        return 0

    target_raw = (event.get("tool_input") or {}).get("file_path")
    if not target_raw:
        return 0

    cwd = event.get("cwd") or os.getcwd()
    try:
        rel = os.path.relpath(target_raw, cwd).replace(os.sep, "/")
    except ValueError:
        return 0
    if rel.startswith("../") or not rel.startswith("wiki/") or not rel.endswith(".md"):
        return 0

    branch = _git(cwd, "rev-parse", "--abbrev-ref", "HEAD")
    if not branch:
        return 0

    if branch == "main":
        _deny(
            f"Pre-flight do /ingest: edição em `{rel}` na branch `main`. "
            "Crie/abra uma worktree feature antes de escrever em wiki/** "
            "(ex.: `git worktree add .claude/worktrees/<slug> -b <slug>`) "
            "ou troque para uma branch feature. CLAUDE.md §5 + ROADMAP §1.3."
        )
        return 0

    behind_raw = _git(cwd, "rev-list", "--count", "HEAD..main")
    if behind_raw is None:
        return 0
    try:
        behind = int(behind_raw)
    except ValueError:
        return 0

    if behind > 0:
        _deny(
            f"Pre-flight do /ingest: branch `{branch}` está {behind} commit(s) "
            f"atrás de `main`. Rebase (`git rebase main`) ou merge antes de "
            f"editar `{rel}` — sem isso, regenerações já em `main` vão colidir "
            "ao subir. ROADMAP §1.3."
        )
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
