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

from cite import (  # noqa: E402
    _find_chapter_range,
    _read_lines,
    extract_capitulo,
    extract_le,
    extract_lm,
    item_blocks,
    literal_text,
    main,
)


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

    def test_numero_decimal_de_tabela_nao_sombreia_item_real(self):
        # O cap. X da Gênese traz uma tabela de composição química cujas linhas
        # são números decimais ("53.360 / 7.021 / 19.686 / 19.934"). A linha
        # "19.686" casava como marcador do item 19 e sombreava o item REAL
        # ("19. Tomamos para termo de comparação o calor…"): `literal_text`
        # devolvia a string "19.686", e o lint acusava de FABRICADA a aspa
        # genuína das páginas que citam esse item.
        code, out, _ = _run(["Gênese", "cap. X, item 19"])
        self.assertEqual(code, 0)
        self.assertIn("Tomamos para termo de comparação", out)
        self.assertIn("verdadeiras pilhas elétricas", out)
        self.assertNotIn("19.686", out)

    def test_enumeracao_ordinal_com_parentese_nao_sombreia_item_real(self):
        # O preâmbulo do ESE cap. XXVIII (Coletânea de preces) enumera as cinco
        # categorias como "1.ª) Preces gerais; / 2.ª) Preces por aquele mesmo que
        # ora; …". Essas linhas casavam como itens 1–5 e sombreavam os itens
        # REAIS do capítulo. O ")" desqualifica — o ordinal sozinho, não.
        code, out, _ = _run(["ESE", "cap. XXVIII, item 2"])
        self.assertEqual(code, 0)
        self.assertIn("Prefácio", out)
        self.assertIn("puséssemos a oração dominical", out)
        self.assertNotIn("Preces por aquele mesmo que ora", out)

    def test_item_3_do_ese_xxviii_traz_a_oracao_dominical(self):
        # O item 3 é a própria oração dominical comentada (I a VII) — várias
        # páginas citam "cap. XXVIII, item 3-I" etc. Antes voltava só a linha
        # "3.ª) Preces pelos vivos;".
        code, out, _ = _run(["ESE", "cap. XXVIII, item 3"])
        self.assertEqual(code, 0)
        self.assertIn("Pai nosso, que estás no céu", out)
        self.assertIn("Venha o teu reino", out)


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


class CiteInvarianteAntiSombreamentoTests(unittest.TestCase):
    """Varredura de invariante — a rede que pega a CLASSE do bug, não o caso.

    Todo bug de sombreamento já visto (cauda `219.)` no LM, tabela decimal
    `19.686` na Gênese, enumeração `2.ª)` no ESE) tem a mesma assinatura: um
    marcador FALSO casa numa linha ANTERIOR à do item verdadeiro, e o extractor
    ancora nele. Daí duas propriedades que o corpus inteiro tem de satisfazer:

    1. **Monotonicidade** — dentro de um capítulo (e ao longo do LE/LM), o item N
       começa numa linha estritamente maior que a do item N-1. Um falso marcador
       à frente do item real faz a linha ANDAR PARA TRÁS.
    2. **Substância** — o corpo de um item tem letras, não só dígitos e
       pontuação. Linha de tabela numérica não é item.

    Isso vale para loci que hoje nem existem em página nenhuma: um regex novo que
    volte a casar ruído quebra estes testes antes de contaminar a wiki.
    """

    ROMANOS = [
        "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII",
        "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX", "XXI", "XXII",
        "XXIII", "XXIV", "XXV", "XXVI", "XXVII", "XXVIII",
    ]
    # (sigla, prefixo da ref, nº de capítulos) — sigla na forma interna que
    # `extract_capitulo` espera ("Genese" sem acento; a normalização da entrada
    # mora na CLI / em `literal_text`). C&I 2ª parte usa relatos nominais (sem
    # itens numerados), então fica fora.
    OBRAS = [
        ("ESE", "", 28),
        ("Genese", "", 18),
        ("C&I", "1ª parte, ", 11),
    ]
    MAX_ITEM = 40  # teto folgado; itens ausentes simplesmente não resolvem

    @staticmethod
    def _linha_inicial(header: str) -> int:
        return int(header.rsplit("linhas ", 1)[1].split("-", 1)[0])

    def _itens_do_capitulo(self, sigla: str, prefixo: str, roman: str):
        """[(n, linha_inicial, corpo)] dos itens que resolvem no capítulo."""
        achados = []
        for n in range(1, self.MAX_ITEM + 1):
            ref = f"{prefixo}cap. {roman}, item {n}"
            try:
                header, body = extract_capitulo(sigla, ref)
            except SystemExit:
                continue  # item inexistente — não é falha
            achados.append((n, self._linha_inicial(header), body))
        return achados

    def test_itens_de_capitulo_sao_monotonicos_e_tem_substancia(self):
        checados = 0
        for sigla, prefixo, n_caps in self.OBRAS:
            for roman in self.ROMANOS[:n_caps]:
                itens = self._itens_do_capitulo(sigla, prefixo, roman)
                anterior_n = anterior_linha = None
                for n, linha, body in itens:
                    checados += 1
                    corpo = body.split("\n", 1)[-1] if body.startswith("AVISO") else body
                    self.assertRegex(
                        corpo, r"[A-Za-zÀ-ÿ]",
                        f"({sigla}, {prefixo}cap. {roman}, item {n}) sem letra "
                        f"nenhuma no corpo — provável linha de tabela numérica: {corpo[:40]!r}",
                    )
                    if anterior_linha is not None:
                        self.assertGreater(
                            linha, anterior_linha,
                            f"({sigla}, {prefixo}cap. {roman}): item {n} começa na linha "
                            f"{linha}, ANTES do item {anterior_n} (linha {anterior_linha}) "
                            f"— marcador falso sombreando o item real",
                        )
                    anterior_n, anterior_linha = n, linha
        # Piso de sanidade: se a varredura parar de achar itens, o teste vira
        # vacuamente verde e deixa de proteger.
        self.assertGreater(checados, 500, "varredura achou itens de menos")

    def test_questoes_do_le_sao_monotonicas(self):
        anterior_n = anterior_linha = None
        checados = 0
        for n in range(1, 1011):
            try:
                header, _ = extract_le(f"q. {n}")
            except SystemExit:
                continue
            linha = self._linha_inicial(header)
            checados += 1
            if anterior_linha is not None:
                self.assertGreater(
                    linha, anterior_linha,
                    f"(LE, q. {n}) começa na linha {linha}, ANTES da q. {anterior_n} "
                    f"(linha {anterior_linha}) — marcador falso sombreando a questão real",
                )
            anterior_n, anterior_linha = n, linha
        self.assertGreater(checados, 950)

    def test_itens_do_lm_sao_monotonicos(self):
        anterior_n = anterior_linha = None
        checados = 0
        for n in range(1, 351):
            try:
                header, _ = extract_lm(f"item {n}")
            except SystemExit:
                continue
            linha = self._linha_inicial(header)
            checados += 1
            if anterior_linha is not None:
                self.assertGreater(
                    linha, anterior_linha,
                    f"(LM, item {n}) começa na linha {linha}, ANTES do item {anterior_n} "
                    f"(linha {anterior_linha}) — marcador falso sombreando o item real",
                )
            anterior_n, anterior_linha = n, linha
        self.assertGreater(checados, 300)


