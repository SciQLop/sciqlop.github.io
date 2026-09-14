---
title: Using catalogs of events
---
In this tutorial we are going to use SciQLop to create a catalog of events and use it to browse data.
# Creating a catalog of events

"Events" are at the center of in situ measurement analysis. Their simplest form represents a couple of times `(begin, end)`. The concept of event in SciQLop, however, is far richer as it can also contain lots of metadata that are very useful. The best definition of a catalog could simply be "a collection of events".

After [[Basic Plotting Workflow|plotting data]], here centered on a nice crossing of the Earth magnetopause by MMS, we start by opening the **catalog view tab** as indicated on the following screenshot. On this image you can also see the icon for the catalog explorer.

![[catalog_noview_with_data.png]]

## The catalog tab

Once you click on the Catalogs tab, you should see a view listing your catalogs. If this is the first time you do that, it will be empty. Here we already have lots of them.

![[catalog_view_with_data.png]]

The list shows from left to right:

- a checkbox, that "activates" the associated catalog
- the name of the catalog
- a button **Add event**
- and, from v0.13, a colour swatch (v0.12 assigns each catalog a colour automatically)

As we build our catalog, we will review all buttons above that list. Let's begin by creating our first catalog. Click on the "+" button and a new catalog called "New Catalog" will appear in the list. We will see how to rename it later. For the moment, activate it by clicking on the checkbox on the left of its name. A panel should appear in the panel below the catalog list with several columns:

- Start
- Stop
- Author
- Tags
- Products
- Rating
- Attributes

As you have probably guessed by now, this panel represents the list of the events catalog you have activated, and the columns are the metadata for each event. Let's create one event that represent the crossing of the magnetopause.

>[!tip] Listing multiple catalogs
>The event list will actually display the union of the events that belong to **all** active catalogs


![[catalog_view_config.png]]

In above screenshot, you see : 

- the "New Catalogue" is selected and activated
- `Panel 2` is selected, meaning that events will be created/displayed on the plot panel 2 where data is currently displayed.
- `interaction mode` is set to `edit`. This will allow to create events and modify their start/stop dates graphically.

## Creating an event

Now clicking on `Add Event` will create a colored zone spanning all plots on `Panel 2`  and located at the center of the window.

![[one_event.png]]

We want the event to define the first boundary layer encounter from the magnetosphere. To do that, click on the left (resp. right) border of the event, the light blue line should turn into a darker blue, indicating the border is now selected. Just select it and slide it to the right (resp. left). Notice the `start` and `stop` times in the event list view dynamically change as you slide the borders.

You can also press the left mouse button in the colored zone representing the event and slide the whole zone left/right to adjust the location of the event.

One great advantage of SciQLop is that zooming in and out is super efficient therefore precisely defining the start and stop times of the events is super easy. Here is the event selected precisely on a zoom around it.

![[one_event_zoomed.png]]


>[!warning] Do not forget to SAVE your modifications
>Any modification to a catalog, whether it is creating, deleting, adjusting the borders of an event etc. will **not be automatically saved**, you **have to hit the save button** on the top of the catalog panel for your modifications to persist.

Let's continue to add more events, the following screenshot shows two additional ones:

![[three_events.png]]

## Reviewing events

Now we have multiple events in our new catalog. Say we want to review them one by one, that is, inspecting some data for the time intervals of each of the events. In the case of the above dummy catalog, all three events are close to each other so what you would probably do is scrolling in time and zooming around each of them.

However, most of the times, your events will be far in time from one another, possibly months or even years apart. Scrolling in time would not be a smart option as it would trigger lots of useless downloads.

SciQLop allows users to "jump" from one event to another. To do that, change the `interaction mode` to `Jump`. In this new mode, you will not be authorized to edit the event position and boundaries as we did above. However, selecting an event from the event list will automatically set the time of the selected panel (here Panel 2) around the selected event.

>[!tip] Zoom factor
>The zoom factor indicates how much of the total window time interval the event will occupy. The default value of `0.60` means the event you jump onto will take 60% of the total window.

![[jump_one_event.png]]

In above screenshot, we selected the first event on the list with a zoom factor `0.3`.

Now, selecting events one after the other, either by clicking on it, or with the arrow keys of your keyboard, will jump from one event to the next, letting you review tons of events in no time.

## Catalog explorer

Let us now rename our catalog, and also set some metadata. The catalog tab only offers a limited view of the catalogs and events. To get a more exhaustive view, open the catalog explorer. This opens the following window.

