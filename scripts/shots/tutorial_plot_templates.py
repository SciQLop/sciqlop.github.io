"""plot templates/simple_mms_template.png: the panel the tutorial's script builds, run verbatim."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from shotlib import grab, main_window, settle  # noqa: E402

from SciQLop.user_api.plot import *  # noqa: E402,F403  as in the tutorial

main_window()
p = create_plot_panel()  # noqa: F405
p.time_range = TimeRange("2020-12-19", "2020-12-20")  # noqa: F405
p.plot("speasy//cda//MMS//MMS1//DIS//MMS1_FPI_FAST_L2_DIS_MOMS//mms1_dis_energyspectr_omni_fast")
p.plot("speasy//cda//MMS//MMS1//DIS//MMS1_FPI_FAST_L2_DIS_MOMS//mms1_dis_numberdensity_fast")
p.plot("speasy//cda//MMS//MMS1//DIS//MMS1_FPI_FAST_L2_DIS_MOMS//mms1_dis_bulkv_gse_fast")
p.plot("speasy//cda//MMS//MMS1//FGM//MMS1_FGM_SRVY_L2//mms1_fgm_b_gse_srvy_l2")
p.plot("speasy//cda//MMS//MMS1//DIS//MMS1_FPI_FAST_L2_DIS_MOMS//mms1_dis_tempperp_fast")
p.plots[4].plot("speasy//cda//MMS//MMS1//DIS//MMS1_FPI_FAST_L2_DIS_MOMS//mms1_dis_temppara_fast")
p.plots[1].y_scale_type = ScaleType.Logarithmic  # noqa: F405
p.plots[4].y_scale_type = ScaleType.Logarithmic  # noqa: F405
settle(p)
grab("plot templates/simple_mms_template.png")
