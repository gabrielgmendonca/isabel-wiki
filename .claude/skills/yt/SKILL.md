---
name: yt
description: Transcreve e resume uma palestra do YouTube para markdown em `raw/palestras/`. Roda yt-dlp + summarize (via Claude CLI). Use com /yt <URL>, "transcrever <URL>", "baixar transcrição do YouTube".
---

# /yt

Gatilhos: `/yt <URL>` · "transcrever este vídeo" · "baixar transcrição do YouTube"

Gera dois arquivos em `raw/palestras/<canal-slug>/`, seguindo a convenção documentada em `.claude/rules/convencoes-palestras.md`:

- `<titulo-slug>.md` — transcrição integral, com `Fonte: <URL>` no topo.
- `summary-<titulo-slug>.md` — resumo executivo.

Canal e título vêm do `yt-dlp` e passam por slugify (kebab-case ASCII, sem acento). Ex.: palestra "O Evangelho à luz da Doutrina Espírita" do canal "Centro Espírita Allan Kardec - RJ" vira `raw/palestras/centro-espirita-allan-kardec-rj/o-evangelho-a-luz-da-doutrina-espirita.md`. Outro exemplo: canal "Haroldo Dutra Dias" vira `haroldo-dutra-dias`.

Ambos os arquivos passam por um lint AWK que junta linhas quebradas no meio de parágrafo e preserva markdown estrutural (headings, listas, blocos de código, citações).

## Escopo

Esta skill **não toca `wiki/`** — só popula `raw/palestras/`. A curadoria editorial (criar página em `wiki/obras/`, vincular personalidades, flaggar divergências) é manual depois, via `/ingest <caminho>`. Isso permite baixar lote bruto agora e curar com calma.

Palestras típicas se enquadram em **nível 3** (Divaldo Franco, Suely Caldas Schubert, Haroldo Dutra Dias, Geraldo Campetti — consagrados ou mediunidade-tier comparável) ou **nível 4** (palestrantes isolados sem estatura doutrinária consolidada) na hierarquia do CLAUDE.md §2. Quando contradisserem o Pentateuco (nível 1), Kardec prevalece e a divergência vira `> [!warning]` na página de obra durante o `/ingest`.

## Passo 1 — Rodar o script

Da raiz do projeto:

```bash
.claude/skills/yt/scripts/yt.sh "<URL do YouTube>"
```

O script:

1. Extrai canal + título em uma única chamada `yt-dlp --print "%(channel)s" --print "%(title)s"`.
2. Slugifica ambos (kebab-case ASCII) e monta `raw/palestras/<canal-slug>/<titulo-slug>.md`.
3. Roda `summarize ... --extract` para a transcrição literal.
4. Roda `summarize ...` sem `--extract` para o resumo, salvo como `summary-<titulo-slug>.md`.
5. Aplica o lint markdown em ambos.

Modelo fixo: `--cli claude` (usa Claude via sua sessão local do Claude Code; sem API key). Para trocar, editar `scripts/yt.sh`.

## Passo 2 — Verificar saída

```bash
ls -la raw/palestras/<canal-slug>/ | tail -5
```

Conferir que os dois arquivos foram criados (`<slug>.md` + `summary-<slug>.md`) e que a transcrição começa com `Fonte: <URL>`. O slug precisa ser kebab-case ASCII puro (sem `_`, sem acento, sem maiúsculas) — o lint da wiki (check `raw_layout`) reprova qualquer outro formato.

## Dependências

- [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) — instalado via `uv` (ver `pyproject.toml`). O script invoca como `uv run yt-dlp`.
- [`summarize`](https://github.com/steipete/summarize) (`@steipete/summarize`) — CLI Node.js, instalado via `brew install summarize`.
- Claude CLI no `$PATH` (o script usa `summarize --cli claude`, então passa pela sua sessão Claude Code — sem API key).
- `BROWSER_COOKIES` env (default: `safari`) — usado para `--cookies-from-browser` evitar bloqueio anti-bot do YouTube.
