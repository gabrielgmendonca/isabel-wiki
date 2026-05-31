export const meta = {
  name: 'critica-profunda',
  description: 'Crítica doutrinária profunda de páginas da wiki IsAbel: divergências com o Pentateuco, citações que não sustentam a afirmação, desvio editorial e tags/links faltando. Aplica correções seguras; difere decisões doutrinárias.',
  whenToUse: 'Invocado pelo skill /critica sobre o conjunto de páginas devidas (recém-editadas). Caro em tokens — rodar com pouca frequência.',
  phases: [
    { title: 'Crítica', detail: 'um agente por página: 4 eixos + auto-fix seguro na própria página' },
    { title: 'Verificação', detail: 'cético adversarial por achado high-stakes (eixo 1 e 2)' },
  ],
}

// args = { pages: [{path, tipo, atualizado_em, ...}], dryRun: bool, terminologiaPath: string }
// O runtime pode entregar `args` como objeto OU como string JSON — normalizar.
let A = args
if (typeof A === 'string') {
  try { A = JSON.parse(A) } catch (e) { A = {} }
}
A = A || {}
const pages = A.pages || []
const dryRun = !!A.dryRun
const terminologiaPath = A.terminologiaPath || 'data/terminologia.json'

// Profundidade da verificação adversarial escala com o budget do turno.
const verifyDepth = budget && budget.total
  ? (budget.total >= 300000 ? 3 : budget.total >= 120000 ? 2 : 1)
  : 1

log(`critica-profunda: ${pages.length} página(s), dryRun=${dryRun}, verifyDepth=${verifyDepth}`)

// ─── Schemas ────────────────────────────────────────────────────────────────

const FINDING = {
  type: 'object',
  required: ['axis', 'severity', 'claim', 'evidence'],
  properties: {
    axis: { type: 'integer', enum: [1, 2, 3, 4], description: '1=divergência Pentateuco, 2=citação, 3=editorial, 4=tags/links' },
    severity: { type: 'string', enum: ['alta', 'media', 'baixa'] },
    line: { type: 'integer', description: 'linha 1-based no ARQUIVO (igual ao lint)' },
    claim: { type: 'string', description: 'o que a página afirma' },
    evidence: { type: 'string', description: 'texto literal de cite.py/qmd que contradiz ou não sustenta, com locus' },
    action: {
      type: 'object',
      properties: {
        type: { type: 'string', description: 'replace-text | add-tag | add-wikilink (aplicada nesta etapa)' },
        detail: { type: 'string', description: 'descrição exata da mudança aplicada' },
      },
    },
  },
}

const CRITIQUE_SCHEMA = {
  type: 'object',
  required: ['path', 'applied', 'deferred', 'summary'],
  properties: {
    path: { type: 'string' },
    tipo: { type: 'string' },
    applied: { type: 'array', items: FINDING, description: 'correções SEGURAS já aplicadas à própria página via critica_apply.py (não mudam sentido doutrinário)' },
    deferred: {
      type: 'array',
      description: 'achados que NÃO podem ser auto-corrigidos com segurança — exigem decisão humana. Qualquer eixo: divergência (1), deturpação de citação (2), mudança de sentido editorial (3), tag/link ambíguo (4). Os de eixo 1 e 2 passam por verificação adversarial antes de diferir; os de eixo 3 e 4 vão direto.',
      items: {
        type: 'object',
        required: ['axis', 'severity', 'claim', 'evidence'],
        properties: {
          axis: { type: 'integer', enum: [1, 2, 3, 4] },
          severity: { type: 'string', enum: ['alta', 'media', 'baixa'] },
          line: { type: 'integer' },
          claim: { type: 'string' },
          evidence: { type: 'string', description: 'locus literal (cite.py) ou trecho qmd com a tensão' },
          proposta: { type: 'string', description: 'o que o humano poderia fazer (não aplicado)' },
          divergencia_slug: { type: 'string', description: 'eixo 1: slug kebab-ascii sugerido para a página de divergência' },
          kardec_pos: { type: 'string' }, kardec_cite: { type: 'string' },
          outra_pos: { type: 'string' }, outra_cite: { type: 'string' },
        },
      },
    },
    summary: { type: 'string', description: 'uma frase sobre o estado doutrinário da página' },
  },
}

const VERDICT_SCHEMA = {
  type: 'object',
  required: ['status', 'note'],
  properties: {
    status: { type: 'string', enum: ['confirmed', 'refuted', 'uncertain'] },
    note: { type: 'string', description: 'por que confirma/refuta; cite.py re-rodado quando aplicável' },
  },
}

