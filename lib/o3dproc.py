# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 15:38:45 2022

@author: Dr. Arndt Rohwedder, Johannes Keppler University, Linz
"""

from open3d import geometry
from open3d import utility
import numpy as np

import lib.orientation
import lib.volumeandsurface
import lib.koerper3D
import lib.extens
import lib.ioply
import lib.get_mean_center
import lib.bodygeofit

class o3dmeth:
    def __init__(self,filename,imfolder):
        self.ofilename = filename
        self.folder_3D = imfolder
        self.resheader = (
        "PCL_max_x_size",#0
        "PCL_max_y_size",#1
        "PCL_ratio_YX_size",#2
        "PCL_ratio_YZ_size",#3
        "PCL_ratio_XZ_size",#4
        "PCL_shape_hint",#5
        "Sep_Comp_Count",#6
        "Spheroid_rotation_X",#7
        "Spheroid_rotation_Y",#8
        "Spheroid_rotation_Z",#9
        "Spheroid_max_x_size",#10
        "Spheroid_max_y_size",#11
        "Spheroid_ratio_YX_size",#12
        "Spheroid_ratio_YZ_size",#13
        "Spheroid_ratio_XZ_size",#14
        "Spheroid_surface_area",#15
        "Spheroid_Volume",#16
        "Spheroid_shape_hint",#17
        "Dev.Torus",#18
        "Dev.Ellipsoid",#19
        "Dev.Parabolid",#20
        "Dev.Hor. Cylinder",#21
        "Dev.Vert.Cylinder",#22"Dev.Spindle",#23
        "Med_Dist_Sph_to_Frag",#24
        "Av_Dist_Sph_to_Frag",#25
        "Var_Dist_Sph_to_Frag",#26
        "Max_Dist_Sph_to_Frag",#27
        "Med_Surf_of_Frag",#28
        "Av_Surf_of_Frag",#29
        "Var_Surf_of_Frag",#30
        "Max_Surf_of_Frag",#31
        "Med_Vol_of_Frag",#32
        "Av_Vol_of_Frag",#33
        "Var_Vol_of_Frag",#34
        "Max_Vol_of_Frag",#35
        'Ext_Count',#36
        'Ext_Max_Surface',#37
        'Ext_Av_Surface',#38
        'Ext_Med_Surface',#39
        'Ext_Surface_sum',#40
        'Ext_Max_length',#41
        'Ext_Av_length',#42
        'Ext_Med_length',#43
        'Ext_Av_Var_length',#44
        'Brim',#45
        'Narrow',#46
        'Broad',#47
        'Small',#48
        "PixResol")#49

        self.center = []
        self.bcoef = []
 
       
    def orientcalc (self,pcloud):
        
        box = pcloud.get_oriented_bounding_box()
        boxpunkte = np.asarray(box.get_box_points())
        ori = lib.orientation.orient(boxpunkte)
        (corr,angl) = ori.get_orientation()
        return corr,angl
    
    def form (self, boxform):
        if ((boxform[0]/boxform[1])< 0.9) or ((boxform[0]/boxform[1])> 1.1):
            inter = "elongated or directed"
        else:
            inter = "round or even spread"
        return inter
    
    def rotatecloud (self,cloud,corrections):
        
        matrixwhat = cloud.get_axis_aligned_bounding_box()
        punkte = np.asarray(matrixwhat.get_box_points())
        box = geometry.PointCloud()
        box = lib.ioply.ioplynow("").fillpcd(box,punkte)
        bigcenter = box.get_center()
        R = cloud.get_rotation_matrix_from_axis_angle(corrections)
        wolke = cloud.rotate(R,bigcenter)
        del matrixwhat
        del punkte
        del box
        del bigcenter
        del R
        return (wolke)
    
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
        
    
    def shapetest (self, cloud, corrections):
        
        namen = ['Torus','Ellipsoid','Parabolid','Hor. Cylinder','Vert. Cylinder']#,'Spindle'
        wolke = self.rotatecloud(cloud, corrections)
        bigform = wolke.get_max_bound()
        bigcenter = self.center
        coef = (self.bcoef[0]/2,self.bcoef[1]/2,self.bcoef[2]/2)
        pcd = geometry.PointCloud()
        bestvekt = []
        for i in range(len(namen)):
        
            pcd2 = lib.ioply.ioplynow("").fillpcd(pcd,self.koerperarray(i,coef,bigcenter,200))

            diff = wolke.compute_point_cloud_distance(pcd2)
            print (namen[i]," Difference -> ",np.mean(diff))
            diffvekt = np.sum(diff)
            bestvekt.append(diffvekt)
        alle = np.sum(bestvekt)
        prozentbest = []
        for i in range(len(namen)):
            prozentbest.append(bestvekt[i]/alle*100)

        bestfit = namen[np.argmin(bestvekt)]
        
        del wolke
        del namen
        del bigform
        del bigcenter
        del coef
        del pcd
        del bestvekt
        del pcd2
        del diff
        del diffvekt
        del alle
        return prozentbest,bestfit
    
    def fullpcl (self, cloud,resol,colorcloud):
                
        resultcoll = []
        wolkenform = cloud.get_max_bound()
        
        (correction,angles) = self.orientcalc(cloud)
        interpret = "Spread "+self.form(wolkenform)
        labels = np.array(cloud.cluster_dbscan(eps=2*self.reso, min_points=10, print_progress=False))
        print ("fullpcl")
        max_label = labels.max()
        partcount = max_label + 1
        resultcoll.append(str(round((wolkenform[0]*self.reso),4)))
        resultcoll.append(str(round((wolkenform[1]*self.reso),4)))
        resultcoll.append(str(round((wolkenform[1]/wolkenform[0]),4)))
        resultcoll.append(str(round((wolkenform[1]/wolkenform[2]),4)))
        resultcoll.append(str(round((wolkenform[0]/wolkenform[2]),4)))
        resultcoll.append(interpret)
        resultcoll.append(str(partcount))

        for winkel in range(len(angles)):
            resultcoll.append(str(angles[winkel]))

        lib.ioply.ioplynow(colorcloud).savecolorply(cloud,labels)
        del wolkenform
        del correction
        del angles
        
        
        return (labels,max_label,partcount,resultcoll)

    def surfvolcalc (self,pcl, res):
        covex, _ = pcl.compute_convex_hull()
        surface = covex.get_surface_area()
        surface = surface*(res*res)        
        volume = covex.get_volume()
        volume = volume*(res*res*res)
        del covex
        
        return surface, volume
    
    def bigpcl (self,cloud,labels,max_label,resultcoll, bigname):
        
        laenger = 0
        labpos = 0
        for gross in list(range(max_label + 1)):
            results2 = np.where(labels == gross)
            resultlist2 = list(results2[0])
            lang = len(resultlist2)
            if lang > laenger:
                laenger = lang
                labpos = gross
        result = np.where(labels == labpos)
        resultlist = list(result[0])
        print ("bigpcl")
        bigone = cloud.select_by_index(resultlist)
        
        if int(max_label  +1 ) < 2:
            bigcloud1 = cloud
        else:
            bigcloud1 = bigone
            
        (self.center,self.bcoef) = lib.get_mean_center.center(bigcloud1).centcalc()

        bigform = self.bcoef * 2
        
        (correction,angles) = self.orientcalc(bigcloud1)

        (surface,volume) = self.surfvolcalc(bigcloud1,self.reso)

        lib.ioply.ioplynow(bigname).saveply(bigcloud1)
        
        resultcoll.append(str(round((bigform[0]*self.reso),4)))
        resultcoll.append(str(round((bigform[1]*self.reso),4)))
        resultcoll.append(str(round((bigform[1]/bigform[0]),4)))
        resultcoll.append(str(round((bigform[1]/bigform[2]),4)))
        resultcoll.append(str(round((bigform[0]/bigform[2]),4)))
        resultcoll.append(str(round(surface,4)))
        resultcoll.append(str(round(volume,4)))
        interpret = "Spheroid "+self.form(bigform)
        resultcoll.append(interpret)
        (prozentbest,bestfit) = self.shapetest(bigcloud1,correction)
        for shapeprozent in range(len(prozentbest)):
            resultcoll.append(str(round(prozentbest[shapeprozent],4)))
        print ('Best shape = ',bestfit)
        del laenger
        del labpos
        del results2
        del resultlist2
        del lang
        del result
        del resultlist
        del bigone
        del bigform
        del correction
        del angles
        del surface
        del volume
        del interpret
        return bigcloud1,resultcoll,bestfit
    
    def surfcalc (self,pcl):
        try:
            pcl.estimate_normals()
            form = pcl.get_max_bound()
            sizeform = int(np.max(form))        
            distances = pcl.compute_nearest_neighbor_distance()
            avg_dist = np.mean(distances)
            radii = [10*avg_dist,10*avg_dist,10*avg_dist]
            #rec_mesh = geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(pcl, utility.DoubleVector(radii))
            covex, _ = pcl.compute_convex_hull()
            #rec_mesh.compute_vertex_normals()

            del pcl
            del form
            del sizeform
            del distances
            del avg_dist
            del radii
            
            surface = covex.get_surface_area()

        except:
            surface = 0
            
        return surface
    
            
    def extfract(self,extcloud,fitcloud,labels,max_label,partcount,outfile,indheader,resultscoll):
        types = ['Brim','Broad','Narrow','Small']
        brim = 0
        narrow = 0
        broad = 0
        small = 0
        
        sizevect = []
        medvect = []
        avvect = []
        varvect = []
        maxvect = []
        typearray = []
        maxdistarray = []
        
        fitarray = np.asarray(fitcloud.points)
        fitarraysize = fitarray.shape[0]
        arealimit = fitarraysize*0.02
        
        fitsize = fitcloud.get_max_bound()
        lengthlimit = (fitsize.max()/2)*0.15
        
        if int(partcount) >= 1:
            outfile = self.resultsfold+self.ofilename+"_ind_exten_results.csv"
            resfile = open( outfile , "w" )
            resfile.writelines(indheader)
            for gross in list(range(max_label+1)):
                results2 = np.where(labels == gross)
                resultlist2 = list(results2[0])
                testcloud = extcloud.select_by_index(resultlist2)
                extpointno = len(testcloud.points)
                if extpointno >= 10:
                    
                    distance =  testcloud.compute_point_cloud_distance(fitcloud)
                    distancearray = np.asarray(distance)
                    size = self.surfcalc(testcloud)*self.reso*self.reso
                    maxdist = np.max(distancearray)
                    avdist = np.average(distancearray)
                    mddist = np.median(distancearray)
                    vardist = np.var(distancearray)
                    maxdistextension =  distancearray.max()
                
                #Brim
                    if maxdistextension <= lengthlimit and size >= arealimit:
                        classification = types[0]
                #Broad
                    if maxdistextension > lengthlimit and size >= arealimit:
                        classification = types[1]
                #Narrow
                    if maxdistextension > lengthlimit and size < arealimit:
                        classification = types[2]
                #Small
                    if maxdistextension <= lengthlimit and size < arealimit:
                        classification = types[3]
                    line = str(gross+1)+","+str(size)+","+str(maxdist)+","+classification+"\n"
                    sizevect.append(size)
                    maxvect.append(maxdist*self.reso)
                    avvect.append(avdist*self.reso)
                    medvect.append(mddist*self.reso)
                    varvect.append(vardist*self.reso)
                    typearray.append(classification)
                    resfile.writelines(line)
                    
                if extpointno < 10:
                    partcount = partcount-1
            resfile.close()
            del testcloud
            del distance
            del fitcloud
            del fitarray
                          
        
        if int(partcount) < 1:
            
            size = 0
            maxdistextension = 0
            maxdist = 0
            avdist = 0
            mddist = 0
            vardist = 0
            classification = 0
            
            sizevect.append(size)
            maxvect.append(maxdist)
            avvect.append(avdist)
            medvect.append(mddist)
            varvect.append(vardist)
            typearray.append(classification)
            
        for i in range(len(typearray)):
            if np.isin('Brim',typearray[i]) == True:
                brim += 1
            if np.isin('Narrow',typearray[i]) == True:
                narrow += 1
            if np.isin('Broad',typearray[i]) == True:
                broad += 1
            if np.isin('Small',typearray[i]) == True:
                small += 1

        maxsize = np.max(sizevect)
        avsize = np.average(sizevect)
        medsize = np.median(sizevect)
        sumsize = np.sum(sizevect)
        maxlength = np.max(maxvect)
        avlength = np.average(avvect)
        medlength = np.average(medvect)
        varlength = np.average(varvect)
        vectors = [partcount,maxsize,avsize,medsize,sumsize,maxlength,avlength,medlength,varlength,brim,narrow,broad,small]
        
        for res in range (len(vectors)):
            resultscoll.append(str(round((vectors[res]),4)))
            
        return resultscoll

    def pclfract(self,cloud,bigcloud1,labels,max_label,partcount,outfile,indheader,resultcoll):
        
        distvectors =[]
        surfacevectors = []
        volumevectors = []
        medvect = 0
        avvect = 0
        varvect = 0
        maxvect = 0
        
        indsurfmed = 0
        indsurfav = 0
        indsurfvar = 0
        indsurfmax = 0
        
        indvolmed = 0
        indvolav = 0
        indvolvar = 0
        indvolmax = 0
        
        if int(partcount) > 1:
            outfile = self.resultsfold+self.ofilename+"_ind_parts_results.csv"
            resfile = open( outfile , "w" )
            resfile.writelines(indheader)
            for gross in list(range(max_label + 1)):
                results2 = np.where(labels == gross)
                resultlist2 = list(results2[0])
                testcloud = cloud.select_by_index(resultlist2)
                distance =  bigcloud1.compute_point_cloud_distance(testcloud)
                distancearray = np.asarray(distance)
                extpointno = len(testcloud.points)
                if extpointno >= 10:
                    (indsurf,indvol) = self.surfvolcalc(testcloud,self.reso)
                    surfarray = np.asarray(indsurf)
                    volarray = np.asarray(indvol)
                    size = indsurf
                    if (distancearray.mean()) > 1:
                        distvectors.append(distancearray.mean())
                        surfacevectors.append(surfarray.mean())
                        volumevectors.append(volarray.mean())
                    line = str(gross+1)+","+str(size)+","+str(np.average(distancearray))+"\n"
                    resfile.writelines(line)
                if extpointno < 10:
                    partcount = partcount-1
            resfile.close()
            del testcloud
            del distance
            del distancearray
            del surfarray
            del volarray
            del cloud
            del bigcloud1
            
            medvect = np.median(distvectors)
            avvect = np.average(distvectors)
            varvect = np.var(distvectors)
            maxvect = np.max(distvectors)
            
            indsurfmed = np.median(surfacevectors)
            indsurfav = np.average(surfacevectors)
            indsurfvar = np.var(surfacevectors)
            indsurfmax = np.max(surfacevectors)
            
            indvolmed = np.median(volumevectors)
            indvolav = np.average(volumevectors)
            indvolvar = np.var(volumevectors)
            indvolmax = np.max(volumevectors)
            
        vectmedavvar = [medvect,avvect,varvect,maxvect]
        vectsurfmedavvarmax = [indsurfmed,indsurfav,indsurfvar,indsurfmax]
        vectvolmedavvarmax = [indvolmed,indvolav,indvolvar,indvolmax]
        
        for medavvar in range(len(vectmedavvar)):
            resultcoll.append(str(round((vectmedavvar[medavvar]*self.reso),4)))

        for surfmedavvarmax in range(len(vectsurfmedavvarmax)):
            resultcoll.append(str(round(vectsurfmedavvarmax[surfmedavvarmax],4)))

        for volmedavvarmax in range(len(vectvolmedavvarmax)):
            resultcoll.append(str(round(vectvolmedavvarmax[volmedavvarmax],4)))

        print ("indpart worked")
        return resultcoll

        
    def o3dcalcul (self,plfile,resfold, resol):
        
        self.plyfile = plfile

        self.resultsfold = resfold
        self.reso = resol
        indheader = "no,size(surf),distance,\n"
        colorcloud = self.folder_3D + self.ofilename+"_color.ply"
        bigname = self.folder_3D + self.ofilename+"_largest.ply"
        outfile = self.resultsfold+self.ofilename+"_ind_parts_results.csv"
        
        resultcoll = []
        cloud = lib.ioply.ioplynow(self.plyfile).openplyfile()
        (labels,max_label,partcount,resultcoll) = self.fullpcl(cloud,self.reso,colorcloud)
        
        (bigcloud1,resultcoll,bestfit) = self.bigpcl(cloud,labels,max_label,resultcoll,bigname)
        
        resultcoll = self.pclfract(cloud,bigcloud1,labels,max_label,partcount,outfile,indheader,resultcoll)
        
        del cloud
        del colorcloud
        del bigcloud1
        

        return resultcoll, bestfit
    
    def remainsarray(self,indexno,factors,cloudarray):
        
        if indexno == 0:
            koerper3D =lib.extens.extens(factors,cloudarray).torusext()
        elif indexno == 1:
            koerper3D =lib.extens.extens(factors,cloudarray).ellipext()
        elif indexno == 2:
            koerper3D =lib.extens.extens(factors,cloudarray).paraext()
        elif indexno == 3:
            koerper3D =lib.extens.extens(factors,cloudarray).horcyext()
        elif indexno ==4:
            koerper3D =lib.extens.extens(factors,cloudarray).vertcylext()
        #elif indexno ==5:

        return koerper3D
    
    
    def o3dextcalc (self, selection, results_folder,folder_3D,resolution,resultscoll):
        
        indheader = "no,size(area),distance,type,\n"
        
        selindex = selection
        
        plyfile = self.folder_3D+self.ofilename+"_largest.ply"
        
        bigcloud = lib.ioply.ioplynow(plyfile).openplyfile()
        
        (correction,angles) = self.orientcalc(bigcloud)
        
        wolke = self.rotatecloud(bigcloud, correction)
        
        (self.center,self.bcoef) = lib.get_mean_center.center(wolke).centcalc()
        
        cloudarray = np.asarray(wolke.points)
        cashape = cloudarray.shape
        xsize = cashape[0]

        coefs = lib.bodygeofit.fitproc(self.folder_3D,self.ofilename,self.center).fitbody(wolke,selindex,self.bcoef)
        print ("fitted")

        factors = self.center,coefs

        extension = self.remainsarray(selindex,factors,cloudarray)
        fitname = folder_3D+self.ofilename+"_fit.ply"
        fittedbody = lib.ioply.ioplynow(fitname).openplyfile()

        extpc = geometry.PointCloud()
        extpc = lib.ioply.ioplynow("").fillpcd(extpc,extension)
        extfilename = folder_3D+self.ofilename+"_extensions.ply"
        lib.ioply.ioplynow(extfilename).saveply(extpc)
        labels = np.array(extpc.cluster_dbscan(eps=10, min_points=100, print_progress=False))
        max_label = 0
        partcount = 0
        outfile = self.resultsfold+self.ofilename+"_results.csv"
        if len(labels) != 0 : 
            max_label = labels.max()
            partcount = max_label + 1

        resultcoll = self.extfract(extpc,fittedbody,labels,max_label,partcount,outfile,indheader,resultscoll)
        resultcoll.append(str(round((resolution),4)))
        
        del bigcloud
        del wolke
        del cloudarray
        del extension
        del fittedbody
        del extpc

        return resultcoll,self.resheader
