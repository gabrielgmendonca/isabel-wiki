---
name: yt-bulk
description: Transcreve em massa os N vídeos mais recentes de um canal do YouTube para `raw/palestras/`. Pula vídeos já baixados. Use com /yt-bulk <URL-canal> --limit N, "transcrever últimos N vídeos do canal X em massa", "baixar canal Y em lote".
---

# /yt-bulk

Gatilhos: `/yt-bulk <URL-do-canal> --limit N` · "transcrever últimos N vídeos do canal X" · "baixar canal Y em massa"

Itera sobre os N vídeos mais recentes de um canal do YouTube e roda o pipeline do `/yt` (transcrição + resumo) em cada um. Pula vídeos cujo par (`<slug>.md` + `summary-<slug>.md`) já existe e está não-vazio em `raw/palestras/<canal-slug>/`, então pode ser re-executado para pegar só vídeos novos (resume natural).

**Não toca `wiki/`** — só `raw/palestras/`. A ingestão na wiki segue manual via `/ingest`, vídeo a vídeo, com curadoria editorial (classificação nível 3/4 conforme CLAUDE.md §2, vínculos de personalidades, checagem de divergências com o Pentateuco).

Casos típicos de uso: baixar lote do canal "Centro Espírita Allan Kardec — RJ", série de palestras de Divaldo Franco, ciclos do Haroldo Dutra Dias ou Suely Caldas Schubert.

## Entrada

- **URL do canal**: aceita formatos `https://www.youtube.com/@usuario`, `@usuario/videos`, `c/Nome`, `channel/UCxxx`, `playlist?list=...`. O `yt-dlp` resolve qualquer um deles via `--flat-playlist`.
- **`--limit N`** (obrigatório): número de vídeos mais recentes a considerar. Sem default — exigir explicitação evita disparar canal inteiro por acidente.

## Saída

Para cada vídeo novo, dois arquivos em `raw/palestras/<canal-slug>/`, seguindo a convenção de `.claude/rules/convencoes-palestras.md`:

- `<titulo-slug>.md` — transcrição integral, com `Fonte: <URL>` no topo.
- `summary-<titulo-slug>.md` — resumo executivo em seções.

Mesmo formato do `/yt` (passam pelo mesmo lint AWK e mesma slugify de canal+título). Slugs em kebab-case ASCII puro (sem `_`, sem acento, sem maiúsculas) — exigido pelo lint `raw_layout` da wiki.

## Passo 1 — Rodar o script

Da raiz do projeto:

```bash
.claude/skills/yt-bulk/scripts/yt-bulk.sh "<URL-do-canal>" --limit N
```

O script:

1. Lista os N video IDs mais recentes via `yt-dlp --flat-playlist --playlist-end N --print "%(id)s"`.
2. Para cada ID:
   - Obtém canal + título via `yt-dlp --print "%(channel)s" --print "%(title)s"` (mesma combo que o `yt.sh` usa) e slugifica ambos para montar o path esperado.
   - Se **ambos** `raw/palestras/<canal-slug>/<titulo-slug>.md` e `summary-<titulo-slug>.md` existem e **não estão vazios** → **skip**. Se algum estiver faltando ou vazio (run anterior abortou no meio), apaga parciais e re-processa.
   - Invoca `.claude/skills/yt/scripts/yt.sh <video-url>`. Falha de um vídeo individual não aborta o batch.
3. Imprime relatório final: `processed=X skipped=Y failed=Z`, com lista de novos arquivos e (se houver) lista de falhas com URL para retry manual.

## Passo 2 — Reportar ao usuário

Após o script terminar, surface ao usuário:

- Contadores (processados / pulados / falhados).
- Caminhos dos arquivos novos (para próximo passo, geralmente `/ingest`).
- URLs que falharam — sugerir retry via `/yt <URL>` individual, ou investigar (vídeo privado, removido, etc.).

## Custo e tempo

Cada vídeo dispara **2 chamadas `summarize --cli claude`** (transcrição + resumo). Cada chamada leva minutos. Para `--limit 50`, planejar dezenas de minutos de execução. Considerar começar com `--limit 5` ou `--limit 10` em canais novos para validar antes de escalar.

## Falhas transitórias e retry

O `claude --print` invocado pelo `summarize` pode falhar pontualmente em batches longos (rate limit, hiccup de sessão). Sintoma típico: `Command failed: claude --print --output-format json --model sonnet` em meio à fase "Gerando resumo".

Como tratar:

- **Re-executar `/yt-bulk` no mesmo canal e mesmo `--limit`** é a recuperação padrão. A checagem de skip considera "completo" só quando ambos os arquivos (transcrição + summary) existem e estão **não-vazios** — então vídeos com summary parcial são detectados, têm os parciais apagados e re-processados.
- **Custo de retry é baixo**: o `summarize` mantém cache local persistente por vídeo (etapas `--extract` e resumo cacheadas separadamente). Em retries, o output mostra `Cached · ...` e nenhuma chamada nova ao Claude é feita.
- **Falha reproduzível no mesmo vídeo** (≥3 tentativas, espaçadas em minutos) **não é transitória** — investigar: vídeo pode disparar filtros do Claude, ter legenda corrompida, ou ser longo demais. Usar `/yt <URL>` isolado para reproduzir e capturar stderr completo.

## Dependências

Mesmas do `/yt` — esta skill é uma camada fina de orquestração sobre `.claude/skills/yt/scripts/yt.sh`:

- [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) — via `uv run` (ver `pyproject.toml`).
- [`summarize`](https://github.com/steipete/summarize) — CLI Node.js, via `brew install summarize`.
- Claude CLI no `$PATH` (chamado por `summarize --cli claude`).
- `BROWSER_COOKIES` env (default: `safari`) — usado para `--cookies-from-browser` evitar bloqueio anti-bot do YouTube.
