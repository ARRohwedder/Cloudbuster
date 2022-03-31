

"""
Created on Sun Feb 14 11:03:17 2021

@author: Dr. Arndt Rohwedder, University of Huddersfield
"""
import numpy as np

class extens:
    
    def __init__(self,ellipsfactors,numparray):
        self.cloudarray = numparray
        self.elfactors = ellipsfactors
        
    def extensions (self):
        centre = self.elfactors[0]
        radius = self.elfactors[1]
        rx, ry, rz = radius
        cx,cy,cz = centre
        xdata = self.cloudarray[:, [0]]
        ydata = self.cloudarray[:, [1]]
        zdata = self.cloudarray[:, [2]]
        
        xdiffs = np.subtract(xdata,cx)
        ydiffs = np.subtract(ydata,cy)
        zdiffs = np.subtract(zdata,cz)
        
        sqxdiffs = np.square(xdiffs)
        sqydiffs = np.square(ydiffs)
        sqzdiffs = np.square(zdiffs)
        
        orihypos = np.sqrt(sqxdiffs+sqydiffs+sqzdiffs)
        
        cosu = xdiffs/np.sqrt(sqxdiffs+sqydiffs)
        cosv = np.sqrt(sqxdiffs+sqydiffs)/np.sqrt(sqxdiffs+sqydiffs+sqzdiffs)
        
        lambd = np.arccos(cosu)
        theta = np.arccos(cosv)
        
        xpre = np.multiply(np.cos(theta), np.cos(lambd))
        ypre = np.multiply(np.cos(theta), np.sin(lambd))
        
        x = np.multiply(xpre,rx)
        y = np.multiply(ypre,ry)
        z = np.multiply(np.sin(theta),rz)
        
        xcorr = np.add(x,cx)
        ycorr = np.add(y,cy)
        zcorr = np.add(z,cz)
        
        xsmdiffs = np.subtract(xcorr,cx)
        ysmdiffs = np.subtract(ycorr,cy)
        zsmdiffs = np.subtract(zcorr,cz)
        
        sqxsmdiffs = np.square(xsmdiffs)
        sqysmdiffs = np.square(ysmdiffs)
        sqzsmdiffs = np.square(zsmdiffs)
        
        calchypos = np.sqrt(sqxsmdiffs+sqysmdiffs+sqzsmdiffs)
        
        posx = []
        posy = []
        posz = []
        
        for was in list(range(orihypos.shape[0])):
            if (orihypos[was])>(calchypos[was]):
                posx.append(xdata[was])
                posy.append(ydata[was])
                posz.append(zdata[was])
                
        left = np.column_stack((posx,posy,posz))
        self.cloudarray = []
        
        return left, orihypos,calchypos
        