import { PageLayout, SharedLayout } from "./quartz/cfg"
import * as Component from "./quartz/components"

// components shared across all pages
export const sharedPageComponents: SharedLayout = {
  head: Component.Head(),
  header: [],
  afterBody: [],
  footer: Component.Footer({
    links: {
      GitHub: "https://github.com/SciQLop/SciQLop",
      "Issue Tracker": "https://github.com/SciQLop/SciQLop/issues",
      "Cite (Zenodo DOI)": "https://doi.org/10.5281/zenodo.7379012",
      Contact: "/Contact",
    },
  }),
}

// Self-contained: Explorer serialises sortFn with toString() and runs it in the browser.
// Keep readingOrder in sync with quartz.config.ts.
const explorer = () =>
  Component.Explorer({
    sortFn: (a, b) => {
      const readingOrder = [
        "tutorials",
        "Basic-Plotting-Workflow",
        "Catalogs",
        "Python-user-API",
        "plot-templates",
        "virtual-products",
        "Batch-quick-looks",
        "Graphic-primitives",
        "Annotation-layers",
        "DSP-toolbox",
        "2D-histograms",
      ]
      if (a.isFolder !== b.isFolder) return a.isFolder ? -1 : 1
      // No inner helper function: the bundler would wrap it in __name(), undefined in the browser.
      const last = readingOrder.length
      const ra = readingOrder.indexOf(a.slugSegment)
      const rb = readingOrder.indexOf(b.slugSegment)
      return (
        (ra < 0 ? last : ra) - (rb < 0 ? last : rb) ||
        a.displayName.localeCompare(b.displayName, undefined, { numeric: true, sensitivity: "base" })
      )
    },
  })

// components for pages that display a single page (e.g. a single note)
export const defaultContentPageLayout: PageLayout = {
  beforeBody: [
    Component.ConditionalRender({
      component: Component.Breadcrumbs(),
      condition: (page) => page.fileData.slug !== "index",
    }),
    Component.ArticleTitle(),
    Component.ContentMeta(),
    Component.TagList(),
  ],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Flex({
      components: [
        {
          Component: Component.Search(),
          grow: true,
        },
        { Component: Component.Darkmode() },
        { Component: Component.ReaderMode() },
      ],
    }),
    explorer(),
  ],
  right: [
    Component.DesktopOnly(Component.TableOfContents()),
  ],
}

// components for pages that display lists of pages  (e.g. tags or folders)
export const defaultListPageLayout: PageLayout = {
  beforeBody: [Component.Breadcrumbs(), Component.ArticleTitle(), Component.ContentMeta()],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Flex({
      components: [
        {
          Component: Component.Search(),
          grow: true,
        },
        { Component: Component.Darkmode() },
      ],
    }),
    explorer(),
  ],
  right: [],
}
