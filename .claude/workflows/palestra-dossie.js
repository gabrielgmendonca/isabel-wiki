export const meta = {
  name: 'palestra-dossie',
  description: 'Monta um dossiê de preparação de palestra a partir de uma página-semente da wiki IsAbel, com foco opcional. Varredura multi-lente Pentateuco-primeiro, julgamento e definição de termos-chave, caça a casos/histórias com crítico, verificação adversarial de citação e painel socrático. Retorna o dossiê em markdown — a escrita do arquivo é serial no main-session.',
  whenToUse: 'Invocado pela skill /palestra para preparar uma palestra sobre uma página da wiki. Caro em tokens (multi-agente, leitura profunda) — rodar sob demanda, não em loop.',
  phases: [
    { title: 'Varredura', detail: 'lentes em paralelo: núcleo Jesus→Pentateuco, consagrados, wiki, palestras raw, tensões' },
    { title: 'Termos & Casos', detail: 'definição julgada de termos-chave; finders de parábolas/casos/romances' },
    { title: 'Crítica de casos', detail: 'crítico de aptidão doutrinária + risco de misatribuição' },
    { title: 'Verificação', detail: 'cético adversarial por citação do Pentateuco (cite.py)' },
    { title: 'Arco socrático', detail: 'painel de 3 ângulos + júri que sintetiza o vencedor' },
    { title: 'Iconografia', detail: 'arte em domínio público para os momentos-chave (busca web, PD-primeiro)' },
    { title: 'Síntese', detail: 'montagem do dossiê + crítico de completude (lacunas/páginas a criar)' },
  ],
}

// args = { seedPath, foco, termosObrigatorios: [string], tema, data, casa, publico }
// O runtime pode entregar `args` como objeto OU como string JSON — normalizar.
let A = args
if (typeof A === 'string') {
  try { A = JSON.parse(A) } catch (e) { A = {} }
}
A = A || {}
const seedPath = A.seedPath
const foco = (A.foco || '').trim()
const termosObrigatorios = Array.isArray(A.termosObrigatorios) ? A.termosObrigatorios : []
const tema = A.tema || ''
const dataPalestra = A.data || ''
const casa = A.casa || ''
const publico = A.publico || 'misto'
// Cobertura de imagens: 'momentos-chave' (abertura+casos+síntese) | 'casos' | 'quase-todos' | 'off'.
const coberturaImagens = A.imagens || 'momentos-chave'
// Geração por IA fica DESLIGADA por default (risco de representação sagrada); opt-in só p/ abstrato.
const permitirIA = !!A.permitirIA

if (!seedPath) {
  log('palestra-dossie: ERRO — args.seedPath é obrigatório')
  return { erro: 'seedPath ausente', dossie: null }
}

const focoLabel = foco ? `, foco em "${foco}"` : ''

// A profundidade da verificação adversarial e o tamanho dos pools escalam com o
// budget do turno (se o usuário passou "+Nk"); sem budget, defaults generosos
// (este workflow é pedido explicitamente "vá fundo").
const verifyDepth = budget && budget.total
  ? (budget.total >= 400000 ? 3 : budget.total >= 150000 ? 2 : 1)
  : 2

log(`palestra-dossie: semente=${seedPath}${focoLabel}; verifyDepth=${verifyDepth}; público=${publico}`)

// ─── Preâmbulo compartilhado ─────────────────────────────────────────────────

const HIERARQUIA = `Hierarquia de autoridade (CLAUDE.md §2): ensinamentos morais de Jesus (Evangelhos, à luz do Pentateuco) → Pentateuco de Kardec (LE, LM, ESE, C&I, Gênese) → Kardec complementar (OPE, OQE, Revista Espírita) → consagrados (Léon Denis, Emmanuel/Chico Xavier, André Luiz, Joanna de Ângelis, Divaldo, Bezerra, Cairbar, Yvonne Pereira…) → secundários → pesquisa psíquica (Flammarion, Bozzano: corroboração fatual, SEM autoridade doutrinária). Quando nível 2/3/4 contradiz o Pentateuco, **Kardec prevalece** e a divergência é registrada, nunca apagada. Use sempre "kardecista" (nunca "kardequista") e "de Kardec" (nunca "kardequiano/a").`

const CITACAO = `Verificação de citação: para QUALQUER citação do Pentateuco — \`(LE, q. N)\`, \`(ESE, cap. X, item Y)\`, \`(LM, item N)\`, \`(C&I, Nª parte, cap. Y)\`, \`(Gênese, cap. X, item Y)\` — rode \`uv run python scripts/cite.py <SIGLA> "<ref>"\` e use o texto LITERAL retornado; nunca cite de memória. Para fontes complementares (Léon Denis, Chico Xavier, romances espíritas, palestras), busque o texto-fonte via mcp__qmd__query (collections=["raw"], intent claro, lex+vec) — qmd não garante texto literal, então confiança menor.`

function seedContext() {
  return `Página-semente da palestra: \`${seedPath}\`${foco ? `\nFOCO da palestra (peso central): **${foco}**` : ''}${tema ? `\nEixo doutrinário: ${tema}` : ''}
Público: ${publico}. Idioma de toda saída: PT-BR.
Comece SEMPRE lendo a semente: \`Read ${seedPath}\`.`
}

// ─── Schemas ─────────────────────────────────────────────────────────────────

const ACHADO = {
  type: 'object',
  required: ['fonte', 'nivel', 'relevancia_foco', 'trecho'],
  properties: {
    fonte: { type: 'string', description: 'locus/obra/página, ex.: "ESE, cap. X, item 13" ou "Léon Denis, O Problema do Ser, cap. IV" ou "wiki/conceitos/caridade"' },
    nivel: { type: 'string', enum: ['jesus-pentateuco', 'kardec-complementar', 'consagrado', 'secundario', 'pesquisa-psiquica', 'wiki', 'palestra-raw'] },
    relevancia_foco: { type: 'string', description: 'como serve ao foco da palestra (1 frase)' },
    trecho: { type: 'string', description: 'trecho literal (Pentateuco, via cite.py) ou paráfrase curta com aspas no que for literal' },
    citavel: { type: 'boolean', description: 'true se é citação verificável de fonte primária' },
  },
}

