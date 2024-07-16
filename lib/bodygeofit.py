import numpy as np
from open3d import geometry
import lib.ioply

class fitproc:
    def __init__(self,fold,filename,stcenter):
        self.fname = filename
        self.startcenter = stcenter
        self.folder_3D = fold

    def koerperarray(self,indexno,coefs,centers,punkte):
        
        koerpersammlung = [
        lib.koerper3D.koerper(punkte).torus(coefs,centers),
        lib.koerper3D.koerper(punkte).ellipsoid(coefs,centers),
        lib.koerper3D.koerper(punkte).parabolid(coefs,centers),
        lib.koerper3D.koerper(punkte).horcylinder(coefs,centers),
        lib.koerper3D.koerper(punkte).vertcylinder(coefs,centers)]
        #lib.koerper3D.koerper(400).spindle(coefs,centers)
        
        koerper3D = koerpersammlung[indexno]
        del koerpersammlung
        return koerper3D

    def cloudsyn (self,cloud,index,coef):
        testcloud = geometry.PointCloud()
        testcloud = lib.ioply.ioplynow("").fillpcd(testcloud,self.koerperarray(index,coef,self.startcenter,200))
        unterschied = geometry.PointCloud.compute_point_cloud_distance(cloud,testcloud)
        return unterschied
        
    def fitbody (self, cloud,index,coef):
        
        coef =(coef[0]*0.3,coef[1]*0.3,coef[2]*1.5)
        coef = list(coef)

        for i in range (2):
            
            unterschied = self.cloudsyn(cloud,index,coef)
            coef[i] = coef[i]+(np.median(unterschied)/10)
            unterschied1 = self.cloudsyn(cloud,index,coef)
            transcoef = coef

            while (np.quantile(unterschied1,0.2)<np.quantile(unterschied,0.2)):
                
                transcoef = coef
                print (np.quantile(unterschied,0.2))
                coef[i] = coef[i]+(np.median(unterschied)/10)
                unterschied = unterschied1
                unterschied1 = self.cloudsyn(cloud,index,coef)

        outfile = self.folder_3D+self.fname+"_fit.ply"
        transcloud = geometry.PointCloud()
        transcloud = lib.ioply.ioplynow("").fillpcd(transcloud,self.koerperarray(index,transcoef,self.startcenter,400))
        transcloud.remove_duplicated_points()
        lib.ioply.ioplynow(outfile).saveply(transcloud)
        return transcoef
        
        
            
