#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 14:34:04 2021

@author: Dr. Arndt Rohwedder, University of Huddersfield
"""
import numpy as np
from open3d import geometry
from open3d import utility
import ellipsave

class fitting:
    def __init__(self,big,form,center):
        self.bigcloud1 = big
        self.form1 = form
        self.center1 = center
        
    def fiteli(self):
        bigcloud = self.bigcloud1.uniform_down_sample(4)
        ellipsoid = []
        cloudarray = []
        radius = self.form1
        cloudarray = np.asarray(bigcloud.points)
        cashape = cloudarray.shape
        xsize = cashape[0]

        helper = [self.center1,radius]
        makeeli = ellipsave.ellipsave(helper,xsize,cloudarray)
        ellipsoid = makeeli.ellipsoid_save()
        ellippc1 = geometry.PointCloud()
        ellippc = ellippc1.uniform_down_sample(4)
        ellippc.points = utility.Vector3dVector(ellipsoid)
        unterschied = geometry.PointCloud.compute_point_cloud_distance(bigcloud,ellippc)
        
        radius[0] = radius[0]*0.95
        radius[1] = radius[1]*0.95
        radius[2] = radius[2]

        
        helper = [self.center1,radius]
        makeeli = ellipsave.ellipsave(helper,xsize,cloudarray)
        ellipsoid = makeeli.ellipsoid_save()
        ellippc1 = geometry.PointCloud()
        ellippc = ellippc1.uniform_down_sample(4)
        ellippc.points = utility.Vector3dVector(ellipsoid)

        unterschied1 = geometry.PointCloud.compute_point_cloud_distance(bigcloud,ellippc)
        ellipsoid = []
        print (np.sum(unterschied))
        print (np.sum(unterschied1))
        while ((np.square(np.sum(unterschied1)))<(np.square(np.sum(unterschied)))):            
            radius[0] = radius[0]*0.95
            radius[1] = radius[1]*0.95
            radius[2] = radius[2]
            helper = [self.center1,radius]
            makeeli = ellipsave.ellipsave(helper,xsize,cloudarray)
            ellipsoid = makeeli.ellipsoid_save()
            ellippc1 = geometry.PointCloud()
            ellippc = ellippc1.uniform_down_sample(4)
            ellippc.points = utility.Vector3dVector(ellipsoid)
            unterschied = unterschied1
            unterschied1 = geometry.PointCloud.compute_point_cloud_distance(bigcloud,ellippc)
            ellipsoid = []        

        radius[0] = radius[0]*0.99
        radius[1] = radius[1]
        radius[2] = radius[2]
        helper = [self.center1,radius]
        makeeli = ellipsave.ellipsave(helper,xsize,cloudarray)
        ellipsoid = makeeli.ellipsoid_save()
        ellippc1 = geometry.PointCloud()
        ellippc = ellippc1.uniform_down_sample(4)
        ellippc.points = utility.Vector3dVector(ellipsoid)

        unterschied1 = geometry.PointCloud.compute_point_cloud_distance(bigcloud,ellippc)
        ellipsoid = []
        print (np.sum(unterschied))
        print (np.sum(unterschied1))        
        
        while ((np.square(np.sum(unterschied1)))<(np.square(np.sum(unterschied)))):            
            radius[0] = radius[0]*0.99
            radius[1] = radius[1]
            radius[2] = radius[2]
            helper = [self.center1,radius]
            makeeli = ellipsave.ellipsave(helper,xsize,cloudarray)
            ellipsoid = makeeli.ellipsoid_save()
            ellippc1 = geometry.PointCloud()
            ellippc = ellippc1.uniform_down_sample(4)
            ellippc.points = utility.Vector3dVector(ellipsoid)
            unterschied = unterschied1
            unterschied1 = geometry.PointCloud.compute_point_cloud_distance(bigcloud,ellippc)
            ellipsoid = []

        radius[0] = radius[0]
        radius[1] = radius[1]*0.99
        radius[2] = radius[2]
        helper = [self.center1,radius]
        makeeli = ellipsave.ellipsave(helper,xsize,cloudarray)
        ellipsoid = makeeli.ellipsoid_save()
        ellippc1 = geometry.PointCloud()
        ellippc = ellippc1.uniform_down_sample(4)
        ellippc.points = utility.Vector3dVector(ellipsoid)

        unterschied1 = geometry.PointCloud.compute_point_cloud_distance(bigcloud,ellippc)
        ellipsoid = []

        while ((np.square(np.sum(unterschied1)))<(np.square(np.sum(unterschied)))):            
            radius[0] = radius[0]
            radius[1] = radius[1]*0.99
            radius[2] = radius[2]
            helper = [self.center1,radius]
            makeeli = ellipsave.ellipsave(helper,xsize,cloudarray)
            ellipsoid = makeeli.ellipsoid_save()
            ellippc1 = geometry.PointCloud()
            ellippc = ellippc1.uniform_down_sample(4)
            ellippc.points = utility.Vector3dVector(ellipsoid)
            unterschied = unterschied1
            unterschied1 = geometry.PointCloud.compute_point_cloud_distance(bigcloud,ellippc)
            ellipsoid = []        
            
        return self.center1, radius