const LENS_SCHEMA = {
  type: 'object',
  required: ['lente', 'achados', 'notas'],
  properties: {
    lente: { type: 'string' },
    achados: { type: 'array', items: ACHADO },
    notas: { type: 'string', description: 'leitura geral da lente: o que é forte, o que falta, tensões' },
  },
}

// O núcleo Jesus→Pentateuco devolve, além dos achados, a lista limpa de citações
// do Pentateuco (sigla+ref) que a fase de Verificação vai conferir uma a uma.
const NUCLEO_SCHEMA = {
  type: 'object',
  required: ['lente', 'achados', 'citacoes_pentateuco', 'ancora_jesus', 'notas'],
  properties: {
    lente: { type: 'string' },
    achados: { type: 'array', items: ACHADO },
    citacoes_pentateuco: {
      type: 'array',
      description: 'cada citação do Pentateuco relevante ao tema/foco, com sigla e ref EXATAS para cite.py',
      items: {
        type: 'object',
        required: ['sigla', 'ref', 'afirmacao'],
        properties: {
          sigla: { type: 'string', description: 'LE | LM | ESE | C&I | Gênese' },
          ref: { type: 'string', description: 'ex.: "cap. X, item 13", "q. 886"' },
          afirmacao: { type: 'string', description: 'o que a palestra quer apoiar com essa citação' },
        },
      },
    },
    ancora_jesus: { type: 'string', description: 'a passagem evangélica que ancora o tema (Mt/Mc/Lc/Jo), lida à luz do Pentateuco' },
    notas: { type: 'string' },
  },
}

const TERMOS_SCHEMA = {
  type: 'object',
  required: ['termos'],
  properties: {
    termos: {
      type: 'array',
      items: {
        type: 'object',
        required: ['termo', 'precisa_definir', 'justificativa'],
        properties: {
          termo: { type: 'string' },
          precisa_definir: { type: 'boolean', description: 'JULGAMENTO: este termo precisa ser definido para ESTE público antes de usar?' },
          justificativa: { type: 'string', description: 'por que precisa (ou não) ser definido' },
          definicao_doutrinaria: { type: 'string', description: 'definição de Kardec / da wiki, com locus; "" se não houver' },
          definicao_cultural: { type: 'string', description: 'glosa histórica/cultural de data/dicionario.json, se aplicável; "" se não' },
          fonte: { type: 'string', description: 'locus(es) da definição doutrinária' },
          citacao: {
            type: 'object',
            description: 'se a definição doutrinária vem do Pentateuco, sigla+ref para verificação; omitir se não-Pentateuco',
            properties: { sigla: { type: 'string' }, ref: { type: 'string' } },
          },
        },
      },
    },
  },
}

const CASOS_SCHEMA = {
  type: 'object',
  required: ['casos'],
  properties: {
    casos: {
      type: 'array',
      items: {
        type: 'object',
        required: ['titulo', 'fonte', 'nivel', 'resumo', 'ilustra'],
        properties: {
          titulo: { type: 'string' },
          fonte: { type: 'string', description: 'locus/obra/capítulo; ex.: "Lc 15:11-32", "C&I, 2ª parte, cap. VI", "André Luiz/Chico Xavier, Nosso Lar, cap. X"' },
          nivel: { type: 'string', enum: ['jesus-pentateuco', 'kardec-complementar', 'consagrado', 'secundario', 'pesquisa-psiquica', 'wiki'] },
          resumo: { type: 'string', description: '1-2 frases do enredo' },
          ilustra: { type: 'string', description: 'como ilustra o foco/tema da palestra' },
          como_contar: { type: 'string', description: 'nota de entrega: o gancho, onde pausar, a virada' },
        },
      },
    },
  },
}

const CASOS_CRITICA_SCHEMA = {
  type: 'object',
  required: ['vereditos'],
  properties: {
    vereditos: {
      type: 'array',
      items: {
        type: 'object',
        required: ['titulo', 'fonte', 'apto', 'risco_misatribuicao', 'efetividade', 'nota'],
        properties: {
          titulo: { type: 'string' },
          fonte: { type: 'string' },
          apto: { type: 'boolean', description: 'ilustra REALMENTE o foco e é doutrinariamente seguro?' },
          nivel_autoridade: { type: 'string' },
          risco_misatribuicao: { type: 'string', enum: ['baixo', 'medio', 'alto'], description: 'a fonte realmente contém este caso, atribuído a este autor/obra?' },
          efetividade: { type: 'string', enum: ['alta', 'media', 'baixa'], description: 'força didática/emocional para uma plateia de casa espírita' },
          nota: { type: 'string' },
        },
      },
    },
  },
}

const VERIFY_SCHEMA = {
  type: 'object',
  required: ['status', 'nota'],
  properties: {
    status: { type: 'string', enum: ['confirmed', 'refuted', 'uncertain'], description: 'confirmed = cite.py prova o locus E sustenta a afirmação' },
    texto_literal: { type: 'string', description: 'o texto retornado por cite.py (recortado ao essencial)' },
    nota: { type: 'string', description: 'por que confirma/refuta; locus corrigido se for typo' },
  },
}

