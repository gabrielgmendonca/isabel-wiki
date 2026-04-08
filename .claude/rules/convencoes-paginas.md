---
paths:
  - "wiki/**"
---

# Convenções de páginas da wiki

## Frontmatter YAML obrigatório

```yaml
---
tipo: conceito | obra | entidade | questao | sintese | divergencia
fontes: [LE, ESE]
tags: [reencarnacao, moral]
url: https://...          # opcional — URL da fonte original (YouTube, site, etc.)
atualizado_em: YYYY-MM-DD
status: rascunho | ativo | revisar
---
```

## Links e slugs

- Links estilo Obsidian: `[[wiki/conceitos/reencarnacao]]`, `[[wiki/obras/livro-dos-espiritos]]`.
- Slugs: minúsculas, sem acento, hífen (`reencarnacao`, `lei-de-causa-e-efeito`).

## Estrutura por tipo

- **obras/**: Cabeçalho · Dados bibliográficos (incluir `**Texto integral:** [[raw/<caminho>]]` quando a fonte existir em `raw/`; incluir `**Fonte original:** [YouTube](url)` + embed `![](url)` quando houver vídeo/áudio online; incluir `Disponível em: <url>` na seção Fontes) · Estrutura · Resumo por parte · Temas centrais · Conceitos tratados · Entidades citadas · Divergências · Fontes.
- **conceitos/**: Definição curta · Ensino de Kardec · Desdobramentos · Aplicação prática · Divergências · Páginas relacionadas · Fontes.
- **entidades/**: Identificação · Papel · Obras associadas · Citações relevantes · Páginas relacionadas · Fontes.
- **questoes/**: Pergunta literal · Resposta dos Espíritos literal · Comentário de Kardec · Análise · Conceitos relacionados · Fontes.
- **sinteses/**: Pergunta motivadora · Análise · Conclusão · Páginas referenciadas · Fontes.
- **divergencias/**: ver regra de divergência.
