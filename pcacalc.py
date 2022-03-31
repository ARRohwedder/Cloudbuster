#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 17:18:45 2021

@author: Dr. Arndt Rohwedder
"""
from pca import pca
import pandas as pd

class pcacalc:
    def __init__(self,fulldata, datarray, selnames):
        self.selframe = fulldata
        self.seldata = datarray
        self.selcols = selnames
        
    def calcul (self):
        model = pca(n_components=0.95)
        results = model.fit_transform(self.seldata)
        
        features = results['topfeat']
        test = results['explained_var']
        count = 0
        for h in range(0, len(test)-1):
            if test[h]<0.96:
                count = count+1
            
        ranking = features[['feature']].to_numpy()

        topten = []
        for i in range(0, count):
            topten.append(self.selcols[int(ranking[i])-1])

        impParas = pd.DataFrame(self.selframe[topten])

        return topten, impParas, model, count
        