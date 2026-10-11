"""Graphic primitives tutorial: the panel after each step, from the tutorial's own code."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from shotlib import main_window, pump, run_blocks, save_panel, settle, tutorial_code  # noqa: E402

LOGO = "/home/jeandet/Documents/prog/SciQLop/SciQLop/resources/icons/SciQLop-150x150.png"
panel, marks, bands, ellipse, *_ = tutorial_code("Graphic primitives", {"/path/to/logo.png": LOGO})

main_window()
ns = run_blocks([panel], {})
settle(ns["p"])
run_blocks([marks], ns)
pump(1)
save_panel(ns["p"], "graphic primitives/primitives_marks.png")
run_blocks([bands], ns)
pump(1)
save_panel(ns["p"], "graphic primitives/primitives_bands.png")
run_blocks([ellipse], ns)
pump(3)  # the Pixmap shows up on a later repaint
save_panel(ns["p"], "graphic primitives/primitives_ellipse_pixmap.png")
