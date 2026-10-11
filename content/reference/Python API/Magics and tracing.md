---
title: Magics and tracing
---
# Magics

| Magic | Usage | What it does |
|---|---|---|
| `%%vp` | options `--path P`, `--debug`, `--start S --stop S`, `--cachable` | Registers the cell's function as a virtual product. |
| `%%layer` | options `--path P`, `--scope` (`auto`, `panel` or `plot`) | Registers the cell's function as an annotation layer. |
| `%plot` | `%plot <product> [panel]` | Plots a product, fuzzy-matched, in a new or named panel. |
| `%timerange` | `%timerange` / `%timerange <panel>` / `%timerange <start> <stop> <panel>` | Prints or sets panel time ranges. |
| `%install` | `%install astropy "scipy>=1.11"` | Installs packages in the workspace and records them. |
| `%workspace` | `%workspace status\|deps\|install\|plugins\|examples\|add-example\|help` | Inspects and manages the workspace. |
| `%job` | `%job submit [--name N] <command>` / `status <id>` / `list` / `cancel <id>` | Runs shell commands as background jobs. |

Panel names with spaces must be quoted. Panels are named `Panel0`, `Panel1`, …

# Other modules

| Module | Functions |
|---|---|
| `SciQLop.user_api.templates` | `load(name_or_path)`, `list_templates()`, `delete(name)`, `rename(old, new)`. See [[plot templates]]. |
| `SciQLop.user_api.themes` | `apply_theme(name)`, `current_theme()`, `list_themes()`. Names: `light`, `dark`, `neutral`, `space`, `github_light`, `nord_light`, `catppuccin_latte`, `high_contrast_light`. |
| `SciQLop.user_api.screenshot` | `capture_window(path)`, `capture_panel(panel, path)` (experimental). Both create missing folders. |
| `SciQLop.user_api.gui` | `get_main_window()`, `show_product_tree()`, `show_inspector()` (the last two experimental). |
| `SciQLop.user_api.packages` | `install_packages(*specs)`: what `%install` uses. Returns a dict with `ok`, `installed`, `already_present`, `error`. |
| `SciQLop.user_api.jobs` | `submit_job(command, name="")`, `job_status(id)`, `list_jobs()`, `cancel_job(id)`. Jobs survive closing SciQLop. |
| `SciQLop.user_api.diagnostics` | `dump_now(...)`, `hot_threads(pid)` and friends, for a SciQLop that feels stuck. |
| `SciQLop.user_api.tracing` | Performance traces. See below. |

## Tracing

`tracing` records what SciQLop does, with timings, into a file you open in [Perfetto](https://ui.perfetto.dev/).

```python
from SciQLop.user_api import tracing

with tracing.session("/tmp/slow_pan.json"):
    p.time_range = TimeRange("2015-10-16T00:00", "2015-10-17T00:00")
# open /tmp/slow_pan.json in https://ui.perfetto.dev/
```

| Name | What it does |
|---|---|
| `session(path)` | Records for the duration of a `with` block. |
| `enable(path)` / `disable()` / `flush()` / `is_enabled()` | Manual control. |
| `zone(name, cat="", **args)` | Marks a block of your own code in the trace. |
| `traced(name=None, cat="", capture=())` | Decorator: marks every call of a function. `capture=("start", "stop")` records those arguments. |
| `counter(name, value, cat="")` | Records a value over time. |
| `async_begin(name, cat="")` / `async_end(handle)` | Marks work that starts and ends in different places. |
| `set_thread_name(name)` | Names the current thread in the trace. |

Setting `SCIQLOP_TRACE=/tmp/trace.json` before starting SciQLop records from the very start.

```python
@tracing.traced(capture=("start", "stop"))
def b_total(start: float, stop: float):
    ...
```

