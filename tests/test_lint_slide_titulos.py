"""Testes do check `check_slide_titulos` (lint_wiki.py).

Camada 0 de dois problemas distintos, ambos de `/slides`:

1. **Título herdado** — o scaffold copiava o H1 da página wiki para a capa e cada
   `##` da página para os section headers. Verbete de índice ("Dor: Rigidez",
   "A tríade") não é título de palestra. Ver `convencoes-titulos-slides.md`.
2. **Pergunta-parágrafo** — os critérios A/B/C de
   `convencoes-perguntas-socraticas.md` corrigiram a vagueza das perguntas-ponte
   e passaram do ponto: o modelo passou a enfiar a âncora dentro da frase da
   pergunta, indo de ~8 para 23-30 palavras num h2 de 64px.

O que estes testes travam são as **invariantes que geram falso positivo**, que
foi onde a primeira versão do check errou:

- `## Parte 3` + `### <nome>` em headings separados **é** parte nomeada (o deck
  `indulgencia` usa esse layout) — não pode acusar `parte_sem_nome`.
- section header estrutural do scaffold ("Síntese", "Para meditar") não pede
  título autoral nem se compara com o heading da wiki.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "lint" / "scripts"))

from lint_wiki import (  # noqa: E402
    _FRASE_BREAK_RE,
    _PARTE_SEM_NOME_RE,
    _norm_titulo,
    _slide_headings,
)

FRONTMATTER = "---\nmarp: true\ntheme: isabel\n---\n\n"


def _section(*headings: str) -> str:
    corpo = "\n\n".join(headings)
    return f"<!-- _class: section -->\n\n{corpo}\n"


class TestParteSemNome(unittest.TestCase):
    """`parte_sem_nome` só quando nenhum heading do slide carrega nome."""

    def test_numeracao_pura_e_sem_nome(self):
        for h in ("Parte 1", "Parte II", "III", "3", "Parte 4 —", "II -"):
            with self.subTest(h=h):
                self.assertRegex(h, _PARTE_SEM_NOME_RE)

    def test_numeracao_com_nome_na_mesma_linha_nao_e_sem_nome(self):
        for h in ("Parte 1 — A dureza social", "III — A tríade"):
            with self.subTest(h=h):
                self.assertIsNone(_PARTE_SEM_NOME_RE.match(h))

    def test_nome_em_heading_separado_conta(self):
        """Layout do deck `indulgencia`: `## Parte 1` + `### <nome>`."""
        slide = _section("## Parte 1", '### "Indulgência é fazer vista grossa"?')
        headings = _slide_headings(slide)
        self.assertEqual(len(headings), 2)
        # O primeiro é numeração pura; o segundo carrega o nome da parte.
        self.assertRegex(headings[0][0], _PARTE_SEM_NOME_RE)
        self.assertIsNone(_PARTE_SEM_NOME_RE.match(headings[1][0]))

    def test_heading_em_comentario_nao_conta(self):
        slide = _section("## Parte 2", "<!-- ## comentado -->")
        self.assertEqual([h for h, _ in _slide_headings(slide)], ["Parte 2"])


class TestNormalizacaoDeTitulo(unittest.TestCase):
    """Comparação deck vs. wiki ignora markdown, aspas, caixa e pontuação final."""

    def test_ignora_markdown_e_aspas(self):
        self.assertEqual(
            _norm_titulo('**"Atire a primeira pedra"**:'),
            "atire a primeira pedra",
        )

    def test_ignora_caixa_e_espaco(self):
        self.assertEqual(_norm_titulo("  Dor:  Rigidez  "), "dor: rigidez")

    def test_titulos_diferentes_nao_colidem(self):
        self.assertNotEqual(
            _norm_titulo("Expiação e arrependimento"),
            _norm_titulo("Ninguém é irrecuperável"),
        )


class TestPerguntaDuasFrases(unittest.TestCase):
    """Setup + pergunta na mesma caixa de 64px é o modo de falha a pegar."""

    def test_pega_setup_mais_pergunta(self):
        q = ('Diante da adúltera, os acusadores se retiraram "afastando-se '
             'primeiro os velhos". Por que os mais velhos foram os primeiros '
             "a largar a pedra?")
        self.assertIsNotNone(_FRASE_BREAK_RE.search(q))

    def test_pergunta_de_uma_frase_passa(self):
        for q in (
            "Por que os mais velhos largaram a pedra primeiro?",
            "Perdão sem limites — então o indulgente é um frouxo?",
            "Severo comigo, indulgente com o outro — quando inverti isso?",
            "Se a causa é anterior, por que esquecemos?",
        ):
            with self.subTest(q=q):
                self.assertIsNone(_FRASE_BREAK_RE.search(q))

    def test_abreviacao_de_citacao_nao_e_quebra_de_frase(self):
        """"cap. X", "q. 886", "item 4." não são fim de frase."""
        for q in (
            "O que Kardec quis dizer no cap. X sobre a indulgência?",
            "A resposta da q. 886 basta para definir caridade?",
            "O item 4. do capítulo contradiz isso?",
        ):
            with self.subTest(q=q):
                self.assertIsNone(_FRASE_BREAK_RE.search(q))


class TestDecksDoRepo(unittest.TestCase):
    """O check roda limpo nos decks versionados — sem erro que barre o CI."""

    def test_check_nao_tem_erro_nos_decks_atuais(self):
        from lint_wiki import check_slide_titulos

        import os
        cwd = os.getcwd()
        os.chdir(ROOT)
        try:
            res = check_slide_titulos([])
        finally:
            os.chdir(cwd)
        erros = [i for i in res["items"] if i["severity"] == "error"]
        self.assertEqual(erros, [], f"erros que barrariam o CI: {erros}")


if __name__ == "__main__":
    unittest.main()
