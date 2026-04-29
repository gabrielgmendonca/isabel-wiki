---
name: glossario
description: Sugere termos culturais/históricos não-doutrinários (alfarroba, denário, fariseu, samaritano…) para adicionar ao dicionário data/dicionario.json — o JSON consumido por scripts/wrap_glossary_terms.py no build do Quartz para envolver primeira ocorrência em <abbr>. Use com /glossario, "atualizar dicionário", "sugerir termos para o glossário".
---

# /glossario

Gatilhos: `/glossario` · "atualizar dicionário" · "sugerir termos para o glossário"

Esta skill propõe **adições** ao glossário cultural/histórico (`data/dicionario.json`), não a doutrinas. Conceitos doutrinários (espírito, perispírito, médium, fluido…) viram página própria em `wiki/conceitos/`, não entrada de dicionário — ver CLAUDE.md §1.

## Passo 1 — Rodar script de sugestão

```bash
uv run python .claude/skills/glossario/scripts/sugerir_termos.py --top 30
```

Flags disponíveis:
- `--top N` — quantos candidatos retornar (padrão 30).
- `--min-count N` — recorrência mínima do termo na wiki (padrão 2).
- `--max-pages N` — termo é candidato apenas se aparece em ≤ N páginas distintas (padrão 15). Termos muito disseminados são doutrinários, não culturais.
- `--min-ratio F` — concentração mínima em contexto bíblico/histórico (padrão 0.7). Termos de uso geral em PT-BR têm ratio baixo.

Saída JSON em stdout. Cada candidato traz:
- `term`, `count`, `biblical_count`, `biblical_ratio`, `pages_distinct`, `pages_sample`, `contexts` (até 3 snippets).

## Passo 2 — Triar candidatos com o usuário

A heurística é leve por design — sempre haverá ruído (verbos arcaicos isolados, adjetivos comuns, nomes próprios que escaparam). Filtrar mentalmente em três pilhas:

- **Aceitar**: substantivo concreto com referencial cultural/histórico claro (`escribas`, `denário`, `centurião`, `iníquo`, `cabritos` no contexto do juízo).
- **Rejeitar — verbos/adjetivos comuns**: `queres`, `mostram`, `morrerem`, `existimos`, `antiga`. Não merecem tooltip.
- **Rejeitar — doutrinário/meta**: tudo que tem página em `wiki/conceitos/` ou que é jargão espírita. Esses termos pertencem ao corpo principal da wiki, não ao dicionário.
- **Marginal — pedir opinião do usuário**: termos que dependem de quem é o público das palestras (`romano`, `genealogia`, `prólogo`).

Apresentar a triagem ao usuário em formato compacto:

```
Aceitar (N):
- escriba (8 ocorrências, 6 páginas)
- denário (3 ocorrências, 2 páginas)
- ...

Marginal (N):
- romano — vale o tooltip ou contexto basta?
- ...

Rejeitar (N):
- queres, mostram, antiga, existimos — verbos/adjetivos comuns
```

Aguardar decisão. Não escrever no JSON antes da aprovação.

## Passo 3 — Propor definições

Para cada termo aceito, escrever uma definição **curta** (≤ 25 palavras), no estilo das já existentes em `data/dicionario.json`:

- Descreve o que é, não como é usado na frase.
- Inclui referência cultural quando agrega (parábola onde aparece, século, povo).
- Sem opiniões, sem doutrinação espírita — é dicionário, não comentário.

Exemplos do estilo já estabelecido:

> `"alfarroba": "Fruto da alfarrobeira, vagem doce usada como alimento de animais (especialmente porcos) na Palestina antiga; aparece na parábola do Filho Pródigo (Lucas 15:16)."`
>
> `"escriba": "Erudito da Lei mosaica responsável por copiar, ensinar e interpretar as Escrituras hebraicas."`

Mostrar todas as definições propostas em bloco, e pedir aprovação ou ajustes antes de gravar.

## Passo 4 — Atualizar `data/dicionario.json`

Adicionar as novas entradas no objeto `termos`, mantendo ordem alfabética não estritamente — o agrupamento natural por tema (moedas juntas, instituições juntas) é mais legível. Não tocar no campo `_comment`.

## Passo 5 — Preview de wraps

Rodar o script de wrap em modo `--check` para ver onde os novos termos passariam a aparecer:

```bash
uv run python scripts/wrap_glossary_terms.py --check wiki/
```

Reportar ao usuário a contagem de páginas que ganharão wraps com os termos novos. Diff de exemplo (1-2 linhas) para confirmar que o resultado faz sentido.

## Passo 6 — Atualizar `log.md`

Registrar a expansão:

```
## [YYYY-MM-DD] glossario | <N termos novos: termo1, termo2, ...>
<1-2 frases sobre o motivo da expansão — ex.: "ingestão recente de Atos exigiu novos termos do contexto romano-judaico do I século">
```

## Regras

- **Não rodar `--apply`.** O wrap acontece no build do Quartz, não no source.
- **Conceitos doutrinários NÃO entram aqui.** Se o usuário pedir para incluir "perispírito" ou "médium", recusar e sugerir página própria em `wiki/conceitos/`.
- **Definições curtas.** Tooltip não é parágrafo — máximo ~25 palavras, uma frase ou duas.
- **Termo cultural ≠ termo raro.** Uma palavra arcaica que não é cultural-específica (`existimos`, `morrerem`) não entra. Critério: agrega informação contextual que o leitor não tem?