![[catalog_explorer.png]]

This is the catalog explorer, which basically lists all catalogs on the left panel and all events of a selected catalog, on the right panel. Here our new catalog is selected, and the right panel shows:

- on the top, the list of the three events we created above
- on the bottom panel, the metadata of the selected catalog

You can here rename the catalog by editing the field "Name". See the page describing the catalog explorer to get a more detailed description of all other fields.

If you now select one event on the right panel, the bottom right panel will display the event's metadata, as in the example below.

![[catalog_explorer_event_selected.png]]

# Catalog overlays: several catalogs on one panel

So far we have worked with a single catalog, but nothing stops you from activating several at once. Check two or three catalogs in the catalog tab, with `Panel 2` still selected, and all of them get drawn on that panel: the events of each catalog appear as coloured zones in that catalog's own colour, so a magnetosheath interval from one catalog and a magnetopause crossing from another are told apart at a glance. The zones span all the plots of the panel, exactly like the event we created above, and the event list shows the union of all active catalogs.

SciQLop picks each catalog's colour from a fixed palette of twelve, so two catalogs can occasionally end up with the same one. What you can change is how the events *within* a catalog are coloured: right-click the catalog in the list and open **Color by...**. `Uniform` is the default, one colour for the whole catalog. Choosing a metadata column instead colours each event by its value: one colour per distinct label for text columns, a colormap for numeric ones (**Configure colormap...** lets you pick the colormap and its min/max). You can also toggle catalogs without leaving the plot: right-click on the panel, the **Catalogs** submenu lists every catalog with a checkbox.

## Building a catalog from data

Catalogs do not have to be drawn by hand. The `SciQLop.user_api.catalogs` module creates them from Python, for instance from a notebook opened in SciQLop. Let's build one from the MMS1 ion density: intervals where the density exceeds 10 cm⁻³ are a crude but effective magnetosheath detector.

```python
import numpy as np
import speasy as spz
from datetime import datetime
from SciQLop.user_api import TimeRange
from SciQLop.user_api.plot import create_plot_panel
from SciQLop.user_api.catalogs import catalogs

start, stop = datetime(2015, 10, 16, 10), datetime(2015, 10, 16, 16)
panel = create_plot_panel()
panel.time_range = TimeRange(start, stop)
panel.plot("speasy//cda//MMS//MMS1//DIS//MMS1_FPI_FAST_L2_DIS_MOMS//mms1_dis_numberdensity_fast")

n = spz.get_data("cda/MMS/MMS1/DIS/MMS1_FPI_FAST_L2_DIS_MOMS/mms1_dis_numberdensity_fast", start, stop)
inside = n.values[:, 0] > 10
edges = np.diff(inside.astype(np.int8), prepend=0, append=0)
starts, stops = np.flatnonzero(edges == 1), np.flatnonzero(edges == -1) - 1
events = [(n.time[a], n.time[b], {"region": "magnetosheath"}) for a, b in zip(starts, stops)]

catalogs.save("My Catalogs//magnetosheath", events)
print(catalogs.list("My Catalogs"))
```

Catalog paths are `//`-separated like product paths, and the first segment is the provider: `My Catalogs` is the local one you have been using in the catalog tab. Each event is a `(start, stop)` or `(start, stop, metadata)` tuple, and any datetime-like value works for the bounds (here `numpy.datetime64` straight from speasy). `catalogs.save` creates the catalog if needed and replaces its events otherwise, so you can rerun the cell after tweaking the threshold; `catalogs.create` refuses to overwrite an existing catalog, `catalogs.add_events` appends to one, and `catalogs.get` returns it as a `speasy.Catalog`.

The new catalog shows up in the catalog tab immediately: activate it there to see its zones on the panel. And as with events drawn by hand, hit the **Save** button to write it to disk.

> [!info] Coming in v0.13
> The next release lets the notebook attach the overlay itself, with `PlotPanel.add_catalog_overlay`:
> ```python
> overlay = panel.add_catalog_overlay("My Catalogs//magnetosheath", override_color="#50FF8800")
> overlay.remove()  # or panel.remove_catalog_overlay(overlay)
> ```
> `override_color` takes a Qt colour string. A colour name or `#RRGGBB` is opaque and the zones hide the data underneath, so give it an alpha with Qt's `#AARRGGBB` form; `#50` (80/255) is the palette's default transparency. The same release adds a colour swatch next to each catalog in the list, to pick a catalog's colour by hand.
