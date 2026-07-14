"""Testes do check `check_unlinked_concept_mention` (lint_wiki.py).

Este check é o "eixo 4" da /critica rebaixado a lint: página-conceito existe, é
nomeada na prosa de outra página, e não é linkada. Antes, um agente Opus derivava
isto página a página — e o achado ainda descia para a fila de decisão humana do
ROADMAP §11. É código, e código é grátis e roda em todo push (ROADMAP §5,
princípio das 3 camadas).

O que os testes travam, em ordem de gravidade:

  1. **Nunca sugerir wikilink dentro de citação literal (`>`)** nem em texto-fonte
     (`capitulo-pentateuco`, `capitulo-biblico`). Enfiar `[[...]]` no meio de
     Kardec adultera a fonte primária. É a invariante que não pode cair.
  2. Exigir SALIÊNCIA (tf >= 2) e ESPECIFICIDADE (df baixo). A versão ingênua
     ("conceito existe e foi nomeado → linkar") rende 3198 achados em 768 páginas
     — ruído que ninguém age. Com os limiares: 64 achados em 54 páginas.
  3. Casar sem acento: a wiki não é consistente (`conceitos/demonios.md` tem
     `# Demonios` no H1, e a prosa alheia escreve "demônios").
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "lint" / "scripts"))

import lint_wiki  # noqa: E402
from lint_wiki import check_unlinked_concept_mention  # noqa: E402


class WikiFalsaMixin(unittest.TestCase):
    """Monta uma wiki de mentira e aponta o lint para ela.

    `_concept_names()` é `lru_cache`ado e varre `WIKI_DIR` — sem limpar o cache
    entre os testes, o segundo teste veria os conceitos do primeiro.
    """

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.wiki = Path(self._tmp.name) / "wiki"
        (self.wiki / "conceitos").mkdir(parents=True)
        (self.wiki / "aprofundamentos").mkdir()
        (self.wiki / "pentateuco").mkdir()
        self._wiki_real = lint_wiki.WIKI_DIR
        lint_wiki.WIKI_DIR = self.wiki
        lint_wiki._concept_names.cache_clear()

    def tearDown(self):
        lint_wiki.WIKI_DIR = self._wiki_real
        lint_wiki._concept_names.cache_clear()
        self._tmp.cleanup()

    def conceito(self, slug: str, titulo: str) -> Path:
        p = self.wiki / "conceitos" / f"{slug}.md"
        p.write_text(
            f"---\ntipo: conceito\nstatus: ativo\n---\n\n# {titulo}\n\nTexto.\n",
            encoding="utf-8",
        )
        return p

    def pagina(self, nome: str, corpo: str, tipo: str = "aprofundamento") -> Path:
        p = self.wiki / "aprofundamentos" / f"{nome}.md"
        p.write_text(
            f"---\ntipo: {tipo}\nstatus: ativo\n---\n\n# {nome}\n\n{corpo}\n",
            encoding="utf-8",
        )
        return p

    def rodar(self, pages: list[Path]) -> list[dict]:
        return check_unlinked_concept_mention(pages)["items"]


class TestNaoAdulteraFonte(WikiFalsaMixin):
    """A invariante que não pode cair."""

    def test_nao_sugere_link_dentro_de_citacao_literal(self):
        """Uma aspa de Kardec é intocável. O termo aparece 3x, mas todas as
        ocorrências estão em blockquote — sugerir link ali adulteraria a
        citação."""
        self.conceito("principio-vital", "Principio vital")
        alvo = self.pagina(
            "estudo",
            "> O principio vital anima. O principio vital nao pensa.\n"
            "> Sem o principio vital nao ha vida organica.",
        )
        self.assertEqual(self.rodar([alvo]), [])

    def test_nao_sugere_link_em_texto_fonte_do_pentateuco(self):
        """`capitulo-pentateuco` é o texto do próprio Kardec, publicado. Nunca
        recebe wikilink, por mais saliente que o conceito seja."""
        self.conceito("principio-vital", "Principio vital")
        p = self.wiki / "pentateuco" / "cap-i.md"
        p.write_text(
            "---\ntipo: capitulo-pentateuco\nstatus: ativo\n---\n\n# Cap I\n\n"
            "O principio vital anima. O principio vital é distinto da alma. "
            "O principio vital reside no fluido.\n",
            encoding="utf-8",
        )
        self.assertEqual(self.rodar([p]), [])


class TestSalienciaEEspecificidade(WikiFalsaMixin):
    def test_menciona_2x_e_nao_linka_ENTAO_reporta(self):
        self.conceito("telepatia", "Telepatia")
        alvo = self.pagina(
            "estudo",
            "A telepatia aparece nos relatos. Bozzano documenta telepatia entre "
            "vivos.",
        )
        items = self.rodar([alvo])
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["target"], "wiki/conceitos/telepatia")
        self.assertEqual(items[0]["mencoes"], 2)

    def test_uma_mencao_de_passagem_NAO_merece_link(self):
        """tf=1 é menção de passagem. Linkar tudo que foi citado uma vez é o que
        produz as 3198 sugestões de ruído."""
        self.conceito("telepatia", "Telepatia")
        alvo = self.pagina("estudo", "Cita-se telepatia de passagem, e mais nada.")
        self.assertEqual(self.rodar([alvo]), [])

    def test_conceito_ja_linkado_NAO_reporta(self):
        """Se o cross-ref já existe (mesmo que só em Páginas relacionadas), o
        resto é polimento sem valor."""
        self.conceito("telepatia", "Telepatia")
        alvo = self.pagina(
            "estudo",
            "A telepatia aparece. Bozzano documenta telepatia.\n\n"
            "## Páginas relacionadas\n- [[wiki/conceitos/telepatia]]",
        )
        self.assertEqual(self.rodar([alvo]), [])

    def test_conceito_ubiquo_NAO_reporta(self):
        """Conceito nomeado em >3% das páginas é vocabulário ambiente ("orgulho",
        "família"): linkar em toda ocorrência polui em vez de conectar. O limiar é
        COMPUTADO da wiki, não uma lista chumbada."""
        self.conceito("orgulho", "Orgulho")
        corpo = "O orgulho cega. O orgulho é raiz de muitos males."
        pages = [self.pagina(f"p{i}", corpo) for i in range(50)]
        self.assertEqual(self.rodar(pages), [])

    def test_pagina_nao_se_autolinka(self):
        c = self.conceito("telepatia", "Telepatia")
        # a própria página-conceito nomeia o conceito no corpo
        c.write_text(
            "---\ntipo: conceito\nstatus: ativo\n---\n\n# Telepatia\n\n"
            "A telepatia é isto. A telepatia é aquilo.\n",
            encoding="utf-8",
        )
        self.assertEqual(self.rodar([c]), [])


class TestAcento(WikiFalsaMixin):
    def test_casa_ignorando_acento(self):
        """O H1 do conceito é "Demonios" (sem acento, como está hoje na wiki) e a
        prosa alheia escreve "demônios". Casar literalmente perderia justamente as
        ocorrências que interessam."""
        self.conceito("demonios", "Demonios")
        alvo = self.pagina(
            "estudo",
            "Os demônios da tradição. Kardec nega demônios como seres à parte.",
        )
        items = self.rodar([alvo])
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["target"], "wiki/conceitos/demonios")


if __name__ == "__main__":
    unittest.main()
