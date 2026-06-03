# tracking/ — filas operacionais de obras

Trackers operacionais da wiki — **não são páginas da wiki** (sem frontmatter, fora do build público: o deploy só copia `wiki/`, `raw/`, `index.md`). Vivem aqui para tirar a poluição da raiz do repo e separar **estado factual** de **estratégia** (que continua no `ROADMAP.md` §1).

O pipeline de uma obra tem dois estágios, e cada um tem sua fila:

```
aquisição → raw/ → /ingest → wiki/
   │                  │
   └─ fila 1          └─ fila 2
```

## Fila 1 — Aquisição (obra ainda **não** está em `raw/`)

O que falta baixar/comprar/converter. Documentos aqui:

| Arquivo | Conteúdo | Regenerável? |
|---|---|---|
| `aquisicao-feb.md` | Catálogo FEB Editora — 54 obras a comprar, por autor | ✅ `scripts/scrape_feb_catalogo.py` |
| `aquisicao-feb-direitos.md` | Triagem jurídica do catálogo FEB (domínio público vs. compra) | ❌ **curado à mão** — não sobrescrever |
| `aquisicao-cealk.md` | Auditoria do catálogo CEAK (301/356 baixadas, 404s, tier ambíguo) | parcial — dados em `data/cealk-catalogo.json`; texto curado |

Regra: arquivo regenerado por script **nunca** recebe edição manual de conteúdo (o re-scrape apaga). O companheiro curado mora ao lado, marcado.

## Fila 2 — Ingestão (obra **está** em `raw/`, falta página em `wiki/obras/`)

**Não há arquivo estático para esta fila** — ela é derivada e envelheceria no minuto seguinte. Fonte de verdade é o script, rodado sob demanda:

```bash
uv run python scripts/list_pending_ingest.py            # lista pendentes por autor
uv run python scripts/list_pending_ingest.py --show-matched   # + as já cobertas (revisar match)
```

Compara slugs de `raw/{autores,mediuns}` contra `wiki/obras/` por heurística de tokens. A estratégia de **qual** autor priorizar (e por quê) vive no `ROADMAP.md` §1.1 — este script só diz o **estado factual**.

## Outros

- `migracao-raw-layout.md` — plano (concluído em 2026-05-10) de normalização do layout de `raw/`. Mantido como nota histórica enquanto os refinos opcionais não forem promovidos.
