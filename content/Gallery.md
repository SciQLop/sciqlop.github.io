---
title: Gallery
---

Real archive data, real events, no synthetic series. Every screenshot below comes from a live SciQLop
session; the products, intervals and features behind each one are listed in the
[sources manifest](https://github.com/SciQLop/sciqlop.github.io/blob/v4/content/gallery/SOURCES.md).

## Magnetopause crossing, five plots, one time axis

![[01-hero-mms-magnetopause-crossing.png]]

MMS1 on the dayside magnetopause, the Burch et al. 2016 electron diffusion region event of 2015-10-16.
FPI-DIS burst omni spectrum, ion density, bulk velocity, temperatures and FGM burst B GSM, stacked on a shared
time axis.

## Orbit projections with linked time markers

![[02-projection-orbit-time-colored.png]]

A full day of MMS1 position in XY, YZ and ZX projections, coloured by time. The red markers are one linked
time marker at the 13:05:42 crossing, shown on all three projections at once.

## Background subtraction on a type II radio burst

![[03-dsp-background-subtract-type-ii-burst.png]]

The type II burst from the X9.3 flare of 2017-09-06, e-CALLISTO station HUMAIN. Left: raw spectrum,
dominated by instrumental gain bands. Right: the same data after `dsp.background_subtract(q=10)` (see the [[DSP toolbox]] tutorial).

## Waterfall: the drift is the lag

![[04-waterfall-type-ii-drift.png]]

Same burst as a 20-channel waterfall. The peak walks later going down the stack. That lag *is* the type II
frequency drift.

## Two plasma regimes in one 2-D histogram

![[05-histogram2d-plasma-regimes.png]]

Three days of MMS1 ion density against perpendicular temperature, log bins on both axes. Hot tenuous
magnetosphere upper left, cold dense magnetosheath lower right, joined by the boundary-crossing track.

## Data-aware annotation layers

![[06-annotation-layer-detector.png]]

A `detectors/magnetosheath` layer: blue spans where ion density exceeds a threshold, orange markers at the
crossings, and the threshold itself as a red line you can drag.

## Parameterised virtual products

![[07-knobs-parameterized-virtual-product.png]]

A virtual product with two knobs, declared with `Annotated[..., Knob(...)]`. The Inspector exposes them as
labelled controls; the threshold knob is drawn on the plot as a movable line.

## Catalog overlays

![[08-catalog-overlays-multi-plot.png]]

Two colour-coded catalogs over three plots. MMS1 sits in the magnetosheath until about 13:40, then enters
the magnetosphere. The events were derived from the data, not hand-drawn.

## Publication-style annotations

![[09-graphic-primitives-annotated-crossing.png]]

Curved arrows, text and vertical lines from the graphic-primitives API, on the same crossing.

## Four palettes

<div class="theme-grid">

![[10-theme-light.png]]

![[10-theme-dark.png]]

![[10-theme-neutral.png]]

![[10-theme-space.png]]

</div>

The same panel under the light, dark, neutral and space themes, switched at runtime with
`themes.apply_theme`.

## New in v0.13

### AI assistant

![[11-ai-assistant-dock.png]]

The agent dock mid-job. It plotted the panel on the right from a one-sentence request, then checked its own
work with a screenshot tool before reporting.

### Guided tours

![[12b-guided-tour-add-more-data.png]]

Coach marks walk new users through their first plot, over real content.

### Find any product

![[14-products-smart-search.png]]

The sidebar smart search narrows the tree of tens of thousands of products as you type, with hit counts and
data coverage per node.

![[13-empty-panel-search-overlay.png]]

A new empty panel opens with a search box, or takes a drop.
