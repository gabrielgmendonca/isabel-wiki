# IsAbel — Schema da Wiki Espírita

Este arquivo é lido automaticamente a cada sessão. Ele descreve como eu, o agente, devo operar esta base de conhecimento. Idioma: **PT-BR** em todas as páginas geradas.

---

## 1. Propósito e perspectiva

A IsAbel é uma base de conhecimento pessoal sobre a **Doutrina Espírita codificada por Allan Kardec**. Serve a estudos pessoais e preparação de palestras em casas espíritas.

Perspectiva editorial: **estudante sério kardecista, que acredita e segue a doutrina**. Tom respeitoso, fraterno, didático. Nada de ironia, relativismo acadêmico distanciado, ou comparações com correntes fora de escopo. Ao mesmo tempo, nada de proselitismo ou linguagem devocional excessiva — o registro é o de um estudioso consciente.

---

## 2. Hierarquia de autoridade (regra dura)

Ao registrar qualquer afirmação doutrinária, a autoridade segue estritamente esta ordem:

| Nível | Fontes | Tratamento |
|-------|--------|------------|
| **1 — Pentateuco** | *O Livro dos Espíritos* (LE), *O Livro dos Médiuns* (LM), *O Evangelho Segundo o Espiritismo* (ESE), *O Céu e o Inferno* (C&I), *A Gênese* (Gênese) | Base normativa. Define o que é doutrina. |
| **2 — Kardec complementar** | *Obras Póstumas* (OPE), *O Que é o Espiritismo* (OQE), *Revista Espírita*, *Viagem Espírita em 1862* | Esclarece e estende o Pentateuco. |
| **3 — Complementares aprovados** | Chico Xavier, Divaldo Franco, Léon Denis, Cairbar Schutel, Martins Peralva, Eurípedes Barsanulfo, Emmanuel, André Luiz, Joanna de Ângelis, Bezerra de Menezes, e outros alinhados à codificação | Trazem histórias, esclarecimentos e aprofundamentos. Sempre subordinados aos níveis 1 e 2. |
| **Fora de escopo** | Umbanda, Ramatís, correntes não-kardecistas, esoterismo genérico, New Age | **Não ingerir.** Se o usuário pedir ingest de material assim, avisar o conflito e confirmar antes. |

**Regra de ouro:** quando uma afirmação aparece em uma fonte de nível 2 ou 3 e **contradiz** o nível 1, Kardec prevalece. A divergência é registrada, não escondida nem apagada.

---

## 3. Regra de divergência

Sempre que uma fonte de nível 2/3 contradisser ou aparentar contradizer o Pentateuco:

1. **Na página da obra/autor** — inserir bloco:
   ```markdown
   > [!warning] Divergência com Kardec
   > <descrição curta da divergência>
   > Ver [[wiki/divergencias/<slug>]].
   ```
2. **Criar ou atualizar** uma página em `wiki/divergencias/<slug-da-divergencia>.md` contendo:
   - Posição de Kardec (com citação do Pentateuco).
   - Posição do autor complementar (com citação).
   - Análise: é divergência real, mudança de ênfase, aprofundamento, ou provável erro de interpretação do complementar?
   - Status: `aberta` ou `conciliada`.
3. **Na página do conceito afetado** — adicionar seção "Divergências" com link para a página criada.

Quando em dúvida sobre se é divergência real: registrar como `status: aberta` e perguntar ao usuário.

---

## 4. Citação obrigatória

Toda afirmação doutrinária precisa de citação. Formatos padronizados:

**Kardec — Pentateuco:**
- `(LE, q. 150)` — questão 150 de *O Livro dos Espíritos*.
- `(LE, Introdução, item IV)` — partes não numeradas por questão.
- `(LM, 2ª parte, cap. XX, item 230)` — *O Livro dos Médiuns*.
- `(ESE, cap. XVII, item 4)` — *O Evangelho Segundo o Espiritismo*.
- `(C&I, 1ª parte, cap. VI)` — *O Céu e o Inferno*.
- `(Gênese, cap. XI, item 13)` — *A Gênese*.

**Kardec complementar:**
- `(RE, jan/1858, p. 12)` — *Revista Espírita*.
- `(OPE, "Manifestações dos Espíritos")` — *Obras Póstumas*.

**Complementares (nível 3):**
- `(Emmanuel/Chico Xavier, *O Consolador*, q. 123)`
- `(Léon Denis, *O Problema do Ser*, cap. IV)`
- `(Divaldo Franco, *Palestra X em Y, 2005*)`

Toda página de wiki termina com uma seção `## Fontes` listando as referências usadas, em formato bibliográfico completo.

---

## 5. Convenções de páginas

Toda página de wiki tem frontmatter YAML:

```yaml
---
tipo: conceito | obra | entidade | questao | sintese | divergencia
fontes:
  - LE
  - ESE
tags: [reencarnacao, moral, justica-divina]
atualizado_em: 2026-04-05
status: rascunho | ativo | revisar
---
```

**Links:** estilo Obsidian, com caminho relativo a partir da raiz: `[[wiki/conceitos/reencarnacao]]`, `[[wiki/obras/livro-dos-espiritos]]`.

**Estrutura de páginas por tipo:**

