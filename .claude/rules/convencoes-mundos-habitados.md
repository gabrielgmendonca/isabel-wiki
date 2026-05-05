---
paths:
  - "wiki/**"
---

# Nomenclatura dos mundos habitados

Kardec fixa em **ESE cap. III, item 4** uma escala canônica de cinco categorias de mundos habitados — base obrigatória para qualquer página da wiki que trate da pluralidade dos mundos, da progressão planetária ou da posição da Terra na escala. Sem disciplina, a wiki acaba misturando "mundo de provas" (sem "expiação"), "mundo regenerado" (particípio), "mundos ditosos", etc. — formas que ora aparecem em Kardec, ora são deformações modernas. A política abaixo fixa **uma forma canônica por categoria** e regula como linkar ou substituir variantes em prosa.

## Escala canônica (ESE cap. III, item 4)

| Ordem | Forma canônica | Slug da página | Variantes aceitas em prosa |
|-------|----------------|-----------------|-----------------------------|
| 1 | **Mundos primitivos** | `wiki/conceitos/mundos-primitivos` | — |
| 2 | **Mundos de expiação e provas** | `wiki/conceitos/mundos-de-expiacao-e-provas` | "mundos expiatórios" (Kardec usa em ESE cap. III, item 15) |
| 3 | **Mundos de regeneração** ou **Mundos regeneradores** | `wiki/conceitos/mundos-regeneradores` | ambas formas são de Kardec (item 4 vs. itens 16-17) |
| 4 | **Mundos felizes** | `wiki/conceitos/mundos-felizes` | "mundos venturosos" (item 10), "mundos ditosos" (item 13 — uma vez) |
| 5 | **Mundos celestes ou divinos** | `wiki/conceitos/mundos-celestes-ou-divinos` | "mundos celestes", "mundos divinos" isoladamente (síntese de "celestes ou divinos") |

A panorâmica que articula as cinco está em `wiki/conceitos/pluralidade-dos-mundos-habitados`.

## Variantes não-canônicas a evitar

| Forma drift | Por quê | Como corrigir |
|-------------|---------|---------------|
| "mundo de provas" / "mundo de prova" (sem "expiação") | Reduz a categoria a um dos seus dois polos; perde a expiação como dimensão moral central | Substituir por `[[wiki/conceitos/mundos-de-expiacao-e-provas\|mundo de expiação e provas]]`, ou pela forma canônica direta |
| "mundo de provas e expiações" (ordem invertida) | Não é a ordem fixada por Kardec em item 4 ("expiação e provas") | Reordenar para a canônica |
| "mundo regenerado" (particípio passado) | Implica processo concluído; "regenerador" descreve o estado de transição | Substituir por "mundo regenerador" (linkado) |

## Termos relativos — não confundir com categorias

Kardec usa em **ESE cap. III, item 8** os termos **"mundos inferiores"** e **"mundos superiores"** — explicita: *"A qualificação de mundos inferiores e mundos superiores nada tem de absoluta; é, antes, muito relativa. Tal mundo é inferior ou superior com referência aos que lhe estão acima ou abaixo, na escala progressiva."* São **descritores relativos válidos**, não categorias da escala canônica. Manter em prosa quando o contexto for de comparação ascendente/descendente; **não** linkar para nenhuma das 6 páginas da escala (não há página de "mundos inferiores").

## Wikilink com display alternativo

Aliases formais (`aliases:` no frontmatter) só existem para `tipo: personalidade|obra` — ver `convencoes-aliases.md`. Para categorias-conceito, a ferramenta análoga é o **wikilink com display**:

- Em prosa nova, preferir a **forma canônica direta**: `Os [[wiki/conceitos/mundos-felizes|mundos felizes]] não são privilégio de poucos.`
- Quando a forma do texto-fonte ou contexto preserva nuance autoral (ex.: parafraseando o item 13 de ESE cap. III, que usa "ditoso"), usar **display alternativo**: `Kardec antecipa "ascender a um planeta mais [[wiki/conceitos/mundos-felizes|ditoso]]" (ESE cap. III, item 13).`
- **Em blockquote citacional** (transcrição literal de Kardec, Léon Denis, médium psicografante, etc.): **não alterar nem linkar**. O lint ignora blockquotes.

## Lint

`check_mundos_habitados_naming` (severity `info`) varre o corpo de cada página e sinaliza variantes não-canônicas em prosa fora de blockquote, inline code e wikilink. Skip por design:

- As 6 páginas-conceito da escala (introduzem suas próprias variantes em "Definição"/"Ensino de Kardec").
- Frontmatter, blockquotes, inline code, wikilinks já existentes.

A severidade é `info` deliberadamente: orienta passes incrementais, não bloqueia merge. Promover a `warning` depois de calibrar contra falso positivo.
