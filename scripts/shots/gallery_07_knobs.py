"""07: full window, Properties dock showing the adjustable inputs of a parameterised
virtual product; its threshold knob is the red line on the bottom plot."""
import os
import sys
from typing import Annotated

import numpy as np
import speasy as spz

sys.path.insert(0, os.path.dirname(__file__))
from mms import BURCH_EDR, FGM_BRST_GSM  # noqa: E402
from shotlib import grab, main_window, pump, select_in_inspector, settle  # noqa: E402

from SciQLop.user_api.knobs import Knob  # noqa: E402
from SciQLop.user_api.plot import create_plot_panel  # noqa: E402
from SciQLop.user_api.virtual_products import VirtualProductType, create_virtual_product  # noqa: E402


def bmag_smoothed(start: float, stop: float,
                  smooth_window: Annotated[int, Knob(min=1, max=200, step=1, label="Smooth window",
                                                     unit="samples")] = 16,
                  threshold: Annotated[float, Knob(widget="hline", min=0.0, max=80.0, step=1.0,
                                                   label="Threshold", unit="nT", color="#e74c3c")] = 25.0):
    b = spz.get_data("cda/MMS1_FGM_BRST_L2/mms1_fgm_b_gsm_brst_l2", start, stop)
    if b is None:
        return None
    bmag = np.linalg.norm(b.values[:, :3], axis=1)
    if smooth_window > 1:
        bmag = np.convolve(bmag, np.ones(smooth_window) / smooth_window, mode="same")
    return b.time.astype("datetime64[ns]").astype(np.int64) / 1e9, bmag


vp = create_virtual_product("demo/Bmag_smoothed", bmag_smoothed, VirtualProductType.Scalar,
                            labels=["|B| smoothed"])

main_window()
panel = create_plot_panel()
panel.time_range = BURCH_EDR
panel.plot(FGM_BRST_GSM)
panel.plot_product(vp, product_inputs={"smooth_window": 128})
settle(panel)
select_in_inspector("Bmag_smoothed")
grab("07-knobs-parameterized-virtual-product.png")
