"""Dreno — contrapeso do /critica: fecha rascunhos em vez de abrir.

O `/critica` (e seu wrapper em loop, `/autocritica`) rebaixa a `rascunho` toda
página cujo achado doutrinário foi diferido a decisão humana, e anota o item no
ROADMAP §11. Sem um dreno, o loop só acumula: hoje há ~158 rascunhos e ~133
itens abertos no §11.

Este script é o lado determinístico do dreno (zero tokens). Ele cruza três
fontes de verdade e diz, para cada rascunho, POR QUE ele é rascunho:

  1. `wiki/**/*.md` com `status: rascunho`
  2. `.claude/skills/critica/state/critica-state.json` — o que a crítica já viu
  3. `ROADMAP.md` §11 — os itens diferidos, abertos `[ ]` vs fechados `[x]`

Buckets:
  A  nunca-criticada        — rascunho de outra origem (/ingest); NÃO é dívida
                              da crítica. Precisa de julgamento de completude.
  B  diferido-aberto        — há item `[ ]` no §11. `rascunho` está CORRETO.
  C  diferido-fechado       — todos os itens do §11 estão `[x]`. → PROMOVER
  D  rastro-perdido         — a crítica diferiu, mas não há item no §11.
  E  sem-diferidos          — criticada, zero diferidos, mas ficou rascunho. → PROMOVER
  X  corpo-alterado         — o corpo mudou depois da crítica; o veredito está
                              obsoleto. Não promover: devolver à fila da crítica.

`promover` aplica só os buckets C e E.

Duas decisões de projeto, deliberadas:

  * NÃO bumpa `atualizado_em`. Promover rascunho→ativo é transição de estado de
    REVISÃO, não revisão de CONTEÚDO — e o `content_sha` prova que o corpo é
    byte-idêntico ao que foi criticado. Bumpar faria a página casar o motivo
    "atualizado-apos-critica" do `critica_scope.py` e voltar à fila do Opus,
    onde tem ~92% de chance de ser diferida de novo → rascunho outra vez.
    Isso é um moto-perpétuo que queima tokens sem mudar uma linha da wiki.
    (Difere de `critica_apply.py set-status`, que bumpa — lá é correto, porque
    o `record` subsequente sincroniza o estado.)

  * Slug ambíguo NUNCA é promovido. O §11 tem itens em dois formatos:
    `**wiki/conceitos/x**` (caminho, não-ambíguo) e `**x**` (slug nu). Há slugs
    repetidos entre diretórios (`reencarnacao`, `alma-dos-animais`,
    `plenitude`), então um slug nu pode casar mais de uma página. Nesse caso o
    item é marcado AMBÍGUO em todas as candidatas, e o bucket F barra as duas.

    Contar só `abertos`/`fechados` não bastava, e a assimetria era sutil: o
    fan-out de um item ABERTO soma `abertos` em todas as homônimas e bloqueia
    todas (seguro), mas o de um item FECHADO soma `fechados` em todas — e
    `fechados > 0` é justamente a condição de PROMOVER. O mesmo mecanismo
    vendido como salvaguarda virava amplificador: um único `[x]` humano,
    dirigido a UMA página, promovia TODAS as homônimas. Pior, a promovida por
    engano nunca mais voltava à fila da crítica (o `content_sha` bate e o
    `atualizado_em` não é bumpado ⇒ `critica_scope._due_reason()` devolve None),
    ficando `ativo` para sempre com diferidos doutrinários jamais resolvidos.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _lib.wiki_utils import parse_frontmatter  # noqa: E402

ROOT = Path(__file__).resolve().parents[4]
WIKI = ROOT / "wiki"
ROADMAP_PATH = ROOT / "ROADMAP.md"
STATE_PATH = ROOT / ".claude/skills/critica/state/critica-state.json"

# Herda o sentinela do /critica: se um dry-run está ativo lá, nada é escrito aqui.
DRYRUN_SENTINEL = ROOT / ".claude/skills/critica/state/.dryrun"

ROADMAP_SECTION = "## 11."
ROADMAP_NEXT = "\n## 12."

# `tipo`s que o critica_scope.py também ignora — capítulos/índices bíblicos não
# entram no fluxo de rascunho→ativo.
SKIP_TIPOS = {"biblia", "biblia-indice", "biblia-capitulo"}

BUCKET_NEVER = "A. nunca-criticada (origem: /ingest — não é dívida da crítica)"
BUCKET_OPEN = "B. diferido ABERTO no §11 (rascunho correto — não tocar)"
BUCKET_DONE = "C. diferido FECHADO no §11 (promover)"
BUCKET_LOST = "D. crítica diferiu, sem item no §11 (rastro perdido)"
BUCKET_CLEAN = "E. criticada, zero diferidos (promover)"
BUCKET_AMBIG = "F. item do §11 por slug AMBÍGUO (casa >1 página — não promove)"
BUCKET_STALE = "X. corpo alterado após a crítica (veredito obsoleto — recriticar)"

PROMOTABLE = {BUCKET_DONE, BUCKET_CLEAN}


def dry_run_active() -> bool:
    return bool(os.environ.get("CRITICA_DRYRUN")) or DRYRUN_SENTINEL.exists()


def body_sha(path: Path) -> str:
    """sha256 do corpo, excluindo o frontmatter. Idêntico ao critica_scope.py —
    é o que permite promover sem invalidar o estado da crítica."""
    import hashlib

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    body = text
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                body = "\n".join(lines[i + 1:])
                break
    return "sha256:" + hashlib.sha256(body.encode("utf-8")).hexdigest()


def load_state() -> dict:
    if not STATE_PATH.exists():
        return {"pages": {}}
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def collect_rascunhos() -> list[dict]:
    out = []
    for md in sorted(WIKI.rglob("*.md")):
        fm, _ = parse_frontmatter(md)
        if str(fm.get("status", "")).strip() != "rascunho":
            continue
        if str(fm.get("tipo", "")).strip() in SKIP_TIPOS:
            continue
        rel = md.relative_to(ROOT)
        out.append({
            "path": str(rel),
            "slug": md.stem,
            "dir": rel.parts[1] if len(rel.parts) > 2 else "",
            "titulo": str(fm.get("titulo", "") or ""),
            "atualizado_em": str(fm.get("atualizado_em", "") or ""),
            "sha": body_sha(md),
        })
    return out


def _slug_index() -> dict[str, list[str]]:
    """slug → [caminhos]. Mais de um caminho ⇒ slug ambíguo."""
    idx: dict[str, list[str]] = defaultdict(list)
    for md in WIKI.rglob("*.md"):
        idx[md.stem].append(str(md.relative_to(ROOT)))
    return idx


def parse_roadmap_items(
    text: str | None = None, slugs: dict[str, list[str]] | None = None
) -> dict[str, dict[str, int]]:
    """Devolve {caminho_da_pagina: {"abertos": n, "fechados": n, "ambiguos": n}}.

    Aceita os dois formatos de item do §11:
      - [ ] **wiki/conceitos/espirito** (…)   → caminho explícito
      - [x] **esquecimento-do-passado** (…)   → slug nu

    Slug nu ambíguo (casa >1 página) é atribuído a TODAS as candidatas E marcado
    em `ambiguos`. Só o fan-out não basta para barrar: um item ABERTO ambíguo
    soma `abertos` em todas (e `abertos > 0` bloqueia), mas um item FECHADO
    ambíguo somaria `fechados` em todas — e `fechados > 0` é a condição de
    PROMOVER. É o contador `ambiguos` que torna o bloqueio simétrico nas duas
    marcas, que é o que o dreno promete.
    """
    if text is None:
        text = ROADMAP_PATH.read_text(encoding="utf-8")
    if ROADMAP_SECTION not in text:
        return {}
    sec = text.split(ROADMAP_SECTION, 1)[1].split(ROADMAP_NEXT, 1)[0]

    if slugs is None:
        slugs = _slug_index()
    items: dict[str, dict[str, int]] = defaultdict(
        lambda: {"abertos": 0, "fechados": 0, "ambiguos": 0}
    )

    for mark, ref in re.findall(r"^- \[( |x)\] \*\*([^*]+)\*\*", sec, re.M):
        ref = ref.strip()
        key = "fechados" if mark == "x" else "abertos"
        if "/" in ref:
            targets = [ref if ref.endswith(".md") else f"{ref}.md"]
        else:
            targets = slugs.get(ref, [])
        for t in targets:
            items[t][key] += 1
            if len(targets) > 1:
                items[t]["ambiguos"] += 1
    return dict(items)


def classify(rascunhos: list[dict], state: dict, roadmap: dict) -> list[dict]:
    spages = state.get("pages", {})
    for r in rascunhos:
        st = spages.get(r["path"])
        rm = roadmap.get(r["path"], {})
        r["itens_abertos"] = rm.get("abertos", 0)
        r["itens_fechados"] = rm.get("fechados", 0)
        r["itens_ambiguos"] = rm.get("ambiguos", 0)

        r["corpo_alterado"] = st is not None and st.get("content_sha") != r["sha"]

        if st is None:
            r["bucket"] = BUCKET_NEVER
        elif r["itens_abertos"] > 0:
            r["bucket"] = BUCKET_OPEN
        elif r["itens_ambiguos"] > 0:
            # Todo item desta página vem de slug nu que casa >1 homônima. Não dá
            # para saber se o `[x]` era para ELA ou para a irmã — e promover a
            # errada é irreversível na prática: o corpo não muda, então o
            # `content_sha` continua batendo e ela nunca mais volta à fila da
            # crítica. Barrar é o único lado seguro; o conserto é humano (trocar
            # o slug nu por caminho explícito no §11).
            r["bucket"] = BUCKET_AMBIG
        elif r["itens_fechados"] > 0:
            # O checkbox `[x]` do §11 é a assinatura HUMANA de que o diferido foi
            # resolvido — e resolvê-lo exige justamente editar a página. Por isso
            # o `content_sha` divergente aqui é sintoma de sucesso, não de risco:
            # o ROADMAP vence o hash. (O hash só decide no bucket E, abaixo, onde
            # "zero diferidos" é a única evidência e um corpo novo a invalida.)
            r["bucket"] = BUCKET_DONE
        elif st.get("deferred_count", 0) > 0:
            r["bucket"] = BUCKET_LOST
        elif r["corpo_alterado"]:
            r["bucket"] = BUCKET_STALE
        else:
            r["bucket"] = BUCKET_CLEAN
        r["promovivel"] = r["bucket"] in PROMOTABLE
    return rascunhos


def promote(path: Path) -> bool:
    """status: rascunho → ativo, SEM tocar em atualizado_em (ver docstring)."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return False
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    else:
        return False

    changed = False
    for j in range(1, end):
        if re.match(r"^status\s*:", lines[j]):
            lines[j] = "status: ativo"
            changed = True
            break
    if not changed:
        return False
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return True


