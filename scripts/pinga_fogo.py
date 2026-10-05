#!/usr/bin/env python3
"""Ferramentas do Pinga-Fogo (TV Tupi, 1971): tempo por frase, busca e conferência.

As transcrições em raw/ só trazem o tempo no início de cada fala, e uma fala de
Chico pode durar vários minutos. Este script alinha a transcrição revisada à
legenda automática do YouTube (tempo por palavra) e grava o tempo de cada frase
em data/pinga-fogo/tempos.json. Com isso:

    uv run python scripts/pinga_fogo.py alinhar            # refaz tempos.json (baixa legendas)
    uv run python scripts/pinga_fogo.py tempo I "trecho"   # tempo exato de um trecho
    uv run python scripts/pinga_fogo.py checar [arquivos]  # confere falas e embeds na wiki

`checar` é camada 0: toda fala citada em bloco `> [!quote] ... Pinga-Fogo I|II, H:MM:SS`
precisa existir na transcrição (trechos separados por "(...)") e o tempo citado
precisa cair no trecho; todo embed `![](youtube...&t=Ns)` precisa cair numa
frase de Chico. A legenda serve só para o tempo; o texto vale sempre o da
transcrição revisada.
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw/mediuns/chico-xavier/emmanuel"
DATA = ROOT / "data/pinga-fogo/tempos.json"
PROGRAMAS = {
    "I": {"arquivo": RAW / "pinga-fogo-1.md", "video": "v5waIS1qedA"},
    "II": {"arquivo": RAW / "pinga-fogo-2.md", "video": "GNaG1qijyp0"},
}
VIDEO_PARA_PROG = {v["video"]: k for k, v in PROGRAMAS.items()}

TURNO_RE = re.compile(r"^\*\*([^*]+):\*\* \[(\d+:\d\d:\d\d)\]\s*(.*)$")
TEMPO_SOLTO_RE = re.compile(r"^\[(\d+:\d\d:\d\d)\]\s*(.*)$")
FRASE_RE = re.compile(r"(?<=[.!?…])[\"”»)]*\s+(?=[\"“«(]?[A-ZÁÉÍÓÚÂÊÔÃÕÀÇ0-9])")
TOKEN_RE = re.compile(r"[a-z0-9]+")


def hms(s: str) -> int:
    h, m, sec = (int(x) for x in s.split(":"))
    return h * 3600 + m * 60 + sec


def fmt(seg: int) -> str:
    return f"{seg // 3600}:{seg % 3600 // 60:02d}:{seg % 60:02d}"


def norm(texto: str) -> str:
    t = unicodedata.normalize("NFKD", texto.lower())
    return "".join(c for c in t if not unicodedata.combining(c))


def tokens(texto: str) -> list[str]:
    return TOKEN_RE.findall(norm(texto))


# --------------------------------------------------------------------------- transcrição

def ler_transcricao(prog: str) -> list[dict]:
    """Frases da seção ## Transcrição: falante, tempo do turno, linha, texto."""
    linhas = PROGRAMAS[prog]["arquivo"].read_text(encoding="utf-8").splitlines()
    frases: list[dict] = []
    dentro = False
    falante, turno_t = None, 0
    for n, linha in enumerate(linhas, 1):
        if linha.startswith("## Transcrição"):
            dentro = True
            continue
        if dentro and linha.startswith("## "):
            break
        if not dentro or not linha.strip() or linha.strip() == "---":
            continue
        m = TURNO_RE.match(linha)
        if m:
            falante, turno_t, corpo = m.group(1), hms(m.group(2)), m.group(3)
        else:
            m2 = TEMPO_SOLTO_RE.match(linha)
            corpo = m2.group(2) if m2 else linha
            if m2:
                turno_t = hms(m2.group(1))
            if corpo.startswith("[") and corpo.endswith("]"):
                continue  # [música — ...]
        for frase in FRASE_RE.split(corpo.strip()):
            if tokens(frase):
                frases.append({"falante": falante, "turno": turno_t, "linha": n, "texto": frase})
    return frases


