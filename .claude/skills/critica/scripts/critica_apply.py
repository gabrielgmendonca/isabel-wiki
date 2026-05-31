#!/usr/bin/env python3
# Executar sempre com: uv run python .claude/skills/critica/scripts/critica_apply.py
"""Applier determinístico das correções do workflow /critica.

A regra de ouro do repo: **o script determinístico faz a mutação mecânica; o LLM
só decide.** Os agentes do /critica nunca editam frontmatter à mão (quebraria o
parser de `_lib/wiki_utils.py`) — eles chamam este applier com payloads
estruturados. Cada ação é targetada (linha + texto exato), idempotente quando
possível, e verifica a pré-condição antes de escrever (falha alta, exit 2).

Caminho SEGURO (auto-fix): add-tag, add-wikilink, replace-text (usado por
fix_locus e por substituição de terminologia), frontmatter set.

Caminho INSEGURO (diferir a humano): set-status rascunho, divergencia-stub
(status: aberta), roadmap-append. Esses NÃO corrigem doutrina — apenas marcam e
roteiam para revisão.

Toda ação que muta o CORPO ou o status de uma página bumpa `atualizado_em` para
a data corrente (a página de fato mudou); o estado em critica-state.json registra
o novo atualizado_em via `critica_scope.py record`.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _lib.wiki_utils import parse_frontmatter  # noqa: E402

ROOT = Path(__file__).resolve().parents[4]
ROADMAP_PATH = ROOT / "ROADMAP.md"
DIVERGENCIAS_DIR = ROOT / "wiki" / "divergencias"
ROADMAP_HEADING = "## 11. Crítica profunda — itens diferidos a decisão humana"
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

# Guarda determinística de dry-run: independente do prompt do agente. Ativa
# quando a env var CRITICA_DRYRUN está setada OU o sentinela existe. O SKILL
# /critica cria/remove o sentinela em torno de um run dryRun; assim, mesmo que
# um agente chame este applier, nenhuma escrita acontece.
DRYRUN_SENTINEL = Path(__file__).resolve().parents[1] / "state" / ".dryrun"


def _dry_run_active() -> bool:
    return bool(os.environ.get("CRITICA_DRYRUN")) or DRYRUN_SENTINEL.exists()


def _fail(msg: str) -> None:
    sys.stderr.write(f"erro: {msg}\n")
    raise SystemExit(2)


def _today(args) -> str:
    return getattr(args, "date", None) or date.today().isoformat()


# ─── manipulação de frontmatter (linhas cruas, preserva formatação) ──────────

def _split_frontmatter(text: str) -> tuple[list[str], list[str], list[str]]:
    """Devolve (fm_lines, body_lines, raw_lines). fm_lines exclui os `---`."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        _fail("página sem frontmatter")
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return lines[1:i], lines[i + 1:], lines
    _fail("frontmatter não fechado")


def _rebuild(fm_lines: list[str], body_lines: list[str]) -> str:
    return "---\n" + "\n".join(fm_lines) + "\n---\n" + "\n".join(body_lines).rstrip("\n") + "\n"


def _fm_set_scalar(fm_lines: list[str], key: str, value: str) -> list[str]:
    out = []
    found = False
    for ln in fm_lines:
        if re.match(rf"^{re.escape(key)}\s*:", ln):
            out.append(f"{key}: {value}")
            found = True
        else:
            out.append(ln)
    if not found:
        out.append(f"{key}: {value}")
    return out


def _fm_add_tag(fm_lines: list[str], tag: str) -> tuple[list[str], bool]:
    """Adiciona `tag` à lista `tags:` (inline `[..]` ou multilinha `- x`)."""
    out: list[str] = []
    added = False
    i = 0
    n = len(fm_lines)
    while i < n:
        ln = fm_lines[i]
        m = re.match(r"^tags\s*:\s*(.*)$", ln)
        if not m:
            out.append(ln)
            i += 1
            continue
        rest = m.group(1).strip()
        if rest.startswith("[") and rest.endswith("]"):
            inner = rest[1:-1]
            items = [t.strip() for t in inner.split(",") if t.strip()]
            if tag in items:
                out.append(ln)
            else:
                items.append(tag)
                out.append("tags: [" + ", ".join(items) + "]")
                added = True
            i += 1
        else:
            # multilinha: coletar itens `- x` subsequentes
            out.append(ln)
            i += 1
            block_items = []
            while i < n and re.match(r"^\s*-\s+", fm_lines[i]):
                block_items.append(fm_lines[i].strip()[2:].strip())
                out.append(fm_lines[i])
                i += 1
            if tag not in block_items:
                out.append(f"  - {tag}")
                added = True
        # copia o resto
        out.extend(fm_lines[i:])
        return out, added
    # sem chave tags:
    out.append(f"tags: [{tag}]")
    return out, True


def _load(path: Path) -> str:
    if not path.exists():
        _fail(f"página inexistente: {path}")
    return path.read_text(encoding="utf-8")


