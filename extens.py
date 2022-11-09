

"""
Created on Sun Feb 14 11:03:17 2021

@author: Dr. Arndt Rohwedder, University of Huddersfield
"""
import numpy as np

class extens:
    
    def __init__(self,ellipsfactors,numparray,earray):
        self.cloudarray = numparray
        self.elfactors = ellipsfactors
        self.eleparray = earray
        
    def extensions (self):
        centre = self.elfactors[0]
        radius = self.elfactors[1]
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
        
        

        #ellipsoid array data
        #elx = self.eleparray[:,[0]]
        #ely = self.eleparray[:,[1]]
        #elz = self.eleparray[:,[2]]

        #elxdiffs = np.subtract(elx,cx)
        #elydiffs = np.subtract(ely,cy)
        #elzdiffs = np.subtract(elz,cz)
        
        #elsqxdiffs = np.square(elxdiffs)
        #elsqydiffs = np.square(elydiffs)
        #elsqzdiffs = np.square(elzdiffs)

        #elcosu = elxdiffs/np.sqrt(elsqxdiffs+elsqydiffs)
        #elcosv = np.sqrt(elsqxdiffs+elsqydiffs)/np.sqrt(elsqxdiffs+elsqydiffs+elsqzdiffs)
        
        
        #ellipsoid data ende
        
        lambd = np.arccos(cosu)
        theta = np.arccos(cosv)
        
        xpre = np.multiply(np.cos(theta), np.cos(lambd))
        ypre = np.multiply(np.cos(theta), np.sin(lambd))
        
        
        
        x = np.multiply(xpre,rx)
        #xneg = np.multiply(x,-1)
        y = np.multiply(ypre,ry)
        #yneg = np.multiply(y,-1)
        z = np.multiply(np.sin(theta),rz)
        #zneg = np.multiply(z,-1)
       
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
        
        #absdiff = np.subtract(orihypos,calchypos)
        
        #diffdiv = np.divide(orihypos,absdiff)
        
        #redx = np.divide(xdata,diffdiv)
        #redy = np.divide(ydata,diffdiv)
        #redz = np.divide(zdata,diffdiv)
        
        #redx = np.divide(redx,2*(np.pi))
        #redy = np.divide(redy,2*(np.pi))
        #redz = np.divide(redz,2*(np.pi))
        
        #print ("cosu: ",len (cosu), " orihypos: ", len(orihypos)," calchypos: ",len(calchypos)," x: ",len(x)," min xdiffs: ",min(xdiffs)," min xcalc: ",min(x))
        
        #ax = np.subtract(xdata,redx)
        #ay = np.subtract(ydata,redy)
        #az = np.subtract(zdata,redz)
 
        
        #xlang = np.concatenate((x,xneg),axis = 0)
        #xlang1 = np.concatenate((xlang,xneg),axis = 0)
        #xlang2 = np.concatenate((xlang1,x),axis = 0)
        #xlang3 = np.concatenate((xlang2,x),axis = 0)
        
        #ylang = np.concatenate((y,yneg),axis = 0)
        #ylang1 = np.concatenate((ylang,y),axis = 0)
        #ylang2 = np.concatenate((ylang1,yneg),axis = 0)
        #ylang3 = np.concatenate((ylang2,y),axis = 0)
        
        #zlang = np.concatenate((z,zneg),axis = 0)
        #zlang1 = np.concatenate((zlang,z),axis = 0)
        #zlang2 = np.concatenate((zlang1,z),axis = 0)
        #zlang3 = np.concatenate((zlang2,zneg),axis = 0)
        
        #xcorr = np.add(xlang3,cx)
        #ycorr = np.add(ylang3,cy)
        #zcorr = np.add(zlang3,cz)
        
        posx = []
        posy = []
        posz = []
        
        for was in list(range(orihypos.shape[0])):
            if (orihypos[was])>(calchypos[was]):
                posx.append(xdata[was])
                #posx.append(ax[was])
               
                posy.append(ydata[was])
                #posy.append(ay[was])
               
                posz.append(zdata[was])
                #posz.append(az[was])
                
        left = np.column_stack((posx,posy,posz))
        self.cloudarray = []
        
        return left, orihypos,calchypos
        