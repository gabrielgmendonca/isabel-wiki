# Relatório de crítica profunda — 2026-10-16

## 1. Metadados do run

- **Data:** 2026-10-16
- **Escopo:** `--path (23 páginas ligadas a Há Dois Mil Anos)`
- **Budget:** 8 agentes Opus (3 páginas grandes isoladas + 5 lotes de 4 personagens); verificação dos 6 achados diferidos feita no main-session com grab.py (fatos de enredo decidíveis por texto)
- **Modelos:** critica=opus, verificacao=main-session + grab.py
- **Páginas devidas / criticadas / puladas:** 23 / 23 / 0
- **Total de achados:** 27 (26 auto, 0 diferidos, 1 descartados)

## 2. Páginas avaliadas

| Página | Tipo | Veredito | Achados | Auto | Diferidos |
|--------|------|----------|---------|------|-----------|
| `wiki/personalidades/publio-lentulus.md` | personalidade | ✓ 4 auto | 4 | 4 | 0 |
| `wiki/personalidades/livia.md` | personalidade | ✓ 4 auto | 4 | 4 | 0 |
| `wiki/personalidades/simeao-da-samaria.md` | personalidade | ✓ 4 auto · ✕ 1 desc | 5 | 4 | 0 |
| `wiki/personalidades/joao-de-cleofas.md` | personalidade | ✓ 4 auto | 4 | 4 | 0 |
| `wiki/personalidades/poncio-pilatos.md` | personalidade | ✓ 3 auto | 3 | 3 | 0 |
| `wiki/personalidades/ana-samaritana.md` | personalidade | limpo | 0 | 0 | 0 |
| `wiki/personalidades/flavia-lentulia.md` | personalidade | ✓ 2 auto | 2 | 2 | 0 |
| `wiki/personalidades/marcus-lentulus.md` | personalidade | limpo | 0 | 0 | 0 |
| `wiki/personalidades/flaminio-severus.md` | personalidade | limpo | 0 | 0 | 0 |
| `wiki/personalidades/calpurnia.md` | personalidade | limpo | 0 | 0 | 0 |
| `wiki/personalidades/agripa-severus.md` | personalidade | limpo | 0 | 0 | 0 |
| `wiki/personalidades/plinio-severus.md` | personalidade | limpo | 0 | 0 | 0 |
| `wiki/personalidades/fulvia-procula.md` | personalidade | limpo | 0 | 0 | 0 |
| `wiki/personalidades/aurelia.md` | personalidade | limpo | 0 | 0 | 0 |
| `wiki/personalidades/emiliano-lucius.md` | personalidade | limpo | 0 | 0 | 0 |
| `wiki/personalidades/sulpicio-tarquinius.md` | personalidade | limpo | 0 | 0 | 0 |
| `wiki/personalidades/andre-de-gioras.md` | personalidade | limpo | 0 | 0 | 0 |
| `wiki/personalidades/saul-de-gioras.md` | personalidade | limpo | 0 | 0 | 0 |
| `wiki/personalidades/pompilio-crasso.md` | personalidade | limpo | 0 | 0 | 0 |
| `wiki/personalidades/araxes.md` | personalidade | limpo | 0 | 0 | 0 |
| `wiki/sinteses/chamado-do-cristo-em-ha-dois-mil-anos.md` | sintese | limpo | 0 | 0 | 0 |
| `wiki/sinteses/consolador-em-ha-dois-mil-anos.md` | sintese | ✓ 1 auto | 1 | 1 | 0 |
| `wiki/obras/ha-dois-mil-anos.md` | obra | ✓ 4 auto | 4 | 4 | 0 |

## 3. Achados por eixo

### Eixo 2 — Citações (24)

- **[media]** `wiki/personalidades/publio-lentulus.md`:24 — ✓ auto-corrigido
  - Afirmação: Fala do tribunal espiritual parafraseada como se fosse literal.
  - Evidência: 1ª p., cap. I: 'Hemos determinado que serás poderoso e rico, para que o teu desprendimento dos caminhos humanos seja mais valioso...'
  - Ação: `replace-text` — aspa trocada pelo texto literal; locus 1ª parte, cap. I