# --------------------------------------------------------------------------- legenda

def baixar_legenda(video: str, destino: Path) -> Path:
    subprocess.run(
        ["yt-dlp", "--skip-download", "--write-auto-subs", "--sub-langs", "pt", "--sub-format", "json3",
         "-o", str(destino / "%(id)s.%(ext)s"), f"https://www.youtube.com/watch?v={video}"],
        check=True, capture_output=True,
    )
    return destino / f"{video}.pt.json3"


def palavras_legenda(arquivo: Path) -> list[tuple[str, float]]:
    dados = json.loads(arquivo.read_text(encoding="utf-8"))
    out: list[tuple[str, float]] = []
    for ev in dados.get("events", []):
        t0 = ev.get("tStartMs", 0)
        for seg in ev.get("segs", []):
            t = (t0 + seg.get("tOffsetMs", 0)) / 1000
            for tok in tokens(seg.get("utf8", "")):
                out.append((tok, t))
    return out


def palavras_whisper(arquivo: Path) -> list[tuple[str, float]]:
    """Palavras com tempo do JSON do (mlx-)whisper rodado com --word-timestamps True."""
    dados = json.loads(arquivo.read_text(encoding="utf-8"))
    return [(tok, w["start"]) for seg in dados.get("segments", [])
            for w in seg.get("words", []) for tok in tokens(w.get("word", ""))]


def alinhar_programa(prog: str, fontes: list[list[tuple[str, float]]]) -> list[dict]:
    """Tempo de cada frase. `fontes` em ordem de preferência (Whisper, depois legenda):
    a segunda só preenche tokens que a primeira não casou."""
    frases = ler_transcricao(prog)
    # tokens da transcrição com índice da frase de origem
    trans_tok: list[str] = []
    dona: list[int] = []
    for i, f in enumerate(frases):
        for tok in tokens(f["texto"]):
            trans_tok.append(tok)
            dona.append(i)
    tempo_tok: list[float | None] = [None] * len(trans_tok)
    # alinha turno a turno: o tempo do turno (Whisper) é confiável e limita a janela
    turnos = sorted({f["turno"] for f in frases})
    fim_turno = {t: (turnos[i + 1] if i + 1 < len(turnos) else t + 3600) for i, t in enumerate(turnos)}
    for leg in fontes:
        k = 0
        while k < len(trans_tok):
            t0 = frases[dona[k]]["turno"]
            a = k
            while k < len(trans_tok) and frases[dona[k]]["turno"] == t0:
                k += 1
            janela = [i for i, (_, t) in enumerate(leg) if t0 - 8 <= t <= fim_turno[t0] + 8]
            if not janela:
                continue
            sm = difflib.SequenceMatcher(None, trans_tok[a:k], [leg[i][0] for i in janela], autojunk=False)
            for bl in sm.get_matching_blocks():
                if bl.size < 2:
                    continue
                for j in range(bl.size):
                    if tempo_tok[a + bl.a + j] is None:
                        tempo_tok[a + bl.a + j] = leg[janela[bl.b + j]][1]
    # interpola tokens sem casamento entre vizinhos alinhados (dentro do turno)
    conhecidos = [(j, t) for j, t in enumerate(tempo_tok) if t is not None]
    inicio_frase: list[float | None] = [None] * len(frases)
    exato = [False] * len(frases)
    ci = 0
    for j, i in enumerate(dona):
        if inicio_frase[i] is not None:
            continue
        if tempo_tok[j] is not None:
            inicio_frase[i], exato[i] = tempo_tok[j], True
            continue
        while ci < len(conhecidos) and conhecidos[ci][0] < j:
            ci += 1
        antes = conhecidos[ci - 1] if ci > 0 else (j, float(frases[i]["turno"]))
        depois = conhecidos[ci] if ci < len(conhecidos) else antes
        if depois[0] == antes[0]:
            t = antes[1]
        else:
            t = antes[1] + (depois[1] - antes[1]) * (j - antes[0]) / (depois[0] - antes[0])
        inicio_frase[i] = max(t, frases[i]["turno"])
    for i, f in enumerate(frases):
        f["t"] = int(inicio_frase[i] if inicio_frase[i] is not None else f["turno"])
        if not exato[i]:
            f["aprox"] = True
    return frases


