"""Testes da camada 0 do `/palestra` — `seed_digest.py` e `repertorio.py`.

Cada caso aqui trava uma regressão observada no run de 2026-09-12:

- o digest por locus **apagou a moldura musical** da semente (a seção "Uso em
  palestra" não tem citação em quase nenhuma linha) e o dossiê saiu sem ela;
- o extrator de `.pptx` juntava os runs com espaço, e "Szymel Slizgol" —
  quebrado em dois runs pelo PowerPoint — não casava com nada, então o
  repertório não avisava que o caso já fora contado;
- sem filtro, "Emmanuel" e "Jesus" entravam como "casos já contados" em todo
  deck, afogando o sinal.
"""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / ".claude" / "skills" / "palestra" / "scripts"


def carregar(nome):
    spec = importlib.util.spec_from_file_location(nome, SCRIPTS / f"{nome}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nome] = mod
    spec.loader.exec_module(mod)
    return mod


seed_digest = carregar("seed_digest")
repertorio = carregar("repertorio")

SEMENTE = """---
tipo: aprofundamento
tags: [testemunho]
---

# Como testemunhar

Parágrafo de prosa comum, sem citação nenhuma, que o digest deve descartar.

> "uma virtude negativa não basta" (ESE, cap. XV, item 10)

## Uso em palestra

0. **Ambientação**. "Além das Janelas", de Ariovaldo Filho. Entra antes da parte
   doutrinária e assenta a plateia.
1. **Abertura** — a promessa. Entra-se pelo dom recebido, não pela cobrança.

## Conceitos relacionados

- Mais prosa sem locus, que o digest descarta.
"""


class TestSeedDigest(unittest.TestCase):
    def test_pagina_curta_passa_inteira_sem_digest(self):
        saida, truncado = seed_digest.preparar(SEMENTE, teto=12000)
        self.assertFalse(truncado)
        self.assertEqual(saida, SEMENTE)

    def test_pagina_grande_vira_digest(self):
        saida, truncado = seed_digest.preparar(SEMENTE, teto=10)
        self.assertTrue(truncado)
        self.assertLess(len(saida), len(SEMENTE))

    def test_preserva_secao_de_roteiro_inteira(self):
        d = seed_digest.digest(SEMENTE)
        self.assertIn("Além das Janelas", d)
        self.assertIn("Ambientação", d)
        self.assertIn("a promessa", d)

    def test_mantem_frontmatter_headers_e_locus(self):
        d = seed_digest.digest(SEMENTE)
        self.assertIn("tipo: aprofundamento", d)
        self.assertIn("## Conceitos relacionados", d)
        self.assertIn("(ESE, cap. XV, item 10)", d)

    def test_descarta_prosa_sem_locus_fora_das_secoes_preservadas(self):
        d = seed_digest.digest(SEMENTE)
        self.assertNotIn("Parágrafo de prosa comum", d)
        self.assertNotIn("Mais prosa sem locus", d)


def pptx_falso(caminho, paragrafos):
    """Gera um .pptx mínimo com cada parágrafo quebrado em DOIS runs `<a:t>`,
    como o PowerPoint faz quando há mudança de formatação no meio do nome."""
    with zipfile.ZipFile(caminho, "w") as z:
        corpo = ""
        for texto in paragrafos:
            meio = len(texto) // 2
            corpo += f"<a:p><a:r><a:t>{texto[:meio]}</a:t></a:r><a:r><a:t>{texto[meio:]}</a:t></a:r></a:p>"
        z.writestr("ppt/slides/slide1.xml", f"<p:sld><p:cSld>{corpo}</p:cSld></p:sld>")


class TestRepertorio(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.raiz = Path(self.tmp.name)
        wiki = self.raiz / "wiki"
        (wiki / "personalidades").mkdir(parents=True)
        (wiki / "conceitos").mkdir(parents=True)
        for slug, h1, tags in [
            ("szymel-slizgol", "Szymel Slizgol", "[ceu-e-inferno, autor/kardec]"),
            ("rainha-de-oude", "A rainha de Oude", "[ceu-e-inferno]"),
            ("emmanuel", "Emmanuel", "[autor/emmanuel]"),
            ("o-castigo", "O Castigo", "[ceu-e-inferno]"),
        ]:
            (wiki / "personalidades" / f"{slug}.md").write_text(
                f"---\ntipo: personalidade\ntags: {tags}\n---\n\n# {h1}\n", encoding="utf-8")
        (wiki / "conceitos" / "parabola-dos-dois-filhos.md").write_text(
            "---\ntipo: conceito\ntags: [parabola]\n---\n\n# Parábola dos dois filhos\n", encoding="utf-8")
        self.decks = self.raiz / "raw" / "palestras" / "gabriel-mendonca"
        self.decks.mkdir(parents=True)

    def tearDown(self):
        self.tmp.cleanup()

    def test_nome_quebrado_em_dois_runs_do_pptx_ainda_casa(self):
        pptx_falso(self.decks / "orgulho-e-humildade.pptx", ["Szymel Slizgol", "A RAINHA DE OUDE"])
        texto = repertorio.texto_pptx(self.decks / "orgulho-e-humildade.pptx")
        self.assertIn("Szymel Slizgol", texto)

    def test_autor_nao_conta_como_caso(self):
        reg = repertorio.termos(self.raiz)
        self.assertIn("Szymel Slizgol", reg)
        self.assertNotIn("Emmanuel", reg)

    def test_parabola_entra_no_registro(self):
        self.assertIn("Parábola dos dois filhos", repertorio.termos(self.raiz))


DECK = """---
marp: true
header: 'Como Testemunhar'
---

# Como Testemunhar

---

<!-- _class: pergunta -->

## Bastará que o homem não pratique o mal?

*Estuda a Doutrina há anos.*

---

<!-- _class: section -->

## Uma virtude negativa não basta

---

<!-- _class: quote -->

> "uma virtude negativa não basta" (ESE, cap. XV, item 10)

---

<!-- _class: pergunta -->

## Bastará que o homem não pratique o mal?
"""


class TestAngulos(unittest.TestCase):
    """Os ângulos são a parte da antiga lente de palestras que é decidível por
    código: o que ele já perguntou e como já cortou o tema em partes."""

    def test_deck_marp_da_titulo_partes_e_perguntas(self):
        a = repertorio.angulos_deck(DECK)
        self.assertEqual(a["titulo"], "Como Testemunhar")
        self.assertEqual(a["partes"], ["Uma virtude negativa não basta"])
        self.assertEqual(a["perguntas"], ["Bastará que o homem não pratique o mal?"])

    def test_nao_confunde_citacao_com_pergunta_nem_parte(self):
        a = repertorio.angulos_deck(DECK)
        self.assertNotIn("Como Testemunhar", a["partes"])
        self.assertFalse([p for p in a["perguntas"] if "virtude negativa" in p])

    def test_pergunta_literal_do_pentateuco_nao_e_angulo_autoral(self):
        a = repertorio.angulos_apresentado(
            "675. Por trabalho só se devem entender as ocupações materiais?\n"
            "— P. Sois feliz?\n"
            "Por que nosso anjo da guarda se esconde?\n")
        self.assertEqual(a["perguntas"], ["Por que nosso anjo da guarda se esconde?"])


if __name__ == "__main__":
    unittest.main()
