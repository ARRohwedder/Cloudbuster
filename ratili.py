#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 23:24:46 2020

@author: linatix2
"""
import numpy as np

class ratios:
    def __init__(self,im,x,y,z):
        self.dimx = float(x)
        self.dimy = float(y)
        self.dimz = float(z)
        self.image = im

    def imratio (self):

        largest = 0
        ratio = 0
        zxratio = 0
        dimensions = []
        largest = np.max(self.image.shape)
        ratio = 750/largest
        zxratio = self.dimz/self.dimx
        dimensions.append(zxratio*ratio)
        dimensions.append(ratio)
        dimensions.append(ratio)
        return dimensions