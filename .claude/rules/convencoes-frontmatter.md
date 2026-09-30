---
paths:
  - "wiki/**"
---

# Frontmatter, links e estrutura por tipo

```yaml
---
tipo: conceito | obra | personalidade | questao | aprofundamento | sintese | divergencia | capitulo-biblico | livro-biblico
fontes: [LE, ESE]
tags: [reencarnacao, moral]
url: https://...          # opcional — fonte original
atualizado_em: YYYY-MM-DD
status: rascunho | ativo | revisar
---
```

`tipo: obra` exige também o bloco `direitos:` (rule carregada em `wiki/obras/**`); `personalidade`/`obra` aceitam `aliases:`.

**Links**: estilo Obsidian, sem `.md` — `[[wiki/conceitos/reencarnacao]]`. Referência a `raw/` também é wikilink (`[[raw/kardec/pentateuco/genese]]`), nunca caminho em backticks. Slugs: minúsculas, sem acento, hífen.

**Estrutura por tipo**:
- **obras/**: Cabeçalho · Dados bibliográficos (`**Texto integral:** [[raw/<caminho>]]` se existir em raw; `**Fonte original:** [YouTube](url)` + embed `![](url)` se houver mídia) · Estrutura · Resumo por parte · Temas centrais · Conceitos tratados · Personalidades citadas · Divergências · Fontes (`Edição: [[raw/<caminho>]].` ou `Disponível em: <url>`).
- **conceitos/**: Definição curta · Ensino de Kardec · Desdobramentos · Aplicação prática · Divergências · Páginas relacionadas · Fontes.
- **personalidades/**: Identificação · Papel · Obras associadas · Citações relevantes · Páginas relacionadas · Fontes.
- **questoes/**: ancorada em **uma** questão (LE/LM/OQE) ou item pontual (C&I/ESE/Gênese). Pergunta · Citação literal · Comentário de Kardec · Análise · Conceitos relacionados · Fontes.
- **aprofundamentos/**: estudo de um tema ou bloco (subseção do LE, capítulo do ESE…), típico de palestra. Contexto doutrinário · Análise item a item ou por eixos · Síntese · Aprofundamento · Conceitos relacionados · Fontes.
- **sinteses/**: Pergunta motivadora · Análise · Conclusão · Páginas referenciadas · Fontes.
- **divergencias/**: ver regra de divergência.
- **biblia/<livro>/<cap>.md** (`capitulo-biblico`): `# <Livro> <N>` · cada versículo sob `## <N>` · sem Fontes. Frontmatter mínimo: `livro`, `capitulo`, `testamento: NT|AT`, `fontes: [NT]|[AT]`; sem `direitos:`, `grau/*` nem `tema/*`.
- **biblia/<livro>/index.md** (`livro-biblico`): `# <Livro>` · nota de contexto · capítulos como wikilinks · link para a página-âncora em `wiki/obras/`.
