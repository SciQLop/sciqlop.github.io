import {QuartzConfig} from "./quartz/cfg"
import * as Plugin from "./quartz/plugins"

/**
 * Quartz 4 Configuration
 *
 * See https://quartz.jzhao.xyz/configuration for more information.
 */
const config: QuartzConfig = {
  configuration : {
    pageTitle : "SciQLop",
    pageTitleSuffix : "",
    enableSPA : true,
    enablePopovers : true,
    analytics : {
      provider : "plausible",
    },
    locale : "en-US",
    baseUrl : "sciqlop.github.io",
    ignorePatterns : [ "private", "templates", ".obsidian", "gallery/SOURCES.md" ],
    defaultDateType : "modified",
    theme : {
      fontOrigin : "googleFonts",
      cdnCaching : true,
      typography : {
        header : "Schibsted Grotesk",
        body : "Source Sans Pro",
        code : "IBM Plex Mono",
      },
      // Palette taken from SciQLop's own themes: resources/palettes/space.yaml (dark) and light.yaml
      colors : {
        lightMode : {
          light : "#f8f9fb",
          lightgray : "#e4e8ef",
          gray : "#b7bec9",
          darkgray : "#4b5366",
          dark : "#202124",
          secondary : "#4f46e5",
          tertiary : "#4338ca",
          highlight : "rgba(79, 70, 229, 0.12)",
          textHighlight : "#fff23688",
        },
        darkMode : {
          light : "#151a2e",
          lightgray : "#2a3358",
          gray : "#5866a0",
          darkgray : "#b8c0d8",
          dark : "#e0e6f0",
          secondary : "#6b8afd",
          tertiary : "#566eca",
          highlight : "rgba(86, 110, 202, 0.18)",
          textHighlight : "#b3aa0288",
        },
      },
    },
  },
  plugins : {
    transformers : [
      Plugin.FrontMatter(),
      Plugin.CreatedModifiedDate({
        priority : [ "frontmatter", "git", "filesystem" ],
      }),
      Plugin.SyntaxHighlighting({
        theme : {
          light : "github-light",
          dark : "github-dark",
        },
        keepBackground : false,
      }),
      Plugin.ObsidianFlavoredMarkdown({enableInHtmlEmbed : false}),
      Plugin.GitHubFlavoredMarkdown(),
      Plugin.TableOfContents(),
      Plugin.CrawlLinks({markdownLinkResolution : "shortest"}),
      Plugin.Description(),
      Plugin.Latex({renderEngine : "katex"}),
    ],
    filters : [ Plugin.RemoveDrafts() ],
    emitters : [
      Plugin.AliasRedirects(),
      Plugin.ComponentResources(),
      Plugin.ContentPage(),
      Plugin.FolderPage(),
      Plugin.TagPage(),
      Plugin.ContentIndex({
        enableSiteMap : true,
        enableRSS : true,
      }),
      Plugin.Assets(),
      Plugin.Static(),
      Plugin.Favicon(),
      Plugin.NotFoundPage(),
      // Comment out CustomOgImages to speed up build time
      Plugin.CustomOgImages(),
    ],
  },
}

export default config
