---
title: Basic workflow
---
In this tutorial we will learn how to plot data with SciQLOP and the basic GUI interactions that will allow you to explore in situ measurements.
# Plotting data

The easiest way to plot data with SciQLOP is via the graphical interface. A more [[advanced workflow]] will enable you to [[plot data from python scripts]] but we are not there yet.

## Start window

The screenshot below shows you an empty SciQLOP interface from which you can plot data. Three items are important here:

- the **Products** tab, where you can find all [[SciQLOP data tree|data accessible to SciQLOP]].
- the **start/stop** fields, which as you can guess will be the time interval for which data will be plotted
- the **add new plot panel** button, which allows you to add a new plotting area.

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
  
 





