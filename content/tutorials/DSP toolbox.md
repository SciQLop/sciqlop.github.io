---
title: DSP toolbox
---
>[!info] Info to beginners:
>This tutorial builds on [[virtual products]]. Read that one first if you have never written a virtual product.

`SciQLop.user_api.dsp` is a small signal-processing layer that works directly on Speasy variables. Give it a `SpeasyVariable`, get a `SpeasyVariable` back, with the time axis, units and column names preserved. Every helper detects gaps and processes each continuous segment on its own, so a data hole never bleeds into the filtered signal.

The main lesson of this page is a pattern: **put the DSP call inside a virtual product**. SciQLop then recomputes it for whatever time window you look at, next to the raw product.

> **_NOTE:_** The module is marked experimental in v0.12. Names are stable enough to use, but expect small changes.

# Low-pass filtering MMS burst data

FGM burst mode samples at 128 Hz. Let's build a virtual product that keeps only what is below 1 Hz. Open a notebook and import what we need:

```python
from datetime import datetime
import speasy as spz
from scipy.signal import butter
from speasy import SpeasyVariable
from SciQLop.user_api import dsp, TimeRange
from SciQLop.user_api.virtual_products import create_virtual_product, VirtualProductType
from SciQLop.user_api.plot import create_plot_panel
```

The callback fetches the raw field, designs a Butterworth filter and applies it with `dsp.sosfiltfilt`, the zero-phase IIR filter:

```python
def b_gsm_lowpass(start: float, stop: float) -> SpeasyVariable | None:
    b = spz.get_data("cda/MMS1_FGM_BRST_L2/mms1_fgm_b_gsm_brst_l2", start, stop)
    if b is None:
        return None
    sos = butter(4, 1.0, fs=128.0, output="sos").astype(b.values.dtype)
    return dsp.sosfiltfilt(b, sos)
```

Two details matter here:

- `.astype(b.values.dtype)`: the filter kernel requires the coefficients and the data to share a dtype. CDF data is often `float32` while SciPy returns `float64`; without the cast you get a `TypeError`.
- the returned variable keeps the four columns of the input (Bx, By, Bz, |B|), so we register it as a `MultiComponent` product with four labels.

```python
b_gsm_lowpass_vp = create_virtual_product("dsp_examples/mms1_b_gsm_lowpass", b_gsm_lowpass,
                                          VirtualProductType.MultiComponent,
                                          labels=["Bx", "By", "Bz", "|B|"])
```

Now plot the raw product and the filtered one in the same panel, on a burst interval:

```python
p = create_plot_panel()
p.time_range = TimeRange(datetime(2015, 10, 16, 13, 5, 25), datetime(2015, 10, 16, 13, 7, 35))
p.plot("speasy//cda//MMS//MMS1//FGM//MMS1_FGM_BRST_L2//mms1_fgm_b_gsm_brst_l2")
p.plot(b_gsm_lowpass_vp)
```

Pan or zoom the panel: the filter is recomputed on the new window. Product paths use `//` as separator; a single `/` raises in v0.12. `time_range` takes a `TimeRange`, not a tuple.

# The other helpers

All of them follow the same shape: a `SpeasyVariable` in, a `SpeasyVariable` out, plus a `gap_factor` keyword (a jump larger than `gap_factor` times the median sample spacing counts as a gap; default 3).

```python
b = spz.get_data("cda/MMS1_FGM_BRST_L2/mms1_fgm_b_gsm_brst_l2",
                 datetime(2015, 10, 16, 13, 5, 25), datetime(2015, 10, 16, 13, 7, 35))

smooth = dsp.rolling_mean(b, 64)          # gap-aware rolling mean over 64 samples
noise = dsp.rolling_std(b, 64)            # rolling standard deviation, same window
uniform = dsp.resample(b, target_dt=0.1)  # uniform 10 Hz grid, one per segment
filled = dsp.interpolate_nan(b, max_consecutive=2)
magnitude = dsp.reduce(b, "norm")         # collapse the columns to one
segments = dsp.split_segments(b)          # list of SpeasyVariable, one per continuous run
```

`dsp.filtfilt(b, coeffs)` is the FIR twin of `sosfiltfilt`; `dsp.fir_filter` and `dsp.iir_sos` are the single-pass (non zero-phase) versions. `dsp.fft` and `dsp.spectrogram` change the axes, so they return lists, one entry per detected segment. A spectrogram segment is a 2D `SpeasyVariable` (time x frequency) that a `Spectrogram` virtual product returns as a 3-tuple:

```python
def bx_spectrogram(start: float, stop: float):
    b = spz.get_data("cda/MMS1_FGM_BRST_L2/mms1_fgm_b_gsm_brst_l2", start, stop)
    if b is None:
        return None
    segs = dsp.spectrogram(b, col=0, window_size=256, overlap=128, window="hann")
    if not segs:
        return None
    s = segs[0]
    return s.time, s.axes[1].values, s.values

bx_spectrogram_vp = create_virtual_product("dsp_examples/mms1_bx_spectrogram", bx_spectrogram,
                                           VirtualProductType.Spectrogram)
p.plot(bx_spectrogram_vp)
```

If you already hold plain numpy arrays, `dsp.arrays` exposes the same functions with `(t, y, ...)` arguments and returns `(t_out, y_out)` tuples.

# Background subtraction on dynamic spectra

Radio dynamic spectra are dominated by the receiver's frequency response: each channel has its own baseline, and a burst is a small excursion on top of it. Removing a per-channel background is what makes a type II burst pop out. A good example event is the e-CALLISTO type II burst of 2017-09-06, 11:58 to 12:16 UT, seen from the HUMAIN station. e-CALLISTO is not a built-in Speasy provider, so the snippets below take a generic spectrogram `SpeasyVariable` named `spec` (time x frequency), whatever its origin: a radio plugin, a file you loaded yourself, or the output of `dsp.spectrogram` above.

`dsp.background_subtract` (new in v0.13) does it in one call:

```python
from datetime import timedelta

clean = dsp.background_subtract(spec, q=50.0, window=timedelta(minutes=5), mode="db")
```

`q` is the percentile used as the background estimate per channel (50 = median; use 5 to 10 when bursts fill most of the window), `window` is `None` for one constant background, an `int` for a sample count or a `timedelta` for a duration, and `mode` is `"diff"`, `"ratio"` or `"db"`.

On v0.12, the same idea fits in a `Spectrogram` virtual product with plain numpy:

```python
import numpy as np

def radio_bgsub(start: float, stop: float):
    spec = ...  # fetch your dynamic spectrum for [start, stop] as a SpeasyVariable
    if spec is None:
        return None
    background = np.nanpercentile(spec.values, 50.0, axis=0)
    return spec.time, spec.axes[1].values, spec.values - background
```

>[!tip] Going further
>The `%%vp` cell magic wraps any of these callbacks into a live pipeline, and knobs turn the cutoff frequency or the FFT window into sliders. Both are shown in tutorial notebook *14 - DSP* bundled with SciQLop (open it from the welcome page).
