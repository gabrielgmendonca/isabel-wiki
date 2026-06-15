"""Testes do índice reverso de locus (scripts/reverse_locus.py).

Dada uma aspa, acha em que questão/item do Pentateuco ela mora — base da
detecção determinística de aspa mal-atribuída (classe 3) e fabricada (classe 2)
do ROADMAP §12. Lê `raw/` (mesmo contrato do cite.py), roda no CI.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from reverse_locus import (  # noqa: E402
    build_index,
    cited_covers,
    classify,
    find_loci,
    word_coverage,
)

# Aspa verbatim distintiva do ESE cap. X, item 13 (a indulgência) — conferida
# contra o raw. Distintiva o bastante para não recorrer em outros loci.
INDULGENCIA = "Atire-lhe a primeira pedra aquele que estiver isento de pecado"


class FindLociTests(unittest.TestCase):
    def test_verbatim_quote_ranks_its_locus_first(self):
        ref, cov, _ = find_loci("ESE", INDULGENCIA, top=1)[0]
        self.assertEqual(ref, "cap. X, item 13")
        self.assertGreaterEqual(cov, 0.95)

    def test_accepts_genese_sigla_spelling(self):
        # _norm_sigla normaliza "Gênese"/"Genese"; não pode devolver vazio.
        self.assertTrue(find_loci("Gênese", "Deus é a inteligência suprema", top=1))

    def test_unknown_sigla_returns_empty(self):
        self.assertEqual(find_loci("RE", "qualquer coisa"), [])


class ClassifyTests(unittest.TestCase):
    def test_misattributed_suggests_real_locus(self):
        # Aspa de ESE cap. X item 13, citada (errado) como cap. XVII item 3.
        v = classify("ESE", "cap. XVII, item 3", INDULGENCIA, cited_coverage=0.0)
        self.assertEqual(v.label, "misattributed")
        self.assertEqual(v.suggested_ref, "cap. X, item 13")
        self.assertGreaterEqual(v.suggested_coverage, 0.95)

    def test_supported_when_best_is_cited(self):
        # Mesmo locus citado certo: best == citado, cobertura ~verbatim →
        # supported (suprime FP de extração); cited_coverage baixo simula o
        # artefato que dispara o flag.
        v = classify("ESE", "cap. X, item 13", INDULGENCIA, cited_coverage=0.3)
        self.assertEqual(v.label, "supported")

    def test_fabricated_when_nowhere(self):
        v = classify(
            "LE", "q. 100",
            "esta frase inventada nao aparece em locus algum do pentateuco kardequiano",
            cited_coverage=0.0,
        )
        self.assertEqual(v.label, "fabricated")


class CitedCoversTests(unittest.TestCase):
    def test_le_range_contains_best(self):
        # Citação em range cobre o locus de cobertura máxima → não é mal-atribuição.
        self.assertTrue(cited_covers("LE", "q. 161–162", "q. 162"))
        self.assertTrue(cited_covers("LE", "q. 825-872", "q. 872"))

    def test_le_single_ref_distinct_is_not_covered(self):
        self.assertFalse(cited_covers("LE", "q. 843", "q. 872"))

    def test_chaptered_range_same_chapter(self):
        self.assertTrue(cited_covers("ESE", "cap. XVI, itens 6-9", "cap. XVI, item 7"))

    def test_chaptered_range_other_chapter_not_covered(self):
        self.assertFalse(cited_covers("ESE", "cap. XVI, itens 6-9", "cap. XV, item 7"))

    def test_ci_part_must_match(self):
        # Mesmo romano em partes diferentes de C&I não se cobrem.
        self.assertFalse(
            cited_covers("C&I", "1ª parte, cap. I, item 4", "2ª parte, cap. I, item 4")
        )


class MonotonicIndexTests(unittest.TestCase):
    def test_le_refs_unique(self):
        # Filtro monotônico → cada questão aparece uma vez (sem segmentos
        # espúrios de ordinais internos "1.º").
        refs = [s.ref for s in build_index("LE")]
        self.assertEqual(len(refs), len(set(refs)))

    def test_lm_refs_unique(self):
        # LM item 223 gerava 27 "item 2" espúrios antes do monotônico.
        refs = [s.ref for s in build_index("LM")]
        self.assertEqual(len(refs), len(set(refs)))
        self.assertEqual(refs.count("item 2"), 1)


class WordCoverageTests(unittest.TestCase):
    def test_verbatim_is_full_coverage(self):
        seg = next(s for s in build_index("ESE") if s.ref == "cap. X, item 13")
        self.assertGreaterEqual(word_coverage(INDULGENCIA, seg.norm_text), 0.95)

    def test_scattered_function_words_score_low(self):
        # Frase de palavras comuns contra texto sem o trecho contíguo: a
        # contiguidade (min_block=3) mantém a cobertura baixa.
        seg = next(s for s in build_index("ESE") if s.ref == "cap. X, item 13")
        self.assertLess(
            word_coverage("a de que em o para com uma por isso", seg.norm_text), 0.5
        )


if __name__ == "__main__":
    unittest.main()
