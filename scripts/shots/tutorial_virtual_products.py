"""virtual products/vp_mirror_plot.png: the tutorial's mirror-mode virtual product, run verbatim,
dropped as the second plot of an MMS panel and shown in the product tree."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from mms import DIS_FAST, FGM_SRVY_GSM, SHEATH_TO_MSPHERE  # noqa: E402
from shotlib import Arrow, grab, main_window, product_row, rect_in_window, set_labels, settle  # noqa: E402

from SciQLop.user_api.plot import create_plot_panel  # noqa: E402
from SciQLop.user_api.virtual_products import create_virtual_product, VirtualProductType  # noqa: E402
from speasy import SpeasyVariable  # noqa: E402
from speasy.signal.resampling import interpolate  # noqa: E402
import speasy as spz  # noqa: E402
import scipy.constants as cst  # noqa: E402


def mirror_mode_threshold(start_time: float, stop_time: float) -> SpeasyVariable | None:
    mms1_products = spz.inventories.data_tree.cda.MMS.MMS1
    products = [mms1_products.DIS.MMS1_FPI_FAST_L2_DIS_MOMS.mms1_dis_temppara_fast,
                mms1_products.DIS.MMS1_FPI_FAST_L2_DIS_MOMS.mms1_dis_tempperp_fast,
                mms1_products.FGM.MMS1_FGM_SRVY_L2.mms1_fgm_b_gse_srvy_l2,
                mms1_products.DIS.MMS1_FPI_FAST_L2_DIS_MOMS.mms1_dis_numberdensity_fast]

    tpara, tperp, b, n = spz.get_data(products, start_time, stop_time)

    anisotropy = tperp / tpara
    Pperp = tperp * n * 1e6
    b = interpolate(tperp, b)
    betaperp = Pperp * cst.mu_0 * cst.e * 2 / (b["Bt"] * 1e-9) ** 2
    mirror = betaperp * (anisotropy - 1)
    return mirror


mirror_mode_threshold_vp = create_virtual_product("mms_vprods/mms1/mirror", mirror_mode_threshold,
                                                  VirtualProductType.Scalar, labels=["Mirror mode threshold"])

main_window()
panel = create_plot_panel()
panel.time_range = SHEATH_TO_MSPHERE
panel.plot(FGM_SRVY_GSM)
mirror_plot, _ = panel.plot(mirror_mode_threshold_vp)
panel.plot(DIS_FAST + "mms1_dis_numberdensity_fast")
settle(panel)
row = product_row(["mms_vprods", "mms1", "mirror"])
set_labels(panel, [("y", "B GSM [nT]"), ("y", "C mirror"), ("y", "Ni [cm⁻³]")])
grab("virtual products/vp_mirror_plot.png", [
    Arrow(row, "your virtual product", (row.center().x() + 120, row.top() - 70), box=True),
])
