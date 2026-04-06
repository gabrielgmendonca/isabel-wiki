---
name: ingest
description: Ingere uma nova fonte de raw/ na wiki IsAbel seguindo o workflow da seção 6 do CLAUDE.md — lê a fonte, discute pontos-chave com o usuário, cria página da obra, atualiza conceitos/entidades, flagga divergências com Kardec, atualiza index.md e log.md. Use quando o usuário disser "faça ingest de X", "acabei de adicionar X em raw/", ou invocar /ingest.
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

Siga os passos 1–2 da seção 6 do CLAUDE.md: ler a fonte e apresentar 5–10 pontos-chave. **Aguardar confirmação explícita do usuário.**

## Fase de escrita

Após confirmação do usuário, **saia de plan mode** (`ExitPlanMode`) e execute os passos 3–8 da seção 6 do CLAUDE.md.

**Passo 3 — link ao texto integral:** nos Dados bibliográficos da página de obra, incluir `**Texto integral:** [[raw/<caminho-da-fonte>]]` apontando para o arquivo original em `raw/`.
