---
paths:
  - "slides/**"
  - ".claude/skills/slides/**"
  - ".claude/skills/palestra/**"
  - ".claude/workflows/palestra-dossie.js"
---

# Imagens em slides de palestra

Imagem é **atmosférica, não informacional**: tira o olhar da plateia do texto enquanto o orador fala.

- **Engatar na cena, não no conceito.** Conceito abstrato ilustrado vira clichê (mãos, pomba, pôr do sol). Usar a cena do caso/parábola que a palestra já cita: indulgência → a mulher adúltera; misericórdia → o filho pródigo.
- **Só em momentos-chave**: abertura, cada caso/"Para meditar", síntese. Citação doutrinária e Q&A ficam tipográficos.
- **Sourcing, nesta ordem**:
  1. Arte **PD/CC** (Doré, Tissot, Rembrandt, Bruegel, Poussin) de Wikimedia Commons, Met, Brooklyn, Rijksmuseum, NGA, Google Arts. Só PD/CC0/CC BY/CC BY-SA, com licença conferida na fonte.
  2. **Placeholder + query de busca + legenda** para o palestrante escolher.
  3. **IA** só com `--imagens-ia`/`permitirIA: true` e só atmosférica (luz, textura, paisagem). **Nunca** figura sagrada ou cena evangélica.
- **Dignidade**: nada de kitsch, devocionalismo ou anacronismo; em dúvida, placeholder.
- **Direitos**: cada imagem em `slides/<slug>/assets/creditos.json` (`arquivo, titulo, autor, ano, licenca, fonte_url, atribuicao`) + crédito no slide via `<!-- _footer: '...' -->`. **Baixar** para `slides/<slug>/assets/` (< ~500 KB; `sips` se preciso), nunca hotlink.
- **Marp/tema `isabel`**: usar layout dividido `![bg right:45%](assets/x.jpg)`. Texto escuro sobre imagem fica ilegível — **não** usar `![bg]` full-bleed nem `brightness:` até existir uma classe de texto claro no tema (criar a classe é válido; estilo inline por slide, não). Slide de imagem leva pouco ou nenhum texto.
- **Handoff**: `/palestra` (estágio Iconografia) só **propõe** cena + 2-3 candidatos com licença; `/slides` baixa e coloca o escolhido pelo palestrante.
