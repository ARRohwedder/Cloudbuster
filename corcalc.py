#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 18:10:53 2021

@author: Dr. Arndt Rohwedder
"""
import pandas as pd
from pandas import set_option
#from matplotlib import pyplot
from sklearn.preprocessing import StandardScaler
#import numpy

class corcalc:
    def __init__(self,pcadata, pcanames):
        self.topdata1 = pcadata
        self.topnames = pcanames
        
    def correlcalc (self):

        topdata = pd.DataFrame(self.topdata1)
        array = topdata.values
        data_scalar = StandardScaler().fit(array)
        data_rescaled = data_scalar.transform(array)
        newtop = pd.DataFrame(data_rescaled)
        correlations = newtop.corr(method='pearson')
        
        set_option('display.width', 100)
        set_option('precision', 2)

        return correlations