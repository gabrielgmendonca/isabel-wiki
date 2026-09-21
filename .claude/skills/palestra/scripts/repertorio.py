"""Repertório já contado — que casos/personagens/parábolas já apareceram nos decks.

Camada 0 do `/palestra` (CLAUDE.md §4): a pergunta "este caso já foi usado?" é
decidível por código — é cruzar o registro de nomes que a wiki já mantém
(`wiki/personalidades/*.md` + `wiki/conceitos/parabola-*.md`, com os `aliases:`)
contra o texto dos decks em `slides/*/deck.md` e das palestras já apresentadas em
`raw/palestras/gabriel-mendonca/*.pptx|*.odp`.

Não é veto: repetir caso em casa diferente é normal. A saída entra no dossiê como
*informação* ("já contado em X"), para o palestrante decidir.

    uv run python .claude/skills/palestra/scripts/repertorio.py [--raiz .] [--json]
"""
import argparse
import json
import re
import sys
import unicodedata
import zipfile
from pathlib import Path

MIN_TERMO = 3  # abaixo disso o nome casa com qualquer coisa ("Max" é caso legítimo)
LIMITE = 6     # perguntas/partes por deck: amostra do jeito de conduzir, não o deck inteiro
UBIQUO = 0.4   # nome presente em ≥40% dos decks é vocabulário, não caso contado


def sem_acento(s):
    return unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode("ascii")


def h1_e_aliases(md):
    """Título canônico (H1) + aliases do frontmatter de uma página da wiki."""
    texto = md.read_text(encoding="utf-8")
    nomes = []
    m = re.search(r"^#\s+(.+?)\s*$", texto, re.M)
    if m:
        nomes.append(re.sub(r"[*_`]|\s*—.*$|\s*\(.*?\)$", "", m.group(1)).strip())
    fm = re.match(r"---\n(.*?)\n---", texto, re.S)
    if fm and "aliases:" in fm.group(1):
        bloco = fm.group(1).split("aliases:", 1)[1]
        for linha in bloco.splitlines()[1:]:
            a = re.match(r"\s+-\s*\"?(.+?)\"?\s*$", linha)
            if not a:
                break
            nomes.append(a.group(1))
    return [n for n in nomes if len(n) >= MIN_TERMO]


def autores(raiz):
    """Slugs do namespace `autor/` (convencoes-tags.md) — quem ASSINA não é caso contado.

    Sem isto, "Emmanuel" e "Allan Kardec" apareceriam como casos em todo deck.
    """
    slugs = set()
    for md in (raiz / "wiki").rglob("*.md"):
        fm = re.match(r"---\n(.*?)\n---", md.read_text(encoding="utf-8"), re.S)
        if fm:
            slugs.update(re.findall(r"autor/([a-z0-9-]+)", fm.group(1)))
    return slugs


def termos(raiz):
    """Registro de nomes: personalidades e parábolas já catalogadas na wiki."""
    pular = autores(raiz)
    reg, visto = {}, set()
    for sub, rotulo in (("personalidades/*.md", "personalidade"), ("conceitos/parabola-*.md", "parábola")):
        for md in sorted((raiz / "wiki").glob(sub)):
            if md.name == "index.md" or md.stem in pular:
                continue
            for nome in h1_e_aliases(md):
                # alias sem acento é redundante: o casamento já normaliza
                chave = sem_acento(nome).lower()
                if chave in visto:
                    continue
                visto.add(chave)
                reg[nome] = (rotulo, f"wiki/{sub.split('/')[0]}/{md.stem}")
    return reg


def texto_pptx(p):
    """Texto por parágrafo. Os runs (`<a:t>`) de um mesmo `<a:p>` são contíguos —
    juntá-los com espaço partiria "Szymel Slizgol" que o PowerPoint quebrou em
    dois runs por formatação, e o nome deixaria de casar."""
    with zipfile.ZipFile(p) as z:
        partes = [n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)]
        paragrafos = []
        for n in sorted(partes):
            xml = z.read(n).decode("utf-8", "ignore")
            for par in re.findall(r"<a:p>(.*?)</a:p>", xml, re.S):
                paragrafos.append("".join(re.findall(r"<a:t>(.*?)</a:t>", par, re.S)))
        return "\n".join(paragrafos)


def texto_odp(p):
    with zipfile.ZipFile(p) as z:
        return re.sub(r"<[^>]+>", " ", z.read("content.xml").decode("utf-8", "ignore"))


