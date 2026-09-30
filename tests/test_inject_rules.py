"""Testes do hook inject-rules — rules entram no contexto uma vez, não a cada chamada.

`unittest` puro (o CI roda `python3 -m unittest discover -s tests` sem
dependências). O hook importa `yaml`; sem ele, os testes são pulados em vez de
derrubar o CI.

Invariantes:

  1. Dedup por sessão: a 2ª edição em wiki/** não reinjeta nada. Antes eram
     ~35 KB (~10k tokens) idênticos a cada Edit.
  2. Subagente (`agent_id`) tem estado próprio — recebe as rules mesmo que a
     sessão-mãe já as tenha visto.
  3. `--reset` (SessionStart compact|clear) devolve as rules, pois a
     compactação descarta o que foi injetado.
  4. `quando:` — mermaid/mundos só entram se o conteúdo escrito casar.
  5. Bash de busca recebe só rules `bash: true`; `repetir: true` reaparece a
     cada busca, mas não a cada edição.
  6. "grep" fora de posição de comando (mensagem de commit, heredoc) não é busca.
"""
from __future__ import annotations

import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / ".claude/hooks/inject-rules.py"
WIKI_BASE = {
    "busca-qmd.md",
    "convencoes-aliases.md",
    "convencoes-frontmatter.md",
    "convencoes-tags.md",
    "regra-divergencia.md",
    "verificacao-citacao.md",
}


@unittest.skipUnless(importlib.util.find_spec("yaml"), "hook requer PyYAML")
class InjectRulesTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.env = {**os.environ, "TMPDIR": self._tmp.name}

    def tearDown(self):
        self._tmp.cleanup()

    def run_hook(self, event: dict, *args: str) -> tuple[set[str], dict | None]:
        event = {"cwd": str(ROOT), **event}
        out = subprocess.run(
            [sys.executable, str(HOOK), *args],
            input=json.dumps(event), capture_output=True, text=True,
            cwd=ROOT, env=self.env, check=True,
        )
        if not out.stdout.strip():
            return set(), None
        hso = json.loads(out.stdout)["hookSpecificOutput"]
        rules = set(re.findall(r"<!-- (\S+) -->", hso.get("additionalContext", "")))
        return rules, hso

    def edit(self, content="texto", path="wiki/conceitos/x.md", session="S", agent=None):
        ev = {"session_id": session, "tool_name": "Edit",
              "tool_input": {"file_path": str(ROOT / path), "new_string": content}}
        if agent:
            ev["agent_id"] = agent
        return self.run_hook(ev)

    def bash(self, command, session="S"):
        return self.run_hook({"session_id": session, "tool_name": "Bash",
                              "tool_input": {"command": command}})

    def test_dedup_por_sessao(self):
        rules, hso = self.edit()
        self.assertEqual(rules, WIKI_BASE)
        rules, hso = self.edit()
        self.assertEqual(rules, set())
        self.assertEqual(hso["permissionDecision"], "allow")

    def test_subagente_tem_estado_proprio(self):
        self.edit()
        rules, _ = self.edit(agent="A1")
        self.assertEqual(rules, WIKI_BASE)

    def test_reset_devolve_as_rules(self):
        self.edit()
        self.edit(agent="A1")
        self.run_hook({"session_id": "S"}, "--reset")
        self.assertEqual(self.edit()[0], WIKI_BASE)
        self.assertEqual(self.edit(agent="A1")[0], WIKI_BASE)

    def test_quando_gate_por_conteudo(self):
        self.assertNotIn("convencoes-mermaid.md", self.edit()[0])
        rules, _ = self.edit("```mermaid\ngraph TD\n```\nnos mundos de regeneração")
        self.assertEqual(rules, {"convencoes-mermaid.md", "convencoes-mundos-habitados.md"})

    def test_bash_busca_so_rules_bash_e_repetir(self):
        self.assertEqual(self.bash("grep -r fé wiki/conceitos")[0], {"busca-qmd.md"})
        self.assertEqual(self.bash("grep -r fé wiki/conceitos")[0], {"busca-qmd.md"})

    def test_repetir_nao_vale_para_edicao(self):
        self.bash("grep -r fé wiki/conceitos")
        self.assertNotIn("busca-qmd.md", self.edit()[0])
        self.assertEqual(self.edit()[0], set())

    def test_busca_em_posicao_de_comando(self):
        for cmd in ("cd x && grep -r fé wiki/", "ls | xargs -0 grep fé wiki/",
                    "echo $(rg fé raw/kardec)", "find wiki -name '*.md'"):
            with self.subTest(cmd=cmd):
                self.assertEqual(self.bash(cmd, session=cmd)[0], {"busca-qmd.md"})

    def test_grep_fora_de_posicao_de_comando_nao_e_busca(self):
        for cmd in ('git commit -m "não usar grep em wiki/**"',
                    "python3 - <<'EOF'\nimport re\ngrep = 'wiki/**'\nEOF",
                    "cat > x.md <<EOF\ngrep -r fé wiki/\nEOF"):
            with self.subTest(cmd=cmd):
                self.assertEqual(self.bash(cmd, session=cmd), (set(), None))


if __name__ == "__main__":
    unittest.main()
