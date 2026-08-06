---
title: What's New
---

Highlights of recent SciQLop releases. Full details in the
[changelog](https://github.com/SciQLop/SciQLop/blob/main/CHANGELOG.md) and
[GitHub releases](https://github.com/SciQLop/SciQLop/releases).

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

## v0.11 — April 2026: the platform release

- **Catalog system rewrite** — local, collaborative ([cocat](https://github.com/SciQLop/cocat), real-time CRDT
  co-editing) and read-only Speasy catalogs in one unified browser, with color-coded overlays and jump-to-event.
- **Command palette** (Ctrl+K) — fuzzy-search every action, with multi-step argument chains.
- **Workspaces** — isolated per-project Python environments managed by uv, all from the welcome page.
- **App Store** — browse and hot-install community plugins from a live registry.
- **`%%vp` cell magic** — define virtual products from a notebook cell with typed annotations and hot reload.
- **Fluent plot API**, Speasy `plot()` backend, settings system, dark mode and theming.

## Coming in v0.13

- **AI assistant** — an agent chat dock with pluggable backends (Claude Code, GitHub Copilot, OpenCode, Albert)
  that can plot products, fetch and describe data, run notebook cells and inspect your workspace.
- **Smart product search** — hybrid full-text + semantic ranking in the sidebar and the empty-panel search overlay.
- **Guided tours** — in-app onboarding for first-time users.
- **Background jobs** (`%job` magic), Windows per-user install without admin rights, HTTP proxy support.
