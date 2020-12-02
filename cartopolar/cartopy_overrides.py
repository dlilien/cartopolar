#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 dlilien <dlilien@hozideh>
#
# Distributed under terms of the MIT license.

"""

"""

import cartopy.crs as ccrs
from cartopy.mpl.geoaxes import GeoAxes
import rasterio
from rasterio.plot import show
import matplotlib
import geopandas as gp


class DeluxGeoAxes(GeoAxes):

    # We want to be able to set up to override default gridlines on custom maps
    _xlocs = None
    _ylocs = None
    _x_inline = None
    _y_inline = None

    def plot_pt_shpfile(self, fn, *args, **kwargs):
        data = gp.read_file(fn)
        data.plot(ax=self, *args, **kwargs)

    def show_tif(self, tif_fn, *args, **kwargs):
        tif = rasterio.open(tif_fn)
        show(tif, ax=self, *args, **kwargs)

    def gridlines(self, crs=None, draw_labels=False,
                  xlocs=None, ylocs=None, dms=False,
                  x_inline=None, y_inline=None, auto_inline=True,
                  xformatter=None, yformatter=None, xlim=None, ylim=None,
                  **kwargs):
        if xlocs is None:
            xlocs = self._xlocs
        if ylocs is None:
            ylocs = self._ylocs

        if x_inline is None:
            x_inline = self._x_inline
        if y_inline is None:
            y_inline = self._y_inline

        return super().gridlines(crs=crs, draw_labels=draw_labels,
                                 xlocs=xlocs, ylocs=ylocs,
                                 x_inline=x_inline, y_inline=y_inline, auto_inline=auto_inline,
                                 dms=dms, xformatter=xformatter, yformatter=yformatter,
                                 xlim=xlim, ylim=ylim,
                                 **kwargs)


DeluxGeoAxesSubplot = matplotlib.axes.subplot_class_factory(DeluxGeoAxes)
DeluxGeoAxesSubplot.__module__ = DeluxGeoAxes.__module__


class NPS(ccrs.Stereographic):

    def __init__(self):
        super().__init__(central_latitude=90.0, central_longitude=-45.0,
                         true_scale_latitude=70)

    def _as_mpl_axes(self):
        return DeluxGeoAxes, {'map_projection': self}


class SPS(ccrs.Stereographic):

    def __int__(self):
        super().__init__(central_latitude=-90.0, central_longitude=0.0,
                         true_scale_latitude=-71)

    def _as_mpl_axes(self):
        return DeluxGeoAxes, {'map_projection': self}
