"""14: Products sidebar with "mms1 fgm" typed: the tree narrowed, with hit counts and coverage."""
import os
import sys

from PySide6.QtWidgets import QTextEdit, QTreeView

sys.path.insert(0, os.path.dirname(__file__))
from mms import FGM_SRVY_GSM, SHEATH_TO_MSPHERE  # noqa: E402
from shotlib import grab, main_window, pump, settle  # noqa: E402

from SciQLop.user_api.gui import show_product_tree  # noqa: E402
from SciQLop.user_api.plot import create_plot_panel  # noqa: E402

mw = main_window()
panel = create_plot_panel()
panel.time_range = SHEATH_TO_MSPHERE
panel.plot(FGM_SRVY_GSM)
settle(panel)
show_product_tree()
pump(1)
search = next(e for e in mw.productTree.findChildren(QTextEdit) if e.isVisible())  # a token box
search.setFocus()
search.setPlainText("mms1 fgm")
pump(8)  # the smart search ranks in the background
next(t for t in mw.productTree.findChildren(QTreeView) if t.isVisible()).expandAll()  # only the hits remain
pump(1)
grab("14-products-smart-search.png")
