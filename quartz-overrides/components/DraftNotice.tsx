// Componente local (não existe no Quartz upstream), copiado em build-time.
// Marca visualmente as páginas com `status: rascunho` no frontmatter — que, por
// usarem campo custom (não o `draft:` do Quartz), são publicadas e renderizam
// idênticas às `ativo`. O aviso fixa a expectativa do leitor público: o conteúdo
// ainda está em revisão (ROADMAP §2 / §10.3). Retorna null em qualquer outro status.
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { classNames } from "../util/lang"

const DraftNotice: QuartzComponent = ({ fileData, displayClass }: QuartzComponentProps) => {
  if (fileData.frontmatter?.status !== "rascunho") {
    return null
  }
  return (
    <aside class={classNames(displayClass, "draft-notice")} role="note">
      <span class="draft-notice-icon" aria-hidden="true">✎</span>
      <span>
        <strong>Página em rascunho.</strong> Conteúdo ainda em revisão — pode conter
        lacunas, seções incompletas ou citações não verificadas.
      </span>
    </aside>
  )
}

DraftNotice.css = `
.draft-notice {
  display: flex;
  gap: 0.55rem;
  align-items: baseline;
  margin: 0.6rem 0 0;
  padding: 0.55rem 0.85rem;
  border-left: 3px solid #c89000;
  border-radius: 5px;
  background: rgba(200, 144, 0, 0.10);
  color: var(--dark);
  font-size: 0.9rem;
  line-height: 1.45;
}
.draft-notice .draft-notice-icon {
  color: #c89000;
  font-weight: 700;
  flex-shrink: 0;
}
.draft-notice strong {
  color: var(--dark);
}
`

export default (() => DraftNotice) satisfies QuartzComponentConstructor
