"""Python user API tutorial: one panel per plotting example, from the page's own code. Each example
gets a fresh panel over the page's time window, so each picture shows that example alone."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from shotlib import main_window, pump, run_blocks, save_panel, settle, tutorial_code  # noqa: E402

from SciQLop.user_api import TimeRange  # noqa: E402
from SciQLop.user_api.plot import create_plot_panel  # noqa: E402

KEEP_OVERLAY = "b_plot.overlay.clear()"
blocks = tutorial_code("Python user API", {KEEP_OVERLAY: ""})
WINDOW = TimeRange("2015-10-16T10:00", "2015-10-16T16:00")


def fresh_panel(ns: dict) -> dict:
    ns["p"] = create_plot_panel()
    ns["p"].time_range = WINDOW
    return ns


def shot(ns: dict, name: str, panel_key: str = "p") -> None:
    settle(ns[panel_key])
    pump(2)
    save_panel(ns[panel_key], f"python user API/{name}.png")


main_window()
ns = run_blocks([blocks[0], blocks[1]], {})            # imports cheat sheet, a first panel
shot(ns, "api_first_panel")

for indices, name in [((9, 10), "api_plot_data"), ((12,), "api_plot_function"), ((13,), "api_waterfall"),
                      ((15,), "api_right_axis"), ((18,), "api_projection"), ((23,), "api_virtual_product")]:
    run_blocks([blocks[i] for i in indices], fresh_panel(ns))
    shot(ns, name)
    if name == "api_right_axis":
        run_blocks([blocks[19]], ns)                    # message over the plot, left shown
        shot(ns, "api_overlay_message")

run_blocks([blocks[21]], ns)                            # fluent builder
shot(ns, "api_fluent", "panel")
