# Log

Histórico cronológico da wiki. Cada entrada começa com `## [YYYY-MM-DD] <tipo> | <título>`, onde `<tipo>` ∈ {`setup`, `ingest`, `query`, `lint`, `refactor`}.

Para ver as últimas N entradas: `grep "^## \[" log.md | tail -N`.

## [2026-04-15] lint | 14 achados
Nenhum erro. 3 `citation_format` são falsos positivos (formato `(LM, cap. XXIX)` sem "2ª parte"). 3 `tag_taxonomy` reais em divergências e em paulo-de-tarso — dessincronia entre campo `fontes` e tags `obra/`. `index.md` com contagens desatualizadas (14→18 fontes, 216→239 páginas).

---

## [2026-04-15] lint | 10 achados (0 erros)

Lint pós-ingest de Lucas: nenhum erro estrutural. Avisos: 1 órfão pré-existente (`estatisticas-da-wiki.md`), 2 falsos positivos de `citation_format` (`(LM, cap. XXIII)` em Lucas e `(LM, caps. XXIV–XXVII)` em Marcos — formato válido não reconhecido pelo regex), 1 inconsistência de taxonomia pré-existente em `sinais-de-marcos-16.md`. Info: contadores de cobertura no `index.md` defasados (14 → 17 fontes complementares; ~216 → 234 páginas).

## [2026-04-15] ingest | Evangelho segundo Lucas (ACF)

Ingerido o terceiro Evangelho canônico (`raw/biblia-acf/lucas/`, 24 caps.). Criados: `wiki/obras/evangelho-segundo-lucas.md`, seis novas páginas de parábola exclusivas de Lucas (filho pródigo, dracma perdida, mordomo infiel, juiz iníquo, fariseu e publicano) e a personalidade `wiki/personalidades/zaqueu.md`. Divergência sobre "inferno/chama/abismo" em Lc 16:19–31 registrada por extensão em `wiki/divergencias/fogo-eterno-em-mateus-25.md` (mesma estrutura doutrinária do "fogo eterno" de Mt 25). Páginas existentes atualizadas: Bom Samaritano, Mau Rico, Rico Insensato, Ovelha Perdida — consolidadas com referências cruzadas à nova página de Lucas.

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

## [2026-04-06] ingest | A conquista da saúde psicológica (Divaldo Franco)

Primeira fonte complementar (nível 3) ingerida. Transcrição de palestra oral de Divaldo Pereira Franco (~2009, Curitiba). Tema: depressão, neurociência, obsessão e saúde psicológica à luz do Espiritismo.

Páginas criadas (3):
- **Obra** (1): `wiki/obras/conquista-da-saude-psicologica.md`
- **Conceito novo** (1): `wiki/conceitos/depressao.md`
- **Entidade nova** (1): `wiki/entidades/divaldo-franco.md`

Páginas atualizadas (2):
- `wiki/conceitos/obsessao.md` — cross-links para depressão e palestra.
- `wiki/conceitos/transicao-planetaria.md` — cross-link para palestra.

`index.md` atualizado com obra (nova subseção "Complementares"), conceito e entidade. Nenhuma divergência com o Pentateuco identificada. Nota registrada sobre referência científica imprecisa ("dois físicos quânticos de Harvard") — fonte provável: Candace Pert (neuropeptídeos) + Herbert Benson (resposta de relaxamento).

## [2026-04-07] ingest | O Problema do Ser e do Destino (Léon Denis, 1908/1922)

Primeira obra de Léon Denis na wiki. Fonte: `raw/autores/leon-denis/O Problema do Ser do Destino e da Dor/O Problema do Ser do Destino e da Dor.md` (456 p., 3 partes, 27 capítulos). Edição CELD 2011, baseada na edição francesa de 1922.

Páginas criadas (6):
- **Obra** (1): `wiki/obras/o-problema-do-ser-e-do-destino.md`
- **Entidade** (1): `wiki/entidades/leon-denis.md`
- **Conceitos novos** (2): `wiki/conceitos/potencias-da-alma.md`, `wiki/conceitos/dor.md`
- **Divergências** (2): `wiki/divergencias/mudanca-de-sexo-reencarnacao.md`, `wiki/divergencias/almas-irmas-criadas-aos-pares.md`

