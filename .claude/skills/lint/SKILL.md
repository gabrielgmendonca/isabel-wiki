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

Flags: `--check NAME` / `--skip NAME` (repetíveis) · `--check-urls` (habilita `broken_urls`, opt-in, I/O externo) · `--file PATH` (só os checks isoláveis sobre uma página; é o que o hook `lint-on-edit.py` usa — não substitui o lint global) · `--list-checks` (catálogo: nome, descrição, se roda em `--file`, se é opt-in).

O catálogo de checks é o próprio registro do script — **não** manter lista aqui. Quando o usuário pedir "rode só X" ou "pule Y", conferir o nome com `--list-checks` e traduzir para as flags.

Ler o JSON de saída. Se o script falhar, reportar o erro ao usuário e parar.

## Passo 2 — Apresentar achados determinísticos

Agrupar os resultados pela `severity` que cada check devolve no JSON (error → corrigir · warning → revisar · info). Para cada categoria com `count > 0`, listar os itens de forma concisa; se o significado de um check não for óbvio, usar a `descricao` de `--list-checks`.

Ressalvas de leitura:
- **orphan_pages**: personalidades do C&I 2ª parte podem ser naturalmente órfãs — destacar sem tratar como grave.
- **status_projeto**: cosmético; corrigir com `uv run python .claude/skills/stats/scripts/update_status.py`.
- **raw_layout**: migração via `uv run python scripts/normalize_raw_layout.py --dry-run` (e `--apply` quando aprovado).
- **slide_overflow**: estimativa geométrica, não medição — o veredito é olhar o PDF. Transbordo intencional declara `<!-- lint: overflow-esperado -->`.

## Passo 3 — Análise LLM (complementar ao script)

Delegar a um subagente Explore com `model: "haiku"` — input é compacto (JSON dos achados) e output é classificação/sugestão estruturada. Preserva o contexto principal e reduz custo. Passar ao subagente o JSON dos achados relevantes e pedir um relatório resumido seguindo as subseções 3a–3d abaixo.

Exceção: se a sessão atual já é Haiku, fazer no main mesmo (sem ganho em delegar). Se houver pouquíssimos achados (≤2 combinados em `citation_format` + `fontes_missing` + `missing_concept_pages` + `divergencias_aberta`), também fazer no main para evitar overhead de spin-up.

### 3a. Citações suspeitas
Para cada item em `citation_format`, avaliar:
- Falso positivo? (formato válido que o regex não reconheceu) → descartar.
- Citação real fora do formato do CLAUDE.md §3? → sugerir correção.

### 3b. Conceitos sem página
Para cada item em `missing_concept_pages`, avaliar:
- O conceito merece página própria? (frequência, importância doutrinária)
- Ação sugerida: criar página / corrigir link / ignorar.

### 3c. Sugestões de fontes para lacunas (exclusivo LLM)
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

## Passo 5 — Atualizar log.md (condicional)

**Diagnóstico puro não é registrado.** Logar em `log.md` somente se o usuário decidir corrigir achados a partir do relatório:

```
## [YYYY-MM-DD] lint | <descrição da correção>
<2–3 frases sobre o que foi corrigido e por quê>
```

Correção puramente cosmética (só `status_projeto` via `update_status.py`) **não** é logada — o `git log` basta.

## Regras

- **Não corrigir nada automaticamente.** Lint é apenas diagnóstico.
- O usuário decide o que corrigir e quando.
- Se o usuário pedir para corrigir um achado específico, fazê-lo como operação separada.
