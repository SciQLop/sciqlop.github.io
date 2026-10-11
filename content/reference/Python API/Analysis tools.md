---
title: Analysis tools
---
# Annotation layers

A layer is a function that returns `Marker`, `Span` and `HLine` objects. SciQLop draws them over a plot and
re-runs the function when the time range or the data changes. [[guides/Annotation layers|Annotation layers]] has a full example.

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
[[guides/Graphic primitives|Graphic primitives]] has a worked example.

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
experimental. [[guides/DSP toolbox|DSP toolbox]] explains them with examples.

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

