"""13: a freshly created panel, with its product search box and drop target."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from shotlib import grab, main_window, pump  # noqa: E402

from SciQLop.user_api.plot import create_plot_panel  # noqa: E402

main_window()
create_plot_panel()
pump(2)
grab("13-empty-panel-search-overlay.png")
