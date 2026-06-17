import { PageLayout, SharedLayout } from "./quartz/cfg"
import * as Component from "./quartz/components"
import FontSize from "./quartz/components/FontSize"
import DraftNotice from "./quartz/components/DraftNotice"

// Componentes compartilhados entre todas as páginas
export const sharedPageComponents: SharedLayout = {
  head: Component.Head(),
  header: [],
  afterBody: [],
  footer: Component.Footer({
    links: {
      GitHub: "https://github.com/gabrielgmendonca/isabel-wiki",
      "Sugerir correção": "https://github.com/gabrielgmendonca/isabel-wiki/issues/new/choose",
    },
  }),
}

// Componentes para páginas de conteúdo individuais
export const defaultContentPageLayout: PageLayout = {
  beforeBody: [
    Component.Breadcrumbs({
      rootName: "Início",
      spacerSymbol: "›",
      resolveFrontmatterTitle: true,
      hideOnRoot: true,
      showCurrentPage: true,
    }),
    Component.ArticleTitle(),
    DraftNotice(),
    Component.ContentMeta(),
    Component.TagList(),
  ],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Search(),
    Component.Darkmode(),
    FontSize(),
    Component.DesktopOnly(Component.Explorer()),
  ],
  right: [
    Component.Graph(),
    Component.DesktopOnly(Component.TableOfContents()),
    Component.Backlinks(),
  ],
}

// Componentes para páginas de listagem (tags, pastas)
export const defaultListPageLayout: PageLayout = {
  beforeBody: [
    Component.Breadcrumbs({
      rootName: "Início",
      spacerSymbol: "›",
      resolveFrontmatterTitle: true,
      hideOnRoot: true,
      showCurrentPage: true,
    }),
    Component.ArticleTitle(),
    Component.ContentMeta(),
  ],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Search(),
    Component.Darkmode(),
    FontSize(),
    Component.DesktopOnly(Component.Explorer()),
  ],
  right: [],
}
