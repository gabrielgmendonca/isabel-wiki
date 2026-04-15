---
name: lint
description: Verifica a integridade e consistência da wiki IsAbel — roda script Python para checks determinísticos e complementa com análise LLM. Use com /lint, "faça lint", ou "verifique a wiki".
---

# /lint

Gatilhos: `/lint` · "faça lint" · "verifique a wiki"

## Passo 1 — Rodar script de validação

Executar a partir da raiz do projeto:

```bash
uv run python .claude/skills/lint/scripts/lint_wiki.py
```

No CI, o workflow usa `python3` (o runner não tem `uv`) — não alterar.

Flags disponíveis:
- `--check NAME` (repetível): rodar apenas os checks listados. Ex: `--check broken_links --check frontmatter`.
- `--skip NAME` (repetível): pular os checks listados.
- `--check-urls`: habilita `broken_urls` (opt-in; I/O externo, pode atrasar).

Quando o usuário pedir "rode só X" ou "pule Y", traduzir para as flags correspondentes. Nomes válidos: `broken_links`, `index_broken`, `index_missing`, `frontmatter`, `orphan_pages`, `fontes_missing`, `citation_format`, `rascunho_stale`, `divergencias_aberta`, `missing_concept_pages`, `pentateuco_completo`, `status_projeto`, `broken_urls`, `tag_taxonomy`.

Ler o JSON de saída. Se o script falhar, reportar o erro ao usuário e parar.

## Passo 2 — Apresentar achados determinísticos

Agrupar os resultados do script por severidade:

### Erros (corrigir)
- **broken_links** — wikilinks apontando para arquivos inexistentes.
- **index_broken** — entradas do `index.md` apontando para arquivos que não existem.
- **frontmatter** — campos obrigatórios ausentes ou valores inválidos de `tipo`/`status`.
- **pentateuco_completo** — alguma das 5 obras do Pentateuco ausente em `wiki/obras/`.

### Avisos (revisar)
- **index_missing** — arquivos em `wiki/` ausentes do `index.md` (use `index: false` no frontmatter para excluir).
- **orphan_pages** — páginas sem nenhum link de entrada de outras páginas da wiki (index.md não conta). Nota: personalidades do C&I 2ª parte podem ser naturalmente órfãs — destacar mas não tratar como problema grave.
- **fontes_missing** — seção `## Fontes` ausente ou vazia.
- **citation_format** — citações com sigla conhecida mas formato fora do padrão da seção 4.
- **rascunho_stale** — páginas com `status: rascunho` há mais de 14 dias.
- **tag_taxonomy** — tags `lei/` fora da taxonomia canônica ou `obra/` inconsistentes com `fontes`.
- **broken_urls** — URLs externas retornando erro (só aparece se `--check-urls` foi passado).

### Info
- **divergencias_aberta** — divergências com `status: aberta`.
- **missing_concept_pages** — links para conceitos que ainda não têm página própria.
- **status_projeto** — contagens na prosa do `index.md` ("N fontes complementares", "~N páginas") divergentes do real. Cosmético, atualizar quando conveniente.

Para cada categoria com `count > 0`, listar os itens de forma concisa.

## Passo 3 — Análise LLM (complementar ao script)

Se houver muitos achados em `citation_format`, `fontes_missing`, `missing_concept_pages` ou `divergencias_aberta` (>~5 itens combinados), delegar esta análise a um subagente Explore para preservar o contexto principal. Passar ao subagente o JSON dos achados relevantes e pedir um relatório resumido seguindo as subseções 3a–3d abaixo. Caso contrário, fazer no main mesmo.

### 3a. Citações suspeitas
Para cada item em `citation_format`, avaliar:
- Falso positivo? (formato válido que o regex não reconheceu) → descartar.
- Citação real fora do formato da seção 4? → sugerir correção.

### 3b. Conceitos sem página
Para cada item em `missing_concept_pages`, avaliar:
- O conceito merece página própria? (frequência, importância doutrinária)
- Ação sugerida: criar página / corrigir link / ignorar.

### 3c. Sugestões de fontes para lacunas (check 9 — exclusivo LLM)
Ler as páginas flaggadas em `fontes_missing`. Para cada uma com `## Fontes` vazia ou rasa, sugerir fontes do Pentateuco ou nível 2/3 que poderiam enriquecer.

### 3d. Divergências abertas
Para cada divergência `status: aberta` flaggada como possivelmente incompleta (`possibly_incomplete: true`), ler a página e avaliar se a análise está de fato incompleta. Sugerir próximos passos.

## Passo 4 — Compilar relatório

Apresentar ao usuário em formato limpo:

```
## Relatório de lint — YYYY-MM-DD

### Erros (corrigir)
- ...

### Avisos (revisar)
- ...

### Sugestões (opcional)
- ...

**Total: N achados** (X erros, Y avisos, Z sugestões)
```

## Passo 5 — Atualizar log.md

Append em `log.md`:

```
## [YYYY-MM-DD] lint | N achados
<2–3 frases resumindo os principais achados>
```

## Regras

- **Não corrigir nada automaticamente.** Lint é apenas diagnóstico.
- O usuário decide o que corrigir e quando.
- Se o usuário pedir para corrigir um achado específico, fazê-lo como operação separada.
