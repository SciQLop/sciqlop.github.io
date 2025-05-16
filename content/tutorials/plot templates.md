---
title: Plot templates
---

>[!info] Info to beginners: 
>This tutorial concerns a more "advanced" usage of SciQLOP. If you are a beginner with SciQLOP, you should probably start looking at the [[Basic Plotting Workflow]] and how to create [[Catalogs]].
# What is a plot template

The [[Basic Plotting Workflow]] allows user to easily plot data with SciQLOP by drag-and-dropping products from the [[SciQLOP data tree]] onto a plot panel. Although this is already way simpler than in most existing tools, this way of creating plots will quickly become a limitation to your workflow.

As you do your data exploration or analysis, you will very probably often want to *look at the same data products* , in the same order, with the same styles, colors, etc. Doing all that with your mouse, each time you re-open SciQLOP, is needlessly long.

Plot templates consists in creating your "routine plots" using the python API SciQLOP offers. 


# A simple MMS template

To obtain the following screenshot

![[simple_mms_template.png]]

simply write this in a jupyter notebook embedded in SciQLOP.

First import all plotting routines offered by SciQLOP:

```python
from SciQLop.user_api.plot import *
```

then create a plot panel (this is the python equivalent of the button on the top of the SciQLOP window) and use the returned plot panel handle (`p` ) to make plots by calling the method `plot`:

```python

p=create_plot_panel()
p.plot("speasy//cda//MMS//MMS1//DIS//MMS1_FPI_FAST_L2_DIS_MOMS//mms1_dis_energyspectr_omni_fast")
p.plot("speasy//cda//MMS//MMS1//DIS//MMS1_FPI_FAST_L2_DIS_MOMS//mms1_dis_numberdensity_fast")
p.plot("speasy//cda//MMS//MMS1//DIS//MMS1_FPI_FAST_L2_DIS_MOMS//mms1_dis_bulkv_gse_fast")
p.plot("speasy//cda//MMS//MMS1//FGM//MMS1_FGM_SRVY_L2//mms1_fgm_b_gse_srvy_l2")
p.plot("speasy//cda//MMS//MMS1//DIS//MMS1_FPI_FAST_L2_DIS_MOMS//mms1_dis_tempperp_fast")
```

>![tip] Get the product path easily
> Note the name of each product is a long string that is tedious to write... but you can get it by drag-and-dropping the product from the [[SciQLOP data tree]] to the notebook cell. Easy !


Then grab the last plot (index `4`in the panel plots `p.plots` list) where the perpendicular temperature is represented, and plot the parallel temperature on top.
```python
p.plots[4].plot("speasy//cda//MMS//MMS1//DIS//MMS1_FPI_FAST_L2_DIS_MOMS//mms1_dis_temppara_fast")
```

Finally, set the time range of the plot panel and set plots indexed 1 and 4 (density and temperatures) to have a log Y scale.

```python
p.time_range = TimeRange("2020-12-19", "2020-12-20")
p.plots[1].set_y_scale_type(ScaleType.Logarithmic)
p.plots[4].set_y_scale_type(ScaleType.Logarithmic)

```



