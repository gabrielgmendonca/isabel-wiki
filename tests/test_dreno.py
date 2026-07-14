"""Testes do dreno — o contrapeso que fecha os rascunhos que o /critica abre.

`unittest` puro, sem pytest: o CI (`lint-pr.yml`) roda `python3 -m unittest
discover -s tests` num runner sem dependências instaladas. Um `import pytest`
aqui derrubaria o CI de TODO pull request.

Cobrem os invariantes descobertos ao desenhar o loop:

  1. Promover NÃO bumpa `atualizado_em` — se bumpasse, a página casaria o motivo
     "atualizado-apos-critica" do critica_scope e voltaria à fila do Opus, onde
     tem ~92% de chance de ser diferida de novo. Moto-perpétuo queimando tokens.
  2. Slug ambíguo (mesmo nome em 2 diretórios) NUNCA promove — falha para o lado
     seguro em vez de promover a página errada.
  3. O `[x]` do ROADMAP §11 vence o `content_sha` — resolver um diferido exige
     editar a página, então hash divergente ali é sintoma de sucesso, não risco.
  4. O agente do nível 1 só promove o bucket A — nunca uma página com diferido
     doutrinário em aberto.
"""
from __future__ import annotations

import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location(
    "dreno", ROOT / ".claude/skills/dreno/scripts/dreno.py"
)
dreno = importlib.util.module_from_spec(_spec)
sys.modules["dreno"] = dreno
_spec.loader.exec_module(dreno)


PAGE = """\
---
titulo: Página de Teste
tipo: conceito
status: rascunho
atualizado_em: 2026-06-03
---

Corpo da página, com uma citação (LE, q. 150).
"""


