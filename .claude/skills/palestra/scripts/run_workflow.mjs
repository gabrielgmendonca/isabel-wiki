// Executor retomável do workflow `palestra-dossie` — para quando a tool Workflow
// não estiver disponível na sessão (foi o caso nos runs de 2026-09-04 e 09-12).
//
// Executa o PRÓPRIO `.claude/workflows/palestra-dossie.js` (orquestração, lotes,
// reconciliação e contagem de agentes são os de verdade); só `agent()` é
// substituído. Cada chamada procura `<estado>/results/<label>.json`; se não
// houver, grava prompt + schema em `<estado>/prompts/` e SUSPENDE o run. O
// main-session despacha os pendentes como subagentes (mesmo prompt, mesmo
// modelo), grava os JSON e roda isto de novo — que avança até o próximo estágio.
//
// O estado em disco é o que torna o run retomável: um 429 no meio de um estágio
// custa relançar os agentes que faltaram, não o run inteiro.
//
//   node .claude/skills/palestra/scripts/run_workflow.mjs --args <args.json> [--estado <dir>]
//   node .claude/skills/palestra/scripts/run_workflow.mjs --args <args.json> --stub   # smoke test sem token
import fs from 'node:fs'
import path from 'node:path'

const argv = process.argv.slice(2)
const opt = (nome, padrao) => {
  const i = argv.indexOf(nome)
  return i >= 0 && argv[i + 1] ? argv[i + 1] : padrao
}
const STUB = argv.includes('--stub')
const REPO = path.resolve(opt('--repo', process.cwd()))
const ARGS = path.resolve(opt('--args', 'args.json'))
const ESTADO = path.resolve(opt('--estado', path.join(path.dirname(ARGS), 'estado')))

for (const sub of ['prompts', 'results']) fs.mkdirSync(path.join(ESTADO, sub), { recursive: true })

const src = fs.readFileSync(path.join(REPO, '.claude/workflows/palestra-dossie.js'), 'utf8')
const corpo = src.replace(/^export const meta/m, 'const meta')

const safe = l => String(l).replace(/[^a-zA-Z0-9_-]+/g, '_')
class Pendente extends Error {}
const pendentes = []
const gasto = []

// Fixture mínima conforme o schema, para o smoke test. Alguns campos ganham
// valor realista (locus, sigla/ref) porque a orquestração os PARSEIA — é assim
// que o modo stub exercita a extração de locus e a reconciliação por eco.
const SEMENTES = { fonte: 'ESE, cap. XVII, item 3', sigla: 'LE', ref: 'q. 642', titulo: 'Caso de teste', afirmacao: 'afirmação de teste' }
function fixture(schema, nome) {
  if (!schema || !schema.type) return SEMENTES[nome] || 'x'
  if (schema.enum) return schema.enum[0]
  switch (schema.type) {
    case 'object': {
      const o = {}
      for (const [k, v] of Object.entries(schema.properties || {})) o[k] = fixture(v, k)
      return o
    }
    case 'array': return [fixture(schema.items, nome)]
    case 'boolean': return true
    case 'integer': case 'number': return 0
    default: return SEMENTES[nome] || 'x'
  }
}

async function agent(prompt, opts = {}) {
  const label = opts.label || `anon${gasto.length}`
  gasto.push({ label, model: opts.model || 'sessao', phase: opts.phase, chars: prompt.length })
  if (STUB) return fixture(opts.schema)
  const res = path.join(ESTADO, 'results', `${safe(label)}.json`)
  if (fs.existsSync(res)) {
    try { return JSON.parse(fs.readFileSync(res, 'utf8')) } catch (e) {
      throw new Error(`JSON inválido em ${res}: ${e.message}`)
    }
  }
  fs.writeFileSync(path.join(ESTADO, 'prompts', `${safe(label)}.md`), prompt)
  fs.writeFileSync(path.join(ESTADO, 'prompts', `${safe(label)}.schema.json`), JSON.stringify(opts.schema || {}, null, 1))
  pendentes.push({ label, arquivo: safe(label), model: opts.model || 'sessao', chars: prompt.length })
  throw new Pendente(label)
}

async function parallel(thunks) {
  const rs = await Promise.allSettled(thunks.map(t => t()))
  const outro = rs.find(r => r.status === 'rejected' && !(r.reason instanceof Pendente))
  if (outro) throw outro.reason
  if (rs.some(r => r.status === 'rejected')) throw new Pendente('parallel')
  return rs.map(r => r.value)
}

const logs = []
const log = m => { logs.push(m); console.log(`[log] ${m}`) }
const phase = p => console.log(`[fase] ${p}`)

const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor
const executar = new AsyncFunction('args', 'budget', 'log', 'phase', 'agent', 'parallel', corpo)

// O runtime real entrega `args` como string JSON — exercitar esse caminho.
const args = fs.readFileSync(ARGS, 'utf8')

try {
  const out = await executar(args, null, log, phase, agent, parallel)
  const saida = path.join(ESTADO, 'output.json')
  fs.writeFileSync(saida, JSON.stringify(out, null, 1))
  fs.writeFileSync(path.join(ESTADO, 'pendentes.json'), '[]')
  console.log(`\nCONCLUÍDO — ${saida} (meta.agentes=${out && out.meta && out.meta.agentes}${STUB ? '; modo STUB, sem token gasto' : ''})`)
} catch (e) {
  if (!(e instanceof Pendente)) { console.error(e); process.exit(1) }
  fs.writeFileSync(path.join(ESTADO, 'pendentes.json'), JSON.stringify(pendentes, null, 1))
  console.log(`\nPENDENTES (${pendentes.length}) — despachar como subagentes e rodar de novo:`)
  for (const p of pendentes) {
    console.log(`  ${p.label}  model=${p.model}  prompt=${p.chars} chars`)
    console.log(`    prompt: ${path.join(ESTADO, 'prompts', p.arquivo)}.md`)
    console.log(`    grave:  ${path.join(ESTADO, 'results', p.arquivo)}.json`)
  }
}
fs.appendFileSync(path.join(ESTADO, 'log.txt'), logs.join('\n') + '\n---\n')
