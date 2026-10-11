"""08: two catalogs derived from the data, drawn over three plots."""
import os
import sys

import numpy as np
import speasy as spz

sys.path.insert(0, os.path.dirname(__file__))
from mms import DIS_FAST, FGM_SRVY_GSM, SHEATH_TO_MSPHERE  # noqa: E402
from shotlib import main_window, set_labels, pump, save_panel, settle  # noqa: E402

from SciQLop.user_api.catalogs import catalogs  # noqa: E402
from SciQLop.user_api.plot import ScaleType, create_plot_panel  # noqa: E402

SHEATH_DENSITY = 10.0  # cm^-3
CROSSING_HALF_WIDTH = np.timedelta64(30, "s")


def intervals(mask: np.ndarray) -> list[tuple[int, int]]:
    edges = np.diff(mask.astype(np.int8), prepend=0, append=0)
    return list(zip(np.flatnonzero(edges == 1), np.flatnonzero(edges == -1) - 1))


n = spz.get_data("cda/MMS1_FPI_FAST_L2_DIS-MOMS/mms1_dis_numberdensity_fast",
                 SHEATH_TO_MSPHERE.start(), SHEATH_TO_MSPHERE.stop())
t, inside = n.time, n.values[:, 0] > SHEATH_DENSITY
sheath = [(t[a], t[b], {"region": "magnetosheath"}) for a, b in intervals(inside)]
crossings = [(t[i] - CROSSING_HALF_WIDTH, t[i] + CROSSING_HALF_WIDTH, {"kind": "boundary"})
             for a, b in intervals(inside) for i in (a, b)]
catalogs.save("My Catalogs//magnetosheath", sheath)
catalogs.save("My Catalogs//boundary crossings", crossings)

main_window()
panel = create_plot_panel()
panel.time_range = SHEATH_TO_MSPHERE
panel.plot(DIS_FAST + "mms1_dis_energyspectr_omni_fast")
panel.plot(FGM_SRVY_GSM)
density, _ = panel.plot(DIS_FAST + "mms1_dis_numberdensity_fast")
settle(panel)
density.y_scale_type = ScaleType.Logarithmic
density.set_y_range(0.2, 60)
panel.add_catalog_overlay("My Catalogs//magnetosheath", override_color="#503498db")
panel.add_catalog_overlay("My Catalogs//boundary crossings", override_color="#80e67e22")
pump(3)
set_labels(panel, [("y2", "Ion energy [eV]"), ("y", "B GSM [nT]"), ("y", "Ni [cm⁻³]")])
save_panel(panel, "08-catalog-overlays-multi-plot.png")
