---
title: SciQLOP
---

# [**Download the Latest release**](https://github.com/SciQLop/SciQLop/releases/latest)

# What Is SciQLop?

**SciQLop** (**SCI**entific **Q**t application for **L**earning from **O**bservations of **P**lasmas) is a powerful and
user-friendly tool designed for the visualization and analysis of in-situ space plasma data: browse, plot, label,
script, and extend — all in one tool.

Using SciQLop will let you:

- have super easy access to tens of thousands of products from the top main data archives in the world — MMS,
  THEMIS/ARTEMIS, Cluster, Solar Orbiter, Parker Solar Probe, Wind, ACE and many more, served by AMDA, NASA CDAWeb,
  ESA CSA and SSCWeb,
- explore multivariate time series effortlessly, with lightning-fast and transparent downloads as you scroll, zoom in,
  and zoom out,
- visualize custom products with simple Python code executed on-the-fly,
- easily label time intervals and make or edit catalogs of events graphically and rapidly,
- collaborate on catalog editing in real time with other users,
- analyze your data in Jupyter notebooks side by side with interactive plots,
- extend SciQLop with community plugins from the built-in App Store,
- get help from an AI assistant that can plot products, fetch data, and inspect your workspace.

![[sciqlop_screenshot.png]]

Heliophysicists now benefit from decades of space exploration through many spacecraft missions.
Exploring this massive amount of data to find events of interest, build catalogs, and conduct statistical multi-mission
data analysis can be a daunting task without the right tool.

SciQLop aims at being this tool! A simple lightweight yet powerful graphical interface coupled to the limitless options
brought by the Jupyter notebook integration, that focuses on providing users with the easiest possible way to explore,
label and analyze huge amounts of data.
SciQLop is also the right tool for teaching space physics and in-situ spacecraft data handling to students
effortlessly — a built-in guided tour walks new users through their first plot.

# Learn SciQLop

- **Tutorials**: step-by-step [tutorials](/tutorials/) covering basic plotting, catalogs, virtual products, plot
  templates, and the Python user API.
- **Bundled examples**: Jupyter notebooks demonstrating common tasks, browsable from the welcome page inside SciQLop.
- **Workshlop**: our annual hands-on training workshop — join the
  [3rd edition, Sept 15–17 2026, in Paris](/workshlops/Workshlop-2026)!
- **Questions?** See the [[Contact]] page.

# Main Features

## Interactive and Responsive Plotting

SciQLop can handle millions of data points without compromising on interactivity.
Users can scroll, zoom, move, and export plots with ease.

![[SciQLop_MMS.gif]]

## Data Access Made Easy

Accessing data in SciQLop is as simple as a drag and drop from the tens of thousands of products readily available.
New empty panels show a built-in search overlay where you can type to find any product instantly, and the sidebar
smart search combines full-text and semantic ranking to find the right products even when your words don't match the
catalog naming exactly.

![[SciQLop_DragAndDrop.gif]]

## Jupyter Notebook Integration

SciQLop embeds a full IPython kernel and can launch a JupyterLab server connected to it.
Create and manipulate plots, define virtual products, and manage catalogs directly from your notebooks.
Dedicated IPython magics make common operations one-liners: `%plot`, `%%vp`, `%timerange`, `%install`,
`%workspace`, `%job`.

![[sciqlop_jupyterlab_plot_side_by_side.png]]

## Catalogs

SciQLop provides a powerful catalog system for labeling and browsing events in your data: local, collaborative
(cocat) and read-only speasy catalogs in a unified browser, color-coded overlays on your plots, graphical event
creation and editing, and a full notebook API.

![[sciqlop_catalogs.png]]

## Collaborative Catalog Editing

Multiple users can co-edit catalogs in real time via [cocat](https://github.com/SciQLop/cocat) (CRDT-based
synchronization over WebSocket). Create, edit and delete events simultaneously — all changes are merged
conflict-free across all connected clients.

## AI Assistant

SciQLop ships an agent chat dock with pluggable AI backends — Claude Code, GitHub Copilot, OpenCode, and
Albert — installable from the App Store. The assistant has access to dedicated tools: it can plot products,
fetch and describe data, run notebook cells, and inspect your workspace, all under your control.

## Command Palette

Press **Ctrl+K** to open the command palette. It fuzzy-searches all available actions and supports multi-step
argument chains (e.g., select "Plot product" then pick the product).

![[sciqlop_command_palette.png]]

## Workspaces

SciQLop organizes your work into **workspaces**, each with its own isolated Python environment (managed by
[uv](https://github.com/astral-sh/uv)), installed packages, enabled plugins, and examples — all managed from the
welcome page.

![[sciqlop_welcome.png]]

## App Store

Browse and install community plugins directly from within SciQLop. The built-in App Store fetches a
[live registry](https://github.com/SciQLop/sciqlop-appstore), shows descriptions, tags, and GitHub stars, and
handles installation and updates. Plugins are hot-loaded into the running application without restart.

![[sciqlop_appstore.png]]

## Virtual Products

Define custom products with simple Python functions. Virtual products behave exactly like built-in products — they
respond to scroll and zoom with on-the-fly computation, and the `%%vp` cell magic lets you define them right from a
notebook cell.

## Themes, Templates and More

Save and restore complete plot layouts as shareable templates, and switch between four built-in palettes
(light, dark, neutral, space) at runtime.

![[sciqlop_theme.png]]

# How to Install SciQLop

## Windows Users

Download the installer from the [latest release](https://github.com/SciQLop/SciQLop/releases/latest) page and run it.

## Mac Users

Download the Mac App Bundle from the [latest release](https://github.com/SciQLop/SciQLop/releases/latest) page — pick
the right architecture for your Mac (ARM64 for Apple M1/2/3/4 chips and x86_64 for Intel).

## Linux Users

Download the AppImage from the
[latest release](https://github.com/SciQLop/SciQLop/releases/latest) and run it (after making it executable).

## From Sources (for developers)

The installers and AppImages above are the recommended way to use SciQLop. If you want to work on SciQLop
itself, clone the repository and run it with [uv](https://github.com/astral-sh/uv), which handles the
virtualenv and dependencies automatically:

```bash
git clone https://github.com/SciQLop/SciQLop
cd SciQLop
uv run sciqlop
```

# Citing SciQLop

If you use SciQLop in your research, please cite it via its Zenodo DOI:
[10.5281/zenodo.7379012](https://doi.org/10.5281/zenodo.7379012) (covers all versions).

# How to Contribute

Fork the [repository](https://github.com/SciQLop/SciQLop), make your changes and submit a pull request. We will be
happy to review and merge your changes.
Reports of bugs and feature requests are also welcome on the
[issue tracker](https://github.com/SciQLop/SciQLop/issues). Do not forget to star the project if you like it!

# License

SciQLop is free software, released under the
[GNU General Public License v3.0](https://github.com/SciQLop/SciQLop/blob/main/COPYING).

# Credits

The development of SciQLop is supported by the [CDPP](http://www.cdpp.eu/).<br />
We acknowledge support from the federation [Plas@Par](https://www.plasapar.sorbonne-universite.fr)

# Thanks

We would like to thank the developers of the following libraries that SciQLop depends on:

- [PySide6](https://doc.qt.io/qtforpython-6/index.html) for the GUI framework and Qt bindings.
- [QCustomPlot](https://www.qcustomplot.com/) for providing the plotting library.
- [uv](https://github.com/astral-sh/uv) for fast, reliable Python package management.
- [The Jupyter project](https://jupyter.org/) for providing the Jupyter notebook integration.
- [NumPy](https://numpy.org/) for providing a fast Python array library.
