#!/usr/bin/env python3
# Executar sempre com: uv run python .claude/skills/critica/scripts/critica_report.py
"""Renderiza o relatório do /critica em Markdown + HTML a partir do findings JSON.

Determinístico, sem tokens e sem dependência externa: o HTML é gerado DIRETO da
estrutura de dados (templating), não por conversão Markdown→HTML — os dois
formatos são renderizações independentes do mesmo JSON. Mantém o script
stdlib-only, no padrão do `lint_wiki.py`.

Grava `report.md` + `report.html` em `reports/critica/<timestamp>/` (dir
versionado, fora do build do Quartz via ignorePatterns).

Schema esperado do findings JSON (`--from`):
{
  "run": {"date","timestamp","scope_flags","budget","models",
          "pages_due","pages_critiqued","pages_skipped"},
  "pages":   [{"path","tipo","verdict","findings_count","auto_count",
               "deferred_count","summary"}],
  "findings":[{"id","path","axis","severity","line","claim","evidence",
               "disposition","action":{"type","detail"},
               "verdict":{"status","note"}}]
}
"""
from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DEFAULT_OUT = ROOT / "reports" / "critica"

AXES = {
    1: "Divergências com o Pentateuco",
    2: "Citações",
    3: "Padrão editorial",
    4: "Tags e cross-references",
}
SEV_ORDER = {"alta": 0, "media": 1, "baixa": 2}
DISPOSITION_LABEL = {
    "auto_fixed": "✓ auto-corrigido",
    "deferred": "⚠ diferido a humano",
    "dropped": "✕ descartado (verificação refutou)",
}


# ─── Markdown ────────────────────────────────────────────────────────────────

def render_md(data: dict) -> str:
    run = data.get("run", {})
    pages = data.get("pages", [])
    findings = data.get("findings", [])
    out: list[str] = []
    A = out.append

    A(f"# Relatório de crítica profunda — {run.get('date', '?')}")
    A("")
    A("## 1. Metadados do run")
    A("")
    A(f"- **Data:** {run.get('date', '?')}")
    A(f"- **Escopo:** `{run.get('scope_flags', '—')}`")
    A(f"- **Budget:** {run.get('budget', '—')}")
    models = run.get("models", {})
    if models:
        A("- **Modelos:** " + ", ".join(f"{k}={v}" for k, v in models.items()))
    A(f"- **Páginas devidas / criticadas / puladas:** "
      f"{run.get('pages_due', '?')} / {run.get('pages_critiqued', '?')} / {run.get('pages_skipped', '?')}")
    A(f"- **Total de achados:** {len(findings)} "
      f"({_count(findings, 'auto_fixed')} auto, {_count(findings, 'deferred')} diferidos, "
      f"{_count(findings, 'dropped')} descartados)")
    A("")

    A("## 2. Páginas avaliadas")
    A("")
    if pages:
        A("| Página | Tipo | Veredito | Achados | Auto | Diferidos |")
        A("|--------|------|----------|---------|------|-----------|")
        for p in pages:
            A(f"| `{p.get('path','')}` | {p.get('tipo','')} | {p.get('verdict','')} | "
              f"{p.get('findings_count',0)} | {p.get('auto_count',0)} | {p.get('deferred_count',0)} |")
    else:
        A("_Nenhuma página avaliada._")
    A("")

    A("## 3. Achados por eixo")
    A("")
    for axis in (1, 2, 3, 4):
        group = [f for f in findings if f.get("axis") == axis]
        if not group:
            continue
        A(f"### Eixo {axis} — {AXES[axis]} ({len(group)})")
        A("")
        for f in sorted(group, key=lambda x: SEV_ORDER.get(x.get("severity", "baixa"), 3)):
            disp = DISPOSITION_LABEL.get(f.get("disposition", ""), f.get("disposition", ""))
            A(f"- **[{f.get('severity','?')}]** `{f.get('path','')}`"
              + (f":{f['line']}" if f.get("line") else "") + f" — {disp}")
            if f.get("claim"):
                A(f"  - Afirmação: {f['claim']}")
            if f.get("evidence"):
                A(f"  - Evidência: {f['evidence']}")
            if f.get("verdict"):
                v = f["verdict"]
                A(f"  - Verificação: **{v.get('status','')}** — {v.get('note','')}")
            act = f.get("action") or {}
            if act:
                A(f"  - Ação: `{act.get('type','')}` — {act.get('detail','')}")
        A("")

    A("## 4. Mudanças auto-aplicadas")
    A("")
    auto = [f for f in findings if f.get("disposition") == "auto_fixed"]
    if auto:
        for f in auto:
            act = f.get("action") or {}
            A(f"- `{f.get('path','')}`"
              + (f":{f['line']}" if f.get("line") else "")
              + f" — `{act.get('type','')}`: {act.get('detail','')}")
    else:
        A("_Nenhuma correção auto-aplicada._")
    A("")

    A("## 5. Diferidos a decisão humana")
    A("")
    deferred = [f for f in findings if f.get("disposition") == "deferred"]
    if deferred:
        A("> Páginas marcadas `status: rascunho`; itens anotados no ROADMAP.md §11.")
        A("")
        for f in deferred:
            A(f"- `{f.get('path','')}` (eixo {f.get('axis','?')}, {f.get('severity','?')}) — "
              f"{f.get('claim','')}")
    else:
        A("_Nenhum item diferido._")
    A("")

    A("## 6. Resumo por página")
    A("")
    for p in pages:
        A(f"### `{p.get('path','')}`")
        A(f"{p.get('summary','—')}")
        A("")

    return "\n".join(out).rstrip() + "\n"


