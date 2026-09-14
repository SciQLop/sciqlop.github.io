# Gallery shoot, round 2 — messages for the in-app SciQLop agent

Written 2026-09-13, two review rounds with opencode. Companion to `HANDOVER.md` and
`content/gallery/SOURCES.md`. The August shoot left three gaps that the kernel alone could
not stage: the AI-assistant dock mid-conversation, the guided-tour coach mark, and shot 07
whose Inspector knobs were unlabelled at the time (fixed in SciQLop `bfb6cf6a2`). The agent
that lives in the chat dock can stage all three, because it *is* the live conversation.

Every API named below was checked against SciQLop 0.13.0.dev0 on 2026-09-13
(`user_api/`, `core/ui/mainwindow.py`, `components/onboarding/`,
`components/agents/tools/_builder.py`). Two facts shape the rules: `capture_window` is a
`QWidget.grab()` of the main window, and the coach mark and command palette are child
widgets of it, so they appear in the grab; and the `main_window` name in the kernel is a
main-thread proxy, so anything private reached through it must run inside an
`on_main_thread` function.

## Operator, by hand, before message 1

The agent cannot do any of this.

- SciQLop 0.13.0.dev0 at or after `bfb6cf6a2`, fresh start, no panels open.
- Window 1600×1000 logical (the August convention, see `SOURCES.md`), theme `dark`.
- Products dock open on the left, Properties dock closed.
- Agents dock open and docked on the right. It appears in every full-window capture and is
  the subject of shot 11, so place it where you want it.
- `mkdir -p ~/sciqlop-website-shots`

Send the messages one at a time. Message 1 is deliberately short and natural: it is the
conversation shot 11 will show.

## Message 1

```
Plot the Burch et al. 2016 MMS1 EDR event, 2015-10-16 13:05:25 to 13:07:35, in one new panel: FGM burst B GSM, FPI-DIS burst ion density, ion bulk velocity GSE, and the omni ion energy spectrogram, stacked in that order.
```

Check the panel by eye. If something is wrong, fix it with a short natural follow-up; that
exchange will be visible in shot 11 and that is fine.

## Message 2

