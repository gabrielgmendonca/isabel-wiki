"""Testes de `validate_candidates.py` — refutação mecânica do Passo 4 de /slides.

O que estes testes travam é a **calibragem contra o corpus real**: cada caso
abaixo é um título ou pergunta que existe (ou existiu) num deck de
`slides/`, ou um ✓/✗ literal das rules. Se alguém apertar um heurístico e
começar a reprovar o padrão que a rule defende, aparece aqui.

O caso que motivou a divisão falha/aviso: o ✓ exemplar da rule socrática
("Como uma mãe que perdeu a filha de seis anos...") tem 16 palavras, e a
primeira versão do validador o reprovava — o validador reprovando o padrão que
existe para defender.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "slides" / "scripts"))

from validate_candidates import (  # noqa: E402
    check_pergunta,
    check_titulo,
    content_words,
    norm,
    parse_candidato,
)


def regras(falhas: list[dict]) -> set[str]:
    return {f["regra"] for f in falhas}


class TestPerguntasDoCorpus(unittest.TestCase):
    """✗ e ✓ literais de convencoes-perguntas-socraticas.md."""

    def test_teasers_com_E_inicial_sao_reprovados(self):
        # As três ✗ "teaser" da rule abrem todas com "E ".
        for q in ("E se quem partiu pudesse falar?",
                  "E a fé que ainda não raciocina, vale?",
                  "E quando a aflição não tem culpa visível?",
                  "E se a vida fosse mais longa do que parece?"):
            with self.subTest(q=q):
                falhas, _ = check_pergunta(q, None)
                self.assertIn("teaser", regras(falhas))

    def test_pergunta_paragrafo_do_indulgencia_e_reprovada(self):
        q = ('Diante da adúltera, os acusadores se retiraram "afastando-se '
             'primeiro os velhos". Por que os mais velhos foram os primeiros '
             "a largar a pedra?")
        falhas, _ = check_pergunta(q, None)
        self.assertIn("pergunta_duas_frases", regras(falhas))
        self.assertIn("pergunta_longa", regras(falhas))

    def test_exemplar_de_16_palavras_passa_com_aviso(self):
        """Teto de 15 é aviso, não bloqueio — senão reprova o ✓ da rule."""
        q = ("Como uma mãe que perdeu a filha de seis anos pode, ainda assim, "
             "agradecer a Deus?")
        falhas, avisos = check_pergunta(q, None)
        self.assertEqual(falhas, [])
        self.assertIn("pergunta_acima_do_orcamento", regras(avisos))

    def test_perguntas_boas_passam_sem_aviso(self):
        for q in ("Se a causa é anterior, por que esquecemos?",
                  "Por que os mais velhos largaram a pedra primeiro?",
                  "Perdão sem limites — então o indulgente é um frouxo?",
                  "Marcel pediu pílulas para não incomodar; que fé sustenta "
                  "isso aos 8 anos?"):
            with self.subTest(q=q):
                falhas, avisos = check_pergunta(q, None)
                self.assertEqual(falhas, [], f"reprovou boa: {regras(falhas)}")
                self.assertEqual(avisos, [])

    def test_sem_interrogacao_e_reprovada(self):
        falhas, _ = check_pergunta("O perdão é divino.", None)
        self.assertIn("nao_e_pergunta", regras(falhas))

    def test_citacao_abreviada_nao_conta_como_duas_frases(self):
        for q in ("O que Kardec diz no cap. X sobre isso?",
                  "A resposta da q. 886 basta para definir caridade?"):
            with self.subTest(q=q):
                falhas, _ = check_pergunta(q, None)
                self.assertNotIn("pergunta_duas_frases", regras(falhas))


class TestReformulacaoDoSectionHeader(unittest.TestCase):
    """Antipadrão "reformulação vazia": a pergunta recicla o header."""

    def test_reciclagem_alta_e_reprovada(self):
        falhas, _ = check_pergunta(
            "Como entender a causa que escapa ao olhar terreno?",
            "A causa que escapa ao olhar terreno",
        )
        self.assertIn("reformulacao_do_section_header", regras(falhas))

    def test_pergunta_independente_passa(self):
        falhas, _ = check_pergunta(
            "Se a causa é anterior, por que esquecemos?",
            "A causa que escapa ao olhar terreno",
        )
        self.assertNotIn("reformulacao_do_section_header", regras(falhas))

    def test_content_words_descarta_stopword(self):
        self.assertNotIn("que", content_words("A causa que escapa"))
        self.assertIn("causa", content_words("A causa que escapa"))


class TestTitulosDoCorpus(unittest.TestCase):
    """Antipadrões e ✓ de convencoes-titulos-slides.md."""

    def test_coordenacao_de_conceitos_reprovada(self):
        falhas, _ = check_titulo("Expiação e arrependimento", "afirmacao",
                                 "", set(), False)
        self.assertIn("coordenacao_de_conceitos", regras(falhas))

    def test_telegrafico_reprovado(self):
        falhas, _ = check_titulo("Dor: Rigidez", "afirmacao", "", set(), False)
        self.assertIn("telegrafico", regras(falhas))

    def test_rotulo_nominal_curto_reprovado(self):
        for t in ("A tríade", "O excesso íntimo", "A dureza social"):
            with self.subTest(t=t):
                falhas, _ = check_titulo(t, "afirmacao", "", set(), False)
                self.assertIn("rotulo_nominal", regras(falhas))

    def test_verbatim_nominal_e_isento(self):
        """"Bem-aventurados os misericordiosos" é nominal e é o padrão nº 1."""
        falhas, _ = check_titulo("Bem-aventurados os misericordiosos",
                                 "verbatim", "", set(), False)
        self.assertEqual(falhas, [])

    def test_mesmo_titulo_sem_declarar_verbatim_e_reprovado(self):
        """Declarar o padrão é o que compra a isenção — não o texto em si."""
        falhas, _ = check_titulo("Bem-aventurados os misericordiosos",
                                 "afirmacao", "", set(), False)
        self.assertIn("rotulo_nominal", regras(falhas))

    def test_afirmacoes_contestaveis_passam(self):
        for t in ("Ninguém é irrecuperável",
                  "O futuro jamais se fecha",
                  "Indulgência não é conivência nem perdão fingido",
                  "Indulgência é dever, porque todos precisamos dela"):
            with self.subTest(t=t):
                falhas, _ = check_titulo(t, "afirmacao", "", set(), False)
                self.assertEqual(falhas, [], f"reprovou bom: {regras(falhas)}")

    def test_cena_tese_longa_passa_no_teto_da_capa(self):
        t = '"Atire a primeira pedra": a indulgência não é fraqueza, é justiça'
        falhas, _ = check_titulo(t, "cena-tese", "", set(), False)
        self.assertEqual(falhas, [])

    def test_teto_de_secao_e_mais_apertado_que_o_de_capa(self):
        t = "A correção de Jesus: indulgência é dever, porque dela todos precisamos"
        capa, _ = check_titulo(t, "cena-tese", "", set(), False)
        secao, _ = check_titulo(t, "cena-tese", "", set(), True)
        self.assertNotIn("longo", regras(capa))
        self.assertIn("longo", regras(secao))


class TestTesteDeOrigem(unittest.TestCase):
    """O único teste obrigatório da rule: não copiar o heading da wiki."""

    def test_igual_ao_h1_da_wiki_reprovado(self):
        falhas, _ = check_titulo("Dor: Rigidez", "afirmacao",
                                 norm("Dor: Rigidez"), set(), False)
        self.assertIn("titulo_herdado", regras(falhas))

    def test_igual_a_heading_da_wiki_reprovado(self):
        hs = {norm("Análise por eixos")}
        falhas, _ = check_titulo("Análise por eixos", "afirmacao", "", hs, True)
        self.assertIn("secao_herdada", regras(falhas))

    def test_titulo_autoral_passa_o_teste_de_origem(self):
        falhas, _ = check_titulo("A dureza que chamamos de firmeza", "afirmacao",
                                 norm("Dor: Rigidez"), set(), False)
        self.assertNotIn("titulo_herdado", regras(falhas))

    def test_parte_sem_nome_reprovada(self):
        for t in ("Parte 1", "Parte II", "III", "Parte 4 —"):
            with self.subTest(t=t):
                falhas, _ = check_titulo(t, "afirmacao", "", set(), True)
                self.assertIn("parte_sem_nome", regras(falhas))


class TestLimitesConhecidos(unittest.TestCase):
    """Trava o que o script NÃO alcança, para o limite não ser esquecido.

    Se um dia estes passarem a reprovar, o docstring do script e a seção de
    auto-refutação do SKILL.md precisam ser revisados — não é regressão, é
    mudança de divisão de trabalho entre camada 0 e camada 1.
    """

    def test_nominalizacao_longa_escapa_do_heuristico(self):
        for t in ("A causa que escapa ao olhar terreno",
                  "A justiça das aflições e a fé que consola"):
            with self.subTest(t=t):
                falhas, _ = check_titulo(t, "afirmacao", "", set(), False)
                self.assertEqual(
                    falhas, [],
                    "se passou a reprovar, atualizar a seção 'Limites "
                    "conhecidos' do script e a auto-refutação do SKILL.md",
                )


class TestParseCandidato(unittest.TestCase):
    def test_sufixo_de_padrao_e_separado(self):
        self.assertEqual(parse_candidato("Ninguém é irrecuperável:afirmacao",
                                         "titulo"),
                         ("Ninguém é irrecuperável", "afirmacao"))

    def test_dois_pontos_no_titulo_nao_confunde(self):
        texto, padrao = parse_candidato(
            '"Atire a primeira pedra": a indulgência é justiça:cena-tese',
            "titulo")
        self.assertEqual(padrao, "cena-tese")
        self.assertTrue(texto.startswith('"Atire'))

    def test_sufixo_invalido_fica_no_texto(self):
        texto, padrao = parse_candidato("Dor: Rigidez", "titulo")
        self.assertEqual(texto, "Dor: Rigidez")
        self.assertEqual(padrao, "")

    def test_pergunta_ignora_sufixo(self):
        self.assertEqual(parse_candidato("Por que assim?", "pergunta"),
                         ("Por que assim?", ""))


if __name__ == "__main__":
    unittest.main()
