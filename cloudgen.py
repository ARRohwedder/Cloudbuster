#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 21:58:01 2020

@author: Dr. Arndt Rohwedder, University of Huddersfield
"""
import numpy as np
import wolki

class wolken:
    
    def __init__(self,stack):
        self.imstack = stack

        
    def combined (self):
        wolkenstack = np.empty(3, dtype=object)
        bild = 0        
        for bild in list(range(self.imstack.shape[0])):
            orig = wolki.wolkenmacher(self.imstack[bild])
            original = orig.makecloud()
            wolkenstack[bild] = original
        return wolkenstack