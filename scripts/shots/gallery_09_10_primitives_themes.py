"""09: publication-style annotation of the crossing with graphic primitives.
10: the same panel in the four built-in palettes."""
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(__file__))
from mms import BURCH_EDR, DIS_BRST, FGM_BRST_GSM  # noqa: E402
from shotlib import main_window, pump, save_panel, set_labels, settle  # noqa: E402

from SciQLop.user_api import themes  # noqa: E402
from SciQLop.user_api.plot import CurvedLine, LineTermination, Text, VerticalLine, create_plot_panel  # noqa: E402

YELLOW, BLUE = "#f1c40f", "#5dade2"


def utc(*hms) -> float:
    return datetime(2015, 10, 16, *hms, tzinfo=timezone.utc).timestamp()


T_CROSS = utc(13, 5, 42)

main_window()
panel = create_plot_panel()
panel.time_range = BURCH_EDR
spectrum, _ = panel.plot(DIS_BRST + "mms1_dis_energyspectr_omni_brst")
b_plot, _ = panel.plot(FGM_BRST_GSM)
settle(panel)
# Primitives use the left y axis, but a spectrogram draws on the right one ("y2"). Pinning the
# unused left axis to 0..1 lets the spectrogram annotations sit at fractions of the plot height.
spectrum.set_axis_range("y", 0.0, 1.0)

annotations = [
    VerticalLine(spectrum, T_CROSS, color=YELLOW, line_width=1.5),
    VerticalLine(b_plot, T_CROSS, color=YELLOW, line_width=1.5),
    Text(spectrum, "magnetosphere", x=utc(13, 5, 31), y=0.14, color="white", font_size=11),
    Text(spectrum, "magnetopause", x=utc(13, 6, 0), y=0.08, color="white", font_size=11),
    Text(spectrum, "magnetosheath", x=utc(13, 6, 40), y=0.14, color="white", font_size=11),
    CurvedLine(spectrum, start=(utc(13, 5, 58), 0.09), stop=(T_CROSS + 1, 0.09), color=YELLOW,
               line_width=2.0, stop_termination=LineTermination.Arrow),
    Text(b_plot, "B rotation across the current sheet", x=utc(13, 6, 15), y=31, color="white",
         font_size=11),
    CurvedLine(b_plot, start=(utc(13, 6, 13), 28), stop=(utc(13, 5, 47), 7), color=BLUE,
               line_width=2.0, stop_termination=LineTermination.Arrow),
]
pump(1)
set_labels(panel, [("y2", "Ion energy [eV]"), ("y", "B GSM [nT]")])
save_panel(panel, "09-graphic-primitives-annotated-crossing.png")

for theme in ["light", "dark", "neutral", "space"]:
    themes.apply_theme(theme)
    pump(1.5)
    set_labels(panel, [("y2", "Ion energy [eV]"), ("y", "B GSM [nT]")])
    save_panel(panel, f"10-theme-{theme}.png")
themes.apply_theme("dark")
