"""Helpers shared by the shot scripts: window setup, waiting, capture, annotations.

Shot scripts run inside SciQLop (`sciqlop --batch`), so they use the public
SciQLop.user_api wherever it exists. Staging a GUI state the API does not cover
(opening a menu, typing in a search box) reaches into widgets here, in one place.
"""
from __future__ import annotations

import math
import os
import time
from dataclasses import dataclass
from pathlib import Path

from PySide6.QtCore import QCoreApplication, QPoint, QPointF, QRect, QRectF, Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPainterPath, QPen, QPolygonF
from PySide6.QtWidgets import QTreeView, QWidget

from SciQLop.user_api import themes
from SciQLop.user_api.gui import get_main_window

OUT = Path(os.environ.get("SHOTS_OUT", "."))
WINDOW_SIZE = (1470, 923)  # logical px; 2940x1846 at scale 2, the size of the Mac shots
ACCENT = QColor("#ff5a4e")


def pump(seconds: float = 0.5) -> None:
    end = time.monotonic() + seconds
    while time.monotonic() < end:
        QCoreApplication.processEvents()
        time.sleep(0.01)


def wait_until(predicate, timeout: float = 30.0, what: str = "condition") -> None:
    end = time.monotonic() + timeout
    while time.monotonic() < end:
        QCoreApplication.processEvents()
        if predicate():
            return
        time.sleep(0.02)
    raise TimeoutError(f"{what} not met after {timeout} s")


def open_jupyterlab() -> QWidget:
    """Open the JupyterLab dock and wait for Lab's page; needs `# needs: webengine`."""
    mw = get_main_window()
    mw.open_jupyterlab_widget()
    wait_until(lambda: mw.dock_manager.findDockWidget("SciQLop JupyterLab") is not None, timeout=120,
               what="the JupyterLab dock")
    pump(20)  # Lab's own page load
    return mw.dock_manager.findDockWidget("SciQLop JupyterLab")


def lab_view(lab_dock: QWidget):
    from PySide6.QtWebEngineWidgets import QWebEngineView
    return lab_dock.findChildren(QWebEngineView)[0]


def toggle_lab_sidebar(lab_dock: QWidget) -> None:
    """Ctrl+B, Lab's "toggle left area" shortcut. Clicking the side-bar tab doesn't work:
    Lumino tabs listen for pointer events, not clicks."""
    lab_view(lab_dock).page().runJavaScript(
        "document.activeElement.dispatchEvent(new KeyboardEvent('keydown',"
        " {key: 'b', code: 'KeyB', keyCode: 66, ctrlKey: true, bubbles: true}))")
    pump(1)


def lab_element_rect(lab_dock: QWidget, selector: str) -> QRect:
    """Window rect of the first element matching `selector` in Lab's page."""
    found = []
    lab_view(lab_dock).page().runJavaScript(
        f"(r => [r.x, r.y, r.width, r.height].join(','))(document.querySelector({selector!r}).getBoundingClientRect())",
        0, found.append)
    wait_until(lambda: found, what=f"Lab element {selector}")
    x, y, w, h = map(float, found[0].split(","))  # a JS array would arrive empty
    origin = rect_in_window(lab_view(lab_dock)).topLeft()
    return QRect(origin.x() + int(x), origin.y() + int(y), int(w), int(h))


def main_window(theme: str = "dark"):
    themes.apply_theme(theme)
    mw = get_main_window()
    mw.resize(*WINDOW_SIZE)
    mw.show()
    pump(1.0)
    return mw


def settle(panel, timeout: float = 300) -> None:
    panel.settle(timeout=timeout)
    pump(0.5)


def set_labels(panel, labels: list[tuple[str, str]]) -> None:
    """(axis, text) per plot, in order. Spectrograms carry their data on "y2", the
    right-hand axis."""
    for plot, (axis, text) in zip(panel.plots, labels):
        plot.set_axis_label(axis, text)
    pump(0.3)


