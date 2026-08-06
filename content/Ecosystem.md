---
title: The SciQLop Ecosystem
---

SciQLop is the visible tip of a full open-source stack for in-situ space physics — think of it as **the in-situ
space physics IDE**. Every layer below the GUI is an independent project you can use on its own, in your scripts,
notebooks, or pipelines.

```
        SciQLop            ← desktop app: plots, catalogs, notebooks, plugins, AI
     SciQLopPlots          ← GPU-accelerated scientific plotting (C++/Qt, Python bindings)
        Speasy             ← data access: 70+ missions, 65 000+ products
  CDFpp · PyISTP · cocat   ← file formats, metadata, collaborative catalogs
 speasy_proxy · SciQLop-cache  ← shared community cache infrastructure
```

## Data access — [Speasy](https://github.com/SciQLop/speasy)

A single, easy-to-use Python interface to **over 70 space missions and 65,000 products**:

- **Providers**: [AMDA](http://amda.irap.omp.eu/) (CDPP/IRAP), [NASA CDAWeb](https://cdaweb.gsfc.nasa.gov/)
  (REST + direct file access), [ESA CSA](https://csa.esac.esa.int/) (Cluster, Double Star),
  [SSCWeb](https://sscweb.gsfc.nasa.gov/) and CDPP 3DView (spacecraft trajectories), plus **direct archive
  access** to any local or remote data archive described by a simple YAML file.
- Transparent multi-level caching, proxy support, and signal-processing helpers (resampling, filtering).
- Runs everywhere Python runs — including **in the browser** (Pyodide/JupyterLite), Binder and Google Colab.
- `pip install speasy` · [Documentation](https://speasy.readthedocs.io/) ·
  Cite: [10.5281/zenodo.4118780](https://doi.org/10.5281/zenodo.4118780)
- [Speasy.jl](https://github.com/SciQLop/Speasy.jl) brings the same interface to Julia.

## Plotting engine — [SciQLopPlots](https://github.com/SciQLop/SciQLopPlots)

The high-performance plotting library behind SciQLop (C++/Qt with Python bindings, `pip install SciQLopPlots`):
GPU-accelerated rendering, millions of points with fluid pan/zoom, time series, spectrograms, 2D histograms,
projection/trajectory plots and waterfalls. Built on [NeoQCP](https://github.com/SciQLop/NeoQCP), our
GPU-accelerated (QRhi) evolution of [QCustomPlot](https://www.qcustomplot.com/).

## File formats & metadata

- [CDFpp / pycdfpp](https://github.com/SciQLop/CDFpp) — a fast modern C++ (and Python) library to read and write
  NASA CDF files.
- [PyISTP](https://github.com/SciQLop/PyISTP) — ISTP-compliant abstraction on top of CDF files.

## Catalogs & collaboration

- [tscat](https://github.com/SciQLop/tscat) — time-series catalog storage and API.
- [cocat](https://github.com/SciQLop/cocat) — real-time collaborative catalog editing (CRDT over WebSocket),
  powering SciQLop's shared catalogs.

## Shared infrastructure

- [speasy_proxy](https://github.com/SciQLop/speasy_proxy) — a community caching proxy that speeds up data access
  for everyone; a public instance runs at
  [sciqlop.lpp.polytechnique.fr/cache](https://sciqlop.lpp.polytechnique.fr/cache/).
- [SciQLop-cache](https://github.com/SciQLop/Sciqlop-cache) — the multi-process-safe persistent cache (C++/SQLite)
  used by Speasy.

## And more

[AstraLint](https://github.com/SciQLop/AstraLint) (ISTP/PDS4 file validation),
[broni](https://github.com/SciQLop/broni) (orbit / region intersections),
[orbit-viewer](https://github.com/SciQLop/orbit-viewer) — browse the full list on the
[SciQLop GitHub organization](https://github.com/SciQLop).

## Citing

If you use these tools in your research, please cite them:

- **SciQLop**: [10.5281/zenodo.7379012](https://doi.org/10.5281/zenodo.7379012)
- **Speasy**: [10.5281/zenodo.4118780](https://doi.org/10.5281/zenodo.4118780)