# ─── triagem do bucket A (rascunhos do /ingest) ──────────────────────────────
#
# Os 78 rascunhos nunca-criticados não são dívida da crítica: são páginas que o
# /ingest deixou como rascunho e ninguém promoveu (ROADMAP §10.3). Promovê-las
# exige julgar completude — mas a maior parte desse julgamento é determinística.
# Só o resíduo ambíguo merece um agente barato.

# As DUAS formas de citação do projeto (CLAUDE.md §3). Contar só a primeira
# rotularia como "esboço" toda página de personalidade/obra, que cita por obra:
#   sigla → (LE, q. 150) · (ESE, cap. XVII, item 4)
#   obra  → (Emmanuel / Chico Xavier, *O Consolador*, q. 123)
CITE_SIGLA_RE = re.compile(r"\((?:LE|LM|ESE|C&I|Gênese|OPE|OQE|RE)[,.]", re.I)
CITE_OBRA_RE = re.compile(r"\([^)]*\*[^*)]+\*[^)]*\)")
STUB_PALAVRAS = 250  # abaixo disso é esboço, não página


def completude(path: Path) -> dict:
    """Sinais determinísticos de que uma página está pronta para `ativo`."""
    text = path.read_text(encoding="utf-8")
    body = text.split("---", 2)[-1] if text.startswith("---") else text
    return {
        "palavras": len(body.split()),
        "citacoes": len(CITE_SIGLA_RE.findall(body)) + len(CITE_OBRA_RE.findall(body)),
        "tem_fontes": bool(re.search(r"^##\s+Fontes", body, re.M)),
        "tem_secoes": len(re.findall(r"^##\s+", body, re.M)),
    }


