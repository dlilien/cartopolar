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

import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from .cartopy_overrides import NPS, CAN
import shapely.geometry as sgeom

AXEL_HEIBERG_EXTENT = (-948000.000, -700000.000, -935000.000, -600000.000)
MUELLER_NPS_EXTENT = (-830000.000, -750000.000, -800000.000, -710000.000)
MUELLER_EXTENT = (500000.0, 560000.0, 8830000.0, 8900000.0)



def heiberg(ax=None, fig_kwargs=None):
    if fig_kwargs is None:
        fig_kwargs = {}
    if ax is None:
        _, ax = plt.subplots(**fig_kwargs, subplot_kw={'projection': NPS()})
    ax.set_extent(AXEL_HEIBERG_EXTENT, ccrs.epsg(3413))
    ax._xlocs = [-75, -60, -45, -30, -15]
    ax._ylocs = [60, 65, 70, 75, 80]
    ax._y_inline = False
    ax._x_inline = False
    return ax


def mueller_nps(ax=None, fig_kwargs=None):
    if fig_kwargs is None:
        fig_kwargs = {}
    if ax is None:
        _, ax = plt.subplots(**fig_kwargs, subplot_kw={'projection': NPS()})
    ax.set_extent(MUELLER_NPS_EXTENT, ccrs.epsg(3413))
    ax._xlocs = np.arange(-180, 180, 1.0)
    ax._ylocs = np.arange(-180, 180, 1.0 / 3.0)
    ax._y_inline = False
    ax._x_inline = False
    return ax


def mueller_map(ax=None, fig_kwargs=None):
    if fig_kwargs is None:
        fig_kwargs = {}
    if ax is None:
        _, ax = plt.subplots(**fig_kwargs, subplot_kw={'projection': CAN()})
    ax.set_extent(MUELLER_EXTENT, CAN())
    ax._xlocs = np.arange(-180, 180, 1.0)
    ax._ylocs = np.arange(-180, 180, 1.0 / 3.0)
    ax._y_inline = False
    ax._x_inline = False
    return ax


def canadian_inset(fig, x0, y0, width=None, height=None, ax_units=None, background=True, grid=True, outline_ax=None, bbox_kwargs={'facecolor': 'none', 'edgecolor': 'blue', 'linewidth': 2}):
    """Make an inset.

    x0: Float
        Lower left x as a fraction of total (fig or ax, depending on ax_units).
    y0: Float
        Lower left y as a fraction of total (fig or ax, depending on ax_units).
    width: float, optional
        The inset width as fraction. If None, height must be specified. If specified, height taken from aspect ratio of inset.
    height: float, optional
        The inset height as fraction. If None, width must be specified. If specified, width taken from aspect ratio of inset.
    ax_units: None or an axis
        If None, x0, y0, and width or height are taken in figure units. Else, they are taken as units of the given axis.
    """
    if not ax_units:
        fig_size = fig.get_size_inches()
        fig_asp = fig_size[0] / fig_size[1]
        if width is None:
            if height is None:
                raise ValueError('Need either a width or a height')
            width = height * GREENLAND_ASP / fig_asp
        elif height is None:
            height = width / GREENLAND_ASP * fig_asp
        else:
            print('Overspecified width and height, use at your own peril')
    else:
        p = ax_units.get_position()
        x0 = p.x0 + x0 * p.width
        y0 = p.y0 + y0 * p.height
        fig_size = fig.get_size_inches()
        fig_asp = p.width * fig_size[0] / (p.height * fig_size[1])
        if width is None:
            if height is None:
                raise ValueError('Need either a width or a height')
            width = height * GREENLAND_ASP / fig_asp * p.width
            height = p.height * height
        elif height is None:
            height = width / GREENLAND_ASP * fig_asp * p.height
            width = p.width * width
        else:
            width = p.width * width
            height = p.height * height
            print('Overspecified width and height, use at your own peril')

    sub_ax = fig.add_axes([x0, y0, width, height], projection=NPS())
    greenland(sub_ax)
    if background:
        sub_ax.show_tif(RADARSAT_FN, cmap='Greys_r', vmin=0, vmax=255)
    if grid:
        sub_ax.gridlines()
    if outline_ax is not None:
        outline_extent = outline_ax.get_extent()
        extent_box = sgeom.box(outline_extent[0], outline_extent[2], outline_extent[1], outline_extent[3])
        sub_ax.add_geometries([extent_box], outline_ax.projection, **bbox_kwargs)

    return sub_ax
