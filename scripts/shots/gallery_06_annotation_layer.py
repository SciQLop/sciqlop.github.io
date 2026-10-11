"""06: a data-aware annotation layer marking the magnetosheath where N_i > threshold."""
import os
import sys
from typing import Annotated

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from mms import BURCH_EDR, DIS_BRST, FGM_BRST_GSM  # noqa: E402
from shotlib import main_window, set_labels, pump, save_panel, settle  # noqa: E402

from SciQLop.user_api.knobs import Knob  # noqa: E402
from SciQLop.user_api.layers import HLine, Marker, Scalar, Span, register_layer  # noqa: E402
from SciQLop.user_api.plot import create_plot_panel  # noqa: E402


@register_layer("detectors/magnetosheath", scope="panel")
def magnetosheath(
    data: Scalar,
    threshold: Annotated[float, Knob(min=0.0, max=50.0, step=0.5, unit="cm^-3")] = 5.0,
) -> list[Marker | Span | HLine]:
    n = data.values[:, 0]
    t = data.time
    if n.size < 2:
        return []
    inside = (n > threshold).astype(np.int8)
    crossings = np.flatnonzero(np.diff(inside)) + 1
    edges = np.flatnonzero(np.diff(np.concatenate([[0], inside, [0]])))
    spans = [Span(start=float(t[a]), stop=float(t[b - 1]), label="magnetosheath")
             for a, b in zip(edges[::2], edges[1::2])]
    markers = [Marker(time=float(t[i]), value=float(n[i])) for i in crossings]
    return spans + markers + [HLine(value=threshold, color="#e74c3c")]


main_window()
panel = create_plot_panel()
panel.time_range = BURCH_EDR
panel.plot(DIS_BRST + "mms1_dis_energyspectr_omni_brst")
panel.plot(FGM_BRST_GSM)
panel.plot(DIS_BRST + "mms1_dis_numberdensity_brst")
settle(panel)
layer = panel.add_layer(magnetosheath, plot_index=2, scope="panel", threshold=5.0)
pump(3)
if layer.last_error:
    raise RuntimeError(f"layer failed: {layer.last_error}")
set_labels(panel, [("y2", "Ion energy [eV]"), ("y", "B GSM [nT]"), ("y", "Ni [cm⁻³]")])
save_panel(panel, "06-annotation-layer-detector.png")
