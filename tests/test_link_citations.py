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

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from link_citations import build_biblia_mapping, resolve_obra_slug, transform  # noqa: E402


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


def load_biblia() -> dict:
    """Carrega o mapping real (66 livros) — é dado canônico, não fixture."""
    return build_biblia_mapping(
        json.loads((ROOT / "data" / "biblia-livros.json").read_text(encoding="utf-8")),
    )


class LinkCitationsTests(unittest.TestCase):
    """Cada teste exercita um caso-canto isolado de transform()."""

    def setUp(self) -> None:
        self.mapping = make_mapping()
        self.revista = make_revista_mapping()
        self.biblia = load_biblia()
        self.obras = OBRAS

    def run_transform(self, text: str) -> str:
        return transform(text, self.mapping, self.obras, self.revista, self.biblia)

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
        text = "[[wiki/obras/o-livro-dos-espiritos|(LE, q. 990)]]"
        self.assertEqual(text, self.run_transform(text))

    # ─── Heading: safe zone (auto-link em heading não renderiza no Quartz) ────

    def test_citation_in_heading_is_left_intact(self) -> None:
        # Auto-link no H1-H6 polui a anchor (slug do heading absorve o link
        # inteiro) e cria link "decorativo" onde a intenção era título.
        text = "## (LE, q. 990) na ordem da criação"
        self.assertEqual(text, self.run_transform(text))

    def test_complementar_in_heading_is_left_intact(self) -> None:
        # Caso concreto que motivou a safe zone: H3 com (Autor, *Obra*, ref)
        # virava `### O sistema [[wiki/obras/...|...]]` (bonus-hora.md, 2026-05-22).
        text = "### O sistema (segundo a senhora Laura, *Nosso Lar*, cap. 22)"
        self.assertEqual(text, self.run_transform(text))

    def test_heading_safe_zone_does_not_leak_to_next_line(self) -> None:
        # MULTILINE + `[^\n]*` deve fechar o heading em \n — citação no corpo
        # da linha seguinte continua sendo linkada normalmente.
        out = self.run_transform("## Título\n(LE, q. 990) explica.")
        self.assertIn("[(LE, q. 990)](https://example.test/le/cap-3-vii)", out)
        self.assertTrue(out.startswith("## Título\n"))

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
        self.assertIn("[[wiki/obras/o-problema-do-ser-e-do-destino|", out)

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
        self.assertIn("[[wiki/obras/o-consolador|", out)

    def test_complementar_unknown_obra_left_intact(self) -> None:
        text = "(Hammed, *Obra Inexistente*, cap. I)"
        self.assertEqual(text, self.run_transform(text))

    def test_complementar_strips_article_for_slug_match(self) -> None:
        # "Nosso Lar" em wiki/obras/nosso-lar.md — slug exato.
        out = self.run_transform("(André Luiz / Chico Xavier, *Nosso Lar*, cap. 1)")
        self.assertIn("[[wiki/obras/nosso-lar|", out)

    def test_complementar_wikilink_uses_wiki_prefix(self) -> None:
        # Regressão (2026-05-22): o gerador produzia `[[obras/<slug>|...]]` sem o
        # prefixo `wiki/`, que não resolve no Quartz nem no `check_broken_links`
        # do lint (este só audita o source, e o link malformado nasce em CI).
        # Toda referência a obra dentro de wikilink deve trazer o prefixo `wiki/`.
        out = self.run_transform(
            "(André Luiz / Chico Xavier, *Nosso Lar*, cap. 1)",
        )
        self.assertIn("[[wiki/obras/nosso-lar|", out)
        self.assertNotIn("[[obras/", out)


    # ─── Bíblia ───────────────────────────────────────────────────────────────

    def test_nt_canonical_becomes_internal_wikilink(self) -> None:
        out = self.run_transform("Em (Mateus 5:3) Jesus abre o sermão.")
        self.assertIn("[[wiki/biblia/mateus/5#3|(Mateus 5:3)]]", out)

    def test_nt_abbreviation_resolves_to_same_slug(self) -> None:
        # Mt sem ponto, Mt. com ponto, S. Mateus — todas viram link interno mateus.
        out = self.run_transform("(Mt 5:3), (Mt. 5:3), (S. Mateus 5:3)")
        self.assertIn("[[wiki/biblia/mateus/5#3|(Mt 5:3)]]", out)
        self.assertIn("[[wiki/biblia/mateus/5#3|(Mt. 5:3)]]", out)
        self.assertIn("[[wiki/biblia/mateus/5#3|(S. Mateus 5:3)]]", out)

    def test_at_canonical_becomes_external_link(self) -> None:
        # Gênesis é AT → URL bibliaonline, no nível do capítulo.
        out = self.run_transform("Veja (Gênesis 1:1) sobre a criação.")
        self.assertIn("[(Gênesis 1:1)](https://www.bibliaonline.com.br/acf/gn/1)", out)

    def test_at_and_nt_in_same_line_resolve_independently(self) -> None:
        out = self.run_transform("Confronto: (Gênesis 1:1) vs (João 1:1).")
        self.assertIn("https://www.bibliaonline.com.br/acf/gn/1", out)
        self.assertIn("[[wiki/biblia/joao/1#1|(João 1:1)]]", out)

    def test_jo_unaccented_jo_does_not_match_job(self) -> None:
        # "Jó" (Job, AT) só casa com diacrítico — não pode pegar "Jo" abrev. João.
        # "Jo 1:1" (sem til) deveria ficar intocado (Jo não é variante NEM de Jó NEM
        # de João sozinha — Jo é abrev. de João só em "1 Jo"/"2 Jo"/"3 Jo").
        text = "Citação ambígua: (Jo 1:1) sem acento."
        out = self.run_transform(text)
        self.assertEqual(text, out)

    def test_numbered_book_with_and_without_space(self) -> None:
        # "1 Coríntios" e "1Co" devem resolver para o mesmo slug.
        out = self.run_transform("(1 Coríntios 13:1) e (1Co 13:4-7)")
        self.assertIn("[[wiki/biblia/1-corintios/13#1|(1 Coríntios 13:1)]]", out)
        self.assertIn("[[wiki/biblia/1-corintios/13#4|(1Co 13:4-7)]]", out)

    def test_verse_range_links_first_verse(self) -> None:
        # (Lc 24:13-35) → anchor #13; label preserva o range.
        out = self.run_transform("Estrada de Emaús em (Lc 24:13-35).")
        self.assertIn("[[wiki/biblia/lucas/24#13|(Lc 24:13-35)]]", out)

    def test_verse_range_with_en_dash(self) -> None:
        # Texto-fonte costuma usar en-dash em vez de hífen ASCII.
        out = self.run_transform("Cf. (Ef 5:22–24).")
        self.assertIn("[[wiki/biblia/efesios/5#22|(Ef 5:22–24)]]", out)

    def test_verse_list_links_first_verse(self) -> None:
        # (Mt 5:3,5,8) → anchor #3; label preserva a lista.
        out = self.run_transform("Bem-aventuranças (Mt 5:3,5,8).")
        self.assertIn("[[wiki/biblia/mateus/5#3|(Mt 5:3,5,8)]]", out)

    def test_unknown_book_left_intact(self) -> None:
        # Livro fora dos 66 — texto preservado.
        text = "Em (Macabeus 1:1) — fora do cânone."
        self.assertEqual(text, self.run_transform(text))

    def test_chapter_only_left_intact(self) -> None:
        # Sem versículo — `(Mateus 5)` não vira link (regex exige `:vers`).
        text = "Lemos (Mateus 5) hoje."
        self.assertEqual(text, self.run_transform(text))

    def test_biblia_in_fenced_code_left_intact(self) -> None:
        # Safe zone do dispatch protege fenced code.
        text = "```\nEx.: (Mateus 5:3)\n```"
        self.assertEqual(text, self.run_transform(text))

    def test_biblia_in_existing_wikilink_left_intact(self) -> None:
        text = "[[wiki/biblia/mateus/5|(Mateus 5:3)]]"
        self.assertEqual(text, self.run_transform(text))

    def test_biblia_in_heading_left_intact(self) -> None:
        text = "## (Mateus 5:3) — Bem-aventuranças"
        self.assertEqual(text, self.run_transform(text))

    def test_biblia_not_breaks_when_mapping_missing(self) -> None:
        # `transform` com biblia_mapping=None deve operar normalmente, sem linkar.
        text = "Em (Mateus 5:3) Jesus ensina."
        out = transform(text, self.mapping, self.obras, self.revista, None)
        self.assertEqual(text, out)


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


