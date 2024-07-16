#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 18:10:53 2021

@author: Dr. Arndt Rohwedder, Johannes Keppler University, Linz
"""
import pandas as pd
from pandas import set_option
from sklearn.preprocessing import StandardScaler
import numpy as np

class corcalc:
    def __init__(self,pcadata, pcanames, pcascale, fold):
        self.topdata1 = pcadata
        self.pca_topten = pcanames
        self.pcadf_scaled = pcascale
        self.basefolder = fold
        
    def correlcalc (self):
        toptenar = np.asarray(self.topdata1)
        topdata = pd.DataFrame(toptenar)
        array = topdata.values
        data_scalar = StandardScaler().fit(array)
        data_rescaled = data_scalar.transform(array)
        newtop = pd.DataFrame(data_rescaled)
        correlations = newtop.corr(method='pearson')
        
        set_option('display.width', 100)
        cordataname = self.basefolder+"Correlation.csv"
        correlations.to_csv(cordataname)
        pcacorred = correlations.drop(correlations.index[[0]])
        firstcol = pcacorred[pcacorred.columns[0:1]].to_numpy()
        pos_text = []
        neg_text = []
        for j in range(0,firstcol.shape[0]):
            if firstcol[j][0] >= 0:
                pos_text.append(self.pca_topten[j+1])
            if firstcol[j][0] < 0:
                neg_text.append(self.pca_topten[j+1])
        pos_df = self.pcadf_scaled[pos_text].mean(axis=1)
        neg_df = self.pcadf_scaled[neg_text].mean(axis=1)
        
        #for grouped data
        
        pre_data = self.pcadf_scaled.groupby(self.pcadf_scaled['Samplenames']).mean()
        grouparray = np.asarray(pre_data.index)
        data_rotated = pre_data.T
        rotated_array = data_rotated.values
        rotated_data_scalar = StandardScaler().fit(rotated_array)
        rotated_data_rescaled = rotated_data_scalar.transform(rotated_array)
        new_rotated = pd.DataFrame(rotated_data_rescaled)
        samplecorr = new_rotated.corr(method='pearson')
            
        #set_option('precision', 2)

        return correlations, pos_df, neg_df, samplecorr, grouparray