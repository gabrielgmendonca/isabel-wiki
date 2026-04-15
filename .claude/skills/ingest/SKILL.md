---
name: ingest
description: Ingere uma nova fonte de raw/ na wiki IsAbel — lê a fonte, discute pontos-chave com o usuário, cria página da obra, atualiza conceitos/entidades, flagga divergências com Kardec, atualiza index.md e log.md. Use quando o usuário disser "faça ingest de X", "acabei de adicionar X em raw/", ou invocar /ingest.
---

# /ingest

Gatilhos: "faça ingest de X" · "acabei de adicionar X em raw/" · `/ingest <caminho>`

## Fase de análise (plan mode)

Ao iniciar, **entre em plan mode** (`EnterPlanMode`). Isso impede escrita acidental antes da confirmação do usuário.

### Passo 0 — Pré-checagem de escopo

1. Identifique autor e obra pelo nome/caminho do arquivo em `raw/`.
2. Classifique conforme seção 2 do CLAUDE.md:
   - Nível 1, 2 ou 3 → siga adiante.
   - **Fora de escopo** → PARE. Informe o conflito e aguarde confirmação explícita antes de prosseguir.
   - Autor desconhecido/ambíguo → pergunte ao usuário antes de classificar.

### Passos 1–2 — Leitura e discussão

1. **Ler** o arquivo em `raw/`.
2. **Conversar**: apresentar 5–10 pontos-chave e aguardar confirmação. **Não escrever nenhuma página antes disso.**

## Fase de escrita

Após confirmação do usuário, **saia de plan mode** (`ExitPlanMode`) e execute:

3. **Criar** `wiki/obras/<slug>.md` ou `wiki/personalidades/<slug>.md`.
4. **Extrair** personalidades e conceitos: atualizar páginas existentes (consolidar, não substituir) ou criar novas.
5. **Checar alinhamento com Kardec**: flaggar divergências conforme regra de divergência (`.claude/rules/regra-divergencia.md`).
6. **Atualizar `index.md`** com links e resumos das páginas novas.
7. **Append em `log.md`**: `## [YYYY-MM-DD] ingest | <título>` + 2–3 frases.
8. **Reportar** arquivos criados/atualizados.

**Passo 3 — link ao texto integral:** nos Dados bibliográficos da página de obra, incluir `**Texto integral:** [[raw/<caminho-da-fonte>]]` apontando para o arquivo original em `raw/`.
