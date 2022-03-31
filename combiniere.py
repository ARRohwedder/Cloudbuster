#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 23:37:09 2020

@author: Dr. Arndt Rohwedder, University of Huddersfield
"""
class combiner:
    def __init__(self,sammelwolke,order):
        self.collect = sammelwolke
        self.ordnung = order

    def addingup (self):
        wowert = 0
        count = 0
        gesamt = []
        zwischena = []
        zeile = []
        gesamt = self.collect[0]
        for count in range(0,2):
            for wowert in list(range(len(self.collect[count+1]))):
                zwischena = self.collect[count+1][wowert]
                zeile.append(zwischena[self.ordnung[count][0]])
                zeile.append(zwischena[self.ordnung[count][1]])
                zeile.append(zwischena[self.ordnung[count][2]])
                gesamt.append(zeile)
                zeile = []
            zwischena=[]
        return gesamt