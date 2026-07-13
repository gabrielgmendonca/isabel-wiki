# Triagem de aspas — blockquotes (ROADMAP §12 Fase 3)

> Gerado em 2026-07-13, após estender `_scan_literal_quotes` a blockquotes.
> Fora do build (`reports/` não é publicado).

**79 candidatos** — 56 fabricated · 13 paraphrase · 10 uncertain. 62 em blockquote (nunca antes varridos), 17 inline.

As 6 `misattributed` desta leva já foram corrigidas (locus trocado, verificado por `cite.py`) — a wiki voltou a 0 `warning` em `quote_misattributed`.

Conserto por classe: **fabricated** → de-quote (vira paráfrase sem aspas) ou reancorar numa aspa verbatim via `insert_quote.py`; **paraphrase** → locus certo, só de-quote ou trocar pelo literal; **uncertain** → conferência humana.

`cob.` = cobertura contígua da aspa no locus citado (0.0 = nada do texto aparece lá).


## fabricated (56)

| Página | L | BQ | cob. | Citação | Aspa |
|---|---|---|---|---|---|
| `aprofundamentos/criacao-do-planeta-terra.md` | 53 | ✓ | 0.0 | (Gênese, cap. VIII, item 3) | A teoria da formação da Terra pela condensação da matéria cósmica é a que hoje prevalec… |
| `conceitos/amorterapia.md` | 31 | ✓ | 0.2 | (ESE, cap. XII) | Amar os inimigos não significa que o homem deva nutrir por eles afeição igual à que tem… |
| `conceitos/armadura-de-deus.md` | 25 | ✓ | 0.12 | (ESE cap. XVII, item 4) | Pelos esforços que o homem faz para se melhorar, por sua perseverança, por sua firmeza,… |
| `conceitos/armadura-de-deus.md` | 37 | ✓ | 0.0 | (C&I 1ª parte cap. IX, item 1) | Os demônios, na acepção vulgar do termo, supõem seres essencialmente maléficos. Ora, se… |
| `conceitos/armadura-de-deus.md` | 39 | ✓ | 0.0 | (C&I 1ª parte cap. IX, item 5) | Os Espíritos não constituem [...] uma categoria à parte na criação. São as almas dos qu… |
| `conceitos/contentamento.md` | 25 | ✓ | 0.0 | (LE, q. 925) | Que pensar das pessoas que esperam da fortuna a felicidade, certas de que, se a possuís… |
| `conceitos/contentamento.md` | 33 | ✓ | 0.0 | (LE q. 919, comentário-paráfrase do tom de Kardec sobre vontade firme) | A resignação consiste em receber, sem queixar-se, todas as provas da vida [...]. A cora… |
| `conceitos/contentamento.md` | 41 | ✓ | 0.0 | (LE q. 919) | Como podemos resistir às tentações do mal? — Pela vontade firme de fazê-lo. |
| `conceitos/contentamento.md` | 49 | ✓ | 0.0 | (LE q. 920–921, paráfrase do tom) | Se os homens praticassem a lei de Deus, gozariam neste mundo de uma felicidade relativa… |
| `conceitos/depressao.md` | 21 | ✓ | 0.13 | (LE, q. 459) | Os Espíritos influem sobre os nossos pensamentos e ações [...]. Há os que nos impelem a… |
| `conceitos/desdobramento.md` | 15 | ✓ | 0.0 | (LE, q. 401) | Quando o corpo descansa, o Espírito se desprende dos laços corporais e fica em estado d… |
| `conceitos/desprendimento-em-vida.md` | 21 | ✓ | 0.08 | (LE q. 401–402, paráfrase) | O homem, durante o sono, recobra momentaneamente sua liberdade. Sua alma se isola do co… |
| `conceitos/discernimento-dos-espiritos.md` | 44 | ✓ | 0.0 | (ESE, cap. XXI, item 9) | Que os adeptos do Espiritismo se compenetrem bem destas palavras de S. João: **Não deis… |
| `conceitos/discernimento-dos-espiritos.md` | 68 | ✓ | 0.0 | (ESE, cap. XXI, item 9) | Toda comunicação em que transpareça o orgulho, ou qualquer sentimento egoístico, é susp… |
| `conceitos/discernimento-dos-espiritos.md` | 82 | ✓ | 0.0 | (LM, 2ª parte, cap. XXVI, item 279 — concordância universal) | A unidade do ensino [...] constitui a prova mais forte de sua origem divina. Quando os … |
| `conceitos/discernimento-dos-espiritos.md` | 90 | ✓ | 0.32 | (LM, 2ª parte, cap. XXIV, parafraseando o princípio central do capítulo) | Não é o nome que faz o valor do ensino; é o ensino que faz o valor do nome. |
| `conceitos/dor.md` | 21 | ✓ | 0.0 | (LE, q. 998) | O sofrimento é, ao mesmo tempo, uma expiação do passado e uma prova para o futuro. |
| `conceitos/egoismo.md` | 19 | ✓ | 0.0 | (LE, Conclusão, item V) | Destruindo o materialismo, que é uma das chagas da sociedade, [o Espiritismo] encaminha… |
| `conceitos/homem-velho-homem-novo.md` | 31 | ✓ | 0.21 | (LE q. 919, paráfrase do contexto) | Como pode o homem destruir os maus pendores? — Pela vontade firme de fazê-lo. |
| `conceitos/homem-velho-homem-novo.md` | 37 | ✓ | 0.05 | (ESE cap. XVII, item 4) | Pelos esforços que o homem faz para se melhorar, por sua perseverança, por sua firmeza,… |
| `conceitos/individuacao.md` | 21 | ✓ | 0.42 | (LE, q. 919) | Conhece-te a ti mesmo, é a primeira lei de toda inteligência. |
| `conceitos/individuacao.md` | 25 | ✓ | 0.12 | (LE, q. 909) | Pode-se ainda nesta vida fazer alguma coisa para se libertar das más inclinações? — Sim… |
| `conceitos/leis-morais/lei-de-causa-e-efeito.md` | 20 | ✓ | 0.0 | (C&I, 1ª parte, cap. VII, item 7) | Deus não pune a criatura pela criatura; a própria criatura, conhecedora do bem e do mal… |
| `conceitos/leis-morais/lei-de-causa-e-efeito.md` | 26 | ✓ | 0.17 | (LE, Parte 2, cap. I, Introdução) | As vicissitudes da vida corpórea são, ao mesmo tempo, expiação das faltas passadas e pr… |
| `conceitos/medico-interno.md` | 27 | ✓ | 0.13 | (LE, q. 459) | Os Espíritos influem sobre os nossos pensamentos e ações [...]. Há os que nos impelem a… |
| `conceitos/mediunidade-curativa.md` | 25 | ✓ | 0.23 | (Gênese, cap. XIV, itens 31–33) | O fluido magnético é uma matéria; o fluido espiritual a essa matéria imprime certas qua… |
| `conceitos/medo.md` | 19 | ✓ | 0.08 | (LE, Introdução) | Toda criatura humana tem instintivamente o desejo de viver e a previsão da vida futura,… |
| `conceitos/mercantilizacao-da-mediunidade.md` | 23 | ✓ | 0.28 | (LM, cap. XXVIII) | A mediunidade é uma dádiva de Deus, da qual cada um pode usar para o bem, mas que se to… |
| `conceitos/mercantilizacao-da-mediunidade.md` | 27 | ✓ | 0.15 | (LM, cap. XXVIII) | Os Espíritos verdadeiramente bons só se comunicam com pessoas de boa moral [...] o médi… |
| `conceitos/onda-mental.md` | 23 | ✓ | 0.0 | (LE, q. 459, comentário) | Já vos dissemos: o pensamento é uma emanação do Espírito; mas, assim como a chama produ… |
| `conceitos/orgulho.md` | 17 | ✓ | 0.0 | (LE, Introdução, item V; Parte 2, cap. I, Introdução) | O orgulho é que gera a incredulidade. O orgulho e a ambição serão sempre uma barreira e… |
| `conceitos/pluralidade-dos-mundos-habitados.md` | 57 |  | 0.0 | (LE, q. 57) | os habitantes [dos outros mundos] têm organizações diferentes |
| `conceitos/separacao-e-reencontro.md` | 19 | ✓ | 0.0 | (LE, q. 274–276) | Os que se amaram se reencontram após a morte e se reconhecem. |
| `conceitos/sete-espiritos-de-deus.md` | 65 | ✓ | 0.05 | (LE q. 113) | Atingiram o máximo da perfeição. [...] Não estão sujeitos a reencarnar nos mundos trans… |
| `divergencias/anjos-rebeldes-em-2-pedro-2.md` | 34 | ✓ | 0.07 | (LE q. 131) | **Existe o diabo?** — Se ele existisse, seria obra de Deus, e Deus não seria nem justo,… |
| `divergencias/escravidao-em-efesios-6.md` | 64 | ✓ | 0.0 | (ESE cap. XII, item 6, ressaltando regra de ouro) | Não façais aos outros o que não quereríeis que vos fizessem. — Esta máxima encerra todo… |
| `divergencias/escravidao-em-efesios-6.md` | 66 | ✓ | 0.0 | (ESE cap. X, item 14, paráfrase) | Se julgares com indulgência, com indulgência sereis julgados [...]. |
| `divergencias/pecado-original-em-romanos-5.md` | 55 | ✓ | 0.1 | (Gênese, cap. XI, itens 38–44) | A gênese mosaica, tomada ao pé da letra, é insustentável diante da ciência positiva. [.… |
| `divergencias/pecado-original-em-romanos-5.md` | 65 | ✓ | 0.0 | (ESE, cap. V, item 4 — síntese) | As aflições da vida presente [são], em primeiro lugar, consequência da imperfeição do h… |
| `divergencias/penas-eternas-em-apocalipse.md` | 33 |  | 0.0 | (C&I, 1ª parte, cap. VII) | Deus tem por si a eternidade para aguardar o arrependimento do culpado |
| `divergencias/penas-eternas-em-apocalipse.md` | 39 |  | 0.0 | (LE q. 1009) | Nenhuma falta é irremissível. As de maior gravidade podem-no [ser remitidas] mediante e… |
| `divergencias/predestinacao-em-romanos-8-9.md` | 78 | ✓ | 0.0 | (ESE, cap. V, item 4 — síntese) | As aflições da vida presente [são], em primeiro lugar, consequência da imperfeição do h… |
| `divergencias/recaida-sem-arrependimento-em-hebreus.md` | 35 | ✓ | 0.07 | (LE, q. 166) | A alma, depois da sua união com um corpo, pode reencarnar-se logo após a morte deste co… |
| `divergencias/recaida-sem-arrependimento-em-hebreus.md` | 42 | ✓ | 0.0 | (LE, q. 1009) | Existem algumas faltas que sejam irremissíveis? Algumas que haja cuja mancha nenhuma ex… |
| `divergencias/recaida-sem-arrependimento-em-hebreus.md` | 45 | ✓ | 0.0 | (LE, q. 1010) | Não está o Espírito em tempo algum a si mesmo entregue? — Jamais. Deus nunca o abandona… |
| `divergencias/recaida-sem-arrependimento-em-hebreus.md` | 54 | ✓ | 0.08 | (LE, q. 1009–1016, síntese) | Chegarão todos os homens, por todos os meios, cedo ou tarde, à perfeição? — Sim, mas, d… |
| `divergencias/sangue-expiatorio-em-1-joao.md` | 40 | ✓ | 0.0 | (LE, q. 875) | Devem os homens descansar somente em Deus para ser felizes na terra? — Cada um trabalha… |
| `divergencias/sangue-expiatorio-em-1-joao.md` | 50 | ✓ | 0.0 | (LE, q. 1003–1006, síntese) | O remorso é a primeira punição que o Espírito sofre, é o aviso que Deus lhe dá para que… |
| `obras/epistola-aos-colossenses.md` | 53 | ✓ | 0.0 | (Gênese cap. I, item 5; cf. LE q. 14) | Foi sempre Deus, é Deus, será Deus quem todas as criou |
| `obras/estela.md` | 117 | ✓ | 0.0 | (LE q. 957) | Não há circunstância alguma que justifique o suicídio. |
| `obras/livro-dos-espiritos.md` | 149 |  | 0.0 | (LE, Conclusão, item IX) | do lado em que o bem jamais esteve de mistura com o mal |
| `obras/o-fim-do-mundo.md` | 90 |  | 0.0 | (LE q. 222) | pode reencarnar no mesmo globo ou passar a mundos superiores |
| `obras/revista-espirita-1860.md` | 62 |  | 0.36 | (C&I, 2ª parte, cap. II) | antes a matéria me apertava com rede inflexível; agora estou livre |
| `personalidades/espiritos-reveladores.md` | 15 | ✓ | 0.06 | (LE, Prolegômenos) | A coerência dos princípios expostos, não obstante a diversidade das fontes em que os bu… |
| `personalidades/santo-agostinho.md` | 25 |  | 0.0 | (LE, Conclusão, item IX — Santo Agostinho) | O Espiritismo é o laço que um dia os unirá, porque lhes mostrará onde está a verdade, o… |
| `sinteses/hierarquia-de-autoridade.md` | 133 | ✓ | 0.45 | (Gênese, Introdução) | O caráter essencial [da doutrina] é generalidade e concordância no ensino. |

## paraphrase (13)

| Página | L | BQ | cob. | Citação | Aspa |
|---|---|---|---|---|---|
| `conceitos/armadura-de-deus.md` | 27 | ✓ | 0.23 | (LE q. 909) | Para vencermos nossas más inclinações, que auxílio podemos esperar? — O homem pode venc… |
| `conceitos/familia.md` | 30 | ✓ | 0.29 | (ESE, cap. XIV, item 8) | A consanguinidade pode estabelecer entre dois seres uma identidade de natureza física, … |
| `conceitos/homem-de-bem.md` | 29 |  | 0.27 | (ESE, cap. XVII, item 3) | A riqueza, para ele, não é mais que um depósito de que deve dar conta |
| `conceitos/homem-velho-homem-novo.md` | 29 | ✓ | 0.23 | (LE q. 909) | Para vencermos nossas más inclinações, que auxílio podemos esperar? — O homem pode venc… |
| `conceitos/pluralidade-dos-mundos-habitados.md` | 53 |  | 0.3 | (LE, q. 173) | pode reencarnar no mesmo globo ou passar a mundos superiores |
| `conceitos/pluralidade-dos-mundos-habitados.md` | 57 |  | 0.3 | (LE, q. 173) | pode reencarnar no mesmo globo ou passar a mundos superiores |
| `conceitos/provas-e-expiacoes.md` | 30 | ✓ | 0.4 | (LE, q. 984–985) | As vicissitudes da vida são sempre a punição de faltas passadas? — Não; nem todas, como… |
| `conceitos/vazio-existencial.md` | 27 |  | 0.44 | (LE q. 132) | O objetivo da encarnação é o aperfeiçoamento dos Espíritos |
| `divergencias/anjos-rebeldes-em-2-pedro-2.md` | 31 | ✓ | 0.39 | (LE q. 115) | **Os Espíritos foram criados todos iguais ou Deus os criou mais ou menos perfeitos?** —… |
| `divergencias/uma-morte-e-juizo-em-hebreus-9.md` | 32 | ✓ | 0.17 | (LE, q. 222) | Os antigos filósofos tinham noção da pluralidade das existências? — Essa doutrina veio … |
| `obras/primeira-epistola-aos-corintios.md` | 124 | ✓ | 0.27 | (LE q. 135, comentário) | Há no homem três coisas: 1ª o corpo, ou ser material análogo aos animais [...]; 2ª a al… |
| `obras/urania.md` | 92 |  | 0.3 | (LE, q. 173) | pode reencarnar no mesmo globo ou passar a mundos superiores |
| `obras/urania.md` | 100 |  | 0.17 | (LE, q. 200) | Têm sexo os Espíritos? — Não, como entendeis. Os sexos existem no organismo. No Espírit… |

## uncertain (10)

| Página | L | BQ | cob. | Citação | Aspa |
|---|---|---|---|---|---|
| `conceitos/arrependimento.md` | 33 | ✓ | 0.0 | (LE, q. 993) | Pretender que certos Espíritos nunca se arrependerão seria negar a lei do progresso e d… |
| `conceitos/homem-velho-homem-novo.md` | 43 | ✓ | 0.0 | (LE q. 893) | A perfeição moral consiste em praticar a lei de justiça, de amor e de caridade na sua m… |
| `conceitos/materialismo.md` | 25 | ✓ | 0.0 | (LE, Conclusão, item V) | Destruindo o materialismo, que é uma das chagas da sociedade, [o Espiritismo] encaminha… |
| `conceitos/prova-experimental-da-sobrevivencia.md` | 37 |  | 0.0 | (ESE, cap. IV) | o Espiritismo nos faz compreender [...] a solidariedade que liga todos os seres |
| `conceitos/telepatia.md` | 27 |  | 0.0 | (LM, 1ª parte, cap. I) | entra no cômputo dos fatos naturais |
| `divergencias/almas-irmas-criadas-aos-pares.md` | 61 |  | 0.0 | (LE q. 298, comentário) | poesia que tem o seu encanto |
| `obras/caminho-verdade-e-vida.md` | 86 |  | 0.38 | (LE, q. 134) | a alma é o princípio da vida moral |
| `obras/epistola-aos-efesios.md` | 155 | ✓ | 0.0 | (LE q. 803) | Os homens são iguais perante Deus |
| `obras/epistola-aos-efesios.md` | 155 | ✓ | 0.0 | (LE q. 803, comentário) | todos têm os mesmos direitos |
| `sinteses/hierarquia-de-autoridade.md` | 75 | ✓ | 0.0 | (ESE, cap. I, item 5) | Não vim destruir a lei cristã, mas dar-lhe execução. |