class TempPageMixin(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def page(self, body: str = PAGE, name: str = "pagina.md") -> Path:
        p = self.tmp / name
        p.write_text(body, encoding="utf-8")
        return p


# ── invariante 1: promoção não toca em atualizado_em ─────────────────────────

class TestPromote(TempPageMixin):
    def test_troca_status_e_preserva_atualizado_em(self):
        p = self.page()
        sha_antes = dreno.body_sha(p)

        self.assertTrue(dreno.promote(p))

        texto = p.read_text(encoding="utf-8")
        self.assertIn("status: ativo", texto)
        self.assertNotIn("status: rascunho", texto)
        # o invariante que impede o moto-perpétuo:
        self.assertIn("atualizado_em: 2026-06-03", texto)
        # e o corpo é byte-idêntico — o veredito da crítica continua válido:
        self.assertEqual(dreno.body_sha(p), sha_antes)

    def test_preserva_o_resto_do_frontmatter_e_do_corpo(self):
        p = self.page()
        dreno.promote(p)
        texto = p.read_text(encoding="utf-8")
        self.assertIn("titulo: Página de Teste", texto)
        self.assertIn("tipo: conceito", texto)
        self.assertIn("Corpo da página, com uma citação (LE, q. 150).", texto)

    def test_recusa_pagina_sem_frontmatter(self):
        p = self.page("só corpo, sem frontmatter\n", name="sem-fm.md")
        self.assertFalse(dreno.promote(p))

    def test_nao_confunde_status_no_corpo_com_status_do_frontmatter(self):
        """`status:` mencionado no CORPO não deve ser reescrito."""
        corpo = PAGE + "\nA página discute o campo `status: rascunho` do frontmatter.\n"
        p = self.page(corpo)
        dreno.promote(p)
        texto = p.read_text(encoding="utf-8")
        self.assertIn("status: ativo", texto.split("---")[1])       # frontmatter trocado
        self.assertIn("`status: rascunho` do frontmatter", texto)   # corpo intacto


# ── invariante 2: parsing do §11 e slug ambíguo ──────────────────────────────

ROADMAP_FAKE = """\
## 11. Crítica profunda — itens diferidos

### conceitos/
- [ ] **wiki/conceitos/espirito** (cit; 2) — item aberto, caminho explícito.
- [x] **wiki/conceitos/purgatorio** (tag; 1) — item fechado, caminho explícito.
- [x] **esquecimento-do-passado** (tag; 1) — item fechado, slug nu.
- [ ] **reencarnacao** (cit; 1) — item aberto, slug AMBÍGUO (2 diretórios).

## 12. Outra seção
- [ ] **nao-deve-entrar** — fora do §11.
"""

SLUGS_FAKE = {
    "espirito": ["wiki/conceitos/espirito.md"],
    "purgatorio": ["wiki/conceitos/purgatorio.md"],
    "esquecimento-do-passado": ["wiki/questoes/esquecimento-do-passado.md"],
    # o caso real: mesmo slug em dois diretórios
    "reencarnacao": [
        "wiki/conceitos/reencarnacao.md",
        "wiki/aprofundamentos/reencarnacao.md",
    ],
    "nao-deve-entrar": ["wiki/conceitos/nao-deve-entrar.md"],
}


class TestRoadmapParsing(unittest.TestCase):
    def test_aceita_os_dois_formatos_de_item(self):
        items = dreno.parse_roadmap_items(ROADMAP_FAKE, SLUGS_FAKE)
        self.assertEqual(items["wiki/conceitos/espirito.md"], {"abertos": 1, "fechados": 0})
        self.assertEqual(items["wiki/conceitos/purgatorio.md"], {"abertos": 0, "fechados": 1})
        # slug nu resolvido via índice
        self.assertEqual(
            items["wiki/questoes/esquecimento-do-passado.md"], {"abertos": 0, "fechados": 1}
        )

    def test_ignora_secoes_fora_do_11(self):
        items = dreno.parse_roadmap_items(ROADMAP_FAKE, SLUGS_FAKE)
        self.assertNotIn("wiki/conceitos/nao-deve-entrar.md", items)

    def test_slug_ambiguo_bloqueia_TODAS_as_candidatas(self):
        """Um item aberto com slug ambíguo é atribuído a todas as páginas
        homônimas, de modo que nenhuma delas seja promovida por engano."""
        items = dreno.parse_roadmap_items(ROADMAP_FAKE, SLUGS_FAKE)
        self.assertEqual(items["wiki/conceitos/reencarnacao.md"]["abertos"], 1)
        self.assertEqual(items["wiki/aprofundamentos/reencarnacao.md"]["abertos"], 1)

    def test_secao_11_ausente_nao_libera_geral(self):
        """Se o §11 sumisse do ROADMAP, um parser ingênuo devolveria zero itens
        e TODO rascunho viraria promovível. Aqui devolve {} — e o bucket A/B
        continua barrado pelo critica-state, não pelo ROADMAP."""
        self.assertEqual(dreno.parse_roadmap_items("# Sem seção 11\n", SLUGS_FAKE), {})


# ── invariante 3: classificação em buckets ──────────────────────────────────

def _rasc(path: str, sha: str = "sha256:aaa") -> dict:
    return {"path": path, "slug": Path(path).stem, "dir": "conceitos", "sha": sha}


class TestClassify(unittest.TestCase):
    def test_bucket_A_nunca_criticada(self):
        out = dreno.classify([_rasc("wiki/conceitos/nova.md")], {"pages": {}}, {})
        self.assertEqual(out[0]["bucket"], dreno.BUCKET_NEVER)
        self.assertFalse(out[0]["promovivel"])

    def test_bucket_B_item_aberto_nao_promove(self):
        st = {"pages": {"wiki/conceitos/x.md": {"content_sha": "sha256:aaa", "deferred_count": 1}}}
        rm = {"wiki/conceitos/x.md": {"abertos": 1, "fechados": 0}}
        out = dreno.classify([_rasc("wiki/conceitos/x.md")], st, rm)
        self.assertEqual(out[0]["bucket"], dreno.BUCKET_OPEN)
        self.assertFalse(out[0]["promovivel"])

    def test_bucket_B_vence_mesmo_com_um_item_ja_fechado(self):
        """Página com 1 item fechado e 1 ainda aberto continua rascunho."""
        st = {"pages": {"wiki/conceitos/x.md": {"content_sha": "sha256:aaa", "deferred_count": 2}}}
        rm = {"wiki/conceitos/x.md": {"abertos": 1, "fechados": 1}}
        out = dreno.classify([_rasc("wiki/conceitos/x.md")], st, rm)
        self.assertEqual(out[0]["bucket"], dreno.BUCKET_OPEN)
        self.assertFalse(out[0]["promovivel"])

    def test_bucket_C_item_fechado_promove_MESMO_com_corpo_alterado(self):
        """Resolver o diferido exigiu editar a página, então o hash diverge — e
        ainda assim ela deve ser promovida. O ROADMAP vence o hash."""
        st = {
            "pages": {
                "wiki/conceitos/x.md": {"content_sha": "sha256:ANTIGO", "deferred_count": 1}
            }
        }
        rm = {"wiki/conceitos/x.md": {"abertos": 0, "fechados": 1}}
        out = dreno.classify([_rasc("wiki/conceitos/x.md", sha="sha256:NOVO")], st, rm)
        self.assertEqual(out[0]["bucket"], dreno.BUCKET_DONE)
        self.assertTrue(out[0]["promovivel"])
        self.assertTrue(out[0]["corpo_alterado"])

    def test_bucket_D_rastro_perdido_nao_promove(self):
        """A crítica diferiu, mas não há item no §11: alguém perdeu o rastro.
        Não promover às cegas — é caso para o humano olhar."""
        st = {"pages": {"wiki/conceitos/x.md": {"content_sha": "sha256:aaa", "deferred_count": 2}}}
        out = dreno.classify([_rasc("wiki/conceitos/x.md")], st, {})
        self.assertEqual(out[0]["bucket"], dreno.BUCKET_LOST)
        self.assertFalse(out[0]["promovivel"])

    def test_bucket_E_zero_diferidos_promove(self):
        st = {"pages": {"wiki/conceitos/x.md": {"content_sha": "sha256:aaa", "deferred_count": 0}}}
        out = dreno.classify([_rasc("wiki/conceitos/x.md")], st, {})
        self.assertEqual(out[0]["bucket"], dreno.BUCKET_CLEAN)
        self.assertTrue(out[0]["promovivel"])

    def test_bucket_E_com_deferred_count_ausente(self):
        """Entrada de estado antiga, sem o campo `deferred_count`."""
        st = {"pages": {"wiki/conceitos/x.md": {"content_sha": "sha256:aaa"}}}
        out = dreno.classify([_rasc("wiki/conceitos/x.md")], st, {})
        self.assertEqual(out[0]["bucket"], dreno.BUCKET_CLEAN)

    def test_bucket_X_criticada_limpa_mas_corpo_mudou_depois(self):
        """Sem item no §11, o `content_sha` é a única evidência — e um corpo novo
        invalida o veredito 'zero diferidos'. Volta para a fila da crítica."""
        st = {
            "pages": {
                "wiki/conceitos/x.md": {"content_sha": "sha256:ANTIGO", "deferred_count": 0}
            }
        }
        out = dreno.classify([_rasc("wiki/conceitos/x.md", sha="sha256:NOVO")], st, {})
        self.assertEqual(out[0]["bucket"], dreno.BUCKET_STALE)
        self.assertFalse(out[0]["promovivel"])


# ── completude: as DUAS formas de citação do projeto ────────────────────────

class TestCompletude(TempPageMixin):
    def test_conta_citacao_por_sigla(self):
        p = self.page()  # corpo tem "(LE, q. 150)"
        self.assertEqual(dreno.completude(p)["citacoes"], 1)

    def test_conta_citacao_por_obra_em_italico(self):
        """Regressão: contar só as siglas do Pentateuco rotulava como 'esboço'
        toda página de personalidade/obra — que cita `(Autor, *Obra*, cap.)`.
        Foi o que aconteceu com clarencio.md (704 palavras, Fontes, 7 citações)."""
        p = self.page(
            PAGE.replace(
                "Corpo da página, com uma citação (LE, q. 150).",
                "Clarêncio orienta o recém-chegado "
                "(Clarêncio a André Luiz, *Nosso Lar*, cap. 12).",
            )
        )
        self.assertEqual(dreno.completude(p)["citacoes"], 1)

    def test_detecta_fontes_e_secoes(self):
        p = self.page(PAGE + "\n## Fontes\n\n- LE\n")
        c = dreno.completude(p)
        self.assertTrue(c["tem_fontes"])
        self.assertEqual(c["tem_secoes"], 1)


class TestTriagem(TempPageMixin):
    def test_separa_esboco_de_candidata(self):
        wiki = self.tmp / "wiki"
        wiki.mkdir()
        (wiki / "completa.md").write_text(
            "---\nstatus: rascunho\n---\n\n"
            + "palavra " * 300
            + "\n\n(LE, q. 150)\n\n## Fontes\n\n- LE\n",
            encoding="utf-8",
        )
        (wiki / "stub.md").write_text(
            "---\nstatus: rascunho\n---\n\nesboço curto.\n", encoding="utf-8"
        )

        original_root = dreno.ROOT
        dreno.ROOT = self.tmp
        try:
            rascunhos = [
                {
                    "path": "wiki/completa.md",
                    "bucket": dreno.BUCKET_NEVER,
                    "atualizado_em": "2026-01-01",
                },
                {
                    "path": "wiki/stub.md",
                    "bucket": dreno.BUCKET_NEVER,
                    "atualizado_em": "2026-01-02",
                },
                # bucket B não entra na triagem — é dívida da crítica, não do /ingest
                {
                    "path": "wiki/completa.md",
                    "bucket": dreno.BUCKET_OPEN,
                    "atualizado_em": "2026-01-03",
                },
            ]
            t = dreno.triagem_bucket_a(rascunhos)
        finally:
            dreno.ROOT = original_root

        self.assertEqual([r["path"] for r in t["candidata"]], ["wiki/completa.md"])
        self.assertEqual([r["path"] for r in t["esboco"]], ["wiki/stub.md"])


# ── invariante 4: o agente do nível 1 só alcança o bucket A ─────────────────

class TestPromoverPagina(TempPageMixin):
    """`promover-pagina` é a ferramenta do agente editorial do nível 1. Ela
    precisa RECUSAR qualquer página fora do bucket A — sobretudo o bucket B,
    onde há divergência doutrinária ainda em aberto. Um agente que julga
    completude editorial não tem autoridade para liberar isso."""

    def _com_estado(self, bucket_de: dict, rm: dict):
        """Monta um build_report() falso com uma única página no bucket dado."""
        rasc = {
            "path": "wiki/conceitos/x.md",
            "slug": "x",
            "dir": "conceitos",
            "atualizado_em": "2026-06-03",
            "sha": "sha256:aaa",
        }
        classificados = dreno.classify([dict(rasc)], bucket_de, rm)
        return {"rascunhos": classificados}

    def test_recusa_bucket_B_diferido_doutrinario_aberto(self):
        st = {"pages": {"wiki/conceitos/x.md": {"content_sha": "sha256:aaa", "deferred_count": 1}}}
        rm = {"wiki/conceitos/x.md": {"abertos": 1, "fechados": 0}}
        rep = self._com_estado(st, rm)

        original = dreno.build_report
        dreno.build_report = lambda: rep
        try:
            args = type("A", (), {"path": "wiki/conceitos/x.md"})()
            rc = dreno.cmd_promover_pagina(args)
        finally:
            dreno.build_report = original

        self.assertEqual(rc, 3, "bucket B jamais pode ser promovido pelo agente editorial")

    def test_recusa_pagina_que_nao_e_rascunho(self):
        original = dreno.build_report
        dreno.build_report = lambda: {"rascunhos": []}
        try:
            args = type("A", (), {"path": "wiki/conceitos/inexistente.md"})()
            rc = dreno.cmd_promover_pagina(args)
        finally:
            dreno.build_report = original
        self.assertEqual(rc, 2)


# ── guarda de dry-run compartilhada com o /critica ───────────────────────────

class TestDryRun(unittest.TestCase):
    def test_ativo_via_env(self):
        os.environ["CRITICA_DRYRUN"] = "1"
        try:
            self.assertTrue(dreno.dry_run_active())
        finally:
            del os.environ["CRITICA_DRYRUN"]

    def test_inativo_por_default(self):
        os.environ.pop("CRITICA_DRYRUN", None)
        original = dreno.DRYRUN_SENTINEL
        dreno.DRYRUN_SENTINEL = Path("/nao/existe/.dryrun")
        try:
            self.assertFalse(dreno.dry_run_active())
        finally:
            dreno.DRYRUN_SENTINEL = original


if __name__ == "__main__":
    unittest.main()