def triagem_bucket_a(rascunhos: list[dict]) -> dict:
    """Separa os rascunhos do /ingest em: esboço (precisa de escrita) vs
    candidata (parece completa — um agente barato confirma e promove)."""
    esboco, candidata = [], []
    for r in rascunhos:
        if r["bucket"] != BUCKET_NEVER:
            continue
        c = completude(ROOT / r["path"])
        r["completude"] = c
        pronta = c["tem_fontes"] and c["palavras"] >= STUB_PALAVRAS and c["citacoes"] >= 1
        (candidata if pronta else esboco).append(r)
    # mais antigas primeiro — o backlog mais parado é o que primeiro drena
    esboco.sort(key=lambda r: r["atualizado_em"] or "0000-00-00")
    candidata.sort(key=lambda r: r["atualizado_em"] or "0000-00-00")
    return {"esboco": esboco, "candidata": candidata}


def cmd_triagem(args) -> int:
    rep = build_report()
    t = triagem_bucket_a(rep["rascunhos"])
    if args.format == "json":
        out = {k: v[: args.limit] if args.limit else v for k, v in t.items()}
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0

    print(f"Dreno — triagem do bucket A ({len(t['esboco']) + len(t['candidata'])} rascunhos do /ingest)\n")
    print(f"  {len(t['candidata']):3d}  CANDIDATA a `ativo` (tem Fontes, ≥{STUB_PALAVRAS} palavras, ≥1 citação)")
    for r in t["candidata"][: args.limit or 10]:
        c = r["completude"]
        print(f"       - {r['path']}  ({c['palavras']}p, {c['citacoes']} cit, {c['tem_secoes']} seções)")
    print(f"\n  {len(t['esboco']):3d}  ESBOÇO — precisa de escrita, não de promoção")
    for r in t["esboco"][: args.limit or 10]:
        c = r["completude"]
        falta = []
        if not c["tem_fontes"]:
            falta.append("sem ## Fontes")
        if c["palavras"] < STUB_PALAVRAS:
            falta.append(f"{c['palavras']}p")
        if not c["citacoes"]:
            falta.append("0 citações")
        print(f"       - {r['path']}  ({', '.join(falta)})")
    return 0


