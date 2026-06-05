"""Testes do check `check_literal_quote_exists` (lint_wiki.py).

Detecta aspa literal atribuída a Kardec que não existe no locus citado
(padrão "citação fabricada", ROADMAP §5). As aspas reais são construídas a
partir do texto-fonte via `cite.literal_text` para não enrijecer o teste com
transcrição manual; lê `raw/` (mesmo contrato do cite.py), roda no CI.
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "lint" / "scripts"))

from cite import literal_text  # noqa: E402
from lint_wiki import check_literal_quote_exists  # noqa: E402


def _words(sigla: str, ref: str) -> list[str]:
    """Palavras do texto literal de um locus (para montar aspas verbatim)."""
    text = literal_text(sigla, ref)
    assert text, f"locus de fixture não resolveu: ({sigla}, {ref})"
    return text.split()


class CheckLiteralQuoteExistsTests(unittest.TestCase):
    # Locus longo o bastante para fatiar fragmentos não-triviais.
    SIGLA, REF, CITE = "ESE", "cap. XVII, item 4", "(ESE, cap. XVII, item 4)"

    @classmethod
    def setUpClass(cls) -> None:
        cls.words = _words(cls.SIGLA, cls.REF)

    def run_check(self, body: str) -> list[dict]:
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "pagina.md"
            p.write_text(body, encoding="utf-8")
            return check_literal_quote_exists([p])["items"]

    def verbatim(self, lo: int, hi: int) -> str:
        return " ".join(self.words[lo:hi])

    # ─── aspa real → sem finding ──────────────────────────────────────────────

    def test_real_quote_not_flagged(self) -> None:
        quote = self.verbatim(3, 14)  # trecho verbatim, ≥5 palavras
        out = self.run_check(f'Kardec ensina "{quote}" {self.CITE}.')
        self.assertEqual(out, [])

    def test_elision_fragments_in_order_not_flagged(self) -> None:
        # Dois trechos verbatim não-adjacentes, ligados por [...] na ordem original.
        quote = f"{self.verbatim(3, 9)} [...] {self.verbatim(15, 21)}"
        out = self.run_check(f'Conforme "{quote}" {self.CITE}.')
        self.assertEqual(out, [])

    # ─── aspa fabricada → finding ─────────────────────────────────────────────

    def test_fabricated_quote_flagged(self) -> None:
        fake = "esta frase foi inteiramente inventada e nao consta da obra em lugar nenhum"
        out = self.run_check(f'Kardec teria dito "{fake}" {self.CITE}.')
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["citation"], self.CITE)
        self.assertLess(out[0]["coverage"], 0.5)

    def test_reordered_real_words_not_flagged(self) -> None:
        # Trechos verbatim reais, mas em ordem invertida: cobertura fuzzy ainda
        # alinha cada metade → não é fabricação (o conteúdo existe na fonte).
        quote = f"{self.verbatim(15, 21)} [...] {self.verbatim(3, 9)}"
        out = self.run_check(f'Conforme "{quote}" {self.CITE}.')
        self.assertEqual(out, [])

    # ─── pisos e skips ────────────────────────────────────────────────────────

    def test_short_quote_ignored(self) -> None:
        # Abaixo do piso (≥30 chars / ≥5 palavras) — não é checada, mesmo fabricada.
        out = self.run_check(f'A "frase curta" {self.CITE}.')
        self.assertEqual(out, [])

    def test_blockquote_ignored(self) -> None:
        fake = "esta frase foi inteiramente inventada e nao consta da obra em lugar nenhum"
        out = self.run_check(f'> Kardec teria dito "{fake}" {self.CITE}.')
        self.assertEqual(out, [])

    def test_inline_code_ignored(self) -> None:
        fake = "esta frase foi inteiramente inventada e nao consta da obra em lugar nenhum"
        out = self.run_check(f'Exemplo: `"{fake}" {self.CITE}`.')
        self.assertEqual(out, [])

    def test_invalid_locus_skipped(self) -> None:
        # Locus inexistente → literal_text=None → skip (check_citation_resolves cobre).
        fake = "esta frase foi inteiramente inventada e nao consta da obra em lugar nenhum"
        out = self.run_check(f'Kardec teria dito "{fake}" (LE, q. 99999).')
        self.assertEqual(out, [])

    def test_non_kardec_citation_ignored(self) -> None:
        # Aspa seguida de citação complementar (não-Pentateuco) → fora de escopo.
        fake = "esta frase foi inteiramente inventada e nao consta da obra em lugar nenhum"
        out = self.run_check(f'Texto "{fake}" (Léon Denis, *O Problema do Ser*, cap. IV).')
        self.assertEqual(out, [])


if __name__ == "__main__":
    unittest.main()