Páginas atualizadas (3):
- `wiki/conceitos/reencarnacao.md` — seção Denis + links para divergências.
- `wiki/conceitos/livre-arbitrio.md` — seção Denis + link para potências da alma.
- `wiki/conceitos/progresso-espiritual.md` — seção Denis + links para dor e potências.

Divergências identificadas (2 reais, 1 mudança de ênfase):
1. **Mudança de sexo** (divergência real): Denis restringe e estigmatiza; Kardec trata com naturalidade (LE, q. 200–202).
2. **Almas-irmãs criadas aos pares** (divergência real): Denis afirma pares predestinados; Kardec nega "união particular e fatal" (LE, q. 298).
3. **Intervalo entre encarnações** (mudança de ênfase): Denis generaliza curto (10–30 anos); Kardec é aberto ("desde algumas horas até milhares de séculos", LE, q. 223).

`index.md` atualizado com obra (subseção Léon Denis), entidade, conceitos novos e divergências.

## [2026-04-07] ingest | Parábola do Semeador (Carlos Mendonça, palestra)

Palestra de Carlos Mendonça (Centro Espírita Bezerra de Menezes de Estácio) sobre a parábola do semeador (Marcos 4:1–25). Estudo do método pedagógico de Jesus e da persistência no bem à luz da Doutrina Espírita, com citação de Vinícius (Pedro de Camargo, *Em torno do Mestre*). Nenhuma divergência com Kardec.

Páginas criadas (3):
- **Obra** (1): `wiki/obras/parabola-do-semeador-carlos-mendonca.md`
- **Entidades** (2): `wiki/entidades/vinicius.md`, `wiki/entidades/carlos-mendonca.md`

Páginas atualizadas (1):
- `wiki/conceitos/parabola-do-semeador.md` — seção "Na palestra de Carlos Mendonça", fontes e páginas relacionadas.

`index.md` atualizado com obra (subseção Carlos Mendonça), entidades.

## [2026-04-07] ingest | Felizes os Pobres em Espírito (Carlos Mendonça)

Palestra sobre a primeira bem-aventurança do Sermão da Montanha (Mateus 5:3) à luz espírita. Pobreza de espírito como humildade moral, não falta de inteligência; conquista do Reino dos Céus pela autotransformação.

Páginas criadas (1):
- `wiki/obras/felizes-os-pobres-em-espirito-carlos-mendonca.md`

Páginas atualizadas (4):
- `wiki/entidades/carlos-mendonca.md` — nova obra associada e páginas relacionadas.
- `wiki/conceitos/bem-aventurancas.md` — link para a palestra.
- `wiki/conceitos/humildade.md` — link para a palestra.
- `index.md` — nova obra na subseção Carlos Mendonça, status atualizado.

## [2026-04-07] ingest | Depois da Morte (Léon Denis, 1890)

Segunda obra de Léon Denis na wiki. Fonte: `raw/autores/leon-denis/l48/l48.md` (10ª ed. FEB, 1977). Obra de popularização e síntese da Doutrina Espírita — 5 partes, 56 capítulos. Panorama histórico das religiões (doutrina secreta), provas da imortalidade, perispírito, vida além-túmulo e moral espírita. Nenhuma divergência com o Pentateuco identificada.

Páginas criadas (1):
- `wiki/obras/depois-da-morte.md`

Páginas atualizadas (2):
- `wiki/entidades/leon-denis.md` — nova obra associada.
- `index.md` — nova obra na subseção Léon Denis, status atualizado (3→4 complementares).

## [2026-04-07] lint | 2 achados
Wiki com 187 páginas em boa saúde. Únicos achados: 2 falsos positivos do script (status `aberta` em divergências flaggado como inválido — o script precisa aceitar vocabulário próprio de divergências). Duas divergências abertas (mudança de sexo e almas-irmãs) com análise completa, aguardando decisão do usuário.

## [2026-04-07] ingest | Cristianismo e Espiritismo (Léon Denis, 1898)

Terceira obra de Denis na wiki. Tese central: o Cristianismo primitivo era essencialmente espírita — mediunidade nos primeiros cristãos, aparições de Jesus como fenômenos naturais, supressão do profetismo pela Igreja. Análise dos dogmas como deturpação do Evangelho e do Espiritismo como Terceira Revelação. Destaque para a seção "Visão de Deus" (cap. X): Denis descreve, com base em comunicações espirituais, a percepção progressiva de Deus pelos Espíritos elevados — mudança de ênfase em relação a Kardec, não divergência doutrinária.

