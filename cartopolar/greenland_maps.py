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
from .cartopy_overrides import NPS
import shapely.geometry as sgeom

GREENLAND_EXTENT = (-660050.000, 859950.000, -3380050.000, -630050.000)
GREENLAND_ASP = (GREENLAND_EXTENT[1] - GREENLAND_EXTENT[0]) / (GREENLAND_EXTENT[3] - GREENLAND_EXTENT[2])
CORE_ONSET_EXTENT = (70000, 325000, -1900000, -1480000)
CORE_ONSET_ASP = (CORE_ONSET_EXTENT[1] - CORE_ONSET_EXTENT[0]) / (CORE_ONSET_EXTENT[3] - CORE_ONSET_EXTENT[2])
UPSTREAM_EXTENT = (0, 450000, -1900000, -1300000)
UPSTREAM_ASP = (UPSTREAM_EXTENT[1] - UPSTREAM_EXTENT[0]) / (UPSTREAM_EXTENT[3] - UPSTREAM_EXTENT[2])

HT_EXTENT = (62000, 128000, -840000, -755000)
HT_ASP = (HT_EXTENT[1] - HT_EXTENT[0]) / (HT_EXTENT[3] - HT_EXTENT[2])

HT_SMALL_EXTENT = (90000, 128000, -800000, -755000)
HT_SMALL_ASP = (HT_SMALL_EXTENT[1] - HT_SMALL_EXTENT[0]) / (HT_SMALL_EXTENT[3] - HT_SMALL_EXTENT[2])

RADARSAT_FN = '/home/dlilien/sw/cartopolar/cartopolar/data/1000mCbandmultiyear.tif'


def greenland(ax=None, fig_kwargs=None):
    if fig_kwargs is None:
        fig_kwargs = {}
    if ax is None:
        _, ax = plt.subplots(**fig_kwargs, subplot_kw={'projection': NPS()})
    ax.set_extent(GREENLAND_EXTENT, NPS())
    ax._xlocs = [-75, -60, -45, -30, -15]
    ax._ylocs = [60, 65, 70, 75, 80]
    ax._y_inline = False
    ax._x_inline = False
    return ax


def core_onset(ax=None, fig_kwargs=None):
    if fig_kwargs is None:
        fig_kwargs = {}
    if ax is None:
        _, ax = plt.subplots(**fig_kwargs, subplot_kw={'projection': NPS()})
    ax.set_extent(CORE_ONSET_EXTENT, ccrs.epsg(3413))
    ax._xlocs = [-45, -40, -35, -30]
    ax._ylocs = np.arange(70, 81)
    ax._y_inline = False
    ax._x_inline = False
    return ax


def upstream(ax=None, fig_kwargs=None):
    if fig_kwargs is None:
        fig_kwargs = {}
    if ax is None:
        _, ax = plt.subplots(**fig_kwargs, subplot_kw={'projection': NPS()})
    ax.set_extent(UPSTREAM_EXTENT, ccrs.epsg(3413))
    ax._xlocs = [-60, -55, -50, -45, -40, -35, -30]
    ax._ylocs = np.arange(65, 85)
    ax._y_inline = False
    ax._x_inline = False
    return ax


def hans_tausen(ax=None, fig_kwargs=None):
    if fig_kwargs is None:
        fig_kwargs = {}
    if ax is None:
        _, ax = plt.subplots(**fig_kwargs, subplot_kw={'projection': NPS()})
    ax.set_extent(HT_EXTENT, ccrs.epsg(3413))
    ax._xlocs = np.arange(-180, 180)
    ax._ylocs = np.arange(65, 85, 0.5)
    ax._y_inline = False
    ax._x_inline = False
    return ax


def hans_tausen_small(ax=None, fig_kwargs=None):
    if fig_kwargs is None:
        fig_kwargs = {}
    if ax is None:
        _, ax = plt.subplots(**fig_kwargs, subplot_kw={'projection': NPS()})
    ax.set_extent(HT_SMALL_EXTENT, ccrs.epsg(3413))
    ax._xlocs = np.arange(-180, 180)
    ax._ylocs = np.arange(65, 85, 0.5)
    ax._y_inline = False
    ax._x_inline = False
    return ax


def greenland_inset(fig, x0, y0, width=None, height=None, ax_units=None, background=True, grid=True, outline_ax=None, bbox_kwargs={'facecolor': 'none', 'edgecolor': 'blue', 'linewidth': 2}):
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