- **[media]** `wiki/personalidades/publio-lentulus.md`:37 — ✓ auto-corrigido
  - Afirmação: Aspa em primeira pessoa ('Sou o ex-senador...') inexistente na fonte; é a apresentação do editor.
  - Evidência: Ao leitor, item 1: '...observações de Emmanuel, o ex-senador Públio Lentulus, descendente da orgulhosa gens Cornélia'
  - Ação: `replace-text` — aspa trocada pelo texto literal do 'Ao leitor'
- **[media]** `wiki/personalidades/livia.md`:27 — ✓ auto-corrigido
  - Afirmação: Aspa fabricada ('Trocaremos hoje a toga e a túnica') fundindo falas de Ana e Lívia.
  - Evidência: 2ª p., cap. V: Ana: 'sou vossa escrava'; Lívia: 'troca hoje comigo a toga da senhora pela túnica da serva!'
  - Ação: `replace-text` — substituída pelo diálogo literal com elisões
- **[media]** `wiki/personalidades/poncio-pilatos.md`:23 — ✓ auto-corrigido
  - Afirmação: Página faz de Pilatos 'responsável direto pela calúnia' e situa a sugestão de Fúlvia 'em seu gabinete em Cesareia'; no romance os caluniadores são Fúlvia e Sulpício, Pilatos é o assediador, e a cena é em Jerusalém no dia do Calvário (a 1ª denúncia é no gabinete do próprio Públio).
  - Evidência: 1ª p., cap. IV: 'Públio Lentulus foi procurado, na intimidade do seu gabinete particular, por Fúlvia'; 1ª p., cap. VIII: 'intoxicado pelo veneno das calúnias de Fúlvia e Sulpício'; 1ª p., cap. IX: janela de Fúlvia; Cesareia só no embarque (2ª p., cap. I).
  - Verificação: **confirmed** — Confirmado literalmente no romance via grab.py pelo main-session; corrigido com aval explícito do usuário (fato de enredo, sem peso doutrinário), sem rebaixar a rascunho.
  - Ação: `replace-text` — Reescrever: Pilatos assedia Lívia, o que dá pretexto à calúnia de Fúlvia e Sulpício; remover Cesareia.
- **[media]** `wiki/personalidades/flavia-lentulia.md`:17 — ✓ auto-corrigido
  - Afirmação: Sugere que os 'prejuízos morais' de que Calpúrnia quer afastar Flávia seriam o orgulho de estirpe; no romance são as ideias cristãs de Lívia. Aspa também não literal ('afastar' vs 'afastando').
  - Evidência: 2ª p., cap. II: 'Colaborarei contigo, afastando Flávia desses prejuízos morais, levando-a para a minha companhia [...] quanto a Lívia, tudo já fiz para convencê-la, inutilmente.'
  - Verificação: **confirmed** — Confirmado literalmente no romance via grab.py pelo main-session; corrigido com aval explícito do usuário (fato de enredo, sem peso doutrinário), sem rebaixar a rascunho.
  - Ação: `replace-text` — Deixar claro que Calpúrnia quer afastar Flávia da fé materna; ajustar aspa.
- **[media]** `wiki/obras/ha-dois-mil-anos.md`:41 — ✓ auto-corrigido
  - Afirmação: Martírio de Lívia e João de Cleofas datado em 64 d.C.; no romance ocorre em 58, sob Nero.
  - Evidência: 2ª p., cap. IV: 'Nos primeiros dias do ano 58, os padecimentos da Calpúrnia foram subitamente agravados'; 2ª p., cap. VII: 'Parecia que o ano 58 estava destinado a assinalar os mais penosos incidentes [...] A morte de Calpúrnia e o falecimento inesperado de Lívia'; o cap. V não menciona 64.
  - Verificação: **confirmed** — Confirmado literalmente no romance via grab.py pelo main-session; corrigido com aval explícito do usuário (fato de enredo, sem peso doutrinário), sem rebaixar a rascunho.
  - Ação: `replace-text` — Trocar 64 por 58 na obra e nas páginas de Lívia, João de Cleofas e Ana.
- **[baixa]** `wiki/personalidades/publio-lentulus.md`:22 — ✓ auto-corrigido
  - Afirmação: Sonho das insígnias de cônsul (Sura) atribuído ao capítulo 'Dois amigos'.
  - Evidência: O trecho está em 1ª p., cap. V ('O Messias de Nazaret').
  - Ação: `replace-text` — locus corrigido para 1ª parte, cap. V; grafia da aspa ajustada à fonte
