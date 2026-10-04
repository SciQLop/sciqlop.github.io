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
  whats-new.md      release highlights (0.11 → 0.13.1) + a "Coming next" section (CHANGELOG Unreleased)
  under-the-hood.md perf path CDF → cache → SciQLop → GPU, and the A/B environment updates
  Contact.md
  tutorials/        GUI + Python tutorials, screenshots in sibling folders
scripts/bump-release.sh   refresh the fallback release links and check the URLs
quartz/static/latest-release.js   resolves the download cards to the latest GitHub release
  workshlops/       Workshlop 2025 / 2026 pages
  Gallery.md        the gallery page (one section per shot, captions from SOURCES.md)
  gallery/          18 PNGs + SOURCES.md provenance manifest
quartz.config.ts    site config (baseUrl, fonts, plugins; colours = SciQLop's space/light palettes)
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

Versions the site currently describes (2026-10-04): **SciQLop v0.13.1** (2026-10-01), Speasy 1.9.0,
SciQLopPlots 0.47, pycdfpp 0.17.0, pysciqlop-cache 0.3.3. The download fallback is v0.13.1 (all
installer URLs checked).

Features that are only on SciQLop `main` carry a `> [!note] Next release` box (Under the hood's A/B
section, several items in the Python user API page and tutorials) and What's New has a "Coming next"
section. **On the next release**: move "Coming next" into a release section and drop those boxes
(`grep -rn "Next release" content`).

## Gallery page: done (2026-09-14)

`content/Gallery.md` exists and is linked from the landing page's "Learn SciQLop" list;
shot 01 is the landing-page hero. The four `10-theme-*.png` are a CSS 2×2 grid
(`.theme-grid` in `custom.scss`), not a composed image. The AI dock, tours, smart
search and empty-panel shots sit under a "New in v0.13" heading.

Notes:
- `07`: the Properties dock is an auto-hiding pane that overlays the plot while open,
  so it covers the Y axis on purpose. Not a defect, don't reshoot for that.
- `12-guided-tour-coach-mark.png` is in the folder but unused; `12b` is on the page.

Screenshots come from a Mac and land in `~/Downloads/sciqlop-website-shots/` here;
`GALLERY-SHOOT-PROMPT.md` has the agent messages that produced 11, 12, 13 and 07.

## Recurring maintenance

**On every SciQLop release**
- The download cards resolve the latest release themselves at page load
  (`quartz/static/latest-release.js` queries the GitHub API and matches each link's
  `data-asset` regex against the asset names; GitHub asset names are versioned, so
  `releases/latest/download/...` can't be used). Nothing to do for the links
  themselves. Still run `scripts/bump-release.sh vX.Y.Z` so the hardcoded fallback
  (used when the API is unreachable or rate-limited) stays current; it also checks
  every binary URL. If an installer is renamed, update its `data-asset` regex.
- `content/whats-new.md`: add a section; move "coming in 0.13" items into it.
- Check tutorials still match the released `user_api` (verify against the
  **tag**, not `main`: `git -C ../SciQLop show vX.Y.Z:SciQLop/user_api/...`).

**Conventions**
- Product paths in code samples are `//`-separated (`speasy//cda//MMS//...`).
  Single `/` is broken — v0.12 raises `ValueError`.
- Spelling is **SciQLop** everywhere (the old "SciQLOP" was normalised out).
- `%%vp` / `%%layer` are safe: Obsidian `%%comments%%` are disabled in `quartz.config.ts` because
  they silently deleted the text between two cell magics (What's New lost ~20 lines).
- Python user API page and tutorials were checked against the v0.13.1 tag on 2026-10-04 by
  reading the code, not by running SciQLop.
- `npx quartz build --serve` crashes when an editor saves through a temp file (ENOENT on
  `*.md.tmp.*`); restart it, or wrap it in a `while true` loop.
- Don't add wikilinks to pages that don't exist; Quartz renders them as broken
  links (ten of those were removed in August).
- OS icons in the hero are inline Font Awesome Free brand SVGs (CC BY 4.0 —
  attribution comment is in `index.md`, keep it).

## Known gaps / ideas not done

- Screenshots to retake (the UI changed; each page carries a note saying so):
  every image of **Basic Plotting Workflow** (old global From/To toolbar, old status bar) and of
  **Catalogs** (old checkbox list, Interaction mode / Zoom factor, removed explorer window).
  `vp_mirror_plot.png` and `simple_mms_template.png` are probably dated too.
- Visual checks: no browser in the toolbox and the playwright MCP wants Chrome. What
  works: `python3 -m venv <dir> && <dir>/bin/pip install playwright && <dir>/bin/playwright
  install chromium` (Chromium lands in `~/.cache/ms-playwright`, survives), then
  `python3 -m http.server` in `public/` and a short Playwright script. Local URLs need
  the `.html` suffix.
- New tutorials (2026-09-14: Annotation layers, DSP toolbox, 2D histograms, Graphic
  primitives, catalog overlays section) were verified against the v0.12.2 tag by
  reading the API, not by running SciQLop. APIs added after 0.12.2 (`dsp.background_subtract`,
  `add_catalog_overlay`, `BinStrategy`, `VerticalLine`, colour swatch) are labelled
  "since v0.13"; all were confirmed present at the v0.13.0 tag.

## Where the deeper notes live

- Claude project memory for this repo lives in two folders, depending on whether the
  session was started from `/var/home` or `/home`:
  `~/.claude/projects/-var-home-jeandet-Documents-prog-sciqlop-github-io/memory/`
  (`gallery-shoot-workflow.md` is in the `-home-` twin)
  (`site-review-2026-08.md` = review + what was implemented,
  `gallery-2026-08-19.md` = shoot notes and the SciQLop API bugs found while
  shooting — most already fixed in SciQLop/SciQLopPlots, see that file).
- Feature/version facts came from the SciQLop and Speasy CHANGELOGs; re-derive
  from there rather than trusting this file when in doubt.
