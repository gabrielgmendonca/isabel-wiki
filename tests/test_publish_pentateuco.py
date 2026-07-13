"""Testes da Fase 2 do híbrido (link interno preferencial p/ o Pentateuco).

Cobre:
- `publish_pentateuco`: round-trip do texto publicado contra `cite.literal_text`
  (garantia de "não perder informação") e que rodar o publisher em modo --check
  não toca em `raw/` (garantia de "não alterar o Kardec").
- `link_citations`: preferência por link interno quando há âncora, com fallback
  ao Kardecpedia nos loci sem âncora (Introdução-item, Conclusão).
"""
from __future__ import annotations

import hashlib
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import publish_pentateuco as pp  # noqa: E402
from cite import literal_text  # noqa: E402
from link_citations import kardec_internal_path, link_kardec  # noqa: E402

ANCHORS = json.loads((ROOT / "data" / "pentateuco-anchors.json").read_text(encoding="utf-8"))
WIKI = ROOT / "wiki" / "pentateuco"


def _block_under_anchor(rel_anchor: str) -> str:
    """Texto sob a âncora `<rel>#<anchor>` no arquivo publicado, até o próximo
    heading `## ` — espelha a terminação que o cite.py usa."""
    rel, anchor = rel_anchor.split("#", 1)
    prefix, n = anchor.split("-", 1)
    heading = f"## q. {n}" if prefix == "q" else f"## item {n}"
    lines = (WIKI / f"{rel}.md").read_text(encoding="utf-8").splitlines()
    i = lines.index(heading)
    out = []
    for line in lines[i + 1:]:
        if line.startswith("## "):
            break
        out.append(line)
    return "\n".join(out).strip()


def _cite_ref(sigla: str, key: str) -> str:
    """Reconstrói a referência cite.py a partir da chave do manifest."""
    if sigla in ("LE", "LM"):
        n = key
        return f"q. {n}" if sigla == "LE" else f"item {n}"
    parts = key.split(":")
    roman, n = parts[-2], parts[-1]  # "ROMAN:n" ou "PART:ROMAN:n"
    return f"cap. {roman}, item {n}"


class RoundTripTests(unittest.TestCase):
    """O bloco sob cada âncora publicada é byte-a-byte igual ao que o cite.py
    extrai do raw — para uma amostra por obra (rápido) e alguns loci canônicos."""

    def _sample(self, sigla: str, unit_key: str, k: int = 25):
        book = ANCHORS[sigla][unit_key]
        keys = list(book.keys())[:k]
        for key in keys:
            rel_anchor = book[key]
            published = _block_under_anchor(rel_anchor)
            truth = literal_text(sigla, _cite_ref(sigla, key))
            self.assertIsNotNone(truth, f"{sigla} {key}: cite.py não resolveu")
            self.assertEqual(
                truth.strip(), published,
                f"{sigla} {key}: texto publicado diverge do raw via cite.py",
            )

    def test_le_questions(self):
        self._sample("LE", "questions")

    def test_lm_items(self):
        self._sample("LM", "items")

    def test_ese_items(self):
        self._sample("ESE", "items")

    def test_ci_items(self):
        self._sample("C&I", "items")

    def test_genese_items(self):
        self._sample("Genese", "items")

    def test_specific_loci(self):
        # Loci citados na doutrina, conferindo o caminho exato.
        self.assertEqual(ANCHORS["LE"]["questions"]["1"],
                         "livro-dos-espiritos/parte-1-cap-i#q-1")
        self.assertEqual(ANCHORS["ESE"]["items"]["XVII:4"],
                         "evangelho-segundo-o-espiritismo/cap-xvii#item-4")
        for sigla, key in [("LE", "990"), ("LM", "230"), ("Genese", "XI:13")]:
            book = ANCHORS[sigla]["questions" if sigla == "LE" else "items"]
            self.assertEqual(_block_under_anchor(book[key]).strip(),
                             literal_text(sigla, _cite_ref(sigla, key)).strip())