def make_deep_mapping() -> dict:
    """Mapping com question_urls (LE) e item_urls (demais) — exercita o deep-link
    por questão/item, e o fallback ao capítulo quando a URL granular falta."""
    base = "https://example.test"
    return {
        "_base": base,
        "books": {
            "LE": {
                "chapters": {"3:VII": "/le/cap-3-vii", "1:I": "/le/cap-1-i"},
                "questions": {"990": "3:VII", "150": "1:I"},
                # q. 990 tem URL própria; q. 150 não (só resolve via capítulo).
                "question_urls": {"990": "/le/q/990"},
            },
            "ESE": {
                "chapters": {"XVII": "/ese/cap-xvii"},
                "questions": {},
                # item reinicia por capítulo → chave "cap:item".
                "item_urls": {"XVII:4": "/ese/xvii/4"},
            },
            "LM": {
                "chapters": {"2:XX": "/lm/parte-2-cap-xx"},
                "questions": {},
                # item contínuo global → chave flat.
                "item_urls": {"230": "/lm/230"},
            },
            "Genese": {
                "chapters": {"XI": "/genese/cap-xi"},
                "questions": {},
                "item_urls": {"XI:13": "/genese/xi/13"},
            },
            "C&I": {
                "chapters": {"1:VI": "/cei/parte-1-cap-vi"},
                "questions": {},
                "item_urls": {"1:VI:3": "/cei/1/vi/3"},
            },
        },
    }


