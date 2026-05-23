import { pathToRoot } from "../util/path"
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { classNames } from "../util/lang"
import { i18n } from "../i18n"

const PageTitle: QuartzComponent = ({ fileData, cfg, displayClass }: QuartzComponentProps) => {
  const title = cfg?.pageTitle ?? i18n(cfg.locale).propertyDefaults.title
  const baseDir = pathToRoot(fileData.slug!)
  return (
    <h2 class={classNames(displayClass, "page-title")}>
      <a href={baseDir} aria-label={title}>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="82 28 235 138"
          role="img"
          aria-label={title}
        >
          <g
            fill="none"
            stroke="var(--secondary)"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path
              d="M118,108 C116,98 110,90 106,82 C102,74 106,66 112,60"
              stroke-width="1.5"
              opacity="0.6"
            />
            <g transform="translate(112,58) rotate(20) scale(0.4)">
              <path
                d="M0,0 C-6,-16 -2,-28 0,-34 C2,-28 6,-16 0,0Z"
                fill="var(--secondary)"
                fill-opacity="0.3"
                stroke-width="1.3"
              />
              <path
                d="M0,0 C-14,-8 -16,-22 -12,-28 C-8,-24 -2,-18 0,0Z"
                fill="var(--secondary)"
                fill-opacity="0.2"
                stroke-width="1.3"
              />
              <path
                d="M0,0 C14,-8 16,-22 12,-28 C8,-24 2,-18 0,0Z"
                fill="var(--secondary)"
                fill-opacity="0.2"
                stroke-width="1.3"
              />
            </g>
            <path
              d="M108,76 C104,72 100,68 102,63 C104,60 106,62 105,65"
              stroke-width="0.9"
              opacity="0.45"
            />
            <g
              transform="translate(106,86)"
              fill="var(--secondary)"
              fill-opacity="0.3"
              stroke-width="0.8"
            >
              <circle cx="-2" cy="0" r="2" />
              <circle cx="2" cy="0" r="2" />
              <circle cx="0" cy="3.5" r="1.8" />
            </g>
          </g>
          <text
            x="120"
            y="108"
            font-family="'Garamond', 'EB Garamond', 'Cormorant Garamond', 'Times New Roman', serif"
            font-size="78"
            font-weight="700"
            fill="var(--dark)"
            letter-spacing="-1"
          >
            I
          </text>
          <text
            x="151"
            y="108"
            font-family="'Garamond', 'EB Garamond', 'Cormorant Garamond', 'Times New Roman', serif"
            font-size="54"
            font-weight="400"
            fill="var(--darkgray)"
            letter-spacing="-0.5"
          >
            s
          </text>
          <text
            x="176"
            y="108"
            font-family="'Garamond', 'EB Garamond', 'Cormorant Garamond', 'Times New Roman', serif"
            font-size="78"
            font-weight="700"
            fill="var(--dark)"
            letter-spacing="-1"
          >
            A
          </text>
          <text
            x="236"
            y="108"
            font-family="'Garamond', 'EB Garamond', 'Cormorant Garamond', 'Times New Roman', serif"
            font-size="54"
            font-weight="400"
            fill="var(--darkgray)"
            letter-spacing="-0.5"
          >
            bel
          </text>
          <text
            x="302"
            y="150"
            font-family="'Garamond', 'EB Garamond', 'Cormorant Garamond', 'Times New Roman', serif"
            font-size="13"
            font-weight="500"
            fill="var(--secondary)"
            text-anchor="end"
            letter-spacing="4"
          >
            WIKI ESPÍRITA
          </text>
        </svg>
      </a>
    </h2>
  )
}

PageTitle.css = `
.page-title {
  margin: 0;
  line-height: 0;
}
.page-title a {
  display: inline-block;
  text-decoration: none;
  background: none;
}
.page-title svg {
  display: block;
  width: 100%;
  max-width: 220px;
  height: auto;
}
@media all and (max-width: 800px) {
  .page-title svg {
    max-width: 150px;
  }
}
`

export default (() => PageTitle) satisfies QuartzComponentConstructor
