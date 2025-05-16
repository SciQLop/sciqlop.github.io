---
title: SciQLOP
---
# [**Download the Latest release**](https://github.com/SciQLop/SciQLop/releases/latest)


# What Is SciQLop?

**SciQLop** (**SCI**entific **Q**t application for **L**earning from **O**bservations of **P**lasmas) is a powerful and
user-friendly tool designed for the visualization and analysis of in-situ space plasma data.

Using SciQLop will let you:

- have a super easy access to tens of thousands of products from the top main data archives in the world,
- explore multivariate time series effortlessly, with lightning-fast and transparent downloads as you scroll, zoom in,
  and zoom out,should
- visualize custom products with simple python code executed on-the-fly,
- easily label time intervals and make or edit catalog of events graphically and rapidely,
- analyze your data in jupyter notebooks,

![[sciqlop_screenshot.png]]

Heliophysicists now benefit from decades of space exploration through many spacecraft missions.
Exploring this massive amount of data to find events of interest, build catalogs, and conduct statistical multi-mission
data analysis
can be a daunting task if not having the right tool.

SciQLop aims at being this tool! A simple lightweight yet powerful graphical interface coupled to the limitless options
brought by the Jupyter Notebook integration,
that focuses on providing users with the easiest possible way to explore, label and analyze huge amounts of data.
SciQLop is also the right tool for teaching space physics and in situ spacecraft data handling to students effortlessly.

# Main Features

## Interactive and responsive 

- SciQLop can handle millions of data points without compromising on interactivity.
- Users can scroll, zoom, move, and export plots with ease.


![[SciQLop_MMS.gif]]

## User Friendly
- Accessing data in SciQLop is as simple as a drag and drop from the tens of thousands of products readily available.
- Custom user products defined in Python behave exactly the same way and bring infinite possibilities.

![[SciQLop_DragAndDrop.gif]]

## Jupyter notebook integration

 SciQLop can be used as a backend for Jupyter notebooks, allowing users to create and manipulate plots from within their notebooks, define new products and much more.

![[sciqlop_jupyterlab_plot_side_by_side.png]]

## Creating and interacting with catalogs

SciQLop provides a catalog system that allows users to easily label events in their data or visualize existing catalogs of events.

![[sciqlop_catalogs.png]]


## Upcoming features

- **community-driven plugins repository**: SciQLop will soon have a plugin system that will allow users to extend the
  software's capabilities by installing community-driven plugins.
- **catalogs coediting**: SciQLop will allow users to coedit catalogs, making it easier to collaborate on event
  labeling and visualization, thereby also improving reproducibility of space physics studies.

# How to install SciQLop

## Mac Users

Since SciQLop 0.7.1 we produce a Mac App Bundle that you can download from
the [latest release](https://github.com/SciQLop/SciQLop/releases/latest) page just pick the
right architecture for your Mac (ARM64 for Apple M1/2/3 chips and x86_64 for intel ones).

## Linux Users

If you are using a Linux distribution, you may not need to install anything, you can just download the AppImage from the
[latest release](https://github.com/SciQLop/SciQLop/releases/latest) and run it (after making it executable).

## From sources

Since SciQLop depends on specific versions of PySide6 you might prefer to use a dedicated virtualenv for SciQLop to
avoid any conflict with any other Python package already installed in your system.

- Using releases from PyPi

```Bash
python -m pip install sciqlop
```

- Using the latest code from GitHub

```Bash
python -m pip install git+https://github.com/SciQLop/SciQLop
```

Once installed the sciqlop launcher should be in your PATH and you should be able to start SciQLop from your terminal.

```Bash
sciqlop
```

or

```Bash
python -m SciQLop.app
```



# How to contribute

Just fork the repository, make your changes and submit a pull request. We will be happy to review and merge your
changes.
Reports of bugs and feature requests are also welcome. Do not forget to star the project if you like it!

# Credits

The development of SciQLop is supported by the [CDPP](http://www.cdpp.eu/).<br />
We acknowledge support from the federation [Plas@Par](https://www.plasapar.sorbonne-universite.fr)

# Thanks

We would like to thank the developers of the following libraries that SciQLop depends on:

- [PySide6](https://doc.qt.io/qtforpython-6/index.html) for the GUI framework and Qt bindings.
- [QCustomPlot](https://www.qcustomplot.com/) for providing the plotting library.
- [DiskCache](https://pypi.org/project/diskcache/) for providing a simple and efficient caching system used
  in [Speasy](https://github.com/SciQLop/speasy).
- [The Jupyter project](https://jupyter.org/) for providing the Jupyter notebook integration.
- [Numpy](https://numpy.org/) for providing fast Python array library.
