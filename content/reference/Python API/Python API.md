---
title: Python API
aliases:
  - tutorials/Python-user-API
---
`SciQLop.user_api` is the public Python API of SciQLop. It is what you use from the embedded Jupyter notebooks,
from plugins, and what the in-app agents use too. With it you create plot panels, plot products, arrays or Python
functions, define your own products, edit catalogs and annotate plots.

These pages are both a guide and a reference. They document **SciQLop v0.13.1**. Features that only exist on
the development branch are marked with a "Next release" box.

This page covers the basics: where your code runs, the imports, product paths and time ranges. The rest is split
by topic:

- [[Panels]]: create, find and close panels; time, navigation and export.
- [[Plotting]]: `panel.plot` and its variants, plot and graph types, waterfalls, histograms, the fluent builder.
- [[Plots and graphs]]: axes, scales, legends, messages over a plot, graph colours.
- [[Virtual products and knobs]]: your own products, their inputs and tunable parameters.
- [[Analysis tools]]: annotation layers, catalogs, graphic primitives and DSP in short, each pointing to its user guide.
- [[Magics and tracing]]: notebook magics, tracing and the other modules.
- [[Threading and common errors]]: what runs where, and the errors you are likely to meet.
- [[Next release API changes]]: what changes on the development branch.

Some topics have a tutorial or a user guide, which these pages link to instead of repeating:
[[Basic Plotting Workflow]], [[virtual products]], [[plot templates]], [[Catalogs]], [[guides/Annotation layers|Annotation layers]],
[[guides/DSP toolbox|DSP toolbox]], [[guides/2D histograms|2D histograms]] and [[guides/Graphic primitives|Graphic primitives]].

> [!info] Stable or experimental?
> Everything under `SciQLop.user_api` is public. Some functions are marked *experimental* in the code: their
> signature may still change. They are flagged "(experimental)" in the tables below. Anything outside
> `SciQLop.user_api` (`SciQLop.components`, `SciQLopPlots`, any `_impl` attribute) is internal and can change at
> any release.

# Getting started

## Where the code runs

Open a notebook from the welcome page. Its kernel runs inside SciQLop, so your cells drive the application
directly. Nothing is imported for you, except a few variables and the magics.

The kernel preloads these names:

| Name | What it is |
|---|---|
| `app` | The SciQLop application object, wrapped for safe use from a cell. |
| `main_window` | The main window, wrapped the same way. |
| `workspace` | The active workspace. |
| `plugins` | The loaded plugins. |
| `background_run` | `await background_run(f, *args)` runs `f` on a worker thread and returns its result. |

It also registers the `%%vp`, `%%layer`, `%plot`, `%timerange`, `%install`, `%workspace` and `%job` magics.
See [[Magics and tracing#Magics|Magics]].

## Imports cheat sheet

```python
from SciQLop.user_api import TimeRange                     # also: dsp, tracing, themes
from SciQLop.user_api.plot import (
    create_plot_panel, plot_panel, PlotPanel,              # panels
    TimeSeriesPlot, XYPlot, ProjectionPlot,                # plots
    PlotType, ScaleType, Histogram2D, Waterfall,           # types
    Text, CurvedLine, Ellipse, Pixmap, HorizontalLine,     # graphic primitives
    VerticalLine, StraightLine, RectangularSpan, HorizontalSpan, LineTermination,
    OverlayLevel, OverlaySizeMode, OverlayPosition,        # in-plot messages
    fluent,                                                # chainable panel builder
)
from SciQLop.user_api.plot.enums import (GraphType, GraphLineStyle, BinStrategy,
                                         AxisType, CoordinateSystem, Orientation)
from SciQLop.user_api.virtual_products import create_virtual_product, VirtualProductType, Depends
from SciQLop.user_api.knobs import Knob
from SciQLop.user_api.layers import register_layer, Marker, Span, HLine
from SciQLop.user_api.catalogs import catalogs
from SciQLop.user_api import dsp
```

> [!note] Where the enums live
> `GraphType`, `GraphLineStyle`, `BinStrategy`, `AxisType`, `CoordinateSystem` and `Orientation` are not
> re-exported by `SciQLop.user_api.plot`. Import them from `SciQLop.user_api.plot.enums`.
>
> **Next release:** they can be imported from `SciQLop.user_api.plot` too.

## A first panel

```python
from SciQLop.user_api import TimeRange
from SciQLop.user_api.plot import create_plot_panel

FGM = "speasy//cda//MMS//MMS1//FGM//MMS1_FGM_SRVY_L2//mms1_fgm_b_gse_srvy_l2"
DENSITY = "speasy//cda//MMS//MMS1//DIS//MMS1_FPI_FAST_L2_DIS_MOMS//mms1_dis_numberdensity_fast"

p = create_plot_panel()
p.time_range = TimeRange("2015-10-16T10:00", "2015-10-16T16:00")
b_plot, b_graph = p.plot(FGM)       # new plot at the bottom of the panel
n_plot, n_graph = p.plot(DENSITY)   # another new plot
```

![[api_first_panel.png]]

Each `plot` call returns two handles: the **plot** (one set of axes) and the **graph** drawn in it. Keep them to
change the plot later.

# Product paths

A product path is the path of a product in the Products tree, from the provider down to the leaf.

- Segments are joined with `//`: `"speasy//cda//MMS//MMS1//FGM//MMS1_FGM_SRVY_L2//mms1_fgm_b_gse_srvy_l2"`.
- `//` is needed because a product name may itself contain a `/` (AMDA has some).
- A path with no `//` at all is split on `/`. So `"speasy/cda/MMS/MMS1/..."` also works, as long as no name
  contains a `/`.
- The segments are the **display names** of the tree, not Speasy ids.
- A list of segments works too: `["speasy", "cda", "MMS", ...]`.

The easy way to get a path: drag a product from the Products tree and drop it into a notebook cell.

> [!tip] Speasy paths are different
> Inside your own callbacks you call Speasy directly, and Speasy has its own path format:
> `spz.get_data("cda/MMS1_FGM_SRVY_L2/mms1_fgm_b_gse_srvy_l2", start, stop)`. Don't mix the two.

# Time ranges

`TimeRange(start, stop)` is the type every time range uses.

| You pass | It means |
|---|---|
| `"2015-10-16T10:00"` | A date string, parsed as UTC. Garbage raises `ValueError`. |
| `datetime(2015, 10, 16, 10)` | A datetime, taken as UTC. |
| `1444989600.0` | Seconds since 1970-01-01 UTC. |

```python
from datetime import datetime
from SciQLop.user_api import TimeRange

tr = TimeRange("2015-10-16T10:00", datetime(2015, 10, 16, 16))
tr.start(), tr.stop()          # epoch seconds, as methods
p.time_range = tr
p.time_range = ("2015-10-16T10:00", "2015-10-16T16:00")   # a (start, stop) pair works too
```

A single string is not a range. `p.time_range = "2015-10-16"` raises `TypeError`.

> [!warning] `numpy.datetime64` bounds
> `TimeRange` converts strings and `datetime` objects itself. Other values go straight to the C++ range type.
> Convert `numpy.datetime64` values to epoch seconds first:
> `t.astype("datetime64[ns]").astype("int64") / 1e9`.