class DeepLinkTests(unittest.TestCase):
    """Preferência por URL de questão/item (B do roadmap §4); fallback ao capítulo."""

    def setUp(self) -> None:
        self.mapping = make_deep_mapping()

    def run_transform(self, text: str) -> str:
        return transform(text, self.mapping, set(), None, None)

    # ─── LE: questão ──────────────────────────────────────────────────────────

    def test_le_question_prefers_question_url(self) -> None:
        out = self.run_transform("Conforme (LE, q. 990).")
        self.assertIn("[(LE, q. 990)](https://example.test/le/q/990)", out)

    def test_le_question_falls_back_to_chapter(self) -> None:
        # q. 150 não tem question_url → resolve via questions→chapters.
        out = self.run_transform("Ver (LE, q. 150).")
        self.assertIn("[(LE, q. 150)](https://example.test/le/cap-1-i)", out)

    # ─── ESE/Gênese/C&I: item reinicia por capítulo (chave cap:item) ──────────

    def test_ese_item_prefers_item_url(self) -> None:
        out = self.run_transform("Ver (ESE, cap. XVII, item 4).")
        self.assertIn("[(ESE, cap. XVII, item 4)](https://example.test/ese/xvii/4)", out)

    def test_ese_item_missing_falls_back_to_chapter(self) -> None:
        # item 9 não está em item_urls → cai no capítulo.
        out = self.run_transform("Ver (ESE, cap. XVII, item 9).")
        self.assertIn("[(ESE, cap. XVII, item 9)](https://example.test/ese/cap-xvii)", out)

    def test_ese_chapter_only_unaffected(self) -> None:
        out = self.run_transform("Ver (ESE, cap. XVII).")
        self.assertIn("[(ESE, cap. XVII)](https://example.test/ese/cap-xvii)", out)

    def test_genese_item_no_part(self) -> None:
        out = self.run_transform("(Gênese, cap. XI, item 13)")
        self.assertIn("[(Gênese, cap. XI, item 13)](https://example.test/genese/xi/13)", out)

    def test_cei_item_with_part(self) -> None:
        out = self.run_transform("(C&I, 1ª parte, cap. VI, item 3)")
        self.assertIn("[(C&I, 1ª parte, cap. VI, item 3)](https://example.test/cei/1/vi/3)", out)

    # ─── LM: item contínuo global (chave flat), com ou sem capítulo ───────────

    def test_lm_item_with_chapter_uses_flat_key(self) -> None:
        out = self.run_transform("(LM, 2ª parte, cap. XX, item 230)")
        self.assertIn("[(LM, 2ª parte, cap. XX, item 230)](https://example.test/lm/230)", out)

    def test_lm_item_without_chapter(self) -> None:
        out = self.run_transform("(LM, item 230)")
        self.assertIn("[(LM, item 230)](https://example.test/lm/230)", out)


if __name__ == "__main__":
    unittest.main()
