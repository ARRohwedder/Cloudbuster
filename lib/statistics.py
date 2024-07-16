# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 11:06:19 2022

@author: Dr. Arndt Rohwedder, Johannes Keppler University, Linz
"""


import pandas as pd
from pandas import set_option
import numpy as np
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sc
import re

class statistics:
    
    def __init__(self,dire,dat,sta,stb,nam,nameparam):
        self.basefolder = dire
        self.Sphdata = dat
        self.strings = sta
        self.strings1 = stb
        self.sname = nam
        self.namparam = nameparam
        
    def compute (self):
        for a in range(0,len(self.strings)):
            del self.Sphdata[self.strings[a]]
        emp_lis = []
        
        selectedddata = self.Sphdata

        for z in range(1,self.Sphdata.shape[1]):
            
            wert = self.Sphdata.iat[1,z]
            new_result = re.findall('[0-9]+', wert)

            if wert.isdigit():
                emp_lis.append(int(z))
            if new_result != []:
                if len(new_result) < 2:
                    self.Sphdata.iloc[:,z] = self.Sphdata.iloc[:,z].astype(float)
                if len(new_result) >= 2:
                    self.Sphdata.iloc[:,z] = self.Sphdata.iloc[:,z].astype(float)
        floats = self.Sphdata.loc[:, self.Sphdata.dtypes == 'float64']
        ints = self.Sphdata.loc[:, self.Sphdata.dtypes == 'int64']
        seldata = pd.concat([floats, ints], axis=1, join='inner')
        
        datacount = seldata.shape[0]
        samplenames = self.Sphdata[[self.strings1[0]]]
        smplnamen = self.Sphdata[self.namparam].to_numpy()#Experiment, 'File'
        
        #PCA
        
        import lib.pcacalc

        calcpca = lib.pcacalc.pcacalc(selectedddata,self.basefolder,samplenames,self.sname,self.namparam)
        
        pcares = calcpca.calcul()
        pca_topten = pcares[0]
        pca_topten_txt = pcares[1]
        pcadf_scaled = pcares[2]

        shortdata = selectedddata[pca_topten]
        # plotting
        print ("PCA Analysis")
        smplnamen = pcadf_scaled['Samplenames'].to_numpy()
            
        #Correlation
        import lib.corcalc
        
        correl = lib.corcalc.corcalc(shortdata,pca_topten,pcadf_scaled, self.basefolder)
        pcacor = correl.correlcalc()
        print ("Correlation")
        
        #plotting

        first = pcacor[1].to_numpy()
        second = pcacor[2].to_numpy()
        figb, axb = plt.subplots(figsize=(10, 9))
        plt.title('Correlation of top rated Parameters', fontsize=12);
        cax = axb.matshow(pcacor[0], vmin=-1, vmax=1,cmap=plt.cm.RdYlGn)
        figb.colorbar(cax)
        figb.show()
        axb.xaxis.set_ticks_position("bottom")

        corfig = self.basefolder+"Correlation.svg"
        plt.savefig(corfig)
        
        figs, axs = plt.subplots(figsize=(14, 13))
        plt.title('Correlation of Samples', fontsize=12);
        cax = axs.matshow(pcacor[3], vmin=-1, vmax=1,cmap=plt.cm.RdYlGn)
        figs.colorbar(cax)
        figs.show()
        axs.xaxis.set_ticks_position("bottom")

        corfigsam = self.basefolder+"Sample_Correlation.svg"
        plt.savefig(corfigsam)

        # For grouped data

        if datacount > 10:
            #Hierarchical Clustering
            import lib.hierclu
            hiera = lib.hierclu.HierClu(pca_topten,first,second,samplenames,self.basefolder)
            hierc = hiera.hiercalc()
            
            figc, axc = plt.subplots(figsize=(8, 10))
            plt.title('Hierarchical Clustering', fontsize=16);
            axc = sc.dendrogram(sc.linkage(hierc, method='ward'),orientation='right', leaf_font_size=2)
            figc.show()
            hierfig = self.basefolder+"Hiercluster.svg"
            plt.savefig(hierfig)
            
            print ("Hierarchical Clustering")
            #DBSCAN clustering
            import lib.kmeans

            kminit = lib.kmeans.myKMeans(self.Sphdata,first,second,pca_topten,self.basefolder,smplnamen,self.namparam)

            clusters = kminit.KMeanscalc()
            print ("DBSCAN clustering")

        text = "PCA : Most relevant (95% of variances) parameters= \n"+pca_topten_txt+"\n\n"+" \n\n"+"Detailed results stored as .csv files and graphs as .svg files in folder: \n"+self.basefolder
        
        return text
            
            
        
        
        
