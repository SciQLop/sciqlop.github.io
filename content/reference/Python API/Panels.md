---
title: Panels
---
A panel is a tab holding a stack of plots that share one time axis.

## Create, find, list, close

| Call | What it does |
|---|---|
| `create_plot_panel()` | Opens a new panel and returns its `PlotPanel`. |
| `plot_panel(name)` | Returns the panel with that tab name, or `None`. A non-string name raises `TypeError`. |
| `panel.name` | The panel's name, like `"Panel0"` (experimental). |
| `panel.close()` | Closes the panel cleanly (experimental). |
| `fluent.panel(name)` | A [[Plotting#Fluent builder|fluent builder]] over an existing panel. |

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

