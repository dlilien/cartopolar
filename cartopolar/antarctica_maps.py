#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 dlilien <dlilien@hozideh>
#
# Distributed under terms of the MIT license.

"""

"""

import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from .cartopy_overrides import SPS
# import shapely.geometry as sgeom

USP_EXTENT = (31000, 35000, -37750, -33750)
# USP_EXTENT = (-100000, 100000, -100000, 100000)
USP_ASP = (USP_EXTENT[1] - USP_EXTENT[0]) / (USP_EXTENT[3] - USP_EXTENT[2])


def upstream(ax=None, fig_kwargs=None):
    if fig_kwargs is None:
        fig_kwargs = {}
    if ax is None:
        _, ax = plt.subplots(**fig_kwargs, subplot_kw={'projection': SPS()})
    ax.set_extent(USP_EXTENT, ccrs.epsg(3031))
    ax._xlocs = np.arange(0, 180)
    ax._ylocs = np.arange(-90, -80, 0.1)
    ax._y_inline = False
    ax._x_inline = False
    return ax
