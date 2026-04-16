#!/usr/bin/env python3
"""PreToolUse hook: inject .claude/rules/*.md bodies whose frontmatter `paths:`
globs match the Edit/Write/MultiEdit target file.

Outputs a `hookSpecificOutput` JSON with `additionalContext` so Claude sees the
rule before the tool runs. `permissionDecision: "allow"` keeps the normal no-
friction UX for file edits within the project.
"""
from __future__ import annotations

import fnmatch
import json
import os
import sys
from pathlib import Path


def parse_frontmatter(text: str) -> tuple[list[str], str]:
    """Return (paths, body). paths=[] when frontmatter is absent or has no `paths:` key."""
    if not text.startswith("---\n"):
        return [], text
    end = text.find("\n---\n", 4)
    if end == -1:
        return [], text
    fm = text[4:end]
    body = text[end + 5 :]

    paths: list[str] = []
    in_paths = False
    for raw in fm.splitlines():
        stripped = raw.strip()
        if not in_paths:
            if stripped.startswith("paths:"):
                in_paths = True
                rest = stripped[len("paths:") :].strip()
                if rest.startswith("[") and rest.endswith("]"):
                    inner = rest[1:-1]
                    for item in inner.split(","):
                        v = item.strip().strip('"').strip("'")
                        if v:
                            paths.append(v)
                    in_paths = False
            continue
        if stripped.startswith("- "):
            val = stripped[2:].strip().strip('"').strip("'")
            if val:
                paths.append(val)
        elif stripped and not stripped.startswith("#"):
            in_paths = False
    return paths, body


def path_matches(rel: str, pattern: str) -> bool:
    if pattern.endswith("/**"):
        prefix = pattern[:-3]
        return rel == prefix or rel.startswith(prefix + "/")
    if pattern.endswith("/*"):
        prefix = pattern[:-2]
        return "/" not in rel[len(prefix) + 1 :] if rel.startswith(prefix + "/") else False
    return fnmatch.fnmatch(rel, pattern)


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except Exception:
        return 0

    tool_input = event.get("tool_input") or {}
    target = tool_input.get("file_path")
    if not target:
        return 0

    cwd = event.get("cwd") or os.getcwd()
    try:
        rel = os.path.relpath(target, cwd)
    except ValueError:
        return 0
    rel = rel.replace(os.sep, "/")
    if rel.startswith("../") or rel == "..":
        return 0

    rules_dir = Path(cwd) / ".claude" / "rules"
    if not rules_dir.is_dir():
        return 0

    matched: list[tuple[str, str]] = []
    for rule_file in sorted(rules_dir.glob("*.md")):
        try:
            text = rule_file.read_text(encoding="utf-8")
        except OSError:
            continue
        paths, body = parse_frontmatter(text)
        if not paths:
            continue
        if any(path_matches(rel, p) for p in paths):
            matched.append((rule_file.name, body.strip()))

    if not matched:
        return 0

    names = ", ".join(n for n, _ in matched)
    sections = "\n\n---\n\n".join(f"<!-- {n} -->\n{b}" for n, b in matched)
    additional = (
        f"Regras do projeto aplicáveis a `{rel}` "
        f"(carregadas automaticamente pelo hook inject-rules):\n\n{sections}"
    )

    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "permissionDecisionReason": f"rules: {names}",
            "additionalContext": additional,
        }
    }
    json.dump(output, sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
