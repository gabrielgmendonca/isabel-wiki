---
paths:
  - "wiki/**"
quando: "```mermaid"
---

# Diagramas Mermaid

O Quartz já renderiza ` ```mermaid `; o que importa é disciplina editorial.

- **Prosa primeiro, mapa ilustra.** O diagrama fica na própria página, *depois* do texto/tabela que resume; nunca página-diagrama autônoma. Não introduz afirmação doutrinária ausente do corpo nem carrega citação (auto-link e glossário pulam blocos cercados — citar fora do bloco).
- Todo nó-conceito também aparece como wikilink real na prosa ou em "Páginas relacionadas" (nó Mermaid não entra no grafo). A prosa/tabela adjacente é o fallback textual obrigatório.
- Rótulos em PT-BR e na forma canônica (H1 da página; mundos habitados conforme a escala do ESE III, 4). Sigla (LE, ESE…) como nó só quando o nó representa a obra enquanto fonte e o contexto já a definiu; em mapa de conceitos, nome por extenso.
- Sintaxe: aspas em rótulo com acento/pontuação (`A["Lei de Causa e Efeito"]`), `<br/>` para quebra; **nunca** cor fixa (`%%{init}%%`, `style` com hex) — contraste é global em `quartz-overrides/styles/custom.scss`. Preferir `graph TD`/`LR`; `mindmap`, `timeline`, `sequenceDiagram` só quando a forma pede, e testar no preview (dependem da versão do Mermaid no CDN).
- Não usar quando tabela/lista basta, com mais de ~12-15 nós, ou para conteúdo argumentativo. Referência de estilo: `wiki/sinteses/hierarquia-de-autoridade.md`.