# --------------------------------------------------------------------------- consulta

def carregar() -> dict[str, list[dict]]:
    return json.loads(DATA.read_text(encoding="utf-8"))


def _texto_normalizado(frases: list[dict]) -> tuple[str, list[int]]:
    """Texto contínuo normalizado e, para cada caractere, o índice da frase."""
    partes, dono = [], []
    for i, f in enumerate(frases):
        t = " ".join(tokens(f["texto"])) + " "
        partes.append(t)
        dono.extend([i] * len(t))
    return "".join(partes), dono


def localizar(prog: str, trecho: str, frases: list[dict] | None = None) -> list[dict]:
    """Frases onde o trecho começa (pode haver mais de uma ocorrência)."""
    frases = frases if frases is not None else carregar()[prog]
    texto, dono = _texto_normalizado(frases)
    agulha = " ".join(tokens(trecho))
    if not agulha:
        return []
    out, pos = [], texto.find(agulha)
    while pos != -1:
        out.append(frases[dono[pos]])
        pos = texto.find(agulha, pos + 1)
    return out


# --------------------------------------------------------------------------- conferência

QUOTE_TITLE_RE = re.compile(
    r"^>\s*\[!quote\][-+]?\s*(.*?Pinga-Fogo (I{1,2})\*?,?\s*(\d+:\d\d:\d\d))", re.I)
EMBED_RE = re.compile(r"!\[[^\]]*\]\((https?://(?:www\.)?youtube\.com/watch\?v=([\w-]{11})[^)]*)\)")
T_PARAM_RE = re.compile(r"[?&]t=(\d+)s?")
ELISAO_RE = re.compile(r"\(\s*(?:\.\.\.|…)\s*\)|\[\s*(?:\.\.\.|…)\s*\]")
ASPA_TEMPO_RE = re.compile(r"[\"“]([^\"”]{12,}?)[\"”][^\"“(]{0,40}\((?:[^()]*?, )?\d+:\d\d:\d\d")
TOLERANCIA = 20  # segundos entre o tempo citado e o início real do trecho


def _blocos_quote(linhas: list[str]):
    i = 0
    while i < len(linhas):
        m = QUOTE_TITLE_RE.match(linhas[i])
        if not m:
            i += 1
            continue
        corpo, j = [], i + 1
        while j < len(linhas) and linhas[j].startswith(">"):
            corpo.append(linhas[j].lstrip(">").strip())
            j += 1
        yield i + 1, m.group(2).upper(), hms(m.group(3)), " ".join(corpo)
        i = j


def _tempo_ok(citado: int, frase: dict) -> bool:
    return abs(citado - frase["t"]) <= TOLERANCIA or citado == frase["turno"]


