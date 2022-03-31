#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 13:00:37 2021

@author: Dr. Arndt Rohwedder
"""
from sklearn.cluster import KMeans
from kneed import KneeLocator

class myKMeans:
    def __init__(self,firsttwo):
        self.firsttwosc = firsttwo
        
    def KMeanscalc (self):
        kmeans_kwargs = {"init": "random","n_init": 10,"max_iter": 300,"random_state": 42,}
        sse = []
        for k in range(1, 11):
            kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
            kmeans.fit(self.firsttwosc)
            sse.append(kmeans.inertia_)
    
        kl = KneeLocator(range(1, 11), sse, curve="convex", direction="decreasing")
        clucount = kl.elbow
        finalkmeans = KMeans(n_clusters=clucount+1, random_state=0).fit(self.firsttwosc)
        order = finalkmeans.labels_
        return order,clucount


        