def _save(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


# ─── ações de página ─────────────────────────────────────────────────────────

def act_add_tag(args) -> dict:
    path = Path(args.path)
    fm, body, _ = _split_frontmatter(_load(path))
    fm, added = _fm_add_tag(fm, args.tag)
    if not added:
        return {"action": "add-tag", "path": str(path), "tag": args.tag, "changed": False}
    fm = _fm_set_scalar(fm, "atualizado_em", _today(args))
    _save(path, _rebuild(fm, body))
    return {"action": "add-tag", "path": str(path), "tag": args.tag, "changed": True}


def act_set_status(args) -> dict:
    path = Path(args.path)
    fm, body, _ = _split_frontmatter(_load(path))
    fm = _fm_set_scalar(fm, "status", args.status)
    fm = _fm_set_scalar(fm, "atualizado_em", _today(args))
    _save(path, _rebuild(fm, body))
    return {"action": "set-status", "path": str(path), "status": args.status, "changed": True}


def act_bump(args) -> dict:
    path = Path(args.path)
    fm, body, _ = _split_frontmatter(_load(path))
    fm = _fm_set_scalar(fm, "atualizado_em", _today(args))
    _save(path, _rebuild(fm, body))
    return {"action": "bump", "path": str(path), "changed": True}


def _edit_body_line(path: Path, line_no: int, transform) -> str:
    """Aplica `transform(line)->new_line` à linha 1-based `line_no` do corpo.

    A numeração de linha segue o ARQUIVO inteiro (igual ao lint/dossiê), não só
    o corpo. Retorna a linha original para conferência.
    """
    text = _load(path)
    lines = text.splitlines()
    idx = line_no - 1
    if idx < 0 or idx >= len(lines):
        _fail(f"linha {line_no} fora do arquivo {path} ({len(lines)} linhas)")
    original = lines[idx]
    new_line = transform(original)
    if new_line == original:
        return original
    lines[idx] = new_line
    # bump atualizado_em via reparse do frontmatter
    fm, body, _ = _split_frontmatter("\n".join(lines) + "\n")
    fm = _fm_set_scalar(fm, "atualizado_em", date.today().isoformat())
    _save(path, _rebuild(fm, body))
    return original


def act_replace_text(args) -> dict:
    """Substituição targetada na linha N: primeira ocorrência de --from por --to.

    Usado por fix_locus (typo de locus de citação) e por substituição de
    terminologia canônica. Verifica que --from existe na linha antes de tocar.
    """
    path = Path(args.path)

    def transform(line: str) -> str:
        if args.from_text not in line:
            _fail(f"texto não encontrado na linha {args.line}: {args.from_text!r}")
        return line.replace(args.from_text, args.to_text, 1)

    original = _edit_body_line(path, args.line, transform)
    return {
        "action": "replace-text", "path": str(path), "line": args.line,
        "from": args.from_text, "to": args.to_text, "changed": True, "original": original,
    }


def act_add_wikilink(args) -> dict:
    """Envolve a primeira ocorrência de --text na linha N num wikilink para --target.

    Não toca se a ocorrência já estiver dentro de `[[...]]`.
    """
    path = Path(args.path)
    target = args.target
    txt = args.text

    def transform(line: str) -> str:
        # já linkado?
        if f"[[{target}" in line or f"|{txt}]]" in line:
            return line
        pos = line.find(txt)
        if pos == -1:
            _fail(f"texto não encontrado na linha {args.line}: {txt!r}")
        # evitar quebrar um wikilink existente que contenha o texto
        before = line[:pos]
        if before.count("[[") > before.count("]]"):
            _fail(f"ocorrência dentro de wikilink existente na linha {args.line}")
        return line[:pos] + f"[[{target}|{txt}]]" + line[pos + len(txt):]

    original = _edit_body_line(path, args.line, transform)
    return {
        "action": "add-wikilink", "path": str(path), "line": args.line,
        "text": txt, "target": target, "changed": True, "original": original,
    }


# ─── ações de roteamento (caminho inseguro) ──────────────────────────────────

DIVERGENCIA_TEMPLATE = """---
tipo: divergencia
fontes: [{fontes}]
tags: [divergencia, grau/avancado{tema}]
atualizado_em: {hoje}
status: aberta
---

# {titulo}

> [!warning] Rascunho gerado por /critica — requer revisão humana
> Esta divergência foi levantada automaticamente pelo workflow de crítica profunda a partir de [[{conceito}]]. As posições abaixo precisam de conferência (citação literal via `scripts/cite.py`) e aprofundamento antes de promover a `status: concluída`. Protocolo: `.claude/rules/regra-divergencia.md`.

## Posição de Kardec (Pentateuco)

{kardec_pos} ({kardec_cite})

## Posição complementar

{outra_pos} ({outra_cite})

## Análise

> [!note] Pendente de análise humana
> Classificar: divergência real (estrutural), deslocamento de ênfase, aprofundamento legítimo ou má interpretação? Quando nível 2/3 contradiz o nível 1, Kardec prevalece — a divergência é registrada, nunca apagada.

## Fontes

- Kardec, Allan. {kardec_cite}.
- {outra_cite}.
"""


def act_divergencia_stub(args) -> dict:
    if not SLUG_RE.match(args.slug):
        _fail(f"slug não-canônico (esperado kebab-case ASCII): {args.slug!r}")
    path = DIVERGENCIAS_DIR / f"{args.slug}.md"
    if path.exists():
        return {"action": "divergencia-stub", "path": str(path), "changed": False, "reason": "já existe"}
    tema = f", {args.tema}" if args.tema else ""
    content = DIVERGENCIA_TEMPLATE.format(
        fontes=args.fontes, tema=tema, hoje=_today(args), titulo=args.titulo,
        conceito=args.conceito, kardec_pos=args.kardec_pos, kardec_cite=args.kardec_cite,
        outra_pos=args.outra_pos, outra_cite=args.outra_cite,
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    _save(path, content)
    return {"action": "divergencia-stub", "path": str(path), "changed": True}


def act_roadmap_append(args) -> dict:
    text = _load(ROADMAP_PATH)
    lines = text.splitlines()
    item = args.item.rstrip()
    if not item.startswith("- "):
        item = "- " + item

    # localizar a seção (heading exato)
    try:
        h = next(i for i, ln in enumerate(lines) if ln.strip() == ROADMAP_HEADING.strip())
    except StopIteration:
        h = None

    if h is None:
        # criar seção no fim do arquivo
        block = [
            "", ROADMAP_HEADING, "",
            "> Itens levantados por `/critica` que exigem julgamento doutrinário "
            "(não auto-corrigíveis). Formato: "
            "`- [ ] **<página>** (<eixo>, <data>) — <tensão> · evidência: <locus/cite> · relatório: <path>`",
            "", item, "",
        ]
        lines = lines + block
    else:
        # achar o fim da seção (próximo "## " ou EOF) e inserir antes
        end = len(lines)
        for i in range(h + 1, len(lines)):
            if lines[i].startswith("## "):
                end = i
                break
        # recuar sobre linhas em branco finais da seção
        insert_at = end
        while insert_at - 1 > h and lines[insert_at - 1].strip() == "":
            insert_at -= 1
        lines = lines[:insert_at] + [item] + lines[insert_at:]

    _save(ROADMAP_PATH, "\n".join(lines).rstrip("\n") + "\n")
    return {"action": "roadmap-append", "path": str(ROADMAP_PATH), "changed": True}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Applier determinístico do /critica.")
    parser.add_argument("--date", help="Sobrescreve a data corrente (testes).")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("add-tag"); p.add_argument("--path", required=True); p.add_argument("--tag", required=True)
    p = sub.add_parser("set-status"); p.add_argument("--path", required=True); p.add_argument("--status", required=True)
    p = sub.add_parser("bump"); p.add_argument("--path", required=True)

    p = sub.add_parser("replace-text")
    p.add_argument("--path", required=True); p.add_argument("--line", type=int, required=True)
    p.add_argument("--from", dest="from_text", required=True); p.add_argument("--to", dest="to_text", required=True)

    p = sub.add_parser("add-wikilink")
    p.add_argument("--path", required=True); p.add_argument("--line", type=int, required=True)
    p.add_argument("--text", required=True); p.add_argument("--target", required=True)

    p = sub.add_parser("divergencia-stub")
    p.add_argument("--slug", required=True); p.add_argument("--titulo", required=True)
    p.add_argument("--conceito", required=True); p.add_argument("--fontes", default="LE")
    p.add_argument("--tema", default=""); p.add_argument("--kardec-pos", dest="kardec_pos", required=True)
    p.add_argument("--kardec-cite", dest="kardec_cite", required=True)
    p.add_argument("--outra-pos", dest="outra_pos", required=True)
    p.add_argument("--outra-cite", dest="outra_cite", required=True)

    p = sub.add_parser("roadmap-append"); p.add_argument("--item", required=True)

    args = parser.parse_args(argv)
    import json
    # Guarda de dry-run determinística: nenhuma escrita acontece, mesmo que um
    # agente chame este applier durante um run dryRun.
    if _dry_run_active():
        sys.stdout.write(json.dumps(
            {"action": args.cmd, "changed": False, "dry_run": True,
             "path": getattr(args, "path", None)}, ensure_ascii=False) + "\n")
        return 0
    dispatch = {
        "add-tag": act_add_tag, "set-status": act_set_status, "bump": act_bump,
        "replace-text": act_replace_text, "add-wikilink": act_add_wikilink,
        "divergencia-stub": act_divergencia_stub, "roadmap-append": act_roadmap_append,
    }
    result = dispatch[args.cmd](args)
    sys.stdout.write(json.dumps(result, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
