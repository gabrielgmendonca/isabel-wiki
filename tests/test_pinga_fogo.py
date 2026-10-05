"""Testes de scripts/pinga_fogo.py (conferência de falas) e scripts/embed_youtube_clips.py."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import pinga_fogo as pf  # noqa: E402
from embed_youtube_clips import converter  # noqa: E402

FRASES = {
    "I": [
        {"t": 100, "turno": 90, "linha": 1, "falante": "Almir Guimarães", "texto": "Qual é a sua pergunta, Chico?"},
        {"t": 120, "turno": 118, "linha": 3, "falante": "Chico Xavier",
         "texto": "A mediunidade não nos isenta, com privilégios especiais, com respeito à desencarnação."},
        {"t": 140, "turno": 118, "linha": 3, "falante": "Chico Xavier",
         "texto": "Que os bons espíritos me livrem de mim mesmo."},
    ],
    "II": [],
}


def pagina(texto: str) -> Path:
    f = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8")
    f.write(texto)
    f.close()
    return Path(f.name)


class TestEmbed(unittest.TestCase):
    def test_embed_com_tempo_vira_iframe_com_start(self):
        out, n = converter("![Pinga-Fogo I, 0:02:00](https://www.youtube.com/watch?v=v5waIS1qedA&t=120s)")
        self.assertEqual(n, 1)
        self.assertIn('src="https://www.youtube-nocookie.com/embed/v5waIS1qedA?start=120', out)
        self.assertIn('loading="lazy"', out)

    def test_embed_sem_tempo_fica_para_o_quartz(self):
        src = "![](https://www.youtube.com/watch?v=v5waIS1qedA)"
        self.assertEqual(converter(src), (src, 0))

    def test_end_opcional(self):
        out, _ = converter("![x](https://www.youtube.com/watch?v=v5waIS1qedA&t=10s&end=40)")
        self.assertIn("start=10&amp;end=40", out)

    def test_bloco_de_codigo_intocado(self):
        src = "```\n![x](https://www.youtube.com/watch?v=v5waIS1qedA&t=10s)\n```"
        self.assertEqual(converter(src)[1], 0)


class TestChecar(unittest.TestCase):
    def test_localizar_ignora_acento_e_pontuacao(self):
        achou = pf.localizar("I", "mediunidade nao nos isenta com privilegios", FRASES["I"])
        self.assertEqual([f["t"] for f in achou], [120])

    def test_fala_literal_com_tempo_certo_passa(self):
        p = pagina('> [!quote] Chico Xavier, *Pinga-Fogo I*, 0:02:00\n'
                   '> "A mediunidade não nos isenta (...) com respeito à desencarnação."\n\n'
                   '![Pinga-Fogo I, 0:02:00](https://www.youtube.com/watch?v=v5waIS1qedA&t=120s)\n')
        self.assertEqual(pf.checar_arquivo(p, FRASES), [])

    def test_tempo_do_turno_tambem_vale(self):
        p = pagina('> [!quote] Chico Xavier, *Pinga-Fogo I*, 0:01:58\n> "Que os bons espíritos me livrem de mim mesmo."\n')
        self.assertEqual(pf.checar_arquivo(p, FRASES), [])

    def test_fala_inventada_e_apontada(self):
        p = pagina('> [!quote] Chico Xavier, *Pinga-Fogo I*, 0:02:00\n> "A mediunidade concede privilégios aos médiuns."\n')
        erros = pf.checar_arquivo(p, FRASES)
        self.assertEqual(len(erros), 1)
        self.assertIn("não está na transcrição", erros[0])

    def test_tempo_errado_e_apontado(self):
        p = pagina('> [!quote] Chico Xavier, *Pinga-Fogo I*, 0:10:00\n> "Que os bons espíritos me livrem de mim mesmo."\n')
        self.assertIn("não bate", pf.checar_arquivo(p, FRASES)[0])

    def test_embed_fora_de_fala_de_chico_e_apontado(self):
        p = pagina("![x](https://www.youtube.com/watch?v=v5waIS1qedA&t=95s)\n")
        self.assertIn("não cai numa fala de Chico", pf.checar_arquivo(p, FRASES)[0])

    def test_aspa_no_corpo_com_tempo_e_conferida(self):
        ok = pagina('Chico diz que "os bons espíritos me livrem de mim mesmo" (0:02:20).\n')
        self.assertEqual(pf.checar_arquivo(ok, FRASES), [])
        ruim = pagina('Chico diz que "os bons espíritos nos protejam sempre" (0:02:20).\n')
        self.assertIn("aspa com tempo", pf.checar_arquivo(ruim, FRASES)[0])

    def test_aspa_sem_tempo_nao_e_conferida(self):
        p = pagina('Kardec diz que "a escravidão é um abuso da força" (LE, q. 829).\n')
        self.assertEqual(pf.checar_arquivo(p, FRASES), [])

    def test_corrigir_reescreve_titulo_e_embed(self):
        p = pagina('> [!quote] Chico Xavier, *Pinga-Fogo I*, 0:10:00\n> "Que os bons espíritos me livrem de mim mesmo."\n\n'
                   '![Pinga-Fogo I, 0:10:00](https://www.youtube.com/watch?v=v5waIS1qedA&t=600s)\n')
        self.assertEqual(pf.corrigir_arquivo(p, FRASES), 1)
        texto = p.read_text(encoding="utf-8")
        self.assertIn("*Pinga-Fogo I*, 0:02:20", texto)
        self.assertIn("&t=140s", texto)
        self.assertIn("[Pinga-Fogo I, 0:02:20]", texto)
        self.assertEqual(pf.checar_arquivo(p, FRASES), [])


if __name__ == "__main__":
    unittest.main()
