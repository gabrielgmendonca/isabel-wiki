# IsAbel — Wiki Espírita

Idioma: **PT-BR** em todas as páginas geradas.

---

## 1. Propósito e tom

Base de conhecimento pessoal sobre a Doutrina Espírita codificada por Allan Kardec. Uso: estudos e preparação de palestras em casas espíritas.

Tom: estudante kardecista sério — respeitoso, fraterno, didático. Sem ironia, relativismo acadêmico distanciado ou devocionalismo excessivo.

**Princípio de crescimento**: a wiki deve crescer com o tempo. Cada pergunta doutrinária é oportunidade de capitalizar conhecimento — transformar resposta efêmera em página citável que alimenta buscas futuras. O default é arquivar; só não arquivar quando o conteúdo for claramente operacional ou efêmero.

---

## 2. Hierarquia de autoridade

| Nível | Fontes |
|-------|--------|
| **Fonte primordial — Ensinamentos morais de Jesus** | Os quatro Evangelhos canônicos (Mateus, Marcos, Lucas, João). Jesus é "o tipo mais perfeito que Deus tem oferecido ao homem" (LE, q. 625); sua moral é a fundação sobre a qual Kardec construiu o ESE. Contudo, os textos evangélicos são lidos à luz do Pentateuco — as alegorias e interpolações históricas são interpretadas pela codificação, não pela exegese teológica tradicional. **Os ensinamentos de Jesus são o sol; o Pentateuco é o telescópio.** |
| **1 — Pentateuco** | *O Livro dos Espíritos* (LE), *O Livro dos Médiuns* (LM), *O Evangelho Segundo o Espiritismo* (ESE), *O Céu e o Inferno* (C&I), *A Gênese* (Gênese) |
| **2 — Kardec complementar** | *Obras Póstumas* (OPE), *O Que é o Espiritismo* (OQE), *Revista Espírita*, *Viagem Espírita em 1862* |
| **3 — Complementares consagrados** | Autores de referência doutrinária amplamente citados nas casas espíritas: Chico Xavier, Divaldo Franco, Léon Denis, Cairbar Schutel, Martins Peralva, Eurípedes Barsanulfo, Emmanuel, André Luiz, Joanna de Ângelis, Bezerra de Menezes. Inclui os escritos apostólicos (Paulo, Pedro, João, Tiago) como fontes seletivamente citadas por Kardec |
| **4 — Complementares secundários** | Autores/médiuns alinhados à codificação e coerentes com Kardec em tese e método, mas sem o peso doutrinário dos consagrados de nível 3. Exemplos: Francisco do Espírito Santo Neto / Hammed, palestras isoladas de estudiosos espíritas. Úteis para estudo; citar com consciência do tier |
| **Fora de escopo** | Umbanda, Candomblé, Ramatís, teosofia, antroposofia, rosacruzes, ocultismo, New Age, neoespiritismo que relativiza o Pentateuco — **não ingerir sem confirmação explícita** |

Regra de ouro: quando nível 2/3/4 contradiz o nível 1, Kardec prevalece. A divergência é registrada, nunca apagada. Quando um trecho evangélico já foi interpretado por Kardec no Pentateuco, essa interpretação é nível 1. Quando não foi, pode ser consultado, mas com consciência de que se trata de alegoria e texto historicamente mediado.

Caso prático — trecho evangélico aparenta divergir do Pentateuco: se Kardec já fixou interpretação no ESE/Gênese/LE, ela prevalece (não a leitura literal do Evangelho). Se ele não tratou o trecho, antes de tomar como doutrina considerar (a) contexto alegórico, (b) interpolação ou tradução, (c) cultura semita do I século. Em qualquer caso, registrar como divergência se for citar.

Ver [[wiki/sinteses/hierarquia-de-autoridade]] para análise completa.

---

## 3. Citação obrigatória

Toda afirmação doutrinária precisa de citação:

- `(LE, q. 150)` · `(LE, Introdução, item IV)`
- `(LM, 2ª parte, cap. XX, item 230)`
- `(ESE, cap. XVII, item 4)`
- `(C&I, 1ª parte, cap. VI)`
- `(Gênese, cap. XI, item 13)`
- `(RE, jan/1858, p. 12)` · `(OPE, "Manifestações dos Espíritos")`
- `(Emmanuel / Chico Xavier, *O Consolador*, q. 123)`
- `(Léon Denis, *O Problema do Ser*, cap. IV)`

