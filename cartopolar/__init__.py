#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 dlilien <dlilien@hozideh>
#
# Distributed under terms of the MIT license.

"""
"""

from .cartopy_overrides import NPS, SPS
nps = NPS()
sps = SPS()
from ._scale_bar import scale_bar

from .colormaps import GMT_globe
