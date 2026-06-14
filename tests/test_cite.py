"""Testes leves de scripts/cite.py.

Usa o LE real em `raw/kardec/pentateuco/livro-dos-espiritos.md` como fixture
estável (o cânon não muda). Smoke + erros previsíveis; cobertura exaustiva
do parser fica para os testes de kardec_structure.
"""
from __future__ import annotations

import io
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from cite import main  # noqa: E402


def _run(args: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = main(args)
    return code, out.getvalue(), err.getvalue()


class CiteSmokeTests(unittest.TestCase):
    def test_le_q1_contem_que_e_deus(self):
        code, out, _ = _run(["LE", "q. 1"])
        self.assertEqual(code, 0)
        self.assertIn("Que é Deus?", out)
        self.assertIn("(LE, q. 1)", out)

    def test_locus_invalido_aborta_com_codigo_nao_zero(self):
        code, _, err = _run(["LE", "q. 99999"])
        self.assertNotEqual(code, 0)
        self.assertIn("fora do range", err)

    def test_sigla_desconhecida_aborta(self):
        code, _, err = _run(["XYZ", "q. 1"])
        self.assertNotEqual(code, 0)
        self.assertIn("sigla desconhecida", err)


class CiteConclusaoNumeracaoDuplaTests(unittest.TestCase):
    """q. 1012–1019 do LE usam numeração dupla 'Kardec [sequencial].' no raw
    (ex.: '1015 [1014].') porque Kardec saltou o nº 1011. cite.py deve
    resolvê-las pelo nº de Kardec e explicar a ausência da 1011."""

    def test_q1015_resolve_pela_numeracao_de_kardec(self):
        code, out, _ = _run(["LE", "q. 1015"])
        self.assertEqual(code, 0)
        self.assertIn("(LE, q. 1015)", out)
        self.assertIn("alma a penar", out)

    def test_q1019_resolve_reinado_do_bem(self):
        code, out, _ = _run(["LE", "q. 1019"])
        self.assertEqual(code, 0)
        self.assertIn("(LE, q. 1019)", out)
        self.assertIn("reinado do bem", out)

    def test_q1011_inexistente_explica_o_salto(self):
        code, _, err = _run(["LE", "q. 1011"])
        self.assertNotEqual(code, 0)
        self.assertIn("saltou", err)


class CiteESEMarcadorNegritoTests(unittest.TestCase):
    """O markdown do ESE alterna entre marcador simples ('N.') e negrito
    ('**N.**') — às vezes dentro do mesmo capítulo. O extractor de item tem de
    casar ambos; antes da tolerância a asteriscos, capítulos inteiros em negrito
    (X, XI, XIII–XVI) davam 'item não encontrado'."""

    def test_item_negrito_resolve(self):
        # cap. X, item 4 vem como "**4.**" no raw.
        code, out, _ = _run(["ESE", "cap. X, item 4"])
        self.assertEqual(code, 0)
        self.assertIn("(ESE, cap. X, item 4)", out)
        self.assertIn("A misericórdia é o complemento da brandura", out)

    def test_item_simples_continua_resolvendo(self):
        # cap. XVII, item 4 vem como "4." simples — não pode regredir.
        code, out, _ = _run(["ESE", "cap. XVII, item 4"])
        self.assertEqual(code, 0)
        self.assertIn("(ESE, cap. XVII, item 4)", out)
        self.assertIn("não institui nenhuma nova moral", out)

    def test_item_negrito_nao_confunde_com_simples_de_outro_capitulo(self):
        # Há "23." simples no cap. IV e "**23.**" negrito no cap. V; a busca
        # restrita ao range do capítulo deve pegar o do cap. V.
        code, out, _ = _run(["ESE", "cap. V, item 23"])
        self.assertEqual(code, 0)
        self.assertIn("(ESE, cap. V, item 23)", out)
        self.assertIn("Vive o homem incessantemente em busca da felicidade", out)


class CiteESEIntroducaoTests(unittest.TestCase):
    """A Introdução do ESE é extraída inteira; itens da Introdução não, porque
    o markup é irregular demais para extração confiável."""

    def test_introducao_inteira_resolve(self):
        code, out, _ = _run(["ESE", "Introdução"])
        self.assertEqual(code, 0)
        self.assertIn("(ESE, Introdução)", out)
        self.assertIn("Objetivo desta obra", out)
        self.assertIn("Autoridade da Doutrina espírita", out)

    def test_item_da_introducao_aborta_com_mensagem_clara(self):
        code, _, err = _run(["ESE", "Introdução, item II"])
        self.assertNotEqual(code, 0)
        self.assertIn("itens da Introdução não são extraídos", err)


class CiteCeuInfernoSegundaParteTests(unittest.TestCase):
    """C&I repete o algarismo romano entre 1ª e 2ª parte (cap. I existe nas
    duas). Antes, extract_capitulo ignorava a parte e devolvia SEMPRE o capítulo
    da 1ª parte — toda citação de 2ª parte (8 capítulos, 200+ ocorrências na
    wiki) caía no texto errado."""

    def test_segunda_parte_cap_v_e_suicidas_nao_purgatorio(self):
        # 2ª parte cap. V = "Suicidas" (linhas 2878–3042); 1ª parte cap. V =
        # "O Purgatório" (linhas 652–805). Não pode devolver o purgatório.
        code, out, err = _run(["C&I", "2ª parte, cap. V"])
        self.assertEqual(code, 0)
        self.assertIn("(C&I, 2ª parte, cap. V)", out)
        self.assertIn(":2878-3042", out)
        self.assertNotIn("O Purgatório", out)

    def test_primeira_parte_cap_v_continua_purgatorio(self):
        # Regressão: a 1ª parte não pode quebrar com a correção.
        code, out, _ = _run(["C&I", "1ª parte, cap. V"])
        self.assertEqual(code, 0)
        self.assertIn("(C&I, 1ª parte, cap. V)", out)
        self.assertIn("O Purgatório", out)

    def test_segunda_parte_cap_i_item_8_e_a_passagem(self):
        # 2ª parte cap. I = "A passagem"; item 8 fala do estado moral da alma.
        code, out, _ = _run(["C&I", "2ª parte, cap. I, item 8"])
        self.assertEqual(code, 0)
        self.assertIn("(C&I, 2ª parte, cap. I, item 8)", out)
        self.assertIn("estado moral da alma", out)

    def test_parte_inexistente_aborta(self):
        # 2ª parte só tem caps I–VIII; cap. XI só existe na 1ª parte. O locus é
        # barrado já na validação estrutural (resolve_locus), antes da extração.
        code, _, err = _run(["C&I", "2ª parte, cap. XI"])
        self.assertNotEqual(code, 0)
        self.assertIn("inexistente", err)


class CiteFalsosItensTests(unittest.TestCase):
    """_ITEM_RE ancora no início da linha; sem cuidado, casava trechos que não
    são marcadores de item de verdade."""

    def test_cross_ref_quebrada_nao_sombreia_item_real(self):
        # '(N.º\n219.)' deixa '219.)' no início da linha 5418; o item 219 REAL
        # está na 5744. O ')' após o ponto deve descartar a cauda.
        code, out, _ = _run(["LM", "item 219"])
        self.assertEqual(code, 0)
        self.assertIn(":5744", out)
        self.assertIn("mudança da caligrafia", out)

    def test_item_ordinal_de_ci_cap_vii_resolve(self):
        # Em C&I 1ª parte cap. VII os itens canônicos do "Código penal da vida
        # futura" são ordinais ("17.º — …"). NÃO podem ser rejeitados como ruído
        # — ~50 citações reais da wiki dependem disso.
        code, out, _ = _run(["C&I", "1ª parte, cap. VII, item 17"])
        self.assertEqual(code, 0)
        self.assertIn("(C&I, 1ª parte, cap. VII, item 17)", out)
        self.assertIn("O arrependimento pode ocorrer em todo lugar", out)


class CiteLEBlockquoteTests(unittest.TestCase):
    """A q. 566 do LE vem dentro de um blockquote ('>566. …'); sem tolerar o
    marcador de citação a questão ficava inacessível."""

    def test_q566_em_blockquote_resolve(self):
        code, out, _ = _run(["LE", "q. 566"])
        self.assertEqual(code, 0)
        self.assertIn("(LE, q. 566)", out)
        self.assertIn("especialidade artística", out)

    def test_q566_subitem_a_resolve(self):
        code, out, _ = _run(["LE", "q. 566a"])
        self.assertEqual(code, 0)
        self.assertIn("(LE, q. 566a)", out)
        self.assertIn("Espíritos muito adiantados", out)


class CiteQuestaoComTextoExtraTests(unittest.TestCase):
    """`(LE, q. 472 sobre alienação…)` etc.: a palavra após o número NÃO pode ser
    lida como letra de subitem ('s' de 'sobre'). O subitem é grudado ('q. 150b')."""

    def test_q_com_palavra_seguinte_resolve_a_questao(self):
        for ref in ("q. 472 sobre alienação", "q. 626 e seguintes", "q. 540 em nota"):
            code, out, _ = _run(["LE", ref])
            self.assertEqual(code, 0, f"falhou: {ref}")
            n = ref.split()[1]
            self.assertIn(f"(LE, q. {n})", out)

    def test_subitem_grudado_ainda_resolve(self):
        # Não pode regredir: 'q. 566a' continua sendo o subitem a.
        code, out, _ = _run(["LE", "q. 566a"])
        self.assertEqual(code, 0)
        self.assertIn("(LE, q. 566a)", out)


class CiteLMCapituloSemItemTests(unittest.TestCase):
    """LM cita capítulo sem item (`(LM, cap. XXIII)`); extract_lm delega o dump
    estrutural a extract_capitulo (part-aware: o LM tem dois 'Capítulo I')."""

    def test_lm_cap_xxiii_sem_item(self):
        code, out, _ = _run(["LM", "cap. XXIII"])
        self.assertEqual(code, 0)
        self.assertIn("(LM, 2ª parte, cap. XXIII)", out)
        self.assertIn("obsessão", out)

    def test_lm_2a_parte_cap_xxiv(self):
        code, out, _ = _run(["LM", "2ª parte, cap. XXIV"])
        self.assertEqual(code, 0)
        self.assertIn("(LM, 2ª parte, cap. XXIV)", out)
        self.assertIn("identidade", out)

    def test_lm_item_global_nao_regride(self):
        # Citação COM item segue o caminho global (numeração contínua 1–350).
        code, out, _ = _run(["LM", "2ª parte, cap. XX, item 230"])
        self.assertEqual(code, 0)
        self.assertIn("(LM, item 230)", out)


class CiteRangeCapitulosTests(unittest.TestCase):
    """`(Gênese, caps. XIII–XV)` faz dump do span (início de XIII ao fim de XV)."""

    def test_range_genese(self):
        code, out, _ = _run(["Gênese", "caps. XIII–XV"])
        self.assertEqual(code, 0)
        self.assertIn("(Genese, caps. XIII–XV)", out)
        self.assertIn(":6430-8990", out)

    def test_em_dash_glosa_nao_e_range(self):
        # "cap. XXV — Mt 6:16" usa em-dash de glosa, não range; 'Mt' não pode
        # virar romano 'M'. Resolve como capítulo único XXV.
        code, out, _ = _run(["ESE", "cap. XXV — Mt 6:16"])
        self.assertEqual(code, 0)
        self.assertIn("(ESE, cap. XXV)", out)
        self.assertIn("Buscai e achareis", out)


class CiteSecoesAvulsasTests(unittest.TestCase):
    """Introdução marcada como `**INTRODUÇÃO**` inline (Gênese/LM) e Prolegômenos
    do LE — seções avulsas extraídas inteiras."""

    def test_genese_introducao_inline(self):
        code, out, _ = _run(["Gênese", "Introdução"])
        self.assertEqual(code, 0)
        self.assertIn("(Genese, Introdução)", out)
        self.assertIn("Esta nova obra", out)

    def test_le_prolegomenos(self):
        code, out, _ = _run(["LE", "Prolegômenos"])
        self.assertEqual(code, 0)
        self.assertIn("(LE, Prolegômenos)", out)
        self.assertIn("Fenômenos alheios às leis da ciência", out)

    def test_le_introducao_inteira(self):
        code, out, _ = _run(["LE", "Introdução"])
        self.assertEqual(code, 0)
        self.assertIn("(LE, Introdução)", out)
        self.assertIn("estudo da doutrina espírita", out)


if __name__ == "__main__":
    unittest.main()
