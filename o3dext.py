#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 12:05:19 2021

@author: Dr. Arndt Rohwedder, University of Huddersfield
"""
from open3d import io
from open3d import geometry
from open3d import utility
import numpy as np
import extens
import ellipsave
import fitting
import pandas as pd

class o3dext:
    
    def __init__(self,bigwolke,filenames,folder,resfolder,threedfolder, resol):
        
        self.bigcloud1 = bigwolke
        self.ofilenames = filenames
        self.foldertarget = folder
        self.resultsfold = resfolder
        self.cloudfold = threedfolder
        self.reso = resol
        
    def o3dextcalc (self):
        
        extheader = ('ExNumber','Brim','Broad','Narrow','Small','Maxlength','AvMaxlength','Avlength','MaxSurface','AvSurface','AvMedlength','AvVarlength')
        types = ['Brim','Broad','Narrow','Small']
        #outfile = self.resultsfold+self.ofilenames+"_indExt_results.csv"

        #build ellipsoid and get factors
        bigcenter1 = self.bigcloud1.get_center()
        bigform = self.bigcloud1.get_max_bound()
        bigcloud = self.bigcloud1.uniform_down_sample(4)
        cloudarray = np.asarray(bigcloud.points)
        cashape = cloudarray.shape
        xsize = cashape[0]

        bigform2 = bigform

        bigform2[0] = bigform[0]*0.4
        bigform2[1] = bigform[1]*0.4
        bigform2[2] = bigform[2]*0.5

        fitsmarti = fitting.fitting(bigcloud,bigform2,bigcenter1)
        smartidata = fitsmarti.fiteli()
        makeeli = ellipsave.ellipsave(smartidata,xsize,cloudarray)
        ellipsoid = makeeli.ellipsoid_save()
        
        ellippc = geometry.PointCloud()
        ellippc.points = utility.Vector3dVector(ellipsoid)

        bigform = smartidata[1]
        downpcd = ellippc.voxel_down_sample(voxel_size=0.5)
        
        #build extensions
        makeextens = extens.extens(smartidata,cloudarray)
        extarray = makeextens.extensions()
        extpc = geometry.PointCloud()
        extpc.points = utility.Vector3dVector(extarray[0])

        #safe ball and extensions
        ballfilemesh = self.cloudfold+self.ofilenames+"_ellipsoid.ply"
        io.write_point_cloud(ballfilemesh, downpcd)
        extfilename = self.cloudfold+self.ofilenames+"_extensions.ply"
        io.write_point_cloud(extfilename, extpc)


        #isolate compartments and find distance 05.06.2021
        labels = np.array(extpc.cluster_dbscan(eps=10, min_points=10, print_progress=False))
        max_label = labels.max()
        partcount = max_label + 1
        
        elliparray = np.asarray(ellippc.points)
        elliparraysize = elliparray.shape[0]
        arealimit = elliparraysize*0.02
        
        ellipsize = ellippc.get_max_bound()
        lengthlimit = (ellipsize.max()/2)*0.15
        
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
        
        if int(partcount) >= 1:
            for gross in list(range(max_label + 1)):
                results2 = np.where(labels == gross)
                resultlist2 = list(results2[0])
                testcloud = extpc.select_by_index(resultlist2)
                distance =  testcloud.compute_point_cloud_distance(downpcd)
                distancearray = np.asarray(distance)
                
                size = len(resultlist2)
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
                
                sizevect.append(size*self.reso)
                maxvect.append(maxdist*self.reso)
                avvect.append(avdist*self.reso)
                medvect.append(mddist*self.reso)
                varvect.append(vardist*self.reso)
                maxdistarray.append(maxdistextension*self.reso)
                typearray.append(classification)
           
        
        if int(partcount) < 1:
            
            size = 0
            maxdistextension = 0
            avdist = 0
            mddist = 0
            vardist = 0
            classification = 0
            
            sizevect.append(size*self.reso)
            maxdistarray.append(maxdistextension*self.reso)
            avvect.append(avdist*self.reso)
            medvect.append(mddist*self.reso)
            varvect.append(vardist*self.reso)
            typearray.append(classification)
        
        
        extpddataframe = pd.DataFrame({'Size': sizevect,'Maxlength': maxdistarray, 'Avlength' : avvect, 'Medlength':medvect,'Varlength': varvect,'Type': typearray}, columns=['Size','Maxlength','Avlength','Medlength', 'Varlength','Type'])
        #extpddataframe.to_csv(outfile)
        
        output1 = np.array(extpddataframe['Type'].value_counts().index)
        output2 = extpddataframe['Type'].value_counts().values
        
        if np.isin('Brim',output1) == True:
            brimcount = np.where(output1 == 'Brim')
            brim = output2[brimcount[0][0]]
        if np.isin('Narrow',output1) == True:
            narrowcount = np.where(output1 == 'Narrow')
            narrow = output2[narrowcount[0][0]]
        if np.isin('Broad',output1) == True:
            broadcount = np.where(output1 == 'Broad')
            broad = output2[broadcount[0][0]]
        if np.isin('Small',output1) == True:
            smallcount = np.where(output1 == 'Small')
            small = output2[smallcount[0][0]]
        
        vectmedavvar = [str(partcount),str(brim),str(broad),str(narrow),str(small),str(np.max(maxdistarray)),str(np.average(maxdistarray)),str(np.average(avvect)),str(np.max(sizevect)),str(np.average(size)),str(np.average(medvect)),str(np.average(varvect))]

        return vectmedavvar,extheader
