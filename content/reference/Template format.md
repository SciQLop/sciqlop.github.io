---
title: Template and share-link format
---

This page describes the files behind [[plot templates]] and the links SciQLop exchanges with the
[Speasy proxy](https://sciqlop.lpp.polytechnique.fr/cache/) web viewer. You need it only to write or
generate templates by hand, or to build a tool around them.

A panel can leave SciQLop in two forms:

1. **A template file**: JSON or YAML, saved with `panel.save_template(...)` or **Panel templates › Export template…**.
2. **A Speasy proxy link**: a `/plot?config=…` URL, opened with **Export › Open in Speasy web viewer**.

The two formats are close, but not the same. SciQLop converts between them through one internal model,
so a panel survives the trip both ways, minus the fields the other side doesn't know.

# Template files

Templates live in `~/.local/share/sciqlop/templates/`, one file per template, named after it. The
extension picks the format: `.json`, `.yaml` or `.yml`. A PNG preview with the same name sits next to the file.

This is what SciQLop saves for a spectrogram above an ion density on a log scale:

```json
{
  "name": "mms_moments_overview",
  "description": "",
  "version": 1,
  "time_range": {
    "start": "2020-12-19T00:00:00+00:00",
    "stop": "2020-12-20T00:00:00+00:00"
  },
  "plots": [
    {
      "products": [
        {
          "path": "speasy//cda//MMS//MMS1//DIS//MMS1_FPI_FAST_L2_DIS_MOMS//mms1_dis_energyspectr_omni_fast",
          "label": "mms1_dis_energyspectr_omni_fast",
          "kind": "speasy",
          "speasy_id": "cda/MMS1_FPI_FAST_L2_DIS-MOMS/mms1_dis_energyspectr_omni_fast",
          "graph_type": "SciQLopColorMapFunction",
          "knobs": {}
        }
      ],
      "y_axis": {"log": false, "range": [0.0, 5.0]},
      "z_axis": {"log": true, "range": [0.001, 61651212.0]}
    },
    {
      "products": [
        {
          "path": "speasy//cda//MMS//MMS1//DIS//MMS1_FPI_FAST_L2_DIS_MOMS//mms1_dis_numberdensity_fast",
          "label": "mms1_dis_numberdensity_fast",
          "kind": "speasy",
          "speasy_id": "cda/MMS1_FPI_FAST_L2_DIS-MOMS/mms1_dis_numberdensity_fast",
          "graph_type": "SciQLopLineGraphFunction",
          "knobs": {}
        }
      ],
      "y_axis": {"log": true, "range": [0.53, 151.5]},
      "z_axis": {"log": false, "range": [0.0, 6.0]}
    }
  ],
  "intervals": [],
  "max_zoom_seconds": 86400.0
}
```

A hand-written template can be much shorter. Only `name`, `plots` and each product's `path` are required:

```yaml
name: mms_density
time_range: {start: '2020-12-19T00:00:00Z', stop: '2020-12-20T00:00:00Z'}
plots:
- products:
  - path: speasy//cda//MMS//MMS1//DIS//MMS1_FPI_FAST_L2_DIS_MOMS//mms1_dis_numberdensity_fast
  y_axis: {log: true}
```

## Panel

| Field | Type | Meaning |
|---|---|---|
| `name` | text, required | The template's name, shown on its welcome-page card. |
| `description` | text | Free text. |
| `version` | integer | Always `1`. SciQLop doesn't check it yet. |
| `time_range` | `{start, stop}` | ISO 8601 times. Without it, the panel keeps its current range. |
| `plots` | list, required | One entry per plot, top to bottom. |
| `max_zoom_seconds` | number | The panel's zoom-out limit. Left out, SciQLop raises its current limit if the time range is wider. |
| `intervals` | list | Reserved: SciQLop neither saves nor restores it yet. |

## Plot

| Field | Type | Meaning |
|---|---|---|
| `products` | list, required | What the plot shows. The first product creates the plot; the others are drawn on top of it. |
| `y_axis` | `{log, range}` | `log`: true for a log scale. `range`: `[min, max]`; left out, the axis fits the data. |
| `z_axis` | `{log, range}` | The same, for a spectrogram's colour scale. Ignored for line plots. |

## Product

| Field | Type | Meaning |
|---|---|---|
| `path` | text, required | The product's path in the product tree, levels separated by `//`: the same path `panel.plot()` takes. Empty for data that can't be re-plotted (arrays, functions); those are skipped on load. |
| `label` | text | The curve name when the template was saved. |
| `kind` | `speasy`, `vp` or empty | Where the product comes from: Speasy, or a virtual product. |
| `speasy_id` | text | The Speasy identifier, `provider/dataset/parameter`, for `kind: speasy`. |
| `graph_type` | text | The kind of graph SciQLop drew. |
| `knobs` | mapping | The product's adjustable inputs: virtual-product knobs, AMDA template arguments, or the `coordinate_system` of a trajectory. |

Loading a template uses only `path` and `knobs`; `label`, `kind`, `speasy_id` and `graph_type` record what
was saved. To get a product's path, drag it from the product tree into a notebook cell.

# Speasy proxy links

A share link is `https://<proxy>/plot?config=<data>`, where `<data>` is the JSON config below encoded as
base64url without `=` padding. SciQLop uses the proxy configured in Speasy.

```json
{
  "version": 1,
  "name": "MMS1 magnetopause crossing",
  "description": "Optional story shown above the plots.",
  "time_range": {"start": "2015-10-16T13:05:25Z", "stop": "2015-10-16T13:07:35Z"},
  "plots": [
    {
      "products": [{"path": "cda/MMS1_FPI_BRST_L2_DIS-MOMS/mms1_dis_energyspectr_omni_brst",
                    "label": "mms1_dis_energyspectr_omni_brst"}],
      "log_z": true,
      "colormap": "jet",
      "z_range": [10000, 10000000]
    },
    {
      "products": [{"path": "ssc/mms1", "coordinate_system": "gse"}],
      "y_axis": {"log": false}
    }
  ],
  "intervals": [{"start": "2015-10-16T13:07:01Z", "stop": "2015-10-16T13:07:03Z",
                 "color": "#f1c40f", "label": "EDR"}]
}
```

| Field | Where | Meaning |
|---|---|---|
| `version` | config | Always `1`. |
| `name`, `description` | config | A story the viewer shows above the plots. Optional. |
| `time_range` | config, required | `{start, stop}`: UTC, ISO 8601, ending in `Z`. |
| `plots` | config, required | One entry per subplot, top to bottom. |
| `intervals` | config | Shaded events: `start`, `stop`, optional `color` and `label`. |
| `products` | subplot, required | Each has a `path`: the **Speasy identifier**, not a tree path. Optional: `label`, `coordinate_system`, and `product_inputs` (AMDA template arguments). |
| `y_axis` | subplot | `{log}`. Left out, the viewer follows the data's own scale hint. |
| `log_z` | subplot | Log colour scale for spectrograms. Left out, the viewer follows the data's hint. |
| `colormap` | subplot | Colour map name; `viridis` when left out. |
| `z_range` | subplot | `[min, max]` of the colour scale; fitted to the data when left out. |

The proxy also serves presets from `GET /get_presets`. A preset is one of these configs as a JSON file, with
its `name` and `description` inside. A proxy reads its presets from the folder named by
`SPEASY_PROXY_PRESETS_PATH`, and highlights the ones in its `featured/` subfolder.

# Between the two

SciQLop turns a panel into a link with **Export › Open in Speasy web viewer**. It turns a link back into a
panel when you paste the link into the search box of an empty panel.

| Template | Proxy link | Notes |
|---|---|---|
| `time_range` | `time_range` | `+00:00` and `Z` are converted. |
| products with `kind: speasy` | `products` | `speasy_id` becomes `path`. On the way back, SciQLop finds the product in its tree from the Speasy identifier. |
| `knobs` | `product_inputs` | Copied as is. |
| `y_axis.log` | `y_axis.log` | |
| `z_axis.log` | `log_z` | Only for plots holding a spectrogram. |

Fields that exist on one side only are lost on the way across:

- **Template → link:** virtual products, data plotted from arrays or functions, axis ranges and the zoom-out
  limit. A plot with no Speasy product left is dropped; with no plot left, SciQLop offers no link.
- **Link → template:** `name`, `description`, `colormap`, `z_range`, `intervals`, and `coordinate_system`.
  Products missing from SciQLop's product tree are skipped, and SciQLop lists them.

# Known problems

These are reported and will be fixed; until then, work around them as below.

- **YAML exports don't load back.** SciQLop writes axis ranges with a Python-only YAML tag
  (`!!python/tuple`), which its own loader refuses. Export templates as JSON.
- **A spectrogram's energy axis isn't saved.** SciQLop draws it on the right-hand axis, but the template
  stores the hidden left one (`"log": false, "range": [0.0, 5.0]` above). The energy axis comes back with
  its default scale, and a share link forces it to linear on the proxy.
- **Coordinate frames don't cross.** SciQLop keeps a trajectory's frame among its knobs, so it travels as
  `product_inputs.coordinate_system`; the proxy reads a separate `coordinate_system` field.
- **Labels must be plain ASCII in links.** The proxy decodes the config as Latin-1: it can't make a link
  when a label holds a character such as `⁻`, and it garbles UTF-8 labels from SciQLop (`cm⁻³` shows
  as `cmâ»Â³`).
