#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 21:46:59 2020

@author: Dr. Arndt Rohwedder, University of Huddersfield
"""
class wolkenmacher:
    
    def __init__(self,positivs):
        self.positive = positivs

    def makecloud (self):
        zwert = 0
        positions = []
        zeile = []
        poswert = 0
        wolke = []
        for zwert in list(range(len(self.positive))):
            positions = self.positive[zwert]
            for poswert in list(range(len(positions))):
                zeile.append(positions[poswert][1])
                zeile.append(positions[poswert][0])
                zeile.append(zwert)
                wolke.append(zeile)
                zeile = []
        return wolke