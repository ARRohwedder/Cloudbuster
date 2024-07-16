#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 13:00:37 2021

@author: Dr. Arndt Rohwedder
"""
#from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
#from kneed import KneeLocator
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np

class myKMeans:
    def __init__(self,data,one,two,top,fold,snames,nameparam):
        self.Sphdata = data
        self.first = one
        self.second = two
        self.pca_topten = top
        self.basefolder = fold
        self.samplenames = snames
        self.namparam = nameparam
        
    def KMeanscalc (self):

        kmdf = pd.DataFrame({'First': self.first,'Second': self.second}, columns=['First','Second'])
        kmdfarray = np.asarray(kmdf)
        kmdf_scalar = StandardScaler().fit(kmdfarray)
        kmdf_rescaled = kmdf_scalar.transform(kmdfarray)

        db = DBSCAN(eps=0.5, min_samples=3).fit(kmdf_rescaled)
        labels = db.labels_
        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
        n_noise_ = list(labels).count(-1)
        print("Estimated number of clusters: %d" % n_clusters_)
        print("Estimated number of noise points: %d" % n_noise_)
        
        clucount = n_clusters_

        order = db.labels_
        
        kmdf_complete = pd.DataFrame(kmdf_rescaled,columns=[self.pca_topten[0],self.pca_topten[1]])
        kmdf_complete.insert(2,'clusters',order,True)

        kmoutdf = pd.DataFrame({self.namparam:self.samplenames,'clusters':order})#Experiment, 'File'
        
        kmdf_name = self.basefolder+"DBScan_clu.csv"
        kmoutdf.to_csv(kmdf_name)
        kmdf_name = self.basefolder+"DBScan_raw.csv"
        kmdf_complete.to_csv(kmdf_name)
        
        import matplotlib.pyplot as plt
        unique_labels = set(labels)
        core_samples_mask = np.zeros_like(labels, dtype=bool)
        core_samples_mask[db.core_sample_indices_] = True
        colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
        figclu, axclu = plt.subplots(figsize=(10, 9))
        for k, col in zip(unique_labels, colors):
            if k == -1:
                col = [0, 0, 0, 1]
            class_member_mask = labels == k
            xy = kmdf_rescaled[class_member_mask & core_samples_mask]
            plt.plot(xy[:, 0],xy[:, 1],"o",markerfacecolor=tuple(col),markeredgecolor="k",markersize=14,)
            xy = kmdf_rescaled[class_member_mask & ~core_samples_mask]
            plt.plot(xy[:, 0],xy[:, 1],"o",markerfacecolor=tuple(col),markeredgecolor="k",markersize=6,)
        plt.title(f"Estimated number of clusters: {n_clusters_}")
        DBScanplt = self.basefolder+"DBScan_clustering.svg"
        figclu.savefig(DBScanplt)
        figclu.show()
        
        
        return kmdf_complete,order,clucount


        