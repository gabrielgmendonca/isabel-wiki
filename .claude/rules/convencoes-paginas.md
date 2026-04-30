---
paths:
  - "wiki/**"
---

# Convenções de páginas da wiki

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

## Direitos autorais (obras nível 3)

Páginas `tipo: obra` declaram a situação de direitos da obra original via campo aninhado `direitos:`. Habilita aviso ao leitor (renderizado pelo transformer Quartz `CopyrightNotice`) e checks de lint específicos para obras protegidas.

```yaml
direitos:
  detentor: dominio-publico | FEB | Boa-Nova | LEAL | IDE | desconhecido
  ano_dp_estimado: 2059        # opcional; ano estimado de entrada em DP (pmcs Brasil = 70 anos após morte)
  url_aquisicao: https://...   # opcional, recomendado para obras protegidas
  observacao: "..."            # opcional
```

| Detentor | Quando usar |
|---|---|
| `dominio-publico` | Kardec (m. 1869), Léon Denis (m. 1927), Cairbar Schutel (m. 1938), Eurípedes Barsanulfo (m. 1918), textos bíblicos. **Não preencher** `ano_dp_estimado` quando DP. |
| `FEB` | Federação Espírita Brasileira — Chico Xavier (toda a série André Luiz, Emmanuel, Humberto de Campos), Bezerra de Menezes (publicações via FEB), Martins Peralva. |
| `Boa-Nova` | Editora Boa Nova — Francisco do Espírito Santo Neto / Hammed. |
| `LEAL` | Livraria Espírita Alvorada — Joanna de Ângelis / Divaldo Franco. |
| `IDE` | Instituto de Difusão Espírita — Yvonne Pereira e outros. |
| `desconhecido` | Detentor não identificado ou ambíguo (palestras, autores nível 4 sem mapeamento claro). Backlog manual. |

Default conservador: ausência do campo `direitos:` em `tipo: obra` é tratada pelo lint como `info` (vai virar `warning` após backfill em massa).

## Taxonomia de tags

Tags livres continuam permitidas. Além delas, **cinco namespaces hierárquicos** (com `/`) habilitam navegação temática no Quartz (que gera `/tags/<slug>/` automaticamente para cada tag em uso):

| Namespace | Conjunto | Origem | Aplica a |
|-----------|----------|--------|----------|
| `obra/` | 8 valores | derivado de `fontes:` (script) | todas |
| `lei/` | 10 valores | atribuído quando trata de lei moral | todas |
| `grau/` | 3 valores | nível de complexidade | exceto `obra`/`trilha` |
| `tema/` | 12 valores | eixo doutrinário (1-3 por página) | todas |
| `autor/` | 12+ valores | linhagem autoral | todas |

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

### `grau/` — grau de complexidade

Conjunto fechado em 3 valores. Sinaliza para o leitor o nível de leitura recomendado e alimenta as trilhas de estudo.

| Tag | Quando aplicar |
|-----|---------------|
| `grau/introdutorio` | primeiros passos, definições básicas, questões pontuais simples, parábolas (Q&A direto) |
| `grau/intermediario` | conceitos doutrinários estruturais, leitura sistemática de obra, ESDE-tier |
| `grau/avancado` | aprofundamentos, sínteses comparativas, divergências, cruzamentos entre obras |

Default heurístico por `tipo:` (aplicado por `scripts/enrich_tags_grau.py`; revisar caso a caso):

| `tipo:` | Default | Observação |
|---------|---------|------------|
| `questao` | `grau/introdutorio` | Q&A pontual ancorado em uma questão/item |
| `parabola` | `grau/intermediario` | aplicação prática, mas exige leitura kardequiana |
| `personalidade` | `grau/intermediario` | (skip stubs) |
| `conceito` | `grau/intermediario` | base estrutural da doutrina |
| `aprofundamento` | `grau/avancado` | estudo sistemático |
| `sintese` | `grau/avancado` | comparativos e panorâmicas |
| `divergencia` | `grau/avancado` | exige Pentateuco como referência |
| `obra` | — | **não recebe** `grau/*` (a obra não tem grau próprio) |
| trilhas (`wiki/trilhas/*` ou tag `trilha`) | — | **não recebem** `grau/*` (trilha agrupa páginas de vários graus) |

### `tema/` — eixo doutrinário

Conjunto fechado em 12 valores. Páginas devem ter **1-3** `tema/*` (preferir 1; 2-3 quando o conteúdo atravessa eixos).

| Tag | Eixo doutrinário |
|-----|------------------|
| `tema/deus` | Deus, providência, criação, atributos divinos |
| `tema/espiritos` | natureza dos espíritos, hierarquia, escala espírita, anjos/demônios |
| `tema/encarnacao` | reencarnação, perispírito, corpo, escolha de provas |
| `tema/mediunidade` | comunicação espiritual, fenômenos, médiuns, obsessão |
| `tema/moral` | leis morais (umbrella), virtudes, vícios, conduta |
| `tema/jesus` | vida, ensinos, parábolas, divindade, missão de Jesus |
| `tema/vida-futura` | pós-morte, céu/inferno, espíritos felizes/sofredores, penas futuras |
| `tema/sociedade` | família, lar, casamento, instituições, política |
| `tema/livre-arbitrio` | liberdade, expiação, fatalidade, responsabilidade |
| `tema/prece-caridade` | adoração, prece, caridade prática |
| `tema/sofrimento` | dor, expiação, provas, suicídio, tédio da vida |
| `tema/historia-doutrina` | codificação, divulgação, biografia de Kardec/médiuns |

Atribuição manual (não automatizada): o significado é semântico e errar em massa vira ruído permanente. O lint `check_tag_coverage` (info-level) lista páginas sem nenhum `tema/*` para passes incrementais.

### `autor/` — linhagem autoral

Conjunto fechado dos autores nível 2/3 mais citados. Para psicografias, marcar **ambos** espírito + médium (ex.: livro do Emmanuel/Chico Xavier → `autor/emmanuel, autor/chico-xavier`).

| Tag | Quando aplicar |
|-----|---------------|
| `autor/kardec` | Pentateuco e complementares Kardec (LE, LM, ESE, C&I, Gênese, OPE, OQE, RE) |
| `autor/leon-denis` | obras de Léon Denis |
| `autor/chico-xavier` | médium — psicografias da série André Luiz, Emmanuel, Humberto de Campos, etc. |
| `autor/emmanuel` | espírito autor (psicografias via Chico Xavier) |
| `autor/andre-luiz` | espírito autor (Nosso Lar, série dos planos da vida) |
| `autor/humberto-de-campos` | espírito autor |
| `autor/joanna-de-angelis` | espírito autor (psicografias via Divaldo) |
| `autor/divaldo-franco` | médium |
| `autor/bezerra-de-menezes` | espírito autor (psicografias via Divaldo, e biografia) |
| `autor/cairbar-schutel` | autor encarnado |
| `autor/hammed` | espírito autor (psicografias via Espírito Santo Neto) |
| `autor/paulo` | apóstolo (epístolas paulinas) |
| `autor/joao` | apóstolo (Evangelho de João, 1-3 João, Apocalipse) |
| `autor/pedro` | apóstolo (1-2 Pedro) |
| `autor/tiago` | apóstolo (Epístola de Tiago) |

O conjunto é extensível: novos autores nível 3/4 podem ser adicionados quando houver páginas que os exijam — atualizar esta tabela e o conjunto canônico no lint na mesma PR.

`scripts/enrich_tags_autor.py` faz backfill mecânico a partir de `fontes:` e tags livres canônicas (`andre-luiz`, `paulo`, `chico-xavier` etc.).

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
