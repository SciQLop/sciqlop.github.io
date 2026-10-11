---
title: Next release API changes
---
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