def checar_arquivo(path: Path, dados: dict[str, list[dict]]) -> list[str]:
    erros: list[str] = []
    linhas = path.read_text(encoding="utf-8").splitlines()
    for n, prog, citado, corpo in _blocos_quote(linhas):
        # só o que está entre aspas é texto do áudio; comentário fora das aspas é livre
        aspas = re.findall(r"[\"“]([^\"”]+)[\"”]", corpo) or [corpo]
        primeiro = None
        for trecho in aspas:
            for pedaco in ELISAO_RE.split(trecho):
                if len(tokens(pedaco)) < 3:
                    continue
                achou = localizar(prog, pedaco, dados[prog])
                if not achou:
                    erros.append(f"{path}:{n}: trecho não está na transcrição de Pinga-Fogo {prog}: "
                                 f"\"{pedaco.strip()[:70]}\"")
                elif primeiro is None:
                    primeiro = achou
        if primeiro and not any(_tempo_ok(citado, f) for f in primeiro):
            reais = ", ".join(fmt(f["t"]) for f in primeiro)
            erros.append(f"{path}:{n}: tempo {fmt(citado)} não bate com o trecho (início em {reais})")
    # aspas no corpo do texto seguidas de um tempo entre parênteses: "…" (0:57:02)
    em_quote = {n for n, *_ in _blocos_quote(linhas)}
    for n, linha in enumerate(linhas, 1):
        if linha.startswith(">") or n in em_quote:
            continue
        for m in ASPA_TEMPO_RE.finditer(linha):
            trecho = m.group(1)
            pedacos = [p for p in ELISAO_RE.split(trecho) if len(tokens(p)) >= 3]
            if pedacos and not any(localizar(pr, p, dados[pr]) for pr in dados for p in pedacos[:1]):
                erros.append(f"{path}:{n}: aspa com tempo não está nas transcrições: \"{trecho.strip()[:70]}\"")
    for n, linha in enumerate(linhas, 1):
        for m in EMBED_RE.finditer(linha):
            prog = VIDEO_PARA_PROG.get(m.group(2))
            if not prog:
                continue
            t = T_PARAM_RE.search(m.group(1))
            if not t:
                continue
            seg = int(t.group(1))
            perto = [f for f in dados[prog] if abs(f["t"] - seg) <= TOLERANCIA or f["turno"] == seg]
            if not any(f["falante"] == "Chico Xavier" for f in perto):
                erros.append(f"{path}:{n}: embed em {fmt(seg)} de Pinga-Fogo {prog} não cai numa fala de Chico")
    return erros


def corrigir_arquivo(path: Path, dados: dict[str, list[dict]]) -> int:
    """Reescreve o tempo do título de cada quote, e o `t=` do embed logo abaixo,
    pelo início real do primeiro trecho citado. Só mexe onde o trecho é achado
    uma única vez; ambíguo ou ausente fica para o `checar` apontar."""
    linhas = path.read_text(encoding="utf-8").splitlines()
    mudou = 0
    for n, prog, citado, corpo in list(_blocos_quote(linhas)):
        aspas = re.findall(r"[\"“]([^\"”]+)[\"”]", corpo) or [corpo]
        pedacos = [p for a in aspas for p in ELISAO_RE.split(a) if len(tokens(p)) >= 3]
        if not pedacos:
            continue
        achou = localizar(prog, pedacos[0], dados[prog])
        if len(achou) != 1 or _tempo_ok(citado, achou[0]) and abs(citado - achou[0]["t"]) <= 3:
            continue
        novo = achou[0]["t"]
        linhas[n - 1] = linhas[n - 1].replace(fmt(citado), fmt(novo), 1)
        video = PROGRAMAS[prog]["video"]
        for j in range(n, min(n + 8, len(linhas))):
            if video in linhas[j] and T_PARAM_RE.search(linhas[j]):
                linhas[j] = T_PARAM_RE.sub(lambda m: m.group(0)[0] + f"t={novo}s", linhas[j], count=1)
                linhas[j] = linhas[j].replace(f"[Pinga-Fogo {prog}, {fmt(citado)}]", f"[Pinga-Fogo {prog}, {fmt(novo)}]")
                break
        mudou += 1
    if mudou:
        path.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    return mudou


def alvos_padrao() -> list[Path]:
    return sorted(p for p in (ROOT / "wiki").rglob("*.md") if "Pinga-Fogo" in p.read_text(encoding="utf-8"))


# --------------------------------------------------------------------------- segmentos e páginas geradas

