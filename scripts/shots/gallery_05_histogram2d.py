"""05: three days of MMS1 ion density vs perpendicular temperature, log bins on both axes."""
import os
import sys

import speasy as spz

sys.path.insert(0, os.path.dirname(__file__))
from shotlib import main_window, pump, save_panel  # noqa: E402

from SciQLop.user_api.plot import BinStrategy, ScaleType, create_plot_panel  # noqa: E402
from SciQLopPlots import ColorGradient  # noqa: E402

DIS = "cda/MMS1_FPI_FAST_L2_DIS-MOMS"
START, STOP = "2015-10-16", "2015-10-19"

n = spz.get_data(f"{DIS}/mms1_dis_numberdensity_fast", START, STOP).values.ravel()
tperp = spz.get_data(f"{DIS}/mms1_dis_tempperp_fast", START, STOP).values.ravel()
ok = (n > 0) & (tperp > 0)

main_window()
panel = create_plot_panel()
plot, _ = panel.histogram2d(n[ok], tperp[ok], x_bins=150, y_bins=150,
                            x_bin_strategy=BinStrategy.Log, y_bin_strategy=BinStrategy.Log,
                            z_log_scale=True, gradient=ColorGradient.Hot,
                            name="MMS1 FPI-DIS 2015-10-16 → 19")
plot.x_scale_type = ScaleType.Logarithmic
plot.y_scale_type = ScaleType.Logarithmic
plot.set_axis_label("x", "Ni", "cm⁻³")
plot.set_axis_label("y", "Ti perp", "eV")
pump(2)
save_panel(panel, "05-histogram2d-plasma-regimes.png")
