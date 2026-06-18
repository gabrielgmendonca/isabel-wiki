"""Testes do `scripts/insert_quote.py` — blockquote de citação literal do
Pentateuco, com o texto SEMPRE vindo da fonte (cite.py) e auto-verificado
verbatim. As expectativas são derivadas de `cite.literal_text` (não transcrição
manual), espelhando o contrato de `test_cite.py`; lê `raw/`, roda no CI.
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from cite import literal_text  # noqa: E402
from reverse_locus import word_coverage  # noqa: E402
from insert_quote import build_quote, _insert_into  # noqa: E402


def _inner(block: str) -> str:
    """Texto entre as aspas do blockquote `> "..." (SIGLA, ref)`."""
    body = block[len("> "):]
    body = body.rsplit(" (", 1)[0]          # tira a citação final
    return body.strip().strip("*").strip('"')


class BuildQuoteTests(unittest.TestCase):
    def test_block_shape_and_verbatim(self) -> None:
        block = build_quote("LE", "q. 358", None, False)
        self.assertTrue(block.startswith('> "'))
        self.assertTrue(block.endswith("(LE, q. 358)"))
        # O texto emitido é verbatim da fonte (cobertura ~1.0).
        cov = word_coverage(_inner(block), literal_text("LE", "q. 358"))
        self.assertGreaterEqual(cov, 0.95)

    def test_sentence_narrows_and_stays_verbatim(self) -> None:
        full = build_quote("ESE", "cap. XVII, item 3", None, False)
        narrowed = build_quote("ESE", "cap. XVII, item 3", "interroga", False)
        self.assertIn("interroga", narrowed.lower())
        # O recorte é menor que o corpo inteiro, mas ainda verbatim da fonte.
        self.assertLess(len(narrowed), len(full))
        cov = word_coverage(_inner(narrowed), literal_text("ESE", "cap. XVII, item 3"))
        self.assertGreaterEqual(cov, 0.95)

    def test_sentence_absent_aborts(self) -> None:
        # Não fabrica recorte: trecho ausente → SystemExit.
        with self.assertRaises(SystemExit):
            build_quote("ESE", "cap. XVII, item 3", "frase que nao consta em lugar nenhum", False)

    def test_italic_wraps(self) -> None:
        block = build_quote("LE", "q. 358", None, True)
        self.assertTrue(block.startswith('> *"'))
        self.assertIn('"*', block)

    def test_unknown_sigla_aborts(self) -> None:
        with self.assertRaises(SystemExit):
            build_quote("XX", "q. 1", None, False)

    def test_unresolved_locus_aborts(self) -> None:
        with self.assertRaises(SystemExit):
            build_quote("LE", "q. 99999", None, False)


class InsertIntoTests(unittest.TestCase):
    def test_insert_after_anchor(self) -> None:
        block = build_quote("LE", "q. 358", None, False)
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "pagina.md"
            p.write_text("# Título\n\n## Ensino de Kardec\n\nTexto.\n", encoding="utf-8")
            ok = _insert_into(p, "## Ensino de Kardec", block)
            self.assertTrue(ok)
            out = p.read_text(encoding="utf-8")
            self.assertIn(block, out)
            # Inserido DEPOIS da âncora.
            self.assertLess(out.index("## Ensino de Kardec"), out.index(block))

    def test_insert_anchor_absent(self) -> None:
        block = build_quote("LE", "q. 358", None, False)
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "pagina.md"
            p.write_text("# Só isto\n", encoding="utf-8")
            self.assertFalse(_insert_into(p, "## Inexistente", block))


if __name__ == "__main__":
    unittest.main()
