"""sciqlop_welcome.png: the welcome page."""
# needs: webengine
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from shotlib import grab, main_window, pump  # noqa: E402

mw = main_window("space")
welcome = mw.dock_manager.findDockWidget("Welcome")
welcome.toggleView(True)
welcome.raise_()
pump(15)  # the page loads the workspaces, templates and the plugin registry
grab("sciqlop_welcome.png")
