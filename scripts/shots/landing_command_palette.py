"""sciqlop_command_palette.png: Ctrl+K over a live panel."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from mms import FGM_SRVY_GSM, SHEATH_TO_MSPHERE  # noqa: E402
from shotlib import grab, main_window, pump, settle  # noqa: E402

from SciQLop.user_api.plot import create_plot_panel  # noqa: E402

mw = main_window("space")
panel = create_plot_panel()
panel.time_range = SHEATH_TO_MSPHERE
panel.plot(FGM_SRVY_GSM)
settle(panel)
mw._command_palette.toggle()
pump(1.5)
grab("sciqlop_command_palette.png")
