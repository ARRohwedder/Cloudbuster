#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 12:37:43 2021

@author: linatix2
"""
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sc
import numpy as np

class figplot:
    def __init__(self,figone,corrtrans,cornames,samcorr,samname,dendr,km,folder,count):
        self.pcaplot = figone
        self.correl = corrtrans
        self.topnames = cornames
        self.firstdat = dendr
        self.kmdf = km
        self.basefolder = folder
        self.pcacount = count
        self.samplecorr = samcorr
        self.samplename = samname
        
    def FigPlot (self):
        
        # PCA
        figa, axa = self.pcaplot.biplot3d(n_feat=10,SPE=True,hotellingt2=True,figsize=(10, 9))
        PCAfig = self.basefolder+"PCA.svg"
        plt.savefig(PCAfig)
        
        # Correlation
        figb, axb = plt.subplots(figsize=(10, 9))
        plt.title('Correlation of top rated Parameters', fontsize=12);
        cax = axb.matshow(self.correl, vmin=-1, vmax=1,cmap=plt.cm.RdYlGn)
        figb.colorbar(cax)
        ticks = np.arange(0,self.pcacount,1)
        axb.set_xticks(ticks)
        axb.set_yticks(ticks)
        axb.xaxis.set_ticks_position("bottom")
        axb.set_xticklabels(self.topnames,rotation=45, ha = "right", rotation_mode="anchor")
        axb.set_yticklabels(self.topnames)
        corfig = self.basefolder+"Correlation.svg"
        plt.savefig(corfig)
        
        figs, axs = plt.subplots(figsize=(14, 13))
        plt.title('Correlation of Samples', fontsize=12);
        cax = axs.matshow(self.samplecorr, vmin=-1, vmax=1,cmap=plt.cm.RdYlGn)
        figs.colorbar(cax)
        ticks = np.arange(0,len(self.samplename),1)
        axs.set_xticks(ticks)
        axs.set_yticks(ticks)
        axs.xaxis.set_ticks_position("bottom")
        axs.set_xticklabels(self.samplename,rotation=90, ha = "right", rotation_mode="anchor")
        axs.set_yticklabels(self.samplename)
        corfigsam = self.basefolder+"Sample_Correlation.svg"
        plt.savefig(corfigsam)
        
        
        # Hierarchical Clustering
        figc, axc = plt.subplots(figsize=(8, 10))
        
        plt.title('Hierarchical Clustering', fontsize=16);
        axc = sc.dendrogram(sc.linkage(self.firstdat, method='ward'),orientation='right', leaf_font_size=2)
        hierfig = self.basefolder+"Hiercluster.svg"
        plt.savefig(hierfig)
        
        # K-Means Clustering
        cols = self.kmdf.columns
        #print(cols)
        u_labels = np.unique(self.kmdf['clusters'])
        filtered_data = []
        figd, axd = plt.subplots()
        plt.title('K-Means Clustering', fontsize=16);
        for i in u_labels:
            filtered_data = self.kmdf[self.kmdf['clusters'] == i]
            axd = plt.scatter(filtered_data[cols[0]] ,filtered_data[cols[1]],label="Cluster "+str(i),s = 8)
            axd = plt.legend()
            filtered_data = []
        
        kfig = self.basefolder+"kmeanscluster.svg"
        plt.savefig(kfig)
        plt.show()     
        
        