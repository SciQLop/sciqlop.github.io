"""01: MMS1 magnetopause crossing (Burch et al. 2016 EDR event), five stacked plots."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from shotlib import main_window, set_labels, save_panel, settle  # noqa: E402
from mms import BURCH_EDR, DIS_BRST, FGM_BRST_GSM  # noqa: E402

from SciQLop.user_api.plot import create_plot_panel  # noqa: E402

main_window()
panel = create_plot_panel()
panel.time_range = BURCH_EDR
panel.plot(DIS_BRST + "mms1_dis_energyspectr_omni_brst")
panel.plot(FGM_BRST_GSM)
panel.plot(DIS_BRST + "mms1_dis_numberdensity_brst")
panel.plot(DIS_BRST + "mms1_dis_bulkv_gse_brst")
panel.plot(DIS_BRST + "mms1_dis_temppara_brst")
panel.plot(DIS_BRST + "mms1_dis_tempperp_brst", plot_index=4)
settle(panel)
set_labels(panel, [("y2", "Ion energy [eV]"), ("y", "B GSM [nT]"), ("y", "Ni [cm⁻³]"),
                   ("y", "Vi GSE [km/s]"), ("y", "Ti [eV]")])
save_panel(panel, "01-hero-mms-magnetopause-crossing.png")
