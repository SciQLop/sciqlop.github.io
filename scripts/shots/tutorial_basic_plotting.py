"""The eight screenshots of the Basic workflow tutorial (content/tutorials/basic plotting/)."""
import os
import sys

from PySide6.QtCore import QRect

sys.path.insert(0, os.path.dirname(__file__))
from shotlib import (Arrow, by_tooltip, collapse_dock, grab, main_window, new_panel_button,  # noqa: E402
                     product_row, pump, rect_in_window, select_in_inspector, settle, side_tab)

from SciQLop.user_api import TimeRange  # noqa: E402
from SciQLop.user_api.plot import create_plot_panel  # noqa: E402

MFI = "speasy//cda//ACE//MAG//AC_H0_MFI//"
MAGNITUDE_PATH = ["speasy", "cda", "ACE", "MAG", "AC_H0_MFI", "Magnitude"]
ONE_DAY = TimeRange("2023-05-19T13:56", "2023-05-20T13:56")
TEN_DAYS = TimeRange("2023-05-15T00:00", "2023-05-25T00:00")
SUB = "basic plotting/"

mw = main_window()
panel = create_plot_panel()
pump(1)
grab(SUB + "empty.png", [
    Arrow(side_tab("Products"), "Products", (150, 140)),
    Arrow(new_panel_button(), "New plot panel", (420, 150)),
    Arrow(by_tooltip("Start time (UTC)"), "Start time", (420, 760)),
    Arrow(by_tooltip("Time window duration"), "Duration", (760, 760)),
])

panel.time_range = ONE_DAY
row = product_row(MAGNITUDE_PATH)
panel_area = rect_in_window(panel._get_impl_or_raise())
grab(SUB + "dragndrop.png", [
    Arrow(row, "Drag and drop", (panel_area.center().x() + 120, panel_area.center().y() - 180), box=True),
])

collapse_dock("Products")
panel.plot(MFI + "Magnitude")
settle(panel)
grab(SUB + "plot_one.png")

_, bgsm = panel.plot(MFI + "BGSM")
settle(panel)
grab(SUB + "plot_2plots.png")

bz = bgsm._get_impl_or_raise().components()[2]
bz.set_visible(False)
bz.set_selected(True)  # expands the legend group, as clicking the ▸ marker does
pump(1)
plot_area = rect_in_window(panel.plots[1]._get_impl_or_raise())
# The legend wrapper exposes no entry geometry: the Bz row sits at a fixed offset from the
# plot's top-right corner (measured on this layout).
bz_row = QRect(plot_area.right() - 118, plot_area.top() + 83, 95, 20)
grab(SUB + "hide.png", [Arrow(bz_row, "double-click to hide", (bz_row.center().x() - 300, bz_row.center().y() + 110),
                              box=True)])

panel.zoom_limit_seconds = 30 * 86400
panel.time_range = TEN_DAYS
pump(0.2)  # before the new data arrives
grab(SUB + "zoomingout.png")
settle(panel)
grab(SUB + "zoomedout.png")

second_plot = panel.plots[1]._get_impl_or_raise().objectName()
select_in_inspector(second_plot)
print("selected plot:", second_plot)
grab(SUB + "properties1.png")
