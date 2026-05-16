---
paths:
  - "wiki/**"
---

# Regra de divergência

## Caso prático — trecho evangélico aparenta divergir do Pentateuco

Se Kardec já fixou interpretação no ESE/Gênese/LE, ela prevalece (não a leitura literal do Evangelho). Se ele não tratou o trecho, antes de tomar como doutrina considerar (a) contexto alegórico, (b) interpolação ou tradução, (c) cultura semita do I século. Em qualquer caso, registrar como divergência se for citar.

## Callout inline ou página própria?

Antes de criar `wiki/divergencias/<slug>.md`, decidir o peso da divergência:

- **Callout `> [!warning]` inline na página da obra, sem página de divergência** — quando a tensão é **pontual**, resolvível com leitura kardequiana clara, ou tem suporte no nível 3 que a dissolve. Perguntar: exige análise de mais de 2–3 citações? Aparece em mais de uma obra do nível 2–3? Se não a ambas, o callout inline já entrega a sinalização sem inflar `wiki/divergencias/`. Ainda assim, correlacionar com o nível 3 quando aplicável (ex.: linkar a página complementar que oferece a leitura conciliadora).
- **Página própria em `wiki/divergencias/`** (protocolo abaixo) — quando a divergência é **estrutural**: recorrente em várias obras, ou exige confronto de várias citações de ambos os lados.
- Se uma divergência **já existente** em `wiki/divergencias/` passar a se aplicar a mais uma obra, **expandir/renomear** a página existente em vez de criar nova.

## Protocolo

Quando a divergência for estrutural (nível 2/3 contradiz o Pentateuco):

1. Na página da obra/autor, inserir:
   ```markdown
   > [!warning] Divergência com Kardec
   > <descrição curta>
   > Ver [[wiki/divergencias/<slug>]].
   ```
2. Criar/atualizar `wiki/divergencias/<slug>.md` com: posição de Kardec (citação), posição do complementar (citação), análise (divergência real / mudança de ênfase / aprofundamento / erro de interpretação) e status: `aberta` ou `concluída`.
3. Na página do conceito afetado, adicionar seção "Divergências" com link.

Em dúvida → registrar `status: aberta` e perguntar ao usuário.
