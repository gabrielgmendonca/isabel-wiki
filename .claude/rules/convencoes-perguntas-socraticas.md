---
paths:
  - "slides/**"
  - ".claude/skills/slides/**"
---

# Perguntas-ponte em slides

Pergunta-ponte = todo slide-pergunta que não é a pergunta literal do LE (abertura, transições antes de citações).

## Orçamento: ≤ 15 palavras, uma frase; âncora no subtítulo

O `h2` da `.pergunta` renderiza a 64px. Contexto e citação vão no `p` logo abaixo, nunca dentro da pergunta:

```markdown
<!-- _class: pergunta -->

## Por que os mais velhos largaram a pedra primeiro?

*"...retiraram-se, um após outro, afastando-se primeiro os velhos" — O Evangelho Segundo o Espiritismo, cap. X, item 12*
```

Duas frases no h2 = âncora no lugar errado. ✓ "Perdão sem limites — então o indulgente é um frouxo?" ✗ versão de 30 palavras com a citação embutida.

## Critérios (satisfazer ao menos um, dentro do orçamento)

- **A. Particular concreto** — nome, cena, número, caso já citado. ✓ "Marcel pediu pílulas para não incomodar; que fé sustenta isso aos 8 anos?" ✗ "Como manter a fé na adversidade?"
- **B. Tensão com a citação anterior** — objeção que nasce do que acabou de ser afirmado. ✓ "Se a causa é anterior, por que esquecemos?"
- **C. Pergunta literal de Kardec ou de Jesus** — ex.: "Por que sofrem uns mais do que outros?" (ESE, cap. V); "Quem é minha mãe?".

Se nenhum se aplica, **suprimir** a pergunta e deixar o section header fazer a transição.

**Antipadrões**: teaser sentimental ("E se quem partiu pudesse falar?"); reformulação do section header; hipótese abstrata; pergunta intercambiável (serviria antes de qualquer citação do tema); sim/não suave ("E a fé que não raciocina, vale?"); pergunta-parágrafo.

**Cadência**: pergunta forte → 1-3 citações → pergunta forte; citações que se sustentam juntas vão encadeadas, sem pergunta no meio. Validar candidatos com `validate_candidates.py --tipo pergunta`.
