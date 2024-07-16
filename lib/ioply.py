# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 15:38:45 2022

@author: Dr. Arndt Rohwedder, Johannes Keppler University, Linz
"""

from open3d import utility
from open3d import io
from open3d import visualization
from open3d import geometry
import matplotlib.pyplot as plt
import numpy as np


class ioplynow:
    def __init__(self,filename):
        self.fname = filename

    def saveplynow (self,nparray):
        pcd = geometry.PointCloud()
        pcd.points = utility.Vector3dVector(nparray)
        io.write_point_cloud(self.fname, pcd)

    def savefromemptyply (self,pcd,nparray):
        pcd.points = utility.Vector3dVector(nparray)
        io.write_point_cloud(self.fname, pcd)

    def saveply (self,pcd):
        io.write_point_cloud(self.fname, pcd)

    def savecolorply (self,pcd,labels):
        colors = plt.get_cmap("tab20")(labels / (labels.max() if labels.max() > 0 else 1))
        colors[labels < 0] = 0
        pcd.colors = utility.Vector3dVector(colors[:, :3])
        io.write_point_cloud(self.fname, pcd)

    def openplyfile (self):
        cloud = io.read_point_cloud(self.fname)
        return cloud

    def fillpcd (self,pcd,nparray):
        pcd.points = utility.Vector3dVector(nparray)
        return pcd

    def showpcd (self):
        visualization.draw_geometries([self.fname],window_name='Point Cloud',width=750,height=750)
