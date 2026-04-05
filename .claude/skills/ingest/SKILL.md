---
name: ingest
description: Ingere uma nova fonte de raw/ na wiki IsAbel seguindo o workflow da seção 6 do CLAUDE.md — lê a fonte, discute pontos-chave com o usuário, cria página da obra, atualiza conceitos/entidades, flagga divergências com Kardec, atualiza index.md e log.md. Use quando o usuário disser "faça ingest de X", "acabei de adicionar X em raw/", ou invocar /ingest.
---

# Ingest de fonte na wiki IsAbel

Esta skill executa o procedimento padronizado de ingest de uma nova fonte na wiki espírita IsAbel. Todo conteúdo gerado é em **PT-BR**.

## Quando usar

Gatilhos:
- "faça ingest de X"
- "acabei de adicionar X em raw/, faça o ingest"
- `/ingest <caminho>`
- Qualquer pedido para processar uma fonte nova e integrá-la à wiki.

## Passo 0 — Pré-checagem de escopo (obrigatório)

Antes de ler a fonte:

1. Identifique autor e obra a partir do nome do arquivo e/ou caminho em `raw/`.
2. Classifique o nível de autoridade conforme **seção 2 do CLAUDE.md**:
   - Nível 1 (Pentateuco de Kardec), Nível 2 (Kardec complementar), ou Nível 3 (complementares aprovados) → siga adiante.
   - **Fora de escopo** (Umbanda, Candomblé, Ramatís, teosofia, antroposofia, rosacruzes, ocultismo genérico, New Age, neoespiritismo que relativiza o Pentateuco) → **PARE**. Informe o usuário do conflito e **aguarde confirmação explícita** antes de prosseguir.
   - Autor desconhecido ou ambíguo → pergunte ao usuário antes de classificar.

## Passos do workflow (seção 6 do CLAUDE.md)

### Passo 1 — Ler

Leia o arquivo em `raw/` com a ferramenta `Read`. Se for PDF grande, leia em partes.

### Passo 2 — Conversar (human-in-the-loop)

Apresente ao usuário **5–10 pontos-chave** extraídos da fonte e **aguarde confirmação** sobre o que ele quer destacar. **Não escreva nenhuma página da wiki antes dessa confirmação.** Ingest é uma fonte por vez — não batch-ingerir.

### Passo 3 — Criar página da obra/autor

Crie `wiki/obras/<slug>.md` para obras, ou `wiki/entidades/<slug>.md` para perfil de autor. Use a estrutura por tipo definida na **seção 5 do CLAUDE.md**:

- **obras/**: Cabeçalho · Dados bibliográficos · Estrutura · Resumo por parte · Temas centrais · Conceitos tratados · Entidades citadas · Divergências (se houver) · Fontes.
- **entidades/**: Identificação · Papel · Obras associadas · Citações relevantes · Páginas relacionadas · Fontes.

Inclua frontmatter YAML obrigatório:
```yaml
---
tipo: obra | entidade
fontes: [LE, ESE, ...]
tags: [...]
atualizado_em: YYYY-MM-DD
status: rascunho | ativo
---
```

### Passo 4 — Extrair e atualizar entidades e conceitos

Para cada entidade/conceito mencionado na fonte:

- **Se a página já existe** em `wiki/conceitos/<slug>.md` ou `wiki/entidades/<slug>.md` → **atualize consolidando** a nova informação. **Não apague conteúdo prévio.** Integre, não substitua.
- **Se não existe** → crie nova página seguindo a estrutura da seção 5 do CLAUDE.md.

Use links Obsidian no formato `[[wiki/conceitos/<slug>]]` para cross-references.

### Passo 5 — Checar alinhamento com Kardec

Para fontes de **nível 2 ou 3**, confronte cada afirmação doutrinária relevante com o Pentateuco. Se houver divergência (ou aparente divergência), aplique o procedimento de 3 partes da **seção 3 do CLAUDE.md**:

1. Na página da obra/autor, inserir bloco:
   ```markdown
   > [!warning] Divergência com Kardec
   > <descrição curta>
   > Ver [[wiki/divergencias/<slug>]].
   ```
2. Criar/atualizar `wiki/divergencias/<slug-da-divergencia>.md` com: posição de Kardec (com citação do Pentateuco), posição do complementar (com citação), análise, status (`aberta` ou `conciliada`).
3. Na página do conceito afetado, adicionar seção "Divergências" com link para a página criada.

Em dúvida se é divergência real → registrar como `status: aberta` e perguntar ao usuário.

### Passo 6 — Atualizar index.md

Adicione as páginas novas em `index.md` nas seções correspondentes (Obras, Conceitos, Entidades, Divergências, etc.), cada uma com uma linha de resumo e link.

### Passo 7 — Append em log.md

Adicione ao final de `log.md`:
```
## [YYYY-MM-DD] ingest | <título da fonte>
<2-3 frases sobre o que foi feito, quantas páginas criadas/atualizadas>
```
Use a data de hoje (disponível no contexto do sistema).

### Passo 8 — Reportar

Liste ao usuário todos os arquivos criados e atualizados.

---

## Lembretes invioláveis

- **Idioma**: PT-BR em 100% do conteúdo gerado.
- **Hierarquia de autoridade**: quando fonte nível 2/3 contradiz Kardec, **Kardec prevalece** — a divergência é registrada, nunca apagada (seção 2 do CLAUDE.md).
- **Citação obrigatória**: toda afirmação doutrinária precisa de citação no formato da **seção 4 do CLAUDE.md** (ex.: `(LE, q. 150)`, `(ESE, cap. XVII, item 4)`, `(Emmanuel/Chico Xavier, *O Consolador*, q. 123)`).
- **Seção `## Fontes`** ao final de toda página, em formato bibliográfico completo.
- **Slugs**: minúsculas, sem acento, hífen como separador (`lei-de-causa-e-efeito`, não `Lei_de_Causa_e_Efeito`).
- **Tom editorial**: estudante sério kardecista — respeitoso, fraterno, didático. Sem ironia, sem relativismo acadêmico, sem devocionalismo excessivo.
- **Human-in-the-loop**: o passo 2 é um gate obrigatório. Nunca escrever páginas antes da confirmação do usuário.

---

## Referência

Esta skill implementa as seções 2, 3, 4, 5 e 6 do `CLAUDE.md` do projeto. Em dúvidas sobre edge cases, consulte essas seções diretamente em vez de improvisar.