Páginas criadas (1): `wiki/obras/cristianismo-e-espiritismo.md`.
Páginas atualizadas (5): `wiki/entidades/leon-denis.md`, `wiki/conceitos/reencarnacao.md`, `wiki/conceitos/deus.md`, `wiki/conceitos/tres-revelacoes.md`, `wiki/conceitos/progresso-espiritual.md`.
Nenhuma divergência nova registrada.

## [2026-04-07] ingest | O Grande Enigma (Léon Denis, 1911)

Quarta obra de Léon Denis na wiki. Fonte: `raw/autores/leon-denis/o_grande_enigma-min/o_grande_enigma-min.md` (296 p., 4 partes, 16 capítulos + 6 notas complementares + síntese doutrinária). Edição CELD 2011, tradução de Maria Lucia Alcantara de Carvalho. Título original: *La Grande Énigme. Dieu et l'Univers*.

Tese central: matéria, força e inteligência são aspectos de uma substância única; as leis universais exigem uma Inteligência ordenadora — Deus. A obra combina argumento cosmológico (caps. I–IX), contemplação poética da natureza (caps. X–XIV), a "lei circular" da vida e morte (cap. XV), a missão do séc. XX (cap. XVI) e uma síntese doutrinária em formato de catecismo (Parte IV). Destaque para a harmonia planetária como prova estética de Deus (cap. IV) — tema original sem contraparte no Pentateuco.

Páginas criadas (2):
- `wiki/obras/o-grande-enigma.md`
- `wiki/conceitos/harmonia-das-esferas.md` — conceito original de Denis, sem contraparte em Kardec

Páginas atualizadas (7):
- `wiki/entidades/leon-denis.md` — nova obra associada, citação e fontes.
- `wiki/conceitos/deus.md` — argumento cosmológico de Denis, harmonia planetária.
- `wiki/conceitos/pluralidade-dos-mundos-habitados.md` — Sol como morada de Espíritos sublimes.
- `wiki/conceitos/morte.md` — morte como segundo nascimento, desprendimento gradual, perturbação.
- `wiki/conceitos/prece.md` — comunhão universal, poder dinâmico, proteção mediúnica.
- `wiki/conceitos/mediunidade.md` — perigos sem elevação moral, necessidade da prece.
- `wiki/conceitos/progresso-espiritual.md` — lei circular, séc. XX como século do espírito.

Nenhuma divergência doutrinária nova identificada. `index.md` atualizado com obra e conceito novo.

## [2026-04-07] ingest | Quando o Invisível se Torna Inevitável (Divaldo Franco, ~2023)

Segunda palestra de Divaldo na wiki. Fonte: web TV Mansão do Caminho. Palestra testemunhal: relato detalhado da obsessão da prima Baby por ex-namorado desencarnado (~1948), psicografia de 11 romances com Victor Hugo (desde 1970), episódio de Chico Xavier e Meimei em Pedro Leopoldo, resignação diante de erro médico, e estrutura do atendimento fraterno na Mansão do Caminho.

Páginas criadas (4): `wiki/obras/quando-o-invisivel-se-torna-inevitavel.md`, `wiki/entidades/meimei.md`, `wiki/entidades/victor-hugo.md`, `wiki/entidades/mansao-do-caminho.md`.
Páginas atualizadas (5): `wiki/entidades/divaldo-franco.md`, `wiki/conceitos/obsessao.md` (seção "Casos ilustrativos" com narrativa da prima Baby), `wiki/conceitos/perispirito.md`, `wiki/conceitos/psicografia.md` (casos Victor Hugo e Meimei), `index.md`.
Nenhuma divergência com o Pentateuco identificada.

## [2026-04-07] ingest | O Que é o Espiritismo? (Allan Kardec, 1859)

Primeira obra de Kardec complementar (nível 2) na wiki. Opúsculo introdutório em três capítulos: diálogos com crítico e cético (Cap. I), noções elementares — natureza dos Espíritos, tríplice constituição, meios de comunicação, escala espírita, mediunidade (Cap. II), e solução de problemas pela reencarnação — pluralidade dos mundos, preexistência da alma, desigualdades, penas e gozos futuros (Cap. III). Contém as duas definições canônicas do Espiritismo.

Páginas criadas (1): `wiki/obras/o-que-e-o-espiritismo.md`.
Páginas atualizadas (1): `index.md`.
Nenhuma divergência — obra do próprio Kardec.

