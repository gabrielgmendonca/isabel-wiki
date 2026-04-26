# Log

Histórico cronológico da wiki. Cada entrada começa com `## [YYYY-MM-DD] <tipo> | <título>`, onde `<tipo>` ∈ {`setup`, `ingest`, `query`, `lint`, `refactor`}.

Para ver as últimas N entradas: `grep "^## \[" log.md | tail -N`.

## [2026-04-26] refactor | Lint: novo check skills_consistency

Adiciona check determinístico que valida coerência entre `CLAUDE.md`, `.claude/skills/*/SKILL.md` e `.claude/rules/*.md`. Detecta três classes de drift: (a) referência a `wiki/<dir>/` inexistente, (b) skill em `.claude/skills/` sem menção em `CLAUDE.md`, (c) caminho `uv run python <path>` apontando para script ausente. Pegou os 4 itens-bug do roadmap §0.1 na primeira execução: `wiki/parabolas/` fantasma referenciado em `slides/SKILL.md:36` e `convencoes-slides.md:19`, e `/slides`/`/stats` não citados em `CLAUDE.md`. Prevenção contra reincidência conforme CLAUDE.md e skills evoluem.

## [2026-04-26] lint | 5 achados

Lint zerado em todos os checks de erro/aviso estruturais. Único alerta: 5 páginas com `status: rascunho` há 19 dias (`a-caminho-da-luz`, `emmanuel`, `mansao-do-caminho`, `meimei`, `victor-hugo`) — todas do mesmo cluster ingerido em 2026-04-07, candidatas a revisão de status para `consolidada` ou aprofundamento.

## [2026-04-26] refactor | Adensamento do grafo: trilhas órfãs zeradas, cross-links conceito↔questão e personalidade↔obra

Análise da wiki via `/stats` (281 nós, 2.451 arestas, 2 órfãs) seguida de adições auditadas em três frentes, cobrindo lacunas de relacionamento sem criar páginas novas. Resultado: **órfãs 2→0**, **arestas 2.451→2.468 (+17)**, lint zerado.

**Categoria 1 — Backlinks p/ trilhas órfãs**: `wiki/trilhas/primeiros-passos` e `wiki/trilhas/palestras` eram órfãs no grafo formal (excluídas do `index.md` e `catalogo.md` por serem meta). Adicionados 3 backlinks-âncora por trilha:
- → `primeiros-passos`: em `conceitos/deus`, `conceitos/reencarnacao`, `conceitos/prece`.
- → `palestras`: em `sinteses/parabolas-de-jesus`, `obras/evangelho-segundo-o-espiritismo`, `aprofundamentos/expiacao-e-arrependimento`.

**Categoria 2 — Conceito/Aprof. ↔ Questão**: as 9 questões já listavam seus conceitos-mãe; o lado reverso tinha 7 lacunas. Adicionados links:
- `sinteses/hierarquia-de-autoridade` ← `jesus-tipo-mais-perfeito`
- `conceitos/livre-arbitrio` ← `por-que-a-acao-dos-espiritos-e-oculta` + `pactos-com-satanas-como-alegoria`
- `conceitos/obsessao` ← `pactos-com-satanas-como-alegoria`
- `conceitos/lei-de-reproducao` ← `paternidade-como-missao`
- `conceitos/responsabilidade` ← `paternidade-como-missao`
- `conceitos/alma` ← `alma-dos-animais`
- `conceitos/lei-de-justica-amor-e-caridade` ← `fora-da-caridade-nao-ha-salvacao`
- `aprofundamentos/expiacao-e-arrependimento` ← `arrependimento-expiacao-e-reparacao` (subcaso aprof.↔questão)

**Categoria 3 — Personalidade ↔ Obra**: auditoria via grep mostrou que o cross-link bidirecional já estava sólido para autores complementares (Léon Denis, Carlos Mendonça, Divaldo, Hammed/Francisco, Emmanuel, André Luiz, Paulo, Pedro, Estêvão, Zaqueu, Melquisedeque, Erasto, Santo Agostinho, São Luís, Espíritos Reveladores). Única lacuna corrigida: `personalidades/chico-xavier` ganhou `[[wiki/obras/entre-a-terra-e-o-ceu]]` em "Obras associadas".

**Total: 14 arquivos editados** (com `atualizado_em` para 2026-04-26). Conceitos selecionados pelo princípio de "âncora mínima" — preferi 3 backlinks-âncora por trilha em conceitos centrais a poluir todas as 14 páginas listadas pela trilha.

## [2026-04-21] lint | 0 achados

Wiki limpa em todos os 13 checks determinísticos (284 páginas, incluindo a ingestão de Hebreus e as duas divergências recém-criadas). Nenhum broken_link, frontmatter inválido, órfão, citação fora de padrão ou lacuna no Pentateuco. Nada a corrigir.

## [2026-04-21] ingest | Epístola aos Hebreus (ACF) + 2 divergências + Melquisedeque

Ingestão da **Epístola aos Hebreus** (ACF, caps. 1–13) como quarta entrada paulina no pipeline de NT (após Atos, 1 Coríntios e Romanos). Hebreus é homilia erudita a cristãos de origem judaica, com cinco núcleos de valor espírita:

1. **Anjos como "espíritos ministradores"** (Hb 1:14; 13:2) — base NT direta para a leitura kardequiana de anjos = Espíritos (LE q. 128; C&I 1ª parte cap. VIII).
2. **Nova aliança — lei escrita no coração** (Hb 8:10, citando Jr 31:33) — gêmea NT do axioma de LE q. 621 e de Rm 2:14–15.
3. **Jesus consagrado pelas aflições; aprendeu pela obediência** (Hb 2:10, 17–18; 4:15; 5:7–9) — base paulina de LE q. 625 e ESE cap. XVII: Cristo modelo real porque viveu como homem.
4. **"Pai dos espíritos" e correção pedagógica** (Hb 12:5–11) — paternidade divina sobre os seres espirituais; sofrimento como pedagogia do Pai, não castigo; corrigibilidade como signo de filiação. Paralelo direto com ESE cap. V.
5. **Fé como "firme fundamento"** (Hb 11:1, 6) + encarnação como peregrinação (Hb 11:13, 16; 13:14) — definição escritural matriz da fé e formulação bíblica do mundo como lugar de passagem.