const ARCO_SCHEMA = {
  type: 'object',
  required: ['angulo', 'titulo', 'abertura', 'partes', 'sintese'],
  properties: {
    angulo: { type: 'string' },
    titulo: { type: 'string', description: 'título da palestra' },
    abertura: { type: 'string', description: 'pergunta de abertura, satisfazendo critério A, B ou C de perguntas socráticas' },
    partes: {
      type: 'array',
      items: {
        type: 'object',
        required: ['titulo', 'citacoes'],
        properties: {
          titulo: { type: 'string', description: 'section header da parte' },
          pergunta_ponte: { type: 'string', description: 'pergunta forte (A/B/C) ou "" se o header carrega a transição' },
          criterio: { type: 'string', description: 'A, B ou C — qual critério a pergunta satisfaz' },
          citacoes: { type: 'array', items: { type: 'string' }, description: 'loci a citar nesta parte, na ordem' },
          glosa: { type: 'string', description: 'o fio condutor da parte em 1-2 frases' },
        },
      },
    },
    para_meditar: { type: 'string', description: 'título + fonte do caso escolhido (sem texto integral)' },
    sintese: { type: 'array', items: { type: 'string' }, description: '3-5 bullets que retomam a abertura' },
    encerramento: { type: 'string', description: 'citação consolidadora ou convite à reforma íntima; "" se a síntese fecha' },
  },
}

const JURI_SCHEMA = {
  type: 'object',
  required: ['vencedor', 'scores', 'enxertos'],
  properties: {
    vencedor: { type: 'integer', description: 'índice (0-based) do arco vencedor' },
    scores: {
      type: 'array',
      items: {
        type: 'object',
        required: ['idx', 'fidelidade', 'fluxo', 'ancoragem', 'total'],
        properties: {
          idx: { type: 'integer' },
          fidelidade: { type: 'integer', description: '0-10: fidelidade doutrinária e respeito à hierarquia' },
          fluxo: { type: 'integer', description: '0-10: fluxo didático e força das perguntas socráticas' },
          ancoragem: { type: 'integer', description: '0-10: ancoragem em Jesus/Pentateuco e serventia ao foco' },
          total: { type: 'integer' },
          nota: { type: 'string' },
        },
      },
    },
    enxertos: { type: 'string', description: 'o que enxertar dos arcos perdedores no vencedor' },
  },
}

const ICONO_SCHEMA = {
  type: 'object',
  required: ['momento', 'o_que_retratar', 'candidatos'],
  properties: {
    momento: { type: 'string', description: 'o momento-chave coberto (ex.: "Abertura", "Caso: Filho Pródigo", "Síntese")' },
    o_que_retratar: { type: 'string', description: 'a CENA concreta a retratar (não o conceito abstrato)' },
    candidatos: {
      type: 'array',
      description: '2-3 imagens reais, legalmente reutilizáveis (domínio público / CC), com proveniência',
      items: {
        type: 'object',
        required: ['titulo', 'licenca', 'fonte_url'],
        properties: {
          titulo: { type: 'string' },
          autor: { type: 'string', description: 'artista/autor da obra' },
          ano: { type: 'string' },
          fonte_url: { type: 'string', description: 'página de proveniência (Wikimedia Commons, Met, Brooklyn Museum, Rijksmuseum…)' },
          imagem_url: { type: 'string', description: 'URL direta do arquivo de imagem em alta resolução, se disponível' },
          licenca: { type: 'string', description: 'PD / CC0 / CC BY / CC BY-SA — só domínio público ou CC reutilizável, CONFIRMADO na fonte' },
          atribuicao: { type: 'string', description: 'string de crédito pronta para o rodapé/manifesto' },
          por_que: { type: 'string', description: 'por que serve a este momento' },
          legenda: { type: 'string', description: 'legenda curta opcional para o slide' },
        },
      },
    },
    query_fallback: { type: 'string', description: 'query de busca manual, caso o palestrante queira procurar outra' },
    nota_abstrato: { type: 'string', description: 'se NÃO há arte figurativa apta: caminho recomendado (placeholder manual / atmosférico / IA opt-in só p/ abstrato)' },
  },
}

const DOSSIE_SCHEMA = {
  type: 'object',
  required: ['markdown', 'resumo_executivo', 'lacunas', 'paginas_a_criar'],
  properties: {
    markdown: { type: 'string', description: 'o dossiê COMPLETO em markdown PT-BR, pronto para gravar' },
    resumo_executivo: { type: 'string', description: '3-4 frases: o que a palestra defende e como se move' },
    lacunas: { type: 'array', items: { type: 'string' }, description: 'o que ficou sem cobertura: fonte nível-1 não lida, citação não-verificável, termo sem definição, tensão sem resposta' },
    paginas_a_criar: { type: 'array', items: { type: 'string' }, description: 'páginas que a wiki deveria ter (capitalizar): "wiki/<tipo>/<slug> — <motivo>"' },
  },
}

// ─── Prompts ─────────────────────────────────────────────────────────────────