// ─── Prompts ────────────────────────────────────────────────────────────────

function critiquePrompt(p) {
  return `Você é um estudante kardecista sério auditando UMA página da wiki IsAbel quanto à fidelidade doutrinária. Página: \`${p.path}\` (tipo: ${p.tipo || '?'}).

Hierarquia de autoridade: ensinamentos de Jesus (Evangelhos) → Pentateuco de Kardec (LE, LM, ESE, C&I, Gênese) → Kardec complementar → consagrados. Quando nível 2/3/4 contradiz o Pentateuco, **Kardec prevalece** e a divergência é REGISTRADA, nunca apagada. Use sempre "kardecista" (nunca "kardequista").

PASSO 1 — Leia a página inteira:
  Read ${p.path}

PASSO 2 — Monte o dossiê de verdade-fonte (NÃO confie em memória):
  - Para CADA citação ao Pentateuco \`(LE, q. N)\`, \`(ESE, cap. X, item Y)\` etc., rode:
      uv run python scripts/cite.py <SIGLA> "<ref>"
    e compare o texto LITERAL retornado com o que a página afirma.
  - Para citações de autores complementares (Léon Denis, Chico Xavier, etc.), busque o texto-fonte na coleção raw via mcp__qmd__query (collections=["raw"], intent claro, lex+vec). qmd NÃO dá texto literal garantido — confiança menor.
  - Rode o lint determinístico da página e leia o JSON:
      uv run python .claude/skills/lint/scripts/lint_wiki.py --file ${p.path}
  - Carregue os vocabulários canônicos relevantes (por tema/fontes) de ${terminologiaPath} para o eixo 3.

PASSO 3 — Critique nos 4 eixos:
  EIXO 1 (divergência com o Pentateuco): a página afirma algo que contradiz o Pentateuco SEM já registrar a tensão (sem \`> [!warning]\` nem link a wiki/divergencias/)? Só conta divergência REAL e ainda não-registrada.
  EIXO 2 (citação incorreta): o trecho citado realmente sustenta a afirmação? O locus é o certo? Distinga: (a) typo de locus — o texto certo existe noutro locus que cite.py confirma sustentar a afirmação; (b) deturpação — a própria afirmação está errada.
  EIXO 3 (padrão editorial): estrutura por tipo, seção ## Fontes, formato de citação, terminologia canônica (use ${terminologiaPath}; vocabulários auto_fix=true têm forma canônica fixa).
  EIXO 4 (tags/cross-references): falta tema/* (1–3 por página), falta wikilink a página-conceito existente já nomeada na prosa.

PASSO 4 — Aplique SÓ correções SEGURAS, na PRÓPRIA página, via critica_apply.py (uma chamada por correção):
  - Typo de locus (eixo 2) **somente** se cite.py provar que o novo locus sustenta a afirmação existente:
      uv run python .claude/skills/critica/scripts/critica_apply.py replace-text --path ${p.path} --line <N> --from "<cit antiga>" --to "<cit nova>"
  - Terminologia drift de vocabulário auto_fix=true (eixo 3):
      ...critica_apply.py replace-text --path ${p.path} --line <N> --from "<forma drift>" --to "<forma canônica>"
  - Tag tema/* faltando (eixo 4):  ...critica_apply.py add-tag --path ${p.path} --tag "tema/<x>"
  - Wikilink a conceito existente (eixo 4):  ...critica_apply.py add-wikilink --path ${p.path} --line <N> --text "<texto>" --target "wiki/conceitos/<slug>"
  ${dryRun ? 'MODO DRY-RUN: NÃO rode critica_apply.py. Apenas proponha em `applied` o que faria (com action.detail começando por "DRY-RUN —").' : 'Verifique que o alvo --target existe antes de add-wikilink (ls/Read).'}
  Só entram em \`applied\` correções que NÃO mudam o sentido — typo de locus confirmado, terminologia auto_fix=true, tag tema/* óbvia, wikilink a conceito existente. Tudo que muda SENTIDO (incl. reenquadramento editorial) vai em \`deferred\`, nunca em \`applied\`.

PASSO 5 — Tudo que NÃO é auto-corrigível com segurança vai em \`deferred\` (qualquer eixo):
  - Eixo 1 (divergência) e eixo 2 (deturpação de citação): preencha as duas posições citadas (kardec_pos/kardec_cite vs outra_pos/outra_cite); no eixo 1, também um divergencia_slug kebab-ascii. Estes passarão por verificação adversarial.
  - Eixo 3 (mudança de sentido/enquadramento editorial) e eixo 4 (tag/link ambíguo): preencha claim, evidence e \`proposta\` (o que o humano faria). Vão direto a diferir.

Retorne o objeto do schema. Seja conservador: na dúvida, \`deferred\`, não \`applied\`.`
}

