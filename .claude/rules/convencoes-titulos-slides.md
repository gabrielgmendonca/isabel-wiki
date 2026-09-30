---
paths:
  - "slides/**"
  - ".claude/skills/slides/**"
---

# Títulos de palestra e de parte

Título de wiki é verbete de índice; título de palestra é anunciado a uma plateia. **Regra obrigatória: título do deck e títulos de parte nunca iguais aos headings da página wiki de origem** — escrever, não herdar. "Parte 1" sem nome não é título.

**Padrões, em ordem de preferência**:
1. **Palavra de Jesus ou Kardec, verbatim** — "Bem-aventurados os misericordiosos"; "Ajuda-te a ti mesmo, que o céu te ajudará".
2. **Cena + tese** — "'Atire a primeira pedra': a indulgência não é fraqueza, é justiça".
3. **Afirmação contestável** (default para partes) — "Ninguém é irrecuperável"; "O futuro jamais se fecha".

**Antipadrões**: "X e Y" ("Expiação e arrependimento"); telegráfico com dois-pontos ("Dor: Rigidez"); parte sem nome; nominalização abstrata ("A tríade", "O excesso íntimo"); título que repete a pergunta-ponte seguinte.

**Comprimento**: capa ≤ ~12 palavras; parte ≤ ~8.

Validação: `validate_candidates.py --tipo titulo|secao` antes de propor; `<!-- skill: renomear título da parte -->` é obrigatório; o CI (`slide_titulos`) barra parte sem nome.
