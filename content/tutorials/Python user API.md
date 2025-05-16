---
title: Python user API
---
# Python user API Examples:

SciQLop has a public API that allows users to create custom products and plots. Here are some examples:

- Creating plot panels:

```python
from SciQLop.user_api import TimeRange
from SciQLop.user_api.plot import create_plot_panel
from datetime import datetime

# all plots are stacked
p = create_plot_panel()
p.time_range = TimeRange(datetime(2015, 10, 22, 6, 4, 30), datetime(2015, 10, 22, 6, 6, 0))
p.plot("speasy/cda/MMS/MMS1/FGM/MMS1_FGM_BRST_L2/mms1_fgm_b_gsm_brst_l2")
p.plot("speasy/cda/MMS/MMS1/DIS/MMS1_FPI_BRST_L2_DIS_MOMS/mms1_dis_bulkv_gse_brst")
p.plot("speasy/cda/MMS/MMS1/DIS/MMS1_FPI_BRST_L2_DIS_MOMS/mms1_dis_energyspectr_omni_brst")

# tha_peif_sc_pot and tha_peif_en_eflux will share the same plot 
p2 = create_plot_panel()
p2.plot("speasy/cda/THEMIS/THA/L2/THA_L2_ESA/tha_peif_en_eflux")
p2.plots[0].plot("speasy/cda/THEMIS/THA/L2/THA_L2_ESA/tha_peif_sc_pot")
p2.plot("speasy/cda/THEMIS/THA/L2/THA_L2_ESA/tha_peif_velocity_dsl")
```

> **_NOTE:_**  An easy way to get product paths, is to drag a product from Products Tree to any text zone or even your
> Python terminal.

- Custom products AKA virtual products:

```python

import numpy as np
from SciQLop.user_api.virtual_products import create_virtual_product, VirtualProductType
from SciQLop.user_api.plot import create_plot_panel
import speasy as spz


# define a custom product that calculates the magnitude of the magnetic field measured by ACE

def ace_b_magnitude(start: float, stop: float) -> spz.SpeasyVariable:
  b_gse = spz.get_data(spz.inventories.tree.amda.Parameters.ACE.MFI.ace_imf_all.imf, start, stop)
  return np.sqrt(b_gse["bx"] ** 2 + b_gse["by"] ** 2 + b_gse["bz"] ** 2)


ace_b_magnitude_virtual_prod = create_virtual_product(path='my_virtual_products/ace_b_magnitude',
                                                      product_type=VirtualProductType.Scalar, callback=ace_b_magnitude,
                                                      labels=["|b|"])

# plot the virtual product
p = create_plot_panel()
p.plot(ace_b_magnitude_virtual_prod)
```

More examples can be found in the [examples](SciQLop/examples) folder, they are also available from the welcome screen.