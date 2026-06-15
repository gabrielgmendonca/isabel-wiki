---
paths:
  - "slides/**"
  - ".claude/skills/slides/**"
  - ".claude/skills/palestra/**"
  - ".claude/workflows/palestra-dossie.js"
---

# Imagens em slides de palestra

Imagens nos decks Marp das palestras de Gabriel. O objetivo é **prender a atenção e tirar o olhar da plateia do texto** enquanto o orador fala — logo, imagem aqui é **atmosférica, não informacional**. Nada de infográfico denso competindo com a voz: o ideal é uma imagem digna ocupando o slide (full-bleed) com pouca ou nenhuma sobreposição de texto.

## Princípio: a imagem engata na cena, não no conceito

Conceito abstrato (indulgência, misericórdia, perdão) **não se ilustra diretamente** — tentar gera clichê (duas mãos, pomba, pôr do sol). Engate sempre na **cena concreta** do caso/parábola que a palestra já cita: "indulgência" → a mulher adúltera ("atire a primeira pedra"); "misericórdia" → o retorno do filho pródigo. Os casos que o dossiê (`/palestra`) levanta **são** os ganchos de imagem.

## Cobertura: momentos-chave

Imagem onde ela carrega peso, não em todo slide. Default = **momentos-chave**: a abertura, cada caso/"Para meditar", e a síntese. Slides de citação doutrinária e Q&A ficam **tipográficos** (a citação literal é o conteúdo). Não poluir o núcleo Q&A com imagem de fundo que dispute com o texto da Resposta dos Espíritos.

## Cascata de sourcing (nesta ordem)

1. **Arte em domínio público / CC — PRIMEIRO.** A história da arte sacra é quase toda PD e é o encaixe perfeito (digna, reconhecível, sem custo de licença): gravuras de **Gustave Doré** (*La Sainte Bible*, 1866), aquarelas de **James Tissot** (*A Vida de Cristo*, Brooklyn Museum, open access), **Rembrandt** (Filho Pródigo), **Bruegel/Poussin** (mulher adúltera). Fontes com proveniência + licença: **Wikimedia Commons, Met Open Access, Brooklyn Museum, Rijksmuseum, NGA, Google Arts**. Confirmar a licença na página da fonte — só **PD/CC0** ou **CC BY / CC BY-SA**. Nunca usar imagem de licença desconhecida ou "all rights reserved".
2. **Placeholder + brief — fallback universal.** Quando não houver arte apta (conceito sem tradição pictórica), emitir um slot com a **query de busca sugerida** e a legenda, para o palestrante escolher manualmente. Custo zero, risco zero.
3. **Geração por IA — opt-in, restrita.** Só com `--imagens-ia` (ou `permitirIA: true` no workflow) e **apenas para imagem atmosférica/abstrata** (textura, luz, paisagem). **Nunca** gerar figura sagrada (Jesus, espíritos, cenas evangélicas) por IA — risco de kitsch, anacronismo e dissonância com uma casa espírita séria. IA é desligada por default.

## Guarda de dignidade

Tom de estudante kardecista sério: sem kitsch, sem devocionalismo excessivo, sem anacronismo grosseiro. Na dúvida sobre a adequação de uma imagem, preferir o placeholder e deixar a escolha com o humano.

## Higiene de direitos (espelha `convencoes-direitos.md`)

A wiki já tem cultura de proveniência — aplicar aqui:

- **Manifesto de créditos**: cada imagem usada num deck entra em `slides/<slug>/assets/creditos.json` com `arquivo`, `titulo`, `autor`, `ano`, `licenca`, `fonte_url`, `atribuicao`. É a fonte de verdade dos direitos do deck.
- **Crédito visível**: rodapé discreto no slide com a atribuição (obrigatório p/ CC BY/BY-SA; recomendado mesmo p/ PD).
- **Offline-first**: **baixar a imagem para `slides/<slug>/assets/`** e referenciar o arquivo local — nunca hotlink de URL no palco (o projetor da casa pode não ter internet). O download + otimização (`sips` no macOS) é passo do build do deck.

## Mecânica no Marp

- Fundo full-bleed: `![bg](assets/<arquivo>.jpg)`. Layout dividido (imagem + citação): `![bg right:40%](assets/<arquivo>.jpg)` ou `![bg left:40%]`. Escurecer p/ legibilidade do texto por cima: `![bg brightness:0.5](...)`.
- Assets em `slides/<slug>/assets/` (versionados junto do `deck.md`; otimizar p/ < ~500 KB). O `build/` do deck (pptx/pdf) continua gitignored.
- Slides de imagem full-bleed levam **pouco ou nenhum texto** — a imagem é a pausa visual enquanto o orador conduz.

## Handoff dossiê → slides

- **`/palestra` (workflow `palestra-dossie`)**: o estágio **Iconografia** propõe, por momento-chave, a cena a retratar + 2-3 candidatos PD/CC com proveniência e licença (busca web). Sai na seção "Sugestões de imagem" do dossiê. **Não baixa nem coloca nada** — só propõe.
- **`/slides`**: consome a seção de imagem do dossiê, o palestrante **escolhe** o candidato (humano no circuito — o modelo não vê a imagem), e o passo de colocação baixa o arquivo p/ `assets/`, emite o `![bg]` e grava `creditos.json`.

## Não publica na wiki

Como o resto de `slides/` e `reports/`, imagens de palestra ficam **fora do build do Quartz** (`ignorePatterns`). Não confundir com assets da wiki pública (`raw/assets/`).
