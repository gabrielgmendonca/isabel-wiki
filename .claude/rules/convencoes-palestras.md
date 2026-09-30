---
paths:
  - "raw/palestras/**"
---

# Convenções de `raw/palestras/`

```
raw/palestras/<canal-slug>/<titulo-slug>.md          # transcrição; 1ª linha "Fonte: <URL>"
raw/palestras/<canal-slug>/summary-<titulo-slug>.md  # resumo
```

- Slugs em kebab-case ASCII (sem acento, `_`, maiúscula ou espaço).
- Arquivo solto fora de subpasta de canal → `uv run python scripts/normalize_raw_layout.py --apply --scope raw/palestras`.
- Entrada: `/yt <URL>` ou `/yt-bulk <canal> --limit N`. Nenhum dos dois toca `wiki/`; a curadoria é via `/ingest`, uma palestra por vez.