def _count(findings: list[dict], disposition: str) -> int:
    return sum(1 for f in findings if f.get("disposition") == disposition)


# ─── HTML (templating direto, sem conversão de Markdown) ─────────────────────

_CSS = """
body{font-family:-apple-system,Segoe UI,Roboto,sans-serif;max-width:54rem;margin:2rem auto;padding:0 1rem;line-height:1.55;color:#1a1a1a}
h1{border-bottom:2px solid #333;padding-bottom:.3rem}
h2{margin-top:2rem;border-bottom:1px solid #ccc;padding-bottom:.2rem}
table{border-collapse:collapse;width:100%;margin:1rem 0}
th,td{border:1px solid #ccc;padding:.4rem .6rem;text-align:left;font-size:.9rem}
th{background:#f4f4f4}
code{background:#f0f0f0;padding:.1rem .3rem;border-radius:3px;font-size:.85em}
.finding{border-left:3px solid #ccc;padding:.4rem .8rem;margin:.6rem 0;background:#fafafa}
.alta{border-left-color:#c0392b}.media{border-left-color:#e67e22}.baixa{border-left-color:#7f8c8d}
.disp-auto_fixed{color:#27ae60}.disp-deferred{color:#e67e22}.disp-dropped{color:#7f8c8d}
.meta li{margin:.2rem 0}
small{color:#666}
"""


def _h(s) -> str:
    return html.escape(str(s))