## [2026-04-07] ingest | Viagem Espírita em 1862 (Allan Kardec)

Segunda obra de Kardec complementar (nível 2) na wiki. Relato da turnê de Kardec pela França em 1862: impressões gerais sobre o crescimento do Espiritismo, discursos em Lyon e Bordeaux (caridade como base da reforma social, combate ao materialismo, transição planetária), instruções práticas aos grupos e modelo de regulamento para sociedades espíritas.

Páginas criadas (4): `wiki/obras/viagem-espirita-em-1862.md`, `wiki/conceitos/verdadeiro-espirita.md`, `wiki/conceitos/evangelizacao-infantojuvenil.md`, `wiki/conceitos/organizacao-de-grupos-espiritas.md`.
Páginas atualizadas (9): `wiki/conceitos/caridade.md`, `wiki/conceitos/materialismo.md`, `wiki/conceitos/egoismo.md`, `wiki/conceitos/transicao-planetaria.md`, `wiki/conceitos/geracao-nova.md`, `wiki/conceitos/proibicao-de-evocar-os-mortos.md`, `wiki/conceitos/mediunidade.md`, `wiki/entidades/allan-kardec.md`, `index.md`.
Nenhuma divergência — obra do próprio Kardec.

## [2026-04-07] lint | 3 achados

1 aviso: `wiki/obras/o-que-e-o-espiritismo.md` é página órfã (nenhuma outra página da wiki linka para ela). 2 info: divergências abertas (`mudanca-de-sexo-reencarnacao`, `almas-irmas-criadas-aos-pares`) com análise completa — candidatas a `conciliada`. Zero erros de links, index ou frontmatter.

## [2026-04-07] ingest | Obras Póstumas (Allan Kardec, edição FEB)

Ingest de *Obras Póstumas* (nível 2 — Kardec complementar). Criados: `wiki/obras/obras-postumas.md`, `wiki/conceitos/morte-espiritual.md`, `wiki/entidades/camille-flammarion.md`. Atualizados: `wiki/entidades/jesus.md` (seção Natureza do Cristo), `wiki/entidades/allan-kardec.md` (seções Primeira iniciação e Missão/Previsões), `wiki/conceitos/perispirito.md`, `wiki/conceitos/emancipacao-da-alma.md`, `wiki/conceitos/materialismo.md`, `wiki/conceitos/egoismo.md`, `wiki/conceitos/orgulho.md`, `wiki/conceitos/fe-raciocinada.md`, `index.md`. Nenhuma divergência com o Pentateuco identificada.

## [2026-04-07] ingest | A Caminho da Luz (Emmanuel/Chico Xavier, FEB, 1939)

Ingest de *A Caminho da Luz* (nível 3 — complementar aprovado). Primeira obra de Emmanuel/Chico Xavier na wiki. Status: **rascunho** (obra rica, demanda aprofundamento futuro). Criados: `wiki/obras/a-caminho-da-luz.md`, `wiki/entidades/emmanuel.md`, `wiki/entidades/chico-xavier.md`. Atualizados: `wiki/entidades/jesus.md` (seção Governador espiritual da Terra), `wiki/conceitos/raca-adamica.md` (desenvolvimento por Emmanuel — Capela), `wiki/conceitos/emigracoes-e-imigracoes-dos-espiritos.md` (exemplo de Capela), `wiki/conceitos/transicao-planetaria.md` (visão de Emmanuel), `wiki/conceitos/progresso-espiritual.md` (progresso civilizatório), `index.md`. Nenhuma divergência com o Pentateuco identificada — informações complementares.

## [2026-04-07] ingest | Jesus Ensina em Cafarnaum (EELDE, palestra)

Ingest de palestra do canal EELDE sobre Marcos 1:21–28 (nível 3 — complementar alinhado). Criado: `wiki/obras/jesus-ensina-em-cafarnaum-eelde.md`. Atualizados: `wiki/conceitos/obsessao.md` (referência à desobsessão em Cafarnaum), `wiki/entidades/jesus.md` (obra associada), `index.md`. Nenhuma divergência com o Pentateuco.

## [2026-04-07] lint | 2 achados

1 broken link (wikilink com `|` no nome do arquivo raw interpretado como alias pelo Obsidian). 1 divergência aberta (mudança de sexo na reencarnação) — análise completa, sem ação necessária.

## [2026-04-08] query | Onde o Novo Testamento se encaixa na hierarquia de autoridade?

