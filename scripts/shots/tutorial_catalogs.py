"""The catalog-tab screenshots of the Catalogs tutorial (content/tutorials/catalogs/).
The two catalog_explorer*.png show a window SciQLop no longer has: the page keeps them as history."""
import os
import sys

from PySide6.QtCore import QItemSelectionModel, Qt
from PySide6.QtWidgets import QSplitter, QTableView, QTreeView

sys.path.insert(0, os.path.dirname(__file__))
from mms import DIS_FAST, FGM_SRVY_GSM  # noqa: E402
from shotlib import Arrow, by_tooltip, grab, main_window, pump, set_labels, settle, wait_until  # noqa: E402

from SciQLop.user_api import TimeRange  # noqa: E402
from SciQLop.user_api.catalogs import catalogs  # noqa: E402
from SciQLop.user_api.plot import create_plot_panel  # noqa: E402

CATALOG = "My Catalogs//MP crossings"
VIEW = TimeRange("2015-10-16T12:50", "2015-10-16T13:15")
ROUGH = ("2015-10-16T13:03:00", "2015-10-16T13:05:30")
PRECISE = ("2015-10-16T13:04:05", "2015-10-16T13:04:55")
MORE = [("2015-10-16T12:58:00", "2015-10-16T12:59:45"), ("2015-10-16T13:05:30", "2015-10-16T13:06:40")]
LABELS = [("y2", "Ion energy [eV]"), ("y", "B GSM [nT]"), ("y", "Ni [cm⁻³]"), ("y", "Vi GSE [km/s]")]
SUB = "catalogs/"

mw = main_window()
panel = create_plot_panel()
panel.time_range = VIEW
for product in ["mms1_dis_energyspectr_omni_fast", None, "mms1_dis_numberdensity_fast", "mms1_dis_bulkv_gse_fast"]:
    panel.plot(DIS_FAST + product if product else FGM_SRVY_GSM)
settle(panel)
browser = mw.catalogs_browser
tree = browser.findChildren(QTreeView)[0]
table = browser.findChildren(QTableView)[0]


def open_catalogs_dock():
    dock = mw.dock_manager.findDockWidget("Catalogs")
    dock.toggleView(True)
    dock.setAutoHide(False)  # pinned: the panel shrinks beside it instead of hiding under it
    dock.raise_()
    pump(0.5)
    splitter = dock.dockAreaWidget().parentWidget()
    splitter.setSizes([520, splitter.width() - 520])
    inner = browser.findChildren(QSplitter)[0]  # catalog tree | event table
    inner.setSizes([190, 330])
    pump(1)


def find_catalog(name: str):
    """Rows read "name *" while unsaved, hence the prefix match."""
    model = tree.model()
    mine = model.match(model.index(0, 0), Qt.DisplayRole, "My Catalogs", 1, Qt.MatchStartsWith)
    if not mine:
        return []
    tree.expand(mine[0])
    return model.match(model.index(0, 0, mine[0]), Qt.DisplayRole, name, 1, Qt.MatchStartsWith)


def select_catalog(name: str):
    wait_until(lambda: find_catalog(name), timeout=20, what=f"catalog {name!r} in the tree")
    tree.setCurrentIndex(find_catalog(name)[0])
    pump(1)


def shot(name, arrows=()):
    set_labels(panel, LABELS)
    grab(SUB + name, arrows)


open_catalogs_dock()
shot("catalog_noview_with_data.png")

catalogs.save(CATALOG, [])
pump(1)
select_catalog("MP crossings")
shot("catalog_view_with_data.png")

panel.add_catalog_overlay(CATALOG)
panel.catalog_mode = "edit"
pump(1)
mode = by_tooltip("Catalog interaction mode")
shot("catalog_view_config.png", [Arrow(mode, "Catalog mode: Edit", (mode.mapTo(mw, mode.rect().center()).x() - 330, 560),
                                       box=True)])

catalogs.save(CATALOG, [ROUGH])
pump(2)
shot("one_event.png")

panel.time_range = TimeRange("2015-10-16T13:03:30", "2015-10-16T13:05:30")
catalogs.save(CATALOG, [PRECISE])
settle(panel)
shot("one_event_zoomed.png")

panel.time_range = VIEW
catalogs.save(CATALOG, [PRECISE, *MORE])
settle(panel)
shot("three_events.png")

panel.catalog_mode = "jump"
pump(1)
table.sortByColumn(0, Qt.AscendingOrder)
table.selectionModel().setCurrentIndex(table.model().index(0, 0),
                                       QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows)
pump(1)
settle(panel)
print("jumped to", panel.time_range)
shot("jump_one_event.png")
catalogs.persist(CATALOG)