def render_html(data: dict) -> str:
    run = data.get("run", {})
    pages = data.get("pages", [])
    findings = data.get("findings", [])
    P: list[str] = []
    A = P.append

    A("<!doctype html><html lang='pt-BR'><head><meta charset='utf-8'>")
    A(f"<title>Crítica profunda — {_h(run.get('date','?'))}</title>")
    A(f"<style>{_CSS}</style></head><body>")
    A(f"<h1>Relatório de crítica profunda — {_h(run.get('date','?'))}</h1>")

    A("<h2>1. Metadados do run</h2><ul class='meta'>")
    A(f"<li><b>Escopo:</b> <code>{_h(run.get('scope_flags','—'))}</code></li>")
    A(f"<li><b>Budget:</b> {_h(run.get('budget','—'))}</li>")
    models = run.get("models", {})
    if models:
        A("<li><b>Modelos:</b> " + ", ".join(f"{_h(k)}={_h(v)}" for k, v in models.items()) + "</li>")
    A(f"<li><b>Páginas devidas / criticadas / puladas:</b> "
      f"{_h(run.get('pages_due','?'))} / {_h(run.get('pages_critiqued','?'))} / {_h(run.get('pages_skipped','?'))}</li>")
    A(f"<li><b>Total de achados:</b> {len(findings)} "
      f"({_count(findings,'auto_fixed')} auto, {_count(findings,'deferred')} diferidos, "
      f"{_count(findings,'dropped')} descartados)</li>")
    A("</ul>")

    A("<h2>2. Páginas avaliadas</h2>")
    if pages:
        A("<table><tr><th>Página</th><th>Tipo</th><th>Veredito</th><th>Achados</th><th>Auto</th><th>Diferidos</th></tr>")
        for p in pages:
            A(f"<tr><td><code>{_h(p.get('path',''))}</code></td><td>{_h(p.get('tipo',''))}</td>"
              f"<td>{_h(p.get('verdict',''))}</td><td>{_h(p.get('findings_count',0))}</td>"
              f"<td>{_h(p.get('auto_count',0))}</td><td>{_h(p.get('deferred_count',0))}</td></tr>")
        A("</table>")
    else:
        A("<p><em>Nenhuma página avaliada.</em></p>")

    A("<h2>3. Achados por eixo</h2>")
    for axis in (1, 2, 3, 4):
        group = [f for f in findings if f.get("axis") == axis]
        if not group:
            continue
        A(f"<h3>Eixo {axis} — {_h(AXES[axis])} ({len(group)})</h3>")
        for f in sorted(group, key=lambda x: SEV_ORDER.get(x.get("severity", "baixa"), 3)):
            sev = f.get("severity", "baixa")
            disp = f.get("disposition", "")
            A(f"<div class='finding {_h(sev)}'>")
            loc = f":{f['line']}" if f.get("line") else ""
            A(f"<b>[{_h(sev)}]</b> <code>{_h(f.get('path',''))}{_h(loc)}</code> "
              f"<span class='disp-{_h(disp)}'>{_h(DISPOSITION_LABEL.get(disp, disp))}</span><br>")
            if f.get("claim"):
                A(f"<small>Afirmação:</small> {_h(f['claim'])}<br>")
            if f.get("evidence"):
                A(f"<small>Evidência:</small> {_h(f['evidence'])}<br>")
            if f.get("verdict"):
                v = f["verdict"]
                A(f"<small>Verificação:</small> <b>{_h(v.get('status',''))}</b> — {_h(v.get('note',''))}<br>")
            act = f.get("action") or {}
            if act:
                A(f"<small>Ação:</small> <code>{_h(act.get('type',''))}</code> — {_h(act.get('detail',''))}")
            A("</div>")

    A("<h2>4. Mudanças auto-aplicadas</h2>")
    auto = [f for f in findings if f.get("disposition") == "auto_fixed"]
    if auto:
        A("<ul>")
        for f in auto:
            act = f.get("action") or {}
            loc = f":{f['line']}" if f.get("line") else ""
            A(f"<li><code>{_h(f.get('path',''))}{_h(loc)}</code> — "
              f"<code>{_h(act.get('type',''))}</code>: {_h(act.get('detail',''))}</li>")
        A("</ul>")
    else:
        A("<p><em>Nenhuma correção auto-aplicada.</em></p>")

    A("<h2>5. Diferidos a decisão humana</h2>")
    deferred = [f for f in findings if f.get("disposition") == "deferred"]
    if deferred:
        A("<p><small>Páginas marcadas <code>status: rascunho</code>; itens no ROADMAP.md §11.</small></p><ul>")
        for f in deferred:
            A(f"<li><code>{_h(f.get('path',''))}</code> (eixo {_h(f.get('axis','?'))}, "
              f"{_h(f.get('severity','?'))}) — {_h(f.get('claim',''))}</li>")
        A("</ul>")
    else:
        A("<p><em>Nenhum item diferido.</em></p>")

    A("<h2>6. Resumo por página</h2>")
    for p in pages:
        A(f"<h3><code>{_h(p.get('path',''))}</code></h3><p>{_h(p.get('summary','—'))}</p>")

    A("</body></html>")
    return "".join(P)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Renderiza o relatório do /critica.")
    parser.add_argument("--from", dest="from_file", help="Findings JSON (default: stdin).")
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT), help="Diretório base dos relatórios.")
    parser.add_argument("--timestamp", help="Subdir do run (ex.: 2026-05-31-1430). Default: run.timestamp ou run.date.")
    args = parser.parse_args(argv)

    raw = Path(args.from_file).read_text(encoding="utf-8") if args.from_file else sys.stdin.read()
    data = json.loads(raw)
    run = data.get("run", {})
    stamp = args.timestamp or run.get("timestamp") or run.get("date") or "sem-data"

    out_dir = Path(args.out_dir) / stamp
    out_dir.mkdir(parents=True, exist_ok=True)
    md_path = out_dir / "report.md"
    html_path = out_dir / "report.html"
    md_path.write_text(render_md(data), encoding="utf-8")
    html_path.write_text(render_html(data), encoding="utf-8")

    sys.stdout.write(json.dumps(
        {"md": str(md_path), "html": str(html_path)}, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
