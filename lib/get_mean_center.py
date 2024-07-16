import numpy as np
from open3d import geometry

class center:
    def __init__(self,cloud):
        self.pointcoord = np.asarray(cloud.points)
    def centcalc(self):
        xarray = self.pointcoord[:,0]
        yarray = self.pointcoord[:,1]
        zarray = self.pointcoord[:,2]

        meancoord = []

        basiccoefs = []

        xmean = np.mean(xarray)
        ymean = np.mean(yarray)
        zmean = np.mean(zarray)


        meancoord.append(xmean)
        meancoord.append(ymean)
        meancoord.append(zmean)

        ctrx = xarray-xmean
        ctry = yarray-ymean

        posx = []
        negx = []
        posy = []
        negy = []

        
        for i in range (len(ctrx)):
            if ctrx[i] > 0:
                posx.append(ctrx[i])
            if ctrx[i] < 0:
                negx.append(ctrx[i])
        
        for i in range (len(ctry)):
            if ctry[i] > 0:
                posy.append(ctry[i])
            if ctry[i] < 0:
                negy.append(ctry[i])
        
        difposnegx = (np.mean(posx)+np.mean(negx))
        difposnegy = (np.mean(posx)+np.mean(negx))

        xmeancorr = xmean+np.absolute(2*difposnegx)
        ymeancorr = ymean+np.absolute(2*difposnegy)

        meancoord[0] = xmeancorr
        meancoord[1] = ymeancorr

        basiccoefs.append(np.max(ctrx))
        basiccoefs.append(np.max(ctry))
        basiccoefs.append(zmean)

        return meancoord,basiccoefs


        

        
