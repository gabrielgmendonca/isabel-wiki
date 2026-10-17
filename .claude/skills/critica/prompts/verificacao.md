# Prompt do subagente de VERIFICAÇÃO adversarial (1 por achado de eixo 1/2)

> Lido pelo subagente cético lançado no Passo 4 do `/critica`. O prompt do Agent só
> traz `CRÍTICA` (o JSON da página), `ÍNDICE` (posição em `deferred`), `LENTE` e `SAÍDA`.

Sua tarefa é TENTAR REFUTAR um achado da crítica — só confirme se não conseguir derrubá-lo. Default `refuted` quando a evidência não se sustentar; `uncertain` quando ficar genuinamente em dúvida. Um falso-positivo custa caro: vira rascunho + item no ROADMAP §11 que só o Gabriel fecha.

## Procedimento

1. Leia `<CRÍTICA>` e pegue o item `deferred[<ÍNDICE>]` (0-based). Leia a linha correspondente da página (`path` do JSON) para ver o contexto.
2. Re-rode `uv run python scripts/cite.py <SIGLA> "<ref>"` para CADA locus do Pentateuco envolvido e confira o texto LITERAL. "Não encontrada" pode ser limite do parser — não é prova de fabricação.
3. Para fonte complementar, re-busque via `mcp__qmd__query` (`collections=["raw"]`, com `intent`).
4. Aplique a lente indicada em `LENTE`:
   - **Eixo 1:** a divergência é REAL e estrutural, ou se dissolve com leitura kardecista correta / já está registrada na wiki (`> [!warning]`, `wiki/divergencias/`)?
   - **Eixo 2:** a citação realmente NÃO sustenta a afirmação? Paráfrase legítima (locus válido, sentido preservado) é `refuted`.

Você não edita nenhum arquivo além de `<SAÍDA>`.

## Saída

Grave em `<SAÍDA>` (Write) o JSON, sem cercas de código, e responda só "ok":

```json
{"status": "confirmed | refuted | uncertain", "note": "por que — com o texto do cite.py re-rodado quando aplicável"}
```
