# Handover — sciqlop.github.io

_Last updated 2026-08-29. Written after the August 2026 site refresh; read this first
when picking the site up again._

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
  gallery/          13 PNGs + SOURCES.md — assets only, NO PAGE YET (see below)
quartz.config.ts    site config (baseUrl, fonts, colours, plugins)
quartz.layout.ts    sidebar / footer components
quartz/styles/custom.scss   our CSS (download buttons live here)
```

Local preview: `npx quartz build --serve` (or plain `npx quartz build` and open
`public/index.html`). Builds take ~2 s.

## State of play (commits on `v4` — check `git status -sb`; as of writing they were NOT yet pushed)

| Commit | What |
|---|---|
| `4d98002` | Site refresh: baseUrl fix, footer, hero download buttons, tutorial fixes, Ecosystem/Teaching/What's New pages, Graph+Backlinks removed |
| `716b004` | Workshlop 2026 registration form link |
| `a5423d5` | Workshlop 2026 venue address + pitch |
| `4be3ed6` | Gallery: 13 screenshots + `SOURCES.md` provenance manifest |

Versions the site currently describes: **SciQLop v0.12.1** (binaries),
SciQLopPlots 0.33.x, Speasy 1.7.1. Anything on SciQLop `main` but not in the
v0.12.1 binaries is labelled *"coming in v0.13"* on the site (AI assistant, smart
search, guided tours, `%job`). Remove those labels when 0.13 ships.

## Next step: build the gallery page

Assets are in `content/gallery/`; the page itself is not written. Everything a
caption needs — event, interval, products, feature shown, caveats — is in
`content/gallery/SOURCES.md`. Plan that was agreed:

1. Create `content/Gallery.md` (title "Gallery"), one section per shot in the
   `01`…`10` order, 1–2 sentence captions taken from `SOURCES.md` (the science
   framing is the selling point — "Burch et al. 2016 EDR event", "type II drift
   *is* the lag in the waterfall").
2. Compose the four `10-theme-*.png` into a single 2×2 image (ImageMagick
   `montage`) rather than four separate embeds.
3. Add a light grid/figure style in `custom.scss` (images `max-width:100%`, caption
   in `var(--darkgray)`), and link the page from the landing-page "Learn SciQLop"
   list and/or make shot 01 the new landing-page hero screenshot.
4. Two teasers were never shot (AI dock, guided-tour coach-mark) — skip them, or
   add later under a clearly labelled "coming in v0.13" heading.

Caveat from the shoot: shot 07's Inspector showed unlabelled spinboxes — since
fixed in SciQLop (`bfb6cf6a2`, 2026-08-20) but the PNG predates the fix; either
reshoot 07 or keep the caption generic ("parameters exposed in the Inspector").

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

- Gallery page (above).
- Theme accent colours in `quartz.config.ts` still Quartz defaults; could be tuned
  to SciQLop's own palette.
- Workshlop 2026 page: room/access plan still "sent to registered participants";
  add it when known. Registration form: Google Form linked on the page.
- Landing-page screenshot (`sciqlop_screenshot.png`) is older than the gallery
  hero — consider swapping in `gallery/01-...png`.
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
