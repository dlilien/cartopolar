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
from rasterio.plot import show, plotting_extent
import matplotlib
import geopandas as gp
import numpy as np
from ._scale_bar import scale_bar

from rasterio.warp import calculate_default_transform, reproject, Resampling


def reproject_mem(ds, dst_crs='EPSG:3348', ndv=-9999.0, src_crs=None, tr=None):
    if src_crs is None:
        src_crs = ds.crs
    transform, width, height = calculate_default_transform(
        src_crs, dst_crs, ds.width, ds.height, *ds.bounds, tr=tr)
    destination = np.zeros((width, height))
    reproject(
        ds.read(1, masked=True),
        destination,
        src_transform=ds.transform,
        src_crs=src_crs,
        dst_transform=transform,
        dst_crs=dst_crs,
        resampling=Resampling.nearest)
    if ndv is not None:
        destination[destination == ndv] = np.nan
    extent = plotting_extent(destination, transform)
    return destination, extent


class DeluxGeoAxes(GeoAxes):

    # We want to be able to set up to override default gridlines on custom maps
    _xlocs = None
    _ylocs = None
    _x_inline = None
    _y_inline = None

    def plot_pt_shpfile(self, fn, cax_bounds=None, *args, **kwargs):
        if ('legend' in kwargs) and (kwargs['legend']) and (cax_bounds is not None):
            kwargs['cax'] = self.get_figure().add_axes(cax_bounds)
        data = gp.read_file(fn)
        data.plot(ax=self, *args, **kwargs)

    def show_tif(self, tif_fn, *args, **kwargs):
        images = self.get_images()
        tif = rasterio.open(tif_fn)
        show(tif, ax=self, *args, **kwargs)
        imagesn = self.get_images()
        if len(images) == len(imagesn):
            return None
        else:
            for img in imagesn:
                if img not in images:
                    return img

    def imshow_tif(self, fn, ndv=None, src_crs=None, *args, **kwargs):
        ds = rasterio.open(fn)
        if src_crs is None:
            src_crs = ds.crs
        if src_crs == self.projection.crs:
            return self.imshow(ds.read(1, masked=True), extent=plotting_extent(ds), *args, **kwargs)
        else:
            arr, extent = reproject_mem(ds, dst_crs=self.projection.crs, ndv=ndv, src_crs=src_crs)
            ds.close()
            return self.imshow(arr, extent=extent, *args, **kwargs)

    def contour_tif(self, tif_fn, ndv=None, src_crs=None, tr=None, *args, **kwargs):
        ds = rasterio.open(tif_fn)
        arr, extent = reproject_mem(ds, dst_crs=self.projection.crs, ndv=ndv, src_crs=src_crs, tr=tr)
        ds.close()
        return self.contour(np.flipud(arr), extent=extent, *args, **kwargs)

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

    def scale_bar(self, *args, **kwargs):
        return scale_bar(self, *args, **kwargs)


DeluxGeoAxesSubplot = matplotlib.axes.subplot_class_factory(DeluxGeoAxes)
DeluxGeoAxesSubplot.__module__ = DeluxGeoAxes.__module__


class NPS(ccrs.Stereographic):
    crs = 'EPSG:3413'

    def __init__(self):
        super().__init__(central_latitude=90.0, central_longitude=-45.0,
                         true_scale_latitude=70)

    def _as_mpl_axes(self):
        return DeluxGeoAxes, {'map_projection': self}


class CANART(ccrs.UTM):
    crs = 'EPSG:32617'

    def __init__(self):
        super().__init__(zone='17N', southern_hemisphere=False)

    def _as_mpl_axes(self):
        return DeluxGeoAxes, {'map_projection': self}


class CAN(ccrs.LambertConformal):
    crs = 'EPSG:3348'

    def __init__(self):
        super().__init__(central_longitude=-91.86666666666, central_latitude=63.390675, false_easting=6200000, false_northing=3000000, standard_parallels=[49, 77])

    def _as_mpl_axes(self):
        return DeluxGeoAxes, {'map_projection': self}


class SPS(ccrs.SouthPolarStereo):
    crs = 'EPSG:3031'

    def __int__(self):
        super().__init__(true_scale_latitude=-71)

    def _as_mpl_axes(self):
        return DeluxGeoAxes, {'map_projection': self}
