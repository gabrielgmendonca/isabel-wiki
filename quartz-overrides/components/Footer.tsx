import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import style from "./styles/footer.scss"
import { version } from "../../package.json"

interface Options {
  links: Record<string, string>
}

export default ((opts?: Options) => {
  const Footer: QuartzComponent = ({ displayClass, cfg }: QuartzComponentProps) => {
    const year = new Date().getFullYear()
    const links = opts?.links ?? []
    return (
      <footer class={`${displayClass ?? ""}`}>
        <div class="footer-cc">
          <a
            rel="license"
            href="https://creativecommons.org/licenses/by-nc-sa/4.0/deed.pt-br"
            target="_blank"
          >
            <img
              alt="Licença Creative Commons"
              src="https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png"
              width="88"
              height="31"
            />
          </a>
          <span>
            Conteúdo licenciado sob{" "}
            <a
              rel="license"
              href="https://creativecommons.org/licenses/by-nc-sa/4.0/deed.pt-br"
              target="_blank"
            >
              CC BY-NC-SA 4.0
            </a>
          </span>
        </div>
        <p>
          Feito com{" "}
          <a href="https://quartz.jzhao.xyz/">Quartz v{version}</a> © {year}
        </p>
        <ul>
          {Object.entries(links).map(([text, link]) => (
            <li>
              <a href={link}>{text}</a>
            </li>
          ))}
        </ul>
      </footer>
    )
  }

  Footer.css = style
  return Footer
}) satisfies QuartzComponentConstructor
