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

## [2026-04-06] ingest | O Livro dos Médiuns (Kardec, trad. Guillon Ribeiro)

Ingest completo do LM. Fonte: `raw/kardec/pentateuco/livro-dos-mediuns.md` (11.904 linhas, 32 capítulos em 2 partes + Introdução + Vocabulário espírita).

Páginas criadas (7):
- **Obra** (1): `wiki/obras/livro-dos-mediuns.md`
- **Conceitos novos** (6): `mediunidade`, `psicografia`, `manifestacoes-espiritas`, `obsessao`, `identidade-dos-espiritos`, `evocacao`.

Páginas atualizadas (8):
- **Conceitos** (5): `perispirito` (manifestações físicas, bicorporeidade, transfiguração), `escala-espirita` (aplicação prática no discernimento), `fluidos` (mecanismo das manifestações, fluido universal + vital do médium), `espirito` (ação sobre a matéria, diversidade das comunicações), `emancipacao-da-alma` (sonambulismo mediúnico, evocação de vivos, médiuns extáticos).
- **Entidades** (2): `sao-luis` (instrutor principal no LM, teoria das manifestações, regra do discernimento, análise de apócrifas), `erasto` (co-autor do quadro sinótico dos médiuns).
- **index.md** atualizado com obra, seção "Mediunidade e prática espírita" e entidades complementadas.

Nenhuma divergência — fonte é nível 1 (Pentateuco). Quarta obra do Pentateuco ingerida; falta *O Céu e o Inferno*.

## [2026-04-06] query | Expiação e arrependimento (LE, q. 990–1002)

Criada página `wiki/questoes/expiacao-e-arrependimento.md` com as 13 questões da subseção "Expiação e arrependimento" do Cap. II (Das penas e gozos futuros), Parte Quarta do LE. Inclui perguntas e respostas literais, comentários de Kardec, análise por questão e síntese temática. `index.md` atualizado.

## [2026-04-06] ingest | O Céu e o Inferno (Kardec, 1865/1869)

Ingest completo do C&I — quinta e última obra do Pentateuco. Fonte: `raw/kardec/pentateuco/ceu-e-inferno.md` (3.500 linhas, 2 partes, 19 capítulos).

Páginas criadas (79):
- **Obra** (1): `wiki/obras/ceu-e-inferno.md`
- **Conceitos novos** (11): `futuro-e-o-nada`, `ceu`, `inferno`, `purgatorio`, `penas-eternas`, `codigo-penal-da-vida-futura`, `expiacao-e-reparacao`, `anjos`, `demonios`, `proibicao-de-evocar-os-mortos`, `perturbacao`.
- **Entidades** (67): 18 espíritos felizes (cap. II), 6 em condição média (cap. III), 10 sofredores (cap. IV), 9 suicidas (cap. V), 5 criminosos arrependidos (cap. VI), 5 endurecidos (cap. VII), 14 expiações terrestres (cap. VIII).

Páginas atualizadas (4):
- **Conceitos** (4): `morte-e-pos-morte` (mecanismo da passagem, apreensão), `penas-e-gozos-futuros` (código penal, refutação das penas eternas), `suicidio` (9 relatos da 2ª parte), `perispirito` (papel na separação alma-corpo).

`index.md` atualizado com obra, conceitos, e 67 entidades organizadas por capítulo. Pentateuco completo.

## [2026-04-06] lint | 20 achados — links de conceitos quebrados

Lint completo da wiki após ingestão do Pentateuco. 155 páginas auditadas: frontmatter, `## Fontes`, formato de citação, links de entidades/obras — tudo OK. Único problema: 20 links `[[wiki/conceitos/...]]` apontando para páginas inexistentes.

Ações tomadas:
- **Merge**: `morte-e-pos-morte.md` → `morte.md` (26 links atualizados).
- **Correção de links**: 6 refs a `perturbacao-espirita` → `perturbacao`.
- **18 conceitos criados**: `expiacao`, `fe`, `arrependimento`, `erraticidade`, `lei-de-causa-e-efeito`, `provas-e-expiacoes`, `egoismo`, `orgulho`, `materialismo`, `humildade`, `resignacao`, `responsabilidade`, `desligamento-do-espirito`, `ligacao-espirito-corpo`, `lei-moral`, `confianca-em-deus`, `avareza`, `separacao-e-reencontro`.
- `index.md` atualizado com novas seções "Justiça divina e consequências morais" e "Virtudes e vícios".
