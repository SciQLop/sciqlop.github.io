# Website screenshots, by script

Each `*.py` here is one shot (or a few related ones). It runs inside SciQLop with batch mode
(`sciqlop --batch`), builds the state it shows with the public `SciQLop.user_api`, and saves PNGs.

```bash
scripts/shots/run.sh                       # every shot
scripts/shots/run.sh gallery_01_hero ...   # some shots
```

- SciQLop comes from the checkout next to this repo (`../SciQLop`, override with `SCIQLOP=`), run with `uv run`.
- Each shot runs under Xvfb at scale 2 (2940×1846 window) with a fresh SciQLop profile in `.state/`:
  no personal catalogs, settings or tours leak in. The Speasy config and cache are shared.
- Output lands in `out/` with a `.log` per shot. Look at every image before copying it into `content/`.
- `shotlib.py`: window setup, waiting, captures, red annotation arrows. `mms.py`, `callisto.py`: shared data.
- A shot needing the embedded browser says `# needs: webengine` in its header.

A shot that fails or looks wrong is a SciQLop bug until shown otherwise: report it with the script as the
reproducer. Workarounds in the scripts are marked "reported 2026-10-11"; drop them once SciQLop is fixed.

Not scriptable yet: `landing_jupyterlab.py` (JupyterLab won't start in batch mode). Their old images
stay on the site. The AI-assistant shot, the GIFs and the two old catalog-explorer shots are made by hand.
