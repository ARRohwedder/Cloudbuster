#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 11:52:17 2022

@author: Arndt Rohwedder
"""
#import open3d as o3d

from open3d import geometry

class surfandvol:
    def __init__(self,pcl, res):
        self.cloud = pcl
        self.resolution = res

    def surfvolcalc (self):
        covex, _ = self.cloud.compute_convex_hull()
        surface = covex.get_surface_area()
        surface = surface*(self.resolution*self.resolution)
        volume = covex.get_volume()
        volume = volume*(self.resolution*self.resolution*self.resolution)
        return surface, volume

