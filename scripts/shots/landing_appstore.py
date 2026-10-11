"""sciqlop_appstore.png: the Plugin Store."""
# needs: webengine
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from shotlib import grab, main_window, pump  # noqa: E402

mw = main_window("space")
mw._show_appstore()
pump(20)  # the store fetches the live registry and the plugin pictures
grab("sciqlop_appstore.png")
