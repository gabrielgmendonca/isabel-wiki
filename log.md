# Log

Histórico cronológico da wiki. Cada entrada começa com `## [YYYY-MM-DD] <tipo> | <título>`, onde `<tipo>` ∈ {`setup`, `ingest`, `query`, `lint`, `refactor`}.

Para ver as últimas N entradas: `grep "^## \[" log.md | tail -N`.

---

## [2026-04-05] setup | Estrutura inicial da wiki criada

Criados `CLAUDE.md` (schema), `index.md` (catálogo), `log.md` (este arquivo), `.gitignore` e a árvore de diretórios `raw/` e `wiki/` conforme o plano. Nenhuma página âncora foi gerada — aguardando ingest de *O Livro dos Espíritos*.

## [2026-04-05] ingest | O Livro dos Espíritos (Kardec, trad. Guillon Ribeiro, FEB)

Primeira obra ingerida. Fonte: `raw/kardec/pentateuco/WEB-Livro-dos-Espíritos-Guillon-1.pdf` (529 p., 1.019 questões).

Páginas criadas (26):
- **Obra** (1): `wiki/obras/livro-dos-espiritos.md`
- **Conceitos** (13): deus, espirito, perispirito, alma, escala-espirita, pluralidade-dos-mundos-habitados, encarnacao, reencarnacao, pluralidade-das-existencias, morte-e-pos-morte, vida-espirita, livre-arbitrio, progresso-espiritual.
- **Leis morais** (12): lei-natural, lei-de-adoracao, lei-do-trabalho, lei-de-reproducao, lei-de-conservacao, lei-de-destruicao, lei-de-sociedade, lei-do-progresso, lei-de-igualdade, lei-de-liberdade, lei-de-justica-amor-e-caridade, perfeicao-moral.
- **Entidades** (5): allan-kardec, espiritos-reveladores, sao-luis (rascunho), santo-agostinho (rascunho), jesus (rascunho).

`index.md` atualizado com catálogo completo. Nenhuma divergência registrada — fonte é nível 1 (Pentateuco).

## [2026-04-06] ingest | Re-ingestão de O Livro dos Espíritos (fonte Markdown)

Re-ingestão completa usando `raw/kardec/pentateuco/livro-dos-espiritos.md` (Markdown, 3.370 linhas) em substituição ao PDF de qualidade inferior.

Alterações:
- **Reescrita** (1): `wiki/obras/livro-dos-espiritos.md` — estrutura mais fiel, citações diretas, cobertura da Introdução (itens I–XVII), Prolegômenos e Conclusão (itens I–IX).
- **Conceitos criados** (4): `principio-vital`, `emancipacao-da-alma`, `suicidio`, `penas-e-gozos-futuros`.
- **Conceitos atualizados** (4): `alma` (tríplice acepção + links), `morte-e-pos-morte`, `vida-espirita`, `lei-de-conservacao` (cross-refs para novos conceitos).
- **Entidades atualizadas** (2): `sao-luis` e `santo-agostinho` — promovidos de rascunho a ativo, com citações nominais do LE.
- `index.md` atualizado com novos conceitos.

## [2026-04-06] ingest | O Evangelho Segundo o Espiritismo (Kardec, trad. Guillon Ribeiro)

Ingest completo do ESE. Fonte: `raw/kardec/pentateuco/evangelho-segundo-o-espiritismo.md` (5.496 linhas, 28 capítulos + Introdução).

Páginas criadas (20):
- **Obra** (1): `wiki/obras/evangelho-segundo-o-espiritismo.md`
- **Conceitos novos** (11): `vida-futura`, `tres-revelacoes`, `caridade`, `fe-raciocinada`, `prece`, `bem-aventurancas`, `desapego-dos-bens-terrenos`, `homem-de-bem`, `mundos-de-expiacao-e-provas`, `mundos-regeneradores`, `mundos-felizes`.
- **Parábolas** (8): `parabola-do-semeador`, `parabola-do-bom-samaritano`, `parabola-do-mau-rico`, `parabola-dos-talentos`, `parabola-do-festim-de-bodas`, `parabola-da-figueira-seca`, `parabola-dos-trabalhadores-da-ultima-hora`, `parabola-da-candeia-sob-o-alqueire`.

Páginas atualizadas (11):
- **Conceitos do LE** (8): `reencarnacao`, `pluralidade-dos-mundos-habitados`, `lei-de-justica-amor-e-caridade`, `perfeicao-moral`, `suicidio`, `livre-arbitrio`, `progresso-espiritual`, `encarnacao` — adicionada seção "No ESE" com cross-refs.
- **Entidades** (3): `santo-agostinho`, `jesus` (atualizados com papel no ESE), `erasto` (criado).

Cross-refs incluídos: versículos do NT (~100+ referências a S. Mateus, S. Lucas, S. João, S. Marcos, S. Paulo) e questões do LE por mapeamento temático. `index.md` atualizado com obra, parábolas e entidade. Nenhuma divergência — fonte é nível 1.

## [2026-04-06] ingest | A Gênese, os Milagres e as Predições Segundo o Espiritismo (Kardec, trad. Guillon Ribeiro)

Ingest completo da Gênese. Fonte: `raw/kardec/pentateuco/genese.md` (11.125 linhas, 18 capítulos + Introdução).

Páginas criadas (8):
- **Obra** (1): `wiki/obras/genese.md`
- **Conceitos novos** (7): `fluido-cosmico-universal`, `fluidos`, `origem-do-mal`, `raca-adamica`, `emigracoes-e-imigracoes-dos-espiritos`, `transicao-planetaria`, `geracao-nova`.

Páginas atualizadas (6):
- **Conceitos do LE** (3): `deus` (Providência, visão de Deus, imutabilidade das leis), `principio-vital` (como modificação do fluido cósmico, analogia elétrica), `perispirito` (origem fluídica, variação conforme mundo e grau moral, irradiação, couraça moral).
- **Entidades** (2): `allan-kardec` (links para obras), `jesus` (milagres explicados, Consolador).
- **index.md** atualizado com obra e todos os novos conceitos.

Nenhuma divergência — fonte é nível 1 (Pentateuco).

## [2026-04-06] query | Veracidade das mensagens psicografadas

Criada síntese `wiki/sinteses/veracidade-das-mensagens-psicografadas.md` a pedido do usuário, cruzando os critérios de análise de comunicações do LM (caps. X, XIX–XXI, XXIII–XXIV, XXVII, XXXI) com a escala espírita do LE (q. 100–113). Inclui os 26 critérios de distinção bons/maus Espíritos, exemplos de comunicações apócrifas comentadas por Kardec e roteiro prático de verificação. `index.md` atualizado.

## [2026-04-06] query | Parábolas faltantes do ESE

Identificadas 3 parábolas do ESE ausentes da wiki. Criadas páginas: `wiki/conceitos/parabola-do-credor-incompassivo.md` (cap. XI), `wiki/conceitos/parabola-do-rico-insensato.md` (cap. XVI), `wiki/conceitos/parabola-da-casa-sobre-a-rocha.md` (cap. XVIII). Atualizados `index.md`, `wiki/obras/evangelho-segundo-o-espiritismo.md` (resumo dos capítulos + tabela de parábolas) e `log.md`.
