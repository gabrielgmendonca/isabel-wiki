# UI Kit · Wiki (Quartz)

Hi-fi recreation of the live IsAbel site — <https://gabrielgmendonca.github.io/isabel-wiki>.

The real wiki is **Quartz v4** with custom overrides. This kit recreates the chrome
in plain React+Babel so you can compose it into mocks without spinning up Quartz.

## Open

`ui_kits/wiki/index.html` — no build step.

## What's in the box

| File              | What it is |
|---|---|
| `wiki.css`        | All wiki-scoped CSS. Imports `colors_and_type.css`. |
| `Icons.jsx`       | Inlined Lucide subset (the icon library used in placeholders + callouts). |
| `LeftRail.jsx`    | `PageTitle`, `SearchBox`, `Toolbar` (darkmode + FontSize A−/A+), `Explorer` tree. |
| `RightRail.jsx`   | `MiniGraph`, `TOC`, `Backlinks`. |
| `Article.jsx`     | `Breadcrumbs`, `ArticleHead`, `Callout` (warning/tip), `AffordanceCard`, `WikiLink`, `Glossary`, `Footer`. |
| `Screens.jsx`     | `Home` (recreates `index.md`) + `ArticleCaridade` (recreates `wiki/conceitos/caridade.md`). Also exports `TREE` — the explorer's source. |
| `App.jsx`         | Two-screen shell. Click a leaf in the Explorer ("caridade") to navigate. |

## Mapped from source

| Live element                        | Source in `isabel-wiki`                                  | Kit equivalent |
|---|---|---|
| `Component.PageTitle`               | `quartz.layout.ts` · the wordmark                         | `<PageTitle/>` in `LeftRail.jsx` |
| `Component.Search`                  | Quartz core                                               | `<SearchBox/>` |
| `Component.Darkmode`                | Quartz core                                               | `<Toolbar/>` |
| `FontSize`                          | `quartz-overrides/components/FontSize.tsx`                | `<Toolbar/>` (A−/A+) |
| `Component.Explorer`                | Quartz core                                               | `<Explorer/>` |
| `Component.Graph`                   | Quartz core                                               | `<MiniGraph/>` |
| `Component.TableOfContents`         | Quartz core                                               | `<TOC/>` |
| `Component.Backlinks`               | Quartz core                                               | `<Backlinks/>` |
| `Component.Breadcrumbs`             | Quartz core                                               | `<Breadcrumbs/>` |
| `Component.Footer`                  | `quartz-overrides/components/Footer.tsx`                  | `<Footer/>` |
| Obsidian callouts (warning / tip)   | `> [!warning]` / `> [!tip]` markdown                      | `<Callout kind=…/>` |
| Affordance cards on homepage        | inline HTML in `index.md`                                 | `<AffordanceCard/>` |
| Glossary `<abbr>`                   | `quartz-overrides/components/styles/glossary.scss`        | `<Glossary/>` |
| Wikilinks `[[wiki/…]]`              | Obsidian-flavoured md transformer                          | `<WikiLink/>` |

## What's intentionally fake

- **Search** is a no-op (real Quartz uses lunr).
- **Graph** is a hand-laid SVG, not a force-directed sim.
- **Tag pages, folder pages, popovers** are not implemented — the kit covers
  content-page and homepage layouts only (the two views that matter for design work).

## How to extend

Add a new screen by:

1. Authoring a `<NewScreen/>` in `Screens.jsx` using the same `prose` markup.
2. Routing to it from `App.jsx`.
3. Wiring it into the explorer `TREE` so the leaf click navigates.
