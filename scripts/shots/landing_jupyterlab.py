"""sciqlop_jupyterlab_plot_side_by_side.png: JupyterLab and a plot panel, side by side."""
# needs: webengine
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from mms import DIS_FAST, FGM_SRVY_GSM  # noqa: E402
from shotlib import grab, main_window, pump, settle, wait_until  # noqa: E402

from PySide6QtAds import RightDockWidgetArea  # noqa: E402
from SciQLop.user_api import TimeRange  # noqa: E402
from SciQLop.user_api.plot import create_plot_panel  # noqa: E402

mw = main_window("space")
mw.open_jupyterlab_widget()
wait_until(lambda: mw.dock_manager.findDockWidget("SciQLop JupyterLab") is not None, timeout=120,
           what="the JupyterLab dock")
pump(20)  # JupyterLab's own page load
panel = create_plot_panel()
panel.time_range = TimeRange("2015-11-18T02:14:30", "2015-11-18T03:34:00")
panel.plot(FGM_SRVY_GSM)
panel.plot(DIS_FAST + "mms1_dis_bulkv_gse_fast")
panel.plot(DIS_FAST + "mms1_dis_numberdensity_fast")
settle(panel)
dock = next(d for d in mw.dock_manager.dockWidgetsMap().values() if d.widget() is panel._impl)
mw.dock_manager.addDockWidget(RightDockWidgetArea, dock)
pump(3)
grab("sciqlop_jupyterlab_plot_side_by_side.png")
