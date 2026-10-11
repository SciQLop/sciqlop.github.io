"""sciqlop_jupyterlab_plot_side_by_side.png: a notebook in JupyterLab and the panel its code builds."""
# needs: webengine
import json
import os
import sys

from PySide6.QtCore import QUrl

sys.path.insert(0, os.path.dirname(__file__))
from shotlib import grab, lab_view, main_window, open_jupyterlab, pump, settle, toggle_lab_sidebar  # noqa: E402

from PySide6QtAds import RightDockWidgetArea  # noqa: E402

NOTEBOOK = "mms_quicklook.ipynb"
CELLS = [
    ("markdown", "## MMS1 quick look, 2015-11-18\n\nField, ion velocity and density in one panel."),
    ("code", "from SciQLop.user_api import TimeRange\nfrom SciQLop.user_api.plot import create_plot_panel"),
    ("code", '''mms1 = "speasy//cda//MMS//MMS1//"
fgm = mms1 + "FGM//MMS1_FGM_SRVY_L2//"
dis = mms1 + "DIS//MMS1_FPI_FAST_L2_DIS_MOMS//"'''),
    ("code", '''panel = create_plot_panel()
panel.time_range = TimeRange("2015-11-18T02:14:30",
                             "2015-11-18T03:34:00")
panel.plot(fgm + "mms1_fgm_b_gsm_srvy_l2")
panel.plot(dis + "mms1_dis_bulkv_gse_fast")
panel.plot(dis + "mms1_dis_numberdensity_fast")'''),
]


def write_notebook(path: str) -> None:
    cells = [{"cell_type": kind, "metadata": {}, "source": src,
              **({"outputs": [], "execution_count": n} if kind == "code" else {})}
             for n, (kind, src) in enumerate(CELLS)]
    nb = {"cells": cells, "metadata": {"kernelspec": {"name": "python3", "display_name": "Python 3"}},
          "nbformat": 4, "nbformat_minor": 5}
    with open(path, "w") as f:
        json.dump(nb, f)


def open_in_lab(lab_dock, path: str) -> None:
    view = lab_view(lab_dock)
    view.setUrl(QUrl(view.url().toString().replace("/lab", f"/lab/tree/{path}")))


def build_panel_from_notebook_code():
    namespace = {}
    for kind, src in CELLS:
        if kind == "code":
            exec(src, namespace)
    return namespace["panel"]


mw = main_window("space")
lab = open_jupyterlab()
write_notebook(NOTEBOOK)  # starting Jupyter moved us into the workspace, the server's root
open_in_lab(lab, NOTEBOOK)
pump(15)
toggle_lab_sidebar(lab)
panel = build_panel_from_notebook_code()
settle(panel)
dock = mw.dock_manager.findDockWidget(panel.name)
mw.dock_manager.addDockWidget(RightDockWidgetArea, dock)
pump(1)
splitter = lab.dockAreaWidget().parentWidget()
splitter.setSizes([int(splitter.width() * 0.5), int(splitter.width() * 0.5)])
pump(3)
grab("sciqlop_jupyterlab_plot_side_by_side.png")
