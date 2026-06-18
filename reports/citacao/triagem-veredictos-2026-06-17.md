# Triagem de aspas do Pentateuco — veredictos (dry-run)

> Gerado em 2026-06-17 pelo workflow `triagem-aspas-dryrun` (70 páginas, 128 aspas das 97 fabricadas + 8 paráfrases + 23 incertas).
> **Report-only — nenhuma página foi mutada.** Cada veredicto vem de um agente que rodou `cite.py` no locus citado + `reverse_locus` na aspa e leu o contexto. Conferir antes de aplicar em lotes.
> Excluído do build (`reports/`). Regenerar pela rodada do workflow `triagem-aspas-dryrun`.

**128 aspas** — keep: 19 · reanchor: 7 · de-quote: 82 · defer: 20

Leitura: `keep` não precisa de conserto (o flag foi falso-positivo de extração). `reanchor`/`de-quote` são os consertos seguros aplicáveis em lote; `defer` exige você.


## ✅ keep — já é verbatim no locus citado (artefato de extração do cite.py; **nenhuma ação** além de talvez confirmar) — 19


**`conceitos/bem-aventuranca-dos-perseguidos.md`**
- L43 · citado `(ESE, cap. XXVIII, item 3, referindo cap. XII)` · classe _fabricated_

  - _A aspa é verbatim no locus citado: ESE cap. XXVIII, item 3 ("3. Prece" da Oração Dominical, subseção V, linha 5333) traz "Constituem parte das nossas provas terrenas as perseguições que os maus nos infligem... Bendigamo…_

**`conceitos/emancipacao-da-alma.md`**
- L49 · citado `(LM, 2ª parte, cap. XIX, item 223, 2ª)` · classe _fabricated_

  - literal da fonte: "A alma do médium pode comunicar-se, como a de qualquer outro."
  - _A aspa é verbatim na resposta 2ª do item 223 ('A alma do médium pode comunicar-se, como a de qualquer outro.'); o flag foi artefato do cite.py, que pelo markup irregular extraiu só a sub-questão 1ª e não a 2ª — o raw da…_

**`conceitos/evocacao.md`**
- L40 · citado `(LM, 2ª parte, cap. XIX, item 223, 2ª; cap. XXV, seção "Evocações das pessoas vivas")` · classe _fabricated_

  - _a aspa é verbatim no item 223, subitem 2ª (linha 5865 do raw): "as quais muitas vezes se comunicam convosco pela escrita, sem que as chameis"; o flag foi artefato de extração — o cite.py devolveu só o primeiro subitem d…_

**`conceitos/mediunidade.md`**
- L42 · citado `(LM, 2ª parte, cap. XIX, item 223, 6ª)` · classe _fabricated_

  - literal da fonte: "O Espírito do médium é o intérprete, porque está ligado ao corpo que serve para falar e por ser necessária uma cadeia entre vós e os Espíritos que se comunicam…"
  - _A aspa é verbatim no subitem 6ª do item 223 (raw linha ~5887); o flag foi artefato do cite.py/reverse_locus, que só imprime o subitem 1ª e indexa o item 223 como bloco único, baixando a cobertura._

**`conceitos/oracao-dominical.md`**
- L13 · citado `(ESE, cap. XXVIII, item 2)` · classe _fabricated_

  - _Verbatim no locus citado: a frase 'o mais perfeito modelo de concisao, verdadeira obra-prima de sublimidade na simplicidade' aparece na linha 5327 do raw, dentro do item 2 ('2. Prefacio') do cap. XXVIII; o flag e artefa…_
- L19 · citado `(ESE, cap. XXVIII, item 2)` · classe _fabricated_

  - _Verbatim no locus citado: 'sob a mais singela forma, ela resume todos os deveres do homem para com Deus, para consigo mesmo e para com o proximo. Encerra uma profissao de fe, um ato de adoracao e de submissao, o pedido …_
- L39 · citado `(ESE, cap. XXVIII, item 3, nota)` · classe _fabricated_

  - _Verbatim no locus citado: a nota de rodape (marcador *) ao item 3 do cap. XXVIII, na linha 5337, diz 'Essa expressao daria a entender que a tentacao promana de Deus... ideia blasfematoria que igualaria Deus a Satanas e …_

**`conceitos/principio-vital.md`**
- L48 · citado `(Gênese, cap. X, item 19)` · classe _fabricated_

  - literal da fonte: "Os corpos orgânicos seriam, então, verdadeiras pilhas elétricas, que funcionam enquanto os elementos dessas pilhas se acham em condições de produzir eletricida…"
  - _A aspa é verbatim no item 19 citado (raw/kardec/pentateuco/genese.md, linhas 4872-4882, com o texto idêntico nas linhas 4876-4879); cite.py devolveu apenas o artefato "19.686" porque latchou no número de uma tabela quím…_

**`obras/livro-dos-espiritos.md`**
- L149 · citado `(LE, Conclusão, item IX)` · classe _fabricated_

  - _A frase é verbatim no locus citado: a resposta dos Espíritos no item IX da Conclusão (raw linha 3366, dentro do item IX iniciado na linha 3363) diz "A unidade se produzirá do lado em que o bem jamais esteve de mistura c…_

