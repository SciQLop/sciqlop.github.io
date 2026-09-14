---
title: Teaching with SciQLop
---

SciQLop was designed with students in mind: it is the easiest way to put *real* spacecraft data — MMS, Cluster,
Solar Orbiter, Parker Solar Probe and many more — in front of a classroom, without spending the first hour of the
session fighting installations.

## Why it works in a classroom

- **One installer per OS, no dependencies.** Students download the [Windows installer, macOS app, or Linux
  AppImage](https://github.com/SciQLop/SciQLop/releases/latest) and are plotting real data minutes later.
- **Isolated workspaces.** Each workspace has its own Python environment managed by
  [uv](https://github.com/astral-sh/uv) — students can `pip install` freely without breaking anything, and a broken
  workspace is just deleted and recreated.
- **Instant gratification.** Drag a product, drop it on a panel, and the data appears — zooming and scrolling
  trigger transparent downloads. Nothing kills curiosity faster than a 45-minute data-wrangling detour.
- **A gentle ramp to real research.** The same tool scales from "first plot ever" to virtual products, event
  catalogs, and publication-grade analysis in embedded Jupyter notebooks.

## Built-in learning material

- **Bundled tutorial notebooks** — a progressive suite (GUI discovery, plotting, virtual products, magics,
  catalogs, DSP, annotation layers, …) browsable directly from the welcome page and copied into the student's
  workspace on first use.
- **Guided tours** — in-app coach-mark tours (Getting Started, Catalogs, Settings) that
  auto-start on first launch.
- **[Website tutorials](/tutorials/)** — step-by-step guides with screenshots for the core workflows.

## Zero-install options

For quick exercises where even an installer is too much, [Speasy](https://github.com/SciQLop/speasy) — SciQLop's
data-access library — runs in the browser: launch its examples on
[Binder or Google Colab](https://speasy.readthedocs.io/), or use it from JupyterLite (Pyodide/WASM). Students can
fetch and plot spacecraft data from any machine with a web browser.

## Hands-on training: the Workshlop

We run an annual hands-on workshop — the **Workshlop** — mixing science talks and guided tutorials.
The [3rd edition takes place Sept 15–17, 2026 in Paris](/workshlops/Workshlop-2026), and registration is open!

## Using SciQLop in your course?

We would love to hear about it — material, feedback, and feature requests for teaching use cases are all welcome.
See the [[Contact]] page.