Análise do lugar dos Evangelhos canônicos e dos escritos apostólicos na hierarquia de fontes da wiki. Conclusão: os ensinamentos morais de Jesus são a fonte primordial (acima do nível 1), mas os textos evangélicos são lidos à luz do Pentateuco — "os ensinamentos de Jesus são o sol; o Pentateuco é o telescópio". Paulo e demais apóstolos entram no nível 3 como fontes seletivamente citadas por Kardec. Criado: `wiki/sinteses/hierarquia-de-autoridade.md`. Atualizados: `CLAUDE.md` (seção 2), `index.md` (hierarquia e índice de sínteses).

## [2026-04-08] lint | 10 achados

Wiki saudável: 0 erros, 2 avisos, 1 info. Página `hierarquia-de-autoridade.md` órfã (sem links de entrada de outras páginas). 8 citações flaggadas são falsos positivos (referências bibliográficas contextuais). 1 divergência aberta sem ação necessária.

## [2026-04-15] ingest | Evangelho segundo João (Bíblia ACF, 21 capítulos)

Primeiro Evangelho canônico ingerido — fonte primordial na hierarquia de autoridade. Texto: Almeida Corrigida e Fiel, 21 capítulos em `raw/biblia-acf/joao/`.

Páginas criadas (1):
- `wiki/obras/evangelho-segundo-joao.md` — estrutura capítulo a capítulo com leitura espírita, tabela de referências cruzadas com o Pentateuco, 8 temas centrais identificados.

Páginas atualizadas (5):
- `wiki/entidades/jesus.md` — nova seção "No Evangelho segundo João" (subordinação ao Pai, unidade moral, preexistência, humanidade de Jesus), nova obra associada.
- `wiki/conceitos/reencarnacao.md` — referência ao texto integral de Jo 3:3-6 (Nicodemos) e Jo 9:2 (cego de nascença) com link para obra.
- `wiki/conceitos/tres-revelacoes.md` — três promessas do Consolador expandidas com texto joanino (Jo 14:16-17, 14:26, 16:13) e link para obra.
- `wiki/conceitos/pluralidade-dos-mundos-habitados.md` — base evangélica (Jo 14:2 "muitas moradas", Jo 10:16 "outras ovelhas") com link para obra.
- `index.md` — nova subseção "Evangelhos canônicos" com link para a obra.

Nenhuma divergência — fonte primordial, lida à luz do Pentateuco.

## [2026-04-15] lint | 9 achados (0 erros)
Wiki íntegra com 208 páginas. Oito avisos de citation_format todos em `hierarquia-de-autoridade.md` são falsos positivos (epígrafes, subtítulos e datas). Uma divergência aberta (`mudanca-de-sexo-reencarnacao`) com análise aparentemente completa.

## [2026-04-15] setup | Página de estatísticas da wiki

Criada skill `/stats` e script `.claude/skills/stats/scripts/stats_wiki.py` que gera `wiki/sinteses/estatisticas-da-wiki.md` — painel determinístico com cobertura por tipo, grafo (grau in/out, PageRank via `networkx`, órfãos, componentes isolados), vocabulário (top 50 palavras + 20 bigramas, stopwords PT-BR via `nltk`), atividade mensal parseada de `log.md` (sparkline ASCII) e sugestões automáticas. Utilitários de parsing extraídos para `.claude/skills/_lib/wiki_utils.py`, compartilhados com `lint_wiki.py` (incluindo o parser YAML robusto introduzido em main, que agora suporta listas multilinha e valores quoted). `index.md` atualizado com entrada na seção Sínteses.

## [2026-04-15] lint | 1 achado
Wiki limpa: 0 erros, 0 avisos. Único achado é info — divergência `mudanca-de-sexo-reencarnacao` com status aberta mas análise aparentemente completa (50 linhas); considerar encerrar.

## [2026-04-15] ingest | Evangelho segundo Mateus (ACF)

Ingerido `raw/biblia-acf/mateus/` (28 capítulos da Bíblia ACF). Criada a obra consolidada `wiki/obras/evangelho-segundo-mateus.md` seguindo o padrão de `evangelho-segundo-joao.md` — outline capítulo a capítulo com versos-chave, referências cruzadas ao Pentateuco e tabela de passagens comentadas por Kardec no ESE.

