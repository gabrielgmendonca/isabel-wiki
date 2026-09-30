---
paths:
  - "wiki/**"
---

# Taxonomia de tags

- **Tags livres**: PT-BR pleno, com acento (`herança-de-fé`, `superstição`).
- **Namespaces fechados** (ASCII, sem acento): só os valores abaixo.
- `obra/*`: derivada de `fontes:` por `scripts/enrich_tags_obra.py` — **não editar à mão**.

**`lei/`** (LE, 3ª parte) — quando a página trata da lei moral: `adoracao` (q. 649-673) · `trabalho` (674-685) · `reproducao` (686-701) · `conservacao` (702-727) · `destruicao` (728-765) · `sociedade` (766-775) · `progresso` (776-800) · `igualdade` (803-824) · `liberdade` (825-872) · `justica-amor-caridade` (873-919).

**`grau/`** — `introdutorio` (definições, questões simples, parábolas) · `intermediario` (conceitos estruturais, leitura de obra, nível ESDE) · `avancado` (aprofundamentos, sínteses, divergências, cruzamentos). Default por tipo via `scripts/enrich_tags_grau.py`: questao→introdutorio; parabola/personalidade/conceito→intermediario; aprofundamento/sintese/divergencia→avancado. `tipo: obra` e trilhas **não** recebem `grau/*`.

**`tema/`** — 1 a 3 por página (preferir 1), atribuição manual:

| Tag | Eixo |
|---|---|
| `deus` | Deus, providência, criação, atributos divinos |
| `espiritos` | natureza dos espíritos, hierarquia, escala espírita, anjos/demônios |
| `encarnacao` | reencarnação, perispírito, corpo, escolha de provas |
| `mediunidade` | comunicação espiritual, fenômenos, médiuns, obsessão |
| `moral` | leis morais (umbrella), virtudes, vícios, conduta |
| `jesus` | vida, ensinos, parábolas, divindade, missão de Jesus |
| `vida-futura` | pós-morte, céu/inferno, espíritos felizes/sofredores, penas futuras |
| `sociedade` | família, lar, casamento, instituições, política |
| `livre-arbitrio` | liberdade, expiação, fatalidade, responsabilidade |
| `prece-caridade` | adoração, prece, caridade prática |
| `sofrimento` | dor, expiação, provas, suicídio, tédio da vida |
| `historia-doutrina` | codificação, divulgação, biografia de Kardec/médiuns |

**`autor/`** — psicografia marca **espírito e médium** (ex.: `autor/emmanuel` + `autor/chico-xavier`):

| Tipo | Valores |
|---|---|
| Kardec | `kardec` (Pentateuco + OPE, OQE, RE) |
| Encarnados | `leon-denis`, `cairbar-schutel`, `waldo-vieira` (obras curadas com Chico Xavier; não é nível 3) |
| Médiuns | `chico-xavier`, `divaldo-franco` |
| Espíritos autores | `emmanuel`, `andre-luiz`, `humberto-de-campos` (via Chico Xavier) · `joanna-de-angelis` (via Divaldo) · `bezerra-de-menezes` (via Divaldo, e biografia) · `hammed` (via Espírito Santo Neto) |
| Apóstolos | `paulo` (epístolas paulinas) · `joao` (Evangelho, 1-3 João, Apocalipse) · `pedro` (1-2 Pedro) · `tiago` (Epístola de Tiago) |
| Pesquisa psíquica | `flammarion` |

Autor novo: adicionar aqui **e** no conjunto canônico do lint, na mesma PR. Backfill: `scripts/enrich_tags_autor.py`.
