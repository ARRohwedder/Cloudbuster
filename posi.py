#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 21:39:07 2020

@author: Dr. Arndt Rohwedder, University of Huddersfield
"""
import numpy as np
from skimage import feature

class identpos:
    
    def __init__(self,im):
        self.image = im

        
    def makepos (self):
        edges = []
        result = []
        positions = []
        poscollect = []
        zwert = 0        
        for zwert in list(range(self.image.shape[0])):
            edges = feature.canny(self.image[zwert])
            result = np.where(edges == True)
            positions = np.asarray(list(zip(result[0], result[1])))
            poscollect.append(positions)
        return poscollect
        