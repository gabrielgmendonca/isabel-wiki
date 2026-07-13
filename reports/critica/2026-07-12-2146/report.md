# Relatório de crítica profunda — 2026-07-12

## 1. Metadados do run

- **Data:** 2026-07-12
- **Escopo:** `--path wiki/sinteses/logoterapia-e-espiritismo.md`
- **Budget:** 3 agentes / 222.950 tokens / 37 tool calls
- **Modelos:** critica=claude-opus-4-8, verificacao=claude-sonnet-5
- **Páginas devidas / criticadas / puladas:** ? / ? / ?
- **Total de achados:** 6 (2 auto, 4 diferidos, 0 descartados)

## 2. Páginas avaliadas

| Página | Tipo | Veredito | Achados | Auto | Diferidos |
|--------|------|----------|---------|------|-----------|
| `wiki/sinteses/logoterapia-e-espiritismo.md` | sintese | sólida com correções pendentes | 6 | 2 | 4 |

## 3. Achados por eixo

### Eixo 2 — Citações (3)

- **[media]** `wiki/sinteses/logoterapia-e-espiritismo.md`:136 — ✓ auto-corrigido
  - Afirmação: Atribui a aspa da gratidão "logoterapêutica" ao cap. 8 de Psicologia da Gratidão.
  - Evidência: A aspa (raw, linha 1768) está dentro do cap. 7 (headings: cap.7 = 1566–1799; cap.8 começa em 1800). Typo de locus puro.
  - Ação: `replace-text` — (cap. 8) → (cap. 7)
- **[baixa]** `wiki/sinteses/logoterapia-e-espiritismo.md`:152 — ⚠ diferido a humano
  - Afirmação: Tabela: "Caridade como fim da lei moral (LE, q. 886–919; ESE, cap. XI)".
  - Evidência: CONFIRMADO por verificação adversarial. O intervalo atravessa fronteira de capítulo: Cap. XI (Lei de justiça, amor e caridade) = q. 873–892; Cap. XII (Da perfeição moral) = q. 893–919. A q. 919 é autoconhecimento (introspecção) — direção oposta à autotranscendência que a linha alega sustentar — e já é usada na mesma tabela para outro ponto. Núcleo (q. 886 + ESE cap. XI) está correto.
  - Ação: `replace-text` — (LE, q. 886–919) → (LE, q. 886; ESE, cap. XI). NOTA: a rule convencoes-tags.md registra lei/justica-amor-caridade como "q. 873-919" — pode ter induzido o erro; conferir se a rule também deve virar 873–892.
- **[baixa]** `wiki/sinteses/logoterapia-e-espiritismo.md`:136 — ⚠ diferido a humano
  - Afirmação: Aspa apresentada como literal: recurso "logoterapêutico, por proporcionar sentido existencial ao ser humano".
  - Evidência: CONFIRMADO por verificação adversarial. A fonte (raw, linha 1768) tem "logoterapêutica" (feminino); a página flexionou para o masculino para concordar com "recurso". Aspa não-verbatim — exatamente a deriva que a Fase 2 do ROADMAP §12 combate.
  - Ação: `rewrite` — Reescrever para acomodar a aspa verbatim: a gratidão é "também logoterapêutica, por proporcionar sentido existencial ao ser humano" — ou de-quote a palavra flexionada.

### Eixo 3 — Padrão editorial (3)

- **[media]** `wiki/sinteses/logoterapia-e-espiritismo.md`:102 — ⚠ diferido a humano
  - Afirmação: Afirma que ociosidade/falta de fé/saciedade (LE q. 943) são "precisamente os três solos em que Frankl viu florescer o vazio", e que a convergência é "quase termo a termo".
  - Evidência: A própria página (linha 120) cita o Frankl de Joanna com OUTRA etiologia: perda de instintos básicos + desaparecimento das tradições (Amor, Imbatível Amor, cap. 22, verbatim). A citação de Kardec está certa; o enquadramento atribui a Frankl uma etiologia desmentida pela fonte citada na própria página.
  - Ação: `rewrite` — Moderar "quase termo a termo" → convergência funcional; apresentar as três raízes como DIAGNÓSTICO ESPÍRITA (Kardec), não como o que "Frankl viu"; registrar as duas causas distintas de Frankl. Ajustar também a nota da tabela (linha 150).
- **[media]** `wiki/sinteses/logoterapia-e-espiritismo.md`:210 — ⚠ diferido a humano
  - Afirmação: Fontes atribui "itens 4, 5 e 18 (Lacordaire, Havre, 1863)" — aposição abrange os três itens.
  - Evidência: cite.py: só o item 18 é assinado por Lacordaire (Havre, 1863); os itens 4 e 5 são comentário do próprio Kardec. Além disso o item 4 não é citado em nenhum ponto do corpo.
  - Ação: `rewrite` — Desmembrar: "item 5 (texto de Kardec) e item 18 (Lacordaire, Havre, 1863)"; remover o item 4 (não usado no corpo).
- **[baixa]** `wiki/sinteses/logoterapia-e-espiritismo.md`:216 — ✓ auto-corrigido
  - Afirmação: Seção Fontes lista Psicologia da Gratidão como "Caps. 8–9".
  - Evidência: As aspas usadas estão nos caps. 7 e 9; o cap. 8 não é citado no corpo.
  - Ação: `replace-text` — Caps. 8–9. → Caps. 7 e 9.

## 4. Mudanças auto-aplicadas

- `wiki/sinteses/logoterapia-e-espiritismo.md`:136 — `replace-text`: (cap. 8) → (cap. 7)
- `wiki/sinteses/logoterapia-e-espiritismo.md`:216 — `replace-text`: Caps. 8–9. → Caps. 7 e 9.

## 5. Diferidos a decisão humana

> Páginas marcadas `status: rascunho`; itens anotados no ROADMAP.md §11.

- `wiki/sinteses/logoterapia-e-espiritismo.md` (eixo 3, media) — Afirma que ociosidade/falta de fé/saciedade (LE q. 943) são "precisamente os três solos em que Frankl viu florescer o vazio", e que a convergência é "quase termo a termo".
- `wiki/sinteses/logoterapia-e-espiritismo.md` (eixo 3, media) — Fontes atribui "itens 4, 5 e 18 (Lacordaire, Havre, 1863)" — aposição abrange os três itens.
- `wiki/sinteses/logoterapia-e-espiritismo.md` (eixo 2, baixa) — Tabela: "Caridade como fim da lei moral (LE, q. 886–919; ESE, cap. XI)".
- `wiki/sinteses/logoterapia-e-espiritismo.md` (eixo 2, baixa) — Aspa apresentada como literal: recurso "logoterapêutico, por proporcionar sentido existencial ao ser humano".

## 6. Resumo por página

### `wiki/sinteses/logoterapia-e-espiritismo.md`
Doutrinariamente sólida e escrupulosa na hierarquia de autoridade; todas as citações do Pentateuco batem verbatim no cite.py e todas as aspas de Joanna existem nas obras citadas. Restam 1 typo de locus (corrigido), 2 imprecisões de referência, 1 aspa não-verbatim e 1 overclaim de convergência.