class ItemBlocksContratoTests(unittest.TestCase):
    """`item_blocks` é a fonte única de segmentação que o `publish_pentateuco`
    consome. O contrato: para cada (sigla, item) que ela devolve, o bloco
    delimitado tem de ser IDÊNTICO ao que `literal_text` extrai — senão o
    round-trip do publisher falha e a âncora é descartada em silêncio.

    A quebra concreta que este teste trava: aplicar a segmentação de capítulo ao
    LM, cujos itens têm numeração CONTÍNUA (não reiniciam por capítulo) e são
    resolvidos por `extract_lm`, não por `extract_capitulo`.
    """

    def _bate(self, sigla: str, slug: str, roman: str, ref_fmt) -> int:
        base = Path(ROOT) / "raw" / "kardec" / "pentateuco"
        lines = _read_lines(base / f"{slug}.md")
        rng = _find_chapter_range(base / f"{slug}.index.md", roman, None)
        self.assertIsNotNone(rng, f"{sigla} cap. {roman} não localizado")
        start, end, _part = rng
        checados = 0
        for i, n, fim in item_blocks(sigla, lines, start, end):
            bloco = "\n".join(lines[i:fim]).strip()
            verdade = literal_text(sigla, ref_fmt(roman, n))
            if verdade is None:
                continue  # locus que o cite.py declina — sem âncora, sem contrato
            self.assertEqual(
                verdade.strip(), bloco,
                f"({sigla}, {ref_fmt(roman, n)}): item_blocks e literal_text discordam "
                f"— o round-trip do publisher descartaria esta âncora",
            )
            checados += 1
        return checados

    def test_contrato_ese_capitulo(self):
        n = self._bate("ESE", "evangelho-segundo-o-espiritismo", "XVII",
                       lambda r, i: f"cap. {r}, item {i}")
        self.assertGreater(n, 3)

    def test_contrato_genese_capitulo_com_transcricao_biblica(self):
        # Cap. XII é o pior caso (versículos bíblicos + tabela comparativa).
        n = self._bate("Genese", "genese", "XII", lambda r, i: f"cap. {r}, item {i}")
        self.assertGreaterEqual(n, 20)

    def test_contrato_lm_numeracao_continua(self):
        # LM não reinicia a numeração por capítulo — a segmentação tem de seguir
        # `extract_lm`, não `extract_capitulo`.
        n = self._bate("LM", "livro-dos-mediuns", "XX", lambda r, i: f"item {i}")
        self.assertGreater(n, 3)


if __name__ == "__main__":
    unittest.main()