SEGMENTOS = ROOT / "data/pinga-fogo/segmentos.json"
GLOSSARIO = ROOT / "data/pinga-fogo/glossario.json"
PASTA_WIKI = ROOT / "wiki/obras/pinga-fogo"
TEMAS = {
    "mediunidade-e-psicografia": "Mediunidade e psicografia",
    "vida-de-chico": "Chico por ele mesmo",
    "reencarnacao-e-justica-divina": "Reencarnação e justiça divina",
    "morte-e-vida-espiritual": "Morte e vida espiritual",
    "ciencia-e-espiritismo": "Ciência e Espiritismo",
    "sexualidade-e-familia": "Sexualidade e família",
    "sociedade-e-moral": "Sociedade e moral",
    "jesus-e-as-religioes": "Jesus e as religiões",
    "programa": "Abertura e intervalos",
}
GERADO = "<!-- Página gerada por scripts/pinga_fogo.py a partir de data/pinga-fogo/. Não editar à mão. -->"


def montar_segmentos(entradas: list[Path]) -> list[dict]:
    """Junta os segmentos anotados, valida os tempos contra os turnos e deriva `fim`/`ate_linha`."""
    segs = [s for e in entradas for s in json.loads(e.read_text(encoding="utf-8"))]
    erros, out = [], []
    for prog in PROGRAMAS:
        linhas = PROGRAMAS[prog]["arquivo"].read_text(encoding="utf-8").splitlines()
        turnos = {}
        fim_transcricao = len(linhas)
        for n, linha in enumerate(linhas, 1):
            if linha.startswith("## Notas de revis"):
                fim_transcricao = n - 1
                break
            m = TURNO_RE.match(linha)
            if m:
                turnos[n] = (m.group(1), m.group(2))
        doprog = sorted((s for s in segs if s["programa"] == prog), key=lambda s: s["linha"])
        for i, s in enumerate(doprog):
            if s["linha"] not in turnos or turnos[s["linha"]][1] != s["inicio"]:
                erros.append(f"{prog} {s['inicio']}: linha {s['linha']} não é o início de turno informado")
            if s.get("resposta") and s["resposta"] not in {t for _, t in turnos.values()}:
                erros.append(f"{prog} {s['inicio']}: resposta {s['resposta']} não é tempo de turno")
            if s["tema"] not in TEMAS:
                erros.append(f"{prog} {s['inicio']}: tema desconhecido {s['tema']}")
            prox = doprog[i + 1] if i + 1 < len(doprog) else None
            s["ate_linha"] = prox["linha"] - 1 if prox else fim_transcricao
            s["fim"] = prox["inicio"] if prox else None
            s["id"] = f"{prog}-{i + 1:03d}"
            s["temas_secundarios"] = [t for t in s.get("temas_secundarios", []) if t in TEMAS and t != s["tema"]]
            out.append(s)
    if erros:
        raise SystemExit("segmentos inválidos:\n  " + "\n  ".join(erros))
    return out


def _ancoras_tematicas() -> dict[str, list[tuple[str, int, str]]]:
    """Para cada programa: (página, segundo do quote, heading ### acima dele)."""
    out: dict[str, list[tuple[str, int, str]]] = {"I": [], "II": []}
    for slug in TEMAS:
        p = PASTA_WIKI / f"{slug}.md"
        if not p.exists():
            continue
        heading = None
        for linha in p.read_text(encoding="utf-8").splitlines():
            if linha.startswith("### "):
                heading = linha[4:].strip()
            m = QUOTE_TITLE_RE.match(linha)
            if m and heading:
                out[m.group(2).upper()].append((slug, hms(m.group(3)), heading))
    return out


