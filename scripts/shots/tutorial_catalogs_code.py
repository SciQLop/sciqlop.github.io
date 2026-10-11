"""Catalogs tutorial, "Building a catalog from data": the catalog the code builds, as an overlay."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from shotlib import main_window, pump, run_blocks, save_panel, settle, tutorial_code  # noqa: E402

REMOVE = "overlay.remove()  # or panel.remove_catalog_overlay(overlay)"
build, overlay, *_ = tutorial_code("Catalogs", {REMOVE: ""})

main_window()
ns = run_blocks([build], {})
settle(ns["panel"])
run_blocks([overlay], ns)
pump(3)
save_panel(ns["panel"], "catalogs/catalog_from_data.png")