- **[baixa]** `wiki/personalidades/publio-lentulus.md`:39 — ✓ auto-corrigido
  - Afirmação: Aspa omitia 'Algum dia' e não indicava a obra.
  - Evidência: Ao leitor, item 3
  - Ação: `replace-text` — acrescentado 'Algum dia,' e o locus
- **[baixa]** `wiki/personalidades/livia.md`:21 — ✓ auto-corrigido
  - Afirmação: Ordem das palavras trocada na aspa do pedido no plano espiritual; sem locus.
  - Evidência: 2ª p., cap. VI
  - Ação: `replace-text` — aspa literal + locus
- **[baixa]** `wiki/personalidades/livia.md`:25 — ✓ auto-corrigido
  - Afirmação: 'a morrer' em vez de 'morrer'; título do capítulo truncado.
  - Evidência: 2ª p., cap. V
  - Ação: `replace-text` — aspa e locus corrigidos
- **[baixa]** `wiki/personalidades/livia.md`:29 — ✓ auto-corrigido
  - Afirmação: Erros de transcrição e falta de locus.
  - Evidência: 2ª p., cap. VI
  - Ação: `replace-text` — aspa literal + locus
- **[baixa]** `wiki/personalidades/simeao-da-samaria.md`:19 — ✓ auto-corrigido
  - Afirmação: Aspa sobre legítima defesa com duas divergências da fonte.
  - Evidência: 1ª p., cap. X
  - Ação: `replace-text` — aspa literal + locus com a parte
- **[baixa]** `wiki/personalidades/simeao-da-samaria.md`:27 — ✓ auto-corrigido
  - Afirmação: Pontuação da aspa; locus sem a parte.
  - Evidência: 1ª p., cap. X
  - Ação: `replace-text` — pontuação e locus
- **[baixa]** `wiki/personalidades/simeao-da-samaria.md`:29 — ✓ auto-corrigido
  - Afirmação: Aspa modernizada ('coisa') e sem locus.
  - Evidência: 1ª p., cap. X: 'Alguma cousa...'
  - Ação: `replace-text` — 'cousa' + locus
- **[baixa]** `wiki/personalidades/simeao-da-samaria.md`:13 — ✓ auto-corrigido
  - Afirmação: Chama Simeão de 'tio-avô' de Ana; o romance diz tio/sobrinha.
  - Evidência: 1ª p., cap. IX: 'Ana e seu tio'; 1ª p., cap. X: 'na fronte da sobrinha'
  - Verificação: **confirmed** — Confirmado literalmente no romance via grab.py pelo main-session; corrigido com aval explícito do usuário (fato de enredo, sem peso doutrinário), sem rebaixar a rascunho.
  - Ação: `replace-text` — 'Tio e protetor de Ana'
- **[baixa]** `wiki/personalidades/simeao-da-samaria.md`:34 — ✕ descartado (verificação refutou)
  - Afirmação: Afirmação de que Simeão conduz Ana às esferas espirituais na morte em Pompeia seria sem apoio.
  - Evidência: 2ª p., cap. X: 'surgiram Lívia e Ana abraçadas'
  - Verificação: **refuted** — Refutado: 2ª p., cap. X, item 17 — 'sentindo-se ela amparada, espiritualmente, pelo venerável samaritano que a conduziu, imediatamente, às mais elevadas Esferas espirituais'. A página está correta.
- **[baixa]** `wiki/personalidades/joao-de-cleofas.md`:19 — ✓ auto-corrigido
  - Afirmação: Aspa omitia 'santas'; locus sem a parte.
  - Evidência: 2ª p., cap. V
  - Ação: `replace-text` — 'Pelas santas revelações' + locus
- **[baixa]** `wiki/personalidades/joao-de-cleofas.md`:21 — ✓ auto-corrigido
  - Afirmação: Grafia/pontuação da aspa sobre Malcus.
  - Evidência: 2ª p., cap. V
  - Ação: `replace-text` — aspa literal
- **[baixa]** `wiki/personalidades/poncio-pilatos.md`:25 — ✓ auto-corrigido
  - Afirmação: Vírgula a mais na aspa sobre o suicídio de Pilatos.
  - Evidência: 1ª p., cap. X: 'onde se suicidou daí a três anos, ralado de remorsos, de privações e de amarguras'
  - Ação: `replace-text` — 'se suicidou, daí a três anos' → 'se suicidou daí a três anos'
