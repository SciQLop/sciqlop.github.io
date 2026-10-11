"""12b: the guided tour's "Add more data" step over a live plot, Products dock open.

The tour is played the way a user would: it remembers the panel created during its
"create a plot panel" step, and later steps point at that panel."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from mms import FGM_SRVY_GSM, SHEATH_TO_MSPHERE  # noqa: E402
from shotlib import grab, main_window, pump, settle, wait_until  # noqa: E402

from SciQLop.components.onboarding.ui.tour_controller import run_tour  # noqa: E402
from SciQLop.user_api.gui import show_product_tree  # noqa: E402
from SciQLop.user_api.plot import create_plot_panel  # noqa: E402

mw = main_window()
tour = run_tour(mw, "getting_started")
pump(1)
panel = None


def step() -> str:
    return tour._current_step().step_id


def do_step():
    global panel
    if step() == "create_panel":
        panel = create_plot_panel()
    elif step() == "plot_product":
        panel.time_range = SHEATH_TO_MSPHERE
        panel.plot(FGM_SRVY_GSM)
        settle(panel)
    else:
        tour._advance()


while step() != "add_more_data":
    before = step()
    print("tour step:", before)
    do_step()
    wait_until(lambda: tour.is_finished or step() != before, timeout=30, what=f"leaving {before}")
    if tour.is_finished:
        raise RuntimeError("the tour ended before its 'add_more_data' step")
    pump(0.5)
show_product_tree()
pump(1.5)
grab("12b-guided-tour-add-more-data.png")
tour.abort()
