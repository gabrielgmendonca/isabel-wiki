// @ts-ignore: padrão Quartz para scripts inline — não devem virar módulos
import fontsizeScript from "./scripts/fontsize.inline"
import styles from "./styles/fontsize.scss"
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { classNames } from "../util/lang"

const FontSize: QuartzComponent = ({ displayClass }: QuartzComponentProps) => {
  return (
    <div class={classNames(displayClass, "fontsize-toggle")}>
      <span class="fontsize-label">Aa</span>
      <button
        id="fontsize-down"
        class="fontsize-down"
        aria-label="Diminuir tamanho da fonte"
        title="Diminuir tamanho da fonte"
      >
        A−
      </button>
      <button
        id="fontsize-up"
        class="fontsize-up"
        aria-label="Aumentar tamanho da fonte"
        title="Aumentar tamanho da fonte"
      >
        A+
      </button>
    </div>
  )
}

FontSize.beforeDOMLoaded = fontsizeScript
FontSize.css = styles

export default (() => FontSize) satisfies QuartzComponentConstructor