**`obras/livro-dos-mediuns.md`**
- L50 · citado `(LM, 1ª parte, cap. II, item 7)` · classe _fabricated_

  - literal da fonte: "Logo, nada há de sobrenatural neste fato, nem de maravilhoso."
  - _O segmento citado após o '[...]' é verbatim na linha 243 do raw, dentro do item 7 do cap. II (item 7 começa na linha 229, item 8 na 244); o flag do cite.py foi artefato de extração (colisão com o item de lista '7.º' da …_
- L111 · citado `(LM, 2ª parte, cap. XIX, item 223, 6ª)` · classe _fabricated_

  - literal da fonte: "O Espírito do médium é o intérprete, porque está ligado ao corpo que serve para falar"
  - _Verbatim no subitem 6.ª do item 223 (linha 5876 do raw), exatamente o locus citado; reverse_locus deu cobertura baixa (0.25) só por ser fragmento de frase longa, mas o texto bate literal._

**`obras/pai-nosso.md`**
- L43 · citado `(ESE, cap. XXVIII, item 3-I)` · classe _fabricated_

  - literal da fonte: "Cego, portanto, é aquele que te não reconhece nas tuas obras, orgulhoso aquele que te não glorifica e ingrato aquele que te não rende graças."
  - _Verbatim no raw ESE linha 5328 sob "3. Prece. — I. Pai nosso...": exatamente o locus citado; reverse_locus deu cobertura baixa (0.30) porque cite.py renderiza item 3 como cabeçalho de lista de uma linha e o índice rever…_
- L71 · citado `(ESE, cap. XXVIII, item 3-VI)` · classe _fabricated_

  - literal da fonte: "Somos nós mesmos que criamos o mal, infringindo as tuas leis e fazendo mau uso da liberdade que nos outorgaste."
  - _Verbatim no raw ESE linha 5334 sob o subitem "VI. Não nos deixes entregues à tentação..." dentro de "3. Prece.": exatamente o locus citado; reverse_locus deu cobertura 0.15 por não indexar a Prece comentada do cap. XXVI…_
- L75 · citado `(ESE, cap. XXVIII, item 2)` · classe _fabricated_

  - literal da fonte: "Com efeito, sob a mais singela forma, ela resume todos os deveres do homem para com Deus, para consigo mesmo e para com o próximo."
  - _Verbatim no raw ESE linha 5327, item "2. Prefácio." do cap. XXVIII: exatamente o locus citado; reverse_locus apontou loci diferentes com cobertura ~0.35 (frase semelhante na q.4 do cap. XI sobre caridade), mas a aspa li…_

**`personalidades/santo-agostinho.md`**
- L25 · citado `(LE, Conclusão, item IX — Santo Agostinho)` · classe _fabricated_

  - _A aspa e verbatim no proprio locus citado: o raw do LE traz a frase exata sob o item IX da Conclusao (heading **IX** na linha 3363, frase na linha 3369); o flag foi artefato do cite.py, que ao resolver 'Conclusao, item …_

**`sinteses/hierarquia-de-autoridade.md`**
- L153 · citado `(LM, 1ª parte, cap. II, item 7)` · classe _fabricated_

  - literal da fonte: "Logo, nada há de sobrenatural neste fato, nem de maravilhoso."
  - _A aspa é verbatim no locus citado: o item 7 do cap. II ('Do maravilhoso e do sobrenatural') roda da linha 229 (início '7. Se a crença nos Espíritos') à 243, e a frase 'nada há de sobrenatural neste fato' aparece literal…_

**`sinteses/veracidade-das-mensagens-psicografadas.md`**
- L100 · citado `(LM, 2ª parte, cap. XIX, item 223, 7ª pergunta)` · classe _uncertain_

  - _Verbatim no raw, item 223, 7.ª pergunta: "pode ele alterar-lhes as respostas e assimilá-las às suas próprias ideias e a seus pendores" (linha 5895); cite.py só devolve o subitem 1.ª e reverse_locus erra a segmentação de…_
- L100 · citado `(LM, 2ª parte, cap. XIX, item 223, 8ª pergunta)` · classe _fabricated_

  - _Verbatim no raw, item 223, 8.ª pergunta: "Os Espíritos procuram o intérprete que mais simpatize com eles" (linha 5897); o trecho citado "procuram o intérprete que mais simpatize com eles" está literal ali; flag é artefa…_
- L130 · citado `(LM, 2ª parte, cap. XXIV, item 267, 1.º)` · classe _fabricated_

  - _Verbatim no raw, item 267, princípio 1.º: "Não há outro critério, senão o bom senso, para se aquilatar do valor dos Espíritos" (linhas 7352-7353, quebrado entre linhas); cite.py devolve só o cabeçalho do item 267 e reve…_

## 🔁 reanchor — trocar o locus citado pelo correto e alinhar ao texto literal — 7


**`conceitos/amorterapia.md`**
- L25 · citado `(ESE, cap. XV, item 4)` · classe _fabricated_ → **`(LE, q. 886)`**

  - literal da fonte: "886. Qual o verdadeiro sentido da palavra caridade, como a entendia Jesus? “Benevolência para com todos, indulgência para as imperfeições dos outros, perdão da…"
  - _reverse_locus dá cobertura 1.00 em LE q. 886 (resposta dos Espíritos ao sentido da caridade segundo Jesus) e ~0.31 no ESE; o item 4 citado de ESE cap. XV traz apenas o texto evangélico dos dois mandamentos (Mt 22), não …_

**`conceitos/fluido-cosmico-universal.md`**
- L31 · citado `(ESE, cap. XXVII, item 9)` · classe _uncertain_ → **`(ESE, cap. XXVII, item 10)`**

  - literal da fonte: "Para apreendermos o que ocorre em tal circunstância, precisamos conceber mergulhados no fluido universal, que ocupa o espaço, todos os seres, encarnados e dese…"
  - _O item 9 citado trata da prece como invocação e nada diz sobre o fluido; a aspa e verbatim no item 10 (reverse_locus 0.75, maior cobertura), onde Kardec descreve os seres mergulhados no fluido universal e o fluido como …_

**`conceitos/homem-de-bem.md`**
- L33 · citado `(LE, q. 893)` · classe _uncertain_ → **`(LE, q. 918)`**

  - literal da fonte: "O verdadeiro homem de bem e o que pratica a lei de justica, amor e caridade, na sua maior pureza."
  - _A q. 893 citada trata de 'a mais meritoria das virtudes' e nao contem a frase; o locus que a sustenta (quase verbatim, reverse_locus 0.47) e a q. 918: 'O verdadeiro homem de bem e o que pratica a lei de justica, amor e …_

**`conceitos/tres-revelacoes.md`**
- L27 · citado `(ESE, cap. I, item 5)` · classe _uncertain_ → **`(ESE, cap. I, item 7)`**

  - literal da fonte: "também o Espiritismo diz: "Não venho destruir a lei cristã, mas dar-lhe execução.""
  - _reverse_locus 0.80 no item 7 vs. 0.00 no item 5 citado; o item 7 traz quase verbatim ('Não venho destruir a lei cristã, mas dar-lhe execução'), a wiki só troca 'venho'→'vim' — mal-atribuição de locus._

**`divergencias/predestinacao-em-romanos-8-9.md`**
- L70 · citado `(LE q. 780)` · classe _uncertain_ → **`(LE, q. 781)`**

  - literal da fonte: "Sendo o progresso uma condição da natureza humana, não está no poder do homem opor-se-lhe. É uma força viva, cuja ação pode ser retardada, porém não anulada, p…"
  - _A aspa não está em q.780 (sobre progresso moral x intelectual); reverse_locus dá 0.62 em q.781, onde o comentário de Kardec diz quase verbatim 'Sendo o progresso uma condição da natureza humana' — só muda 'Sendo o progr…_

**`obras/epistola-de-tiago.md`**
- L116 · citado `(LE q. 100)` · classe _fabricated_ → **`(LE, q. 101)`**

  - literal da fonte: "101. Características gerais. – Predominância da matéria sobre o espírito. Propensão para o mal. Ignorância, orgulho, egoísmo e todas as paixões que lhes são co…"
  - _O locus citado (q. 100) tem cobertura 0.00 e não traz a frase; a aspa mora verbatim em q. 101 ('Ignorância, orgulho, egoísmo'), cobertura 0.75 — a única lacuna é o inciso interpolado 'desejo de gozos materiais', que não…_

**`personalidades/erasto.md`**
- L26 · citado `(LM, 2ª parte, cap. XVI, item 185)` · classe _uncertain_ → **`(LM, 2ª parte, cap. XVI, item 186)`**

  - literal da fonte: "o dito quadro é, a bem dizer, obra deles. Mediante aspas, destacamos as suas observações textuais, sempre que nos pareceu conveniente assiná-las. São, na sua m…"
  - _reverse_locus dá cobertura 0.94 no item 186 e ~0.18 nos demais; o cite.py do item 185 trata só dos médiuns especiais (não menciona o quadro nem Erasto/Sócrates), enquanto o item 186 termina exatamente com a frase verbat…_

## ✂️ de-quote — paráfrase fiel mal-aspeada: tirar as aspas (vira síntese da wiki) mantendo a citação de apoio — 82


**`aprofundamentos/dor-rigidez.md`**
- L61 · citado `(LE, q. 762)` · classe _fabricated_ · sustenta: `(LE, q. 762)`

  - literal da fonte: "O homem julga necessária uma coisa sempre que não descobre nada melhor."
  - _cite.py q.762 traz "O homem julga necessária uma coisa sempre que não descobre nada melhor"; a aspa "sempre que não se descobre outra melhor" é paráfrase fiel (reverse_locus dá só 0.43 em todo locus, não é verbatim), co…_

**`aprofundamentos/escolha-de-provas.md`**
- L47 · citado `(LE, q. 984–985)` · classe _paraphrase_ · sustenta: `(LE, q. 984)`

  - literal da fonte: "984. As vicissitudes da vida são sempre a punição das faltas atuais? “Não; já dissemos: são provas impostas por Deus, ou que vós mesmos escolhestes como Espíri…"
  - _A aspa não é verbatim (reverse_locus 0.40 em q. 984, nada maior alhures): q. 984 diz ‘são provas impostas por Deus, ou que vós mesmos escolhestes... para expiação das faltas cometidas em outra existência’, mas a wiki re…_

**`aprofundamentos/missao-de-kardec.md`**
- L41 · citado `(ESE, cap. I, item 7)` · classe _fabricated_ · sustenta: `(ESE, Introdução, item II)`

  - literal da fonte: "Quis Deus que a nova revelação chegasse aos homens por mais rápido caminho e mais autêntico. Incumbiu, pois, os Espíritos de levá-la de um polo a outro, manife…"
  - _Aspa não-verbatim em locus nenhum (reverse_locus max 0.21 em cap. I item 6; cite.py do cap. I item 7 traz 'Não vim destruir a lei'), mas é paráfrase fiel do 'controle universal' da Introdução IV ('os Espíritos de levá-l…_
- L42 · citado `(ESE, Introdução, item 4)` · classe _fabricated_ · sustenta: `(ESE, Introdução)`

  - _Aspa aforística sem nenhum match verbatim (grep zero p/ 'grau de revelação'/'fase do progresso'; reverse_locus max 0.38), mas resume fielmente a revelação progressiva que a Introdução trata ('Não atacam as grandes quest…_
- L67 · citado `(LE, Conclusão, item I)` · classe _fabricated_ · sustenta: `(ESE, Introdução, item II)`

  - literal da fonte: "O primeiro controle é, pois, sem contradita, o da razão, ao qual cumpre se submeta, sem exceção, tudo o que venha dos Espíritos. Toda teoria em manifesta contr…"
  - _Aspa não-verbatim no LE (reverse_locus max 0.25; cite.py do Conclusão I trata de magnetismo/mesas girantes, não sustenta a frase), mas é paráfrase fiel do crivo da razão expresso literalmente na Introdução do ESE ('deve…_

**`aprofundamentos/reencarnacao.md`**
- L262 · citado `(ESE, cap. IV, item 18)` · classe _uncertain_ · sustenta: `(ESE, cap. IV, item 18)`

  - literal da fonte: "Os laços de família não sofrem destruição alguma com a reencarnação, como o pensam certas pessoas. Ao contrário, tornam-se mais fortalecidos e apertados. O pri…"
  - _A aspa nao e verbatim em locus nenhum (reverse_locus da no maximo 0.54 em item 23, baixo em todos), mas e parafrase/condensacao fiel do item 18 citado, que diz literalmente que os lacos de familia 'nao sofrem destruicao…_

**`aprofundamentos/sexualidade-em-andre-luiz.md`**
- L103 · citado `(LE, q. 200)` · classe _fabricated_ · sustenta: `(LE, q. 200)`

  - literal da fonte: "200. Têm sexos os Espíritos? “Não como o entendeis, pois que os sexos dependem do organismo. Há entre eles amor e simpatia, mas baseados na semelhança dos sent…"
  - _Reverse_locus dá cobertura baixíssima (0.19) em todo locus — a aspa não é verbatim em parte nenhuma; mas é paráfrase fiel da q.200 citada ('Não como o entendeis, pois que os sexos dependem do organismo'), idea preservad…_

**`conceitos/avareza.md`**
- L22 · citado `(ESE, cap. XVI; S. Lucas, 12:16–21; ver [[wiki/conceitos/parabola-do-rico-insensato]])` · classe _fabricated_ · sustenta: `(ESE, cap. XVI, item 9)`

  - literal da fonte: "E direi a minha alma: Minha alma, tens de reserva muitos bens para longos anos; repousa, come, bebe, goza. – Mas, Deus, ao mesmo tempo, disse ao homem: Que ins…"
  - _reverse_locus dá cobertura baixa (0.38) em todos os loci — a aspa não é verbatim; a parábola do rico insensato está sim em ESE cap. XVI item 9 (linha 2609), mas a redação de Guillon Ribeiro é 'Que insensato és! Esta noi…_

**`conceitos/bem-aventuranca-dos-famintos-de-justica.md`**
- L40 · citado `(ESE, cap. XV, item 5)` · classe _fabricated_ · sustenta: `(ESE, cap. XV, item 5)`

  - literal da fonte: "Não considera, portanto, a caridade apenas como uma das condições para a salvação, mas como a condição única. [...] é que ela implicitamente abrange todas as o…"
  - _A frase 'A caridade é a mais completa e mais sublime expressão da justiça' não é verbatim (reverse_locus máx. 0.33); cite.py em cap. XV item 5 traz 'Fora da caridade não há salvação' e o item ensina que a caridade abran…_

**`conceitos/bem-aventuranca-dos-pobres-de-espirito.md`**
- L43 · citado `(ESE, cap. VII, item 5)` · classe _uncertain_ · sustenta: `(ESE, cap. VII, item 12)`

  - literal da fonte: "O orgulho, eis a fonte de todos os vossos males. Aplicai-vos, portanto, em destruí-lo, se não lhe quiserdes perpetuar as funestas consequências."
  - _A aspa não é verbatim em locus nenhum (reverse_locus: melhor cobertura só 0.53 no item 12; o item 5 citado é apenas a parábola de S. Lucas 14, sem a frase); é síntese fiel — o item 12 diz "O orgulho, eis a fonte de todo…_

**`conceitos/bem-aventuranca-dos-puros-de-coracao.md`**
- L53 · citado `(LM, 2ª parte, cap. XIX, item 226)` · classe _fabricated_ · sustenta: `(LM, 2ª parte, cap. XIX, item 227)`

  - literal da fonte: "Ora, os bons têm afinidade com os bons e os maus com os maus, donde se segue que as qualidades morais do médium exercem influência capital sobre a natureza dos…"
  - _A aspa tem cobertura máxima de 0.23 no reverse_locus (não é verbatim em lugar nenhum) e o item 226 citado trata de outra coisa (se a mediunidade se desenvolve com o moral do médium); a ideia é paráfrase fiel do item 227…_

**`conceitos/caridade.md`**
- L19 · citado `(ESE, cap. XV, item 10)` · classe _fabricated_ · sustenta: `(ESE, cap. XV, item 10)`

  - literal da fonte: "na Terra, porque à sombra desse estandarte eles viverão em paz; no céu, porque os que a houverem praticado acharão graças diante do Senhor."
  - _A aspa não é verbatim em XV.10 (cobertura máx. 0.38 em XXVIII.41, sem locus verbatim), mas é síntese fiel da tese do próprio XV.10 — salvação pela prática efetiva da caridade, não pela crença professada ('os que a houve…_
- L54 · citado `(ESE, cap. XI, item 11)` · classe _fabricated_ · sustenta: `(ESE, cap. XI, item 11)`

  - literal da fonte: "O egoísmo, chaga da Humanidade, tem que desaparecer da Terra, a cujo progresso moral obsta."
  - _A aspa é parafrase fiel do início literal de XI.11 ('O egoísmo, chaga da Humanidade, tem que desaparecer da Terra'), com pequena troca de forma ('da sociedade'/'da face da Terra') — não-verbatim (reverse 0.00) mas a ide…_
- L58 · citado `(ESE, cap. XIII, item 4)` · classe _fabricated_ · sustenta: `(ESE, cap. XIII, item 4)`

  - literal da fonte: "Esses infortúnios discretos e ocultos são os que a verdadeira generosidade sabe descobrir, sem esperar que peçam assistência."
  - _XIII.4 é o relato narrativo da benfeitora discreta; a aspa não é verbatim (reverse máx. 0.32 em XI.14), mas sintetiza fielmente a tese do cap. XIII — caridade verdadeira excede a esmola, abarcando benevolência e cuidado…_

**`conceitos/culto-do-evangelho-no-lar.md`**
- L25 · citado `(ESE, cap. XXVII, item 9)` · classe _fabricated_ · sustenta: `(ESE, cap. XXVII, item 15)`

  - literal da fonte: "A prece em comum tem ação mais poderosa, quando todos os que oram se associam de coração a um mesmo pensamento e colimam o mesmo objetivo, porquanto é como se …"
  - _ESE XXVII item 9 é só a definição de prece (não fala de oração em comum); reverse_locus na aspa dá cobertura baixa (0.19 no melhor, item 15) — a forma aspeada "pelo coração e pelo pensamento, se associam a um mesmo sent…_
- L114 · citado `(ESE, cap. XXVII, item 8)` · classe _uncertain_ · sustenta: `(ESE, cap. XXVII, item 13)`

  - literal da fonte: "Do coração do egoísta, do daquele que apenas de lábios ora, unicamente saem palavras, nunca os ímpetos de caridade que dão à prece todo o seu poder."
  - _ESE XXVII item 8 é o exemplo do homem perdido no deserto, não diz "sentir o que diz"; reverse_locus dá cobertura baixa (0.50 no máx., aponta ESE XXVI item 8 que diz "pedi-las seriamente", não casa) — a aspa não é verbat…_

**`conceitos/desdobramento.md`**
- L23 · citado `(LE, q. 401)` · classe _paraphrase_ · sustenta: `(LE, q. 401)`

  - literal da fonte: "Não, o Espírito jamais está inativo. Durante o sono, afrouxam-se os laços que o prendem ao corpo e, não precisando este então da sua presença, ele se lança pel…"
  - _A aspa não é verbatim em locus nenhum (reverse_locus máx. 0.10 em q.401/402/410); cite.py q.401 traz outra formulação ("o Espírito jamais está inativo... afrouxam-se os laços"), mas a ideia (sono como liberação parcial …_
- L24 · citado `(LE, q. 400, comentário)` · classe _uncertain_ · sustenta: `(LE, q. 155)`

  - literal da fonte: "Durante a vida, o Espírito se acha preso ao corpo pelo seu envoltório semimaterial ou perispírito. A morte é a destruição do corpo somente, não a desse outro e…"
  - _q.400 não tem comentário de Kardec (cite.py só devolve P&R sobre o Espírito aspirar à libertação); a ideia do liame que se rompe pela morte é o comentário de q.155 ("preso ao corpo pelo seu envoltório... A morte é a des…_
- L28 · citado `(LE, q. 439)` · classe _fabricated_ · sustenta: `(LE, q. 439)`

  - literal da fonte: "O êxtase é um sonambulismo mais apurado. A alma do extático é ainda mais independente."
  - _A aspa não é verbatim (reverse_locus máx. 0.20, e em q.153/164/222, não em q.439), mas é paráfrase fiel do que cite.py q.439 realmente diz ("O êxtase é um sonambulismo mais apurado. A alma do extático é ainda mais indep…_

**`conceitos/discernimento-dos-espiritos.md`**
- L60 · citado `(LM, 2ª parte, cap. XXIV, item 267)` · classe _fabricated_ · sustenta: `(LM, 2ª parte, cap. XXIV, item 267)`

  - literal da fonte: "Os Espíritos superiores usam sempre de uma linguagem digna, nobre, elevada, sem eiva de trivialidade; tudo dizem com simplicidade e modéstia, jamais se vanglor…"
  - _A frase entre aspas não é verbatim em locus nenhum (reverse_locus 0.00; 'descortês' nem aparece no cap. XXIV); mas é paráfrase fiel do subitem 4.º do item 267 citado, que diz que o Espírito superior usa linguagem digna/…_

**`conceitos/dor.md`**
- L25 · citado `(LE, q. 920)` · classe _fabricated_ · sustenta: `(LE, q. 967)`

  - literal da fonte: "Somente os Espíritos puros gozam, é exato, da felicidade suprema, mas nem todos os outros são infelizes. Entre os maus e os perfeitos há uma infinidade de grau…"
  - _reverse_locus dá cobertura máxima de 0,25 em todos os loci (não é verbatim em parte nenhuma) e o locus citado q. 920 trata da felicidade na Terra, não da perfeição absoluta; a ideia é paráfrase fiel da q. 967 ('Somente …_

**`conceitos/egoismo.md`**
- L35 · citado `(LE, Conclusão, item III)` · classe _fabricated_ · sustenta: `(LE, q. 918)`

  - literal da fonte: "Se interrogar a própria consciência sobre os atos que praticou, perguntará se não transgrediu essa lei, se não fez o mal, se fez todo o bem que podia [...] faz…"
  - _reverse_locus dá cobertura baixa em todos (máx. 0.33 em q.918) — a aspa interrogativa não é verbatim em parte nenhuma; o locus citado (Conclusão III) trata de ceticismo e fraternidade, não de autoexame, mas a ideia é pa…_

**`conceitos/emancipacao-da-alma.md`**
- L48 · citado `(LM, 2ª parte, cap. XIX, item 223, 2ª; cap. XXV)` · classe _fabricated_ · sustenta: `(LM, 2ª parte, cap. XIX, item 223, 2ª)`

  - literal da fonte: "A alma do médium pode comunicar-se, como a de qualquer outro. Se goza de certo grau de liberdade, recobra suas qualidades de Espírito. Tendes a prova disso nas…"
  - _A frase exata 'o Espírito pode emancipar-se e comunicar-se' não é verbatim em locus nenhum (reverse_locus máx. 0.38), mas é paráfrase fiel da resposta 2ª do item 223, que diz que a alma do médium recobra suas qualidades…_

**`conceitos/evocacao.md`**
- L37 · citado `(LM, 2ª parte, cap. XXV, item 272, paráfrase)` · classe _fabricated_ · sustenta: `(LM, 2ª parte, cap. XXV, item 271)`

  - literal da fonte: "Se o Espírito evocado não pode vir de pronto, o mensageiro (os pagãos diriam Mercúrio) marca um prazo, às vezes de cinco minutos, um quarto de hora e até muito…"
  - _reverse_locus cobre no máximo 0.21 (item 169) — não é verbatim em lugar nenhum; o item 272 citado trata da dificuldade das evocações para os médiuns, não do tema; a ideia (qualquer Espírito vem por evocação se puder) é …_

**`conceitos/expiacao.md`**
- L23 · citado `(LE, q. 132)` · classe _uncertain_ · sustenta: `(LE, q. 196)`

  - literal da fonte: "Não podendo os Espíritos aperfeiçoar-se, a não ser por meio das tribulações da existência corpórea, segue-se que a vida material seja uma espécie de filtro ou …"
  - _A imagem 'uma espécie de filtro ou depurador' é verbatim em LE q. 196 (na pergunta), não em q. 132 (cite.py de q. 132 não contém a frase); reverse_locus dá cobertura 0.62 em q. 196 e ~0 nas demais — a cauda 'de onde sae…_

**`conceitos/fe-raciocinada.md`**
- L23 · citado `(ESE, cap. XIX, item 6)` · classe _uncertain_ · sustenta: `(ESE, cap. XIX, item 7)`

  - literal da fonte: "A fé raciocinada, por se apoiar nos fatos e na lógica, nenhuma obscuridade deixa. A criatura então crê, porque tem certeza, e ninguém tem certeza senão porque …"
  - _Não é verbatim no item 6 citado (cite.py item 6 trata de fé religiosa raciocinada/cega, sem a frase); o item 7 traz a formulação verbatim, mas a aspa da wiki a reescreve ('a que se baseia nos fatos e na lógica, nada dei…_
- L27 · citado `(ESE, cap. XIX, item 4)` · classe _fabricated_ · sustenta: `(ESE, cap. XIX, item 3)`

  - literal da fonte: "Num como noutro caso, pode ela dar lugar a que se executem grandes coisas."
  - _O item 4 citado trata de fé vs. presunção e não contém a frase (cite.py); reverse_locus dá cobertura máxima 0.27, não-verbatim em parte nenhuma. A ideia ('a fé... leva ao cumprimento das grandes coisas') é paráfrase fie…_

**`conceitos/fe.md`**
- L23 · citado `(ESE, cap. XIX, item 6)` · classe _fabricated_ · sustenta: `(ESE, cap. XIX, item 7)`

  - literal da fonte: "A fé raciocinada, por se apoiar nos fatos e na lógica, nenhuma obscuridade deixa. A criatura então crê, porque tem certeza, e ninguém tem certeza senão porque …"
  - _O cite.py do item 6 citado trata de fé religiosa/cega e não contém a aspa; o reverse_locus aponta o item 7 (cob. 0,43, a mais alta) — onde a frase existe verbatim mas com redação diferente da aspa, que é paráfrase fiel …_

**`conceitos/homem-de-bem.md`**
- L21 · citado `(ESE, cap. XVII, item 3)` · classe _fabricated_ · sustenta: `(ESE, cap. XVII, item 3)`

  - _Aspa nao e verbatim (reverse_locus cobertura max 0.24 em loci aleatorios), mas e parafrase fiel do item 3 citado, que diz 'Deposita fe em Deus, na sua bondade, na sua justica e na sua sabedoria' e 'todas as dores... sao…_
- L25 · citado `(ESE, cap. XVII, item 3)` · classe _fabricated_ · sustenta: `(ESE, cap. XVII, item 3)`

  - _Nao verbatim (reverse_locus 0.20), mas parafrase fiel do item 3 citado: 'Se ele interroga a consciencia sobre seus proprios atos, a si mesmo perguntara se violou essa lei... se fez a outrem tudo o que desejara lhe fizes…_
- L27 · citado `(ESE, cap. XVII, item 3)` · classe _paraphrase_ · sustenta: `(ESE, cap. XVII, item 3)`

  - _Nao verbatim, mas reverse_locus aponta o proprio cap. XVII item 3 como top locus; o item diz 'trata-os com bondade e benevolencia... usa da sua autoridade para lhes levantar o moral e nao para os esmagar com o seu orgul…_
- L29 · citado `(ESE, cap. XVII, item 3)` · classe _paraphrase_ · sustenta: `(ESE, cap. XVII, item 3)`

  - _Nao verbatim, mas reverse_locus aponta o proprio cap. XVII item 3 como top locus; o item diz 'sabe que e um deposito de que tera de prestar contas' — parafrase fiel da riqueza como deposito._

**`conceitos/ideoplastia.md`**
- L29 · citado `(LM, 2ª parte, cap. VI)` · classe _fabricated_ · sustenta: `(LM, 2ª parte, cap. VI)`

  - literal da fonte: "Pela combinação dos fluidos, o Espírito pode tornar os seus membros ou todo o seu corpo momentaneamente tangíveis, o que prova haver matéria entre vós e eles."
  - _reverse_locus deu cobertura 0.00 em todos os loci (não é verbatim em LM), mas a ideia é fiel ao cap. VI citado, que ensina que o perispírito se torna visível e momentaneamente tangível pela combinação/condensação dos fl…_

**`conceitos/leis-morais/index.md`**
- L22 · citado `(LE, q. 621)` · classe _fabricated_ · sustenta: `(LE, q. 621)`

  - literal da fonte: "621. Onde está escrita a lei de Deus? “Na consciência.” a) — Visto que o homem traz em sua consciência a lei de Deus, que necessidade havia de lhe ser ela reve…"
  - _reverse_locus dá 0.00 em todos os loci (não é verbatim em parte nenhuma), mas a q. 621 citada diz exatamente a ideia — a lei de Deus está escrita "Na consciência" —, logo a aspa é paráfrase fiel: tirar as aspas mantendo…_

**`conceitos/leis-morais/lei-de-conservacao.md`**
- L56 · citado `(LE, q. 726)` · classe _fabricated_ · sustenta: `(LE, q. 726)`

  - literal da fonte: "Vistam o indigente; consolem o que chora; trabalhem pelo que está enfermo; sofram privações para alívio dos infelizes e então suas vidas serão úteis e agradáve…"
  - _Aspa não-verbatim (reverse_locus max 0.38 em qualquer locus); mas o locus citado q.726 diz literalmente 'suas vidas serão úteis e agradáveis a Deus' apos vestir o indigente, consolar quem chora e trabalhar pelo enfermo …_

**`conceitos/mediunidade-curativa.md`**
- L21 · citado `(LM, 2ª parte, cap. XIV, item 175)` · classe _fabricated_ · sustenta: `(LM, 2ª parte, cap. XIV, item 175)`

  - literal da fonte: "Diremos apenas que este gênero de mediunidade consiste, principalmente, no dom que possuem certas pessoas de curar pelo simples toque, pelo olhar, mesmo por um…"
  - _Reverse_locus dá cobertura máxima de só 0.14-0.33 (não verbatim em parte alguma); o cite.py no item 175 não traz essa frase, mas o item 175 e a definição glossarial de "médiuns curadores" ("exaltação do poder magnético,…_

**`conceitos/mediunidade.md`**
- L52 · citado `(LM, 2ª parte, cap. XXXI, comunicação XII)` · classe _fabricated_ · sustenta: `(LM, 2ª parte, cap. XXXI, comunicação XII)`

  - _A frase entre aspas não é verbatim em locus nenhum (reverse_locus ~0.16 em todos), mas a comunicação XII de Joana d'Arc (cap. XXXI) e o verbete 'Mediunato' do vocabulário sustentam fielmente a ideia de missão providenci…_

**`conceitos/mundos-de-expiacao-e-provas.md`**
- L23 · citado `(ESE, cap. III, item 13)` · classe _fabricated_ · sustenta: `(ESE, cap. III, item 13)`

  - literal da fonte: "Que vos direi dos mundos de expiações que já não saibais, pois basta observeis o em que habitais? [...] Por isso os colocou Deus num mundo ingrato, para expiar…"
  - _reverse_locus dá cobertura máxima 0.18 (não verbatim em lugar nenhum); o item 13 citado descreve o mundo ingrato de expiação por penoso trabalho e misérias, mas a frase sobre a inteligência desenvolver-se nas lutas é sí…_
- L27 · citado `(ESE, cap. III, item 14)` · classe _fabricated_ · sustenta: `(ESE, cap. III, item 4)`

  - literal da fonte: "A Terra pertence à categoria dos mundos de expiação e provas, razão por que aí vive o homem a braços com tantas misérias."
  - _reverse_locus dá cobertura máxima 0.16 (não verbatim); a ideia — Terra é um desses mundos, por isso o homem sujeito a vicissitudes — é parafrase fiel sustentada quase ipsis litteris pelo item 4 e pelo gist do item 14 ci…_
- L39 · citado `(LE, q. 55)` · classe _paraphrase_ · sustenta: `(LE, q. 55)`

  - literal da fonte: "São habitados todos os globos que se movem no espaço? "Sim e o homem terreno está longe de ser, como supõe, o primeiro em inteligência, em bondade e em perfeiç…"
  - _reverse_locus dá cobertura 0.44 em q.55 (não verbatim); é parafrase fiel da pergunta da q.55 ('São habitados todos os globos que se movem no espaço?'), inclusive já rotulada como paraphrase no flag — tirar as aspas mant…_

**`conceitos/mundos-felizes.md`**
- L27 · citado `(ESE, cap. III, item 10)` · classe _paraphrase_ · sustenta: `(ESE, cap. III, item 10)`

  - literal da fonte: "um laço de amor e fraternidade prende uns aos outros todos os homens, ajudando os mais fortes aos mais fracos"
  - _Cobertura 0.45 no item 10 citado (máx. em qualquer locus); o item 10 traz fielmente a ideia ("um laço de amor e fraternidade prende uns aos outros todos os homens"), mas a aspa da wiki ("reúne todos os habitantes") refo…_
- L35 · citado `(ESE, cap. III, item 12)` · classe _fabricated_ · sustenta: `(ESE, cap. III, item 12)`

  - literal da fonte: "os mundos felizes não são orbes privilegiados, visto que Deus não é parcial para qualquer de seus filhos; a todos dá os mesmos direitos e as mesmas facilidades…"
  - _Cobertura 0.14 (máx.) — não verbatim em locus nenhum; porém o item 12 citado sustenta fielmente a ideia (Deus não é parcial, mesmos direitos, conquista pelo trabalho) — a aspa da wiki é paráfrase fiel do locus citado, c…_

**`conceitos/mundos-regeneradores.md`**
- L19 · citado `(ESE, cap. III, item 16)` · classe _uncertain_ · sustenta: `(ESE, cap. III, item 17)`

  - literal da fonte: "Os mundos regeneradores servem de transição entre os mundos de expiação e os mundos felizes. A alma penitente encontra neles a calma e o repouso e acaba por de…"
  - _Aspa nao verbatim em lugar nenhum (reverse_locus 0.46 no item 17, baixo no resto); a frase literal 'servem de transicao... acaba por depurar-se' mora no item 17, nao no 16 citado — parafrase fiel cujo apoio correto e o …_
- L35 · citado `(ESE, cap. III, item 18)` · classe _fabricated_ · sustenta: `(ESE, cap. III, item 17)`

  - literal da fonte: "Nesses mundos, todavia, ainda nao existe a felicidade perfeita, mas a aurora da felicidade. [...] o homem divisa, melhor do que vos, o futuro; compreende a exi…"
  - _reverse_locus 0.13 (nao verbatim); o item 18 cuda da falibilidade/recaida, mas a ideia 'nao plenamente feliz, ja nao desgracado, entreve a felicidade perfeita' e parafrase fiel do item 17 ('aurora da felicidade', 'divis…_

**`conceitos/nao-julgar.md`**
- L17 · citado `(ESE cap. X)` · classe _fabricated_ · sustenta: `(ESE, cap. X, item 11)`

  - literal da fonte: "Não julgueis, a fim de não serdes julgados; – porquanto sereis julgados conforme houverdes julgado os outros; empregar-se-á convosco a mesma medida de que vos …"
  - _Aspa é um H3/título de seção, paráfrase do verso evangélico Mt 7:1; reverse_locus dá cobertura só 0.43 (palavras comuns) — não é verbatim de ESE; o cite.py mostra que o item 11 de ESE cap. X traz a forma de Guillon Ribe…_
- L51 · citado `(ESE cap. X, item 10)` · classe _fabricated_ · sustenta: `(ESE, cap. X, item 19)`

  - literal da fonte: "Mas, por isso mesmo, deveis fazê-lo com moderação, para um fim útil, e não, como as mais das vezes, pelo prazer de denegrir."
  - _Reverse_locus dá cobertura máxima de 0.23 (não-verbatim em parte alguma); o item 10 citado trata de 'ver o mal de outrem antes do próprio', não da censura sem aspereza; a ideia (censurar com moderação, para um fim útil)…_

**`conceitos/parabola-da-figueira-seca.md`**
- L31 · citado `(ESE, cap. XIX, item 10)` · classe _fabricated_ · sustenta: `(ESE, cap. XIX, item 11)`

  - literal da fonte: "A fé: mãe da esperança e da caridade. 11. Para ser proveitosa, a fé tem de ser ativa; não deve entorpecer-se. Mãe de todas as virtudes que conduzem a Deus... A…"
  - _Item 10 (citado) trata dos médiuns/figueira estéril e não contém a frase; reverse_locus dá cobertura máxima de só 0.40 — não é verbatim em lugar nenhum. A frase é uma reformulação ('A fé é a mãe...') do título de seção …_

**`conceitos/parabola-do-filho-prodigo.md`**
- L31 · citado `(LE, q. 1001)` · classe _fabricated_ · sustenta: `(LE, q. 1000)`

  - literal da fonte: "Já desde esta vida poderemos ir resgatando as nossas faltas? “Sim, reparando-as. (...) Só por meio do bem se repara o mal, e a reparação nenhum mérito apresent…"
  - _A aspa “sempre se pode reparar o mal que se fez” não é verbatim em locus nenhum (reverse_locus cobertura máx. 0.33); q. 1001 trata do legado de bens após a morte, não de reparação, mas a ideia é paráfrase fiel da q. 100…_

**`conceitos/parabola-do-juiz-iniquo.md`**
- L23 · citado `(ESE, cap. XXVII, item 7)` · classe _fabricated_ · sustenta: `(ESE, cap. XXVII, item 7)`

  - _Apresentada como aspa literal de Kardec ("Como Kardec formula de modo lapidar"), mas o reverse_locus dá cobertura máxima de só 0.33 (em ESE cap. V) e o cite.py do item 7 citado não traz a frase — é um epigrama devociona…_

**`conceitos/passe.md`**
- L23 · citado `(Gênese, cap. XIV, item 14)` · classe _uncertain_ · sustenta: `(Gênese, cap. XIV, item 14)`

  - literal da fonte: "Os Espíritos atuam sobre os fluidos espirituais, não manipulando-os como os homens manipulam os gases, mas empregando o pensamento e a vontade. [...] Pelo pens…"
  - _Não é verbatim em locus nenhum (reverse_locus: item 18 só 0.67, item 14 nem aparece no top-3), mas é paráfrase fiel: item 14 afirma que os Espíritos, pelo pensamento, imprimem aos fluidos espirituais direção/forma ('Pel…_

**`conceitos/potencias-da-alma.md`**
- L25 · citado `(LE, q. 621)` · classe _fabricated_ · sustenta: `(LE, q. 621)`

  - literal da fonte: "621. Onde esta escrita a lei de Deus? "Na consciencia." a) — Visto que o homem traz em sua consciencia a lei de Deus, que necessidade havia de lhe ser ela reve…"
  - _Aspa nao e verbatim (q.621 diz 'Na consciencia', nao 'gravou no coracao do homem'; cobertura baixa em todos), mas e parafrase fiel da ideia do proprio locus citado q.621 — a lei de Deus esta inscrita no interior do home…_
- L29 · citado `(LE, q. 843)` · classe _uncertain_ · sustenta: `(LE, q. 872)`

  - literal da fonte: "872. A questao do livre-arbitrio se pode resumir assim: o homem nao e fatalmente levado ao mal; os atos que pratica nao foram previamente determinados; os crim…"
  - _Aspa nao e verbatim no q.843 citado (que so traz 'Tem o homem o livre-arbitrio...'); e parafrase de q.872 (cobertura 0.76), que diz 'o homem nao e fatalmente levado ao mal; os atos que pratica nao foram previamente dete…_

**`conceitos/prece.md`**
- L19 · citado `(ESE, cap. XXVII, item 1)` · classe _fabricated_ · sustenta: `(ESE, cap. XXVII, item 9)`

  - literal da fonte: "A prece é uma invocação, mediante a qual o homem entra, pelo pensamento, em comunicação com o ser a quem se dirige."
  - _reverse_locus dá cobertura máxima 0.25 (não verbatim em lugar nenhum); o item 1 citado é só a passagem de Mateus 6:5-8, mas a ideia 'prece é comunicação com Deus' é fiel ao item 9 ('o homem entra, pelo pensamento, em co…_
- L19 · citado `(ESE, cap. XXVII, item 4)` · classe _fabricated_ · sustenta: `(ESE, cap. XXVII, item 4)`

  - literal da fonte: "Não afeteis orar muito, pois não é pela multiplicidade das palavras que sereis escutados, mas pela sinceridade delas."
  - _reverse_locus cobertura máxima 0.27 (não verbatim); o item 4 citado sustenta fielmente a ideia de orar com o coração e não por fórmula ('pela sinceridade delas', 'coração purificado'), só muda a forma._
- L23 · citado `(ESE, cap. XXVII, item 7)` · classe _fabricated_ · sustenta: `(ESE, cap. XXVII, item 6)`

  - literal da fonte: "Sem dúvida alguma há leis naturais e imutáveis que não podem ser ab-rogadas ao capricho de cada um."
  - _reverse_locus cobertura máxima 0.23 (não verbatim); a ideia 'Deus não muda a ordem da Natureza ao gosto de cada um' é fiel ao item 6 ('leis naturais e imutáveis que não podem ser ab-rogadas ao capricho de cada um'), loc…_
- L27 · citado `(ESE, cap. XXVII, item 9)` · classe _fabricated_ · sustenta: `(ESE, cap. XXVII, item 11)`

  - literal da fonte: "Pela prece, obtém o homem o concurso dos bons Espíritos que acorrem a sustentá-lo em suas boas resoluções e a inspirar-lhe ideias sãs."
  - _reverse_locus cobertura máxima 0.43 no item 11 (não verbatim, mas paráfrase próxima); a frase citada reescreve o item 11 ('obtém'→'atrai', 'acorrem a sustentá-lo'→'secundam', 'ideias sãs'→'bons pensamentos'), não o item…_
- L31 · citado `(ESE, cap. XXVII, item 5)` · classe _fabricated_ · sustenta: `(ESE, cap. XXVII, item 4)`

  - literal da fonte: "Não afeteis orar muito, pois não é pela multiplicidade das palavras que sereis escutados, mas pela sinceridade delas."
  - _reverse_locus cobertura 0.00 (não verbatim); o item 5 citado é só Marcos 11:24, mas a ideia 'prece sentida vale mais que fórmula repetida' é fiel ao item 4 (sinceridade > multiplicidade de palavras)._
- L35 · citado `(ESE, cap. XXVII, item 18)` · classe _fabricated_ · sustenta: `(ESE, cap. XXVII, item 18)`

  - literal da fonte: "É nesse sentido que lhes pode não só aliviar, como abreviar os sofrimentos."
  - _reverse_locus cobertura máxima 0.21 (não verbatim); o item 18 citado sustenta fielmente a ideia de que a prece pode aliviar e abreviar os sofrimentos do Espírito sofredor ('pode não só aliviar, como abreviar os sofrimen…_

**`conceitos/responsabilidade.md`**
- L11 · citado `(ESE, cap. XVI; S. Lucas, 12:48)` · classe _fabricated_ · sustenta: `(ESE, cap. XVI, item 13)`

  - literal da fonte: "Sendo o homem o depositário, o administrador dos bens que Deus lhe pôs nas mãos, contas severas lhe serão pedidas do emprego que lhes haja ele dado, em virtude…"
  - _reverse_locus dá 0.00 em todo o ESE — a aspa não é verbatim de Kardec, é paráfrase do logion bíblico de S. Lucas 12:48; mas a ideia (prestação de contas proporcional ao que se recebeu/foi confiado) é fielmente sustentad…_

**`conceitos/suicidio.md`**
- L48 · citado `(LE, q. 953, paráfrase)` · classe _fabricated_ · sustenta: `(LE, q. 951)`

  - literal da fonte: "Isso é sublime, conforme a intenção, e, em tal caso, o sacrifício da vida não constitui suicídio."
  - _A aspa já é auto-rotulada 'paráfrase' e o reverse_locus não a acha verbatim em lugar nenhum (cobertura máx. 0.24); q.953 trata de abreviar a própria morte ante fim inevitável, não de arriscar a vida por outrem — a ideia…_
- L85 · citado `(C&I, 2ª parte, cap. IV)` · classe _fabricated_ · sustenta: `(C&I, 2ª parte, cap. IV)`

  - literal da fonte: "Aquele que sacrifica aos instintos brutais a inteligência e os bons sentimentos que Deus pôs nele, assemelha-se ao animal que ele muitas vezes maltrata. [...] …"
  - _A aspa é uma concatenação de dois fragmentos do relato 'Arrependimento de um dissoluto' (cap. IV) — 'sacrifica aos instintos brutais' e 'desprender-se dos gozos materiais' — que não existe como string contígua verbatim,…_

**`conceitos/tres-revelacoes.md`**
- L19 · citado `(ESE, cap. I, item 5)` · classe _fabricated_ · sustenta: `(ESE, cap. I, item 2)`

  - literal da fonte: "Todas as outras são leis que Moisés decretou, obrigado que se via a conter, pelo temor, um povo de seu natural turbulento e indisciplinado [...] só a ideia de …"
  - _reverse_locus 0.00 em todo o ESE — não verbatim em parte nenhuma; o item 5 citado fala do Espiritismo como ciência, não de Moisés; mas a ideia (a lei mosaica conteve pelo temor um povo rude/ignorante) é paráfrase fiel d…_
- L23 · citado `(ESE, cap. I, item 6)` · classe _uncertain_ · sustenta: `(ESE, cap. I, item 7)`

  - literal da fonte: "Assim como o Cristo disse: "Não vim destruir a lei, porém cumpri-la""
  - _reverse_locus dá só 0.62 no item 7 e 0.00 no item 6 citado (que trata do ser coletivo); a forma da wiki ('destruir a Lei, mas completá-la') é paráfrase — Kardec escreve 'porém cumpri-la' (item 7) / 'veio cumpri-la' (ite…_
- L43 · citado `(ESE, cap. I, item 7)` · classe _fabricated_ · sustenta: `(ESE, cap. I, item 6)`

  - literal da fonte: "O Espiritismo é a terceira revelação da lei de Deus, mas não tem a personificá-la nenhuma individualidade [...] É, de certa maneira, um ser coletivo, formado p…"
  - _reverse_locus só 0.38 no item 6 (cobertura baixa = não verbatim) e o item 7 citado não contém a frase; a ideia ('ser coletivo', 'nenhuma individualidade a personificá-la') é paráfrase fiel de ESE cap. I, item 6, não do …_
- L47 · citado `(ESE, Introdução, item 4)` · classe _fabricated_ · sustenta: `(ESE, cap. I, item 3)`

  - literal da fonte: "Jesus não veio destruir a lei [...] veio cumpri-la, isto é, desenvolvê-la, dar-lhe o verdadeiro sentido e adaptá-la ao grau de adiantamento dos homens."
  - _reverse_locus máx 0.38 (não verbatim em nenhum locus) e a Introdução nem tem 'item 4' numerado (é estruturada por seções romanas I–IV); o aforismo é síntese fiel da tese da revelação progressiva ('adaptá-la ao grau de a…_

**`conceitos/verdadeiro-espirita.md`**
- L53 · citado `(LE, Conclusão, item III)` · classe _fabricated_ · sustenta: `(LE, q. 918)`

  - literal da fonte: "Se interrogar a própria consciência sobre os atos que praticou, perguntará se não transgrediu essa lei, se não fez o mal, se fez todo o bem que podia, se ningu…"
  - _reverse_locus não acha a aspa verbatim em lugar nenhum (cobertura máx. 0.33 em q.918); o locus citado (Conclusão item III) trata de Espiritismo vs. incredulidade e não contém a ideia, mas a LE q.918 descreve fielmente o…_
- L53 · citado `(ESE, cap. XV, item 10)` · classe _uncertain_ · sustenta: `(ESE, cap. XV, item 10)`

  - literal da fonte: "Esforçai-vos, pois, para que os vossos irmãos, observando-vos, sejam induzidos a reconhecer que verdadeiro espírita e verdadeiro cristão são uma só e a mesma c…"
  - _A aspa não é verbatim no locus citado (reverse_locus máx. 0.50, em cap. XXI item 10, onde 'dar o mais formal desmentido' aparece mas referido a falsos Espíritos, contexto diverso); o cap. XV item 10 sustenta a ideia ('v…_

**`conceitos/vida-futura.md`**
- L19 · citado `(ESE, cap. II, item 2)` · classe _uncertain_ · sustenta: `(ESE, cap. II, item 2)`

  - _Aspa não é verbatim em locus nenhum (reverse_locus máx 0.56 em cap. XXIII, item 8; 0 no citado), mas é síntese fiel da tese do cap. II — item 5 diz 'a vida corpórea se torna simples passagem' e o capítulo todo apresenta…_
- L27 · citado `(ESE, cap. II, item 3)` · classe _fabricated_ · sustenta: `(ESE, cap. II, item 6)`

  - literal da fonte: "Simplesmente, aquele que se preocupa com o futuro não liga ao presente mais do que relativa importância e facilmente se consola dos seus insucessos, pensando n…"
  - _Aspa não é verbatim (reverse_locus máx 0.12) e o item 3 citado trata da noção imprecisa dos judeus; mas a ideia é paráfrase fiel do item 6 ('aquele que se preocupa com o futuro não liga ao presente mais do que relativa …_

**`divergencias/escravidao-em-efesios-6.md`**
- L103 · citado `(LE q. 825–828, contexto)` · classe _fabricated_ · sustenta: `(LE, q. 829)`

  - literal da fonte: "É contrária à lei de Deus toda sujeição absoluta de um homem a outro homem. A escravidão é um abuso da força. Desaparece com o progresso, como gradativamente d…"
  - _reverse_locus dá cobertura máxima 0.21 (não-verbatim em lugar nenhum) e a frase entre aspas não aparece literal no locus citado (q.825-828, sobre liberdade relativa); mas é paráfrase fiel de LE q.829, que diz literalmen…_

**`divergencias/predestinacao-em-romanos-8-9.md`**
- L70 · citado `(LE q. 115, q. 121)` · classe _fabricated_ · sustenta: `(LE, q. 115)`

  - literal da fonte: "Deus criou todos os Espíritos simples e ignorantes, isto é, sem saber. A cada um deu determinada missão, com o fim de esclarecê-los e de os fazer chegar progre…"
  - _O Q&A 'chegarão todos os Espíritos à perfeição? Sim, por mais penoso que lhes seja o caminho' não é verbatim em locus nenhum (reverse_locus <=0.50, disperso); mas a ideia é fiel a q.115, que diz que Deus criou os Espíri…_

**`divergencias/recaida-sem-arrependimento-em-hebreus.md`**
- L120 · citado `(LE q. 1009)` · classe _fabricated_ · sustenta: `(LE, q. 1009)`

  - _reverse_locus dá cobertura 0.00 para "mais dolorosas e mais prolongadas" em todo o LE (não é verbatim em lugar nenhum), mas a ideia de que a duração/gravidade da pena depende do culpado é fiel a q. 1009 ("no fazer que a…_

**`obras/epistola-aos-efesios.md`**
- L153 · citado `(LE q. 829, paráfrase do comentário)` · classe _uncertain_ · sustenta: `(LE, q. 829)`

  - literal da fonte: "É contrária à lei de Deus toda sujeição absoluta de um homem a outro homem. A escravidão é um abuso da força. Desaparece com o progresso, como gradativamente d…"
  - _Não é verbatim em locus nenhum (reverse_locus: máx. 0.62 em q.799, sem frase contígua); mas q.829 sustenta fielmente a ideia — diz que a escravidão é 'um abuso da força', 'contrária à lei de Deus' e degrada o homem 'fís…_

**`obras/epistola-aos-galatas.md`**
- L105 · citado `(ESE cap. XV, item 10)` · classe _fabricated_ · sustenta: `(ESE, cap. XV, item 10)`

  - literal da fonte: "uma virtude negativa não basta: é necessária uma virtude ativa; para fazer-se o bem, mister sempre se torna a ação da vontade; para não se praticar o mal, bast…"
  - _Aspa não-verbatim (reverse_locus top 0.38, nenhuma cobertura alta), mas o cite.py confirma que ESE cap. XV, item 10 ensina fielmente a ideia — 'uma virtude negativa não basta: é necessária uma virtude ativa' (responsabi…_

**`obras/felizes-os-pobres-em-espirito-carlos-mendonca.md`**
- L47 · citado `(ESE, cap. VII, item 2)` · classe _paraphrase_ · sustenta: `(ESE, cap. VII, item 2)`

  - literal da fonte: "Por pobres de espírito Jesus não entende os baldos de inteligência, mas os humildes, tanto que diz ser para estes o reino dos céus e não para os orgulhosos."
  - _O locus citado está correto, mas a aspa não é verbatim (cobertura 0.44 no reverse_locus; cite.py traz 'não entende os baldos de inteligência, mas os humildes', enquanto a wiki escreve 'não se refere aos homens desprovid…_

**`obras/livro-dos-espiritos.md`**
- L130 · citado `(LE, q. 920–921, paráfrase)` · classe _fabricated_ · sustenta: `(LE, q. 920–921)`

  - literal da fonte: "920. Pode o homem gozar de completa felicidade na Terra? "Não, pois a vida lhe foi dada como prova ou expiação. Dele, porém, depende a suavização de seus males…"
  - _reverse_locus dá só 0.30 no melhor locus (não é verbatim em lugar nenhum), mas a frase entre aspas é paráfrase fiel de q.920 ("Não, pois a vida lhe foi dada como prova") + q.921 (felicidade relativa pela prática da lei …_

**`obras/livro-dos-mediuns.md`**
- L142 · citado `(LM, 2ª parte, cap. XXVIII, item 304, paráfrase)` · classe _fabricated_ · sustenta: `(LM, 2ª parte, cap. XXVIII, item 304)`

  - _Não é verbatim em locus nenhum (reverse_locus ~0.17 em todos), e a própria citação já marca '(paráfrase)'; o item 304 trata de não explorar/comercializar a faculdade mediúnica, sustentando fielmente a ideia — tirar as a…_

**`obras/segunda-epistola-a-timoteo.md`**
- L198 · citado `(ESE cap. XIX, item 7)` · classe _fabricated_ · sustenta: `(ESE, cap. XIX, item 7)`

  - literal da fonte: "Fé inabalável só o é a que pode encarar de frente a razão em todas as épocas da humanidade."
  - _O locus citado (ESE cap. XIX, item 7) traz verbatim 'Fé inabalável só o é a que pode encarar de frente a razão em todas as épocas da humanidade'; a aspa 'encarar a razão face a face' é parafrase fiel (reverse_locus 0.00…_

**`obras/segunda-epistola-de-pedro.md`**
- L124 · citado `(LE q. 131; [[wiki/obras/ceu-e-inferno|C&I]] 1ª parte cap. IX, "Anjos e demônios", itens 4–21)` · classe _fabricated_ · sustenta: `(LE, q. 131)`

  - literal da fonte: "Os homens fizeram com os demônios o que fizeram com os anjos. Assim como acreditaram na existência de seres perfeitos desde toda a eternidade, também tomaram o…"
  - _A frase 'anjos criados perfeitos que caíram' tem cobertura 0.00 no reverse_locus em LE e em C&I — não é verbatim em lugar nenhum; é a formulação da própria wiki para a doutrina REJEITADA (aspas de rótulo na construção '…_

**`personalidades/espiritos-reveladores.md`**
- L53 · citado `(LE, Prolegômenos)` · classe _fabricated_ · sustenta: `(LE, Prolegômenos)`

  - literal da fonte: "Entre os Espíritos que concorreram para a execução desta obra, muitos se contam que viveram, em épocas diversas, na Terra, onde pregaram e praticaram a virtude…"
  - _O cite.py dos Prolegômenos não contém a frase entre aspas e o reverse_locus dá cobertura máxima de 0,14 em todo o LE (e 0,14 no ESE) — não é verbatim em lugar nenhum; mas a ideia da sanção histórica por homens eminentes…_

**`questoes/arrependimento-expiacao-e-reparacao.md`**
- L43 · citado `(LE, q. 1007)` · classe _uncertain_ · sustenta: `(LE, q. 1007)`

  - literal da fonte: "Há Espíritos de arrependimento muito tardio; pretender-se, porém, que nunca se melhorarão seria negar a lei do progresso, como alguém que dissesse que a crianç…"
  - _A aspa não é verbatim em locus nenhum (reverse_locus dá cobertura máxima 0.46 na própria q. 1007); o cite.py mostra que o texto real de q. 1007 diz 'pretender-se, porém, que nunca se melhorarão seria negar a lei do prog…_

**`sinteses/sermao-do-monte-em-emmanuel.md`**
- L143 · citado `(ESE, cap. XVII, item 4)` · classe _fabricated_ · sustenta: `(ESE, cap. XVII, item 4)`

  - literal da fonte: "Reconhece-se o verdadeiro espírita pela sua transformação moral e pelos esforços que emprega para domar suas inclinações más."
  - _reverse_locus 0.00 em todos os loci (não-verbatim em lugar nenhum), mas o locus citado ESE cap. XVII item 4 traz literalmente 'Reconhece-se o verdadeiro espírita pela sua transformação moral e pelos esforços que emprega…_

## ⚠️ defer — fabricação genuína ou caso doutrinário/ambíguo → decisão humana — 20


**`aprofundamentos/dor-rigidez.md`**
- L185 · citado `(LE, Conclusão, item III)` · classe _fabricated_

  - _A frase "Que fiz do orgulho e da vaidade? Sacrifiquei-os?" não é verbatim em locus nenhum (reverse_locus 0.40 em tudo, grep vazio) e a Conclusão III (cite.py, linhas 3328-3330) trata de fraternidade vs. ceticismo, não d…_

**`aprofundamentos/escolha-de-provas.md`**
- L284 · citado `(ESE, cap. V, item 12)` · classe _fabricated_

  - _A aspa não é verbatim em locus nenhum (reverse_locus máx. 0.24 em ESE, 0.18 em LE); o item 12 citado trata da parábola do devedor e não afirma o sofrimento como ‘único meio’ — o absoluto ‘único’ extrapola tanto o item 1…_

**`conceitos/bem-aventuranca-dos-famintos-de-justica.md`**
- L30 · citado `(ESE, cap. V, item 16)` · classe _fabricated_

  - _O locus citado (ESE cap. V, item 16) trata do suicídio e da incredulidade, não de 'justos, pobres e aflitos'; reverse_locus dá cobertura máx. 0.19 em qualquer item e a expressão 'três palavras — justos, pobres e aflitos…_

**`conceitos/bem-aventuranca-dos-perseguidos.md`**
- L19 · citado `(ESE, cap. V, item 16)` · classe _fabricated_

  - _O locus citado (ESE cap. V item 16) trata de suicídio e materialismo, não de "justos, pobres e aflitos"; a frase nao aparece verbatim em parte alguma do ESE (grep zero; reverse_locus máx. 0.12) e a ideia nao é parafrase…_

**`conceitos/caridade.md`**
- L25 · citado `(ESE, cap. XIII, item 6)` · classe _uncertain_

  - _Não-verbatim em XIII.6 (que trata do desejo de riquezas para o bem; reverse máx. 0.45 em XI.6) e a formulação 'restituir-lhe o que lhe é devido' não aparece nesse locus nem é claramente sustentada por ele — caso incerto…_
- L26 · citado `(ESE, cap. XI, item 9)` · classe _fabricated_

  - _XI.9 (Fénelon, 'o amor é de essência divina') não contém a definição tripartite benevolência/indulgência/perdão; reverse máx. 0.21 — a taxonomia 'caridade moral vs material' não está nesse locus nem é parafrase fiel del…_

**`conceitos/cartas-vivas-de-jesus.md`**
- L32 · citado `(LM, 2ª parte, cap. XX, item 220 e seguintes)` · classe _fabricated_

  - _Aspa não é verbatim em locus nenhum (reverse_locus máx. 0.33 em item 264; cobertura baixa em todos); o item 220 citado trata de intermitência da faculdade e na 14ª pergunta afirma o OPOSTO — a mediunidade 'não constitui…_

**`conceitos/culto-do-evangelho-no-lar.md`**
- L19 · citado `(LE, q. 666)` · classe _fabricated_

  - _LE q.666 trata de orar AOS Espíritos bons ("Pode-se orar aos Espíritos?"), nada diz sobre lugar nem sobre lugares particulares de reunião; reverse_locus na aspa dá cobertura máxima 0.33 (não-verbatim em lugar nenhum no …_

**`conceitos/fe.md`**
- L51 · citado `(ESE, cap. XIX, item 12)` · classe _fabricated_

  - _"Crê e caminha! A fé é o farol que dissipa as trevas" não é verbatim em locus nenhum (reverse_locus 0,00 para "Crê e caminha"; nenhuma ocorrência de "farol que dissipa" no ESE), o item 12 citado trata de fé como sentime…_

**`conceitos/mundos-de-expiacao-e-provas.md`**
- L35 · citado `(ESE, cap. III, item 4)` · classe _fabricated_

  - _reverse_locus dá cobertura máxima 0.27 (não verbatim); o item 4 citado é a classificação das categorias de mundos e NÃO contém nem sustenta o aforismo 'a dor é o aguilhão que leva o Espírito a avançar' — locus citado fa…_

**`conceitos/mundos-felizes.md`**
- L31 · citado `(ESE, cap. III, item 11)` · classe _fabricated_

  - _Cobertura 0.00-0.31 em toda a ESE; o item 11 citado trata da necessidade de contrastes (mal/bem, noite/luz), não diz nada disto, e a 2ª oração ("As artes, as ciências, a indústria são cultivadas... para o bem geral") nã…_

**`conceitos/mundos-regeneradores.md`**
- L23 · citado `(ESE, cap. III, item 17)` · classe _paraphrase_

  - _reverse_locus 0.12 em toda parte (nao verbatim); o item 17 diz que o homem 'ainda tem de suportar provas' e e 'sujeito as vicissitudes', logo afirmar que 'doencas, sofrimentos, tribulacoes ja sao passado' contradiz o te…_
- L27 · citado `(ESE, cap. III, item 17)` · classe _fabricated_

  - _reverse_locus baixo (0.09); equidade/amor/inveja sao do item 17, mas 'autoridade conquistada pela superioridade moral... ninguem se arvora em senhor' e material dos mundos felizes (item 10: 'so a superioridade moral... …_

**`conceitos/orgulho.md`**
- L31 · citado `(LE, Conclusão, item III)` · classe _fabricated_

  - _reverse_locus dá cobertura máxima de 0.44 (q.487/604/940) e nenhum grep no LE acha "Sacrifiquei" ou "Que fiz"; o locus citado (LE, Conclusão, III) trata da polêmica Espiritismo vs. incredulidade e ordem social, sem qual…_

**`conceitos/parabola-do-semeador.md`**
- L33 · citado `(ESE, cap. XVII, item 6)` · classe _fabricated_

  - _cite.py confirma que ESE cap. XVII, item 6 trata da parábola do semeador, mas o texto descreve as categorias de ouvintes (curiosos, frios/indiferentes, os que admiram os conselhos mas só os aplicam aos outros) e NÃO con…_

**`conceitos/potencias-da-alma.md`**
- L21 · citado `(LE, q. 459)` · classe _uncertain_

  - _Aspa nao e verbatim em locus nenhum (cobertura max 0.59 em q.375, sobre a materia reagir no Espirito, sentido inverso); o locus citado q.459 trata de Espiritos influirem em nossos pensamentos, nao do Espirito atuar sobr…_

**`conceitos/vida-futura.md`**
- L23 · citado `(ESE, cap. II, item 5)` · classe _fabricated_

  - _Aspa não é verbatim (reverse_locus máx 0.15) e o item 5 citado trata do efeito moral da crença na vida futura, não da encarnação como meio de aperfeiçoamento; a ideia é doutrina reencarnacionista (LE), não está nesse lo…_
- L31 · citado `(LE, q. 149)` · classe _fabricated_

  - _Aspa não é verbatim (reverse_locus máx 0.40 em q.319/329); q.149 pergunta 'Que sucede à alma no instante da morte?' e responde 'Volta a ser Espírito...', não define 'vida futura como a que se segue ao túmulo' — definiçã…_

**`divergencias/jesus-igual-a-deus-em-filipenses-2.md`**
- L116 · citado `(Gênese cap. XVII)` · classe _uncertain_

  - _reverse_locus na Gênese topa em 0.60 (cap. I, item 10) — não verbatim em locus nenhum; o cap. XVII citado é 'Predições do Evangelho' (ninguém é profeta em sua terra) e não trata do Espírito Santo, logo não sustenta a id…_

**`obras/epistola-aos-romanos.md`**
- L134 · citado `(ESE cap. XII, item 3, comentário)` · classe _fabricated_

  - _cite.py em ESE cap. XII item 3 trata só do sentido de "amar os inimigos" (não fala em brandura nem em vingança); reverse_locus dá cobertura baixa em todo o ESE (0.38 para o 1º fragmento, 0.22 para o 2º) e os termos "é m…_


---

## Validação adversarial (2026-06-17) — addendum

> O passe adversarial **LLM** (70 céticos re-derivando cada veredicto) **falhou no limite de sessão** (reseta 16:10 America/Sao_Paulo) — 0 pareceres. Em substituição, validação **determinística** (cite.py + reverse_locus + grep no raw) dos veredictos de alegação *falsificável* (verbatim). A fidelidade das 82 paráfrases (de-quote) **não** é checável sem LLM → segue pendente do reset.

**keep (19/19) — CONFIRMADOS.** Todas verbatim no raw da obra citada (artefato de extração do cite.py em markup irregular: LM item 223 sub-respostas, ESE cap. XXVIII oração, etc.). **Não-problemas; nenhuma ação.**

**reanchor (7) — locus certo, mas 3 ressalvas que o `word_coverage` (lenient) mascarou:**
- ✗ **homem-de-bem L33 — MIS-VERDITO.** "A perfeição moral consiste em praticar a lei de justiça, de amor e de caridade, na sua maior pureza" **não** existe verbatim em q.893 nem em q.918. q.918 diz "O verdadeiro homem de bem é o que **pratica** a lei de justiça, amor e caridade, na sua maior pureza". É **paráfrase** (de-quote), não mal-atribuição. → revisão humana.
- ⚠ **deriva de palavra** (locus certo, texto a alinhar ao verbatim): tres-revelacoes "vim"→"venho" (ESE I.7); predestinacao "O progresso é…" vs fonte "Sendo o progresso…" (LE q.781 — beira de-quote); erasto "Este quadro" vs "o dito quadro" (LM 2ª/XVI/186); epistola-de-tiago interpolação "desejo de gozos materiais" não está em q.101.
- ✓ **limpos (exatos contra a fonte)**: amorterapia → LE q. 886; tres-revelacoes → ESE I.7 (após "vim"→"venho").

**de-quote (82) + defer (20) — NÃO validados.** Dependem do passe LLM (fidelidade da paráfrase / fabricação genuína), bloqueado até 16:10.

**Aplicação:** tentei aplicar os 2 limpos (amorterapia, tres-revelacoes); **bloqueados pelo pre-flight** (branch 1 commit atrás de main). Nenhuma página alterada.
