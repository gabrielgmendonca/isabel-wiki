"""Testes do check `check_kardequiano` (lint_wiki.py).

Detecta formas adjetivais proibidas derivadas de "Kardec" — "kardequiano/a",
"kardeciano/a" — que violam a regra dura do usuário (ROADMAP §13). As formas
vêm do registro data-driven `data/terminologia.json` ('derivados-de-kardec');
"kardecista" (movimento) é válido e NÃO deve ser sinalizado.
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "lint" / "scripts"))

from lint_wiki import check_kardequiano  # noqa: E402


class CheckKardequianoTests(unittest.TestCase):
    def run_check(self, body: str) -> list[dict]:
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "pagina.md"
            p.write_text(body, encoding="utf-8")
            return check_kardequiano([p])["items"]

    # ─── formas proibidas → finding ───────────────────────────────────────────

    def test_kardequiana_flagged(self) -> None:
        out = self.run_check("A leitura kardequiana do texto é clara.")
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["forma"].lower(), "kardequiana")
        self.assertEqual(out[0]["sugestao"], "de Kardec")
        self.assertEqual(out[0]["line"], 1)

    def test_kardequiano_flagged(self) -> None:
        out = self.run_check("O Pentateuco kardequiano é a base.")
        self.assertEqual(len(out), 1)

    def test_kardeciano_variant_flagged(self) -> None:
        out = self.run_check("Em registro kardeciano isso muda.")
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["forma"].lower(), "kardeciano")

    def test_case_insensitive(self) -> None:
        out = self.run_check("Kardequiana, com inicial maiúscula, ainda conta.")
        self.assertEqual(len(out), 1)

    def test_line_number_reported(self) -> None:
        out = self.run_check("linha um\nlinha dois kardequiana\nlinha tres")
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["line"], 2)

    def test_multiple_occurrences_same_line(self) -> None:
        out = self.run_check("kardequiana e kardequiano na mesma linha")
        self.assertEqual(len(out), 2)

    # ─── formas válidas → sem finding ─────────────────────────────────────────

    def test_kardecista_not_flagged(self) -> None:
        # "kardecista" é VÁLIDO (movimento espírita) — nunca sinalizar.
        out = self.run_check("O movimento kardecista cresceu muito.")
        self.assertEqual(out, [])

    def test_de_kardec_not_flagged(self) -> None:
        out = self.run_check("A leitura de Kardec do texto é clara.")
        self.assertEqual(out, [])

    def test_word_boundary(self) -> None:
        # Substring dentro de outra palavra não casa (\b protege).
        out = self.run_check("antikardequianamente não é uma palavra alvo isolada")
        # "kardequiana" está embutida sem fronteira à esquerda → não casa.
        self.assertEqual(out, [])

    # ─── skips ────────────────────────────────────────────────────────────────

    def test_blockquote_ignored(self) -> None:
        # Citação literal de fonte secundária — não reescrever aspas.
        out = self.run_check("> A leitura kardequiana, segundo o autor X.")
        self.assertEqual(out, [])

    def test_inline_code_ignored(self) -> None:
        out = self.run_check("Exemplo de termo: `kardequiana`.")
        self.assertEqual(out, [])

    def test_wikilink_ignored(self) -> None:
        out = self.run_check("Ver [[wiki/sinteses/leitura-kardequiana|leitura kardequiana]].")
        self.assertEqual(out, [])

    def test_corpus_tipo_skipped(self) -> None:
        # Páginas de corpus verbatim (Pentateuco/Bíblia) não são reescritas.
        body = "---\ntipo: capitulo-pentateuco\n---\nTexto kardequiana verbatim."
        out = self.run_check(body)
        self.assertEqual(out, [])

    def test_frontmatter_not_scanned(self) -> None:
        # Frontmatter é removido antes da varredura.
        body = "---\ntipo: conceito\ntitulo: leitura kardequiana\n---\nCorpo limpo."
        out = self.run_check(body)
        self.assertEqual(out, [])


if __name__ == "__main__":
    unittest.main()
