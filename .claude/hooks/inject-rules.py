#!/usr/bin/env python3
"""PreToolUse hook: inject .claude/rules/*.md bodies whose frontmatter `paths:`
globs match the target of an Edit/Write/MultiEdit, or the wiki/raw path
referenced by a Bash search command (grep/rg/find/ag).

Also injects `convencoes-shell.md` unconditionally when a Bash command matches
a high-signal "shell hazard" pattern (`sed -i`, `mapfile`, `readarray`) — these
are the markers of bash-4-or-GNU habits that fail silently on macOS bash 3.2 +
BSD coreutils. Gate is by command regex, not by file path.

Outputs a `hookSpecificOutput` JSON with `additionalContext` so Claude sees the
rule before the tool runs. For file edits, also sets `permissionDecision: "allow"`
to keep the existing no-friction UX. For Bash, omits the permission decision so
the normal allowlist still gates execution.

Anti-bloat (cada rule entra no contexto uma vez, não a cada chamada):

- **Dedup por sessão**: cada rule é injetada no máximo 1× por (session_id,
  agent_id). Subagentes têm `agent_id` próprio, então recebem as rules mesmo
  que a sessão-mãe já as tenha visto. Estado em `$TMPDIR/isabel-inject-rules/`.
  `--reset` (hook SessionStart `compact|clear`) apaga o estado da sessão, pois a
  compactação descarta o que foi injetado.
- **`quando:`** (frontmatter, regex opcional): a rule só entra se o conteúdo
  sendo escrito (`new_string`/`content`) casar — ex.: mermaid só quando há
  bloco ```mermaid.
- **`bash: true`** (frontmatter): só rules marcadas assim entram num Bash de
  busca; as demais são sobre *escrever* e não se aplicam a um `grep`.
- **`repetir: true`** (frontmatter): reinjeta a rule a cada Bash de busca,
  ignorando o dedup (em edições ela segue entrando 1×) — para lembretes curtos
  cujo efeito depende da repetição (ex.: `busca-qmd`, contra o reflexo do grep).
"""
from __future__ import annotations

import fnmatch
import json
import os
import re
import sys
import tempfile
from pathlib import Path

import yaml

# Busca só conta em posição de comando (início de linha, após `|`, `;`, `&`,
# `(`, `$(`, `xargs`) — não quando "grep" aparece num argumento, numa mensagem
# de commit ou no corpo de um heredoc (que é removido antes do teste).
SEARCH_CMD_RE = re.compile(
    r"(?:^|[|;&(]|\$\(|\bxargs(?:\s+-\S+)*)\s*(?:sudo\s+)?"
    r"(?:grep|rg|ripgrep|fgrep|egrep|find|ag)\b",
    re.M,
)
HEREDOC_RE = re.compile(r"<<-?\s*(['\"]?)(\w+)\1[^\n]*\n.*?^\s*\2\s*$", re.S | re.M)
WIKI_RAW_REL_RE = re.compile(r"(?:^|[\s'\"=({])((?:wiki|raw)(?:/[\w\-./*?]+)?)")
# High-signal markers: sed in-place (BSD/GNU divergence + classic for+sed silent
# failure) and bash 4 array builtins (don't exist on macOS bash 3.2).
SHELL_HAZARD_RE = re.compile(r"\bsed\s+-i\b|\bmapfile\b|\breadarray\b")
SHELL_RULE_NAME = "convencoes-shell.md"


def parse_rule(text: str) -> tuple[dict, str]:
    """Return (frontmatter, body). frontmatter={} when absent or invalid."""
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    fm_raw = text[4:end]
    body = text[end + 5 :]

    try:
        fm = yaml.safe_load(fm_raw) or {}
    except yaml.YAMLError as exc:
        print(f"inject-rules: YAML parse error in frontmatter: {exc}", file=sys.stderr)
        return {}, body
    return (fm if isinstance(fm, dict) else {}), body


def rule_paths(fm: dict) -> list[str]:
    raw_paths = fm.get("paths")
    if isinstance(raw_paths, str):
        return [raw_paths]
    if isinstance(raw_paths, list):
        return [str(p) for p in raw_paths if p]
    return []


def written_content(tool_input: dict) -> str:
    """Texto que o Edit/Write/MultiEdit vai gravar (alvo do gate `quando:`)."""
    parts = [tool_input.get("new_string") or "", tool_input.get("content") or ""]
    for edit in tool_input.get("edits") or []:
        if isinstance(edit, dict):
            parts.append(edit.get("new_string") or "")
    return "\n".join(parts)


def state_file(event: dict) -> Path | None:
    session = event.get("session_id")
    if not session:
        return None
    key = session + ("-" + event["agent_id"] if event.get("agent_id") else "")
    key = re.sub(r"[^\w\-]", "_", key)
    return Path(tempfile.gettempdir()) / "isabel-inject-rules" / f"{key}.json"


def load_seen(path: Path | None) -> set[str]:
    if not path:
        return set()
    try:
        return set(json.loads(path.read_text()))
    except (OSError, ValueError):
        return set()


def save_seen(path: Path | None, seen: set[str]) -> None:
    if not path:
        return
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(sorted(seen)))
    except OSError as exc:
        print(f"inject-rules: cannot save state: {exc}", file=sys.stderr)


