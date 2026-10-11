"""09: the Burch et al. (2016) crossing marked with graphic primitives: the magnetopause and the
electron diffusion region. 10: the same panel in the four built-in palettes."""
import os
import sys
from datetime import datetime, timezone

import numpy as np
import speasy as spz

sys.path.insert(0, os.path.dirname(__file__))
from mms import BURCH_EDR, DIS_BRST, FGM_BRST_GSM  # noqa: E402
from shotlib import main_window, pump, save_panel, set_labels, settle  # noqa: E402

from SciQLop.user_api import themes  # noqa: E402
from SciQLop.user_api.plot import RectangularSpan, Text, VerticalLine, create_plot_panel  # noqa: E402
from PySide6.QtCore import Qt  # noqa: E402

ORANGE, EDR_FILL = "#e67e22", "#66f1c40f"
SHEATH_DENSITY = 5.0  # cm^-3
LABEL_Y = 52.0  # nT, in the headroom above the field traces


def utc(h: int, m: int, s: float) -> float:
    return datetime(2015, 10, 16, h, m, tzinfo=timezone.utc).timestamp() + s


def magnetopause_time() -> float:
    n = spz.get_data("cda/MMS1_FPI_BRST_L2_DIS-MOMS/mms1_dis_numberdensity_brst",
                     BURCH_EDR.start(), BURCH_EDR.stop())
    first = np.argmax(n.values[:, 0] > SHEATH_DENSITY)
    return n.time[first].astype("datetime64[ns]").astype("int64") / 1e9


T_MP = magnetopause_time()
EDR = (utc(13, 7, 1.6), utc(13, 7, 2.8))

main_window()
panel = create_plot_panel()
panel.time_range = BURCH_EDR
spectrum, _ = panel.plot(DIS_BRST + "mms1_dis_energyspectr_omni_brst")
b_plot, _ = panel.plot(FGM_BRST_GSM)
settle(panel)
# Primitives use the left y axis; a spectrogram draws on the right one ("y2"). Pinning the
# unused left axis to 0..1 lets the spectrogram marks span the full plot height.
spectrum.set_axis_range("y", 0.0, 1.0)
b_plot.set_y_range(-40.0, 60.0)

annotations = [
    *(VerticalLine(p, T_MP, color=ORANGE, line_width=2.0, line_style=Qt.PenStyle.DashLine)
      for p in (spectrum, b_plot)),
    RectangularSpan(spectrum, x1=EDR[0], y1=0.0, x2=EDR[1], y2=1.0, color=EDR_FILL, read_only=True),
    RectangularSpan(b_plot, x1=EDR[0], y1=-40.0, x2=EDR[1], y2=60.0, color=EDR_FILL, read_only=True),
    Text(b_plot, "magnetosphere", x=utc(13, 5, 34), y=LABEL_Y, font_size=11),
    Text(b_plot, "magnetopause", x=T_MP + 8, y=-33.0, font_size=11),
    Text(b_plot, "magnetosheath", x=utc(13, 6, 20), y=LABEL_Y, font_size=11),
    Text(b_plot, "electron diffusion region", x=EDR[0] - 11, y=-35.0, font_size=11),
]
pump(1)
set_labels(panel, [("y2", "Ion energy [eV]"), ("y", "B GSM [nT]")])
save_panel(panel, "09-graphic-primitives-annotated-crossing.png")

for theme in ["light", "dark", "neutral", "space"]:
    themes.apply_theme(theme)
    pump(4)
    save_panel(panel, f"10-theme-{theme}.png")
themes.apply_theme("dark")
