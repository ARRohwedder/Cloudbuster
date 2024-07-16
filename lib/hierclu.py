#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 21:18:40 2021

@author: Dr. Arndt Rohwedder, Johannes Keppler University, Linz
"""


from sklearn.cluster import AgglomerativeClustering
import numpy as np
import pandas as pd

class HierClu:
    def __init__(self,top,pos,neg,names,fold):

        self.toptennames = top
        self.first = pos
        self.second = neg
        self.samplenames = names
        self.basefolder = fold
        
    def hiercalc (self):
        

        count=np.arange(0,self.first.size)
        dend = pd.DataFrame({'index': count,'First': self.first}, columns=['index','First'])

        model = AgglomerativeClustering(distance_threshold=0, n_clusters=None)

        model = model.fit(dend)

        datsize = dend.shape
        clnumb = 10
        if datsize[0] < 10:
            clnumb = datsize[0]
        
        clustering = AgglomerativeClustering(distance_threshold=None, n_clusters=clnumb).fit(dend)
        hierdf = pd.DataFrame(self.samplenames)
        hierdf.insert(1,'CluOrder',model.labels_,True)
        hiername = self.basefolder+"Hier_Clu.csv"
        hierdf.to_csv(hiername)

        return dend
        
        