def reset(event: dict) -> None:
    """Apaga o estado da sessão (e de seus subagentes) após compact/clear."""
    session = event.get("session_id")
    if not session:
        return
    prefix = re.sub(r"[^\w\-]", "_", session)
    for f in (Path(tempfile.gettempdir()) / "isabel-inject-rules").glob(f"{prefix}*.json"):
        try:
            f.unlink()
        except OSError:
            pass


def path_matches(rel: str, pattern: str) -> bool:
    if pattern.endswith("/**"):
        prefix = pattern[:-3]
        return rel == prefix or rel.startswith(prefix + "/")
    if pattern.endswith("/*"):
        prefix = pattern[:-2]
        return "/" not in rel[len(prefix) + 1 :] if rel.startswith(prefix + "/") else False
    return fnmatch.fnmatch(rel, pattern)


def derive_rel(tool_name: str, tool_input: dict, cwd: str) -> str | None:
    """Return a repo-relative path for path-matching, or None to skip injection."""
    if tool_name in ("Edit", "Write", "MultiEdit"):
        target = tool_input.get("file_path")
        if not target:
            return None
        try:
            rel = os.path.relpath(target, cwd)
        except ValueError:
            return None
        rel = rel.replace(os.sep, "/")
        if rel.startswith("../") or rel == "..":
            return None
        return rel

    if tool_name == "Bash":
        cmd = HEREDOC_RE.sub("", tool_input.get("command") or "")
        if not SEARCH_CMD_RE.search(cmd):
            return None
        # Normalize absolute paths under cwd to relative form, then look for
        # the first reference to wiki/ or raw/ in the command.
        cwd_norm = cwd.rstrip("/") + "/"
        normalized = cmd.replace(cwd_norm, "")
        m = WIKI_RAW_REL_RE.search(normalized)
        if m:
            return m.group(1)
        return None

    return None


def _load_rule_body(rules_dir: Path, name: str) -> str | None:
    """Read a rule file by filename and return its body (frontmatter stripped)."""
    rule_file = rules_dir / name
    if not rule_file.is_file():
        return None
    try:
        text = rule_file.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"inject-rules: cannot read {name}: {exc}", file=sys.stderr)
        return None
    _, body = parse_rule(text)
    return body.strip()


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        print(f"inject-rules: invalid event JSON on stdin: {exc}", file=sys.stderr)
        return 0

    if "--reset" in sys.argv[1:]:
        reset(event)
        return 0

    tool_name = event.get("tool_name") or ""
    tool_input = event.get("tool_input") or {}
    cwd = event.get("cwd") or os.getcwd()

    rel = derive_rel(tool_name, tool_input, cwd)
    bash_cmd = tool_input.get("command") or "" if tool_name == "Bash" else ""
    shell_hazard = bool(bash_cmd and SHELL_HAZARD_RE.search(bash_cmd))

    if not rel and not shell_hazard:
        return 0

    rules_dir = Path(cwd) / ".claude" / "rules"
    if not rules_dir.is_dir():
        return 0

    is_edit = tool_name in ("Edit", "Write", "MultiEdit")
    content = written_content(tool_input) if is_edit else ""

    matched: list[tuple[str, str]] = []
    repeat: set[str] = set()
    if rel:
        for rule_file in sorted(rules_dir.glob("*.md")):
            try:
                text = rule_file.read_text(encoding="utf-8")
            except OSError as exc:
                print(f"inject-rules: cannot read {rule_file.name}: {exc}", file=sys.stderr)
                continue
            fm, body = parse_rule(text)
            paths = rule_paths(fm)
            if not paths or not any(path_matches(rel, p) for p in paths):
                continue
            if not is_edit and not fm.get("bash"):
                continue
            quando = fm.get("quando")
            if is_edit and quando and not re.search(str(quando), content, re.I | re.M):
                continue
            matched.append((rule_file.name, body.strip()))
            if fm.get("repetir"):
                repeat.add(rule_file.name)

    if shell_hazard and not any(n == SHELL_RULE_NAME for n, _ in matched):
        body = _load_rule_body(rules_dir, SHELL_RULE_NAME)
        if body:
            matched.append((SHELL_RULE_NAME, body))

    if not matched:
        return 0

    names = ", ".join(n for n, _ in matched)
    state = state_file(event)
    seen = load_seen(state)
    fresh = [(n, b) for n, b in matched if n not in seen or (n in repeat and not is_edit)]
    new_names = {n for n, _ in fresh} - seen
    if new_names:
        save_seen(state, seen | new_names)
    matched = fresh
    sections = "\n\n---\n\n".join(f"<!-- {n} -->\n{b}" for n, b in matched)
    header = (
        f"Regras do projeto aplicáveis a `{rel}` "
        if rel
        else "Regras do projeto aplicáveis ao comando Bash "
    )
    additional = (
        header
        + f"(carregadas automaticamente pelo hook inject-rules):\n\n{sections}"
    )

    hook_output: dict = {"hookEventName": "PreToolUse"}
    if matched:
        hook_output["additionalContext"] = additional
    elif not is_edit:
        return 0
    # Auto-allow only for file edits — Bash still goes through the normal
    # allowlist so this hook can never broaden permissions.
    if is_edit:
        hook_output["permissionDecision"] = "allow"
        hook_output["permissionDecisionReason"] = f"rules: {names}"

    json.dump({"hookSpecificOutput": hook_output}, sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
