"""Testes da camada estrutural do Pentateuco — kardec_structure.py.

Cobre o parser de .index.md, a normalização de sigla, a truncagem de
citações encadeadas e os 4 casos do resolve_locus. Fixtures inline; sem
I/O do raw/ (testes rápidos, rodam no CI antes do build).
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from kardec_structure import (  # noqa: E402
    NEXT_SIGLA_RE,
    Structure,
    _parse_index,
    _roman_to_int,
    resolve_locus,
)


def _make_index(content: str, tmp_path: Path) -> Path:
    p = tmp_path / "obra.index.md"
    p.write_text(content, encoding="utf-8")
    return p


def _ese_like() -> Structure:
    """ESE: sem partes, capítulos I-XXVIII, com Introdução."""
    return Structure(
        chapters={"I", "II", "III", "XVII", "XXVIII"},
        parts=set(),
        intro_items=set(),
        has_intro=True,
    )


def _ci_like() -> Structure:
    """C&I: 2 partes, sem Introdução kardequiana, capítulos por parte."""
    return Structure(
        chapters={"1:I", "1:VI", "1:XI", "2:I", "2:VIII"},
        parts={1, 2},
        intro_items=set(),
        has_intro=False,
    )


def _le_like() -> Structure:
    """LE: 4 partes, intro com 17 items, questões 1-1019."""
    return Structure(
        chapters={"1:I", "1:IV", "2:I", "3:VII", "4:II"},
        parts={1, 2, 3, 4},
        intro_items={"I", "IV", "XVII"},
        has_intro=True,
        questoes_range=(1, 1019),
    )


class RomanTests(unittest.TestCase):
    def test_basic_numerals(self) -> None:
        self.assertEqual(_roman_to_int("I"), 1)
        self.assertEqual(_roman_to_int("IV"), 4)
        self.assertEqual(_roman_to_int("IX"), 9)
        self.assertEqual(_roman_to_int("XXVIII"), 28)

    def test_invalid_returns_none(self) -> None:
        self.assertIsNone(_roman_to_int("XYZ"))


class ParseIndexTests(unittest.TestCase):
    """Cobertura do parser de .index.md: partes + capítulos + introdução."""

    def test_parses_chapters_without_parts(self) -> None:
        # ESE-like: só capítulos, sem ### parte.
        index = (Path(__file__).parent / "_tmp_ese.index.md")
        index.write_text(
            "### Introdução\n"
            "_Linhas 1–10_\n"
            "\n"
            "- **Capítulo I — Não vim destruir** (linhas 11–50)\n"
            "- **Capítulo II — Meu reino** (linhas 51–100)\n"
            "- **Capítulo XVII — Sede perfeitos** (linhas 200–300)\n",
            encoding="utf-8",
        )
        try:
            s = _parse_index(index)
            self.assertEqual(s.chapters, {"I", "II", "XVII"})
            self.assertEqual(s.parts, set())
            self.assertTrue(s.has_intro)
        finally:
            index.unlink()

    def test_parses_chapters_with_parts(self) -> None:
        # C&I-like: ### Primeira parte / ### Segunda parte.
        index = Path(__file__).parent / "_tmp_ci.index.md"
        index.write_text(
            "### Primeira parte — Doutrina\n"
            "_Linhas 1–10_\n"
            "\n"
            "- **Capítulo I — Futuro** (linhas 11–50)\n"
            "- **Capítulo VI — Penas eternas** (linhas 200–500)\n"
            "### Segunda parte — Exemplos\n"
            "_Linhas 600–600_\n"
            "\n"
            "- **Capítulo I — A passagem** (linhas 601–700)\n",
            encoding="utf-8",
        )
        try:
            s = _parse_index(index)
            self.assertEqual(s.chapters, {"1:I", "1:VI", "2:I"})
            self.assertEqual(s.parts, {1, 2})
            self.assertFalse(s.has_intro)
        finally:
            index.unlink()


class NextSiglaTruncationTests(unittest.TestCase):
    """A regex de corte da citação encadeada — coração da redução de FPs."""

    def test_truncates_at_semicolon_sigla(self) -> None:
        m = NEXT_SIGLA_RE.search(", q. 200; ESE, cap. XVII")
        self.assertIsNotNone(m)
        self.assertEqual("ESE", m.group(1))

    def test_truncates_at_comma_sigla(self) -> None:
        m = NEXT_SIGLA_RE.search(", cap. I, Gênese cap. II")
        # "Gênese" precedido de vírgula → casa.
        self.assertIsNotNone(m)
        self.assertEqual("Gênese", m.group(1))

    def test_truncates_at_cf_prefix(self) -> None:
        # Ponte editorial "; cf. C&I" — o `cf.` ficaria no meio sem o opcional.
        m = NEXT_SIGLA_RE.search("cap. XII; cf. C&I 1ª parte cap. III")
        self.assertIsNotNone(m)
        self.assertEqual("C&I", m.group(1))

    def test_truncates_at_wikilink_alias(self) -> None:
        # Padrão idiomático: sigla embrulhada em wikilink-com-alias.
        # "; [[wiki/obras/ceu-e-inferno|C&I]] 1ª parte cap. IX"
        m = NEXT_SIGLA_RE.search("q. 131; [[wiki/obras/ceu-e-inferno|C&I]] 1ª parte cap. IX")
        self.assertIsNotNone(m)
        self.assertEqual("C&I", m.group(1))

    def test_does_not_match_plain_word(self) -> None:
        # ", cap." sem sigla seguinte não dispara truncagem.
        self.assertIsNone(NEXT_SIGLA_RE.search("cap. III, item 4"))


class ResolveLocusTests(unittest.TestCase):
    """Os 4 casos do resolve_locus + invariantes (truncagem, sigla fora)."""

    # ─── Caso 3a: capítulo simples, obra sem partes ───────────────────────────

    def test_ese_chapter_exists(self) -> None:
        ok, _ = resolve_locus("ESE", ", cap. XVII, item 4", _ese_like())
        self.assertTrue(ok)

    def test_ese_chapter_missing_fails(self) -> None:
        ok, reason = resolve_locus("ESE", ", cap. XXX", _ese_like())
        self.assertFalse(ok)
        self.assertIn("XXX", reason)

    # ─── Caso 3b: capítulo com parte ──────────────────────────────────────────

    def test_ci_chapter_with_part_exists(self) -> None:
        ok, _ = resolve_locus("C&I", ", 1ª parte, cap. VI", _ci_like())
        self.assertTrue(ok)

    def test_ci_chapter_with_wrong_part_fails(self) -> None:
        ok, reason = resolve_locus("C&I", ", 2ª parte, cap. VI", _ci_like())
        self.assertFalse(ok)
        self.assertIn("2ª parte, cap. VI", reason)

    def test_ci_part_out_of_range_fails(self) -> None:
        ok, reason = resolve_locus("C&I", ", 3ª parte, cap. I", _ci_like())
        self.assertFalse(ok)
        self.assertIn("3ª parte", reason)

    # ─── Caso 4: questão de LE ────────────────────────────────────────────────

    def test_le_question_in_range(self) -> None:
        ok, _ = resolve_locus("LE", ", q. 990", _le_like())
        self.assertTrue(ok)

    def test_le_conclusion_question_in_range(self) -> None:
        # q. 1011-1019 → Conclusão; ficam dentro do range.
        ok, _ = resolve_locus("LE", ", q. 1019", _le_like())
        self.assertTrue(ok)

    def test_le_question_out_of_range_fails(self) -> None:
        ok, reason = resolve_locus("LE", ", q. 5000", _le_like())
        self.assertFalse(ok)
        self.assertIn("5000", reason)

    # ─── Casos 1+2: Introdução ────────────────────────────────────────────────

    def test_le_intro_item_exists(self) -> None:
        ok, _ = resolve_locus("LE", ", Introdução, item IV", _le_like())
        self.assertTrue(ok)

    def test_le_intro_item_missing_fails(self) -> None:
        ok, reason = resolve_locus("LE", ", Introdução, item XX", _le_like())
        self.assertFalse(ok)
        self.assertIn("XX", reason)

    def test_ci_intro_unavailable_fails(self) -> None:
        # C&I tem prefácio, não introdução kardequiana — citação inválida.
        ok, reason = resolve_locus("C&I", ", Introdução", _ci_like())
        self.assertFalse(ok)
        self.assertIn("Introdução", reason)

    # ─── Truncagem: rest poluído por sigla seguinte ───────────────────────────

    def test_chained_citation_truncates(self) -> None:
        # `(LE q. 200; ESE cap. XVII)` — cap. XVII pertence a ESE, não LE.
        # Sem truncagem, LE falharia procurando "cap. XVII" entre seus
        # capítulos `1:I..4:II`.
        ok, _ = resolve_locus("LE", ", q. 200; ESE cap. XVII", _le_like())
        self.assertTrue(ok)

    def test_chained_with_cf_prefix(self) -> None:
        # Ponte "; cf. C&I" também deve cortar — caso real do `apocalipse.md`.
        ok, _ = resolve_locus(
            "Gênese", ", cap. XII; cf. C&I 1ª parte cap. III",
            Structure(chapters={"I", "XII", "XVIII"}, has_intro=False),
        )
        self.assertTrue(ok)

    # ─── Não-falsificação: padrão não-reconhecido devolve True ────────────────

    def test_unrecognized_pattern_returns_true(self) -> None:
        # Ano de publicação — check_citation_format cuida da forma; aqui passa.
        ok, _ = resolve_locus("LE", ", 1857", _le_like())
        self.assertTrue(ok)


if __name__ == "__main__":
    unittest.main()
