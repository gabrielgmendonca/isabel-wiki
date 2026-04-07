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
| **1 — Pentateuco** | *O Livro dos Espíritos* (LE), *O Livro dos Médiuns* (LM), *O Evangelho Segundo o Espiritismo* (ESE), *O Céu e o Inferno* (C&I), *A Gênese* (Gênese) |
| **2 — Kardec complementar** | *Obras Póstumas* (OPE), *O Que é o Espiritismo* (OQE), *Revista Espírita*, *Viagem Espírita em 1862* |
| **3 — Complementares aprovados** | Chico Xavier, Divaldo Franco, Léon Denis, Cairbar Schutel, Martins Peralva, Eurípedes Barsanulfo, Emmanuel, André Luiz, Joanna de Ângelis, Bezerra de Menezes, e outros alinhados à codificação |
| **Fora de escopo** | Umbanda, Candomblé, Ramatís, teosofia, antroposofia, rosacruzes, ocultismo, New Age, neoespiritismo que relativiza o Pentateuco — **não ingerir sem confirmação explícita** |

Regra de ouro: quando nível 2/3 contradiz o nível 1, Kardec prevalece. A divergência é registrada, nunca apagada.

---

## 3. Regra de divergência

Quando nível 2/3 contradiz o Pentateuco:

1. Na página da obra/autor, inserir:
   ```markdown
   > [!warning] Divergência com Kardec
   > <descrição curta>
   > Ver [[wiki/divergencias/<slug>]].
   ```
2. Criar/atualizar `wiki/divergencias/<slug>.md` com: posição de Kardec (citação), posição do complementar (citação), análise (divergência real / mudança de ênfase / aprofundamento / erro de interpretação) e status: `aberta` ou `concluída`.
3. Na página do conceito afetado, adicionar seção "Divergências" com link.

Em dúvida → registrar `status: aberta` e perguntar ao usuário.

---

## 4. Citação obrigatória

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

## 5. Convenções de páginas

Frontmatter YAML obrigatório:
```yaml
---
tipo: conceito | obra | entidade | questao | sintese | divergencia
fontes: [LE, ESE]
tags: [reencarnacao, moral]
url: https://...          # opcional — URL da fonte original (YouTube, site, etc.)
atualizado_em: YYYY-MM-DD
status: rascunho | ativo | revisar
---
```

Links estilo Obsidian: `[[wiki/conceitos/reencarnacao]]`, `[[wiki/obras/livro-dos-espiritos]]`.

Slugs: minúsculas, sem acento, hífen (`reencarnacao`, `lei-de-causa-e-efeito`).

Estrutura por tipo:
- **obras/**: Cabeçalho · Dados bibliográficos (incluir `**Texto integral:** [[raw/<caminho>]]` quando a fonte existir em `raw/`; incluir `**Fonte original:** [YouTube](url)` + embed `![](url)` quando houver vídeo/áudio online; incluir `Disponível em: <url>` na seção Fontes) · Estrutura · Resumo por parte · Temas centrais · Conceitos tratados · Entidades citadas · Divergências · Fontes.
- **conceitos/**: Definição curta · Ensino de Kardec · Desdobramentos · Aplicação prática · Divergências · Páginas relacionadas · Fontes.
- **entidades/**: Identificação · Papel · Obras associadas · Citações relevantes · Páginas relacionadas · Fontes.
- **questoes/**: Pergunta literal · Resposta dos Espíritos literal · Comentário de Kardec · Análise · Conceitos relacionados · Fontes.
- **sinteses/**: Pergunta motivadora · Análise · Conclusão · Páginas referenciadas · Fontes.
- **divergencias/**: ver seção 3.

---

## 5.1. Convenções de `raw/palestras/`

Palestras de YouTube são armazenadas em pares:
- `<TÍTULO>.md` — transcrição completa (com URL da fonte na primeira linha)
- `summary-<TÍTULO>.md` — resumo gerado a partir da mesma transcrição

---

## 6. Workflow de ingest

1. **Ler** o arquivo em `raw/`.
2. **Conversar**: apresentar 5–10 pontos-chave e aguardar confirmação. **Não escrever nenhuma página antes disso.**
3. **Criar** `wiki/obras/<slug>.md` ou `wiki/entidades/<slug>.md`.
4. **Extrair** entidades e conceitos: atualizar páginas existentes (consolidar, não substituir) ou criar novas.
5. **Checar alinhamento com Kardec**: flaggar divergências conforme seção 3.
6. **Atualizar `index.md`** com links e resumos das páginas novas.
7. **Append em `log.md`**: `## [YYYY-MM-DD] ingest | <título>` + 2–3 frases.
8. **Reportar** arquivos criados/atualizados.

Ingest é feito uma fonte por vez, com o usuário no circuito.

---

## 7. Workflow de query

1. Ler `index.md` para mapear páginas candidatas.
2. Ler as páginas relevantes.
3. Se insuficiente, consultar `raw/` diretamente.
4. Responder com citações (seção 4), começando pelo que Kardec diz.
5. Se substancial e reutilizável, oferecer arquivar como `wiki/sinteses/<slug>.md` ou `wiki/questoes/<slug>.md`.
6. Se arquivada, atualizar `index.md` e `log.md`: `## [YYYY-MM-DD] query | <pergunta resumida>`.

---

## 8. Workflow de lint

Sob demanda, verificar e reportar (não corrigir silenciosamente):
- Divergências `status: aberta` sem análise completa.
- Páginas órfãs (sem links de entrada).
- Conceitos mencionados em múltiplas páginas sem página própria.
- Cross-references faltando.
- `## Fontes` vazia ou incompleta.
- Citações fora do formato da seção 4.
- `index.md` desatualizado vs. arquivos reais em `wiki/`.
- Páginas com `status: rascunho` há muito tempo.
- Sugestões de fontes para lacunas.

Append em `log.md`: `## [YYYY-MM-DD] lint | <N achados>`.
