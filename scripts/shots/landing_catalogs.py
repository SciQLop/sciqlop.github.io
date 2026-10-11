"""sciqlop_catalogs.png: an ICME seen by ACE in July 2012, labelled by a catalog event."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from shotlib import main_window, pump, save_panel, set_labels, settle  # noqa: E402

from SciQLop.user_api import TimeRange  # noqa: E402
from SciQLop.user_api.catalogs import catalogs  # noqa: E402
from SciQLop.user_api.plot import create_plot_panel  # noqa: E402

MFI, SWE = "speasy//cda//ACE//MAG//AC_H0_MFI//", "speasy//cda//ACE//SWEP//AC_H0_SWE//"
VIEW = TimeRange("2012-07-14T14:00", "2012-07-17T14:00")

catalogs.save("My Catalogs//ICMEs", [("2012-07-15T06:20", "2012-07-17T04:00", {"type": "ICME"})])

main_window("space")
panel = create_plot_panel()
panel.zoom_limit_seconds = 7 * 86400
panel.time_range = VIEW
for product in [MFI + "Magnitude", MFI + "BGSM", SWE + "Vp", SWE + "Np", SWE + "Tpr"]:
    panel.plot(product)
settle(panel)
panel.add_catalog_overlay("My Catalogs//ICMEs", override_color="#60f1c40f")
pump(2)
set_labels(panel, [("y", "|B| [nT]"), ("y", "B GSM [nT]"), ("y", "Vp [km/s]"), ("y", "Np [cm⁻³]"),
                   ("y", "Tp [K]")])
save_panel(panel, "sciqlop_catalogs.png")