- **[baixa]** `wiki/personalidades/flavia-lentulia.md`:23 — ✓ auto-corrigido
  - Afirmação: Diz que os cosméticos envenenados 'lhe curam a pele'; foram os remédios que venceram o veneno na pele.
  - Evidência: 2ª p., cap. VII: 'Na epiderme, os venenos de Atheia haviam sido anulados e vencidos pelas substâncias medicamentosas aplicadas, mas a luz dos seus olhos fora aniquilada para todo o sempre.'
  - Verificação: **confirmed** — Confirmado literalmente no romance via grab.py pelo main-session; corrigido com aval explícito do usuário (fato de enredo, sem peso doutrinário), sem rebaixar a rascunho.
  - Ação: `replace-text` — Reescrever: os remédios vencem o veneno na pele, mas não salvam a vista.
- **[baixa]** `wiki/sinteses/consolador-em-ha-dois-mil-anos.md`:74 — ✓ auto-corrigido
  - Afirmação: Aspa atribuída a Lívia trazia 'destinada ao meu modo de ser', particípio inexistente na fonte.
  - Evidência: Há Dois Mil Anos…, 2ª parte, cap. VI: 'da alma gêmea da minha, que a sabedoria de Deus, em seus profundos e doces mistérios, destinou ao meu modo de ser, desde a aurora dos tempos!…'
  - Ação: `replace-text` — aspa corrigida para o texto literal ('que a sabedoria de Deus, em seus profundos e doces mistérios, destinou ao meu modo de ser')
- **[baixa]** `wiki/obras/ha-dois-mil-anos.md`:65 — ✓ auto-corrigido
  - Afirmação: Aspa do 'minuto glorioso' omitia o artigo ('utilizar tua liberdade').
  - Evidência: 1ª p., cap. V: 'se conseguires utilizar a tua liberdade para que seja ele...'
  - Ação: `replace-text` — 'utilizar tua liberdade' → 'utilizar a tua liberdade'
- **[baixa]** `wiki/obras/ha-dois-mil-anos.md`:79 — ✓ auto-corrigido
  - Afirmação: Transcrição da aspa de Simeão sobre a legítima defesa.
  - Evidência: 1ª p., cap. X: 'porque está escrito na Lei que “Não Matarás”, sem nenhuma cláusula...'
  - Ação: `replace-text` — "escrito na Lei: 'Não Matarás'," → "escrito na Lei que 'Não Matarás',"
- **[baixa]** `wiki/obras/ha-dois-mil-anos.md`:144 — ✓ auto-corrigido
  - Afirmação: Locus errado: 'ESE cap. XIV (Os fluidos)'; o ESE XIV é 'Honrai a vosso pai e a vossa mãe'; 'Os fluidos' é Gênese XIV, já citada.
  - Evidência: cite.py ESE cap. XIV → 'Honrai a vosso pai e a vossa mãe'; Gênese cap. XIV → 'Os fluidos'
  - Ação: `replace-text` — 'ESE cap. XIV (Os fluidos) e Gênese cap. XIV' → 'Gênese cap. XIV (Os fluidos)'

### Eixo 3 — Padrão editorial (3)

- **[baixa]** `wiki/personalidades/joao-de-cleofas.md`:25 — ✓ auto-corrigido
  - Afirmação: Citação sem locus.
  - Evidência: 2ª p., cap. V
  - Ação: `replace-text` — locus acrescentado
- **[baixa]** `wiki/personalidades/joao-de-cleofas.md`:27 — ✓ auto-corrigido
  - Afirmação: Citação sem locus.
  - Evidência: 2ª p., cap. V
  - Ação: `replace-text` — locus acrescentado
- **[baixa]** `wiki/personalidades/poncio-pilatos.md`:31 — ✓ auto-corrigido
  - Afirmação: Citação do romance sem locus (fala de Lívia após o martírio de Simeão).
  - Evidência: 1ª p., cap. X
  - Ação: `replace-text` — acrescentado '1ª parte, cap. X' à referência

## 4. Mudanças auto-aplicadas

