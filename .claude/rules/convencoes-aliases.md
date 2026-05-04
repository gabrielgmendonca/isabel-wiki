---
paths:
  - "wiki/**"
---

# Aliases canônicos para personalidades e obras

Conforme a wiki cresce, o mesmo autor ou obra acaba sendo mencionado de várias formas — Kardec/Rivail, Chico Xavier/Francisco Cândido, *O Livro dos Espíritos*/*Le Livre des Esprits*. Drift sem política gera ruído no grafo do Quartz, dificulta busca textual e divide referências entre páginas que deveriam apontar para a mesma entidade.

A política abaixo fixa **uma forma canônica por entidade** e registra as formas alternativas como `aliases:` no frontmatter — usadas pelo lint (`check_canonical_names`) para sinalizar drift e pelo leitor humano como fonte de verdade.

## Forma canônica

A forma canônica de uma personalidade ou obra é o **H1 da página** correspondente em `wiki/personalidades/<slug>.md` ou `wiki/obras/<slug>.md`. O slug é a versão sem acento e em hífen do mesmo nome. Princípios:

- **Personalidades** — preferir o nome pelo qual a pessoa é mais conhecida no movimento espírita, não o nome civil exaustivo. "Allan Kardec", não "Hippolyte Léon Denizard Rivail". "Chico Xavier", não "Francisco Cândido Xavier". "Léon Denis", não "Hippolyte Léon Denis".
- **Obras** — título completo em PT-BR com artigo definido inicial preservado quando faz parte do título. "O Livro dos Espíritos", não "Livro dos Espíritos" nem "Le Livre des Esprits". Para subtítulos, usar o título principal sem o subtítulo (ex.: "A Gênese" e não "A Gênese, os Milagres e as Predições segundo o Espiritismo").
- **Obras psicografadas** — título da obra é a forma canônica (ex.: "O Consolador"). A coautoria mediúnica `Autor espiritual / Médium` aparece em citação parentética e em `## Fontes`, não como título.

## Frontmatter `aliases:`

```yaml
aliases:
  - "Rivail"
  - "Hippolyte Léon Denizard Rivail"
  - "Hippolyte Rivail"
```

Regras:

1. **Lista plana de strings**, uma por linha. A forma canônica (H1 da página) **não** entra em `aliases:` — ela já é canônica.
2. **Cada alias deve ser inequívoco** — string que aponta para esta entidade e nenhuma outra. "Denis" é ambíguo demais (existem outros Denis na wiki); "Léon Denis" já é canônico; um alias razoável é o nome civil completo ("Hippolyte Léon Denis"). Em dúvida, **não cadastrar**.
3. **Aliases ≥ 4 caracteres** — strings curtas geram falsos positivos catastróficos. Siglas de citação (LE, ESE, LM) **não** são aliases — são notação de citação coberta em `convencoes-frontmatter.md`.
4. **Variantes ortográficas pertinentes** entram (com ou sem acento, com ou sem hífen) quando a forma alternativa de fato circula em texto-fonte (ex.: "Joanna de Angelis" sem til ao lado de "Joanna de Ângelis").

Aplica-se a `tipo: personalidade` e `tipo: obra`. Demais tipos (`conceito`, `aprofundamento`, `sintese`, `questao`, `divergencia`) não recebem `aliases:` — são páginas analíticas, não nomes próprios.

## Uso em prosa

- **Em prosa nova**: usar a forma canônica. "Allan Kardec publicou..." e não "Rivail publicou...".
- **Quando o contexto biográfico exige a forma alternativa** (ex.: anos pré-codificação em que ainda assinava Rivail), usar wikilink com alias: `[[wiki/personalidades/allan-kardec|Rivail]]`. O link mantém a integridade do grafo; o texto preserva a precisão histórica.
- **Em blockquote citacional** (transcrição literal de fonte de época, jornal do séc. XIX, etc.), **não alterar**. O lint ignora blockquotes.

## Lint

`check_canonical_names` (severity `info`) varre o corpo de cada página e sinaliza ocorrências de alias registrado fora de wikilink. Skip por design:

- Frontmatter, blockquotes, inline code e wikilinks já existentes.
- A página canônica da própria entidade (ela introduz seus próprios aliases).
- Match exige whole-word boundary — "Denisar" não casa com alias "Denis" (e "Denis" não é alias registrável de qualquer modo, ver regra 3 acima).

A severidade é `info` deliberadamente: o sinal orienta passes incrementais, não bloqueia merge. Promover a `warning` depois de calibrar contra falso positivo.

## Backfill

`scripts/enrich_aliases.py` não é necessário hoje — o conjunto de aliases é pequeno o suficiente para edição manual. Adicionar conforme a wiki citar a mesma entidade com formas variantes (o lint vai surfar candidatos).
