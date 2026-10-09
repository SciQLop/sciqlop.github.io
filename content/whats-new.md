---
title: What's New
---

Highlights of recent SciQLop releases. Full details in the
[changelog](https://github.com/SciQLop/SciQLop/blob/main/CHANGELOG.md) and
[GitHub releases](https://github.com/SciQLop/SciQLop/releases).

## Coming next (not released yet)

These changes are on `main`. They will ship in the next release.

- **Batch mode** — `sciqlop --batch script.py` runs a script with no window and exits. Handy for quick-look
  plots: one run, one PNG per day. It needs no display, so it runs over SSH or from cron.
  See [[Batch quick-looks]].

- **Updates that can't break a workspace** — each workspace gets two environments. The new version installs
  into the spare one while you keep working. The next start switches to it. A failed update changes nothing.
  See [[under-the-hood#updating-without-breaking-ab-environments|Under the hood]].
- **Reset environment** — when SciQLop fails to start, one button rebuilds the workspace's Python
  environment. Notebooks and settings are kept.
- **Stuck workspaces start again** — a workspace pinned to a version that no longer installs moves to the
  release you are running.
- **Faster** — Speasy fetches use less memory. Panels stay responsive while data loads. Panning and zooming
  near the view no longer refetch.
- **Linux AppImage without `libfuse2`** — it starts on systems that only ship fuse3, like recent Fedora.
- **Keyboard shortcuts** — change any shortcut in Settings. Press **F1** to list them all.
- **Plugin Store** — an **Update all** button, and the welcome page tells you when plugins have updates.
- **Crash help** — every launch keeps its own log. After a crash, an agent can read it and draft the bug
  report for you.
- **Interval timelines** (experimental) — lanes of named intervals, like a logic analyzer's wave view.

## v0.13 — September 2026: the assistant release

Released 2026-09-14. Binaries for each platform are on the [download cards](/#download-sciqlop).

- **AI assistant** — an agent chat dock with pluggable backends (Claude Code, GitHub Copilot, OpenCode, Kimi, Albert)
  that can plot products, fetch and describe data, run notebook cells and inspect your workspace. The transcript
  shows the model's thinking, live and when resuming a session.
- **Smart product search** — hybrid full-text + semantic ranking in the sidebar, and a search overlay on every
  new empty panel.
- **Guided tours** — in-app coach-mark onboarding (Getting Started, Catalogs, Settings); replay from Tools.
- **Background jobs** — the `%job` magic runs long computations off the kernel.
- **DSP: `background_subtract`** — per-channel background removal for dynamic spectra (percentile, sliding
  window, diff/ratio/dB). See the [[DSP toolbox]] tutorial.
- **Catalogs from Python** — `panel.add_catalog_overlay(path, override_color=...)`, plus a colour swatch per
  catalog in the list. See [[Catalogs]].
- **Graphic primitives** — `VerticalLine`, `StraightLine`, `HorizontalSpan`, `RectangularSpan`, `remove()` and
  `visible` on every item. See [[Graphic primitives]].
- **2D histograms** — `BinStrategy.Log` / `SymLog` bins. See [[2D histograms]].
- **Windows**: per-user install, no administrator rights needed. **HTTP proxy** support for every download
  path (uv, Speasy, Jupyter, Qt WebEngine), with a proxy page in the online installer.
- **User API hardening** — a fuzzing campaign turned dozens of silent failures into clear `ValueError` /
  `TypeError` messages: unknown product paths, garbage time ranges (`TimeRange` now parses strings and
  timezone-aware datetimes correctly), invalid virtual-product arguments, failing `panel.save`.
- Fixes for the embedded JupyterLab (recovery after Shut Down / Log Out, package-update breakage) and for
  cross-thread widget access from notebook cells and agent tools.
- **v0.13.1 (2026-10-01)** — bugfix release. Creating or updating a workspace could fail with
  "can't find Rust compiler". An old dependency was pulled in on Python 3.14. It is now pinned to a recent
  version.

## v0.12 — May–August 2026: the analysis release

- **Parameterized virtual products (knobs)** — keyword arguments on your callback become interactive sliders,
  spinboxes, draggable threshold lines and time-range spans in the plot inspector.
- **Annotation layers** — Python functions returning markers, spans or horizontal lines, rendered as overlays on
  your plots; register them with `@register_layer`, the `%%layer` magic, or drag-and-drop from the product tree.
- **DSP toolbox** (`SciQLop.user_api.dsp`) — gap-aware filtering (`filtfilt`, FIR/IIR), resampling, rolling
  statistics, FFT and spectrograms, round-tripping Speasy variables with their metadata.
- **2D histograms** and **in-canvas overlays** (status/info messages on plots).
- **"Copy Python code"** — right-click any graph to get a ready-to-run reproducer snippet (SciQLop panel or
  matplotlib notebook flavor).
- **Editable event metadata** — the catalog event table is now a full editing surface: typed columns, bulk edit,
  tag chips, custom attributes; drag events between catalogs.
- **Panel templates** — save any panel layout as shareable YAML, re-instantiate from the welcome page.
- **ISTP-aware plots** — axis labels, units and log scales picked up automatically from product metadata.
- Graphic primitives (text, ellipses, arrows, images on plots), per-panel crosshair, Perfetto-based profiling,
  much faster startup.
- **v0.12.2 (2026-08-06)** — bugfix release: code execution in the embedded JupyterLab and console
  silently hung in the 0.12.1 installers (IPython 9.16 change); and JupyterLab no longer breaks after package
  updates. If you installed 0.12.1, update.

## v0.11 — April 2026: the platform release

- **Catalog system rewrite** — local, collaborative ([cocat](https://github.com/SciQLop/cocat), real-time CRDT
  co-editing) and read-only Speasy catalogs in one unified browser, with color-coded overlays and jump-to-event.
- **Command palette** (Ctrl+K) — fuzzy-search every action, with multi-step argument chains.
- **Workspaces** — isolated per-project Python environments managed by uv, all from the welcome page.
- **App Store** — browse and hot-install community plugins from a live registry.
- **`%%vp` cell magic** — define virtual products from a notebook cell with typed annotations and hot reload.
- **Fluent plot API**, Speasy `plot()` backend, settings system, dark mode and theming.

