#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 dlilien <dlilien@hozideh>
#
# Distributed under terms of the MIT license.

"""
Setup plots as desired for Greenland.
"""
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from .cartopy_overrides import NPS
import numpy as np


def greenland(ax=None, fig_kwargs={}):
    extent = (-660050.000, 859950.000, -3380050.000, -630050.000)
    if ax is None:
        _, ax = plt.subplots(**fig_kwargs, subplot_kw={'projection': NPS()})
    ax.set_extent(extent, ccrs.epsg(3413))
    ax._xlocs = [-75, -60, -45, -30, -15]
    ax._ylocs = [60, 65, 70, 75, 80]
    ax._y_inline = False
    ax._x_inline = False
    return ax


def core_onset(ax=None, fig_kwargs={}):
    extent = (70000, 325000, -1900000, -1500000)
    if ax is None:
        _, ax = plt.subplots(**fig_kwargs, subplot_kw={'projection': NPS()})
    ax.set_extent(extent, ccrs.epsg(3413))
    ax._xlocs = [-45, -40, -35, -30]
    ax._ylocs = np.arange(70, 81)
    ax._y_inline = False
    ax._x_inline = False
    return ax
