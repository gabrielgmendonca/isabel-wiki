---
paths:
  - "wiki/**"
---

# Diagramas Mermaid (mapas conceituais)

O Quartz (clonado no CI na tag `v4.4.0`) renderiza Mermaid nativamente: o transformer `ObsidianFlavoredMarkdown()` — já ativo em `quartz.config.ts` — traz `mermaid: true` por default, detecta blocos ` ```mermaid `, marca a classe CSS `mermaid` e renderiza client-side via CDN, respeitando o tema claro/escuro. Não há plumbing a fazer: escrever o bloco já basta. O que falta é disciplina editorial — sem ela o diagrama vira ruído paralelo ao grafo do Quartz e fonte de drift de nomenclatura. Esta política fixa **onde o diagrama mora, o que ele pode dizer e o que continua sendo obrigação da prosa**.

## Princípio: prosa primeiro, mapa ilustra

O diagrama **nunca substitui** a prosa fundamentada nem a citação. Ele é mnemônico e estrutural — resume uma relação que o texto já estabeleceu e citou. Toda afirmação doutrinária continua exigindo `(LE, q. X)` na prosa adjacente (CLAUDE.md §3); o diagrama não carrega citação e **não pode introduzir afirmação doutrinária que não esteja sustentada no corpo da página**.

Consequência prática: se um conceito aparece como nó no diagrama, ele deve aparecer também como **wikilink real** (`[[wiki/...]]`) na prosa ou em "Páginas relacionadas". Nós Mermaid **não são wikilinks** — não entram no grafo do Quartz, não contam para `broken_links`, não são indexados pela busca full-text nem aparecem no PDF/EPUB futuro (§7). O diagrama complementa o grafo; não o alimenta.

## Onde o diagrama mora

Na **própria página-conceito, síntese ou aprofundamento que ele ilustra** — junto da seção cujo conteúdo ele resume. **Não criar um diretório de mapas dedicado em `wiki/`** nem páginas-diagrama autônomas: um mapa sem a prosa que o fundamenta é uma afirmação sem citação. Posicionar o bloco *depois* do texto/tabela que ele sintetiza, não antes (prosa primeiro).

## Rótulos dos nós

- **Forma canônica, sempre.** Personalidade ou obra → o H1 da página correspondente (ver `convencoes-aliases.md`): "Allan Kardec", não "Rivail"; "O Livro dos Espíritos", não "Le Livre des Esprits". Conceito → o título da página-conceito. Mundos habitados → a forma canônica de `convencoes-mundos-habitados.md`. O diagrama é prosa nova: vale a mesma regra anti-drift.
- **PT-BR.** Rótulos, legendas de aresta e títulos em português.
- **Siglas de citação (LE, ESE, LM…) como nó** só quando o nó representa a obra enquanto fonte e o contexto já as definiu (ex.: mapa da hierarquia de autoridade). Em mapa de conceitos, preferir o nome por extenso.

## Sintaxe segura

- Envolver em aspas todo rótulo com acento, pontuação, `&`, `:` ou parêntese: `A["Lei de Causa e Efeito"]`, `B["C&I — 1ª parte"]`. Acento funciona dentro de aspas; fora delas o parser pode quebrar.
- Quebra de linha no nó: `<br/>`.
- **Não fixar cores** via `%%{init}%%` ou `style` com hex — cor hard-coded quebra num dos modos. O Quartz v4.4.0 inicializa o Mermaid com o tema stock (`default`/`dark`), sem integração com a paleta do site; o ajuste de contraste é **global e único**, em `quartz-overrides/styles/custom.scss` (mapeia o SVG do Mermaid para os tokens CSS `--light`/`--dark`/`--secondary`/`--darkgray` etc., que o Quartz já troca por tema). Tunar cor de diagrama = editar esse arquivo, nunca o bloco ` ```mermaid `.
- Preferir `graph TD` / `graph LR` (mapa conceitual e fluxo). `mindmap`, `timeline`, `sequenceDiagram` só quando a forma realmente pede — e testar no preview, pois dependem da versão do Mermaid servida pelo CDN.

## Interação com os pré-processadores

`scripts/link_citations.py` e `scripts/wrap_glossary_terms.py` **pulam blocos cercados** (regex `` ```.*?``` ``). Portanto, dentro do bloco Mermaid:

- `(LE, q. 150)` **não** vira link para a Kardecpedia — não escrever citação no diagrama esperando auto-link; citar na prosa/legenda fora do bloco.
- Termos do glossário cultural **não** ganham `<abbr>` — idem.

Isso é desejável (auto-link dentro do diagrama quebraria a sintaxe), mas significa que o diagrama é um artefato textualmente "morto" para o pipeline: tudo que precisa ser linkável ou citável vive fora dele.

## Fallback textual obrigatório

Todo diagrama vem acompanhado de uma frase, lista ou tabela que comunica a mesma relação em texto. Razões: leitor sem JS / leitor de tela / export PDF-EPUB (§7) não veem o SVG; e a busca full-text do Quartz indexa texto, não o desenho. Na prática isso já ocorre quando se respeita "prosa primeiro" — a tabela ou os parágrafos que o diagrama resume *são* o fallback.

## Quando NÃO usar

- Quando uma tabela ou lista comunica melhor (dados tabulares, enumeração simples).
- Relações com mais de ~12-15 nós — ilegível no client e pesado de renderizar.
- Conteúdo narrativo/argumentativo — diagrama é para estrutura e relação, não para discurso.
- Só para "decorar" uma página que já está clara sem ele.

## Exemplo canônico

`wiki/sinteses/hierarquia-de-autoridade.md` — diagrama da escala de autoridade logo após a tabela "visão geral" e a regra de ouro (prosa primeiro), rótulos na forma canônica, aresta tracejada para a regra "Kardec prevalece". É a referência de estilo; novos mapas seguem esse padrão.

## Lint

**Sem check determinístico hoje** (decisão do escopo "validar + convencionar", 2026-05-17). Os checks de `lint_wiki.py` que operam sobre prosa (`broken_links`, `citation_format`, `canonical_names`, `mundos_habitados_naming`) já ignoram blocos cercados, então um bloco Mermaid não gera falso-positivo — mas, pelo mesmo motivo, **drift de nomenclatura dentro de um rótulo Mermaid não é detectado por nenhum check**. É o risco aberto conhecido. Candidato a um `check_mermaid_labels` (severity `info`, varrendo rótulos `["..."]` contra o mapa alias→canônico já construído por `check_canonical_names`) quando houver volume de diagramas que justifique calibrar. Registrado no ROADMAP §7.
