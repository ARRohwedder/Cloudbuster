#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 20:50:34 2020

@author: Dr. Arndt Rohwedder, University of Huddersfield
"""
from open3d import io
from open3d import utility
import matplotlib.pyplot as plt
import numpy as np


class o3dcalc:
    

    def __init__(self,plfile,filenames,basefolder,resfold,threedfolder, resol):
        self.plyfile = plfile
        self.imagefolder = basefolder
        self.ofilenames = filenames
        self.resultsfold = resfold
        self.cloudfold = threedfolder
        self.reso = resol
        
    def o3dcalcul (self):
        #resheader = ("AMaxX","AMaxY","AMaxZ","ARatYX","ARatYZ","ARatXZ","A_Hint","Sep_Comp","SpMaxX","SPMaxY","SPMaxZ","SPRatYX","SPRatYZ","SPRatXZ","Sp_Hint","MedCl_Dist","AvCl_Dist","VarCl_Dist","MaxCl_Dist","PixResol")
        resheader = ("AMaxX","AMaxY","ARatYX","ARatYZ","ARatXZ","A_Hint","Sep_Comp","SpMaxX","SPMaxY","SPRatYX","SPRatYZ","SPRatXZ","Sp_Hint","MedCl_Dist","AvCl_Dist","VarCl_Dist","MaxCl_Dist","PixResol")
        indheader = "no,size(surf),distance,\n"
        resultcoll = []
        cloud = io.read_point_cloud(self.plyfile)
        wolkenform = cloud.get_max_bound()
        
        #isolate compartments and find largest 30.05.2021
        labels = np.array(cloud.cluster_dbscan(eps=10, min_points=10, print_progress=False))
        max_label = labels.max()
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
        print (len(resultlist))
        bigone = cloud.select_by_index(resultlist)

        partcount = max_label + 1

        #large spheroid  30.05.2021
        if int(max_label  +1 ) < 2:
            bigcloud1 = cloud
            
        else:
            bigcloud1 =bigone
        bigform = bigcloud1.get_max_bound()
        colors = plt.get_cmap("tab20")(labels / (max_label if max_label > 0 else 1))
        colors[labels < 0] = 0
        cloud.colors = utility.Vector3dVector(colors[:, :3])
        colorcloud = self.cloudfold + self.ofilenames+"_color.ply"
        bigname = self.cloudfold + self.ofilenames+"_largest.ply"
        io.write_point_cloud(bigname, bigcloud1)
        io.write_point_cloud(colorcloud, cloud)
        
        #calc cloudcenter distances 30.05.2021
        distvectors =[]
        medvect = 0
        avvect = 0
        varvect = 0
        maxvect = 0
        
        if int(partcount) > 1:
            outfile = self.resultsfold+self.ofilenames+"_ind_parts_results.csv"
            resfile = open( outfile , "w" )
            resfile.writelines(indheader)
            for gross in list(range(max_label + 1)):
                results2 = np.where(labels == gross)
                resultlist2 = list(results2[0])
                lang = len(resultlist2)
                testcloud = cloud.select_by_index(resultlist2)
                distance =  bigcloud1.compute_point_cloud_distance(testcloud)
                distancearray = np.asarray(distance)
                
                
                size = lang*self.reso
                if (distancearray.mean()) > 1:
                    distvectors.append(distancearray.mean())
                line = str(gross)+","+str(size)+","+str(np.average(distancearray))+"\n"
                resfile.writelines(line)
            resfile.close()
            medvect = np.median(distvectors)
            avvect = np.average(distvectors)
            varvect = np.var(distvectors)
            maxvect = np.max(distvectors)

        vectmedavvar = [medvect,avvect,varvect,maxvect]
    
        resultcoll.append(str(round((wolkenform[0]*self.reso),4)))
        resultcoll.append(str(round((wolkenform[1]*self.reso),4)))
        #resultcoll.append(str(round((wolkenform[2]*self.reso),4)))
        resultcoll.append(str(round((wolkenform[1]/wolkenform[0]),4)))
        resultcoll.append(str(round((wolkenform[1]/wolkenform[2]),4)))
        resultcoll.append(str(round((wolkenform[0]/wolkenform[2]),4)))

        if ((wolkenform[0]/wolkenform[1])< 0.9) or ((wolkenform[0]/wolkenform[1])> 1.1):
            interpret = "Spread elongated or directed"
        else:
            interpret = "Spread round or even spread"

        resultcoll.append(interpret)
        resultcoll.append(str(partcount))
        resultcoll.append(str(round((bigform[0]*self.reso),4)))
        resultcoll.append(str(round((bigform[1]*self.reso),4)))
        #resultcoll.append(str(round((bigform[2]*self.reso),4)))
        resultcoll.append(str(round((bigform[1]/bigform[0]),4)))
        resultcoll.append(str(round((bigform[1]/bigform[2]),4)))
        resultcoll.append(str(round((bigform[0]/bigform[2]),4)))
        
        if ((bigform[0]/bigform[1])< 0.9) or ((bigform[0]/bigform[1])> 1.1):
            interpret = "Spheroid elongated"
        else:
            interpret = "Spheroid round"

        resultcoll.append(interpret)
        resultcoll.append(str(round((vectmedavvar[0]*self.reso),4)))
        resultcoll.append(str(round((vectmedavvar[1]*self.reso),4)))
        resultcoll.append(str(round((vectmedavvar[2]*self.reso),4)))
        resultcoll.append(str(round((vectmedavvar[3]*self.reso),4)))
        resultcoll.append(str(round((self.reso),4)))

        return bigcloud1, resultcoll, resheader
