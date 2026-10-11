"""Batch quick-looks tutorial: the PNG the first script writes, made by that script itself."""
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(__file__))
from shotlib import OUT, run_blocks, tutorial_code  # noqa: E402

quicklook, *_ = tutorial_code("Batch quick-looks")

sys.argv = ["quicklook.py", "2015-10-16"]
run_blocks([quicklook], {"__name__": "__main__"})
target = OUT / "batch quick-looks" / "mms1_2015-10-16.png"
target.parent.mkdir(parents=True, exist_ok=True)
shutil.move("mms1_2015-10-16.png", target)
print("saved", target)