def build_report() -> dict:
    rascunhos = classify(collect_rascunhos(), load_state(), parse_roadmap_items())
    buckets: dict[str, list[dict]] = defaultdict(list)
    for r in rascunhos:
        buckets[r["bucket"]].append(r)
    return {
        "total_rascunhos": len(rascunhos),
        "promoviveis": sum(1 for r in rascunhos if r["promovivel"]),
        "buckets": {k: buckets[k] for k in sorted(buckets)},
        "rascunhos": rascunhos,
    }


def cmd_anatomia(args) -> int:
    rep = build_report()
    if args.format == "json":
        print(json.dumps(rep, ensure_ascii=False, indent=2))
        return 0

    print(f"Dreno — anatomia dos rascunhos ({rep['total_rascunhos']} no total)\n")
    for name, items in rep["buckets"].items():
        by_dir = defaultdict(int)
        for it in items:
            by_dir[it["dir"]] += 1
        dirs = ", ".join(f"{d}:{n}" for d, n in sorted(by_dir.items(), key=lambda x: -x[1]))
        print(f"  {len(items):3d}  {name}")
        print(f"       {dirs}")
    print(f"\n  → promovíveis agora (buckets C+E): {rep['promoviveis']}")
    if rep["promoviveis"]:
        for r in rep["rascunhos"]:
            if r["promovivel"]:
                print(f"       - {r['path']}")
    return 0


