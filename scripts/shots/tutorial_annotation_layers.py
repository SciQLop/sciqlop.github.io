"""Annotation layers tutorial: the magnetosheath layer attached to the panel."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from shotlib import main_window, pump, run_blocks, save_panel, settle, tutorial_code  # noqa: E402

types, panel, layer, attach, *_ = tutorial_code("Annotation layers")

main_window()
ns = run_blocks([panel], {})
settle(ns["p"])
run_blocks([layer, attach], ns)
pump(3)
if ns["layer"].last_error:
    raise RuntimeError(f"layer failed: {ns['layer'].last_error}")
save_panel(ns["p"], "annotation layers/layer_magnetosheath.png")
