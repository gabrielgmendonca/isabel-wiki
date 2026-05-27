"""Testes leves de scripts/cite.py.

Usa o LE real em `raw/kardec/pentateuco/livro-dos-espiritos.md` como fixture
estável (o cânon não muda). Smoke + erros previsíveis; cobertura exaustiva
do parser fica para os testes de kardec_structure.
"""
from __future__ import annotations

import io
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from cite import main  # noqa: E402


def _run(args: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = main(args)
    return code, out.getvalue(), err.getvalue()


class CiteSmokeTests(unittest.TestCase):
    def test_le_q1_contem_que_e_deus(self):
        code, out, _ = _run(["LE", "q. 1"])
        self.assertEqual(code, 0)
        self.assertIn("Que é Deus?", out)
        self.assertIn("(LE, q. 1)", out)

    def test_locus_invalido_aborta_com_codigo_nao_zero(self):
        code, _, err = _run(["LE", "q. 99999"])
        self.assertNotEqual(code, 0)
        self.assertIn("fora do range", err)

    def test_sigla_desconhecida_aborta(self):
        code, _, err = _run(["XYZ", "q. 1"])
        self.assertNotEqual(code, 0)
        self.assertIn("sigla desconhecida", err)


if __name__ == "__main__":
    unittest.main()
