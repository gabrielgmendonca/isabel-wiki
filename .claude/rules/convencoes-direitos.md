---
paths:
  - "wiki/obras/**"
---

# Direitos autorais (`tipo: obra`)

```yaml
direitos:
  detentor: dominio-publico | FEB | Boa-Nova | LEAL | IDE | desconhecido
  ano_dp_estimado: 2059        # opcional; 70 anos após a morte. Omitir se DP.
  url_aquisicao: https://...   # recomendado se protegida
  observacao: "..."            # opcional
```

| Detentor | Obras |
|---|---|
| `dominio-publico` | Kardec, Léon Denis, Cairbar Schutel, Eurípedes Barsanulfo, textos bíblicos |
| `FEB` | Chico Xavier (André Luiz, Emmanuel, Humberto de Campos), Bezerra (via FEB), Martins Peralva |
| `Boa-Nova` | Espírito Santo Neto / Hammed |
| `LEAL` | Divaldo Franco / Joanna de Ângelis |
| `IDE` | Yvonne Pereira e outros |
| `desconhecido` | detentor ambíguo (palestras, nível 4) |

**Obra protegida** (detentor ≠ `dominio-publico`) — guia editorial de citação:
- Até **400 palavras corridas** ou **3 questões/itens consecutivos** citados por página, o que vier primeiro.
- Citação direta ≤ 25% do corpo; o leitor sai com a interpretação da wiki, não com a obra transcrita.
- Precisando de mais: parafrasear + 1 trecho-chave curto, linkando `url_aquisicao`. Em `tipo: obra`, o resumo por eixos é paráfrase + citações curtas.
- Evangelhos canônicos: DP, citar livremente.