function verifyPrompt(p, hs, lens) {
  return `Verificação ADVERSARIAL de um achado de crítica na página \`${p.path}\`. Sua tarefa é TENTAR REFUTAR o achado — só confirme se não conseguir derrubá-lo. Default para "refuted" quando a evidência não se sustentar; "uncertain" quando ficar genuinamente em dúvida.

Lente desta verificação: **${lens}**.

Achado (eixo ${hs.axis}, ${hs.severity}):
  Afirmação da página: ${hs.claim}
  Evidência alegada: ${hs.evidence}
  ${hs.kardec_cite ? 'Posição Kardec: ' + (hs.kardec_pos || '') + ' (' + hs.kardec_cite + ')' : ''}
  ${hs.outra_cite ? 'Posição complementar: ' + (hs.outra_pos || '') + ' (' + hs.outra_cite + ')' : ''}

Procedimento:
  - Re-rode \`uv run python scripts/cite.py <SIGLA> "<ref>"\` para CADA locus do Pentateuco citado e confira o texto LITERAL.
  - Para fonte complementar, re-busque via mcp__qmd__query (collections=["raw"]).
  - ${hs.axis === 1 ? 'Eixo 1: a divergência é REAL e estrutural, ou se dissolve com leitura kardecista correta / já está registrada na wiki? Uma divergência falsa-positiva no ROADMAP é cara.' : 'Eixo 2: a citação realmente NÃO sustenta a afirmação? Cuidado com paráfrase legítima (locus válido, sentido preservado) — isso é "refuted".'}

Retorne o veredito do schema.`
}

const VERIFY_LENSES = ['correção factual via cite.py', 'leitura kardecista alternativa', 'a fonte realmente diz isso?']

// ─── Pipeline ───────────────────────────────────────────────────────────────

async function processDeferred(critique, p) {
  const items = (critique && critique.deferred) || []
  const out = []
  for (const it of items) {
    // Só eixo 1 (divergência) e 2 (citação) — high-stakes — passam pelo cético
    // adversarial, para matar falso-positivo antes de poluir o ROADMAP. Eixo 3/4
    // são baixo-risco: vão direto a diferir.
    if (it.axis === 1 || it.axis === 2) {
      const votes = await parallel(
        Array.from({ length: verifyDepth }, (_, k) => () =>
          agent(verifyPrompt(p, it, VERIFY_LENSES[k % VERIFY_LENSES.length]), {
            schema: VERDICT_SCHEMA,
            model: 'sonnet',
            phase: 'Verificação',
            label: `verify:${p.path.split('/').pop()}#${it.axis}`,
          })
        )
      )
      const ok = votes.filter(Boolean)
      const refuted = ok.filter(v => v.status === 'refuted').length
      const confirmed = ok.filter(v => v.status === 'confirmed').length
      // Refutado pela maioria → descartar. Senão (confirmado ou incerto) → diferir.
      const disposition = (ok.length && refuted > confirmed && refuted >= Math.ceil(ok.length / 2))
        ? 'dropped' : 'deferred'
      out.push({ ...it, disposition, verdicts: ok })
    } else {
      out.push({ ...it, disposition: 'deferred', verdicts: [] })
    }
  }
  return { ...critique, deferred: out }
}

const results = await pipeline(
  pages,
  (p) => agent(critiquePrompt(p), {
    schema: CRITIQUE_SCHEMA,
    phase: 'Crítica',
    label: `critica:${p.path.split('/').pop()}`,
  }),
  (critique, p) => processDeferred(critique, p)
)

const clean = results.filter(Boolean)
log(`critica-profunda: ${clean.length} página(s) avaliadas; ` +
    `${clean.reduce((n, r) => n + (r.applied ? r.applied.length : 0), 0)} auto-fix, ` +
    `${clean.reduce((n, r) => n + (r.deferred ? r.deferred.filter(v => v.disposition === 'deferred').length : 0), 0)} a diferir`)

// Retorna o agregado para a síntese serial do main-session (/critica SKILL):
// escritas em arquivos compartilhados (status, divergencia-stub, ROADMAP, log,
// state, relatório) acontecem LÁ, nunca em agentes paralelos.
return { pages: clean }
