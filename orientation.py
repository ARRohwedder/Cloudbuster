#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 19:30:36 2022

@author: linatix2
"""

# takes a binding box from a pointcloud as a numpy array and returns 2 arrays: 
# 3,1 array with values for rotataion (correction) and 3,1 array for 
# angle values (angles) in x,y,z axes.

import numpy as np

class orient:
    def __init__(self,box):
        self.boxbounds = box
        
    def get_orientation(self):
        
        # sort axis values
        neu = self.boxbounds[self.boxbounds[:, 0].argsort()]
        
        # calculate lengths of katheds
        xxes = np.abs(neu[0,0]-neu[4,0])
        yons = np.abs(neu[0,1]-neu[4,1])
        zets = np.abs(neu[0,2]-neu[4,2])
        
        corrections = []
        angles = []
        
        # calculate values for rotations in x,y,z axes direction
        corrections.append(zets/yons)
        corrections.append(zets/xxes)
        corrections.append(yons/xxes)
        
        # calculate orientaion angles in x,y,z axes of bounding box
        angles.append(np.tan(zets/yons))
        angles.append(np.tan(zets/xxes))
        angles.append(np.tan(yons/xxes))
        
        return corrections,angles
        