```
Good. Now a screenshot job. Rules first, then the shots.

Rules
1. Never fake a shot. If one cannot be produced from inside the app, say why, mark it skipped, move on.
2. Capture with `from SciQLop.user_api.screenshot import capture_window` inside sciqlop_exec_python. capture_window(path) saves the whole main window including docks, the command palette and tour bubbles. Save into ~/sciqlop-website-shots/ with the exact filenames below. sciqlop_screenshot_panel does not save a file; use it only to check plots.
3. Prefer SciQLop.user_api. Anything else goes through this helper, defined once, and nothing private is touched outside it:
     from SciQLop.user_api.threading import on_main_thread, unwrap
     @on_main_thread
     def gui(fn):
         return fn(unwrap(main_window))
     def show_dock(mw, title):
         dw = mw.dock_manager.findDockWidget(title)
         if dw is None:
             raise LookupError(f"no dock titled {title!r}")
         dw.toggleView(True); dw.raise_()
   Allowed inside gui(): run_tour and the controller's abort() (see shot C), show_dock. No window resizing, no synthetic key presses, no typing into widgets.
4. Product paths for plot_product come from sciqlop_products_tree (//-joined). Inside a virtual-product callback, spz.get_data needs the speasy id instead: take spz_uid from sciqlop_speasy_inventory. The two forms are not interchangeable.
5. After every plot_product, sciqlop_wait_for_plot_data on that panel, then look with sciqlop_screenshot_panel. Empty or half-loaded is a failed shot: retry once, then skipped. Do not call sciqlop_wait_for_plot_data on an empty panel, it errors.
6. Leave no trace: note current_theme() at start and restore it at the end; virtual products only under the demo/ prefix (there is no public call to remove one, list them in the report); never call catalogs.create, catalogs.save, add_events or remove_events; close every panel you created except the one from my first message.

Shots, in this order

A. 11-ai-assistant-dock.png — capture_window right now, before anything else changes. The panel from my first message and this conversation are the subject.

B. 13-empty-panel-search-overlay.png — sciqlop_create_panel, then in one exec_python cell: time.sleep(2) so the built-in search overlay has appeared, then capture_window. Close that panel.

C. 12-guided-tour-coach-mark.png — in exec_python:
     from SciQLop.components.onboarding.ui.tour_controller import run_tour
     ctl = gui(lambda mw: run_tour(mw, "getting_started"))
     time.sleep(1); capture_window(...)
     gui(lambda mw: ctl.abort())
   Tell me in the report that abort() marks the tour completed in the onboarding settings, so it will not offer itself again on this install; Tools → Take a tour replays it.

D. Staging for 07-knobs-parameterized-virtual-product.png, do not capture yet. Create the virtual product demo/Bmag_smoothed with create_virtual_product(path, callback, VirtualProductType.Scalar, labels=["|B| smoothed"]): the callback fetches mms1_fgm_b_gsm_brst_l2 with spz.get_data, takes the magnitude of the first three components, smooths it with a boxcar whose width is a knob, and has a second knob drawn as a horizontal line:
     smooth_window: Annotated[int, Knob(min=1, max=200, step=1, label="Smooth window", unit="samples")] = 16
     threshold: Annotated[float, Knob(widget="hline", min=0.0, max=80.0, step=1.0, label="Threshold", unit="nT", color="#e74c3c")] = 25.0
   Follow examples/tutorials/SciQLop/15-SciQLopParameterizedVirtualProducts.ipynb. Then a NEW panel: sciqlop_set_time_range to the same window as the first panel, B GSM on top, demo/Bmag_smoothed below, wait for data. user_api.gui.show_inspector(). Then stop and tell me it is staged: I will click the smoothed graph so the Inspector shows its Parameters section, and ask you to capture.

Report
A table with one row per file in the SOURCES.md format: file, event/data, interval, products (exact tree paths), feature shown. Then: status per shot (ok / skipped: reason), theme restored to, virtual products created, panels still open. Finally any user_api call you needed and could not find.
```

## Message 3, after you clicked the smoothed graph

Look at the Inspector first. If it does not show a Parameters section with "Smooth window"
and "Threshold", click again on the graph line itself, not the panel, before sending this.

```
Capture 07-knobs-parameterized-virtual-product.png now with capture_window, then close the second panel and give me the report.
```

## Operator, afterwards

- Copy 11, 12, 13 and the reshot 07 into `content/gallery/`.
- Paste the agent's SOURCES.md rows into `content/gallery/SOURCES.md`; drop the 07 caveat,
  it no longer applies.
- Reset the onboarding "completed" flag if you want the tour to auto-offer again.
- Still by hand, with an OS screenshot: the three stale landing-page pictures
  (`sciqlop_command_palette.png` with Ctrl+K, `sciqlop_welcome.png`, `sciqlop_appstore.png`
  from Tools → Plugin Store), `sciqlop_jupyterlab_plot_side_by_side.png`, and the sidebar
  smart search with a typed query. One keypress each; not worth an agent round-trip, and a
  palette left open by a failed toggle would poison every later capture.

---

# Round 3, 2026-09-14 — shot 07 only

Round 2 delivered 11, 12, 13 but not the 07 reshoot. This is a standalone session for
07 alone. Checked against SciQLop `main` (`e2462c619`, after the `bfb6cf6a2` Inspector
fix) on 2026-09-14: `create_virtual_product` accepts `Annotated[..., Knob(...)]`
parameters, a `widget="hline"` knob is drawn on the plot by SciQLop itself
(`knob_inspector/plot_items.py::_MovableHLine`), and `panel.plot()` takes the
`VirtualProduct` object directly, so the agent never needs the tree path of the
virtual product.

## Operator, by hand, before message 1