def _link_tema(seg: dict, ancoras: dict) -> str:
    ini = hms(seg["inicio"])
    fim = hms(seg["fim"]) if seg.get("fim") else 10 ** 6
    dentro = [(slug, heading) for slug, t, heading in ancoras[seg["programa"]] if ini <= t < fim]
    preferidas = [seg["tema"], *seg.get("temas_secundarios", [])]
    dentro.sort(key=lambda a: preferidas.index(a[0]) if a[0] in preferidas else len(preferidas))
    if dentro:
        slug, heading = dentro[0]
        return f"[[wiki/obras/pinga-fogo/{slug}#{heading}|{TEMAS[slug]}]]"
    slug = seg["tema"]
    if slug != "programa" and (PASTA_WIKI / f"{slug}.md").exists():
        return f"[[wiki/obras/pinga-fogo/{slug}|{TEMAS[slug]}]]"
    return TEMAS[slug]


def _video(seg: dict, campo: str = "resposta") -> str:
    t = seg.get(campo) or seg["inicio"]
    return f"[▶ {t}](https://www.youtube.com/watch?v={PROGRAMAS[seg['programa']]['video']}&t={hms(t)}s)"


def _cel(texto: str) -> str:
    return texto.replace("|", "\\|").replace("\n", " ").strip()


def _celula_link(link: str) -> str:
    """Wikilink com rótulo dentro de tabela: o `|` do alias precisa de escape."""
    return link.replace("|", "\\|")


def _frontmatter(tags: list[str]) -> str:
    return ("---\ntipo: sintese\nfontes: [Chico Xavier]\n"
            f"tags: [{', '.join(tags)}]\n"
            f"atualizado_em: {__import__('datetime').date.today().isoformat()}\nstatus: ativo\n---\n")


def gerar_indice(segs: list[dict]) -> str:
    ancoras = _ancoras_tematicas()
    partes = [_frontmatter(["pinga-fogo", "chico-xavier", "índice", "tema/historia-doutrina", "autor/chico-xavier"]),
              GERADO, "", "# Pinga-Fogo: índice das perguntas", "",
              "Todas as perguntas feitas a Chico Xavier nos dois programas *Pinga-Fogo* (TV Tupi, 1971), "
              "na ordem em que foram ao ar. O tempo abre o vídeo no início da resposta; o tema leva à fala "
              "comentada, com trecho literal e relação com as obras de Chico e com o Pentateuco. "
              "Visão geral em [[wiki/obras/pinga-fogo|Pinga-Fogo (1971)]]; termos e nomes em "
              "[[wiki/obras/pinga-fogo/indice-remissivo|índice remissivo]].", ""]
    partes += ["## Por tema", ""]
    for slug, nome in TEMAS.items():
        n = sum(1 for s in segs if s["tema"] == slug)
        if slug == "programa" or not n:
            continue
        alvo = f"[[wiki/obras/pinga-fogo/{slug}|{nome}]]" if (PASTA_WIKI / f"{slug}.md").exists() else nome
        partes.append(f"- {alvo}: {n} pergunta{'s' if n > 1 else ''}")
    partes.append("")
    rotulos = {"I": "Pinga-Fogo I (27–28 de julho de 1971)", "II": "Pinga-Fogo II (21 de dezembro de 1971)"}
    for prog in PROGRAMAS:
        partes += [f"## {rotulos[prog]}", "", "| Tempo | Quem pergunta | Pergunta | Resposta de Chico, em resumo | Tema |",
                   "|---|---|---|---|---|"]
        for s in (s for s in segs if s["programa"] == prog):
            if s["tema"] == "programa":
                partes.append(f"| {_video(s, 'inicio')} | — | *{_cel(s['pergunta'])}* | {_cel(s.get('resumo') or '')} | — |")
                continue
            partes.append(f"| {_video(s)} | {_cel(s['pergunta_por'])} | {_cel(s['pergunta'])} | "
                          f"{_cel(s.get('resumo') or '')} | {_celula_link(_link_tema(s, ancoras))} |")
        partes.append("")
    partes += ["## Fontes", "",
               "- Chico Xavier, *Pinga-Fogo I* (TV Tupi, 28/07/1971), transcrição do áudio: "
               "[[raw/mediuns/chico-xavier/emmanuel/pinga-fogo-1]].",
               "- Chico Xavier, *Pinga-Fogo II* (TV Tupi, 21/12/1971), transcrição do áudio: "
               "[[raw/mediuns/chico-xavier/emmanuel/pinga-fogo-2]].", ""]
    return "\n".join(partes)