**Ressalva sobre autoria** documentada com destaque: Hebreus não nomeia autor e sua atribuição a Paulo é contestada desde Orígenes ("quem de fato escreveu a carta, só Deus sabe"). Mantida no corpus paulino ampliado (tradição das casas espíritas brasileiras) com "Nota sobre a autoria" no cabeçalho da página da obra e nota correspondente em `paulo-de-tarso.md`, apontando para o verbete da Wikipédia em português e para o comentário crítico de Luke Timothy Johnson.

Duas divergências registradas (páginas próprias):

- **Hb 9:27** ("aos homens está ordenado morrerem uma vez, vindo depois disso o juízo") — passagem mais mobilizada pelas tradições cristãs contra a reencarnação. Leitura espírita: argumento tipológico-sacerdotal da carta (paralelo entre unicidade do sacrifício de Cristo e unicidade da morte em cada existência), não afirmação cosmológica. Compatível com pluralidade das existências.
- **Hb 6:4–6 e 10:26–27** (impossibilidade de renovação após recaída) — lida como hipérbole parenética pastoral dirigida a comunidade em perigo de apostasia, não doutrina sobre irrecuperabilidade metafísica do Espírito (mitigada pelo próprio 6:9–12 e 10:39). Divergência real apenas com a leitura literalista-rigorista da tradição.

Nova página de personalidade: **Melquisedeque** (Gn 14:18–20; Sl 110:4; Hb 5–7), figura enigmática que Hebreus recupera para fundar o argumento do sacerdócio de Cristo superior ao levítico. Tratada como Espírito adiantado encarnado antes da codificação mosaica, com recusa explícita de leituras teosófico-ocultistas ("ordem de Melquisedeque" como linhagem iniciática).

Atualizações em `paulo-de-tarso.md` (nota sobre autoria + Hebreus nas páginas relacionadas e divergências), `anjos.md` (Hb 1:14; 13:2 como base NT direta), `fe.md` (Hb 11:1, 6 como definição escritural matriz), `lei-natural.md` (Hb 8:10 nova aliança), `provas-e-expiacoes.md` (Hb 12:5–11 correção do "Pai dos espíritos"), `reencarnacao.md` (link para divergência Hb 9:27). Entradas adicionadas no `wiki/sinteses/catalogo.md` (obras NT, personalidades, divergências).

## [2026-04-20] ingest | Epístola aos Romanos (ACF) + 2 divergências + ampliação da divergência sobre sexo

Ingestão da **Epístola aos Romanos** (ACF, caps. 1–16) como terceira epístola paulina no pipeline de NT (após Atos e 1 Coríntios). Romanos é a paulina mais sistemática — tratado doutrinário com quatro núcleos de valor espírita:

1. **Lei moral inscrita no coração** (Rm 2:14–15) — formulação paulina direta do axioma kardequiano da lei na consciência (LE q. 621).
2. **Luta moral interior** (Rm 7:15–25) — "o mal que não quero, esse faço" — base paulina do combate moral do homem de bem (ESE cap. XVII; LE q. 908).
3. **Amor como cumprimento da lei** (Rm 13:8–10) — gêmea de 1 Co 13 e de Mt 22:37–40 (Lei de Justiça, Amor e Caridade).
4. **Aflições com sentido** (Rm 5:3–5; 8:18, 28) — armadura escritural de ESE cap. V (bem-aventurados os aflitos).

**Criado:**

1. [[wiki/obras/epistola-aos-romanos]] — página da obra (nível 3), 4 blocos estruturais (pecado universal/justificação caps. 1–4; vida segundo o Espírito caps. 5–8; Israel e plano divino caps. 9–11; ética da vida nova caps. 12–16), 10 temas centrais, tabela de cross-refs com Pentateuco, personalidades (Paulo, Tércio, Febe, Priscila/Áquila, Andrônico/Júnias, Rufo, Timóteo, Gaio, Erasto).
2. [[wiki/divergencias/pecado-original-em-romanos-5]] — Rm 5:12–19 ("por um homem entrou o pecado") vs. Kardec: lei na consciência (LE q. 621), Adão não é o primeiro homem (Gênese cap. XI, itens 38–44; [[wiki/conceitos/raca-adamica]]), sofrimentos próprios do progresso (ESE cap. V). Status: aberta.
3. [[wiki/divergencias/predestinacao-em-romanos-8-9]] — Rm 8:29–30 ("predestinou / chamou / justificou") + 9:11–23 (Jacó/Esaú; oleiro e barro) vs. livre-arbítrio (LE q. 843). Análise da leitura histórico-retórica (endurecimento parcial de Israel) + distinção presciência vs. decreto. Status: aberta.

**Atualizado:**

