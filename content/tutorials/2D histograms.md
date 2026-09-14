---
title: 2D histograms
---
# 2D histograms

`PlotPanel.histogram2d` bins `(x, y)` samples into a density map. It is the tool for "is this one population or two?"
questions where a scatter plot would just be a blob. You can feed it static arrays, or a callback that SciQLop re-runs
every time the panel's time range changes.

> **_NOTE:_** SciQLop product paths are `//`-separated (`speasy//cda//MMS//...`). Speasy's own `get_data` uses its
> usual `cda/DATASET/parameter` form. The example below uses both.

## Ion density against perpendicular temperature

Three days of MMS1 FPI-DIS fast moments, 2015-10-16 to 2015-10-19. During that interval MMS1 crosses the magnetopause
many times, so the ions come from two very different plasmas. Binning density against perpendicular temperature
separates them.

```python
import numpy as np
import speasy as spz
from SciQLop.user_api import TimeRange
from SciQLop.user_api.plot import create_plot_panel
from SciQLopPlots import ColorGradient

DIS = "cda/MMS1_FPI_FAST_L2_DIS_MOMS"


def density_vs_tperp(start, stop):
    """(log10 n, log10 T_perp) for the panel's current time range."""
    n = spz.get_data(f"{DIS}/mms1_dis_numberdensity_fast", start, stop)
    t = spz.get_data(f"{DIS}/mms1_dis_tempperp_fast", start, stop)
    if n is None or t is None:
        return np.array([]), np.array([])
    n, t = n.values.ravel(), t.values.ravel()
    ok = (n > 0) & (t > 0)
    return np.log10(n[ok]), np.log10(t[ok])


p = create_plot_panel()
xy_plot, hist = p.histogram2d(density_vs_tperp, x_bins=100, y_bins=100,
                              z_log_scale=True, gradient=ColorGradient.Hot)
xy_plot.set_axis_label("x", "log10 n", "cm^-3")
xy_plot.set_axis_label("y", "log10 T_perp", "eV")

# the density time series underneath shows which crossings feed the histogram
p.plot("speasy//cda//MMS//MMS1//DIS//MMS1_FPI_FAST_L2_DIS_MOMS//mms1_dis_numberdensity_fast")
p.time_range = TimeRange("2015-10-16T00:00:00", "2015-10-19T00:00:00")
```

Two clusters show up. Upper left is the magnetosphere: hot (keV) and tenuous (well under 1 cm⁻³). Lower right is the
magnetosheath: cold (~100 eV) and dense (tens of cm⁻³). The thin track joining them is the boundary layer sampled
during each crossing. Pan the time range and the histogram re-bins — narrow it to a single crossing and the track is
all that is left.

## Static arrays instead of a callback

If you already hold the samples, pass two arrays. The histogram is then fixed, but you can replace its data at any
time.

```python
rng = np.random.default_rng(0)
x, y = rng.standard_normal(20_000), rng.standard_normal(20_000)

p2 = create_plot_panel()
_, static_hist = p2.histogram2d(x, y, x_bins=60, y_bins=60, name="noise")
static_hist.set_data(x, y * 2)
```

## Bins, scales and gradient

- `x_bins` / `y_bins` are integer bin counts, spread linearly over the data range. The example takes `log10`
  inside the callback so that linear bins in log space *are* log bins; that works on every version. Since v0.13
  you can keep the raw values and pass `x_bin_strategy=BinStrategy.Log` / `y_bin_strategy=BinStrategy.Log`
  instead (`from SciQLop.user_api.plot.enums import BinStrategy`; `SymLog` also exists).
- `z_log_scale=True` (or `hist.z_log_scale = True` later) puts the colour scale on a log axis. Use it whenever counts
  span several decades — otherwise the dense magnetosheath cluster saturates and the boundary track disappears.
- `gradient` takes a `SciQLopPlots.ColorGradient` value: `Candy`, `Cold`, `Hot` or `Polar`. A gradient name as a
  string is not accepted in v0.12. `hist.gradient = ColorGradient.Cold` changes it afterwards.
- The returned `XYPlot` owns the axes: `set_axis_label`, `set_x_range`, `set_y_range`, and `x_scale_type` /
  `y_scale_type` (`ScaleType.Linear` or `ScaleType.Logarithmic`). Keep the axes linear when the data is already
  `log10`-transformed.

Pin the axes if the histogram jumps around while you pan:

```python
xy_plot.set_x_range(-2, 2)   # 0.01 to 100 cm^-3
xy_plot.set_y_range(0, 4)    # 1 eV to 10 keV
```

## How the callback follows the time range

The callback signature is `f(start, stop) -> (x, y)` with `start` and `stop` as epoch floats, the same convention as
virtual products, so `spz.get_data` takes them directly. SciQLop calls it on every time range change: the time-range
bar, a zoom, a pan, or `p.time_range = TimeRange(...)`. Return two empty arrays when there is nothing in the interval.

`PlotPanel.time_range` wants a `TimeRange` (ISO strings or `datetime` objects), not a tuple. Set it after the plots
exist, and keep at least one time-series plot in the panel — the histogram is an XY plot and has no time axis of its
own to move.

Each `histogram2d` call creates its own plot: a plot holds a single colour scale, so adding a second colormap-style
plottable to an existing plot raises `RuntimeError`. Use `plot_index` to choose where the new plot goes in the panel.
