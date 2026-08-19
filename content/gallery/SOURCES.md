# Gallery sources

All shots produced 2026-08-19 from a live SciQLop 0.13.0.dev0 (SciQLopPlots 0.34.0,
Speasy 1.7.1), window 1600x1000 logical / 2560x1370 px, dark theme unless stated.
Every panel uses real archive data — no synthetic series.

| File | Event / data | Interval (UTC) | Products | Feature shown |
|---|---|---|---|---|
| `01-hero-mms-magnetopause-crossing.png` | MMS1 dayside magnetopause crossing (Burch et al. 2016 EDR event). S/C at (8.31, 7.08, −4.80) R_E GSM, R = 11.9 R_E — verified against MMS1 MEC EPHT89Q. | 2015-10-16 13:05:25–13:07:35 | FPI-DIS burst L2 (omni energy spectrum, N_i, V_i GSE, T_∥/T_⊥) + FGM burst L2 B GSM | 5 stacked plots, shared time axis |
| `02-projection-orbit-time-colored.png` | MMS1 orbit, full day. Red markers = linked time marker at the 13:05:42 crossing, on all three projections. | 2015-10-16 00:00–24:00 | `mms1_fgm_r_gsm_srvy_l2` | N-D projection plot (XY/YZ/ZX), time-coloured curve, linked time markers |
| `03-dsp-background-subtract-type-ii-burst.png` | Type II radio burst from the X9.3 flare of 2017-09-06 (largest of solar cycle 24), e-CALLISTO station HUMAIN (Belgium). Left: raw, dominated by instrumental gain bands. Right: `dsp.background_subtract(q=10)`. | 2017-09-06 11:58–12:16 | e-CALLISTO HUMAIN focus code 59, 45–110 MHz | `SciQLop.user_api.dsp.background_subtract`, side-by-side sub-panels |
| `04-waterfall-type-ii-drift.png` | Same burst as a 20-channel waterfall. The peak walks later going down the stack — that lag *is* the type II frequency drift. | 2017-09-06 12:01–12:10 | e-CALLISTO HUMAIN, 46.5–84.4 MHz | `panel.waterfall(..., offsets=, gain=, normalize=True)` |
| `05-histogram2d-plasma-regimes.png` | MMS1 ion moments over 3 days. Two populations: hot/tenuous magnetosphere (upper left) and cold/dense sheath + plasmasphere (lower right), joined by the boundary-crossing track. | 2015-10-16 → 2015-10-19 | FPI-DIS fast L2: `numberdensity_fast` vs `tempperp_fast` | `histogram2d` with log X/Y bins and log Z |
| `06-annotation-layer-detector.png` | Data-aware annotation layer `detectors/magnetosheath`: blue spans = N_i > threshold, orange markers = threshold crossings, red line = the threshold knob itself. | 2015-10-16 13:05:25–13:07:35 | as shot 01 | `@register_layer`, `panel.add_layer` |
| `07-knobs-parameterized-virtual-product.png` | Full window. Inspector shows a parameterised virtual product (`demo/Bmag_smoothed`) with its Parameters section; the red line on the bottom plot is the draggable `ThresholdKnob` (`widget="hline"`, 25 nT). | 2015-10-16 13:05:25–13:07:35 | FGM burst \|B\| smoothed by a knob-controlled boxcar | `create_virtual_product` + `Annotated[..., Knob(...)]` |
| `08-catalog-overlays-multi-plot.png` | Two colour-coded catalogs over three plots. MMS1 sits in the magnetosheath (N_i ≈ 20–40 cm⁻³, cold ions, turbulent B) until ~13:40, then enters the magnetosphere. Events were **derived from the data**, not hand-drawn. | 2015-10-16 10:00–16:00 | FPI-DIS + FGM survey L2 | `catalogs.save`, `add_catalog_overlay(override_color=...)` |
| `09-graphic-primitives-annotated-crossing.png` | Publication-style annotation of the same crossing. | 2015-10-16 13:05:25–13:07:35 | as shot 01 | `CurvedLine` (arrow terminations), `Text`, `VerticalLine` |
| `10-theme-{light,dark,neutral,space}.png` | Identical panel in all four palettes — compose as a 2×2. | as shot 09 | as shot 09 | `themes.apply_theme` |

## Not produced

The two v0.13 teasers (AI assistant dock mid-conversation, guided-tour coach-mark) were
not attempted — they need a live conversation / tour state that can't be staged from the
kernel.

## Caveats worth knowing before writing captions

- Shot 03 was originally planned as I-LOFAR. The ASTRON host (`spaceweather.astron.nl`)
  is unreachable from here (60 s connect timeout), so the LOFAR LBA virtual product
  returns nothing. e-CALLISTO (`soleil.i4ds.ch`) is up and was used instead.
- Shot 04: e-CALLISTO channel index 1 carries a periodic calibration ramp, not sky
  signal. It is excluded (channels above 46 MHz only).
- Shot 07: the Inspector renders knobs as **bare, unlabelled spinboxes**. The specs do
  carry `label`, `unit`, `min`/`max`/`step` (verified via
  `knobs.extract_specs_from_callback`), and no slider widget is produced. Don't write a
  caption promising "labelled sliders" until that's fixed.
