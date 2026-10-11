"""virtual products/jupyterlab.png: JupyterLab's launcher, where a new notebook starts."""
# needs: webengine
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from shotlib import Arrow, grab, lab_element_rect, main_window, open_jupyterlab, toggle_lab_sidebar  # noqa: E402

main_window()
lab = open_jupyterlab()
toggle_lab_sidebar(lab)
notebook_card = lab_element_rect(lab, ".jp-Launcher-section .jp-LauncherCard")
grab("virtual products/jupyterlab.png",
     [Arrow(notebook_card, "new notebook", (notebook_card.right() + 140, notebook_card.center().y()), box=True)])