def gerar_remissivo(segs: list[dict]) -> str:
    ancoras = _ancoras_tematicas()
    glossario = json.loads(GLOSSARIO.read_text(encoding="utf-8")) if GLOSSARIO.exists() else {}
    defs = {norm(k): v for k, v in glossario.get("termos", {}).items()}
    rotulo = {norm(k): k for k in glossario.get("termos", {})}
    canonico = {norm(k): norm(k) for k in glossario.get("termos", {})}
    for k, v in glossario.get("termos", {}).items():
        for var in v.get("variantes", []):
            canonico[norm(var)] = norm(k)
    excluir = {norm(x) for x in glossario.get("excluir", [])}
    termos: dict[str, dict] = {}
    for s in segs:
        for termo in s.get("termos", []):
            chave = norm(termo.strip())
            if chave in excluir:
                continue
            chave = canonico.get(chave, chave)
            e = termos.setdefault(chave, {"rotulo": rotulo.get(chave, termo.strip()), "segs": []})
            if s not in e["segs"]:
                e["segs"].append(s)
    partes = [_frontmatter(["pinga-fogo", "chico-xavier", "glossário", "índice", "tema/historia-doutrina",
                            "autor/chico-xavier"]),
              GERADO, "", "# Pinga-Fogo: índice remissivo", "",
              "Nomes, obras e conceitos que aparecem nas respostas de Chico Xavier nos dois programas *Pinga-Fogo* "
              "(1971), com uma definição curta e cada ocorrência no vídeo. As perguntas em ordem estão no "
              "[[wiki/obras/pinga-fogo/indice|índice das perguntas]]. Use a busca do navegador (Ctrl+F) para "
              "achar um termo.", ""]
    letra = None
    for chave in sorted(termos, key=lambda k: k.lstrip("\"'«")):
        e = termos[chave]
        inicial = chave[:1].upper()
        inicial = "0–9" if inicial.isdigit() else inicial
        if inicial != letra:
            if letra is not None:
                partes.append("")
            letra = inicial
            partes += [f"## {letra}", ""]
        d = defs.get(chave, {})
        definicao = d.get("definicao", "") if isinstance(d, dict) else str(d)
        ver = d.get("ver") if isinstance(d, dict) else None
        linha = f"- **{e['rotulo']}**"
        variantes = d.get("variantes") if isinstance(d, dict) else None
        if variantes:
            linha += f" (também: {', '.join(variantes)})"
        if definicao:
            linha += f": {definicao}"
        if ver:
            linha += f" Ver [[{ver}]]."
        ocorr = []
        for s in e["segs"]:
            tema = _link_tema(s, ancoras) if s["tema"] != "programa" else ""
            ocorr.append(f"{s['programa']} {_video(s)}" + (f" ({tema})" if tema else ""))
        partes.append(linha)
        partes.append(f"  - {' · '.join(ocorr)}")
    partes += ["", "## Fontes", "",
               "- Chico Xavier, *Pinga-Fogo I* e *Pinga-Fogo II* (TV Tupi, 1971), transcrições do áudio: "
               "[[raw/mediuns/chico-xavier/emmanuel/pinga-fogo-1]] e [[raw/mediuns/chico-xavier/emmanuel/pinga-fogo-2]].",
               ""]
    return "\n".join(partes)


