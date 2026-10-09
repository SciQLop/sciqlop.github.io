---
title: Python user API
---
# The Python user API

`SciQLop.user_api` is the public Python API of SciQLop. It is what you use from the embedded Jupyter notebooks,
from plugins, and what the in-app agents use too. With it you create plot panels, plot products, arrays or Python
functions, define your own products, edit catalogs and annotate plots.

This page is both a guide and a reference. It documents **SciQLop v0.13.1**. Features that only exist on the
development branch are marked with a "Next release" box.

Some topics have their own tutorial. This page links to them instead of repeating them:
[[Basic Plotting Workflow]], [[virtual products]], [[plot templates]], [[Catalogs]], [[Annotation layers]],
[[DSP toolbox]], [[2D histograms]] and [[Graphic primitives]].

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
See [Magics](#magics).

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

# Panels

A panel is a tab holding a stack of plots that share one time axis.

## Create, find, list, close

| Call | What it does |
|---|---|
| `create_plot_panel()` | Opens a new panel and returns its `PlotPanel`. |
| `plot_panel(name)` | Returns the panel with that tab name, or `None`. A non-string name raises `TypeError`. |
| `panel.name` | The panel's name, like `"Panel0"` (experimental). |
| `panel.close()` | Closes the panel cleanly (experimental). |
| `fluent.panel(name)` | A [fluent builder](#fluent-builder) over an existing panel. |

There is no `user_api` function that lists panels yet. Ask the main window, on the GUI thread:

```python
from SciQLop.user_api.gui import get_main_window
from SciQLop.user_api.threading import invoke_on_main_thread

names = invoke_on_main_thread(lambda: get_main_window().plot_panels())   # ['Panel0', 'Panel1']
p = plot_panel(names[0])
```

Panels are named `Panel0`, `Panel1`, … in creation order. `create_plot_panel()` takes no name.

> [!note] Next release
> - `create_plot_panel(name="Flux")` names the panel. If the name is taken, it is made unique.
> - `list_plot_panels()` returns the panel names. Pass one to `plot_panel(name)` to get the panel.

## Time, navigation and export

| Member | What it does |
|---|---|
| `panel.time_range` | Get or set the panel's time range. The setter moves every plot. |
| `panel.duration` | Get or set the duration text of the time-range bar (for example `"1h"`). |
| `panel.step_forward(n=1)` / `panel.step_backward(n=1)` | Move the time range by `n` steps, like the bar's arrows. |
| `panel.zoom_limit_seconds` | Widest time span allowed, in seconds. `0` means unlimited. |
| `panel.is_busy()` | `True` while a graph is still fetching data (experimental). |
| `panel.wait_for_data(timeout=10.0, poll_interval=0.1)` | Waits until nothing is fetching. Returns `False` on timeout (experimental). |
| `panel.save(path)` | Saves the panel as `.png`, `.pdf`, `.jpg`, `.jpeg` or `.bmp`, picked from the extension. |
| `panel.save_template(name_or_path)` | Saves the layout as a template. See [[plot templates]]. |

```python
p.time_range = TimeRange("2015-10-16T13:00", "2015-10-16T13:10")
if p.wait_for_data(timeout=30):
    p.save("/tmp/mms_crossing.png")
```

> [!tip] Wide time ranges
> A panel clips spans wider than `zoom_limit_seconds`. If you push a range of several days, raise the limit
> first, but only when a limit is set. `0` already means unlimited.
> ```python
> span = 7 * 86400
> if 0 < p.zoom_limit_seconds < span:
>     p.zoom_limit_seconds = span
> ```

> [!note] Next release
> `panel.settle(timeout=None)` waits until the panel shows its data: downloaded, drawn and rescaled. It raises
> `TimeoutError` after `timeout` seconds. `wait_for_data` now waits for the same thing, so an export right
> after it no longer shows the old axis range. To make images from a script with no window, see
> [[Batch quick-looks]].

`save_template("my_layout")` writes `my_layout.json` in the templates folder. A name with a `/` is used as a
file path instead.

## Managing the plots of a panel

| Member | What it does |
|---|---|
| `panel.plots` | The panel's plots, top to bottom, as `TimeSeriesPlot`, `XYPlot` or `ProjectionPlot`. |
| `panel.remove_plot(i)` | Removes plot `i`. Negative indices count from the end. The plots below slide up. |
| `panel.add_sub_panel(orientation=Orientation.Horizontal)` | Adds a nested panel and returns it as a `PlotPanel` (experimental). |

```python
p.plots[1].y_scale_type = ScaleType.Logarithmic
p.remove_plot(-1)     # drop the last plot
```

> [!note] Next release
> `panel.move_plot(from_index, to_index)` reorders plots. Negative indices count from the end.

# Plotting

## One entry point: `panel.plot`

`panel.plot(...)` looks at what you give it and calls the matching typed method.

| You pass | It calls | You get |
|---|---|---|
| a product path (`str`, list of `str`) or a `VirtualProduct` | `plot_product` | `(plot, graph)` |
| a `SpeasyVariable` | `plot_data` | `(plot, graph)` |
| arrays `(x, y)` or `(x, y, z)` | `plot_data` | `(plot, graph)` |
| a function `f(start, stop)` | `plot_function` | `(plot, graph)` |
| `(x, y, z)` with `graph_type=GraphType.Waterfall` | `waterfall` | `(plot, waterfall)` |

All of them take `plot_index`. It picks the plot that receives the new graph:

- `-1` (the default), or any index past the end, appends a **new** plot.
- An existing index draws **into** that plot, on top of what is there.

```python
DENSITY_BRST = "speasy//cda//MMS//MMS1//DIS//MMS1_FPI_BRST_L2_DIS_MOMS//mms1_dis_numberdensity_brst"

p.plot(DENSITY)                       # a new plot
p.plot(DENSITY_BRST, plot_index=0)    # drawn on the same axes as the first plot
```

Anything else `plot()` cannot read raises `ValueError: plot() could not interpret its arguments ...`.

## Plotting a product: `plot_product`

```python
plot, graph = p.plot_product(product, plot_index=-1, *, plot_type=PlotType.TimeSeries,
                             graph_type=GraphType.Line, product_inputs=None, **kwargs)
```

- `product` is a path or a `VirtualProduct`.
- `plot_type` and `graph_type` are the only display options that work here.
- `product_inputs` gives initial values to the product's parameters, the ones shown in the inspector. Unknown
  names are ignored.

The provider decides labels, the graph name and log scales. Passing `labels=` or a log-scale option for a product is
not supported. `labels=` raises `TypeError`.

An unknown path raises `ValueError: cannot plot product '...': not found in the products tree, or its provider is
unavailable`.

## Plotting arrays: `plot_data`

```python
plot, graph = p.plot_data(x, y=None, z=None, plot_index=-1, *, labels=None, name=None,
                          plot_type=PlotType.TimeSeries, graph_type=GraphType.Line,
                          colors=None, y_log_scale=False, z_log_scale=False,
                          line_style=None, **kwargs)
```

What gets drawn depends on the shapes:

| Data | Result |
|---|---|
| `x` 1-D, `y` 1-D | One line. |
| `x` 1-D, `y` 2-D `(len(x), n)` | `n` lines, one per column. |
| `x` 1-D, `y` 1-D, `z` 2-D `(len(x), len(y))` | A colormap (spectrogram). |
| a `SpeasyVariable` alone | Its time and values. With a numeric second axis, a colormap. |

Arrays are converted to `float64` for you. `numpy.datetime64` time arrays are converted to epoch seconds.

```python
import numpy as np

t = np.arange("2015-10-16T10:00", "2015-10-16T16:00", np.timedelta64(10, "s"), dtype="datetime64[ns]")
y = np.column_stack([np.sin(np.arange(t.size) / 100), np.cos(np.arange(t.size) / 100)])
plot, graph = p.plot_data(t, y, labels=["sin", "cos"], name="demo")
```

A colormap from arrays:

```python
energy = np.logspace(1, 4, 32)                    # must be ascending
flux = np.random.default_rng(0).random((t.size, energy.size))
plot, cmap = p.plot_data(t, energy, flux, y_log_scale=True, z_log_scale=True)
```

> [!warning] Colormap axes must be ascending
> Both `x` and `y` of a colormap must be sorted ascending. A descending energy table gives an empty or scrambled
> picture, not a flipped one. CDF energy tables are often stored high to low: flip `y` and the last axis of `z`.

## Plotting a Python function: `plot_function`

The function is called again every time the panel's time range changes.

```python
plot, graph = p.plot_function(f, plot_index=-1, *, labels=None, name=None,
                              plot_type=PlotType.TimeSeries, graph_type=GraphType.Line,
                              colors=None, y_log_scale=False, z_log_scale=False, **kwargs)
```

- `f(start, stop)` gets epoch seconds as floats.
- It returns `(x, y)` for lines, or `(x, y, z)` with `graph_type=GraphType.ColorMap` for a colormap.
- The number of lines comes from the returned data. `labels` only names them.
- `name` defaults to the function's name, unless it is a lambda.

```python
import speasy as spz

def b_total(start, stop):
    b = spz.get_data("cda/MMS1_FGM_SRVY_L2/mms1_fgm_b_gse_srvy_l2", start, stop)
    if b is None:
        return np.array([]), np.array([])
    t = b.time.astype("datetime64[ns]").astype("int64") / 1e9
    return t, b.values[:, 3]

plot, graph = p.plot_function(b_total, labels=["|B|"])
```

If the function raises, the error shows as a red message over the plot. It goes away on the next successful call.

> [!tip] Function or virtual product?
> `plot_function` lives in one panel only. A [virtual product](#virtual-products) appears in the Products tree,
> can be dragged anywhere, carries units and labels, and can be cached. Prefer a virtual product for anything you
> will reuse.

## Plot types and graph types

`plot_type` picks the kind of plot created. `graph_type` picks how the data is drawn.

| `PlotType` | Plot | X axis |
|---|---|---|
| `TimeSeries` (default) | `TimeSeriesPlot` | time, shared by the panel |
| `XY` | `XYPlot` | any quantity |
| `Projection` | `ProjectionPlot` | several 2-D projections of vector data |

| `GraphType` | Drawing |
|---|---|
| `Line` (default) | A line. X must be sorted, which allows fast drawing. |
| `Curve` | A parametric curve. X may go back and forth. |
| `ColorMap` | A colormap. |
| `Scatter` | Markers only. |
| `Waterfall` | Stacked lines, through `panel.plot(x, y, z, graph_type=GraphType.Waterfall)`. |

On an `XY` or `Projection` plot, `plot_product`, `plot_data` and `plot_function` always draw a `Curve`. The
`graph_type` you pass is replaced. For markers on an XY plot, use `plot.scatter(x, y)`.

> [!note] Next release
> The `graph_type` you pass is honoured: `p.plot_data(x, y, plot_type=PlotType.XY, graph_type=GraphType.Scatter)`
> draws markers. Without `graph_type`, XY and projection plots still draw a curve.

## Display options

These options are accepted by `plot_data`, `plot_function` and the `plot()` method of a plot. Always pass them by
keyword.

| Option | Effect |
|---|---|
| `labels=["Bx", "By", "Bz"]` | Legend names, one per component. |
| `name="b_gse"` | The graph's name. |
| `colors=[QColor("red"), ...]` | One colour per component. Defaults to the panel palette. |
| `y_log_scale=True` | Log Y scale. |
| `z_log_scale=True` | Log colour scale for a colormap. |
| `line_style=GraphLineStyle.Dash` | Dash pattern: `Solid`, `Dash`, `Dot`, `DashDot`, `DashDotDot`. Not on `plot_function`. |
| `y_axis="y2"` | Put the graph on the right-hand axis. Only on `plot.plot(...)`, and only for lines, curves and scatter. |
| `gradient=...` | Colour gradient of a colormap, passed through to SciQLopPlots. |

## Waterfalls

A waterfall stacks one line per row of a matrix.

```python
x = np.linspace(0, 10, 200)
y = np.linspace(0, 5, 12)
z = np.sin(x) * np.exp(-y[:, None])          # shape (len(y), len(x))
wf = p.waterfall(x, y, z, name="stack", offsets=1.0, gain=1.0, normalize=False, color="#1f77b4")
wf.gain = 2.0
```

`panel.waterfall(...)` (experimental) returns the `Waterfall` only. `XYPlot.waterfall(...)` and
`TimeSeriesPlot.waterfall(...)` add one to an existing plot. A wrong `z` shape raises `ValueError`.

## 2D histograms

`panel.histogram2d(...)` bins `(x, y)` samples into a density map, in a new XY plot.

```python
xy_plot, hist = p.histogram2d(x, y, name="histogram", x_bins=100, y_bins=100,
                              x_bin_strategy=BinStrategy.Linear, y_bin_strategy=BinStrategy.Linear,
                              z_log_scale=False, gradient=None, plot_index=-1)
```

Give it two arrays, or a function `f(start, stop) -> (x, y)` that follows the panel's time range. The full story is
in [[2D histograms]].

- `x_bins` and `y_bins` must be integers. Explicit bin edges raise `NotImplementedError` in v0.13.1.
- `BinStrategy.Log` works. `BinStrategy.SymLog` raises `NotImplementedError` in v0.13.1.
- More than 25 million cells, or fewer than one bin, raises `ValueError`.

> [!note] Next release
> A histogram fed by a function loads as soon as it is created. In v0.13.1 it stays empty until the time range
> changes. Set `p.time_range` after creating it.

# Plots

`panel.plots` and every `plot` call give you plot objects. `TimeSeriesPlot` and `XYPlot` share most of their
methods. `ProjectionPlot` is different.

## Common to time-series and XY plots

| Member | What it does |
|---|---|
| `plot.plot(...)` | Adds a graph to this plot. See below. |
| `plot.scatter(x, y, *, labels, name, colors, **kwargs)` | Adds a scatter graph, filled circles by default (experimental). |
| `plot.histogram2d(x, y, ...)` | Adds a 2D histogram to this plot (experimental). |
| `plot.waterfall(x, y, z, ...)` | Adds a waterfall to this plot (experimental). |
| `plot.add_hline(value, *, color=None, movable=False)` | Adds a horizontal line, returns a `HorizontalLine` (experimental). |
| `plot.remove_graph(graph)` | Removes a graph you got from `plot`, `scatter`, … (experimental). |
| `plot.set_x_range(lo, hi)` / `plot.set_y_range(lo, hi)` | Sets an axis range. Bounds are swapped if reversed. |
| `plot.y_scale_type` | `ScaleType.Linear` or `ScaleType.Logarithmic`. Settable. |
| `plot.set_axis_label(axis, label, unit=None)` | Labels `"x"`, `"y"`, `"y2"` or `"z"`. The unit shows as `label [unit]`. |
| `plot.set_axis_scale(axis, ScaleType.Logarithmic)` | Sets one axis to linear or log. |
| `plot.set_axis_range(axis, lo, hi)` | Sets one axis range. |
| `plot.set_axis_type(axis, AxisType.DateTime)` | `Linear`, `Logarithmic` or `DateTime`. |
| `plot.apply_hints(hints)` | Applies a `PlotHints` bundle (labels, units, scales) at once. |
| `plot.rescale_axes()` | Fits the axes to the visible data. Set the X or time range first. |
| `plot.replot()` | Forces a redraw. |
| `plot.overlay` | The plot's message overlay. See [Messages over a plot](#messages-over-a-plot). |
| `plot.plot_type` | `PlotType.TimeSeries` or `PlotType.XY`. |

The secondary Y axis on the right (experimental):

| Member | What it does |
|---|---|
| `plot.y2_visible` | Show or hide the right axis. |
| `plot.y2_scale_type` | Linear or log right axis. |
| `plot.set_y2_range(lo, hi)` | Right axis range. |
| `graph.y_axis = "y2"` | Move an existing line to the right axis. |

```python
from SciQLop.user_api.plot import ScaleType

b_plot, _ = p.plot(FGM)
_, n_graph = p.plot(DENSITY, plot_index=0)    # density on the same axes as B
n_graph.y_axis = "y2"                         # ... but against the right axis
b_plot.y2_visible = True
b_plot.y2_scale_type = ScaleType.Logarithmic
b_plot.set_y2_range(0.1, 100)
b_plot.set_axis_label("y", "B", "nT")
b_plot.set_axis_label("y2", "n", "cm^-3")
```

A plot has a single colour scale. Adding a second colormap, histogram or waterfall to the same plot raises
`RuntimeError`. Colormaps cannot live on `y2`; `y_axis="y2"` is ignored for them.

## `TimeSeriesPlot`

The X axis is time and it is shared with the whole panel.

```python
graph = ts_plot.plot(*args, labels=None, name=None, colors=None, graph_type=None,
                     y_log_scale=False, z_log_scale=False, line_style=None, y_axis="y", **kwargs)
```

It accepts a product path, a function `f(start, stop)`, `(x, y)` or `(x, y, z)`. It returns the graph only, not a
tuple. With a product path, `labels=` raises `TypeError`; `name=` works on every path.

| Member | What it does |
|---|---|
| `ts_plot.time_range` | Get or set this plot's time range. |
| `ts_plot.set_x_range(start, stop)` | Same as setting `time_range`, with any datetime-like bounds. |
| `ts_plot.set_y_scale_type(scale)` | Same as `y_scale_type = scale`. |

## `XYPlot`

Any quantity on both axes. You usually get one from `panel.histogram2d` or `plot_type=PlotType.XY`.

```python
graph = xy_plot.plot(x, y)          # a curve
cmap = xy_plot.plot(x, y, z)        # a colormap
graph = xy_plot.plot(f)             # a function f(start, stop) -> (x, y)
```

A product path is rejected here with `ValueError`. `xy_plot.x_scale_type` and `xy_plot.y_scale_type` set the
scales.

## `ProjectionPlot`

A projection plot draws vector data as several 2-D projections, one panel per pair of components. Give it a
three-component product, like a velocity or a spacecraft position.

```python
VI = "speasy//cda//MMS//MMS1//DIS//MMS1_FPI_FAST_L2_DIS_MOMS//mms1_dis_bulkv_gse_fast"
proj, graph = p.plot_product(VI, plot_type=PlotType.Projection)
proj.set_x_range(-500, 500)
proj.set_y_range(-500, 500)
```

| Member | What it does |
|---|---|
| `proj.plot(product)` | Adds a product. |
| `proj.set_x_range(lo, hi)` / `proj.set_y_range(lo, hi)` | Applies to every projection. |
| `proj.set_x_scale_type(scale)` / `proj.set_y_scale_type(scale)` | Applies to every projection. |
| `proj.set_axis_type(axis, axis_type)` | `axis` is `"x"` or `"y"`. |
| `proj.plot_time_colored_curve(x, y, t, *, z=None, name=None, colormap="viridis")` | A curve coloured by time (experimental). Needs one array per projection: pass `z` on a 3-projection plot. |

A projection plot has no `overlay`, no axis labels and no `y2` axis. That is by design: it is a different widget
from the other plots, a grid of 2-D projections, so those features don't exist there.

## Messages over a plot

Every time-series and XY plot has an `overlay` for in-canvas messages.

```python
from SciQLop.user_api.plot import OverlayLevel, OverlayPosition, OverlaySizeMode

b_plot.overlay.show("Burst data only after 13:00", level=OverlayLevel.Warning,
                    size_mode=OverlaySizeMode.FitContent, position=OverlayPosition.Top)
b_plot.overlay.collapsible = True
b_plot.overlay.clear()
```

`show` and `clear` are experimental. `text`, `level`, `position` and `size_mode` read the current message.
`collapsible`, `collapsed` and `opacity` are settable. Don't keep the overlay object: read `plot.overlay` again
each time.

# Graphs

The second value returned by `plot` calls is a graph handle. Its type depends on what was drawn.

| Type | Members |
|---|---|
| `Graph` (lines, curves, scatter) | `data`, `set_data(x, y)`, `visible`, `y_axis` |
| `ColorMap` | `data`, `set_data(x, y, z)`, `visible` |
| `Histogram2D` | `data`, `set_data(x, y)`, `visible`, `z_log_scale`, `gradient`, `x_bin_edges`, `y_bin_edges` |
| `Waterfall` | `data`, `set_data(x, y, z)`, `visible`, `offsets`, `gain`, `normalize`, `colors`, `color`, `line_count` |

```python
graph.visible = False
graph.set_data(t, y * 2)          # replace static data
x, y = graph.data
```

`set_data` replaces data you plotted from arrays. A graph fed by a product or a function gets new data on every
time range change.

Once its plot or panel is closed, a handle raises `ValueError: The graph does not exist anymore.` The same goes
for plots, panels and items.

## Colours and gradients

- Colours of primitives, waterfalls and overlays are Qt colour strings: a name like `"red"`, `"#RRGGBB"`, or
  `"#AARRGGBB"` for transparency. CSS `rgba(...)` is not understood.

> [!note] Next release
> Every plot item accepts CSS `rgb(...)` and `rgba(...)`: lines, spans, text, ellipses, curves, waterfall and
> timeline colours. A colour string SciQLop can't read raises `ValueError` instead of silently drawing nothing.

- `colors=` on plot calls takes one colour per component. `QColor` objects are the safe choice there.
- Gradients are `SciQLopPlots.ColorGradient` values, like `ColorGradient.Jet` or `ColorGradient.Thermal`.
  `hist.gradient = ColorGradient.Hot` sets one.
- In v0.13.1, a gradient given *by name* (`"hot"`) only works for `Candy`, `Cold`, `Hot` and `Polar`. Other names
  raise `ValueError`. Use the enum value.

> [!note] Next release
> Every gradient can be given by name: `hist.gradient = "thermal"`.

## Next release: timelines, steps and text ticks

> [!note] Next release
> These ship after v0.13.1.
>
> - **Step lines.** `plot_data(...)` and `plot.plot(...)` take `line_shape=LineShape.StepLeft` (also
>   `StepRight`, `StepCenter`, `Line`). `gap_threshold=0` stops a line graph from breaking at long flat
>   stretches. Both are also `Graph` properties. `from SciQLop.user_api.plot import LineShape`.
> - **Text ticks.** `plot.set_axis_tick_labels("y", {0: "MAG", -1: "SWA"})` shows names instead of numbers.
>   `None` restores the numbers.
> - **Legend.** `plot.legend_visible = False` hides a plot's legend.
> - **Listing graphs.** `plot.graphs` lists a plot's graphs in draw order. Every graph has a `name`.
>   `plot.remove_graph(plot.graphs[0])` removes the first one.
> - **Interval timelines** (experimental). `plot, tl = panel.add_timeline()` adds a plot of named lanes, and
>   `ts_plot.add_timeline()` adds a strip to an existing plot. Fill it with
>   `tl.set_intervals(start, stop, lane=[...], category=[...], label=[...], ids=[...])`. Times can be epoch
>   seconds, `datetime64`, datetimes or date strings. `tl.on_edit`, `on_create`, `on_delete`, `on_hover` and
>   `on_selection` report user actions back with your ids. Edits are proposals: the timeline only changes when
>   you call `set_intervals` again.
> - **Panel menus.** `register_panel_menu(title, entries)` adds a submenu to every panel's right-click menu.
>   `entries(panel)` returns `(label, callback)` pairs. `unregister_panel_menu(title)` removes it.

# Fluent builder

`fluent` builds a panel in one chained expression. Each call returns the builder.

```python
from SciQLop.user_api.plot import fluent

builder = (fluent.new_panel()
    .plot(FGM)
    .y_range(-75, 75)
    .subplot()
        .plot(DENSITY)
        .log_y()
        .y_range(0.1, 100)
    .time_range("2015-10-16T10:00", "2015-10-16T16:00"))

panel = builder.panel          # the underlying PlotPanel
```

| Method | What it does |
|---|---|
| `fluent.new_panel()` | Creates a panel and returns a builder. |
| `fluent.panel(name)` | A builder over an existing panel. Unknown name raises `ValueError`. |
| `.plot(*args, **kwargs)` | Same arguments as `PlotPanel.plot`. Adds to the current plot, or creates the first one. |
| `.subplot()` | The next `.plot()` starts a new plot. |
| `.histogram2d(*args, **kwargs)` | A 2D histogram in a new plot. |
| `.layer(func, **kwargs)` | Attaches an [annotation layer](#annotation-layers) to the current plot. |
| `.y_range(lo, hi)`, `.log_y()`, `.linear_y()` | Y axis of the current plot. |
| `.time_range(start, stop)` | The panel's time range. |
| `.panel` | The `PlotPanel` being built. |

Calling `.y_range()`, `.log_y()` or `.layer()` before any `.plot()` raises `RuntimeError`.

# Virtual products

A virtual product is a Python function that SciQLop calls for the visible time range. It shows in the Products
tree under the path you choose, and it plots like any other product. [[virtual products]] walks through a full
example.

## `create_virtual_product`

```python
vp = create_virtual_product(path, callback, product_type, labels=None,
                            debug=False, cachable=False,
                            knobs_model=None, knobs_kwarg_name="knobs",
                            display_name=None)
```

| Parameter | Meaning |
|---|---|
| `path` | Where it goes in the Products tree, like `"my_products//mms1//b_total"`. |
| `callback` | Your function `f(start, stop, ...)`. |
| `product_type` | A `VirtualProductType`. See the table below. |
| `labels` | Component names. How many depends on the type. |
| `debug` | `True` prints the callback's stack traces. Handy while writing it. |
| `cachable` | `True` tells SciQLop the function always returns the same data for the same range, so results can be cached. |
| `knobs_model` | A Pydantic model whose fields become knobs. The instance is passed as `knobs_kwarg_name`. |
| `display_name` | Name shown in the tree and on the plot. Used by spectrograms only in v0.13.1; by every type in the next release. |

| `VirtualProductType` | `labels` | Callback returns |
|---|---|---|
| `Scalar` | exactly 1 | `(t, y)` with `y` of shape `(N,)` or `(N, 1)`, or a `SpeasyVariable` |
| `Vector` | exactly 3 | `(t, y)` with `y` of shape `(N, 3)`, or a `SpeasyVariable` |
| `MultiComponent` | any number, at least 1 | `(t, y)` with `y` of shape `(N, n)`, or a `SpeasyVariable` |
| `Spectrogram` | ignored | `(t, y, z)` or a 2-D `SpeasyVariable` |

> [!note] Next release
> `labels` can come from the callback's return annotation. With `def f(start, stop) -> Scalar["|B|^2"]`,
> `create_virtual_product(path, f, VirtualProductType.Scalar)` needs no `labels=`. An explicit `labels=` still
> wins.

The result is a `VirtualProduct`. Pass it anywhere a product path is accepted: `p.plot(vp)`. Its `path` and
`product_type` are readable. Registering the same path again replaces the old product.

```python
import numpy as np
import speasy as spz
from speasy.products import SpeasyVariable
from SciQLop.user_api.virtual_products import create_virtual_product, VirtualProductType

def b_total(start: float, stop: float) -> SpeasyVariable | None:
    b = spz.get_data("cda/MMS1_FGM_SRVY_L2/mms1_fgm_b_gse_srvy_l2", start, stop)
    if b is None:
        return None
    return b["Bt"]

b_total_vp = create_virtual_product("my_products//mms1//b_total", b_total,
                                    VirtualProductType.Scalar, labels=["|B|"], cachable=True)
p.plot(b_total_vp)
```

## The callback contract

1. SciQLop calls the function with `start` and `stop`, the range to compute.
2. Their type follows your annotations. `float` (or no annotation) gives epoch seconds. `datetime` gives UTC
   datetimes. `np.datetime64` gives `datetime64[ns]`.
3. The function returns a `SpeasyVariable`, a tuple of arrays, or `None` for "no data".
4. The time axis you return can be `datetime64` or epoch seconds as `float64`.
5. The call runs on a worker thread, not the GUI thread. Compute and return data. Don't drive the GUI from there.

Returning a `SpeasyVariable` is the better choice. Its units, axis labels and scale reach the plot for free. Do
the maths on the `SpeasyVariable` itself, not on `.values`, so the time axis and units stay attached.

## Inputs with `Depends`

A callback can declare the products it needs. SciQLop fetches them for the same range and passes them in.

```python
from typing import Annotated
from speasy.products import SpeasyVariable
from SciQLop.user_api.virtual_products import Depends, create_virtual_product, VirtualProductType

FGM_DS = "speasy//cda//MMS//MMS1//FGM//MMS1_FGM_SRVY_L2"

def b_squared(start: float, stop: float,
              b: Annotated[SpeasyVariable, Depends(FGM_DS + "//mms1_fgm_b_gse_srvy_l2", pad=30.0)],
              ) -> SpeasyVariable | None:
    return None if b is None else b["Bt"] ** 2

create_virtual_product("my_products//mms1//b_squared", b_squared,
                       VirtualProductType.Scalar, labels=["|B|^2"])
```

- The target can be a product path, a `VirtualProduct`, or a function `f(start, stop)`.
- `pad` widens the fetched range on both sides, in seconds or as a `timedelta`.
- Dependencies are always resolved with epoch-second bounds.

## Knobs: parameters you can tune

Keyword arguments with a default become **knobs**. You tune them in the inspector, and the product is
recomputed. See [Knobs](#knobs) for the full list.

```python
from typing import Annotated, Literal
from SciQLop.user_api.knobs import Knob

COLUMN = {"Bx": 0, "By": 1, "Bz": 2}

def smoothed(start: float, stop: float,
             window: Annotated[int, Knob(min=1, max=200, step=1, label="Window", unit="samples")] = 10,
             component: Literal["Bx", "By", "Bz"] = "Bx"):
    b = spz.get_data("cda/MMS1_FGM_SRVY_L2/mms1_fgm_b_gse_srvy_l2", start, stop)
    if b is None:
        return None
    y = np.convolve(b.values[:, COLUMN[component]], np.ones(window) / window, mode="same")
    return b.time, y

create_virtual_product("my_products//mms1//b_smoothed", smoothed,
                       VirtualProductType.Scalar, labels=["B smoothed"])
```

The names `start`, `stop` and `data` are reserved and never become knobs.

## From a notebook cell: `%%vp`

The `%%vp` cell magic registers the function defined in the cell. Re-running the cell hot-reloads it: open plots
use the new code on their next fetch.

```python
%%vp --path "my_products/sine" --debug --start "2020-01-01" --stop "2020-01-02"
import numpy as np

def sine(start: float, stop: float, frequency: float = 0.01) -> Scalar["sin"]:
    t = np.arange(start, stop, 5.0)
    return t, np.sin(2 * np.pi * frequency * (t - start))
```

- `Scalar`, `Vector`, `MultiComponent` and `Spectrogram` are injected into the cell. Annotate the return with
  them: `-> Vector["Bx", "By", "Bz"]`.
- Without an annotation, the magic calls the function once and guesses the type from the result.
- The cell must define exactly one public function. Name helpers with a leading `_`.
- Options: `--path` (defaults to the function name), `--debug` (opens a debug panel), `--start` / `--stop`
  (the test range), `--cachable`.

## Other helpers

| Name | What it does |
|---|---|
| `VirtualScalar`, `VirtualVector`, `VirtualMultiComponent`, `VirtualSpectrogram` | The classes behind `create_virtual_product`. Their constructors also take `out_of_process=True`. |
| `SciQLop.user_api.virtual_products.fspeasy` | `get_data`, `lift`, `pipeline`: a `speasy.get_data` that returns `Something`/`Nothing` instead of `None`, for chained pipelines. |

> [!note] Next release
> - `list_virtual_products()` returns the `//` paths of every registered virtual product.
> - A virtual product can colour its line by a scalar. Return `Colored(data, color=c)` with one value per
>   sample, and register with `create_virtual_product(..., colored=True, color_label="|B| (nT)",
>   color_gradient="thermal")`. In a `%%vp` cell, annotate `-> Colored[Vector["X", "Y", "Z"]]`. Not for
>   spectrograms.
> - `cachable=True` products fetch half a view extra on each side, so small pans need no new fetch.
> - `%%vp` understands return annotations written under `from __future__ import annotations`.

# Knobs

Knobs are tunable parameters of virtual products and annotation layers. SciQLop builds them from the callback's
keyword arguments.

| Keyword argument | Knob | Inspector widget |
|---|---|---|
| `n: int = 10` | `IntKnob` | spin box |
| `x: float = 0.5` | `FloatKnob` | spin box |
| `flag: bool = True` | `BoolKnob` | check box |
| `mode: Literal["a", "b"] = "a"` | `ChoiceKnob` | drop-down |
| `name: str = "x"` | `StringKnob` | text field |
| `w: SciQLopPlotRange = SciQLopPlotRange(0.3, 0.7)` | `TimeRangeKnob` | a draggable span on the plot |
| `level: Annotated[float, Knob(widget="hline")] = 1.0` | `ThresholdKnob` | a draggable horizontal line |

Wrap the type in `Annotated[..., Knob(...)]` to add details:

```python
Knob(min=None, max=None, step=None, label="", unit="", description="",
     apply="live", choices=None, pattern="", widget="", color="")
```

| Field | Meaning |
|---|---|
| `min`, `max`, `step` | Bounds and increment. |
| `label`, `unit`, `description` | Text shown in the inspector. |
| `apply` | `"live"` recomputes on every change. `"manual"` waits for you to apply. |
| `choices` | A list of values, or `(label, value)` pairs, for a drop-down. |
| `pattern` | A regular expression a string knob must match. |
| `widget` | `"vspan"` for a time span, `"hline"` for a horizontal line. |
| `color` | Colour of the span or line on the plot. |

A time-span knob given a default between 0 and 1, like `SciQLopPlotRange(0.3, 0.7)`, starts as that fraction of
the visible range. Import `SciQLopPlotRange` from `SciQLop.user_api.knobs`.

`DatetimeKnob` and `StringListKnob` are exported too, but only catalog attribute editing uses them. A callback's
keyword arguments never produce them.

> [!note] Next release
> - `Annotated[float, Knob(widget="vline")] = 0.5` is a **time cursor**: a draggable vertical line. The callback
>   gets its time in epoch seconds. A default between 0 and 1 is a fraction of the visible range.
> - `Knob(scope="plot")` keeps a span or cursor on the product's own plot. The default, `"panel"`, draws it on
>   every plot of the panel.

# Annotation layers

A layer is a function that returns `Marker`, `Span` and `HLine` objects. SciQLop draws them over a plot and
re-runs the function when the time range or the data changes. [[Annotation layers]] has a full example.

```python
from SciQLop.user_api.layers import register_layer, Span, Scalar

@register_layer("detectors/dense", scope="auto")
def dense(data: Scalar, threshold: float = 10.0) -> list[Span]:
    above = data.values[:, 0] > threshold
    return [Span(start=float(t), stop=float(t) + 4.5, color="#e67e22") for t in data.time[above]]

renderer = p.add_layer(dense, plot_index=1, scope="panel", threshold=8.0)
```

| Name | What it does |
|---|---|
| `register_layer(path=None, scope="auto")` | Decorator. Puts the function in the Products tree under `Layers/`. |
| `panel.add_layer(func, plot_index=0, scope="auto", **initial_knobs)` | Attaches a layer to one plot (experimental). Returns its renderer, with `last_error` and a `callback_failed` signal. |
| `Marker(time, value, label=None, color=None, meta={})` | A point. |
| `Span(start, stop, label=None, color=None, meta={})` | A shaded time interval. |
| `HLine(value, label=None, color=None, meta={})` | A horizontal line. |
| `Scalar`, `Vector`, `MultiComponent`, `Spectrogram` | Type hints for the `data` argument of a data-aware layer. `data.time` and `data.values` hold the graph's data. |

- A layer `f(start, stop, **knobs)` follows the time range.
- A layer `f(data: Vector, **knobs)` reads the data of the matching graph on the plot.
- `scope="panel"` draws spans on every plot of the panel. `"plot"` keeps them on one plot. `"auto"` picks
  `"plot"` for data-aware layers and `"panel"` for the others. Markers and lines always stay on one plot.
- The `%%layer` cell magic does the same as `register_layer`, with hot reload. Options: `--path`, `--scope`.

# Catalogs

`catalogs` creates, reads and edits event catalogs. [[Catalogs]] shows the GUI side and a full example.

Catalog paths look like product paths: `"provider//sub//folder//name"`. The first segment is the provider.
`"My Catalogs"` is the local store you see in the Catalogs tab.

| Call | What it does |
|---|---|
| `catalogs.list(prefix=None)` | All catalog paths, or those under a provider or folder. |
| `catalogs.get(path)` | The catalog as a `speasy.Catalog`. |
| `catalogs.save(path, events)` | Creates the catalog if needed, then replaces all its events. |
| `catalogs.create(path, events)` | Creates a new catalog. Raises `ValueError` if it exists. |
| `catalogs.add_events(path, events)` | Appends events. |
| `catalogs.remove_events(path, events)` | Removes events you got from `get()`, or UUID strings. |
| `catalogs.remove(path)` | Deletes the catalog. |

`events` is a `speasy.Catalog`, or a list of `(start, stop)` or `(start, stop, {"meta": "data"})` tuples. Any
datetime-like bound works.

```python
from SciQLop.user_api.catalogs import catalogs

catalogs.save("My Catalogs//crossings", [
    ("2015-10-16T13:05:40", "2015-10-16T13:06:00", {"label": "magnetopause"}),
    ("2015-10-16T13:07:00", "2015-10-16T13:07:05"),
])
cat = catalogs.get("My Catalogs//crossings")
catalogs.remove_events("My Catalogs//crossings", [cat[1]])
```

Changes show in SciQLop right away. Press **Save** in the Catalogs tab to write them to disk.

Showing a catalog on a panel (experimental):

```python
overlay = p.add_catalog_overlay("My Catalogs//crossings", override_color="#50FF8800")
overlay.remove()           # or p.remove_catalog_overlay(overlay)
```

`override_color` is a Qt colour string. Give it transparency (`#AARRGGBB`), or it hides the data underneath.

> [!note] Next release
> `add_catalog_overlay(..., show_spans=False)` attaches a catalog without drawing its events. Jump mode still
> moves the panel to them. `overlay.show_spans` toggles it later.

# Graphic primitives

Static marks on one plot: text, arrows, lines, spans, ellipses, images. They follow the plot when you pan or zoom.
[[Graphic primitives]] has a worked example.

| Class | Signature |
|---|---|
| `Text` | `Text(plot, text, x, y, *, color=None, font_size=None, font_family=None, coordinate_system=Data)` |
| `CurvedLine` | `CurvedLine(plot, start=(x, y), stop=(x, y), *, color=None, line_width=None, line_style=None, start_termination=NoneTermination, stop_termination=Arrow, start_direction=None, stop_direction=None, coordinate_system=Data)` |
| `HorizontalLine` | `HorizontalLine(plot, value, *, color=None, movable=False)`. Black by default; next release: the theme's text colour, plus `visible` and `remove()` |
| `VerticalLine` | `VerticalLine(plot, value, *, color=None, line_width=None, line_style=None, coordinate_system=Data, movable=False)` |
| `StraightLine` | `StraightLine(plot, x1, y1, x2, y2, *, color=None, line_width=None, line_style=None, coordinate_system=Data, movable=False)` |
| `RectangularSpan` | `RectangularSpan(plot, x1, y1, x2, y2, *, color=None, borders_color=None, line_width=None, line_style=None, read_only=False, visible=True, tool_tip="")` |
| `HorizontalSpan` | `HorizontalSpan(plot, y1, y2, *, color=None, borders_color=None, line_width=None, line_style=None, read_only=False, visible=True, tool_tip="")` |
| `Ellipse` | `Ellipse(plot, x, y, width, height, *, line_color=None, line_width=None, line_style=None, fill_color=None, coordinate_system=Data, tool_tip="")` |
| `Pixmap` | `Pixmap(plot, x, y, width, height, image, coordinate_system=Data)` with `image` a path, bytes or `QPixmap` |

- On a time-series plot, X in data coordinates is epoch seconds.
- **Keep a reference** to each item. An item created as a bare statement is garbage-collected and disappears.
- `del item` or `item.remove()` erases it.
- `StraightLine` only draws horizontal or vertical lines. Diagonal end points are turned into the closest one.

```python
from datetime import datetime, timezone
from SciQLop.user_api.plot import Text, VerticalLine

t0 = datetime(2015, 10, 16, 13, 5, 45, tzinfo=timezone.utc).timestamp()
marks = [VerticalLine(b_plot, t0, color="#e74c3c"),
         Text(b_plot, "magnetopause", t0 + 2, 35, color="#e74c3c")]
```

# DSP

`SciQLop.user_api.dsp` filters and transforms `SpeasyVariable`s and handles data gaps. All its functions are
experimental. [[DSP toolbox]] explains them with examples.

| Function | What it does |
|---|---|
| `filtfilt(data, coeffs, *, gap_factor=3.0, has_gaps=True)` | Zero-phase FIR filter. |
| `sosfiltfilt(data, sos, *, gap_factor=3.0, has_gaps=True)` | Zero-phase IIR filter (second-order sections). |
| `fir_filter(data, coeffs, *, gap_factor=3.0)` | Single-pass FIR filter. |
| `iir_sos(data, sos, *, gap_factor=3.0)` | Single-pass IIR filter. |
| `interpolate_nan(data, *, max_consecutive=1)` | Fills short NaN runs. |
| `rolling_mean(data, window, *, gap_factor=3.0)` | Rolling mean over `window` samples. |
| `rolling_std(data, window, *, gap_factor=3.0)` | Rolling standard deviation. |
| `resample(data, *, target_dt=0.0, gap_factor=3.0)` | Uniform time grid. |
| `reduce(data, op, *, gap_factor=3.0)` | Collapses the columns, for example `op="norm"`. |
| `reduce_axes(data, shape, axes, *, op="sum", has_gaps=False)` | Reduces chosen axes within each row. |
| `split_segments(data, *, gap_factor=3.0)` | One `SpeasyVariable` per continuous segment. |
| `fft(data, *, gap_factor=3.0, window="hann")` | A list of `(freqs, magnitude)` tuples, one per segment. |
| `spectrogram(data, *, col=0, window_size=256, overlap=0, gap_factor=3.0, window="hann")` | A list of 2-D `SpeasyVariable`s, one per segment. |
| `background_subtract(data, *, q=50.0, window=None, mode="diff", gap_factor=3.0)` | Removes a per-channel background from a spectrogram. |

These functions take a `SpeasyVariable` and raise `TypeError` for plain arrays. For arrays, use the same names in
`dsp.arrays`, which take `(x, y, ...)`.

# Magics

| Magic | Usage | What it does |
|---|---|---|
| `%%vp` | options `--path P`, `--debug`, `--start S --stop S`, `--cachable` | Registers the cell's function as a virtual product. |
| `%%layer` | options `--path P`, `--scope` (`auto`, `panel` or `plot`) | Registers the cell's function as an annotation layer. |
| `%plot` | `%plot <product> [panel]` | Plots a product, fuzzy-matched, in a new or named panel. |
| `%timerange` | `%timerange` / `%timerange <panel>` / `%timerange <start> <stop> <panel>` | Prints or sets panel time ranges. |
| `%install` | `%install astropy "scipy>=1.11"` | Installs packages in the workspace and records them. |
| `%workspace` | `%workspace status\|deps\|install\|plugins\|examples\|add-example\|help` | Inspects and manages the workspace. |
| `%job` | `%job submit [--name N] <command>` / `status <id>` / `list` / `cancel <id>` | Runs shell commands as background jobs. |

Panel names with spaces must be quoted. Panels are named `Panel0`, `Panel1`, …

# Other modules

| Module | Functions |
|---|---|
| `SciQLop.user_api.templates` | `load(name_or_path)`, `list_templates()`, `delete(name)`, `rename(old, new)`. See [[plot templates]]. |
| `SciQLop.user_api.themes` | `apply_theme(name)`, `current_theme()`, `list_themes()`. Names: `light`, `dark`, `neutral`, `space`, `github_light`, `nord_light`, `catppuccin_latte`, `high_contrast_light`. |
| `SciQLop.user_api.screenshot` | `capture_window(path)`, `capture_panel(panel, path)` (experimental). Both create missing folders. |
| `SciQLop.user_api.gui` | `get_main_window()`, `show_product_tree()`, `show_inspector()` (the last two experimental). |
| `SciQLop.user_api.packages` | `install_packages(*specs)`: what `%install` uses. Returns a dict with `ok`, `installed`, `already_present`, `error`. |
| `SciQLop.user_api.jobs` | `submit_job(command, name="")`, `job_status(id)`, `list_jobs()`, `cancel_job(id)`. Jobs survive closing SciQLop. |
| `SciQLop.user_api.diagnostics` | `dump_now(...)`, `hot_threads(pid)` and friends, for a SciQLop that feels stuck. |
| `SciQLop.user_api.tracing` | Performance traces. See below. |

## Tracing

`tracing` records what SciQLop does, with timings, into a file you open in [Perfetto](https://ui.perfetto.dev/).

```python
from SciQLop.user_api import tracing

with tracing.session("/tmp/slow_pan.json"):
    p.time_range = TimeRange("2015-10-16T00:00", "2015-10-17T00:00")
# open /tmp/slow_pan.json in https://ui.perfetto.dev/
```

| Name | What it does |
|---|---|
| `session(path)` | Records for the duration of a `with` block. |
| `enable(path)` / `disable()` / `flush()` / `is_enabled()` | Manual control. |
| `zone(name, cat="", **args)` | Marks a block of your own code in the trace. |
| `traced(name=None, cat="", capture=())` | Decorator: marks every call of a function. `capture=("start", "stop")` records those arguments. |
| `counter(name, value, cat="")` | Records a value over time. |
| `async_begin(name, cat="")` / `async_end(handle)` | Marks work that starts and ends in different places. |
| `set_thread_name(name)` | Names the current thread in the trace. |

Setting `SCIQLOP_TRACE=/tmp/trace.json` before starting SciQLop records from the very start.

```python
@tracing.traced(capture=("start", "stop"))
def b_total(start: float, stop: float):
    ...
```

# Threading rules

SciQLop's window runs on one thread, the GUI thread. Your notebook cells run on another, the kernel thread. Qt
objects must only be touched from the GUI thread.

1. You call a `user_api` function from a cell.
2. The function sends the work to the GUI thread and waits for it to finish.
3. You get the result back in your cell, as if the call were local.

So `user_api` calls are safe from cells, plugins and agents. A few rules keep it that way:

- **Go through `user_api`.** Don't import `SciQLopPlots` or Qt objects to change plots, and don't call methods on
  them in a loop.
- **Never touch `_impl`.** It is the raw Qt object behind a wrapper. Calling it from a cell can crash SciQLop.
- **Data callbacks run on worker threads.** Virtual products, `plot_function` callbacks, histogram callbacks and
  layers compute data and return it. They should not drive the GUI.
- **For your own Qt code**, use `SciQLop.user_api.threading`:

```python
from SciQLop.user_api.gui import get_main_window
from SciQLop.user_api.threading import on_main_thread, invoke_on_main_thread

@on_main_thread
def my_helper(widget):
    widget.setWindowTitle("Analysis")      # runs on the GUI thread

title = invoke_on_main_thread(lambda: get_main_window().windowTitle())
```

`on_main_thread` is a decorator. It does nothing when you are already on the GUI thread. `invoke_on_main_thread`
runs one call there and returns its result. The preloaded `app` and `main_window` are already wrapped this way.

> [!note] Next release
> Outside the GUI thread, a wrapper's `_impl` becomes a proxy that forwards each call to the GUI thread. Code that
> reaches into `_impl` stops crashing. It is still internal API.

# Common errors

Misuse raises a clear exception instead of failing silently. The messages you are most likely to meet:

| Exception | Message starts with | Cause |
|---|---|---|
| `ValueError` | `cannot plot product '...': not found in the products tree` | Wrong path, or the provider is not available. |
| `ValueError` | `invalid product ...` | Empty path, `None`, a number. |
| `ValueError` | `plot() could not interpret its arguments` | `plot()` got something it can't plot. |
| `ValueError` | `y data is required unless x is a SpeasyVariable` | `plot_data(x)` with plain arrays. |
| `ValueError` | `scalar (0-d) data is not plottable` | A single number instead of an array. |
| `ValueError` | `complex data is not plottable` | Take `.real`, `.imag` or `np.abs()` first. |
| `ValueError` | `time range bounds must be finite` | A NaN or infinite bound. |
| `ValueError` | `zero-width time range` | `start == stop`. |
| `TypeError` | `expected a TimeRange or a (start, stop) pair` | A single string or date given as a range. |
| `ValueError` | `zero-width y-axis range` | `set_y_range(1, 1)` and friends. |
| `ValueError` | `axis 'w' not available on this plot` | Axis names are `"x"`, `"y"`, `"y2"`, `"z"`. |
| `IndexError` | `plot_index 5 out of range (0..2)` | `remove_plot` or `add_layer` on a plot that doesn't exist. |
| `ValueError` | `The plot panel does not exist anymore.` | The panel was closed. Same for plots, graphs and items. |
| `ValueError` | `Unsupported format '.svg'` | `save()` only writes png, pdf, jpg, jpeg and bmp. |
| `OSError` | `failed to save ...` | The folder doesn't exist or is not writable. |
| `ValueError` | `zoom_limit_seconds must be >= 0` | Negative zoom limit. |
| `TypeError` | `panel name must be a str` | `plot_panel(0)`. |
| `RuntimeError` | `this plot already contains a colormap-style plottable` | A second colormap, histogram or waterfall in one plot. |
| `ValueError` | `histogram bins must be >= 1` / `exceeds the 25,000,000-cell sanity cap` | Bad bin counts. |
| `ValueError` | `unknown gradient 'viridis'` | A gradient name that doesn't exist (or isn't readable by name in v0.13.1). |
| `TypeError` | `line_style must be a GraphLineStyle` | A Qt pen style or string passed as `line_style`. |
| `ValueError` | `Scalar virtual products need exactly one label` | `labels` doesn't fit the product type. |
| `TypeError` | `product_type must be a VirtualProductType` | A string like `"scalar"` instead of the enum. |
| `ValueError` | `virtual product path must be a non-empty product-tree path` | Empty path or empty segment. |
| `KeyError` | `Catalog not found` / `Provider not found` | Wrong catalog path. |
| `PermissionError` | `Provider '...' cannot create catalogs` | Read-only provider, like `Remote`. |
| `ValueError` | `event start must be before stop` | An event with `start > stop`. |
| `TypeError` | `filtfilt(data, coeffs, ...) requires a SpeasyVariable` | Plain arrays given to `dsp`. Use `dsp.arrays`. |

When a data callback fails, the error is not raised in your cell: the callback runs later, on a worker thread.
Look for the red message over the plot. For layers, read `renderer.last_error`.

# What changes in the next release

Everything marked "Next release" on this page, in one list:

- `PlotPanel.move_plot`, `plot.graphs`, `graph.name`, `plot.legend_visible`.
- `LineShape`, `line_shape=` and `gap_threshold=` for step and state data.
- `plot.set_axis_tick_labels` for text ticks.
- Interval timelines: `panel.add_timeline`, `TimeSeriesPlot.add_timeline`, `Timeline`, `Interval`,
  `IntervalEdit`.
- `register_panel_menu` and `unregister_panel_menu`.
- All colour gradients by name.
- Histograms fed by a function load right away.
- `list_virtual_products()`, `Colored` virtual products, wider fetches for `cachable=True`.
- Time cursors (`Knob(widget="vline")`, `CursorKnob`) and `Knob(scope=...)`.
- `add_catalog_overlay(..., show_spans=False)` and `CatalogOverlay.show_spans`.
- `_impl` proxied outside the GUI thread.
- `create_plot_panel(name=...)` and `list_plot_panels()`.
- Enums importable from `SciQLop.user_api.plot`.
- `graph_type` honoured on XY and projection plots.
- CSS `rgb()`/`rgba()` colours everywhere; unreadable colours raise `ValueError`.
- Virtual product `labels` read from the return annotation; `display_name` for every type.
- `HorizontalLine` follows the theme and gets `visible` and `remove()`.

More examples live in the tutorial notebooks bundled with SciQLop (open them from the welcome page) and in the
[examples folder](https://github.com/SciQLop/SciQLop/tree/main/SciQLop/examples) of the repository.
