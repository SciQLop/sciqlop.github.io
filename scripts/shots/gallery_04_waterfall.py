"""04: the same burst as a 20-channel waterfall; the lag down the stack is the frequency drift."""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import callisto  # noqa: E402
from shotlib import main_window, pump, save_panel  # noqa: E402

from SciQLop.user_api import dsp  # noqa: E402
from SciQLop.user_api.plot import TimeRange, create_plot_panel  # noqa: E402

N_LINES = 20
F_MIN = 46.0  # the lowest channel carries a calibration ramp, not sky signal

t, f, z = callisto.burst()
z = dsp.arrays.background_subtract(t, z, q=10)
sky = np.flatnonzero(f > F_MIN)
lines = sky[np.linspace(0, len(sky) - 1, N_LINES).astype(int)]  # line 0, at the bottom, is the lowest frequency

main_window()
panel = create_plot_panel()
panel.waterfall(t, f[lines], z[:, lines].T, offsets=1.0, normalize=True,
                name="e-CALLISTO HUMAIN — 2017-09-06 type II burst")
panel.plots[0].set_axis_label("y", f"{f[lines[0]]:.1f} → {f[lines[-1]]:.1f} MHz (one line per channel)")
panel.time_range = TimeRange("2017-09-06T12:01", "2017-09-06T12:10")
panel.plots[0].set_y_range(-0.3, N_LINES + 0.3)  # the waterfall doesn't fit itself yet (reported 2026-10-11)
pump(3)
save_panel(panel, "04-waterfall-type-ii-drift.png")