const LENTES = [
  {
    key: 'nucleo',
    schema: NUCLEO_SCHEMA,
    prompt: () => `Você é um estudante kardecista sério montando o NÚCLEO doutrinário de uma palestra. Lente: **Jesus → Pentateuco** (a fundação que tudo o mais ilustra).

${seedContext()}
${HIERARQUIA}
${CITACAO}

Tarefa:
1. Leia a semente e identifique a obra-base e o range (frontmatter \`fontes:\` + citações no corpo).
2. Ancore o tema PRIMEIRO em Jesus: qual passagem evangélica funda o tema${foco ? ` e, em especial, o foco "${foco}"` : ''}? (preencha ancora_jesus).
3. Levante TODAS as citações do Pentateuco relevantes ao tema e ao foco. Para cada uma, rode cite.py e confira o texto literal. Para um capítulo do ESE, leia o \`.index.md\` da obra se precisar localizar item por item. Inclua cross-refs para o LE (ex.: lei de justiça, amor e caridade, q. 873-919) e para bem-aventuranças/virtudes irmãs quando sustentarem o foco.
4. Devolva achados (com trecho literal) E a lista limpa \`citacoes_pentateuco\` (sigla+ref+afirmação) — esta lista será re-verificada adversarialmente, então só inclua loci que você mesmo confirmou com cite.py.
${foco ? `\nDê PESO CENTRAL ao foco "${foco}": separe os itens do capítulo que tratam dele especificamente.` : ''}`,
  },
  {
    key: 'consagrados',
    schema: LENS_SCHEMA,
    prompt: () => `Lente: **vozes consagradas (nível 3)** sobre o tema da palestra. Você complementa o núcleo do Pentateuco com aprofundamento dos espíritos e autores consagrados — sempre com ressalva de nível.

${seedContext()}
${HIERARQUIA}
${CITACAO}

Tarefa: busque via mcp__qmd__query (collections=["wiki","raw"]) o que os consagrados dizem sobre o tema${foco ? ` e o foco "${foco}"` : ''}: Léon Denis, Emmanuel (O Consolador, Caminho Verdade e Vida, Pensamento e Vida), André Luiz, Joanna de Ângelis (via Divaldo), Bezerra de Menezes, Cairbar Schutel, Yvonne Pereira. Para cada achado: marque o nível, traga paráfrase curta (qmd não dá literal garantido), aponte a relevância ao foco. Se algum autor APROFUNDA além do Pentateuco, ótimo; se algum CONTRADIZ o Pentateuco, registre como tensão em \`notas\` (não apague). Lembre: pesquisa psíquica (Flammarion/Bozzano) entra só como corroboração fatual, sem autoridade doutrinária.`,
  },
  {
    key: 'wiki',
    schema: LENS_SCHEMA,
    prompt: () => `Lente: **o que a wiki já tem**. Mapeie as páginas existentes que a palestra deve aproveitar e cruzar — e as que faltam.

${seedContext()}

Tarefa: via mcp__qmd__query (collections=["wiki"]) e leitura da seção "Páginas relacionadas" da semente, liste as páginas-conceito, sínteses, aprofundamentos, questões e personalidades já existentes sobre o tema${foco ? ` e o foco "${foco}"` : ''} (ex.: caridade, perdão, obsessão, leis morais, bem-aventuranças irmãs). Para cada: \`fonte\` = caminho \`wiki/...\`, \`nivel\` = "wiki", \`relevancia_foco\` = como entra na palestra (definição, desdobramento, cross-link). Em \`notas\`, diga o que JÁ está bem coberto e quais páginas faltam (candidatas a capitalizar). NÃO edite nada — só mapeie.`,
  },
  {
    key: 'palestras',
    schema: LENS_SCHEMA,
    prompt: () => `Lente: **palestras já transcritas em raw/palestras/**. Reaproveite enquadramentos, perguntas e anedotas que já funcionaram.

${seedContext()}

Tarefa: via mcp__qmd__query (collections=["raw"], intent claro) busque em \`raw/palestras/**\` material sobre o tema${foco ? ` e o foco "${foco}"` : ''}. Priorize \`raw/palestras/gabriel-mendonca/\` (o estilo do próprio palestrante), depois outros canais. Para cada achado útil: \`fonte\` = caminho + título, \`nivel\` = "palestra-raw", \`relevancia_foco\` = o enquadramento/pergunta/história aproveitável. \`citavel\`=false (palestra não é fonte doutrinária — é material de apoio). Em \`notas\`, sintetize os ângulos já usados para o tema (para não repetir e para herdar o que deu certo). Se não houver nada, devolva achados vazios e diga isso em notas.`,
  },
  {
    key: 'tensoes',
    schema: LENS_SCHEMA,
    prompt: () => `Lente: **tensões e objeções** — as perguntas difíceis que a plateia faria e os pontos onde o tema é mal compreendido. É aqui que mora a profundidade da palestra.

${seedContext()}
${HIERARQUIA}
${CITACAO}

Tarefa: identifique 4-8 tensões legítimas sobre o tema${foco ? ` e o foco "${foco}"` : ''}, por exemplo: a virtude vira conivência com o erro? como conciliar com o discernimento ("a letra mata, o espírito vivifica")? onde o senso comum deturpa o ensino? há divergência registrada em \`wiki/divergencias/\`? Para cada tensão: \`fonte\` = o locus do Pentateuco que a resolve (verifique com cite.py), \`nivel\`, \`relevancia_foco\` = a objeção em 1 frase, \`trecho\` = a chave de leitura kardecista que dissolve a tensão. Em \`notas\`, liste as objeções como perguntas que a plateia faria. Isto alimenta a seção "perguntas prováveis" do dossiê.`,
  },
]

function termosPrompt() {
  const obg = termosObrigatorios.length
    ? `Termos que o palestrante PEDIU explicitamente para definir (sempre incluir, com precisa_definir=true): ${termosObrigatorios.map(t => `"${t}"`).join(', ')}.`
    : 'Nenhum termo obrigatório pré-fixado.'
  return `Você cuida das **definições de termos-chave** da palestra. Definição clara de um termo serve a esta e a várias palestras futuras.

${seedContext()}
${CITACAO}

${obg}

Tarefa:
1. Leia a semente e liste os termos centrais do tema${foco ? ` e do foco "${foco}"` : ''}.
2. JULGUE, para cada termo, se ele precisa ser definido para o público "${publico}" antes de usar (precisa_definir + justificativa). Um termo doutrinário denso ("indulgência", "misericórdia", "expiação") quase sempre precisa; um termo trivial não. Esse julgamento é seu — seja criterioso, não defina o óbvio.
3. Para cada termo que precisa definir, traga DUAS fontes quando aplicável:
   - **definicao_doutrinaria**: como Kardec / a wiki define. Use cite.py para o locus literal do Pentateuco (ex.: a definição de misericórdia em ESE cap. X, item 4) e mcp__qmd__query para a página-conceito da wiki. Preencha \`fonte\` e, se for Pentateuco, \`citacao\` (sigla+ref) para verificação.
   - **definicao_cultural**: leia \`data/dicionario.json\` (\`Read data/dicionario.json\`) e, se o termo (ou um termo cultural/histórico vizinho que aparece nas citações — ex.: "ceitil", "altar", "publicano") estiver lá, traga a glosa. Caso contrário, "".
Distinga sempre os dois registros: a definição DOUTRINÁRIA (autoridade) e a glosa CULTURAL (contexto). Não invente definição — se não achar, diga na justificativa.`
}

