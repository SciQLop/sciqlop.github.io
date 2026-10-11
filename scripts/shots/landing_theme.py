"""sciqlop_theme.png: the same window in the space and light palettes, side by side."""
import os
import sys

from PySide6.QtGui import QPainter, QPixmap

sys.path.insert(0, os.path.dirname(__file__))
from mms import FGM_SRVY_GSM, SHEATH_TO_MSPHERE  # noqa: E402
from shotlib import OUT, main_window, pump, settle  # noqa: E402

from SciQLop.user_api import themes  # noqa: E402
from SciQLop.user_api.plot import create_plot_panel  # noqa: E402

GAP = 24  # px between the two windows

mw = main_window("space")
mw.resize(1000, 923)
panel = create_plot_panel()
panel.time_range = SHEATH_TO_MSPHERE
panel.plot(FGM_SRVY_GSM)
panel.plot("speasy//cda//MMS//MMS1//DIS//MMS1_FPI_FAST_L2_DIS_MOMS//mms1_dis_numberdensity_fast")
settle(panel)


def window_in(theme: str) -> QPixmap:
    themes.apply_theme(theme)
    pump(1.5)
    shot = mw.grab()
    shot.setDevicePixelRatio(1.0)  # compose in device pixels
    return shot


left, right = window_in("space"), window_in("light")
themes.apply_theme("dark")
out = QPixmap(left.width() + GAP + right.width(), left.height())
out.fill(0)
p = QPainter(out)
p.drawPixmap(0, 0, left)
p.drawPixmap(left.width() + GAP, 0, right)
p.end()
out.save(str(OUT / "sciqlop_theme.png"))
print("saved sciqlop_theme.png", out.width(), "x", out.height())
