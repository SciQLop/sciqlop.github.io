"""DSP toolbox tutorial: raw vs low-passed field, then the spectrogram virtual product."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from shotlib import main_window, run_blocks, save_panel, settle, tutorial_code  # noqa: E402

imports, lowpass, register, panel, helpers, spectrogram, *_ = tutorial_code("DSP toolbox")

main_window()
ns = run_blocks([imports, lowpass, register, panel], {})
settle(ns["p"])
save_panel(ns["p"], "dsp toolbox/dsp_lowpass.png")
run_blocks([spectrogram], ns)
settle(ns["p"])
save_panel(ns["p"], "dsp toolbox/dsp_spectrogram.png")
