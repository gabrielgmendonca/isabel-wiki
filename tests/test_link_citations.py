"""Testes de regressão para scripts/link_citations.py.

Casos-canto (roadmap §5):
- citação dentro de code block fenced/inline
- citação em link Markdown ou wikilink já existente
- sigla ambígua (Léon Denis não vira LE Kardec)
- citação composta com range de questões (usa primeira)
- citação em heading
- Revista Espírita: mês casado vs fallback de ano
- Complementar: obra com slug e sem slug
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from link_citations import resolve_obra_slug, transform  # noqa: E402


def make_mapping() -> dict:
    """Mapping mínimo: cobre cada ramo de kardec_url()."""
    base = "https://example.test"
    return {
        "_base": base,
        "books": {
            "LE": {
                "intro": "/le/intro",
                "intro_items": {"IV": "/le/intro/iv"},
                "chapters": {
                    "1:I": "/le/cap-1-i",
                    "3:VII": "/le/cap-3-vii",
                },
                "questions": {
                    "150": "1:I",
                    "151": "1:I",
                    "990": "3:VII",
                },
            },
            "ESE": {
                "chapters": {"XVII": "/ese/cap-xvii"},
                "questions": {},
            },
            "C&I": {
                "chapters": {"1:VI": "/cei/parte-1-cap-vi"},
                "questions": {},
            },
            "Genese": {
                "chapters": {"XI": "/genese/cap-xi"},
                "questions": {},
            },
            "LM": {"chapters": {}, "questions": {}},
        },
    }


def make_revista_mapping() -> dict:
    return {
        "anos": {
            "1858": {
                "url": "https://example.test/re/1858",
                "artigos": [
                    {"mes": "janeiro", "url": "https://example.test/re/1858/jan/art1"},
                    {"mes": "janeiro", "url": "https://example.test/re/1858/jan/art2"},
                    {"mes": "marco", "url": "https://example.test/re/1858/mar/art1"},
                ],
            },
        },
    }


OBRAS = {"o-consolador", "nosso-lar", "o-problema-do-ser-e-do-destino"}


class LinkCitationsTests(unittest.TestCase):
    """Cada teste exercita um caso-canto isolado de transform()."""

    def setUp(self) -> None:
        self.mapping = make_mapping()
        self.revista = make_revista_mapping()
        self.obras = OBRAS

    def run_transform(self, text: str) -> str:
        return transform(text, self.mapping, self.obras, self.revista)

    # ─── Kardec: capítulo / questão / introdução ──────────────────────────────

    def test_kardec_chapter_link(self) -> None:
        out = self.run_transform("Ver (ESE, cap. XVII, item 4) sobre caridade.")
        self.assertIn("[(ESE, cap. XVII, item 4)](https://example.test/ese/cap-xvii)", out)

    def test_kardec_question_link(self) -> None:
        out = self.run_transform("Conforme (LE, q. 990).")
        self.assertIn("[(LE, q. 990)](https://example.test/le/cap-3-vii)", out)

    def test_kardec_question_range_uses_first(self) -> None:
        # Citação composta: (LE, q. 150-152) deve usar 150 → cap 1:I.
        out = self.run_transform("Bloco (LE, q. 150-152) das causas primárias.")
        self.assertIn("[(LE, q. 150-152)](https://example.test/le/cap-1-i)", out)

    def test_kardec_intro_with_item(self) -> None:
        out = self.run_transform("(LE, Introdução, item IV) trata do método.")
        self.assertIn("[(LE, Introdução, item IV)](https://example.test/le/intro/iv)", out)

    def test_kardec_intro_without_item(self) -> None:
        out = self.run_transform("(LE, Introdução) — método espírita.")
        self.assertIn("[(LE, Introdução)](https://example.test/le/intro)", out)

    def test_kardec_chapter_with_part(self) -> None:
        out = self.run_transform("(C&I, 1ª parte, cap. VI) sobre anjos.")
        self.assertIn("[(C&I, 1ª parte, cap. VI)](https://example.test/cei/parte-1-cap-vi)", out)

    def test_kardec_genese_normalizes_sigla(self) -> None:
        # "Gênese" no texto deve resolver via SIGLA_NORM → "Genese".
        out = self.run_transform("(Gênese, cap. XI, item 13)")
        self.assertIn("[(Gênese, cap. XI, item 13)](https://example.test/genese/cap-xi)", out)

    def test_kardec_unknown_chapter_returns_unlinked(self) -> None:
        # cap. XXIII não existe na fixture: regex casa, mas sem URL → texto intacto.
        text = "(ESE, cap. XXIII)"
        out = self.run_transform(text)
        self.assertEqual(text, out)

    # ─── Safe zones: nada dentro de code/link/wikilink é tocado ───────────────

    def test_inline_code_left_intact(self) -> None:
        text = "Veja `(LE, q. 990)` no fonte."
        self.assertEqual(text, self.run_transform(text))

    def test_fenced_code_left_intact(self) -> None:
        text = "```\nReferência: (LE, q. 990)\n```"
        self.assertEqual(text, self.run_transform(text))

    def test_existing_markdown_link_left_intact(self) -> None:
        # Já linkado: não pode aninhar [(...)]( ... ).
        text = "[(LE, q. 990)](https://outro.example/le)"
        self.assertEqual(text, self.run_transform(text))

    def test_inside_wikilink_left_intact(self) -> None:
        text = "[[obras/o-livro-dos-espiritos|(LE, q. 990)]]"
        self.assertEqual(text, self.run_transform(text))

    # ─── Heading: linkagem normal (parser ignora '#') ─────────────────────────

    def test_citation_in_heading_is_linked(self) -> None:
        out = self.run_transform("## (LE, q. 990) na ordem da criação")
        self.assertIn("[(LE, q. 990)](https://example.test/le/cap-3-vii)", out)
        self.assertTrue(out.startswith("## "))

    # ─── Sigla ambígua: Léon Denis não vira link Kardec ───────────────────────

    def test_leon_denis_does_not_match_le(self) -> None:
        # "Léon Denis" não está envolto em "(LE" — o regex exige boundary "(LE\b".
        text = "Léon Denis tratou disso em obra própria."
        self.assertEqual(text, self.run_transform(text))

    def test_complementar_with_le_in_author_name_does_not_kardec(self) -> None:
        # (Léon Denis, *Obra*, ...) — autor inicia com "L" mas não casa "(LE\b".
        text = "(Léon Denis, *O Problema do Ser e do Destino*, cap. IV)"
        out = self.run_transform(text)
        # Não deve virar link Kardec.
        self.assertNotIn("kardecpedia", out.lower())
        self.assertNotIn("example.test/le/", out)
        # Deve virar wikilink complementar (obra existe na fixture).
        self.assertIn("[[obras/o-problema-do-ser-e-do-destino|", out)

    # ─── Revista Espírita ─────────────────────────────────────────────────────

    def test_revista_month_match(self) -> None:
        out = self.run_transform("Conforme (RE, jan/1858, p. 12).")
        self.assertIn(
            "[(RE, jan/1858, p. 12)](https://example.test/re/1858/jan/art1)", out,
        )

    def test_revista_month_unmatched_falls_back_to_year(self) -> None:
        # Fevereiro de 1858 não tem artigo na fixture → cai pro índice do ano.
        out = self.run_transform("(RE, fevereiro/1858)")
        self.assertIn("[(RE, fevereiro/1858)](https://example.test/re/1858)", out)

    def test_revista_unknown_year_left_intact(self) -> None:
        text = "(RE, jan/1900)"
        self.assertEqual(text, self.run_transform(text))

    def test_revista_with_de_separator(self) -> None:
        # (RE, março de 1858) — separador alternativo " de ".
        out = self.run_transform("(RE, março de 1858)")
        self.assertIn("[(RE, março de 1858)](https://example.test/re/1858/mar/art1)", out)

    # ─── Complementares ───────────────────────────────────────────────────────

    def test_complementar_known_obra_becomes_wikilink(self) -> None:
        out = self.run_transform("(Emmanuel / Chico Xavier, *O Consolador*, q. 123)")
        self.assertIn("[[obras/o-consolador|", out)

    def test_complementar_unknown_obra_left_intact(self) -> None:
        text = "(Hammed, *Obra Inexistente*, cap. I)"
        self.assertEqual(text, self.run_transform(text))

    def test_complementar_strips_article_for_slug_match(self) -> None:
        # "Nosso Lar" em wiki/obras/nosso-lar.md — slug exato.
        out = self.run_transform("(André Luiz / Chico Xavier, *Nosso Lar*, cap. 1)")
        self.assertIn("[[obras/nosso-lar|", out)


class ResolveObraSlugTests(unittest.TestCase):
    """resolve_obra_slug: estratégias de match isoladas."""

    def setUp(self) -> None:
        self.index = {"o-consolador", "nosso-lar", "consolador-extra"}

    def test_exact_slug(self) -> None:
        self.assertEqual(resolve_obra_slug("Nosso Lar", self.index), "nosso-lar")

    def test_strips_article(self) -> None:
        self.assertEqual(
            resolve_obra_slug("O Consolador", self.index), "o-consolador",
        )

    def test_no_match_returns_none(self) -> None:
        self.assertIsNone(resolve_obra_slug("Obra Inexistente", self.index))


if __name__ == "__main__":
    unittest.main()
