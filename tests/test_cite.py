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


class CiteConclusaoNumeracaoDuplaTests(unittest.TestCase):
    """q. 1012–1019 do LE usam numeração dupla 'Kardec [sequencial].' no raw
    (ex.: '1015 [1014].') porque Kardec saltou o nº 1011. cite.py deve
    resolvê-las pelo nº de Kardec e explicar a ausência da 1011."""

    def test_q1015_resolve_pela_numeracao_de_kardec(self):
        code, out, _ = _run(["LE", "q. 1015"])
        self.assertEqual(code, 0)
        self.assertIn("(LE, q. 1015)", out)
        self.assertIn("alma a penar", out)

    def test_q1019_resolve_reinado_do_bem(self):
        code, out, _ = _run(["LE", "q. 1019"])
        self.assertEqual(code, 0)
        self.assertIn("(LE, q. 1019)", out)
        self.assertIn("reinado do bem", out)

    def test_q1011_inexistente_explica_o_salto(self):
        code, _, err = _run(["LE", "q. 1011"])
        self.assertNotEqual(code, 0)
        self.assertIn("saltou", err)


if __name__ == "__main__":
    unittest.main()
