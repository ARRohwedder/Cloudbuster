#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 17:18:45 2021

@author: Dr. Arndt Rohwedder, Johannes Keppler University, Linz
"""
from pca import pca
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

class pcacalc:
    def __init__(self,fulldata, fold, smlnames,nam,nameparam):
        self.selframe = fulldata
        self.basefolder = fold
        self.samplenames = smlnames
        self.sname = nam
        self.namparam = nameparam
        
        
    def calcul (self):
        namen = self.selframe[self.namparam].to_numpy()#"File"
        del self.selframe[self.namparam]#"File"
        selarray = self.selframe.values
        data_scalar = StandardScaler().fit(selarray)
        
        data_rescaled = data_scalar.transform(selarray)
        
        selnames = np.asarray(self.selframe.columns)
        
        model = pca(n_components=0.95)
        results = model.fit_transform(data_rescaled)
        
        features = results['topfeat']
        test = results['explained_var']
        count = 0
        for h in range(0, len(test)-1):
            if test[h]<0.96:
                count = count+1
            
        ranking = features[['feature']].to_numpy()

        topten = []

        for i in range(0, count):
            topten.append(selnames[int(ranking[i])-1])

        pca_topten = list(dict.fromkeys(topten))
        pca_toptxt = []
        shortdata = self.selframe[pca_topten]

        for h in range(0,len(pca_topten)):
            pca_toptxt.append(pca_topten[h])
        pca_topten_txt = ", ".join(pca_toptxt)
        pcadf = pd.DataFrame(pca_topten)
        pcadataname = self.basefolder+"PCA_top.csv"
        pcadf.to_csv(pcadataname)
        pcadataname = self.basefolder+"PCA_top_raws.csv"
        shortdata.to_csv(pcadataname)
        testout = self.basefolder+"Scaled_toprated.csv"
        column_headers = list(shortdata.columns.values)
        pcadfarray = np.asarray(shortdata)
        pcadf_scalar = StandardScaler().fit(pcadfarray)
        pcadf_rescaled = pcadf_scalar.transform(pcadfarray)
        pcadf_scaled = pd.DataFrame(pcadf_rescaled)
        
        pcadf_scaled.columns =column_headers
        
        print (pcadf_scaled.shape," ",namen[0])
        
        pcadf_scaled.insert(0,"Samplenames",namen.tolist(),True)
        pcadf_scaled.to_csv(testout)

        return pca_topten, pca_topten_txt, pcadf_scaled, model
        