const CASE_FINDERS = [
  {
    key: 'evangelho-ci',
    prompt: () => `Você caça **parábolas evangélicas e casos de C&I** para a palestra contar. Histórias prendem a plateia e fixam o ensino.

${seedContext()}
${CITACAO}

Tarefa: encontre parábolas de Jesus e casos d'O Céu e o Inferno (C&I) que ilustrem o tema${foco ? ` e, sobretudo, o foco "${foco}"` : ''}. Busque em mcp__qmd__query (collections=["raw"] para Evangelho e C&I; collections=["wiki"] para \`wiki/sinteses/parabolas-de-jesus\`). Candidatos típicos para misericórdia/perdão/indulgência: Filho Pródigo (Lc 15), servo incompassivo / credor incompassivo (Mt 18:23-35), Bom Samaritano (Lc 10), mulher adúltera (Jo 8), fariseu e publicano (Lc 18). Da C&I, casos da 1ª e da 2ª parte (Exemplos). Para cada caso preencha o schema, com \`como_contar\` (gancho, onde pausar, a virada). Verifique o locus antes de afirmar. Traga 4-8 candidatos fortes, não uma lista exaustiva fraca.`,
  },
  {
    key: 'romances-andre-luiz',
    prompt: () => `Você caça **casos dos romances espíritas** — André Luiz e outros — para a palestra contar.

${seedContext()}
${CITACAO}

Tarefa: via mcp__qmd__query (collections=["raw"], foco em \`raw/mediuns/**\`) encontre episódios da série André Luiz/Chico Xavier (Nosso Lar, Os Mensageiros, Missionários da Luz, Obreiros da Vida Eterna, Entre a Terra e o Céu, Libertação, E a Vida Continua…), dos romances de Emmanuel (Há Dois Mil Anos, Cinquenta Anos Depois, Paulo e Estêvão, Renúncia, Ave Cristo), de Yvonne Pereira (Memórias de um Suicida, Recordações da Mediunidade) e de Joanna de Ângelis que ilustrem o tema${foco ? ` e o foco "${foco}"` : ''}. Cuidado com autoria: o autor espiritual ≠ o médium (confira o frontmatter de \`raw/mediuns/<médium>/<obra>.md\`, campo \`Autor espiritual:\`). Preencha o schema com \`fonte\` no formato "Autor espiritual / Médium, Obra, cap." e \`como_contar\`. Marque \`nivel\` corretamente. Traga 3-6 candidatos verificáveis — episódios que você localizou no texto, não de memória.`,
  },
]

function casosCriticaPrompt(candidatos) {
  return `Você é o **crítico de casos e histórias** da palestra. Sua função é proteger o palestrante de contar caso impróprio, mal-atribuído ou fraco. Seja adversarial: na dúvida, reprove.

${seedContext()}
${CITACAO}

Candidatos levantados pelos finders (JSON):
${JSON.stringify(candidatos, null, 1)}

Para CADA candidato, julgue:
1. **apto** — ilustra REALMENTE o foco${foco ? ` "${foco}"` : ''}/tema, e é doutrinariamente seguro (não passa mensagem que contradiz o Pentateuco)? Um caso que "fala de perdão genericamente" mas não toca o foco da palestra NÃO é apto.
2. **risco_misatribuicao** — a fonte/autor/locus está certo? Verifique pontos suspeitos com mcp__qmd__query (raw) ou cite.py. "Filho Pródigo é de Mateus" seria um erro grave; pegue isso. Atribuir a André Luiz algo que é de Emmanuel, idem. Alto risco = você não conseguiu confirmar a atribuição.
3. **efetividade** — força didática/emocional para uma plateia de casa espírita.
Devolva um veredito por candidato. Reprove (apto=false) os que não tocam o foco, os de alto risco de misatribuição e os de baixa efetividade redundante.`
}

function verifyPrompt(c, lens) {
  return `Verificação ADVERSARIAL de uma citação do Pentateuco destinada a uma palestra. Sua tarefa é TENTAR REFUTAR que o locus sustenta a afirmação — só confirme se não conseguir. Lente: **${lens}**.

Citação a conferir:
  Obra/locus: ${c.sigla} ${c.ref}
  Afirmação que ela deveria sustentar: ${c.afirmacao || '(definir a partir do texto)'}

Procedimento:
  - Rode \`uv run python scripts/cite.py ${c.sigla} "${c.ref}"\` e leia o texto LITERAL.
  - Se o locus for inválido/fora do range, NÃO ajuste no chute: busque o locus correto com mcp__qmd__query (collections=["raw"]) e relate no campo nota; status=uncertain ou refuted.
  - Confirme (status=confirmed) só se o texto literal de fato sustenta a afirmação. Cuidado com paráfrase legítima (sentido preservado = confirmed) vs deturpação (sentido torcido = refuted).
  - Devolva o texto_literal recortado ao essencial.`
}

const VERIFY_LENSES = ['o locus existe e bate?', 'o texto sustenta MESMO a afirmação?', 'há deturpação de sentido?']

