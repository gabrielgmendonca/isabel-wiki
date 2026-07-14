---
name: dreno
description: Contrapeso do /critica — FECHA rascunhos em vez de abrir. Promove a `ativo` os rascunhos cujo diferido do ROADMAP §11 já foi resolvido (determinístico, zero tokens), tria os rascunhos do /ingest em esboço vs candidata, e revisa um lote pequeno de candidatas com agente barato. Feito para rodar 1×/dia via cron. Use com /dreno, /dreno N, /dreno --dry, "drenar rascunhos", "promover rascunhos".
---

# /dreno

Gatilhos: `/dreno` · `/dreno <N>` · `/dreno --dry` · cron diário (`scripts/loop-diario.sh`)

O `/critica` e o `/autocritica` **abrem** trabalho: toda página com achado doutrinário diferido vira `status: rascunho` + item no ROADMAP §11. Sem contrapeso, o loop só acumula — a medição de 2026-07-13 encontrou **158 rascunhos** e **133 itens abertos** no §11, com taxa de diferimento de **92%** (110 de 120 páginas criticadas geraram diferido). Rodar a crítica nas ~640 páginas restantes, nessa taxa, produziria ~590 novos rascunhos que ninguém drenaria.

O `/dreno` é o outro lado: **fecha**. É barato por construção — quase todo o trabalho é determinístico, e o agente só olha o resíduo ambíguo.

## Passo 1 — Promover o que é seguro (zero tokens)

```bash
uv run python .claude/skills/dreno/scripts/dreno.py promover
```

Promove a `ativo` só os buckets **C** (todos os itens do §11 fechados `[x]`) e **E** (criticada, zero diferidos). Tudo o mais fica como está.

Duas invariantes, ambas cobertas por `tests/test_dreno.py` — **não afrouxar**:

- **Não bumpa `atualizado_em`.** Se bumpasse, a página casaria o motivo `atualizado-apos-critica` do `critica_scope.py`, voltaria à fila do Opus, seria diferida de novo (92%) e viraria rascunho outra vez — moto-perpétuo queimando tokens sem mudar uma linha da wiki. Promover é transição de estado de *revisão*, não de *conteúdo*; o `content_sha` prova que o corpo é byte-idêntico.
- **Slug ambíguo nunca promove.** O §11 mistura `**wiki/conceitos/x**` (caminho) e `**x**` (slug nu), e há slugs repetidos entre diretórios (`reencarnacao`, `alma-dos-animais`, `plenitude`). Slug nu ambíguo cai no **bucket F** e nenhuma das homônimas é promovida. Cuidado ao mexer: contar só `abertos`/`fechados` **não** basta. Um item `[ ]` ambíguo bloqueia de graça (porque `abertos > 0` bloqueia), mas um item `[x]` ambíguo soma `fechados` em todas as homônimas — e `fechados > 0` é justamente a condição de *promover*. Sem o contador `ambiguos`, um único `[x]` seu, dirigido a UMA página, promovia TODAS as homônimas; a promovida por engano ia a `ativo` com diferidos doutrinários em aberto e, como o corpo não muda, nunca mais voltava à fila da crítica. O conserto humano é trocar o slug nu por caminho explícito no §11.

## Passo 2 — Anatomia do que sobrou (zero tokens)

```bash
uv run python .claude/skills/dreno/scripts/dreno.py anatomia
```

| Bucket | O que é | Ação |
|---|---|---|
| **A** | nunca-criticada — rascunho do `/ingest`, **não** é dívida da crítica | Passo 3 |
| **B** | diferido **aberto** no §11 | `rascunho` está correto — **não tocar** |
| **C** | diferido **fechado** no §11 | promovida no Passo 1 |
| **D** | crítica diferiu, sem item no §11 — rastro perdido | reportar ao humano |
| **F** | item do §11 por slug nu **ambíguo** (casa >1 página) | **não promove** — trocar por caminho explícito no §11 |
| **X** | corpo alterado depois de uma crítica limpa — veredito obsoleto | devolver à fila do `/critica` |

## Passo 3 — Triar os rascunhos do /ingest (zero tokens)

```bash
uv run python .claude/skills/dreno/scripts/dreno.py triagem --limit <N>
```

Separa o bucket A por sinais determinísticos (tem `## Fontes`, ≥250 palavras, ≥1 citação — contando **as duas** formas do projeto: sigla `(LE, q. 150)` e obra `(Autor, *Obra*, cap.)`):

- **ESBOÇO** — falta escrita, não promoção. Não é trabalho do dreno: anotar no ROADMAP §10.3 e seguir.
- **CANDIDATA** — parece completa. Vai ao Passo 4.

## Passo 4 — Revisar N candidatas com agente barato

Só aqui gasta token, e pouco. Para as **N primeiras candidatas** (default **3**; as mais antigas primeiro), lançar **um agente Haiku por página**, em paralelo:

> Leia `<página>`. Ela está `status: rascunho` e nunca passou pela crítica doutrinária. Decida **uma** coisa: ela está pronta para `ativo`?
>
> Pronta = tem `## Fontes`; as afirmações doutrinárias têm citação; nada está visivelmente incompleto (seção vazia, TODO, frase cortada); o tom é o do projeto (estudante kardecista sério).
>
> **Não** audite fidelidade doutrinária — isso é trabalho do `/critica`, não seu. Você só julga completude editorial.
>
> Responda: `{"pronta": bool, "motivo": "<1 frase>", "falta": ["<item>", ...]}`

Então, serial no main-session:

- `pronta: true` → promover **com a ferramenta**, nunca editando o frontmatter na mão:
  ```bash
  uv run python .claude/skills/dreno/scripts/dreno.py promover-pagina --path <página>
  ```
  Ela preserva `atualizado_em` (o `Edit` na mão ou o `critica_apply.py set-status` bumpariam, e a página recairia na fila do Opus) e **recusa** qualquer página fora do bucket A — o agente editorial não tem autoridade para liberar página com diferido doutrinário em aberto.
- `pronta: false` → **não** promover. Anotar no ROADMAP §10.3 o que falta, em uma linha por página.

## Passo 5 — Relatar

Uma linha: quantas promovidas (Passo 1 + Passo 4), quantas ficaram, backlog restante por bucket. Se houve mudança, registrar em `log.md`:

```
## [YYYY-MM-DD] dreno | N rascunhos promovidos a `ativo`
<1-2 frases: quantas por bucket, quantas ficaram como esboço e por quê.>
```

## Regras

- **Só fecha, nunca abre.** Se o dreno acha um problema doutrinário, ele **não** difere nem cria stub — isso é trabalho do `/critica`. Ele apenas deixa a página como rascunho e segue.
- **Bucket B é intocável.** Item aberto no §11 = decisão humana pendente. Promover ali seria publicar como `ativo` uma página com divergência doutrinária conhecida e não resolvida.
- **Conservador na dúvida.** Sinal ambíguo → não promove. O custo de deixar um rascunho a mais é zero; o de promover uma página errada é doutrinário.
- **Commit fica com o usuário** (`/ship`), como no `/autocritica`.
