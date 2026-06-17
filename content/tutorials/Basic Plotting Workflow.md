---
title: Basic workflow
---
In this tutorial we will learn how to plot data with SciQLOP and the basic GUI interactions that will allow you to explore in situ measurements.
# Plotting data

The easiest way to plot data with SciQLOP is via the graphical interface. A more advanced workflow will enable you to [[plot data from python scripts]] but we are not there yet.

## Start window

The screenshot below shows you an empty SciQLOP interface from which you can plot data. Three items are important here:

- the **Products** tab, where you can find all [[SciQLOP data tree|data accessible to SciQLOP]].
- the **start/stop** fields, which as you can guess will be the time interval for which data will be plotted
- the **add new [[plot panel]]** button, which allows you to add a new plotting area.

![[empty.png]]

## Drag and drop products to plot

You are ready to see data?
- Setup the start and stop dates
- click on **add new plot panel** 
- click on **products**
- explore the [[SciQLOP data tree]] and drag and drop the product you want to see onto the plot panel

![[dragndrop.png]]

SciQLOP will download the data for you and display it on the plot panel. Depending on your connection speed and whether you already have data in [[cache]] or not this may be either instantaneous or take up to several seconds.

![[plot_one.png]]

If all goes well you should see your data in the plot panel. In the above example we have selected the amplitude of the magnetic field measured by the ACE mission during one day.

>[!warning] **You don't see your data, what could have gone wrong?**
>- check your internet connection
>- move the mouse over the data product in the [[SciQLOP data tree|product tree]] and check the start/stop dates you have chosen are in the data range that should appear under the cursor.
>- Is your product part of the [[builtin plottable products]]?
>  
>  
>  It is so easy to get data with SciQLOP that sometimes users are a bit ambitious on the start/stop times, and not seeing the data could be that it's just taking a lot of time to download. Drag and dropping a month of MMS burst FPI data is cannot and will not be fast ;-)
>
>Check the "Network" activity in the status bar, if SciQLOP is downloading you should see it.
  
 
Let's plot another product into the plot panel. We have two options:

- plot **onto the previous plot**: this is typically what you want to do if you have the same units, like plotting burst and non-burst particle density, or perpendicular and parallel temperatures
- plot in the same [[plot panel]] above or bellow another plot

Choosing between the two options simply consists in where you drop the product once selected from the [[SciQLOP data tree]]. In the following, we have chosen to plot the magnetic field vector components in the GSM coordinate system, underneath the magnetic amplitude.

![[plot_2plots.png]]

>[!tip] Hidding curves
>Sometimes it is useful to hide some of the curves displayed on a plot. Let's say here we don't want to see the Bz component. Just **double click on the legend** and it will hide the associated curve on the plot. Double click again, and the curve will reappear.
>![[hide.png]]

## Browse data

The main advantage of SciQLOP is that it allows you to browse data by just interacting with the plot. Let's zoom out to see the context of the current interval. Doing so depends on your keyboard, either **Cmd-wheel** or **Ctrl-wheel**.

### Zooming in and out
The following screenshot shows the result of zooming out. The data previously taking the whole window now only appear in the central zone, surrounded by white empty areas, because data is being downloaded.

![[zoomingout.png]]

>[!tip] Download in progress
>Have you noticed the network activity is showing download is in progress?

Ok data should arrive rapidly since in our example we are plotting low resolution vectors. It should even be almost instantaneous if you have data in [[cache]] Once the download is finished data should appear

We now see we were zoomed in a nice interplanetary coronal mass ejection!

![[zoomedout.png]]

Zooming in is the exact opposite action


### Going forward and backward in time

To see future or past measurements relative to the currently displayed interval, simply press the left mouse button in an empty area of the plot panel and move your mouse in the horizontal direction left/right to move into the future/past respectively.

As for the zoom-out, data in the past and future times may not be in [[cache]] and it can take time to be displayed.


## Plot properties

Sometimes we want to change the way the data is plotted. Open the **properties** tab.

![[properties1.png]]

This will show a hierarchical tree of all SciQLOP objects currently displayed, from plot panels down to curves. Each level in the hierarchy has its own properties. For instance above we have selected the **plot 5** in **panel 2** which is visually represented by a dashed surrounding rectangle on the plot panel. At this level we can:

- change the vertical scale from [[auto scale]] mode to manual.
- hide/show the legend

At the level of the components Bx, By, Bz you will be able to change curve colors and styles.


>[!tip] panel and plot numbering
>you may wonder why in the **properties** the only panel is **panel 2** and the two plots are numbered 4 and 5. This is because panel and plots are numbered with increasing indexes regardless of previous ones possibly deleted. The screenshot above has been made after panel 1 was deleted, and after plots 1, 2, 3 were deleted on panel 2.

>[!ti] deleting a panel / plot
>Deleting a panel or a plot from the currently displayed view is done by pressing `Suppr` key on the selected item.