function arcoPrompt(angulo, nucleo, casosAprovados, termos) {
  return `Você desenha um **arco socrático** completo para a palestra, no ângulo **${angulo.nome}**: ${angulo.desc}

${seedContext()}
${dataPalestra ? `Data da palestra: ${dataPalestra}. ` : ''}${casa ? `Casa: ${casa}. ` : ''}Público: ${publico}.

Estrutura socrática invariante das palestras de Gabriel: Capa → Pergunta de abertura → Partes temáticas (cada uma com section header) → Núcleo Q&A (citações literais) → "Para meditar" (um caso) → Síntese (retoma a abertura) → Encerramento opcional.

Critérios das perguntas-ponte (toda pergunta socrática precisa satisfazer ao menos UM; senão, suprima a pergunta e deixe o header carregar):
  A. Ancorar num particular concreto (nome, cena, número já citado) — nunca conceito abstrato sozinho.
  B. Expor tensão com a resposta anterior (a pergunta nasce do que acabou de ser citado).
  C. Reproduzir pergunta literal de Kardec ou de Jesus.
Evite teaser sentimental, reformulação vazia do header e pergunta de sim/não suave.

Material disponível (use SÓ o que está aqui; Pentateuco primeiro):
  Núcleo Pentateuco: ${JSON.stringify(nucleo && nucleo.citacoes_pentateuco || [], null, 0)}
  Âncora em Jesus: ${nucleo && nucleo.ancora_jesus || ''}
  Casos aprovados para "Para meditar": ${JSON.stringify((casosAprovados || []).map(c => ({ titulo: c.titulo, fonte: c.fonte })), null, 0)}
  Termos a definir cedo na palestra: ${JSON.stringify((termos && termos.termos || []).filter(t => t.precisa_definir).map(t => t.termo), null, 0)}

Monte o arco no schema. ${foco ? `O foco "${foco}" deve organizar as partes — não o tema inteiro diluído.` : ''} Marque o critério (A/B/C) de cada pergunta-ponte.`
}

const ARC_ANGLES = [
  { key: 'didatico', nome: 'Didático', desc: 'explica do zero, mais glosa e exemplos; ideal para iniciantes/misto. Constrói de Jesus para fora.' },
  { key: 'problematizacao', nome: 'Problematização', desc: 'abre com uma leitura corrente mal-compreendida do tema (a tese a contestar) e organiza as partes pelo contraste.' },
  { key: 'qa-puro', nome: 'Q&A puro', desc: 'segue a ordem dos itens da obra-base sem desvio, com mínimo de glosa; a plateia acompanha o texto.' },
]

function juriPrompt(arcos) {
  return `Você é o **júri** que escolhe o melhor arco de palestra entre ${arcos.length} candidatos e diz o que enxertar dos perdedores no vencedor.

${seedContext()}

Critérios (0-10 cada): fidelidade doutrinária e hierarquia (Pentateuco prevalece); fluxo didático e força das perguntas socráticas (A/B/C, sem teaser/sim-não); ancoragem em Jesus/Pentateuco e serventia ao foco${foco ? ` "${foco}"` : ''}. Some em total.

Arcos candidatos (JSON):
${JSON.stringify(arcos.map((a, i) => ({ idx: i, ...a })), null, 1)}

Pontue cada um, escolha o vencedor (índice 0-based) e descreva em \`enxertos\` os melhores momentos dos perdedores que valem ser incorporados ao vencedor.`
}

function iconoPrompt(m, permitirIaAbstrato) {
  return `Você é o **diretor de arte** da palestra. Encontre imagens DIGNAS e LEGALMENTE reutilizáveis para um momento-chave, no tom de uma casa espírita séria — sem kitsch, sem devocionalismo excessivo, sem anacronismo.

${seedContext()}

Momento-chave: **${m.chave}**
O que ele evoca: ${m.desc}

Princípios:
- **Engate na CENA, não no conceito abstrato.** "Indulgência"/"misericórdia" não se ilustram diretamente; a CENA do caso/parábola, sim (ex.: a mulher adúltera — "atire a primeira pedra"; o retorno do filho pródigo). Procure a cena concreta.
- **Arte em domínio público PRIMEIRO.** A história da arte sacra é quase toda PD e perfeita aqui: gravuras de **Gustave Doré** (La Sainte Bible, 1866), aquarelas de **James Tissot** (A Vida de Cristo, Brooklyn Museum, open access), **Rembrandt** (Filho Pródigo), **Bruegel/Poussin** (mulher adúltera). Fontes com proveniência e licença: **Wikimedia Commons, Met Open Access, Brooklyn Museum, Rijksmuseum, NGA, Google Arts**.
- Use **busca e fetch na web** (procure por WebSearch/WebFetch via ToolSearch) para achar candidatos REAIS. Para cada um, abra a página de proveniência e CONFIRME a licença. Só proponha **domínio público (PD/CC0)** ou **CC reutilizável (CC BY / CC BY-SA)**, com a string de atribuição pronta. NUNCA proponha imagem de licença desconhecida ou "all rights reserved", nem invente URL — se não confirmou, não liste.
- **Enquadramento de destino: faixa vertical de ~45% da tela** (\`![bg right:45%]\` no tema \`isabel\` — texto escuro sobre fundo claro não permite texto por cima da imagem). Prefira composições cujo assunto sobreviva a esse recorte: figura central ou grupo legível, não panorâmica horizontal que depende da largura inteira. Quando um candidato só funcionar em largura cheia, proponha-o e **diga isso** na legenda, para o palestrante decidir.
- Traga 2-3 candidatos, com \`fonte_url\` (e \`imagem_url\` direta quando achar), legenda curta e o porquê de servir ao momento.
- Se NÃO houver arte figurativa apta (conceito abstrato puro, cena sem tradição pictórica), preencha \`nota_abstrato\` com o caminho: placeholder para busca manual (com a \`query_fallback\`)${permitirIaAbstrato ? ', ou geração por IA SÓ se for atmosférico/abstrato (textura, luz, paisagem) — NUNCA figura sagrada gerada por IA.' : ' (geração por IA está DESLIGADA neste run — não sugira IA).'}

Devolva o schema. Idioma: PT-BR.`
}