- `wiki/personalidades/publio-lentulus.md`:22 — `replace-text`: locus corrigido para 1ª parte, cap. V; grafia da aspa ajustada à fonte
- `wiki/personalidades/publio-lentulus.md`:24 — `replace-text`: aspa trocada pelo texto literal; locus 1ª parte, cap. I
- `wiki/personalidades/publio-lentulus.md`:37 — `replace-text`: aspa trocada pelo texto literal do 'Ao leitor'
- `wiki/personalidades/publio-lentulus.md`:39 — `replace-text`: acrescentado 'Algum dia,' e o locus
- `wiki/personalidades/livia.md`:21 — `replace-text`: aspa literal + locus
- `wiki/personalidades/livia.md`:25 — `replace-text`: aspa e locus corrigidos
- `wiki/personalidades/livia.md`:27 — `replace-text`: substituída pelo diálogo literal com elisões
- `wiki/personalidades/livia.md`:29 — `replace-text`: aspa literal + locus
- `wiki/personalidades/simeao-da-samaria.md`:19 — `replace-text`: aspa literal + locus com a parte
- `wiki/personalidades/simeao-da-samaria.md`:27 — `replace-text`: pontuação e locus
- `wiki/personalidades/simeao-da-samaria.md`:29 — `replace-text`: 'cousa' + locus
- `wiki/personalidades/simeao-da-samaria.md`:13 — `replace-text`: 'Tio e protetor de Ana'
- `wiki/personalidades/joao-de-cleofas.md`:19 — `replace-text`: 'Pelas santas revelações' + locus
- `wiki/personalidades/joao-de-cleofas.md`:21 — `replace-text`: aspa literal
- `wiki/personalidades/joao-de-cleofas.md`:25 — `replace-text`: locus acrescentado
- `wiki/personalidades/joao-de-cleofas.md`:27 — `replace-text`: locus acrescentado
- `wiki/personalidades/poncio-pilatos.md`:25 — `replace-text`: 'se suicidou, daí a três anos' → 'se suicidou daí a três anos'
- `wiki/personalidades/poncio-pilatos.md`:31 — `replace-text`: acrescentado '1ª parte, cap. X' à referência
- `wiki/personalidades/poncio-pilatos.md`:23 — `replace-text`: Reescrever: Pilatos assedia Lívia, o que dá pretexto à calúnia de Fúlvia e Sulpício; remover Cesareia.
- `wiki/personalidades/flavia-lentulia.md`:17 — `replace-text`: Deixar claro que Calpúrnia quer afastar Flávia da fé materna; ajustar aspa.
- `wiki/personalidades/flavia-lentulia.md`:23 — `replace-text`: Reescrever: os remédios vencem o veneno na pele, mas não salvam a vista.
- `wiki/sinteses/consolador-em-ha-dois-mil-anos.md`:74 — `replace-text`: aspa corrigida para o texto literal ('que a sabedoria de Deus, em seus profundos e doces mistérios, destinou ao meu modo de ser')
- `wiki/obras/ha-dois-mil-anos.md`:65 — `replace-text`: 'utilizar tua liberdade' → 'utilizar a tua liberdade'
- `wiki/obras/ha-dois-mil-anos.md`:79 — `replace-text`: "escrito na Lei: 'Não Matarás'," → "escrito na Lei que 'Não Matarás',"
- `wiki/obras/ha-dois-mil-anos.md`:144 — `replace-text`: 'ESE cap. XIV (Os fluidos) e Gênese cap. XIV' → 'Gênese cap. XIV (Os fluidos)'
- `wiki/obras/ha-dois-mil-anos.md`:41 — `replace-text`: Trocar 64 por 58 na obra e nas páginas de Lívia, João de Cleofas e Ana.

## 5. Diferidos a decisão humana

_Nenhum item diferido._

## 6. Resumo por página

### `wiki/personalidades/publio-lentulus.md`
Fiel ao romance, sem tensão com o Pentateuco; locus trocado e duas aspas parafraseadas corrigidos.

### `wiki/personalidades/livia.md`
Enredo confere; aspas corrigidas ao literal; sem tensão com o Pentateuco.

### `wiki/personalidades/simeao-da-samaria.md`
Sem divergência com o Pentateuco; aspas corrigidas; parentesco com Ana a corrigir.

