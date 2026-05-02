---
paths:
  - "wiki/**"
---

# Frontmatter, links e estrutura por tipo

## Frontmatter YAML obrigatório

```yaml
---
tipo: conceito | obra | personalidade | questao | aprofundamento | sintese | divergencia
fontes: [LE, ESE]
tags: [reencarnacao, moral]
url: https://...          # opcional — URL da fonte original (YouTube, site, etc.)
atualizado_em: YYYY-MM-DD
status: rascunho | ativo | revisar
---
```

Para `tipo: obra`, completar com o bloco `direitos:` — schema e tabela de detentores em `convencoes-direitos.md` (carrega ao editar `wiki/obras/**`). Para taxonomia de tags hierárquicas (`obra/`, `lei/`, `grau/`, `tema/`, `autor/`), ver `convencoes-tags.md`.

## Links e slugs

- Links estilo Obsidian: `[[wiki/conceitos/reencarnacao]]`, `[[wiki/obras/livro-dos-espiritos]]`.
- **Referências a `raw/` também são wikilinks**, nunca código em backticks. Sempre sem extensão `.md`.
  - ✅ `Edição: [[raw/kardec/pentateuco/genese]].`
  - ❌ `[Edição em \`raw/kardec/pentateuco/genese.md\`]` — backticks viram inline code, o colchete sem `()` ou `[[]]` não vira link.
  - ❌ `Disponível em: \`raw/.../arquivo.md\`.` — mesmo problema.
- Slugs: minúsculas, sem acento, hífen (`reencarnacao`, `lei-de-causa-e-efeito`).

## Estrutura por tipo

- **obras/**: Cabeçalho · Dados bibliográficos (incluir `**Texto integral:** [[raw/<caminho>]]` quando a fonte existir em `raw/`; incluir `**Fonte original:** [YouTube](url)` + embed `![](url)` quando houver vídeo/áudio online; na seção Fontes, incluir `Edição: [[raw/<caminho>]].` quando a fonte existir em `raw/`, ou `Disponível em: <url>` quando houver URL externa) · Estrutura · Resumo por parte · Temas centrais · Conceitos tratados · Personalidades citadas · Divergências · Fontes.
- **conceitos/**: Definição curta · Ensino de Kardec · Desdobramentos · Aplicação prática · Divergências · Páginas relacionadas · Fontes.
- **personalidades/**: Identificação · Papel · Obras associadas · Citações relevantes · Páginas relacionadas · Fontes.
- **questoes/**: Q&A direta ancorada em **uma única questão ou item pontual** do Pentateuco — questão numerada de LE/LM/OQE (com "Resposta dos Espíritos") ou item pontual de C&I/ESE/Gênese (ex.: C&I, 1ª parte, cap. VII, item 16). Estrutura: Pergunta (literal da obra, quando for LE/LM/OQE, ou reformulada pelo estudante) · Citação literal (Resposta dos Espíritos ou item da obra) · Comentário de Kardec · Análise · Conceitos relacionados · Fontes.
- **aprofundamentos/**: Estudo sistemático de um **tema ou bloco doutrinário** (subseção do LE, capítulo do ESE, conjunto de itens de C&I, etc.). Estrutura: Contexto doutrinário · Análise item a item ou por eixos · Síntese · Aprofundamento · Conceitos relacionados · Fontes. Use este tipo para material de palestra que cobre múltiplas questões/itens.
- **sinteses/**: Pergunta motivadora · Análise · Conclusão · Páginas referenciadas · Fontes.
- **divergencias/**: ver regra de divergência.