def angulos_deck(texto):
    """Título, títulos de parte e perguntas de um `deck.md` Marp.

    O que a lente de palestras herdava por julgamento — "como ele já abriu um
    tema assim" — em boa parte está aqui, em código: o deck marca a função de
    cada slide com `_class`. Não substitui a lente (ela explica POR QUE deu
    certo), mas dá ao arco um banco de aberturas e cortes já testados no palco.
    """
    fm = re.match(r"---\n(.*?)\n---", texto, re.S)
    titulo = ""
    if fm:
        h = re.search(r"^header:\s*'?\"?(.+?)'?\"?\s*$", fm.group(1), re.M)
        titulo = h.group(1).strip() if h else ""
    partes, perguntas = [], []
    for bloco in re.split(r"^---\s*$", texto, flags=re.M):
        m = re.search(r"^##\s+(.+?)\s*$", bloco, re.M)
        if not m:
            continue
        if "_class: pergunta" in bloco:
            perguntas.append(m.group(1).strip())
        elif "_class: section" in bloco:
            partes.append(m.group(1).strip())
    unico = lambda xs: list(dict.fromkeys(xs))
    return {"titulo": titulo, "partes": unico(partes), "perguntas": unico(perguntas)}


def angulos_apresentado(texto):
    """Dos `.pptx`/`.odp` só dá para colher com segurança as perguntas —
    a estrutura de parte não é marcada como num deck Marp.

    Descarta a pergunta LITERAL do Pentateuco ("675. Por trabalho só se devem
    entender…"): ela é a citação do slide de Q&A, não o jeito do palestrante de
    conduzir. O que interessa aqui é a pergunta que ELE escreveu."""
    vistas, perguntas = set(), []
    for ln in texto.splitlines():
        ln = ln.strip()
        if not ln.endswith("?") or not 3 <= len(ln.split()) <= 25:
            continue
        if re.match(r"^(\d+\.|[a-z]\)|\(|[—–-])", ln):
            continue
        chave = sem_acento(ln).lower()
        if chave in vistas:
            continue
        vistas.add(chave)
        perguntas.append(ln)
    return {"titulo": "", "partes": [], "perguntas": perguntas}


def fontes(raiz):
    """Decks versionados + palestras já apresentadas, cada um com seu extrator."""
    for deck in sorted(raiz.glob("slides/*/deck.md")):
        yield f"slides/{deck.parent.name}", deck.read_text(encoding="utf-8"), "deck"
    for p in sorted(raiz.glob("raw/palestras/gabriel-mendonca/*")):
        try:
            if p.suffix == ".pptx":
                yield p.name, texto_pptx(p), "apresentado"
            elif p.suffix == ".odp":
                yield p.name, texto_odp(p), "apresentado"
        except (zipfile.BadZipFile, KeyError) as e:
            print(f"aviso: {p.name} ilegível ({e})", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--raiz", default=".", type=Path)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--casos", action="store_true", help="só os casos já contados, sem os ângulos")
    args = ap.parse_args()

    reg = termos(args.raiz)
    achados, angulos = {}, {}
    origens = list(fontes(args.raiz))
    for origem, texto, tipo in origens:
        a = angulos_deck(texto) if tipo == "deck" else angulos_apresentado(texto)
        if a["titulo"] or a["partes"] or a["perguntas"]:
            angulos[origem] = a
        plano = sem_acento(texto)
        for nome, (rotulo, pagina) in reg.items():
            # Caixa ignorada no casamento (título de slide vem em CAIXA ALTA), mas
            # a ocorrência precisa ser NOME PRÓPRIO — senão "O Castigo" casaria com
            # a palavra "castigo" solta na prosa de qualquer deck.
            achou = [m.group(0) for m in re.finditer(rf"\b{re.escape(sem_acento(nome))}\b", plano, re.I)]
            if any(o.lstrip()[:1].isupper() for o in achou):
                achados.setdefault(nome, {"tipo": rotulo, "pagina": pagina, "decks": []})
                if origem not in achados[nome]["decks"]:
                    achados[nome]["decks"].append(origem)

    # Um nome que aparece em quase todo deck ("Jesus", "Allan Kardec") não
    # distingue nada — é vocabulário do repertório inteiro, não caso já contado.
    teto = max(4, round(UBIQUO * len(origens)))
    achados = {n: a for n, a in achados.items() if len(a["decks"]) < teto}

    if args.json:
        print(json.dumps({"casos": achados, "angulos": angulos}, ensure_ascii=False, indent=1))
        return

    print("== CASOS JÁ CONTADOS ==")
    if not achados:
        print("(nenhum caso do registro da wiki aparece nos decks existentes)")
    for nome in sorted(achados, key=lambda n: (-len(achados[n]["decks"]), n)):
        a = achados[nome]
        print(f"{nome} ({a['tipo']}) — {', '.join(a['decks'])}")

    if args.casos:
        return
    print("\n== ÂNGULOS JÁ USADOS (abertura e cortes que já foram ao palco) ==")
    for origem in sorted(angulos):
        a = angulos[origem]
        print(f"{origem}{' — ' + a['titulo'] if a['titulo'] else ''}")
        for p in a["perguntas"][:LIMITE]:
            print(f"  pergunta: {p}")
        for t in a["partes"][:LIMITE]:
            print(f"  parte: {t}")


if __name__ == "__main__":
    main()