# --------------------------------------------------------------------------- CLI

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("alinhar", help="refaz data/pinga-fogo/tempos.json")
    a.add_argument("--legendas", type=Path, help="pasta com <id>.pt.json3 já baixados")
    a.add_argument("--whisper", type=Path,
                   help="pasta com <id>.json do mlx_whisper --word-timestamps True (fonte preferida)")
    t = sub.add_parser("tempo", help="tempo exato de um trecho")
    t.add_argument("programa", choices=["I", "II"])
    t.add_argument("trecho")
    c = sub.add_parser("checar", help="confere falas citadas e embeds na wiki")
    c.add_argument("arquivos", nargs="*", type=Path)
    c.add_argument("--corrigir", action="store_true",
                   help="reescreve tempos de quote e embed pelo alinhamento atual antes de conferir")
    sg = sub.add_parser("segmentos", help="junta e valida os segmentos anotados em data/pinga-fogo/segmentos.json")
    sg.add_argument("entradas", nargs="+", type=Path)
    sub.add_parser("paginas", help="gera o índice das perguntas e o índice remissivo")
    args = ap.parse_args()

    if args.cmd == "segmentos":
        segs = montar_segmentos(args.entradas)
        SEGMENTOS.parent.mkdir(parents=True, exist_ok=True)
        SEGMENTOS.write_text(json.dumps(segs, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"{len(segs)} segmentos válidos")
        return 0

    if args.cmd == "paginas":
        segs = json.loads(SEGMENTOS.read_text(encoding="utf-8"))
        PASTA_WIKI.mkdir(parents=True, exist_ok=True)
        (PASTA_WIKI / "indice.md").write_text(gerar_indice(segs), encoding="utf-8")
        (PASTA_WIKI / "indice-remissivo.md").write_text(gerar_remissivo(segs), encoding="utf-8")
        print("gerados: wiki/obras/pinga-fogo/indice.md e indice-remissivo.md")
        return 0

    if args.cmd == "alinhar":
        saida: dict[str, list[dict]] = {}
        with tempfile.TemporaryDirectory() as tmp:
            pasta = args.legendas or Path(tmp)
            for prog, cfg in PROGRAMAS.items():
                leg = pasta / f"{cfg['video']}.pt.json3"
                if not leg.exists():
                    leg = baixar_legenda(cfg["video"], pasta)
                fontes = [palavras_legenda(leg)]
                wj = args.whisper / f"{cfg['video']}.json" if args.whisper else None
                if wj and wj.exists():
                    fontes.insert(0, palavras_whisper(wj))
                frases = alinhar_programa(prog, fontes)
                saida[prog] = [{k: f[k] for k in ("t", "turno", "linha", "falante", "texto")}
                               | ({"aprox": True} if f.get("aprox") else {}) for f in frases]
                aprox = sum(1 for f in frases if f.get("aprox"))
                print(f"Pinga-Fogo {prog}: {len(frases)} frases, {aprox} com tempo interpolado")
        DATA.parent.mkdir(parents=True, exist_ok=True)
        DATA.write_text(json.dumps(saida, ensure_ascii=False, indent=0), encoding="utf-8")
        return 0

    dados = carregar()
    if args.cmd == "tempo":
        achou = localizar(args.programa, args.trecho, dados[args.programa])
        if not achou:
            print("trecho não encontrado na transcrição", file=sys.stderr)
            return 1
        video = PROGRAMAS[args.programa]["video"]
        for f in achou:
            marca = " (interpolado)" if f.get("aprox") else ""
            print(f"{fmt(f['t'])}{marca}  turno {fmt(f['turno'])}  {f['falante']}  linha {f['linha']}")
            print(f"  https://www.youtube.com/watch?v={video}&t={f['t']}s")
        return 0

    arquivos = args.arquivos or alvos_padrao()
    if args.corrigir:
        for p in arquivos:
            if (n := corrigir_arquivo(p, dados)):
                print(f"{p}: {n} tempo(s) corrigido(s)")
    erros = [e for p in arquivos for e in checar_arquivo(p, dados)]
    for e in erros:
        print(e)
    print(f"{len(arquivos)} arquivo(s), {len(erros)} problema(s)")
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