def save_panel(panel, name: str) -> Path:
    # Not panel.save(): it exports at logical size, half resolution on a HiDPI screen, and its
    # scale argument re-lays the panel out bigger instead (reported to SciQLop 2026-10-11).
    # A widget grab is what the screen shows. Go back to panel.save() once it honours the DPR.
    pump(0.5)
    path = OUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    if not panel._get_impl_or_raise().grab().save(str(path)):
        raise OSError(f"failed to save {path}")
    print("saved", path)
    return path


def hide_empty_panel_overlays() -> None:
    from SciQLop.components.plotting.ui.product_search_overlay import ProductSearchOverlay
    for overlay in get_main_window().findChildren(ProductSearchOverlay):
        overlay.hide()
    pump(0.3)


def select_in_inspector(text: str) -> None:
    """Select the Properties tree row showing `text`, as a click on it would."""
    from PySide6.QtCore import QItemSelectionModel
    from PySide6.QtWidgets import QTreeView
    from SciQLop.user_api.gui import show_inspector
    show_inspector()
    pump(0.5)
    view = get_main_window().properties_panel.findChild(QTreeView)
    view.expandAll()
    model = view.model()
    hits = model.match(model.index(0, 0), Qt.DisplayRole, text, 1, Qt.MatchExactly | Qt.MatchRecursive)
    if not hits:
        raise LookupError(f"no {text!r} row in the Properties tree")
    view.selectionModel().select(hits[0], QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows)
    view.setCurrentIndex(hits[0])
    pump(1.0)


def side_tab(dock_title: str) -> QWidget:
    """The left side-bar button of an auto-hiding dock."""
    return get_main_window().dock_manager.findDockWidget(dock_title).sideTabWidget()


def collapse_dock(dock_title: str) -> None:
    dock = get_main_window().dock_manager.findDockWidget(dock_title)
    container = dock.autoHideDockContainer()
    if container is not None:
        container.collapseView(True)
    pump(0.5)


def new_panel_button() -> QWidget:
    from SciQLop.components.onboarding.backend.targets import resolve_add_panel_button
    return resolve_add_panel_button(get_main_window(), {})


def by_tooltip(title: str, root: QWidget | None = None) -> QWidget:
    """The visible widget whose rich tooltip starts with <b>title</b>."""
    root = root or get_main_window()
    for w in root.findChildren(QWidget):
        if w.isVisible() and w.toolTip().startswith(f"<b>{title}</b>"):
            return w
    raise LookupError(f"no visible widget with tooltip {title!r}")


def product_row(path: list[str], select: bool = True) -> QRect:
    """Reveal a product in the Products tree; its row's rectangle in window coordinates."""
    from PySide6.QtCore import QItemSelectionModel
    from SciQLop.components.onboarding.backend.targets import _expand_ancestors, find_index_by_path
    from SciQLop.user_api.gui import show_product_tree
    show_product_tree()
    pump(0.5)
    tree = next(t for t in get_main_window().productTree.findChildren(QTreeView) if t.isVisible())
    index = find_index_by_path(tree.model(), path)
    if index is None:
        raise LookupError(f"no product {'//'.join(path)!r} in the tree")
    _expand_ancestors(tree, index)
    tree.scrollTo(index)
    if select:
        tree.selectionModel().select(index, QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows)
    pump(0.5)
    row = tree.visualRect(index)
    return QRect(tree.viewport().mapTo(get_main_window(), row.topLeft()), row.size())


def rect_in_window(widget: QWidget) -> QRect:
    mw = get_main_window()
    return QRect(widget.mapTo(mw, QPoint(0, 0)), QWidget.size(widget))  # panels redefine size()


