#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 16:43:04 2020

@author: Dr. Arndt Rohwedder, University of Huddersfield
"""
import numpy as np
import posi

class positionen:
    
    def __init__(self,stack):
        self.imstack = stack

        
    def combined (self):
        edgestack = np.empty(3, dtype=object)
        bild = 0        
        for bild in list(range(self.imstack.shape[0])):
            orig = posi.identpos(self.imstack[bild])
            original = orig.makepos()
            edgestack[bild] = original
        return edgestack


