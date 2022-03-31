#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 21:23:19 2021

@author: Dr. Arndt Rohwedder, University of Huddersfield
"""
#import open3d as o3d
from open3d import geometry
from open3d import utility
from open3d import io


class saveply:
    
    def __init__(self,filename,numparray):
        self.cloud = numparray
        self.ofilename = filename
        
    def saveplynow (self):
        pcd = geometry.PointCloud()
        pcd.points = utility.Vector3dVector(self.cloud)
        io.write_point_cloud(self.ofilename, pcd)