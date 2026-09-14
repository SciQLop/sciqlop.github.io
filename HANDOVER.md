# Handover — sciqlop.github.io

_Last updated 2026-09-14. Written after the August 2026 site refresh and the September
gallery work; read this first when picking the site up again._

## What this repo is

The public SciQLop website (https://sciqlop.github.io), built with **Quartz 4**
(Markdown in `content/` → static HTML in `public/`). Branch **`v4`** is the live
branch: every push to it runs `.github/workflows/deploy.yml` (`npx quartz build` →
GitHub Pages). `docs/` is Quartz's own documentation, not ours — ignore it.

```
content/            all site pages (Obsidian-flavoured Markdown, [[wikilinks]] ok)
  index.md          landing page: hero downloads, features, install, cite
  Ecosystem.md      the stack under SciQLop (Speasy, SciQLopPlots, CDFpp, cocat …)
  Teaching.md       students / instructors entry point
  whats-new.md      release highlights (0.11, 0.12, "coming in 0.13")
  Contact.md
  tutorials/        GUI + Python tutorials, screenshots in sibling folders
  workshlops/       Workshlop 2025 / 2026 pages
  Gallery.md        the gallery page (one section per shot, captions from SOURCES.md)
  gallery/          18 PNGs + SOURCES.md provenance manifest
quartz.config.ts    site config (baseUrl, fonts, colours, plugins)
quartz.layout.ts    sidebar / footer components
quartz/styles/custom.scss   our CSS (download buttons live here)
```

Local preview: `npm ci` once if `node_modules/` is missing (it lives outside `$HOME`
in the toolbox and vanishes on container recreation), then `npx quartz build --serve` (or plain `npx quartz build` and open
`public/index.html`). Builds take ~2 s.

## State of play (commits on `v4` — check `git status -sb`; as of writing they were NOT yet pushed)

| Commit | What |
|---|---|
| `4d98002` | Site refresh: baseUrl fix, footer, hero download buttons, tutorial fixes, Ecosystem/Teaching/What's New pages, Graph+Backlinks removed |
| `716b004` | Workshlop 2026 registration form link |
| `a5423d5` | Workshlop 2026 venue address + pitch |
| `4be3ed6` | Gallery: 13 screenshots + `SOURCES.md` provenance manifest |
| `4f5aaa6`, `012a5e0` | `GALLERY-SHOOT-PROMPT.md`: agent scripts for the round-2/3 shoots |
| (2026-09-14) | Gallery page, 5 new shots, 07 reshoot, landing-page pictures refreshed |

Versions the site currently describes: **SciQLop v0.12.2** (binaries, bumped 2026-09-14),
SciQLopPlots 0.33.x, Speasy 1.7.1. Anything on SciQLop `main` but not in the
v0.12.2 binaries is labelled *"coming in v0.13"* on the site (AI assistant, smart
search, guided tours, `%job`). Remove those labels when 0.13 ships.

## Gallery page: done (2026-09-14)

`content/Gallery.md` exists and is linked from the landing page's "Learn SciQLop" list;
shot 01 is the landing-page hero. The four `10-theme-*.png` are a CSS 2×2 grid
(`.theme-grid` in `custom.scss`), not a composed image. The v0.13 teasers (AI dock,
tours, smart search, empty-panel overlay) sit under a "Coming in v0.13" heading; drop
that heading when 0.13 ships.

Notes:
- `07`: the Properties dock is an auto-hiding pane that overlays the plot while open,
  so it covers the Y axis on purpose. Not a defect, don't reshoot for that.
- `12-guided-tour-coach-mark.png` is in the folder but unused; `12b` is on the page.

Screenshots come from a Mac and land in `~/Downloads/sciqlop-website-shots/` here;
`GALLERY-SHOOT-PROMPT.md` has the agent messages that produced 11, 12, 13 and 07.

## Recurring maintenance

**On every SciQLop release**
- `content/index.md`: bump the version in the **6 asset URLs** of the download
  buttons and the "Latest release" badge (GitHub asset names are versioned, so
  `releases/latest/download/...` can't be used). There is an HTML comment at the
  spot.
- `content/whats-new.md`: add a section; move "coming in 0.13" items into it.
- Check tutorials still match the released `user_api` (verify against the
  **tag**, not `main`: `git -C ../SciQLop show vX.Y.Z:SciQLop/user_api/...`).

**Conventions**
- Product paths in code samples are `//`-separated (`speasy//cda//MMS//...`).
  Single `/` is broken — v0.12 raises `ValueError`.
- Spelling is **SciQLop** everywhere (the old "SciQLOP" was normalised out).
- Don't add wikilinks to pages that don't exist; Quartz renders them as broken
  links (ten of those were removed in August).
- OS icons in the hero are inline Font Awesome Free brand SVGs (CC BY 4.0 —
  attribution comment is in `index.md`, keep it).

## Known gaps / ideas not done

- Theme accent colours in `quartz.config.ts` still Quartz defaults; could be tuned
  to SciQLop's own palette.
- Workshlop 2026 page: room/access plan still "sent to registered participants";
  add it when known. Registration form: Google Form linked on the page.
- Local `playwright` CLI shim is broken (ModuleNotFoundError); for visual checks
  use the browser MCP tools or a fresh `pip install playwright`.

## Where the deeper notes live

- Claude project memory for this repo:
  `~/.claude/projects/-var-home-jeandet-Documents-prog-sciqlop-github-io/memory/`
  (`site-review-2026-08.md` = review + what was implemented,
  `gallery-2026-08-19.md` = shoot notes and the SciQLop API bugs found while
  shooting — most already fixed in SciQLop/SciQLopPlots, see that file).
- Feature/version facts came from the SciQLop and Speasy CHANGELOGs; re-derive
  from there rather than trusting this file when in doubt.
