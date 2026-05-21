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
"""
from __future__ import annotations

import fnmatch
import json
import os
import re
import sys
from pathlib import Path

import yaml

SEARCH_CMD_RE = re.compile(r"\b(grep|rg|ripgrep|fgrep|egrep|find|ag)\b")
WIKI_RAW_REL_RE = re.compile(r"(?:^|[\s'\"=({])((?:wiki|raw)(?:/[\w\-./*?]+)?)")
# High-signal markers: sed in-place (BSD/GNU divergence + classic for+sed silent
# failure) and bash 4 array builtins (don't exist on macOS bash 3.2).
SHELL_HAZARD_RE = re.compile(r"\bsed\s+-i\b|\bmapfile\b|\breadarray\b")
SHELL_RULE_NAME = "convencoes-shell.md"


def parse_frontmatter(text: str) -> tuple[list[str], str]:
    """Return (paths, body). paths=[] when frontmatter is absent or has no `paths:` key."""
    if not text.startswith("---\n"):
        return [], text
    end = text.find("\n---\n", 4)
    if end == -1:
        return [], text
    fm_raw = text[4:end]
    body = text[end + 5 :]

    try:
        fm = yaml.safe_load(fm_raw) or {}
    except yaml.YAMLError as exc:
        print(f"inject-rules: YAML parse error in frontmatter: {exc}", file=sys.stderr)
        return [], body

    raw_paths = fm.get("paths") if isinstance(fm, dict) else None
    if isinstance(raw_paths, str):
        return [raw_paths], body
    if isinstance(raw_paths, list):
        return [str(p) for p in raw_paths if p], body
    return [], body


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
        cmd = tool_input.get("command") or ""
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
    _, body = parse_frontmatter(text)
    return body.strip()


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        print(f"inject-rules: invalid event JSON on stdin: {exc}", file=sys.stderr)
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

    matched: list[tuple[str, str]] = []
    if rel:
        for rule_file in sorted(rules_dir.glob("*.md")):
            try:
                text = rule_file.read_text(encoding="utf-8")
            except OSError as exc:
                print(f"inject-rules: cannot read {rule_file.name}: {exc}", file=sys.stderr)
                continue
            paths, body = parse_frontmatter(text)
            if not paths:
                continue
            if any(path_matches(rel, p) for p in paths):
                matched.append((rule_file.name, body.strip()))

    if shell_hazard and not any(n == SHELL_RULE_NAME for n, _ in matched):
        body = _load_rule_body(rules_dir, SHELL_RULE_NAME)
        if body:
            matched.append((SHELL_RULE_NAME, body))

    if not matched:
        return 0

    names = ", ".join(n for n, _ in matched)
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

    hook_output: dict = {
        "hookEventName": "PreToolUse",
        "additionalContext": additional,
    }
    # Auto-allow only for file edits — Bash still goes through the normal
    # allowlist so this hook can never broaden permissions.
    if tool_name in ("Edit", "Write", "MultiEdit"):
        hook_output["permissionDecision"] = "allow"
        hook_output["permissionDecisionReason"] = f"rules: {names}"

    json.dump({"hookSpecificOutput": hook_output}, sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
