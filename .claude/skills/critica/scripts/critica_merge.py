#!/usr/bin/env python3
# Executar sempre com: uv run python .claude/skills/critica/scripts/critica_merge.py
"""Cola determinística entre os subagentes do /critica e a síntese serial.

Substitui o antigo workflow `critica-profunda.js`: a orquestração agora é feita
pelo main-session com a tool Agent, e tudo o que é decidível por código fica aqui
(camada 0) — nomes de arquivo de saída, quais achados precisam de cético,
regra de descarte e montagem do findings JSON.

Contrato: cada subagente GRAVA seu resultado num arquivo do run-dir (nunca se
parseia o eco textual do agente).

  plan        --scope S --run-dir D   → manifest.json + tabela path/tipo/saída
  verify-list --run-dir D             → JSON dos achados de eixo 1/2 a verificar
  merge       --run-dir D [--scope-flags ...] [--pages-due N] [--dry]
                                      → findings JSON (schema do critica_report.py)

Regra de disposição (igual à do workflow antigo com 1 cético): veredito
`refuted` → `dropped`; `confirmed`, `uncertain` ou veredito ausente → `deferred`
(ausência de verificação nunca descarta). Página sem arquivo de crítica é
contada como pulada e NÃO entra em `pages` — logo não é registrada e continua
devida no próximo run.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

LENSES = {
    1: "leitura kardecista alternativa — a divergência se dissolve ou já está registrada?",
    2: "correção factual via cite.py — a fonte realmente diz isso?",
}


def _slug(path: str) -> str:
    p = path[:-3] if path.endswith(".md") else path
    if p.startswith("wiki/"):
        p = p[5:]
    return p.replace("/", "__")


def _load_json(path: Path):
    text = path.read_text(encoding="utf-8").strip()
    if text.startswith("```"):  # agente cercou o JSON apesar da instrução
        text = text.split("\n", 1)[1] if "\n" in text else ""
        text = text.rsplit("```", 1)[0]
    return json.loads(text)


def _manifest(run_dir: Path) -> dict:
    mf = run_dir / "manifest.json"
    if not mf.exists():
        sys.exit(f"erro: {mf} não existe — rode `plan` primeiro")
    return json.loads(mf.read_text(encoding="utf-8"))


def cmd_plan(args) -> int:
    scope = json.loads(Path(args.scope).read_text(encoding="utf-8"))
    run_dir = Path(args.run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    pages = []
    for p in scope.get("pages", []):
        slug = _slug(p["path"])
        pages.append({"path": p["path"], "tipo": p.get("tipo") or "",
                      "slug": slug, "out": str(run_dir / f"{slug}.json")})
    manifest = {"pages": pages, "due_count": scope.get("due_count", len(pages))}
    (run_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    for p in pages:
        print(f"{p['path']}\t{p['tipo'] or '—'}\t{p['out']}")
    return 0


def cmd_verify_list(args) -> int:
    run_dir = Path(args.run_dir)
    todo, missing = [], []
    for p in _manifest(run_dir)["pages"]:
        out = Path(p["out"])
        if not out.exists():
            missing.append(p["path"])
            continue
        crit = _load_json(out)
        for i, it in enumerate(crit.get("deferred") or []):
            axis = it.get("axis")
            if axis in (1, 2):
                vout = run_dir / f"{p['slug']}.v{i}.json"
                if vout.exists():
                    continue  # retomada: já verificado
                todo.append({"critica": str(out), "indice": i, "axis": axis,
                             "severity": it.get("severity", ""), "lente": LENSES[axis],
                             "saida": str(vout), "path": p["path"]})
    print(json.dumps({"verify": todo, "missing_critique": missing}, ensure_ascii=False, indent=2))
    return 0


def _verdict_label(auto: int, dif: int, drop: int) -> str:
    parts = []
    if auto:
        parts.append(f"✓ {auto} auto")
    if dif:
        parts.append(f"⚠ {dif} diferido" + ("s" if dif > 1 else ""))
    if drop:
        parts.append(f"✕ {drop} desc")
    return " · ".join(parts) or "limpo"


def cmd_merge(args) -> int:
    run_dir = Path(args.run_dir)
    manifest = _manifest(run_dir)
    pages_out, findings, skipped = [], [], []
    fid = 0
    for p in manifest["pages"]:
        out = Path(p["out"])
        if not out.exists():
            skipped.append(p["path"])
            continue
        try:
            crit = _load_json(out)
        except json.JSONDecodeError as e:
            sys.stderr.write(f"aviso: JSON inválido em {out}: {e} — página pulada\n")
            skipped.append(p["path"])
            continue
        auto = dif = drop = 0
        for it in crit.get("applied") or []:
            fid += 1
            auto += 1
            findings.append({**it, "id": f"F{fid:03d}", "path": p["path"], "disposition": "auto_fixed"})
        for i, it in enumerate(crit.get("deferred") or []):
            fid += 1
            rec = {**it, "id": f"F{fid:03d}", "path": p["path"], "disposition": "deferred"}
            vout = run_dir / f"{p['slug']}.v{i}.json"
            if it.get("axis") in (1, 2):
                if vout.exists():
                    try:
                        v = _load_json(vout)
                        rec["verdict"] = {"status": v.get("status", "uncertain"), "note": v.get("note", "")}
                        if v.get("status") == "refuted":
                            rec["disposition"] = "dropped"
                    except json.JSONDecodeError:
                        rec["verdict"] = {"status": "uncertain", "note": "veredito ilegível — mantido diferido"}
                else:
                    rec["verdict"] = {"status": "uncertain", "note": "sem verificação — mantido diferido"}
            if rec["disposition"] == "dropped":
                drop += 1
            else:
                dif += 1
            findings.append(rec)
        pages_out.append({
            "path": p["path"], "tipo": p["tipo"] or crit.get("tipo", ""),
            "verdict": _verdict_label(auto, dif, drop),
            "findings_count": auto + dif + drop, "auto_count": auto,
            "deferred_count": dif, "summary": crit.get("summary", ""),
        })
    now = datetime.now()
    data = {
        "run": {
            "date": now.strftime("%Y-%m-%d"),
            "timestamp": args.timestamp or now.strftime("%Y-%m-%d-%H%M"),
            "scope_flags": args.scope_flags or "—",
            "budget": "dry-run" if args.dry else "—",
            "models": {"critica": "opus", "verificacao": "sonnet"},
            "pages_due": args.pages_due if args.pages_due is not None else manifest.get("due_count"),
            "pages_critiqued": len(pages_out),
            "pages_skipped": len(skipped),
            "skipped": skipped,
        },
        "pages": pages_out,
        "findings": findings,
    }
    text = json.dumps(data, ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
        print(json.dumps({"out": args.out, "pages": len(pages_out), "skipped": skipped,
                          "auto": sum(x["auto_count"] for x in pages_out),
                          "deferred": sum(x["deferred_count"] for x in pages_out),
                          "dropped": sum(1 for f in findings if f["disposition"] == "dropped")},
                         ensure_ascii=False))
    else:
        print(text)
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("plan"); p.add_argument("--scope", required=True); p.add_argument("--run-dir", required=True)
    p = sub.add_parser("verify-list"); p.add_argument("--run-dir", required=True)
    p = sub.add_parser("merge"); p.add_argument("--run-dir", required=True)
    p.add_argument("--out"); p.add_argument("--scope-flags"); p.add_argument("--timestamp")
    p.add_argument("--pages-due", type=int); p.add_argument("--dry", action="store_true")
    args = ap.parse_args(argv)
    return {"plan": cmd_plan, "verify-list": cmd_verify_list, "merge": cmd_merge}[args.cmd](args)


if __name__ == "__main__":
    raise SystemExit(main())
