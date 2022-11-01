#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 21:18:40 2021

@author: Dr. Arndt Rohwedder
"""

#from matplotlib import pyplot as plt
#from scipy.cluster.hierarchy import dendrogram
from sklearn.cluster import AgglomerativeClustering
#import scipy.cluster.hierarchy as sc

class HierClu:
    def __init__(self,firstdata):
        self.firstdat = firstdata
        
    def hiercalc (self):

        model = AgglomerativeClustering(distance_threshold=0, n_clusters=None)
        model = model.fit(self.firstdat)
        datsize = self.firstdat.shape
        clnumb = 10
        if datsize[0] < 10:
            clnumb = datsize[0]
        
        print (self.firstdat.shape)
        #clustering = AgglomerativeClustering(distance_threshold=None, n_clusters=10).fit(self.firstdat)
        clustering = AgglomerativeClustering(distance_threshold=None, n_clusters=clnumb).fit(self.firstdat)

        return model.labels_
        
        