- SciQLop 0.13.0.dev0, fresh start, no panels open, theme `dark`, window 1600×1000.
- Products dock open on the left. Agents dock open.
- **Float the Agents dock** (drag its title bar out of the main window) before you ask
  for the capture in message 2. `capture_window` grabs the main window only, so a
  floating dock stays out of the picture. The August 07 had no chat dock in it.
- `mkdir -p ~/sciqlop-website-shots`

## Message 1

```
Screenshot job, one shot. Rules first.

Rules
1. Never fake a shot. If it cannot be produced from inside the app, say why and stop.
2. Prefer SciQLop.user_api. Nothing private.
3. Product paths for panel.plot come from sciqlop_products_tree (//-joined). Inside a virtual-product callback, spz.get_data needs the speasy id instead, take it from sciqlop_speasy_inventory. The two forms are not interchangeable.
4. After every plot, sciqlop_wait_for_plot_data on that panel, then check with sciqlop_screenshot_panel. Empty or half-loaded is a failed shot: retry once, then stop and tell me.
5. Leave no trace beyond what I ask for: one virtual product under demo/, one panel.

Staging, in one sciqlop_exec_python cell or a few:

a. Create a virtual product demo/Bmag_smoothed with
     from SciQLop.user_api.virtual_products import create_virtual_product, VirtualProductType
     from SciQLop.user_api.knobs import Knob
     from typing import Annotated
     import numpy as np, speasy as spz
   The callback signature is exactly:
     def bmag_smoothed(start: float, stop: float,
         smooth_window: Annotated[int, Knob(min=1, max=200, step=1, label="Smooth window", unit="samples")] = 16,
         threshold: Annotated[float, Knob(widget="hline", min=0.0, max=80.0, step=1.0, label="Threshold", unit="nT", color="#e74c3c")] = 25.0):
   It fetches MMS1 FGM burst L2 B GSM (mms1_fgm_b_gsm_brst_l2) with spz.get_data, returns None if the fetch is None, takes the magnitude of the first three components, smooths it with a boxcar of smooth_window samples (np.convolve, mode="same", skip when smooth_window == 1), and returns (t, bmag) with t as float seconds. Do not use the threshold in the maths: the hline knob is drawn by SciQLop. Register it with
     vp = create_virtual_product("demo/Bmag_smoothed", bmag_smoothed, VirtualProductType.Scalar, labels=["|B| smoothed"])

b. New panel, time range 2015-10-16 13:05:25 to 13:07:35 UTC (Burch et al. 2016 EDR event). Top plot: FGM burst L2 B GSM from the products tree. Second plot below it: panel.plot(vp). Wait for data on both, check the panel: the bottom plot must show a smooth |B| trace with a red horizontal line at 25 nT.

c. from SciQLop.user_api.gui import show_inspector; show_inspector()

Then stop and tell me it is staged. I will click the smoothed graph so the Inspector shows its Parameters section, and ask you to capture. Do not capture yet.
```

## Operator, between messages

Click the **line** of the smoothed graph (bottom plot), not the empty plot area. The
Inspector should show a Parameters section with "Smooth window" and "Threshold" as
labelled controls. If it still shows bare spinboxes the build is older than `bfb6cf6a2`;
stop and rebuild. Float the Agents dock now if you have not yet.

## Message 2

```
Capture now: from SciQLop.user_api.screenshot import capture_window; capture_window("~/sciqlop-website-shots/07-knobs-parameterized-virtual-product.png") with the path expanded. Then report one SOURCES.md row: file, event/data, interval, products (exact tree paths), feature shown. Add which virtual product and panel you left open.
```

## Operator, afterwards

- Copy the PNG over `content/gallery/07-knobs-parameterized-virtual-product.png`.
- In `content/gallery/SOURCES.md`, replace the 07 row with the agent's, and delete the
  "Shot 07: the Inspector renders knobs as bare, unlabelled spinboxes" caveat.
