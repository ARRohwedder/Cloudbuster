#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 16:32:28 2021

@author: Dr. Arndt Rohwedder, University of Huddersfield
"""
import numpy as np

class ellipsave:
    def __init__(self,basedata,datasize,wolke):
        self.data = basedata
        self.xsize = datasize
        self.cloudarray = wolke

    def ellipsoid_save(self):
        ellipsoid = []
        codata = self.data[1]
        coefs = (codata[0],codata[1],codata[2])
        
        rx, ry, rz = coefs
        
        cendata = self.data[0]
        centre = (cendata[0],cendata[1],cendata[2])
        cx,cy,cz = centre
        
        xdata = self.cloudarray[:, [0]]
        ydata = self.cloudarray[:, [1]]
        zdata = self.cloudarray[:, [2]]
        
        xdiffs = np.subtract(xdata,cx)
        ydiffs = np.subtract(ydata,cy)
        zdiffs = np.subtract(zdata,cz)
        
        sqxdiffs = np.multiply(xdiffs,xdiffs)
        sqydiffs = np.multiply(ydiffs,ydiffs)
        sqzdiffs = np.multiply(zdiffs,zdiffs)
        
        cosu = xdiffs/np.sqrt(sqxdiffs+sqydiffs)
        lambd = np.arccos(cosu)
        
        cosv = np.sqrt(sqxdiffs+sqydiffs)/np.sqrt(sqxdiffs+sqydiffs+sqzdiffs)
        theta = np.arccos(cosv)
        
        xpre = np.multiply(np.cos(theta), np.cos(lambd))
        x = np.multiply(xpre,rx)
        xneg = np.multiply(x,-1)
        
        ypre = np.multiply(np.cos(theta), np.sin(lambd))
        y = np.multiply(ypre,ry)
        yneg = np.multiply(y,-1)
        
        z = np.multiply(np.sin(theta),rz)
        zneg = np.multiply(z,-1)
        
        xlang = np.concatenate((x,xneg),axis = 0)
        xlang1 = np.concatenate((xlang,xneg),axis = 0)
        xlang2 = np.concatenate((xlang1,x),axis = 0)
        xlang3 = np.concatenate((xlang2,x),axis = 0)
        
        ylang = np.concatenate((y,yneg),axis = 0)
        ylang1 = np.concatenate((ylang,y),axis = 0)
        ylang2 = np.concatenate((ylang1,yneg),axis = 0)
        ylang3 = np.concatenate((ylang2,y),axis = 0)
        
        zlang = np.concatenate((z,zneg),axis = 0)
        zlang1 = np.concatenate((zlang,z),axis = 0)
        zlang2 = np.concatenate((zlang1,z),axis = 0)
        zlang3 = np.concatenate((zlang2,zneg),axis = 0)
        
        xcorr = np.add(xlang3,cx)
        ycorr = np.add(ylang3,cy)
        zcorr = np.add(zlang3,cz)
        
        ellipsoidraw = np.column_stack((xcorr,ycorr,zcorr))
        ellipsoid = np.unique(ellipsoidraw,axis=0)
        
        return ellipsoid
