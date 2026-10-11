"""Python API reference: one panel per plotting example, from the pages' own code. Each example gets
a fresh panel over the pages' time window, so each picture shows that example alone."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from shotlib import main_window, pump, run_blocks, save_panel, settle, tutorial_code  # noqa: E402

from SciQLop.user_api import TimeRange  # noqa: E402
from SciQLop.user_api.plot import create_plot_panel  # noqa: E402

basics = tutorial_code("Python API")
plotting = tutorial_code("Plotting")
plots = tutorial_code("Plots and graphs", {"b_plot.overlay.clear()": ""})  # keep the message shown
vps = tutorial_code("Virtual products and knobs")
WINDOW = TimeRange("2015-10-16T10:00", "2015-10-16T16:00")
EXAMPLES = [
    ([plotting[3], plotting[4]], "api_plot_data"),
    ([plotting[6]], "api_plot_function"),
    ([plotting[7]], "api_waterfall"),
    ([plots[0]], "api_right_axis"),
    ([plots[4]], "api_overlay_message"),   # on the right-axis panel, see below
    ([plots[3]], "api_projection"),
    ([vps[1]], "api_virtual_product"),
]


def fresh_panel(ns: dict) -> dict:
    ns["p"] = create_plot_panel()
    ns["p"].time_range = WINDOW
    return ns


def shot(ns: dict, name: str, panel_key: str = "p") -> None:
    settle(ns[panel_key])
    pump(2)
    save_panel(ns[panel_key], f"Python API/screenshots/{name}.png")


main_window()
ns = run_blocks([basics[0], basics[1]], {})            # imports cheat sheet, a first panel
shot(ns, "api_first_panel")
for blocks, name in EXAMPLES:
    run_blocks(blocks, ns if name == "api_overlay_message" else fresh_panel(ns))
    shot(ns, name)
run_blocks([plotting[9]], ns)                          # fluent builder
shot(ns, "api_fluent", "panel")
