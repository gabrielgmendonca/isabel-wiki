---
paths:
  - "wiki/obras/**"
---

# Direitos autorais (obras nível 3)

Páginas `tipo: obra` declaram a situação de direitos da obra original via campo aninhado `direitos:`. Habilita aviso ao leitor (renderizado pelo transformer Quartz `CopyrightNotice`) e checks de lint específicos para obras protegidas.

```yaml
direitos:
  detentor: dominio-publico | FEB | Boa-Nova | LEAL | IDE | desconhecido
  ano_dp_estimado: 2059        # opcional; ano estimado de entrada em DP (pmcs Brasil = 70 anos após morte)
  url_aquisicao: https://...   # opcional, recomendado para obras protegidas
  observacao: "..."            # opcional
```

| Detentor | Quando usar |
|---|---|
| `dominio-publico` | Kardec (m. 1869), Léon Denis (m. 1927), Cairbar Schutel (m. 1938), Eurípedes Barsanulfo (m. 1918), textos bíblicos. **Não preencher** `ano_dp_estimado` quando DP. |
| `FEB` | Federação Espírita Brasileira — Chico Xavier (toda a série André Luiz, Emmanuel, Humberto de Campos), Bezerra de Menezes (publicações via FEB), Martins Peralva. |
| `Boa-Nova` | Editora Boa Nova — Francisco do Espírito Santo Neto / Hammed. |
| `LEAL` | Livraria Espírita Alvorada — Joanna de Ângelis / Divaldo Franco. |
| `IDE` | Instituto de Difusão Espírita — Yvonne Pereira e outros. |
| `desconhecido` | Detentor não identificado ou ambíguo (palestras, autores nível 4 sem mapeamento claro). Backlog manual. |

Default conservador: ausência do campo `direitos:` em `tipo: obra` é tratada pelo lint como `info` (vai virar `warning` após backfill em massa).

## Limites de citação para obras protegidas

Para obras com `direitos.detentor` diferente de `dominio-publico`, aplicar limites operacionais — não é doutrina jurídica de fair-use, é guia editorial para citar com respeito ao autor:

- **Trecho citado direto**: até **400 palavras corridas** ou **3 questões/itens consecutivos** por página, o que vier primeiro.
- **Proporção**: citação direta ≤ 25% do corpo da página; comentário próprio ≥ 75%. O leitor deve sair com a interpretação da wiki, não com a obra original transcrita.
- **Quando exceder for necessário**: parafrasear ("conforme Hammed argumenta em *As Dores da Alma*, capítulo X, [paráfrase]") + 1 trecho-chave breve em citação direta. Linkar o `url_aquisicao` da página de obra.
- **Páginas `tipo: obra`** podem citar mais (resumo estrutural por capítulo/parte), mas o "Resumo por eixos" deve ser **paráfrase + citações curtas**, não transcrição.
- **Ensinamentos morais de Jesus** (Evangelhos canônicos): texto-base em DP, citar livremente.

O lint (`check_quote_proportion`) reporta páginas que excedem como `info`; revisão manual decide se promove para `warning`.
