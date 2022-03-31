#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 00:00:28 2020

@author: Dr. Arndt Rohwedder, University of Huddersfield
"""
from skimage import transform
from skimage.draw import rectangle_perimeter
import numpy as np

class scale:
    def __init__(self,im,x,y,z,hinter):
        self.image = im
        self.xdim = x
        self.ydim = y
        self.zdim = z
        self.backg = hinter

    def sortscale (self):

        imscale = []
        bild = []
        bild2 = []
        bild2 = transform.rescale(self.image, (self.zdim,self.ydim,self.xdim),mode="edge",preserve_range=False)
        start = (1, 1)

        for slide in range(bild2.shape[0]-1):
            einzelbild = bild2[slide]
            endx = (einzelbild.shape[0])-2
            endy = (einzelbild.shape[1])-2
            end = (endx, endy)
            rr, cc = rectangle_perimeter(start, end, shape=einzelbild.shape)
            einzelbild[rr, cc] = self.backg
            bild2[slide] = einzelbild
        bild = np.full((1,bild2.shape[1], bild2.shape[2]), self.backg)
        imscale = np.concatenate([bild,bild2,bild])
        return imscale

        