def find(cls=QWidget, name: str | None = None, text: str | None = None,
         visible: bool = True, root: QWidget | None = None) -> QWidget:
    """The first child widget of the main window matching class, objectName and text."""
    root = root or get_main_window()
    for w in root.findChildren(cls):
        if visible and not w.isVisible():
            continue
        if name is not None and w.objectName() != name:
            continue
        if text is not None and getattr(w, "text", lambda: None)() != text:
            continue
        return w
    raise LookupError(f"no visible {cls.__name__} name={name!r} text={text!r}")


@dataclass
class Arrow:
    """A label at `label_at` with an arrow to `target` (a widget, a QRect or a QPoint),
    all in logical window coordinates."""
    target: object
    label: str
    label_at: tuple[float, float]
    box: bool = False


def _target_rect(target) -> QRectF:
    if isinstance(target, QWidget):
        return QRectF(rect_in_window(target))
    if isinstance(target, QRect):
        return QRectF(target)
    return QRectF(QPointF(target), QPointF(target))


def _edge_point(rect: QRectF, toward: QPointF, margin: float = 6) -> QPointF:
    """Where a line from `toward` to the rect centre crosses the rect border, pulled out a little."""
    c = rect.center()
    dx, dy = toward.x() - c.x(), toward.y() - c.y()
    if dx == 0 and dy == 0:
        return c
    hw, hh = rect.width() / 2 + margin, rect.height() / 2 + margin
    s = min(hw / abs(dx) if dx else math.inf, hh / abs(dy) if dy else math.inf)
    return QPointF(c.x() + dx * s, c.y() + dy * s)


def _draw_arrow(p: QPainter, start: QPointF, end: QPointF) -> None:
    p.drawLine(start, end)
    angle = math.atan2(end.y() - start.y(), end.x() - start.x())
    size = 14
    head = QPolygonF([end,
                      QPointF(end.x() - size * math.cos(angle - 0.4), end.y() - size * math.sin(angle - 0.4)),
                      QPointF(end.x() - size * math.cos(angle + 0.4), end.y() - size * math.sin(angle + 0.4))])
    p.setBrush(ACCENT)
    p.drawPolygon(head)


def annotate(pixmap, arrows: list[Arrow]) -> None:
    p = QPainter(pixmap)
    p.setRenderHint(QPainter.Antialiasing)
    font = QFont(p.font())
    font.setPointSizeF(20)
    font.setBold(True)
    p.setFont(font)
    for a in arrows:
        rect = _target_rect(a.target)
        label = QRectF(0, 0, 600, 200)
        bounds = p.boundingRect(label, Qt.AlignLeft | Qt.AlignTop, a.label)
        bounds.moveCenter(QPointF(*a.label_at))
        _draw_label(p, bounds, a.label)
        p.setPen(QPen(ACCENT, 3.5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        if a.box:
            p.setBrush(Qt.NoBrush)
            p.drawRoundedRect(rect.adjusted(-4, -4, 4, 4), 6, 6)
        start = _edge_point(bounds, rect.center(), margin=8)
        end = _edge_point(rect, bounds.center(), margin=6 if not a.box else 10)
        _draw_arrow(p, start, end)
    p.end()


def _draw_label(p: QPainter, bounds: QRectF, text: str) -> None:
    pad = 8
    bg = bounds.adjusted(-pad, -pad / 2, pad, pad / 2)
    path = QPainterPath()
    path.addRoundedRect(bg, 8, 8)
    p.fillPath(path, QColor(20, 20, 20, 210))
    p.setBrush(Qt.NoBrush)
    p.setPen(QPen(ACCENT, 2))
    p.drawPath(path)
    p.setPen(QColor("white"))
    p.drawText(bounds, Qt.AlignCenter, text)


def grab(name: str, arrows: list[Arrow] = ()) -> Path:
    pump(0.5)
    pixmap = get_main_window().grab()
    if arrows:
        annotate(pixmap, list(arrows))
    path = OUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    if not pixmap.save(str(path)):
        raise OSError(f"failed to save {path}")
    print("saved", path, pixmap.width(), "x", pixmap.height())
    return path