### `wiki/personalidades/joao-de-cleofas.md`
Enredo confere; aspas e loci ajustados; sem tensão com o Pentateuco.

### `wiki/personalidades/poncio-pilatos.md`
Sem tensão com o Pentateuco; 2 correções de transcrição/locus; erro de enredo sobre autoria e local da calúnia.

### `wiki/personalidades/ana-samaritana.md`
Página fiel: aspas e loci conferem; ESE VII, 2 e X, 11 sustentam a leitura.

### `wiki/personalidades/flavia-lentulia.md`
Leitura doutrinária correta (ESE V, 12); dois erros de enredo (sentido dos 'prejuízos morais' e efeito dos cosméticos).

### `wiki/personalidades/marcus-lentulus.md`
Página fiel: aspas do romance, C&I VII, 13 e citação de 50 anos depois conferem.

### `wiki/personalidades/flaminio-severus.md`
Página fiel: aspas e loci do romance conferem; LE q. 489 e 495 confirmados; fatos do enredo corretos.

### `wiki/personalidades/calpurnia.md`
Página fiel: aspas conferem (2ª p., I, II, IV); ESE XVII, 4 (Kardec) e X, 15 (Paulo) com autoria correta.

### `wiki/personalidades/agripa-severus.md`
Página fiel: falas e fatos conferem (2ª p., II, IV, VII, X); ESE XII, 9 atribuído a Júlio Olivier.

### `wiki/personalidades/plinio-severus.md`
Página fiel: aspas e fatos conferem; ESE IX, 6 (Lázaro) e C&I VII, 17 literais.

### `wiki/personalidades/fulvia-procula.md`
Página fiel: aspas e capítulos do romance conferem; ESE IX, 6 corretamente atribuído a Lázaro; C&I VII, 16 sustenta a tríade.

### `wiki/personalidades/aurelia.md`
Página fiel: advertência de Araxes, Atheia, Sérgio Acerronius e Antium conferem (2ª p., III e VII); LE q. 908 e 554 literais; almas-gêmeas já registrada.

### `wiki/personalidades/emiliano-lucius.md`
Página fiel: fatos conferem (2ª p., II, IV, X); LE q. 944 e 957 literais; não deduz regra sobre a sorte do suicida.

### `wiki/personalidades/sulpicio-tarquinius.md`
Página fiel: fatos e aspas conferem (1ª p., II, III, VI, X; 2ª p., IV); Carta de 50 anos depois nomeia Sulpício; C&I VII, 13 literal.

### `wiki/personalidades/andre-de-gioras.md`
Página fiel: ESE X, 8 (Kardec) e XII, 9 (Júlio Olivier) conferem com autoria correta; aspas e loci do romance confirmados.

### `wiki/personalidades/saul-de-gioras.md`
Página fiel: ESE XII, 9 e LE q. 553 literais; aspas do romance e da Carta de 50 anos depois conferem; fatos do enredo corretos.

### `wiki/personalidades/pompilio-crasso.md`
Sem afirmação doutrinária contra o Pentateuco; identidade Pompílio = Helvídio Lucius e aspas da Carta ao leitor conferem.

### `wiki/personalidades/araxes.md`
Página fiel: LE q. 552-554 e 298-299 literais; almas-gêmeas já registrada; aspas da 2ª p., III, IV e VII conferem.

### `wiki/sinteses/chamado-do-cristo-em-ha-dois-mil-anos.md`
Sem achados: 38 aspas/paráfrases do Pentateuco conferidas (autorias de Lacordaire, Constantino e São Luís corretas); citações do romance e de Emmanuel (Fonte Viva 5, Vinha de Luz 100, Pão Nosso 166, A Caminho da Luz 7-8, 50 anos depois) conferem; ensino complementar de Emmanuel sinalizado como tal.

### `wiki/sinteses/consolador-em-ha-dois-mil-anos.md`
Síntese fiel; citações ao Pentateuco (ESE VI 1/3/4, III 1; LE q. 934-936, 298-299) conferem; divergência das almas-gêmeas já registrada; só uma transcrição corrigida.

### `wiki/obras/ha-dois-mil-anos.md`
Fiel ao Pentateuco; almas-gêmeas registrada; 2 aspas e 1 locus do ESE corrigidos; data do martírio (64→58) a corrigir; citação direta ~300 palavras, dentro do limite FEB.
