"""basic plotting/welcome.png: the welcome page, its parts numbered as the tutorial lists them."""
# needs: webengine
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from shotlib import Arrow, grab, main_window, pump, web_element_rect, web_view  # noqa: E402

PARTS = [  # (number, CSS selector, label offset from the box's top-left, in logical px)
    ("1", "#primary-actions > :nth-child(1)", (-16, -16)),
    ("2", "#primary-actions > :nth-child(2)", (-16, -16)),
    ("3", "#primary-actions > :nth-child(3)", (-16, -16)),
    ("4", "#recent-workspaces", (-16, -16)),
    ("5", "#examples .section-header", (-16, -16)),
    ("6", "#templates .section-header", (-16, -16)),
    ("7", "#featured", (-16, -16)),
]

mw = main_window()
welcome = mw.dock_manager.findDockWidget("Welcome")
welcome.toggleView(True)
welcome.raise_()
pump(15)  # the page loads the workspaces, templates and the plugin registry
web_view(welcome).page().runJavaScript("document.getElementById('news-dismiss')?.click()")
pump(1)
arrows = []
for number, selector, (dx, dy) in PARTS:
    r = web_element_rect(welcome, selector)
    arrows.append(Arrow(r, number, (r.left() + dx, r.top() + dy), box=True))
grab("basic plotting/welcome.png", arrows)
