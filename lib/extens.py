

"""
Created on Sun Feb 14 11:03:17 2021

@author: Dr. Arndt Rohwedder, University of Huddersfield
"""
import numpy as np

class extens:
    
    def __init__(self,fact,numparray):
        self.cloudarray = numparray
        self.factors = fact
        
    def collect (self,hyp1,hyp2,xdata,ydata,zdata):
        
        posx = []
        posy = []
        posz = []
        
        for was in list(range(hyp1.shape[0])):
            if (hyp1[was])>(hyp2[was]):
                posx.append(xdata[was])
                posy.append(ydata[was])
                posz.append(zdata[was])
        left = np.column_stack((posx,posy,posz))
        leftclean = np.unique(left,axis=0)
        
        return leftclean
        
    def ellipext (self):
        centre = self.factors[0]
        radius = self.factors[1]
        rx, ry, rz = radius
        cx,cy,cz = centre

        #original cloud data
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

        left = self.collect(orihypos,calchypos,xdata,ydata,zdata)

        #posx = []
        #posy = []
        #posz = []
        
        #for was in list(range(orihypos.shape[0])):
        #    if (orihypos[was])>(calchypos[was]):
        #        posx.append(xdata[was])
        #        posy.append(ydata[was])
        #        posz.append(zdata[was])
                
        #left = np.column_stack((posx,posy,posz))
        self.cloudarray = []
        
        return left
    
    def torusext (self):
        centre = self.factors[0]
        radius = self.factors[1]

        rx, ry, rz = radius
        cx,cy,cz = centre
        
        A = rx
        B = ry
        A1 = rz
        B1 = B/2
        
        xdata = self.cloudarray[:, [0]]
        ydata = self.cloudarray[:, [1]]
        zdata = self.cloudarray[:, [2]]
        
        xdiffs = np.subtract(xdata,cx)
        ydiffs = np.subtract(ydata,cy)
        zdiffs = np.subtract(zdata,cz)
        
        firsthypos = np.hypot(xdiffs,ydiffs)
        
        thetas1 = np.arctan(xdiffs/ydiffs)
        
        rthetas1 = (A*B)/(np.sqrt(np.square(B*np.cos(thetas1))+np.square(A*np.sin(thetas1))))
        
        difs1 = rthetas1 - firsthypos
        
        newx = difs1 * np.sin(thetas1)
        
        thetas2 = np.arctan(newx/zdiffs)
        
        secondhypos = np.hypot(newx,zdiffs)
        
        rthetas2 = (A1*B1)/(np.sqrt(np.square(B1*np.cos(thetas2))+np.square(A1*np.sin(thetas2))))
        
        posx = []
        posy = []
        posz = []
        #print (secondhypos.shape[0]," ",rthetas2.shape[0]," ",len(xdata))
        for was in list(range(secondhypos.shape[0])):
            if (secondhypos[was])>(rthetas2[was]):
                #print(was)
                posx.append(xdata[was])
                posy.append(ydata[was])
                posz.append(zdata[was])
        
        #print (firsthypos.shape[0]," ",rthetas1.shape[0]," ",len(xdata))
        for was in list(range(firsthypos.shape[0])):
            if (firsthypos[was])>(rthetas1[was]):
                posx.append(xdata[was])
                posy.append(ydata[was])
                posz.append(zdata[was])
                
        left = np.column_stack((posx,posy,posz))
        leftclean = np.unique(left,axis=0)
        self.cloudarray = []

        return leftclean
        
    def paraext (self):
        centre = self.factors[0]
        radius = self.factors[1]
        rx, ry, rz = radius
        cx,cy,cz = centre

        A = rx
        B = ry
        
        xdata = self.cloudarray[:, [0]]
        ydata = self.cloudarray[:, [1]]
        zdata = self.cloudarray[:, [2]]
        
        xdiffs = np.subtract(xdata,cx)
        ydiffs = np.subtract(ydata,cy)
        
        factx = A/np.square(rz)
        facty = B/np.square(rz)
        
        aatz = np.sqrt(zdata/factx)
        batz = np.sqrt(zdata/facty)
        
        firsthypos = np.hypot(xdiffs,ydiffs)
        
        thetas1 = np.arctan(xdiffs/ydiffs)
        
        rthetas1 = (aatz*batz)/(np.sqrt(np.square(batz*np.cos(thetas1))+np.square(aatz*np.sin(thetas1))))
        
        left = []
        posx = []
        posy = []
        posz = []
        
        for was in list(range(firsthypos.shape[0])):
            if (firsthypos[was])>(rthetas1[was]):
                posx.append(xdata[was])
                posy.append(ydata[was])
                posz.append(zdata[was])
                
        left = np.column_stack((posx,posy,posz))
        
        self.cloudarray = []
        
        return left
    
    def horcyext (self):
        
        centre = self.factors[0]
        radius = self.factors[1]
        rx, ry, rz = radius
        cx,cy,cz = centre
        
        A = rx
        B = rz
        
        xdata = self.cloudarray[:, [0]]
        ydata = self.cloudarray[:, [1]]
        zdata = self.cloudarray[:, [2]]
        
        xdiffs = np.subtract(xdata,cx)
        zdiffs = np.subtract(zdata,cz)
        
        firsthypos = np.hypot(zdiffs,xdiffs)
        
        thetas1 = np.arctan(zdiffs/xdiffs)
        
        rthetas1 = (A*B)/(np.sqrt(np.square(B*np.cos(thetas1))+np.square(A*np.sin(thetas1))))
        
        left = []
        posx = []
        posy = []
        posz = []
        
        for was in list(range(firsthypos.shape[0])):
            if (firsthypos[was])>(rthetas1[was]):
                posx.append(xdata[was])
                posy.append(ydata[was])
                posz.append(zdata[was])
                
        left = np.column_stack((posx,posy,posz))
        
        self.cloudarray = []
        
        return left
    
    def vertcylext (self):
        
        centre = self.factors[0]
        radius = self.factors[1]
        rx, ry, rz = radius
        cx,cy,cz = centre
        
        A = rx
        B = ry
        
        xdata = self.cloudarray[:, [0]]
        ydata = self.cloudarray[:, [1]]
        zdata = self.cloudarray[:, [2]]
        
        xdiffs = np.subtract(xdata,cx)
        ydiffs = np.subtract(ydata,cy)
        
        firsthypos = np.hypot(xdiffs,ydiffs)
        
        thetas1 = np.arctan(xdiffs/ydiffs)
        
        rthetas1 = (A*B)/(np.sqrt(np.square(B*np.cos(thetas1))+np.square(A*np.sin(thetas1))))
        
        left = []
        posx = []
        posy = []
        posz = []
        
        for was in list(range(firsthypos.shape[0])):
            if (firsthypos[was])>(rthetas1[was]):
                posx.append(xdata[was])
                posy.append(ydata[was])
                posz.append(zdata[was])
                
        left = np.column_stack((posx,posy,posz))
        
        self.cloudarray = []
        
        return left
    
    def spindleext (self):
        
        centre = self.factors[0]
        radius = self.factors[1]
        rz, ry, rx = radius
        cz,cy,cx = centre
        
        xdata = self.cloudarray[:, [0]]
        ydata = self.cloudarray[:, [1]]
        zdata = self.cloudarray[:, [2]]
        
        xdiffs = np.subtract(zdata,cx)
        ydiffs = np.subtract(ydata,cy)
        zdiffs = np.subtract(xdata,cz)
        
        A = rx
        B = ry
        
        factx = A/np.square(rz)
        facty = B/np.square(rz)
        
        aatz = np.sqrt(zdata/factx)
        batz = np.sqrt(zdata/facty)
        
        firsthypos = np.hypot(xdiffs,ydiffs)
        
        thetas1 = np.arctan(xdiffs/ydiffs)
        
        rthetas1 = (aatz*batz)/(np.sqrt(np.square(batz*np.cos(thetas1))+np.square(aatz*np.sin(thetas1))))
        
        left = []
        posx = []
        posy = []
        posz = []
        
        for was in list(range(firsthypos.shape[0])):
            if (firsthypos[was])>(rthetas1[was]):
                posx.append(xdata[was])
                posy.append(ydata[was])
                posz.append(zdata[was])
                
        left = np.column_stack((posx,posy,posz))
        
        self.cloudarray = []
        
        return left
        
        #=(D2*D3)/WURZEL(POTENZ((D3*COS(F6));2)+POTENZ((D2*SIN(F6));2))
        
        
        