"""03: e-CALLISTO type II burst, raw (left) and dsp.background_subtract (right)."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import callisto  # noqa: E402
from shotlib import hide_empty_panel_overlays, main_window, pump, save_panel  # noqa: E402

from SciQLop.user_api import dsp  # noqa: E402
from SciQLop.user_api.plot import Orientation, TimeRange, create_plot_panel  # noqa: E402

t, f, z = callisto.burst()
clean = dsp.arrays.background_subtract(t, z, q=10)

main_window()
panel = create_plot_panel()
side_by_side = panel.add_sub_panel(Orientation.Horizontal)
for data, name, unit in [(z, "raw dynamic spectrum", "Intensity [digits]"),
                         (clean, "dsp.background_subtract(q=10)", "Intensity - background [digits]")]:
    plot, _ = side_by_side.plot_data(t, f, data, name=name)
    plot.set_axis_label("y", "Frequency [MHz]")
    plot.set_axis_label("z", unit)
side_by_side.time_range = TimeRange(callisto.START, callisto.STOP)
pump(3)
hide_empty_panel_overlays()  # drawn over the sub-panel (reported 2026-10-11)
save_panel(panel, "03-dsp-background-subtract-type-ii-burst.png")
