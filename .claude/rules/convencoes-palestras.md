---
paths:
  - "raw/palestras/**"
---

# Convenções de `raw/palestras/`

Palestras de YouTube são armazenadas em pares lado a lado, dentro de uma subpasta por canal:

```
raw/palestras/<canal-slug>/<titulo-slug>.md          # transcrição
raw/palestras/<canal-slug>/summary-<titulo-slug>.md  # resumo
```

- **`<TÍTULO>.md`** — transcrição completa, **primeira linha** `Fonte: <URL>` (o pipeline do `/yt` injeta esse cabeçalho).
- **`summary-<TÍTULO>.md`** — resumo gerado a partir da mesma transcrição.

Slugs (canal e título) seguem o canônico do projeto: **kebab-case ASCII puro** — sem `_`, sem acento, sem maiúsculas, sem espaços. O lint `raw_layout` verifica; `/yt` e `/yt-bulk` já produzem nesse formato via slugify (NFKD + `[^a-z0-9]+` → `-`).

Quando a palestra cai solta em `raw/palestras/` (sem subpasta de canal), está fora do padrão — rodar `uv run python scripts/normalize_raw_layout.py --apply --scope raw/palestras` para migrar.

Entrada canônica: `/yt <URL>` para um vídeo, `/yt-bulk <canal> --limit N` para os N mais recentes de um canal (skip de já baixados). Nenhuma das duas toca `wiki/` — a curadoria via `/ingest` continua manual, palestra a palestra.
