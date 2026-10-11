"""02: one day of MMS1 orbit in XY/YZ/ZX projections, coloured by time, with the linked
time marker at the 13:05:42 magnetopause crossing."""
import os
import sys

import numpy as np
import speasy as spz

sys.path.insert(0, os.path.dirname(__file__))
from mms import MMS_DAY  # noqa: E402
from shotlib import main_window, pump, save_panel, settle  # noqa: E402

from SciQLop.user_api.plot import PlotType, create_plot_panel  # noqa: E402

EARTH_RADIUS_KM = 6371.2
ORBIT = "MMS1 orbit 2015-10-16"
CROSSING = np.datetime64("2015-10-16T13:05:42", "ns").astype("int64") / 1e9

r = spz.get_data("cda/MMS1_FGM_SRVY_L2/mms1_fgm_r_gsm_srvy_l2", MMS_DAY.start(), MMS_DAY.stop())
t = r.time.astype("datetime64[ns]").astype("int64") / 1e9
xyz = np.ascontiguousarray(r.values[:, :3] / EARTH_RADIUS_KM)

main_window()
panel = create_plot_panel()
panel.time_range = MMS_DAY
proj, curve = panel.plot_data(t, xyz, plot_type=PlotType.Projection,
                              name=ORBIT, labels=["X GSM [Re]", "Y GSM [Re]", "Z GSM [Re]"])
settle(panel)
impl = proj._get_impl_or_raise()
impl.set_time_color_enabled(True)
proj.set_x_range(-5.5, 10.2)
proj.set_y_range(-5.5, 10.2)
pump(2)
impl.set_time_marker(CROSSING)
pump(1)
save_panel(panel, "02-projection-orbit-time-colored.png")