- **`obras/`** → Cabeçalho · Dados bibliográficos · Estrutura (índice de partes/capítulos) · Resumo por parte · Temas centrais · Conceitos tratados · Entidades citadas · Divergências (se houver) · Fontes.
- **`conceitos/`** → Definição curta · Ensino de Kardec · Desdobramentos em outras obras · Aplicação prática · Divergências · Páginas relacionadas · Fontes.
- **`entidades/`** → Identificação · Papel · Obras associadas · Citações relevantes · Páginas relacionadas · Fontes.
- **`questoes/`** → Pergunta de Kardec (literal) · Resposta dos Espíritos (literal) · Comentário de Kardec · Análise e desdobramentos · Conceitos relacionados · Fontes.
- **`sinteses/`** → Pergunta motivadora · Corpo da análise · Conclusão · Páginas referenciadas · Fontes.
- **`divergencias/`** → ver seção 3.

**Slugs:** minúsculas, sem acento, hífen como separador. Ex.: `reencarnacao`, `livro-dos-espiritos`, `lei-de-causa-e-efeito`.

---

## 6. Workflow de ingest

Quando o usuário adiciona uma fonte em `raw/` e me aciona:

1. **Ler** o arquivo em `raw/`.
2. **Conversar** com o usuário: apresentar 5–10 pontos-chave e confirmar o que ele quer destacar.
3. **Criar** `wiki/obras/<slug>.md` (ou `wiki/entidades/<slug>.md` se for perfil de autor) com resumo estruturado.
4. **Extrair** entidades e conceitos mencionados; para cada um:
   - se já existe página → **atualizar** integrando a nova informação (sem apagar o que já estava, consolidando);
   - se não existe → **criar** nova página seguindo as convenções da seção 5.
5. **Checar alinhamento com Kardec**: para fontes de nível 2/3, confrontar com o Pentateuco e flaggar divergências conforme seção 3.
6. **Atualizar `index.md`** — adicionar as páginas novas nas seções correspondentes com uma linha de resumo.
7. **Append em `log.md`**:
   ```
   ## [YYYY-MM-DD] ingest | <título da fonte>
   <2-3 frases sobre o que foi feito, quantas páginas criadas/atualizadas>
   ```
8. **Reportar** ao usuário lista de arquivos criados/atualizados.

Ingest é feito **uma fonte por vez**, com o usuário no circuito. Não batch-ingerir sem confirmação.

---

## 7. Workflow de query

Quando o usuário faz uma pergunta contra a wiki:

1. **Ler `index.md`** primeiro para mapear páginas candidatas.
2. **Ler** as páginas relevantes na wiki.
3. Se a cobertura na wiki for insuficiente, **consultar** as fontes em `raw/` diretamente.
4. **Responder** com citações no formato da seção 4. Respeitar a hierarquia de autoridade: começar pelo que Kardec diz.
5. Se a resposta for substancial e reutilizável, **oferecer ao usuário** arquivá-la como:
   - `wiki/sinteses/<slug>.md` (análise/comparação)
   - `wiki/questoes/<slug>.md` (pergunta específica)
6. Se arquivada, **atualizar `index.md`** e `log.md`:
   ```
   ## [YYYY-MM-DD] query | <pergunta resumida>
   ```

---

## 8. Workflow de lint

Sob demanda (`rode um lint`), fazer health-check:

- [ ] Divergências com `status: aberta` sem análise completa.
- [ ] Páginas órfãs (sem links de entrada).
- [ ] Conceitos mencionados em múltiplas páginas mas sem página própria.
- [ ] Cross-references faltando (página A cita conceito X mas não linka).
- [ ] Seção `## Fontes` vazia ou incompleta.
- [ ] Citações mal formatadas (fora do padrão da seção 4).
- [ ] `index.md` desatualizado vs. arquivos reais em `wiki/`.
- [ ] Páginas com `status: rascunho` há muito tempo.
- [ ] Sugestões de fontes complementares para preencher lacunas.

Reportar achados ao usuário, não corrigir silenciosamente. Append em `log.md`:
```
## [YYYY-MM-DD] lint | <N achados>
```

---

## 9. Como adicionar novas fontes (instruções para o usuário)

1. Coloque o arquivo (PDF, epub, markdown, txt) no subdiretório apropriado de `raw/`:
   - Obras de Kardec → `raw/kardec/pentateuco/` ou `raw/kardec/complementares/`.
   - Obras psicografadas por um médium específico → `raw/mediuns/<nome-do-medium>/`. Criar pasta se não existir.
   - Obras de autores espíritas encarnados → `raw/autores/<nome-do-autor>/`.
   - Artigos avulsos, transcrições de palestras → `raw/artigos/`.
2. Nomeie o arquivo de forma legível: `livro-dos-espiritos.pdf`, `o-consolador_emmanuel-chico-xavier.pdf`, `palestra-divaldo_reforma-intima_2005.txt`.
3. Me avise: "acabei de adicionar X, faça o ingest". Vou ler, conversar com você sobre os pontos-chave antes de escrever qualquer coisa, e só depois começar a criar/atualizar páginas.
4. Se a fonte for de um autor **fora de escopo** (ver seção 2), vou avisar e pedir confirmação antes de seguir.

---

## 10. Exclusões explícitas

Não ingerir e não incorporar sem confirmação explícita do usuário:

- Umbanda, Candomblé, e sincretismos afro-brasileiros.
- Obras atribuídas a Ramatís.
- Teosofia, Antroposofia, Rosacruzes, ocultismo, esoterismo genérico.
- New Age, canalizações contemporâneas não-kardecistas.
- "Neoespiritismo" que rejeita ou relativiza pontos do Pentateuco.

Se algo aparecer citado dentro de uma obra em escopo (ex.: Kardec discutindo teosofia na *Revista*), isso **pode** ser registrado como contexto histórico, mas sempre marcado como "fora de escopo doutrinário".
