"""2D histograms tutorial: the density/T_perp histogram, then the static-arrays one."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from shotlib import main_window, pump, run_blocks, save_panel, settle, tutorial_code  # noqa: E402

callback, static, *_ = tutorial_code("2D histograms")

main_window()
ns = run_blocks([callback], {})
settle(ns["p"])
pump(3)  # the histogram callback runs after the time series fetch
save_panel(ns["p"], "2D histograms/hist2d_density_tperp.png")
run_blocks([static], ns)
pump(2)
save_panel(ns["p2"], "2D histograms/hist2d_static.png")