function sintesePrompt(payload) {
  return `Você monta o **dossiê final de preparação de palestra** — o documento que o palestrante usará para preparar e conduzir a palestra. Escreva em PT-BR, tom de estudante kardecista sério.

${seedContext()}
${HIERARQUIA}

Você recebe todo o material já levantado e verificado (JSON):
${JSON.stringify(payload, null, 1)}

Produza \`markdown\` com EXATAMENTE esta estrutura (use \`##\`/\`###\`):

# Dossiê de palestra — <título sugerido pelo arco vencedor>
Linha de metadados: tema, foco${dataPalestra ? ', data' : ''}${casa ? ', casa' : ''}, página-semente, gerado por /palestra.

## Resumo executivo
3-4 frases: a tese da palestra e como ela se move.

## Núcleo doutrinário (Jesus → Pentateuco)
Comece pela âncora evangélica, depois as citações do Pentateuco. SÓ use citações com status "confirmed" na verificação; marque qualquer "uncertain"/"refuted" com ⚠ e explique. Cite no formato canônico (CLAUDE.md §3) e use nome de obra por extenso onde fizer sentido.

## Definições dos termos-chave
Para cada termo com precisa_definir=true: a definição doutrinária (com locus) e, quando houver, a glosa cultural — distinguindo os dois registros.

## Vozes complementares
Aprofundamentos dos consagrados, SEMPRE com ressalva de nível. Pesquisa psíquica (se houver) marcada como corroboração fatual sem autoridade doutrinária. Tensões/divergências registradas, nunca apagadas.

## Casos e histórias para contar
SÓ os casos com apto=true no crítico. Para cada: título, fonte, o que ilustra, e a nota de como contar. Ordene por efetividade.

## Perguntas prováveis da plateia
As tensões levantadas, formuladas como perguntas, cada uma com a chave de leitura kardecista que responde (com locus).

## Arco socrático sugerido
O arco vencedor do júri (com os enxertos incorporados): abertura, partes com perguntas-ponte (marque A/B/C), Q&A, "Para meditar", síntese, encerramento. Pronto para virar /slides.

## Sugestões de imagem (momentos-chave)
A partir de \`iconografia\` no payload. Para cada momento-chave (abertura, casos, síntese): a cena a retratar e os candidatos de imagem em **domínio público / CC**, cada um com **título, autor, licença, link de proveniência e atribuição** pronta. Marque com ⚠ qualquer candidato sem licença confirmada (não usar). Onde \`nota_abstrato\` indicar que não há arte figurativa apta, registre o caminho (placeholder para busca manual com a query, ou imagem atmosférica). Lembre: a imagem engata na CENA, não no conceito abstrato; e o slide é atmosférico (pouco texto), não infográfico. O enquadramento de destino no tema \`isabel\` é o **layout dividido** (\`![bg right:45%]\`) — prefira candidatos que sobrevivam a ocupar uma faixa vertical de ~45% da tela, e anote quando a composição só funcionar na largura inteira (ver \`convencoes-imagens.md\`, §Mecânica no Marp). Esta seção é o handoff para a colocação no /slides (download local + manifesto de créditos).

## Citações verificadas (apêndice)
Tabela: locus · status · nota. Transparência sobre o que foi conferido com cite.py.

## Lacunas e páginas a capitalizar
O que ficou descoberto e quais páginas a wiki deveria ganhar (princípio de crescimento, CLAUDE.md §1).

## Fontes
Lista das obras citadas.

Também devolva resumo_executivo, lacunas[] e paginas_a_criar[] nos campos próprios. Seja fiel ao material — não invente citação que não esteja no payload verificado.`
}

// ─── Orquestração ────────────────────────────────────────────────────────────

// Stage A — Varredura + termos + finders de casos, tudo em paralelo (cada um só
// depende da semente). Barreira: as etapas seguintes precisam do conjunto todo.
phase('Varredura')
const stageA = await parallel([
  ...LENTES.map(L => () => agent(L.prompt(), { schema: L.schema, phase: 'Varredura', label: `varredura:${L.key}` })),
  () => agent(termosPrompt(), { schema: TERMOS_SCHEMA, phase: 'Termos & Casos', label: 'termos' }),
  ...CASE_FINDERS.map(F => () => agent(F.prompt(), { schema: CASOS_SCHEMA, phase: 'Termos & Casos', label: `casos:${F.key}` })),
])

const nLentes = LENTES.length
const lentes = stageA.slice(0, nLentes)
const nucleo = lentes[0] // schema NUCLEO
const termos = stageA[nLentes] || { termos: [] }
const casosFinders = stageA.slice(nLentes + 1).filter(Boolean)
const casosCandidatos = casosFinders.flatMap(r => (r && r.casos) || [])
log(`varredura: ${lentes.filter(Boolean).length}/${nLentes} lentes, ${(termos.termos || []).length} termos, ${casosCandidatos.length} casos candidatos`)

// Stage B — Crítico de casos (precisa de todos os candidatos juntos).
phase('Crítica de casos')
const casosCritica = casosCandidatos.length
  ? await agent(casosCriticaPrompt(casosCandidatos), { schema: CASOS_CRITICA_SCHEMA, phase: 'Crítica de casos', label: 'casos:critico' })
  : { vereditos: [] }
const aprovadoSet = new Set((casosCritica.vereditos || []).filter(v => v.apto).map(v => `${v.titulo}|${v.fonte}`))
const casosAprovados = casosCandidatos.filter(c => aprovadoSet.has(`${c.titulo}|${c.fonte}`))
log(`casos: ${casosAprovados.length}/${casosCandidatos.length} aprovados pelo crítico`)

