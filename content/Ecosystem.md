---
title: The SciQLop Ecosystem
---

SciQLop is the visible tip of a full open-source stack for in-situ space physics — think of it as **the in-situ
space physics IDE**. Every layer below the GUI is an independent project you can use on its own, in your scripts,
notebooks, or pipelines.

Curious how the pieces fit together and why they are fast? See [[under-the-hood|Under the hood]].

```
        SciQLop            ← desktop app: plots, catalogs, notebooks, plugins, AI
  SciQLopPlots · NeoQCP    ← GPU-accelerated scientific plotting (C++/Qt, Python bindings)
        Speasy             ← data access: 70+ missions, 65 000+ products
  CDFpp · PyISTP · cocat   ← file formats, metadata, collaborative catalogs
 speasy_proxy · SciQLop-cache  ← local cache and shared community cache
```

## Data access — [Speasy](https://github.com/SciQLop/speasy)

A single, easy-to-use Python interface to **over 70 space missions and 65,000 products**:

- **Providers**: [AMDA](https://amda.irap.omp.eu/) (CDPP/IRAP), [NASA CDAWeb](https://cdaweb.gsfc.nasa.gov/)
  (REST + direct file access), [ESA CSA](https://csa.esac.esa.int/) (Cluster, Double Star),
  [SSCWeb](https://sscweb.gsfc.nasa.gov/) and CDPP 3DView (spacecraft trajectories), plus **direct archive
  access** to any local or remote data archive described by a simple YAML file.
- Transparent multi-level caching, proxy support, and signal-processing helpers (resampling, filtering).
- Runs everywhere Python runs — including **in the browser** (Pyodide/JupyterLite), Binder and Google Colab.
- Current release: 1.9.0.
- `pip install speasy` · [Documentation](https://speasy.readthedocs.io/en/latest/) ·
  Cite: [10.5281/zenodo.4118780](https://doi.org/10.5281/zenodo.4118780)
- [Speasy.jl](https://github.com/SciQLop/Speasy.jl) brings the same interface to Julia.

## Plotting engine — [SciQLopPlots](https://github.com/SciQLop/SciQLopPlots)

The high-performance plotting library behind SciQLop (C++/Qt with Python bindings, `pip install SciQLopPlots`):
GPU-accelerated rendering, millions of points with fluid pan/zoom, time series, spectrograms, 2D histograms,
projection/trajectory plots and waterfalls. Current release: 0.47.
[User guide](https://github.com/SciQLop/SciQLopPlots/blob/main/docs/user-guide.md).

It is built on [NeoQCP](https://github.com/SciQLop/NeoQCP), our modernized fork of
[QCustomPlot](https://www.qcustomplot.com/). NeoQCP is Qt6 only. It draws through QRhi, Qt's GPU layer, which
uses Metal, Direct3D, Vulkan or OpenGL depending on the system. The `NEOQCP_RHI_BACKEND` environment variable
forces one. Current release: 2.0.1.
[Architecture notes](https://github.com/SciQLop/NeoQCP/tree/main/docs/architecture).

## File formats & metadata

- [CDFpp / pycdfpp](https://github.com/SciQLop/CDFpp) — a fast modern C++ (and Python) library to read and write
  NASA CDF files. Thread-safe, MIT-licensed, and it runs in the browser too. Current release: 0.17.0.
  `pip install pycdfpp` · [Documentation](https://pycdfpp.readthedocs.io/en/latest/)
- [PyISTP](https://github.com/SciQLop/PyISTP) — ISTP-compliant abstraction on top of CDF files.

## Catalogs & collaboration

- [tscat](https://github.com/SciQLop/tscat) — time-series catalog storage and API.
- [cocat](https://github.com/SciQLop/cocat) — real-time collaborative catalog editing (CRDT over WebSocket),
  powering SciQLop's shared catalogs.

## Shared infrastructure

- [speasy_proxy](https://github.com/SciQLop/speasy_proxy) — a community caching proxy that speeds up data access
  for everyone; a public instance runs at
  [sciqlop.lpp.polytechnique.fr/cache](https://sciqlop.lpp.polytechnique.fr/cache/).
- [SciQLop-cache](https://github.com/SciQLop/Sciqlop-cache) — the persistent cache behind Speasy. It is a
  key-value store with a C++20 core. Many threads and processes can use it at once, safely. Small values live in
  SQLite; big arrays are memory-mapped files. Current release: 0.3.3.
  `pip install pysciqlop-cache` · [Documentation](https://sciqlop-cache.readthedocs.io/en/latest/)

## Notebooks inside the app

- [jupyqt](https://github.com/SciQLop/jupyqt) — embeds JupyterLab in a PySide6 application. The kernel runs on a
  background thread, so a long cell never freezes the GUI. SciQLop's notebooks run on it.
  `pip install jupyqt`

## And more

[AstraLint](https://github.com/SciQLop/AstraLint) (ISTP/PDS4 file validation),
[broni](https://github.com/SciQLop/broni) (orbit / region intersections),
[orbit-viewer](https://github.com/SciQLop/orbit-viewer) — browse the full list on the
[SciQLop GitHub organization](https://github.com/SciQLop).

## Citing

If you use these tools in your research, please cite them:

- **SciQLop**: [10.5281/zenodo.7379012](https://doi.org/10.5281/zenodo.7379012)
- **Speasy**: [10.5281/zenodo.4118780](https://doi.org/10.5281/zenodo.4118780)