- [[wiki/divergencias/mudanca-de-sexo-reencarnacao]] — **ampliada** com seção "Extensão: Paulo e a 'natureza' em Romanos 1" articulando Rm 1:26–27 ("paixões infames", "contrário à natureza") e o cap. 13 de *O Problema do Ser e do Destino* de Léon Denis ("anormais / viragos") como duas variações do mesmo literalismo da "natureza" sexual — dissolvidas pela mesma tríade kardequiana LE q. 200–202 ("os sexos dependem do organismo"; alternância pedagógica; "isso pouco lhe importa"). Decisão de incorporar Rm 1 aqui em vez de criar divergência autônoma: compartilham estrutura argumentativa, não exigem página nova. Frontmatter atualizado com `NT` em fontes e `paulo, romanos` em tags.
- [[wiki/conceitos/lei-natural]] — nova seção "Base escritural: Romanos 2" com Rm 2:14–15 articulando à formulação de LE q. 621.
- [[wiki/conceitos/livre-arbitrio]] — nova seção "Formulação paulina: cada um dará conta de si mesmo" (Rm 14:12) + nota sobre leitura da "predestinação" paulina e remissão à divergência.
- [[wiki/conceitos/origem-do-mal]] — nova seção "Divergências" com análise da leitura paulina do pecado original e remissão.
- [[wiki/conceitos/lei-de-justica-amor-e-caridade]] — nova seção "Formulação paulina: o cumprimento da lei é o amor" (Rm 13:8–10 + Rm 12:9–21).
- [[wiki/conceitos/bem-aventuranca-dos-aflitos]] — subseção "Ressonância em Paulo: Romanos 5 e 8" (Rm 5:3–5 e 8:18).
- [[wiki/conceitos/responsabilidade]] — nova seção "Formulação paulina: Romanos 2 e 14" (Rm 2:6, 11 e 14:12).
- [[wiki/personalidades/paulo-de-tarso]] — expandido com citações paulinas de Rm (2:14–15, 7:19, 8:18, 8:28, 13:10, 14:12), nova obra em "Páginas relacionadas", três divergências registradas (pecado-original, predestinação, mudança-de-sexo ampliada).

**Não mexido** (conforme prática das últimas ingestões): `index.md`. Contagens de cobertura atualizadas depois pelo `update_status.py`.

**Motivação:** continuar cobertura NT como escrito apostólico (nível 3) após Evangelhos, Atos e 1 Coríntios. Romanos foi priorizada por densidade doutrinária e por três passagens-chave que o estudo espírita aproveita na íntegra: Rm 2:14–15 (lei na consciência), Rm 13:8–10 (amor cumpre a lei), Rm 8:18 (aflições e glória). A ingestão também precipitou a ampliação da divergência existente sobre mudança de sexo — Rm 1 e Denis OPS cap. 13 operam com o mesmo literalismo da "natureza", dissolvido pela mesma passagem de Kardec (LE q. 200–202).

---

## [2026-04-20] lint | 50 achados (após correção do script)

Lint pós-ingest de 1 Coríntios. Duas correções no script de lint eliminaram **85 falsos positivos**:

