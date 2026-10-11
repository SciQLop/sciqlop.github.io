---
title: Threading and common errors
---
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

