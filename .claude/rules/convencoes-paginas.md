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

## Taxonomia de tags

Tags livres continuam permitidas. Além delas, dois namespaces hierárquicos (com `/`) habilitam navegação temática no Quartz:

### `obra/` — obra de origem

Derivadas **automaticamente** do campo `fontes` pelo script `scripts/enrich_tags_obra.py`. Não manter manualmente.

| Fonte | Tag |
|-------|-----|
| LE | `obra/le` |
| LM | `obra/lm` |
| ESE | `obra/ese` |
| C&I | `obra/ci` |
| Gênese | `obra/genese` |
| OPE | `obra/ope` |
| OQE | `obra/oqe` |

### `lei/` — 10 leis morais (LE, Parte 3)

Atribuídas a páginas que tratam diretamente de uma lei moral. Conjunto fechado — só os valores abaixo são válidos:

| Tag | Lei | Questões LE |
|-----|-----|-------------|
| `lei/adoracao` | Lei de Adoração | q. 649-673 |
| `lei/trabalho` | Lei do Trabalho | q. 674-685 |
| `lei/reproducao` | Lei de Reprodução | q. 686-701 |
| `lei/conservacao` | Lei de Conservação | q. 702-727 |
| `lei/destruicao` | Lei de Destruição | q. 728-765 |
| `lei/sociedade` | Lei de Sociedade | q. 766-775 |
| `lei/progresso` | Lei do Progresso | q. 776-800 |
| `lei/igualdade` | Lei de Igualdade | q. 803-824 |
| `lei/liberdade` | Lei de Liberdade | q. 825-872 |
| `lei/justica-amor-caridade` | Lei de Justiça, Amor e Caridade | q. 873-919 |

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
