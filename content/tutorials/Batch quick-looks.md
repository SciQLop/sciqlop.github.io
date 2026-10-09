---
title: Batch quick-looks
---
# Quick-look plots from the command line

You have a panel you like. Now you want the same panel for every day of a month, as PNG files.
Batch mode does that. You write a short Python script, and SciQLop runs it with no window:

```bash
sciqlop --batch quicklook.py 2015-10-16
```

SciQLop starts, runs the script, and exits. There is no display to open, so it also runs over SSH, in a
container or from a cron job.

> [!note] Next release
> Batch mode ships with the next SciQLop release, after v0.14.1.

The script uses the same [[Python user API]] as the notebooks. If you can make the plot in a notebook, you can
make it in batch.

# Getting the `sciqlop` command

Batch mode needs the `sciqlop` command in a terminal. You get it from the Python package:

```bash
uv tool install sciqlop        # or: pip install sciqlop
```

From a source checkout, `uv run sciqlop --batch ...` works too.

> [!warning] Not from the installers
> The Windows installer, the macOS app and the AppImage don't pass `--batch` on yet. They open the normal
> window instead. Use the Python package for batch runs.

On Windows, use `sciqlop-console` instead of `sciqlop`. It keeps the console, so you see the script's output.

# A first quick-look

Save this as `quicklook.py`:

```python
import sys
from SciQLop.user_api.plot import create_plot_panel

FGM = "speasy//cda//MMS//MMS1//FGM//MMS1_FGM_SRVY_L2//mms1_fgm_b_gse_srvy_l2"
DENSITY = "speasy//cda//MMS//MMS1//DIS//MMS1_FPI_FAST_L2_DIS_MOMS//mms1_dis_numberdensity_fast"

day = sys.argv[1]

panel = create_plot_panel()
panel.plot(FGM)
panel.plot(DENSITY)
panel.time_range = (f"{day}T00:00", f"{day}T23:59:59")
panel.settle(timeout=300)
panel.save(f"mms1_{day}.png")
```

Run it:

```bash
sciqlop --batch quicklook.py 2015-10-16
```

You get `mms1_2015-10-16.png` in the folder you ran the command from.

Three things happen in that script:

1. `panel.time_range = ...` asks for the data. The download starts in the background.
2. `panel.settle(...)` waits until the panel shows that data: downloaded, drawn and rescaled.
3. `panel.save(...)` writes the image. `.png`, `.pdf`, `.jpg` and `.bmp` work, picked from the extension.

> [!tip] Always `settle()` before `save()`
> Without it, you save the panel while it is still loading. The image shows empty plots, or the previous
> time range.

The easiest way to get a product path is to drag the product from the product tree into a notebook cell.
See [[Python user API#Product paths|Product paths]].

# Many days in one run

Starting SciQLop takes a few seconds. So make one run produce many images: build the panel once, then
move it in time.

```python
import sys
from datetime import datetime, timedelta
from SciQLop.user_api.plot import create_plot_panel

FGM = "speasy//cda//MMS//MMS1//FGM//MMS1_FGM_SRVY_L2//mms1_fgm_b_gse_srvy_l2"
DENSITY = "speasy//cda//MMS//MMS1//DIS//MMS1_FPI_FAST_L2_DIS_MOMS//mms1_dis_numberdensity_fast"

first_day = datetime.fromisoformat(sys.argv[1])
n_days = int(sys.argv[2])

panel = create_plot_panel()
panel.plot(FGM)
panel.plot(DENSITY)

for i in range(n_days):
    start = first_day + timedelta(days=i)
    panel.time_range = (start, start + timedelta(days=1))
    panel.settle(timeout=300)
    panel.save(f"mms1_{start:%Y%m%d}.png")
    print("saved", start.date())
```

```bash
sciqlop --batch quicklooks.py 2015-10-01 31
```

That is one image per day for October 2015.

> [!tip] Spans wider than a day
> New panels don't zoom out past one day by default. For weekly plots, raise the limit first:
> ```python
> panel.zoom_limit_seconds = 7 * 86400
> ```

Tip: try the panel in a notebook first. Once it looks right, copy the cells into the script.

# The command line

```bash
sciqlop [-w WORKSPACE] [--webengine] --batch SCRIPT [ARGS...]
```

- **Everything after the script name goes to the script**, in `sys.argv`. So SciQLop's own options, like
  `-w`, go *before* `--batch`.
- **`-w WORKSPACE`** picks the workspace, as usual. A workspace made for your quick-looks is a good idea. The
  script then runs with that workspace's packages and plugins.
- **Relative paths** are relative to the folder you ran the command from, not to the workspace.
- **The exit code is the script's.** A script that ends normally exits with `0`. `sys.exit(3)` exits with
  `3`. An uncaught exception prints its traceback and exits with `1`.

That last point makes failures easy to catch. If the data takes too long, `settle(timeout=300)` raises
`TimeoutError`. The run then exits with `1`, and your shell script or cron job sees it.

If you'd rather skip a slow day than stop, use `panel.wait_for_data(timeout=300)` instead. It returns `False`
on timeout and doesn't raise.

# Running without a screen

Batch mode draws offscreen. It needs no X server, no Wayland, no `DISPLAY`. So it works:

- over SSH, on a remote machine;
- in a container;
- from a cron job.

A nightly quick-look of yesterday, from cron:

```bash
0 6 * * * cd /data/quicklooks && sciqlop -w quicklooks --batch quicklook.py $(date -d yesterday +\%F) >> ql.log 2>&1
```

To use a real display anyway, set `QT_QPA_PLATFORM` yourself. SciQLop respects it.

# What is different from a normal session

- **No embedded browser.** Batch mode doesn't start Chromium. It is only needed by the welcome page, the
  plugin store and the agent chat, so a quick-look script never misses it. If your script needs it, put
  `--webengine` before `--batch`.
- **No questions at exit.** When the script ends, SciQLop quits like a normal close: plugins shut down and save
  their state. But it doesn't ask about running jobs or unsaved catalogs. It prints a warning instead, naming
  the catalogs whose unsaved changes are lost. If your script edits catalogs, save them in the script.
- **The first run of a workspace is slow.** SciQLop installs the workspace's Python environment first, as in
  a normal start. Later runs reuse it.
- **Downloads are cached.** Speasy keeps what it fetched. Running the same days again is much faster.