**Obras psicografadas**: citar como `Autor espiritual / Médium` (ex.: `Emmanuel / Chico Xavier`, `André Luiz / Chico Xavier`, `Humberto de Campos / Chico Xavier`). Conferir o frontmatter de `raw/mediuns/<médium>/<obra>.md` (campo `Autor espiritual:`) antes de citar — o médium não é o autor. Não inferir autor a partir do médium.

Toda página termina com `## Fontes` em formato bibliográfico completo.

---

## 4. Workflows

- **Ingest** (`/ingest`): ingestão de fontes de `raw/` na wiki. Skill autocontido.
- **Lint** (`/lint`): verificação de integridade da wiki. Skill autocontido.
- **Slides** (`/slides <página>`): gera apresentação Marp (PPTX + PDF) no padrão socrático Q&A. Skill autocontido.
- **Stats** (`/stats`): regenera `wiki/sinteses/estatisticas-da-wiki.md` com métricas determinísticas. Skill autocontido.
- **Auto-link de citações** (`scripts/link_citations.py`): no build do CI, citações inline do Pentateuco viram links Markdown para Kardecpedia (nível do capítulo), e citações de complementares no formato `(Autor, *Obra*, ref)` viram wikilinks para `wiki/obras/<slug>` quando a página existir. Autor escreve `(LE, q. 990)` cru — a transformação acontece sobre a cópia em `/tmp/quartz/content`, sem alterar arquivos do repo. Mapeamento em `data/kardec-mapping.json`, regerável com `scripts/build_kardec_mapping.py`.

### Query

Workflow para responder a uma pergunta usando a wiki como base.

**Como buscar.** `qmd` é MCP server local (BM25 + vetorial sobre 920 documentos). Coleções: `raw` (713 docs, fonte: Kardec, Léon Denis, Chico Xavier, palestras) e `wiki` (207 docs, curado, com frontmatter e citações). Tipos de busca:

- `lex` — BM25 keyword. Use para sigla, número de questão, termo técnico exato.
- `vec` — semântico. Use para conceito, sinônimos, paráfrase.
- `hyde` — hipotético. Use quando você sabe como a resposta *parece*, não as palavras-chave.

Combinar `lex` + `vec` na mesma chamada cobre a maioria dos casos. Sempre fornecer `intent` para desambiguar. Buscar primeiro em `wiki/`, descer para `raw/` se necessário. Fallback sem qmd: ler `wiki/sinteses/catalogo.md` (a home `index.md` é landing de trilhas, não listagem).

**Citar começando por Kardec.** Respeitar a hierarquia (§2): Jesus/Pentateuco antes de complementares. Usar os formatos de §3.

**Default = oferecer arquivar.** Toda resposta substantiva merece virar página citável. Escolher o tipo:

- `wiki/sinteses/` — panorama, conexões entre temas, comparativos entre obras/autores.
- `wiki/aprofundamentos/` — estudo sistemático de um tema ou bloco doutrinário (subseção do LE, capítulo do ESE, conjunto de itens de C&I).
- `wiki/questoes/` — Q&A direta ancorada em **uma única** questão ou item pontual do Pentateuco (questão numerada de LE/LM/OQE ou item de C&I/ESE/Gênese).

Só pular o oferecimento quando a pergunta for puramente operacional. Se arquivado, listar a nova página em `wiki/sinteses/catalogo.md` e registrar entrada em `log.md`.

---

## 5. Regras condicionais

Rules em `.claude/rules/*.md` são injetadas automaticamente no contexto pelo hook `PreToolUse` (`.claude/hooks/inject-rules.py`) quando o arquivo-alvo de `Edit`/`Write`/`MultiEdit` bate com o glob declarado no frontmatter `paths:` da rule. Fora disso, não entram no contexto.

- `.claude/rules/convencoes-paginas.md` — `paths: wiki/**` — frontmatter, links, estrutura por tipo
- `.claude/rules/convencoes-palestras.md` — `paths: raw/palestras/**` — pares transcrição/resumo
- `.claude/rules/convencoes-slides.md` — `paths: slides/**, .claude/skills/slides/**` — padrão socrático Marp
- `.claude/rules/regra-divergencia.md` — `paths: wiki/**` — protocolo de registro de divergências
- `.claude/rules/scripts.md` — `paths: .claude/skills/**` — `uv run python` para scripts locais