Criadas 9 páginas de parábolas ainda ausentes: joio-e-do-trigo, grão-de-mostarda, fermento, tesouro-escondido-e-da-perola, rede, ovelha-perdida, das-dez-virgens, dos-dois-filhos, dos-lavradores-maus. Registrada divergência `fogo-eterno-em-mateus-25` (Mt 25:41, 46 vs. penas temporárias em C&I). Atualizados `wiki/personalidades/jesus.md` (nova seção "No Evangelho segundo Mateus" e lista de parábolas expandida), `wiki/conceitos/bem-aventurancas.md` (cross-link), `index.md` (seção Evangelhos canônicos, Parábolas de Jesus e Divergências).

## [2026-04-15] query | Parábolas de João sem página na wiki

Analisado o Evangelho de João (caps. 1–21 em `raw/biblia-acf/joao/`) em busca de parábolas ainda sem página dedicada. João não contém parábolas curtas como os sinóticos, mas três alegorias estendidas se qualificam — o próprio texto chama Jo 10 de "parábola" (Jo 10:6). Candidatas como Pão da Vida, Água Viva, Luz do Mundo e Caminho/Verdade/Vida foram descartadas por serem metáforas "Eu sou" (auto-declarações) e não parábolas propriamente ditas.

Páginas criadas (3):
- `wiki/conceitos/parabola-do-bom-pastor.md` — Jo 10:1–18; porta/pastor/mercenário, "outras ovelhas que não são deste aprisco", unidade moral com o Pai (OPE §VIII).
- `wiki/conceitos/parabola-da-videira-verdadeira.md` — Jo 15:1–8; permanência vital na moral do Cristo, Pai como lavrador, poda como prova (ESE caps. V, XVII).
- `wiki/conceitos/parabola-do-grao-de-trigo.md` — Jo 12:24; renúncia fecunda, desapego, paixão como exemplo moral (ESE cap. XXIV, item 15).

Atualizados: `index.md` (três novas entradas na seção Parábolas de Jesus), `wiki/obras/evangelho-segundo-joao.md` (wikilinks diretos nas seções dos caps. 10, 12 e 15, em vez de menções soltas).

## [2026-04-15] ingest | Evangelho segundo Marcos (ACF)

Ingerido `raw/biblia-acf/marcos/` (16 capítulos). Nova página `wiki/obras/evangelho-segundo-marcos.md` destacando segredo messiânico, humanidade de Jesus, quatro casos de obsessão (Cafarnaum, Gadareno/"Legião", siro-fenícia, epiléptico), cura gradual do cego de Betsaida, óbolo da viúva e Shemá no maior mandamento. Criada `wiki/conceitos/parabola-da-semente-que-cresce-por-si.md` (exclusiva de Mc 4:26–29). Registradas duas divergências abertas sobre o final longo (Mc 16:9–20): `condenacao-dos-incredulos-em-marcos-16.md` e `sinais-de-marcos-16.md`. Ampliada `wiki/conceitos/obsessao.md` com as quatro narrativas-base de Marcos. `index.md` atualizado.

## [2026-04-15] ingest | Atos dos Apóstolos (ACF)

Ingerido `raw/biblia-acf/atos/` (28 capítulos). Criada `wiki/obras/atos-dos-apostolos.md` como escrito apostólico nível 3, destacando Pentecostes como anúncio programático da mediunidade universal (cumprimento de Joel), repertório fenomenológico apostólico (aparições, xenoglossia, curas por imposição/contato, transporte, desmaterialização, morte aparente, profecia), desobsessões (pitonisa de Filipos, filhos de Ceva), distinção entre mediunidade gratuita e magia mercenária (Simão, o Mago), universalismo moral (At 10:34; At 17:26–28) e passagens citadas por Kardec (At 17:24–28 em ESE cap. I; At 20:35 em ESE cap. XIII).

Criadas três personalidades: `paulo-de-tarso.md`, `pedro-apostolo.md`, `estevao-o-martir.md`. Registrada divergência aberta `morte-de-ananias-e-safira.md` (At 5:1–11 vs. progressividade das penas em C&I 1ª parte e LE q. 1009–1016). Ampliadas `wiki/conceitos/obsessao.md` (pitonisa e filhos de Ceva), `wiki/conceitos/mediunidade.md` (nova seção "Mediunidade no NT: Atos"), `wiki/conceitos/caridade.md` (comunhão de bens e "dar do que receber"). `index.md` ganhou nova seção "Escritos apostólicos (nível 3)" e entradas em Personalidades e Divergências.