1. **`find_wikilinks` em `_lib/wiki_utils.py`** — a regex `\[\[([^\]|#]+)` capturava trailing `\` antes do pipe escapado em tabelas Markdown (`[[slug\|label]]`), produzindo alvos inexistentes terminados em `\`. Fix: `.rstrip("\\")` no target capturado. Resultado: `broken_links` 37 → 0; `missing_concept_pages` 37 → 0.

2. **`check_divergencias_aberta` em `lint_wiki.py`** — o check listava TODAS as divergências com `status: aberta`, inclusive as de análise completa (que são aberta por design — o conflito teológico permanece registrado, não porque falte trabalho). Fix: só flagga quando `body_lines < 20` (stubs/incompletas). Resultado: `divergencias_aberta` 7 → 0.

Total final: **50 achados** (era 135). Residuais todos pré-existentes ou esperados:
- `index_missing` (33): 4 novas de 1 Co (instrução do usuário: não tocar `index.md`) + 29 parábolas + 8 bem-aventuranças.
- `tag_taxonomy` (13): `wiki/trilhas/*` e `dores-da-alma.md` (pré-existentes).
- `fontes_missing` (1), `citation_format` (1): ambos em `wiki/sinteses/catalogo.md` (pré-existente).
- `status_projeto` (2): contagens no `index.md` desatualizadas (cosmético).

---

---

## [2026-04-20] ingest | Primeira Epístola aos Coríntios (ACF) + discernimento dos espíritos + 2 divergências

Ingestão de **1 Coríntios** (ACF, caps. 1–16) como segunda epístola paulina no pipeline de NT (após Atos). Carta de maior densidade doutrinária para o estudo espírita entre as paulinas: cap. 13 (caridade) é base escritural de ESE cap. XV; cap. 15:44 (corpo espiritual) é formulação neotestamentária do perispírito aproveitada por Kardec em Gênese cap. XIV; caps. 12–14 constituem o maior corpus NT sobre mediunidade, incluindo "discernimento dos espíritos" (12:10), "os espíritos dos profetas estão sujeitos aos profetas" (14:32) e o critério "Deus não é Deus de confusão, senão de paz" (14:33).

**Criado:**

1. [[wiki/obras/primeira-epistola-aos-corintios]] — página da obra (nível 3), estrutura por capítulo, 10 temas centrais, referências cruzadas com Pentateuco, personalidades (Paulo, Sóstenes, Apolo, Cefas/Pedro, Timóteo, Áquila/Priscila, Estéfanas, Cloé, Crispo, Gaio, Barnabé, Fortunato, Acaico).
2. [[wiki/divergencias/celibato-como-ideal-paulino]] — 1 Co 7 (celibato como ideal superior) vs. LE q. 695–701, esp. q. 698 ("os que [vivem por celibato] por egoísmo desagradam a Deus e enganam o mundo"). Status: aberta.
3. [[wiki/divergencias/silencio-das-mulheres-em-corintios]] — 1 Co 11:3–16 (véu e "cabeça") + 14:34–35 ("mulheres caladas nas igrejas") vs. LE q. 817–822 (Lei de Igualdade, esp. q. 822). Inclui análise crítico-textual (possível interpolação de 14:34–35) e contraste interno com At 2:17 e Gl 3:28. Status: aberta.
4. [[wiki/conceitos/discernimento-dos-espiritos]] — nova página-conceito ancorada em 1 Co 12:10 + 14:29, 32–33 + 1 Jo 4:1 + LM 2ª parte cap. XXIV (a pedido do usuário, como página própria linkada de [[wiki/conceitos/mediunidade]], não como seção inline).

**Atualizado:**

- [[wiki/conceitos/caridade]] — adicionada nota filológica (ACF "amor" = Kardec "caridade" = *agape*) e hierarquia paulina fé/esperança/amor (1 Co 13:13).
- [[wiki/conceitos/perispirito]] — nova seção "Base escritural: 1 Coríntios 15" com as passagens 15:42–44, 15:50, 15:40–41, 15:48 articuladas à teoria kardequiana.
- [[wiki/conceitos/mediunidade]] — nova seção "Mediunidade em 1 Coríntios: os dons e a ordenação" com mapeamento dos dons paulinos ao quadro de LM caps. XVI–XVII e extração da tríade controle + paz + julgamento coletivo como síntese paulina da boa prática mediúnica.
- [[wiki/personalidades/paulo-de-tarso]] — página-relacionadas expandida com a nova obra, o conceito de discernimento e as duas divergências.
- `ROADMAP.md` (editado antes do ingest) — adicionada priorização dos NT restantes (1-coríntios → romanos → tiago → 1-joão → 1-pedro → hebreus → demais → apocalipse).

**Não mexido** (conforme instrução do usuário): `index.md`. Contagens de cobertura ficarão desatualizadas até próxima regeração.

**Motivação:** continuar a cobertura do NT como escrito apostólico (nível 3) após Evangelhos + Atos. 1 Coríntios foi priorizada por ser a paulina mais citada por Kardec e por sustentar três pilares da doutrina espírita no NT: caridade, perispírito e mediunidade ordenada. A ingestão adiciona também nova ferramenta conceitual — [[wiki/conceitos/discernimento-dos-espiritos]] — que será reaproveitada quando ingerirmos 1 João (4:1 é a outra metade desse conceito).

---

## [2026-04-20] refactor | Páginas individuais das oito bem-aventuranças

A pedido do usuário ("já temos um artigo para cada Bem-aventurança?"), foi constatado que a wiki tinha apenas uma página única [[wiki/conceitos/bem-aventurancas]] cobrindo cinco das oito bem-aventuranças de Mt 5:3–10 em seções inline, sem páginas-conceito dedicadas. Criadas agora as oito páginas individuais, uma por bem-aventurança, seguindo o mesmo padrão das parábolas de Jesus (página própria por parábola + síntese-índice):

1. [[wiki/conceitos/bem-aventuranca-dos-pobres-de-espirito]] (Mt 5:3 / ESE cap. VII) — humildade, mistérios ocultos aos doutos, aquele que se eleva será rebaixado.
2. [[wiki/conceitos/bem-aventuranca-dos-aflitos]] (Mt 5:4 / ESE cap. V) — justiça das aflições, causas atuais e anteriores, sentido positivo do sofrimento, contrapartida de Lucas ("ai de vós, ricos!").
3. [[wiki/conceitos/bem-aventuranca-dos-brandos]] (Mt 5:5 / ESE cap. IX) — brandura como lei, "possuirão a Terra" = Terra regenerada, afabilidade verdadeira vs. verniz, cólera como sintoma de orgulho.
4. [[wiki/conceitos/bem-aventuranca-dos-famintos-de-justica]] (Mt 5:6 / ESE cap. V) — saciedade só na vida futura e na Terra regenerada, justiça evangélica vs. retributiva.
5. [[wiki/conceitos/bem-aventuranca-dos-misericordiosos]] (Mt 5:7 / ESE cap. X) — perdão setenta vezes sete, duas maneiras de perdoar (dos lábios/do coração), reconciliação antes da morte como profilaxia de obsessão.
6. [[wiki/conceitos/bem-aventuranca-dos-puros-de-coracao]] (Mt 5:8 / ESE cap. VIII) — pureza de intenção não ritual, três gradações do pensamento, criança como emblema da pureza, pureza como pré-requisito mediúnico.
7. [[wiki/conceitos/bem-aventuranca-dos-pacificadores]] (Mt 5:9 / ESE cap. IX) — "serão chamados filhos de Deus", pacificação interior precede exterior, pacificadores vs. apaziguadores falsos.
8. [[wiki/conceitos/bem-aventuranca-dos-perseguidos]] (Mt 5:10–12 / ESE caps. V, XII, XXIV, XXVIII) — perseguição como "batismo de toda ideia nova", resposta evangélica (amai os inimigos, orai pelos que vos persigam), Kardec aplica aos próprios espíritas na Oração dos Espíritas.

**Refatoração da página-índice** ([[wiki/conceitos/bem-aventurancas]]): convertida de conceito com 5 seções inline para índice/overview das 8 páginas, com tabela de correspondência (Mt × ESE × virtude-eixo), reagrupamento em 5 blocos temáticos conforme Kardec, progressão lógica das 8 máximas e enquadramento pela síntese de Kardec no ESE cap. XVII, item 3 ("Toda a moral de Jesus se resume na caridade e na humildade").

**Index.md:** item único substituído por item expandido com 8 sublinks inline para as páginas dedicadas. Segue o mesmo padrão usado em "Parábolas de Jesus" (hub curto + síntese temática), mantendo navegabilidade.

**Motivação:** aplica o princípio de crescimento do CLAUDE.md §1 — transformar as bem-aventuranças de bloco textual único em rede de páginas citáveis. Cada bem-aventurança, por ser ela mesma tema de palestra e de capítulo ESE, merecia página autônoma. Buscas qmd por "misericórdia", "humildade", "pureza de coração" agora retornam a página específica, não apenas a síntese geral. Material pronto para ciclos de oito palestras em casas espíritas (uma por bem-aventurança).

---

## [2026-04-19] refactor | Síntese-índice das parábolas de Jesus

Criada página [[wiki/sinteses/parabolas-de-jesus]] consolidando as 29 parábolas de Jesus já cobertas em `wiki/conceitos/parabola-*` num índice temático único. A síntese organiza o material em 10 agrupamentos temáticos (misericórdia/arrependimento, justiça na vida futura, uso dos bens, prece/humildade, parábolas do Reino, vigilância, responsabilidade agravada, caridade, testemunho, parábolas joaninas), traz tabela completa com referências cruzadas evangelho × capítulo ESE × tema, distribuição por evangelho (Mt 18 · Mc 5 · Lc 11 · Jo 3) com marcação das exclusivas (1 de Mc, 8 de Lc, 3 de Jo) e fecha com três lições transversais (pluralidade das existências como chave, caridade efetiva, progresso como lei natural).

**Enxugamento do `index.md`:** a seção `### Parábolas de Jesus (ESE)` foi reduzida de 29 entradas (linhas 277–306) para um único item apontando para a nova síntese. A lista completa agora vive em um só lugar, o que torna o índice mais navegável e cria uma porta de entrada temática para quem busca "parábolas de X" sem ter que ler o index sequencialmente. Nova síntese também listada em `## Sínteses`.

**Motivação:** aplica o princípio de crescimento do CLAUDE.md — transformar conhecimento disperso (30 páginas + lista sequencial no index) em página citável que alimenta buscas futuras. A busca qmd por "parábolas" antes retornava páginas individuais ou a hierarquia de autoridade; agora retorna o hub dedicado.

---

## [2026-04-19] ingest | *As Dores da Alma* (Hammed/Francisco do Espírito Santo Neto) + novo tier nível 4

Ingestão da obra *As Dores da Alma* (Hammed/Francisco do Espírito Santo Neto, 1998, 8ª ed. ago/2000, Editora Boa Nova), comentário psicológico ao LE que reinterpreta os "sete pecados capitais" da moralidade medieval como **dores da alma** — fases naturais da evolução espiritual. A obra reúne 47 comentários agrupados em 21 temas (crueldade, orgulho, irresponsabilidade, crítica, ilusão, medo, preocupação, vício, solidão, culpa, mágoa, egoísmo, baixa estima, rigidez, ansiedade, perda, insegurança, repressão, depressão, dependência, inveja), cada um ancorado em questões específicas do LE.

**Novo tier na hierarquia de autoridade** (`CLAUDE.md` §2): introduzido **nível 4 — Complementares secundários** para autores/médiuns alinhados à codificação mas sem o peso doutrinário dos consagrados de nível 3 (Léon Denis, Chico Xavier, Divaldo Franco, Emmanuel, André Luiz, Bezerra de Menezes, Cairbar Schutel, Joanna de Ângelis). Hammed/Francisco Neto é o primeiro caso registrado nesse tier. A regra de ouro passa a mencionar "nível 2/3/4" ao falar de conflito com o Pentateuco. Convenção preservada: classificação de obras nível 3 existentes (Léon Denis, Emmanuel, Chico Xavier, Divaldo Franco, Carlos Mendonça) não foi alterada — qualquer reclassificação futura é escopo separado.

**Artefatos criados:**
1. `wiki/obras/as-dores-da-alma.md` — página da obra com 21 temas × 47 comentários tabulados, resumo por eixos, vocabulário/método (registro dos usos pontuais de "carmas" e "chakras" sem abrir divergência), conceitos e personalidades citadas.
2. `wiki/personalidades/francisco-do-espirito-santo-neto.md` — médium psicógrafo (Catanduva-SP).
3. `wiki/personalidades/hammed.md` — Espírito autor; equipe espiritual Port-Royal/jansenista (Pascal, Pavillon, Catherine de Vertus, Walon de Beaupuis, Arnauld, Nicole) registrada sem criar personalidades individuais.
4. `wiki/conceitos/dores-da-alma.md` — conceito-síntese ancorado em LE q. 754 ("senso moral em estado embrionário"), q. 636 (bem e mal relativos) e q. 903 (estudar defeitos alheios).

**Atualizações em conceitos existentes** (seção "Em Hammed — *As Dores da Alma*"):
- `wiki/conceitos/orgulho.md` (LE q. 558, q. 559 — orgulho como controle alheio)
- `wiki/conceitos/egoismo.md` (LE q. 882, q. 917 — vaidade e mesquinhez como filhos do egoísmo)
- `wiki/conceitos/responsabilidade.md` (LE q. 851, q. 860 — fatalidade, limites internos)
- `wiki/conceitos/depressao.md` (LE q. 725, q. 974, q. 1000 — complementa Divaldo Franco)
- `wiki/conceitos/materialismo.md` (LE q. 8, q. 115 — base psicológica na baixa estima)

**Divergências:** nenhuma formalizada. O livro é rigorosamente ancorado no LE; dois deslizes de vocabulário ("carmas", "chakras") registrados na página da obra em "Vocabulário e método".

**index.md:** nova subseção `### Obras complementares secundárias (nível 4)` com `#### Hammed / Francisco do Espírito Santo Neto`; 2 personalidades adicionadas; conceito "dores-da-alma" listado em "Virtudes e vícios".

---

## [2026-04-19] ingest | Três questões-chave fundacionais (LE q. 1, LE q. 625, ESE cap. XV item 5)

Continuação do item §3 do ROADMAP ("Extrair questões-chave do Pentateuco"). Criadas 3 páginas em `wiki/questoes/` cobrindo as questões mais iconicamente citáveis e fundacionais do Pentateuco — bases das quais derivam, respectivamente, a teologia (Deus), a hierarquia de autoridade (Jesus) e a moral (caridade):

1. `o-que-e-deus.md` — LE, q. 1 ("Deus é a inteligência suprema, causa primária de todas as coisas"). Desdobra os dois atributos mínimos (inteligência × causa primária), a ligação com o argumento cosmológico da q. 4 e os sete atributos da q. 13, e explica por que a concisão proposital é pedagógica.
2. `jesus-tipo-mais-perfeito.md` — LE, q. 625 ("Jesus"). Articula a resposta monossilábica com o contexto das q. 621-627 (revelação da lei divina), delimita o que a questão afirma (modelo moral supremo) × o que não afirma (consubstancialidade), cruza com *Obras Póstumas* e mostra por que esta questão ancora a hierarquia de autoridade da wiki.
3. `fora-da-caridade-nao-ha-salvacao.md` — ESE, cap. XV, item 5. A máxima como síntese absoluta da moral cristã no Espiritismo, contrastada com "fora da Igreja" (item 8) e "fora da verdade" (item 9), complementada pela instrução do Espírito Paulo (item 10) e prolongada na *Viagem Espírita em 1862* ("fora da caridade não há verdadeiros espíritas").

Impacto na cobertura: o bloco 1–100 do LE (antes sem questoes dedicadas) ganha sua questão mais fundacional; a q. 625 cobre o topo da Parte 3 (revelações); e o ESE cap. XV passa a ter verbete-âncora para sua máxima-chave. Total de páginas em `questoes/` sobe de 6 para 9.

---

## [2026-04-19] lint | 5 achados

Wiki limpa: 0 erros, 0 avisos. Os 3 órfãos da rodada anterior foram resolvidos pela adição de links de retorno em `conceitos/deus.md`, `personalidades/jesus.md` e `conceitos/caridade.md`. Os 5 achados restantes são `info` — as mesmas divergências `status: aberta` já flaggadas antes, nenhuma possivelmente incompleta.

---

## [2026-04-19] lint | 8 achados

Wiki limpa: 0 erros. 3 avisos (`orphan_pages`) nas 3 novas questoes criadas na mesma data (`o-que-e-deus`, `jesus-tipo-mais-perfeito`, `fora-da-caridade-nao-ha-salvacao`) — esperado para questoes recém-criadas, corrigível adicionando links de retorno de `conceitos/deus.md`, `personalidades/jesus.md` e `conceitos/caridade.md`. 5 infos são as divergências `status: aberta` já flaggadas no lint anterior — nenhuma marcada como possivelmente incompleta. 254 páginas no total (119 conceitos, 92 personalidades, 24 obras, 9 questões, 6 divergências, 3 sínteses, 1 aprofundamento).

---

## [2026-04-19] lint | 5 achados

Wiki limpa: 0 erros, 0 avisos. Os 5 achados são de nível `info`, todos divergências com `status: aberta` (mudança de sexo na reencarnação, sinais de Marcos 16, morte de Ananias e Safira, condenação dos incrédulos em Marcos 16, fogo eterno em Mateus 25) — nenhuma marcada como possivelmente incompleta. 251 páginas no total (119 conceitos, 92 personalidades, 24 obras, 6 questões, 6 divergências, 3 sínteses, 1 aprofundamento).

## [2026-04-19] ingest | Expansão das 4 Leis Morais em stub (Adoração, Trabalho, Reprodução, Sociedade)

Ataque ao item §3 do ROADMAP ("Completar páginas das 10 Leis Morais"). As quatro leis que restavam como stubs (<105 palavras) foram reescritas a partir do raw do LE e do ESE:

1. `lei-de-adoracao.md` (88 → ~650 palavras) — cobre LE q. 649–673 integralmente: sentimento inato, adoração interior/exterior, vida contemplativa, prece (caráter, efeito, por outrem, pelos mortos, aos Espíritos), politeísmo, sacrifícios. Cruzamento com ESE cap. XXVII e XXVIII.
2. `lei-do-trabalho.md` (stub → ~580 palavras) — cobre LE q. 674–685: trabalho espiritual, expiação + progresso, homem × animais, mundos aperfeiçoados, dispensa do rico, trabalho entre gerações, repouso, abuso de autoridade, velhice. Cruzamento com ESE cap. XX e XXV.
3. `lei-de-reproducao.md` (stub → ~580 palavras) — cobre LE q. 686–701: equilíbrio populacional, sucessão das raças e reencarnação, Ciência e aperfeiçoamento, obstáculos artificiais × regulação, casamento como progresso, indissolubilidade, celibato (egoísmo × sacrifício), poligamia. Cruzamento com ESE cap. XXII.
4. `lei-de-sociedade.md` (stub → ~510 palavras) — cobre LE q. 766–775: necessidade da vida social, vida reclusa (duplo egoísmo × reclusão produtiva), voto de silêncio, laços de família. Cruzamento com ESE cap. XI, XIV, XV.

Cada página agora segue a estrutura canônica (Definição · Ensino · Desdobramentos · Aplicação prática · Páginas relacionadas · Fontes) das 6 leis já completas. Impacto: a tag-namespace `lei/` passa a ter cobertura doutrinária simétrica nas 10 leis, e o bloco 601–700 do LE ganha ~8 questões únicas citadas.

---

## [2026-04-19] ingest | Cinco questões-chave do LE (bloco 501–600)

Ataque ao item §3 do ROADMAP ("Extrair questões-chave do Pentateuco") e à sugestão automática do `stats_wiki.py` que apontava 4 blocos de 100 questões do LE com <20% de cobertura — em especial o bloco 501–600, com apenas 2% de cobertura. Criadas 5 páginas em `wiki/questoes/`, cobrindo subtópicos diversos do bloco:

1. `por-que-a-acao-dos-espiritos-e-oculta.md` — LE, q. 501 (anjos guardiães, livre-arbítrio como razão da invisibilidade do auxílio espiritual).
2. `espiritos-e-as-leis-da-natureza.md` — LE, q. 526–527 (escada podre e raio: Espíritos atuam dentro das leis naturais, não as derrogam; base doutrinária contra milagre-ruptura e superstição).
3. `pactos-com-satanas-como-alegoria.md` — LE, q. 549–550 (lendas fantásticas como símbolo moral; sintonia com Espíritos inferiores sempre rompível pela vontade; negação das penas eternas).
4. `paternidade-como-missao.md` — LE, q. 582–583 (paternidade como missão; responsabilidade simétrica ao livre-arbítrio do filho; janela providencial da infância).
5. `alma-dos-animais.md` — LE, q. 597–600 (princípio inteligente sobrevive, conserva individualidade, sem livre-arbítrio nem consciência do eu; negação frontal da metempsicose popular).

Seguem rigorosamente o padrão de `arrependimento-expiacao-e-reparacao.md` (Pergunta · Resposta dos Espíritos · Análise · Conceitos relacionados · Fontes). Impacto esperado nas próximas estatísticas: questões únicas citadas do LE passam de 215 → ~230 (+7%); páginas em `wiki/questoes/` passam de 1 → 6; razão conceitos/questões cai de 119:1 para ~20:1. `index.md` atualizado com as 5 entradas na seção Questões.

---

## [2026-04-19] refactor | Lint ignora conteúdo em backticks; remove estatísticas de `index.md`

Lint rodado sobre 246 páginas encontrou 11 achados — todos falsos positivos em `wiki/sinteses/estatisticas-da-wiki.md` (1 `[[...]]` e 4 citações `(LE, q. N)` dentro de inline code, usados como exemplo didático) ou cosméticos (contagem de páginas no `index.md`). Dois ajustes:

1. **`wiki_utils.strip_inline_code`** nova: substitui conteúdo de ``` ``` e `...` por espaços preservando quebras de linha. `find_wikilinks` agora usa antes de scanear, e `check_citation_format` também. Fim dos falsos positivos em prosa explicativa sobre o próprio regex.
2. **`index.md`** perde contagens numéricas ("19 fontes complementares", "~245 páginas") — delegadas a `[[wiki/sinteses/estatisticas-da-wiki]]`. `check_status_projeto` atualizado para não reclamar de ausência (só divergência). 

Pós-correção: 0 erros, 0 avisos, 5 info (divergências abertas, by design, todas com `possibly_incomplete: false`).

---

## [2026-04-16] refactor | `wiki/questoes/` admite itens pontuais de C&I/ESE/Gênese

Convenção de `wiki/questoes/` estendida: deixa de ser restrita a "uma única questão do Pentateuco (LE/LM/OQE)" e passa a admitir também itens pontuais de C&I/ESE/Gênese — mantendo o espírito de Q&A direta (uma pergunta, uma citação literal, um comentário, uma análise). Motivo: a primeira página de questão (`arrependimento-expiacao-e-reparacao`) nasce ancorada em C&I, 1ª parte, cap. VII, itens 16–17, e não se encaixa na definição antiga. Ajustados: `.claude/rules/convencoes-paginas.md`, `CLAUDE.md` §4, `.claude/skills/ingest/SKILL.md`.

---

## [2026-04-16] query | Tríade arrependimento–expiação–reparação (C&I)

Pergunta de estudo: "Segundo *O Céu e o Inferno*, qual a diferença entre arrependimento, expiação e reparação?". Resposta ancorada em C&I, 1ª parte, cap. VII, itens 16–17 (e nota). Arquivado como `wiki/questoes/arrependimento-expiacao-e-reparacao.md` — estrutura Q&A com citação literal dos itens 16–17, comentário de Kardec sobre a reparação como "verdadeira lei de reabilitação moral dos Espíritos", tabela-síntese dos três papéis e análise das três esferas da expiação. Links recíprocos adicionados em `arrependimento`, `expiacao`, `expiacao-e-reparacao` e `codigo-penal-da-vida-futura`; datas bumpadas para 2026-04-16. `index.md` atualizado (primeira entrada da seção Questões).

---

## [2026-04-16] refactor | Nova pasta `wiki/aprofundamentos/`

Introduzido o tipo `aprofundamento` para estudos sistemáticos de temas ou blocos doutrinários (subseções do LE, capítulos do ESE, conjuntos de itens de C&I). `wiki/questoes/` fica reservado para Q&A direta de **uma única questão** do Pentateuco. `expiacao-e-arrependimento.md` (13 questões, 990–1002) migrou de `questoes/` para `aprofundamentos/` — tipo e links atualizados. Diretivas ajustadas: CLAUDE.md §4, `.claude/rules/convencoes-paginas.md`, `.claude/skills/ingest/SKILL.md`, `.claude/skills/slides/SKILL.md`, scripts de stats/update_status/lint. Reexecutar `/stats` para atualizar `wiki/sinteses/estatisticas-da-wiki.md`.

---

## [2026-04-16] lint | 18 achados

Os 10 erros/avisos em torno de `expiacao-e-arrependimento` têm causa única — o rename de `wiki/questoes/` → `wiki/aprofundamentos/` ainda não foi propagado (7 broken_links + 1 index_broken + órfão + index_missing). Frontmatter erra como falso positivo: `lint_wiki.py:436` ainda não aceita `aprofundamento` em `valid_tipos`. 1 `citation_format` real em `(C&I, item 20)` sem parte/capítulo. 5 divergências abertas, todas completas.

---

## [2026-04-16] lint | 9 achados

Restam 2 broken_links em `wiki/sinteses/estatisticas-da-wiki.md` apontando para `wiki/questoes/expiacao-e-arrependimento` (caminho antigo) — regerar via `/stats`. 1 `citation_format` persistente em `(C&I, item 20)` (sem parte/capítulo) em `wiki/aprofundamentos/expiacao-e-arrependimento.md:332`. 5 divergências abertas, todas completas. 1 info cosmético no `index.md` (15 vs 19 fontes complementares).

---

## [2026-04-16] lint | 5 achados

Wiki limpa: 0 erros, 0 avisos. Apenas as 5 divergências abertas esperadas (status informativo), todas com corpo completo (`possibly_incomplete: false`). 245 páginas catalogadas (1 aprofundamento, 119 conceitos, 6 divergências, 24 obras, 92 personalidades, 3 sínteses).

---

## [2026-04-15] ingest | Entre a Terra e o Céu (André Luiz/Chico Xavier)

Ingerido o 8º livro da série André Luiz (1954, FEB, 40 capítulos) a partir de `raw/mediuns/entre-a-terra-e-o-ceu.md`. Criadas: `wiki/obras/entre-a-terra-e-o-ceu.md` e cinco personalidades (andre-luiz, clarencio, irma-clara, odila, zulmira). Os conceitos `obsessao`, `reencarnacao` e `prece` foram estendidos: obsessão por sintonia de remorso (caso Zulmira–Odila) e protocolo de desobsessão envolvente; mecânica fluídica da gravidez e hereditariedade relativa; distinção prece × invocação. Nenhuma divergência com o Pentateuco identificada — obra aprofunda a mecânica perispirítica de forma coerente com LE/LM/ESE.

---

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

## [2026-04-15] lint | 7 achados
0 erros. 1 aviso (estatisticas-da-wiki órfã, esperado). 5 divergências abertas (todas já desenvolvidas). index.md diz 15 fontes complementares mas há 19 — cosmético.

## [2026-04-18] lint | 6 achados
0 erros, 0 avisos. 5 divergências abertas (todas desenvolvidas, sem sinal de incompletude). index.md diz ~245 páginas mas há 246 — cosmético.

## [2026-04-19] refactor | Higiene do script de estatísticas

Em `.claude/skills/stats/scripts/stats_wiki.py`: (1) meta-páginas (`tipo: sintese` + tag `meta`) excluídas de grafo, vocabulário e tamanho via helper `is_meta_page()`; (2) seções-template `## Fontes`, `## Páginas relacionadas`, `## Páginas referenciadas` e `## Conceitos relacionados` removidas antes da tokenização via `TEMPLATE_SECTION_RE`. Impacto: grafo 246→245 nós, 1918→1873 arestas; `estatisticas-da-wiki` não aparece mais como #2 conector. Bigramas dominantes passam de "trad guillon ribeiro" (262), "fontes kardec" (205), "páginas relacionadas" (202) para "mundo espiritual" (100), "ensino kardec" (96), "aplicação prática" (90) — sinal doutrinário em vez de aparato bibliográfico. Marca item correspondente no ROADMAP como concluído.

## [2026-04-21] lint | 41 achados

Nenhum erro; integridade estrutural OK (links, frontmatter, Pentateuco completo). 36 avisos de `index_missing` concentrados em parábolas (ESE) e páginas recentes de Romanos/1 Coríntios (obras + 4 divergências) ainda não inseridas no `index.md`. 1 `fontes_missing` em `sinteses/catalogo.md` (meta), 1 `citation_format` em LM (referência a parte, provável falso positivo) e 1 `tag_taxonomy` em `trilhas/leitura-livre.md`. Info: contagens do `index.md` desatualizadas (18→22 complementares, ~276→280 páginas).

## [2026-04-21] refactor | Renomeia checks `index_*` → `catalogo_*` no lint

A home `index.md` virou landing de trilhas e não lista páginas individuais — a listagem linear vive em `wiki/sinteses/catalogo.md`. Para refletir isso: (1) checks `index_broken` e `index_missing` renomeados para `catalogo_broken` e `catalogo_missing`, lendo apenas o catálogo; (2) `ingest/SKILL.md`, `stats/SKILL.md` e `CLAUDE.md` §4 atualizados para apontar ao catálogo nas instruções de "listar novas páginas". `update_status.py` (atualização da linha "Cobertura atual" na home) segue válido.

## [2026-04-21] lint | 42 achados

0 erros; integridade estrutural OK (links, frontmatter, Pentateuco). 37 `catalogo_missing`: 30 parábolas (criadas nos ingests do ESE, nunca listadas), 2 obras (Epístola aos Romanos, 1 Coríntios) e 4 divergências recentes, mais o próprio `sinteses/catalogo.md` (falta `index: false` no frontmatter). 1 `fontes_missing` e 1 `citation_format` (`LM, 1ª e 2ª parte`, descritivo/falso positivo) ambos em `catalogo.md` — meta. 1 `tag_taxonomy` em `trilhas/leitura-livre.md` (fonte C&I presente, falta `obra/ci`). Info: contagens do `index.md` desatualizadas (18→22 complementares, ~276→280 páginas).

## [2026-04-21] refactor | Cobertura completa do catálogo + correção das contagens de status

Resolvidos os 42 achados do lint anterior. Em `wiki/sinteses/catalogo.md`: (1) adicionadas 30 parábolas em "Parábolas de Jesus" (lista individual após o índice temático), (2) adicionados `discernimento-dos-espiritos`, `epistola-aos-romanos` e `primeira-epistola-aos-corintios` nas seções correspondentes, (3) adicionadas 4 divergências paulinas (`pecado-original-em-romanos-5`, `predestinacao-em-romanos-8-9`, `celibato-como-ideal-paulino`, `silencio-das-mulheres-em-corintios`) na seção Divergências, (4) `index: false` no frontmatter para excluir a meta-página dos checks de catálogo/órfãs, (5) seção `## Fontes` mínima e reescrita do falso positivo `(LM, 1ª e 2ª parte)`. Em `wiki/trilhas/leitura-livre.md`: incluída tag `obra/ci` ausente. Corrigida a divergência de definição de "fontes complementares" entre o lint e o `update_status.py`: ambos agora excluem Pentateuco **e** Evangelhos canônicos (lint ganhou `EVANGELHOS_SLUGS`); `update_status.py` passou a contar também `wiki/trilhas/` no total de páginas. Resultado: lint zerado (0/0/0).
