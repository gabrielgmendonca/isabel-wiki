"""Testes do check `check_slide_overflow` (lint_wiki.py).

Estima se um slide Marp estoura a caixa de conteúdo de 1080 x 560 px do tema
isabel — o problema que custou uma palestra para ser descoberto (ROADMAP §7).

O modelo é uma aproximação, então o que estes testes travam é a **calibragem**:
as alturas e contagens de linha aqui vieram de medir o PDF renderizado de
`slides/themes/preview.md`, não de rodar o próprio modelo. Se alguém mexer nas
constantes de geometria, o desvio aparece aqui em vez de aparecer no projetor.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "lint" / "scripts"))

from lint_wiki import (  # noqa: E402
    _CONTENT_H,
    _wrapped_lines,
    check_slide_overflow,
    estimate_slide_height,
    split_slides,
)

PREVIEW = ROOT / "slides" / "themes" / "preview.md"

# Contagem de linhas observada no render do preview. (texto, px, largura, serif)
LINHAS_OBSERVADAS = [
    ('"Atire a primeira pedra": a indulgência não é fraqueza',
     56, 1280 * 0.57 - 200, False, 4),
    ('Se a misericórdia é "o esquecimento e o perdão das ofensas", sem limites, '
     'não seria pregar que tudo se releva — que o indulgente é o frouxo que tudo '
     'desculpa?', 64, 1080 * 0.9, False, 6),
    ("Severos com os outros, indulgentes conosco: o que muda ao inverter a direção?",
     64, 1080 * 0.9, False, 3),
    ('"Atire a primeira pedra" não relativiza o erro — faz da indulgência um '
     "dever de quem também precisa dela (cap. X, item 13).", 30, 1010, False, 2),
    ("Não é laxismo: repreender com moderação e fim útil continua dever "
     "(item 19); o perdão dos lábios que guarda rancor não conta diante de "
     "Deus (item 15).", 30, 1010, False, 3),
    ("A indulgência não vê os defeitos de outrem, ou, se os vê, evita falar "
     "deles, divulgá-los. (...) Sede, pois, severos para convosco, indulgentes "
     "para com os outros. (...) Sede indulgentes, meus amigos, porquanto a "
     "indulgência atrai, acalma, ergue, ao passo que o rigor desanima, afasta "
     "e irrita.", 34, 1080 - 52, True, 4),
    ("Benevolência para com todos, indulgência para as imperfeições dos "
     "outros, perdão das ofensas.", 34, 1080 - 52, True, 2),
]

# Altura de conteúdo medida no PDF, por número de slide do preview.
ALTURA_MEDIDA = {9: 371, 10: 690, 11: 520}


class TestQuebraDeLinha(unittest.TestCase):
    def test_reproduz_o_render(self):
        for texto, size, width, serif, esperado in LINHAS_OBSERVADAS:
            with self.subTest(texto=texto[:40]):
                self.assertEqual(
                    _wrapped_lines(texto, size, width, serif=serif), esperado)

    def test_markdown_nao_conta_como_texto(self):
        puro = "Misericórdia é o coração que se compadece e perdoa"
        marcado = "**Misericórdia** é o *coração* que se compadece e perdoa"
        self.assertEqual(_wrapped_lines(marcado, 30, 300),
                         _wrapped_lines(puro, 30, 300))

    def test_split_background_estreita_a_coluna(self):
        texto = '"Atire a primeira pedra": a indulgência não é fraqueza'
        self.assertGreater(_wrapped_lines(texto, 56, 1280 * 0.57 - 200),
                           _wrapped_lines(texto, 56, 1080))


class TestAlturaEstimada(unittest.TestCase):
    """Confere a estimativa contra a altura medida no PDF (tolerância 8%)."""

    def setUp(self):
        if not PREVIEW.exists():
            self.skipTest("slides/themes/preview.md ausente")
        self.slides = split_slides(PREVIEW.read_text(encoding="utf-8"))

    def test_bate_com_o_medido(self):
        for numero, medido in ALTURA_MEDIDA.items():
            with self.subTest(slide=numero):
                altura, _ = estimate_slide_height(self.slides[numero - 1])
                self.assertLess(
                    abs(altura - medido) / medido, 0.08,
                    f"slide {numero}: estimado {altura:.0f}px, medido {medido}px")

    def test_cinco_bullets_estouram_e_tres_nao(self):
        """A invariante que originou o check (ROADMAP §7)."""
        tres, _ = estimate_slide_height(self.slides[8])
        cinco, _ = estimate_slide_height(self.slides[9])
        self.assertLessEqual(tres, _CONTENT_H)
        self.assertGreater(cinco, _CONTENT_H)

    def test_classes_sao_reconhecidas(self):
        classes = [estimate_slide_height(s)[1] for s in self.slides]
        for esperada in ("pergunta", "quote", "section"):
            self.assertIn(esperada, classes)


class TestClasseDeSlide(unittest.TestCase):
    def test_underscore_vale_so_no_slide(self):
        altura, klass = estimate_slide_height(
            "<!-- _class: quote -->\n\n> uma citação", inherited_class="default")
        self.assertEqual(klass, "quote")

    def test_classe_herdada_se_aplica(self):
        _, klass = estimate_slide_height("> uma citação", inherited_class="quote")
        self.assertEqual(klass, "quote")

    def test_classe_desconhecida_cai_no_default(self):
        _, klass = estimate_slide_height("<!-- _class: inexistente -->\n\ntexto")
        self.assertEqual(klass, "default")


class TestSplitSlides(unittest.TestCase):
    def test_descarta_front_matter(self):
        deck = "---\nmarp: true\ntheme: isabel\n---\n\n# Um\n\n---\n\n# Dois\n"
        slides = split_slides(deck)
        self.assertEqual(len(slides), 2)
        self.assertIn("# Um", slides[0])
        self.assertNotIn("marp", slides[0])


class TestCheck(unittest.TestCase):
    def test_severidade_info(self):
        self.assertEqual(check_slide_overflow([])["severity"], "info")

    def test_itens_apontam_deck_e_slide(self):
        for item in check_slide_overflow([])["items"]:
            self.assertTrue(item["path"].startswith("slides/"))
            self.assertGreaterEqual(item["slide"], 1)
            self.assertGreater(item["altura_estimada_px"], item["limite_px"])

    def test_opt_out_silencia_o_slide(self):
        """O slide de calibragem do preview transborda de propósito."""
        if not PREVIEW.exists():
            self.skipTest("slides/themes/preview.md ausente")
        slides = split_slides(PREVIEW.read_text(encoding="utf-8"))
        calibragem = slides[9]
        self.assertIn("lint: overflow-esperado", calibragem)
        self.assertGreater(estimate_slide_height(calibragem)[0], _CONTENT_H)
        flagrados = [
            it for it in check_slide_overflow([])["items"]
            if it["path"].endswith("themes/preview.md") and it["slide"] == 10
        ]
        self.assertEqual(flagrados, [])


if __name__ == "__main__":
    unittest.main()