def cmd_promover(args) -> int:
    rep = build_report()
    alvos = [r for r in rep["rascunhos"] if r["promovivel"]]
    if args.limit:
        alvos = alvos[: args.limit]

    if not alvos:
        print("Dreno: nada promovível (0 páginas). Backlog seguro está vazio.")
        return 0

    dry = args.dry_run or dry_run_active()
    if dry:
        print(f"Dreno [DRY-RUN]: {len(alvos)} página(s) seriam promovidas a `ativo`:")
        for r in alvos:
            print(f"  - {r['path']}  ({r['bucket'][:1]}; §11 fechados: {r['itens_fechados']})")
        return 0

    done = 0
    for r in alvos:
        if promote(ROOT / r["path"]):
            done += 1
            print(f"  ✓ ativo  {r['path']}")
        else:
            print(f"  ✗ falhou {r['path']} (frontmatter inesperado)", file=sys.stderr)
    print(f"\nDreno: {done} página(s) promovidas a `ativo` (atualizado_em preservado).")
    return 0


def cmd_promover_pagina(args) -> int:
    """Promove UMA página nomeada — a ferramenta segura para o agente do nível 1.

    Existe para tirar o footgun da mão do agente: sem ela, a única forma de ele
    promover uma página do bucket A seria editar o frontmatter na mão (podendo
    bumpar `atualizado_em` sem querer) ou chamar `critica_apply.py set-status`,
    que bumpa por design. Ambos devolveriam a página à fila do Opus.

    Recusa qualquer página fora do bucket A: o agente do nível 1 julga completude
    EDITORIAL, e não tem autoridade para liberar página com diferido doutrinário
    em aberto (bucket B) nem com veredito obsoleto (bucket X).
    """
    path = Path(args.path)
    rel = str(path.relative_to(ROOT) if path.is_absolute() else path)

    if dry_run_active():
        print(f"[DRY-RUN] {rel} não foi promovida (sentinela de dry-run ativo).")
        return 0

    alvo = next((r for r in build_report()["rascunhos"] if r["path"] == rel), None)
    if alvo is None:
        print(f"erro: {rel} não é um rascunho (ou não existe).", file=sys.stderr)
        return 2
    if alvo["bucket"] != BUCKET_NEVER:
        print(
            f"erro: {rel} está no bucket «{alvo['bucket']}» — fora do alcance do nível 1.\n"
            "       O agente editorial só promove o bucket A (rascunho do /ingest).",
            file=sys.stderr,
        )
        return 3

    if promote(ROOT / rel):
        print(f"  ✓ ativo  {rel}  (atualizado_em preservado)")
        return 0
    print(f"erro: frontmatter inesperado em {rel}", file=sys.stderr)
    return 4


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Dreno — fecha rascunhos que a crítica abriu.")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("anatomia", help="Classifica os rascunhos por origem (não escreve).")
    a.add_argument("--format", choices=("summary", "json"), default="summary")
    a.set_defaults(func=cmd_anatomia)

    pr = sub.add_parser("promover", help="Promove a `ativo` os rascunhos seguros (buckets C+E).")
    pr.add_argument("--limit", type=int, default=0, metavar="N")
    pr.add_argument("--dry-run", action="store_true")
    pr.set_defaults(func=cmd_promover)

    tr = sub.add_parser("triagem", help="Bucket A (rascunhos do /ingest): esboço vs candidata.")
    tr.add_argument("--limit", type=int, default=0, metavar="N")
    tr.add_argument("--format", choices=("summary", "json"), default="summary")
    tr.set_defaults(func=cmd_triagem)

    pp = sub.add_parser(
        "promover-pagina",
        help="Promove UMA página do bucket A (ferramenta segura do agente do nível 1).",
    )
    pp.add_argument("--path", required=True, metavar="wiki/…/pagina.md")
    pp.set_defaults(func=cmd_promover_pagina)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
