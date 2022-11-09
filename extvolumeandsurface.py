#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 11:52:17 2022

@author: Arndt Rohwedder
"""
import open3d as o3d
import numpy as np
#from open3d import geometry

class surfandvol:
    def __init__(self,pcl, res):
        self.cloud = pcl
        self.resolution = res

    def surfvolcalc (self):

        #self.cloud.compute_convex_hull()
        try:
            self.cloud.estimate_normals()
            form = self.cloud.get_max_bound()
            sizeform = int(np.max(form))
            self.cloud.orient_normals_consistent_tangent_plane(2*sizeform)
        
            distances = self.cloud.compute_nearest_neighbor_distance()
            avg_dist = np.mean(distances)
            radii = [0.1*avg_dist,5*avg_dist,1*avg_dist, 2*avg_dist]
            rec_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(self.cloud, o3d.utility.DoubleVector(radii))
            rec_mesh.compute_vertex_normals()
            rec_mesh.remove_degenerate_triangles()
            surface = rec_mesh.get_surface_area()
            print ("surface: ", surface)
            surface = surface*(self.resolution*self.resolution)
        #volume = rec_mesh.get_volume()

        except:
            surface = 0
        #volume = volume*(self.resolution*self.resolution*self.resolution)
        return surface

