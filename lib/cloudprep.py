# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 14:05:42 2022

@author: Dr. Arndt Rohwedder, Johannes Keppler University, Linz
"""

import numpy as np

class wolke:
    
    def combined (self,stack):
        self.imstack = stack
        wolkenstack = np.empty(3, dtype=object)
        bild = 0
        for bild in list(range(self.imstack.shape[0])):
            zwert = 0
            positions = []
            zeile = []
            poswert = 0
            wolke = []
            positive = self.imstack[bild]
            for zwert in list(range(len(positive))):
                positions = positive[zwert]
                for poswert in list(range(len(positions))):
                    zeile.append(positions[poswert][1])
                    zeile.append(positions[poswert][0])
                    zeile.append(zwert)
                    wolke.append(zeile)
                    zeile = []
            wolkenstack[bild] = wolke
        return wolkenstack
    
    def addingup (self,sammelwolke):
        self.collect = sammelwolke
        #self.ordnung = order
        ordnung = [[0,2,1],[1,2,0]]
        wowert = 0
        count = 0
        gesamt = []
        zwischena = []
        zeile = []
        gesamt = self.collect[0]
        for count in range(0,2):
            for wowert in list(range(len(self.collect[count+1]))):
                zwischena = self.collect[count+1][wowert]
                zeile.append(zwischena[ordnung[count][0]])
                zeile.append(zwischena[ordnung[count][1]])
                zeile.append(zwischena[ordnung[count][2]])
                gesamt.append(zeile)
                zeile = []
            zwischena=[]
        sauber = np.unique(gesamt,axis=0)
        return gesamt
            
            