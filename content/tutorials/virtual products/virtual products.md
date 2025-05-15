---
title: Virtual Products
---
>[!info] Info to beginners: 
>This tutorial concerns a more "advanced" usage of SciQLOP. If you are a beginner with SciQLOP, you should probably start looking at the [[Basic Plotting Workflow]] and how to create [[Catalogs]].

In the [[Basic Plotting Workflow]] tutorial, we have plotted data that is accessible from the [[SciQLOP data tree]] and proposed by web services. Although tens of thousands of products are readily available in there, you may quickly feel limited as your research workflow will sooner or later require plotting quantities that are more complex than data proposed by mission servers. 

For instance, you may want to plot, along with "regular" data from servers:

- the result of a mathematical expression such as the local plasma frequency, or the firehose or mirror instability threshold, or the components of the local $\mathbf{E}\times\mathbf{B}$ velocity
- the magnetic field components, transformed into another coordinate system
- a pitch angle spectrogram for a specific energy band from the distribution function
- etc.

In this tutorial we will a great feature of SciQLOP that will allow you *to plot basically anything you want*, provided you can write a little bit of python.

# What is a virtual product?

A virtual product is like a "normal" data product you get from the [[SciQLOP data tree]], but instead *comes from running a user defined python function*. It is very simple to make a virtual product and interact with it:

- define a python function that takes two arguments `start` and `stop`, the time interval for which the product is computed

```python

def mirror_mode_threshold(start, stop)

	 my_prod = ... # compute your product the way you want

	return my_prod

```

- let SciQLOP know about your function by creating a virtual product:

```python
create_virtual_product("/mms_vprods/mms2/mirror",
					    mirror_mode_threshold,
					    VirtualProductType.Scalar,
                        labels=["Mirror mode threshold"])
```

don't worry we will explain this in more details below. Essentially this will add a product in the [[SciQLOP data tree]] at the path `"/mms_vprods/mms2/mirror"`, which you can now drag and drop in a plot panel as any other product. SciQLOP will call your function passing the window's time interval as argument and display the result. It's as simple as that.


# Open a Jupyter notebook

Jupyter notebooks are embedded in SciQLOP to let you interact with the software. Click on "python 3" under "Notebook" to open a new notebook.

![[jupyterlab.png]]

## Mirror mode instability threshold

Let's investigate the mirror mode instability with SciQLOP. The formula is:

$$
C = \beta_\perp\left(\frac{T_\perp}{T_\parallel}-1\right)
$$
with $\beta_\perp = 2\mu_0P_\perp/B^2$

We aim at plotting $C$ as a regular product along with other products.

In our notebook let's first import SciQLOP packages for virtual product definition

```python
from SciQLop.user_api.virtual_products import create_virtual_product, VirtualProductType
```

then import SPEasy to download and manipulate data, as well as SciPY:

```python
from speasy import SpeasyVariable
from speasy.signal.resampling import interpolate
import speasy as spz
import scipy.constants as cst
```


here comes our mirror mode threshold function:

```python
  
def mirror_mode_threshold(start_time: float, stop_time: float) -> SpeasyVariable or None:
    mms1_products = spz.inventories.data_tree.cda.MMS.MMS1
    products = [mms1_products.DIS.MMS1_FPI_FAST_L2_DIS_MOMS.mms1_dis_temppara_fast,
                mms1_products.DIS.MMS1_FPI_FAST_L2_DIS_MOMS.mms1_dis_tempperp_fast,
                mms1_products.FGM.MMS1_FGM_SRVY_L2.mms1_fgm_b_gse_srvy_l2,
                mms1_products.DIS.MMS1_FPI_FAST_L2_DIS_MOMS.mms1_dis_numberdensity_fast]

    tpara, tperp, b, n = spz.get_data(products, start_time, stop_time)

    anisotropy = tperp / tpara
    Pperp = tperp * n * 1e6
    b = interpolate(tperp, b)
    betaperp = Pperp * cst.mu_0 * cst.e * 2 / (b["Bt"] * 1e-9) ** 2
    mirror = betaperp * (anisotropy - 1)
    return mirror
    ```

in this function we simply:
- ask speasy to download all raw products from CDAWeb for the time interval SciQLOP will provide to the function
- compute the mirror mode formula given above. Note this requires interpolating the temperature onto the magnetic field timestamps, which speasy allows you to do easily
- return the `mirror` variable

Then comes our virtual product definition already given above:

```python
  
	mirror_mode_threshold_vp = create_virtual_product("/mms_vprods/mms2/mirror", 
													  mirror_mode_threshold, 
													  VirtualProductType.Scalar,
                                                      labels=["Mirror mode threshold"])
```


From now on, SciQLOP knows about our virtual product. It is registered in the [[SciQLOP data tree]] at the path `/mms/mirror`. The arguments to the `create_virtual_product` are:

- `"/mms_vprods/mms2/mirror"` : the path in the data tree where the virtual product will be accessible
- `mirror_mode_threshold` the name of the python function SciQLOP needs to call to compute this virtual product
- `VirtualProductType.Scalar` : is the type of virtual product, here it is a scalar but you can also compute vectors (`VirtualProductType.Vector`) or spectrograms (`VirtualProductType.Spectrogram`)
- `labels=["Mirror mode threshold"]` will be the legend SciQLOP will show on the plot


The screenshot below shows, on the left in the [[SciQLOP data tree]], the virtual product we have created. It has been drag-and-dropped in the second plot from the top in the current plot panel in the following screenshot.

![[vp_mirror_plot.png]]