class CoberturaDeAncorasTests(unittest.TestCase):
    """Piso de cobertura por obra — trava PERDA SILENCIOSA de âncora.

    O round-trip é fail-safe: quando o publisher e o `cite.py` discordam sobre
    onde um item começa/termina, a âncora simplesmente NÃO é registrada e a
    citação cai no link externo. Isso é seguro, mas silencioso — nenhum teste
    quebra. Foi o que aconteceu ao alinhar as duas segmentações: aplicar a
    segmentação de capítulo ao LM (cuja numeração é contínua, não reinicia por
    capítulo) evaporou 29 âncoras legítimas sem falhar teste nenhum.

    Os pisos ficam ~5% abaixo da cobertura real medida em 2026-07-13, para não
    quebrarem a cada âncora nova, mas pegarem um colapso.
    """

    PISOS = {
        ("LE", "questions"): 960,
        ("LM", "items"): 290,
        ("ESE", "items"): 450,
        ("C&I", "items"): 185,
        ("Genese", "items"): 610,
    }

    def test_cobertura_por_obra_nao_colapsa(self):
        for (sigla, unit), piso in self.PISOS.items():
            n = len(ANCHORS[sigla][unit])
            self.assertGreaterEqual(
                n, piso,
                f"{sigla}/{unit}: só {n} âncoras (piso {piso}). Publisher e cite.py "
                f"provavelmente divergiram na segmentação — o round-trip descartou "
                f"as âncoras em silêncio. Regenerar: uv run python scripts/publish_pentateuco.py",
            )

    def test_ancoras_do_manifest_existem_na_pagina(self):
        # Uma âncora registrada tem de ter heading correspondente na página.
        for sigla, unit in self.PISOS:
            book = ANCHORS[sigla][unit]
            for key in list(book)[:40]:
                self.assertIsNotNone(
                    _block_under_anchor(book[key]),
                    f"{sigla} {key}: manifest aponta para âncora inexistente ({book[key]})",
                )


class InternalLinkTests(unittest.TestCase):
    def test_internal_path_le_question(self):
        p = kardec_internal_path(ANCHORS, "LE", ", q. 1")
        self.assertEqual(p, "livro-dos-espiritos/parte-1-cap-i#q-1")

    def test_internal_path_ese_item(self):
        p = kardec_internal_path(ANCHORS, "ESE", ", cap. XVII, item 4")
        self.assertEqual(p, "evangelho-segundo-o-espiritismo/cap-xvii#item-4")

    def test_internal_path_lm_item_with_chapter(self):
        # (LM, 2ª parte, cap. XX, item 230) → cai no item flat global.
        p = kardec_internal_path(ANCHORS, "LM", ", 2ª parte, cap. XX, item 230")
        self.assertEqual(p, "livro-dos-mediuns/parte-2-cap-xx#item-230")

    def test_internal_path_genese_with_accent(self):
        # A sigla "Gênese" normaliza para "Genese" (chave do manifest).
        p = kardec_internal_path(ANCHORS, "Gênese", ", cap. XI, item 13")
        self.assertEqual(p, "genese/cap-xi#item-13")

    def test_internal_none_for_intro_item(self):
        # (LE, Introdução, item IV) não tem âncora → None (fallback externo).
        self.assertIsNone(kardec_internal_path(ANCHORS, "LE", ", Introdução, item IV"))

    def test_internal_none_for_conclusion(self):
        self.assertIsNone(kardec_internal_path(ANCHORS, "LE", ", Conclusão, IX"))

    def test_link_kardec_prefers_internal(self):
        repl = link_kardec({"books": {}}, ANCHORS)
        import re
        m = re.search(r"\(\s*(?P<sigla>LE)\b(?P<rest>[^)]*)\)", "(LE, q. 1)")
        out = repl(m)
        self.assertEqual(out, "[[wiki/pentateuco/livro-dos-espiritos/parte-1-cap-i#q-1|(LE, q. 1)]]")

    def test_link_kardec_external_fallback_without_anchors(self):
        # Sem manifest, mantém o comportamento externo (mapping vazio → intacto).
        repl = link_kardec({"books": {}}, None)
        import re
        m = re.search(r"\(\s*(?P<sigla>LE)\b(?P<rest>[^)]*)\)", "(LE, q. 1)")
        self.assertEqual(repl(m), "(LE, q. 1)")


class RawUntouchedTests(unittest.TestCase):
    def test_check_only_does_not_touch_raw(self):
        raw_files = sorted(pp.PENTATEUCO_DIR.glob("*.md"))
        self.assertTrue(raw_files, "nenhum arquivo raw encontrado")
        before = {f: hashlib.sha256(f.read_bytes()).hexdigest() for f in raw_files}
        rc = pp.publish(check_only=True)
        self.assertEqual(rc, 0)
        after = {f: hashlib.sha256(f.read_bytes()).hexdigest() for f in raw_files}
        self.assertEqual(before, after, "publisher alterou arquivo(s) em raw/")


if __name__ == "__main__":
    unittest.main()