// Stage C — Verificação adversarial das citações do Pentateuco (coletadas do
// núcleo + definições de termos; dedup; barreira justificada: dedup antes de gastar).
const citacoes = []
const seen = new Set()
function pushCit(sigla, ref, afirmacao) {
  if (!sigla || !ref) return
  const k = `${String(sigla).toLowerCase()}|${String(ref).toLowerCase()}`
  if (seen.has(k)) return
  seen.add(k)
  citacoes.push({ sigla, ref, afirmacao: afirmacao || '' })
}
;(nucleo && nucleo.citacoes_pentateuco || []).forEach(c => pushCit(c.sigla, c.ref, c.afirmacao))
;(termos.termos || []).forEach(t => { if (t.citacao && t.citacao.sigla) pushCit(t.citacao.sigla, t.citacao.ref, `definição de ${t.termo}`) })

phase('Verificação')
log(`verificação: ${citacoes.length} citações do Pentateuco × ${verifyDepth} cético(s)`)
const verificacoes = await parallel(citacoes.map(c => () =>
  parallel(Array.from({ length: verifyDepth }, (_, k) =>
    () => agent(verifyPrompt(c, VERIFY_LENSES[k % VERIFY_LENSES.length]), {
      schema: VERIFY_SCHEMA, model: 'sonnet', phase: 'Verificação', label: `verify:${c.sigla} ${c.ref}`,
    })
  )).then(votes => {
    const ok = votes.filter(Boolean)
    const conf = ok.filter(v => v.status === 'confirmed').length
    const ref = ok.filter(v => v.status === 'refuted').length
    const status = ref > conf ? 'refuted' : (conf >= Math.ceil((ok.length || 1) / 2) ? 'confirmed' : 'uncertain')
    const lit = (ok.find(v => v.texto_literal) || {}).texto_literal || ''
    return { ...c, status, texto_literal: lit, votos: ok }
  })
))
const verificadas = verificacoes.filter(Boolean)
log(`verificação: ${verificadas.filter(v => v.status === 'confirmed').length} confirmadas, ${verificadas.filter(v => v.status === 'refuted').length} refutadas, ${verificadas.filter(v => v.status === 'uncertain').length} incertas`)

// Stage D — Painel socrático: 3 ângulos em paralelo, depois o júri.
phase('Arco socrático')
const arcos = (await parallel(ARC_ANGLES.map(a => () =>
  agent(arcoPrompt(a, nucleo, casosAprovados, termos), { schema: ARCO_SCHEMA, phase: 'Arco socrático', label: `arco:${a.key}` })
))).filter(Boolean)
const juri = arcos.length
  ? await agent(juriPrompt(arcos), { schema: JURI_SCHEMA, phase: 'Arco socrático', label: 'arco:juri' })
  : { vencedor: 0, scores: [], enxertos: '' }
const arcoVencedor = arcos[juri.vencedor] || arcos[0] || null
log(`arco: ${arcos.length} candidatos; vencedor = ${arcoVencedor ? arcoVencedor.angulo : 'n/a'}`)

// Stage D.5 — Iconografia: candidatos de imagem (arte PD-primeiro) para os momentos-chave.
// Engata nas CENAS dos casos aprovados + abertura + síntese; nunca no conceito abstrato.
const momentos = []
if (coberturaImagens !== 'off' && arcoVencedor) {
  momentos.push({ chave: 'Abertura', desc: `a abertura da palestra: "${arcoVencedor.abertura || ''}" (foco: ${foco || tema})` })
  const limiteCasos = coberturaImagens === 'quase-todos' ? 6 : 4
  for (const c of casosAprovados.slice(0, limiteCasos)) {
    momentos.push({ chave: `Caso: ${c.titulo}`, desc: `${c.resumo} — fonte: ${c.fonte}. Ilustra: ${c.ilustra}` })
  }
  if (coberturaImagens !== 'casos') {
    momentos.push({ chave: 'Síntese', desc: `o fechamento da palestra: ${(arcoVencedor.sintese || []).join('; ')}` })
  }
  if (coberturaImagens === 'quase-todos') {
    for (const p of (arcoVencedor.partes || [])) momentos.push({ chave: `Parte: ${p.titulo}`, desc: p.glosa || p.titulo })
  }
}
phase('Iconografia')
log(`iconografia: ${momentos.length} momento(s)-chave; cobertura=${coberturaImagens}; IA=${permitirIA ? 'on' : 'off'}`)
const iconografia = momentos.length
  ? (await parallel(momentos.map(m => () =>
      agent(iconoPrompt(m, permitirIA), { schema: ICONO_SCHEMA, phase: 'Iconografia', label: `imagem:${m.chave}` })
    ))).filter(Boolean)
  : []
log(`iconografia: ${iconografia.reduce((n, i) => n + ((i.candidatos || []).length), 0)} candidato(s) de imagem em ${iconografia.length} momento(s)`)

// Stage E — Síntese do dossiê (+ crítico de completude embutido nos campos lacunas/paginas).
phase('Síntese')
const payload = {
  tema, foco, seedPath, data: dataPalestra, casa, publico,
  nucleo,
  lentes_complementares: lentes.slice(1).filter(Boolean),
  termos,
  casos_aprovados: casosAprovados,
  casos_reprovados: (casosCritica.vereditos || []).filter(v => !v.apto),
  citacoes_verificadas: verificadas,
  arco_vencedor: arcoVencedor,
  arco_enxertos: juri.enxertos,
  iconografia,
}
const dossie = await agent(sintesePrompt(payload), { schema: DOSSIE_SCHEMA, phase: 'Síntese', label: 'sintese' })

log('palestra-dossie: dossiê montado.')

// Retorna o agregado; a GRAVAÇÃO do arquivo (reports/palestra/...) é serial no
// main-session da skill /palestra — workflows não escrevem em disco.
return {
  meta: { seedPath, foco, tema, data: dataPalestra, casa, publico, verifyDepth },
  dossie,
  detalhe: {
    nucleo,
    lentes,
    termos,
    casos: { candidatos: casosCandidatos, vereditos: casosCritica.vereditos, aprovados: casosAprovados },
    verificacoes: verificadas,
    arcos,
    juri,
    iconografia,
  },
}
