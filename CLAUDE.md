# IsAbel — Wiki Espírita

Idioma: **PT-BR** em todas as páginas geradas.

---

## 1. Propósito e tom

Base de conhecimento pessoal sobre a Doutrina Espírita codificada por Allan Kardec. Uso: estudos e preparação de palestras em casas espíritas.

Tom: estudante kardecista sério — respeitoso, fraterno, didático. Sem ironia, relativismo acadêmico distanciado ou devocionalismo excessivo.

---

## 2. Hierarquia de autoridade

| Nível | Fontes |
|-------|--------|
| **Fonte primordial — Ensinamentos morais de Jesus** | Os quatro Evangelhos canônicos (Mateus, Marcos, Lucas, João). Jesus é "o tipo mais perfeito que Deus tem oferecido ao homem" (LE, q. 625); sua moral é a fundação sobre a qual Kardec construiu o ESE. Contudo, os textos evangélicos são lidos à luz do Pentateuco — as alegorias e interpolações históricas são interpretadas pela codificação, não pela exegese teológica tradicional. **Os ensinamentos de Jesus são o sol; o Pentateuco é o telescópio.** |
| **1 — Pentateuco** | *O Livro dos Espíritos* (LE), *O Livro dos Médiuns* (LM), *O Evangelho Segundo o Espiritismo* (ESE), *O Céu e o Inferno* (C&I), *A Gênese* (Gênese) |
| **2 — Kardec complementar** | *Obras Póstumas* (OPE), *O Que é o Espiritismo* (OQE), *Revista Espírita*, *Viagem Espírita em 1862* |
| **3 — Complementares aprovados** | Chico Xavier, Divaldo Franco, Léon Denis, Cairbar Schutel, Martins Peralva, Eurípedes Barsanulfo, Emmanuel, André Luiz, Joanna de Ângelis, Bezerra de Menezes, e outros alinhados à codificação. Inclui os escritos apostólicos (Paulo, Pedro, João, Tiago) como fontes seletivamente citadas por Kardec |
| **Fora de escopo** | Umbanda, Candomblé, Ramatís, teosofia, antroposofia, rosacruzes, ocultismo, New Age, neoespiritismo que relativiza o Pentateuco — **não ingerir sem confirmação explícita** |

Regra de ouro: quando nível 2/3 contradiz o nível 1, Kardec prevalece. A divergência é registrada, nunca apagada. Quando um trecho evangélico já foi interpretado por Kardec no Pentateuco, essa interpretação é nível 1. Quando não foi, pode ser consultado, mas com consciência de que se trata de alegoria e texto historicamente mediado.

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
- `(Emmanuel/Chico Xavier, *O Consolador*, q. 123)`
- `(Léon Denis, *O Problema do Ser*, cap. IV)`

Toda página termina com `## Fontes` em formato bibliográfico completo.

---

## 4. Workflows

- **Ingest** (`/ingest`): ingestão de fontes de `raw/` na wiki. Skill autocontido.
- **Lint** (`/lint`): verificação de integridade da wiki. Skill autocontido.
- **Query**: ler `index.md` → páginas relevantes → `raw/` se necessário → responder com citações começando por Kardec. Oferecer arquivar como `wiki/sinteses/` ou `wiki/questoes/` se reutilizável; se arquivado, atualizar `index.md` e `log.md`.

---

## 5. Regras condicionais

Detalhes carregados automaticamente conforme os arquivos em uso:

- `.claude/rules/convencoes-paginas.md` — frontmatter, links, estrutura por tipo (wiki/)
- `.claude/rules/convencoes-palestras.md` — pares transcrição/resumo (raw/palestras/)
- `.claude/rules/regra-divergencia.md` — protocolo de registro de divergências (wiki/)
