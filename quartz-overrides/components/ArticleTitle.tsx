// Override de quartz/components/ArticleTitle.tsx (Quartz v4.4.0), copiado em build-time.
// Motivo: as páginas da wiki não usam `title:` no frontmatter (a convenção é abrir
// com `# Título`). O transformer do Quartz, sem `title:`, usa o NOME DO ARQUIVO (slug)
// como título — então ~98% das páginas exibiam "reencarnacao" (minúsculo, sem acento)
// como <h1>, seguido do `# Reencarnação` do markdown: dois <h1> por página, o primeiro
// um identificador de máquina (ROADMAP §2 / achado 2026-06-17).
//
// Este override:
//  (a) quando não há `title:` explícito, usa o texto do primeiro `# H1` do conteúdo;
//  (b) remove esse H1 líder do corpo quando ele só repete o título exibido — eliminando
//      a duplicata. A árvore (`tree`) é compartilhada por referência e o beforeBody
//      renderiza antes do Content, então o splice se reflete no corpo renderizado.
//
// Limite conhecido: corrige o <h1> VISÍVEL. O título da aba/OG/busca/breadcrumb ainda
// vem de `frontmatter.title` (Head e Breadcrumbs renderizam antes deste componente) —
// para corrigi-los também seria preciso um transformer que preencha `title:` na origem.
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { classNames } from "../util/lang"

// concatena o texto de um nó hast (texto de todos os descendentes)
function textOf(node: any): string {
  if (!node) return ""
  if (node.type === "text") return node.value ?? ""
  if (Array.isArray(node.children)) return node.children.map(textOf).join("")
  return ""
}

const ArticleTitle: QuartzComponent = ({ fileData, tree, displayClass }: QuartzComponentProps) => {
  const fmTitle = fileData.frontmatter?.title
  const stem = fileData.slug?.split("/").pop()
  // o transformer do Quartz só usa o stem (slug) quando NÃO há `title:` explícito;
  // logo, title !== stem ⇒ o autor definiu um título de verdade.
  const explicit = !!fmTitle && fmTitle !== stem

  // primeiro `# H1` do conteúdo
  const root = tree as any
  let h1idx = -1
  let h1text = ""
  if (root && Array.isArray(root.children)) {
    h1idx = root.children.findIndex(
      (n: any) => n.type === "element" && n.tagName === "h1",
    )
    if (h1idx >= 0) {
      h1text = textOf(root.children[h1idx]).trim()
    }
  }

  const title = explicit ? fmTitle : h1text || fmTitle

  // remove o H1 líder se ele apenas repete o título exibido (evita <h1> duplicado)
  if (h1idx >= 0 && h1text && title && h1text.toLowerCase() === String(title).toLowerCase()) {
    root.children.splice(h1idx, 1)
  }

  if (title) {
    return <h1 class={classNames(displayClass, "article-title")}>{title}</h1>
  }
  return null
}

ArticleTitle.css = `
.article-title {
  margin: 2rem 0 0 0;
}
`

export default (() => ArticleTitle) satisfies QuartzComponentConstructor
