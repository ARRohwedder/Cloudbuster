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
import volumeandsurface
import orientation


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
        resheader = ("PCL_max_x_size","PCL_max_y_size","PCL_ratio_YX_size","PCL_ratio_YZ_size","PCL_ratio_XZ_size","PCL_shape_hint","Sep_Comp_Count","Spheroid_rotation_X","Spheroid_rotation_Y","Spheroid_rotation_Z","Spheroid_max_x_size","Spheroid_max_y_size","Spheroid_ratio_YX_size","Spheroid_ratio_YZ_size","Spheroid_ratio_XZ_size","Spheroid_surface_area","Spheroid_Volume","Spheroid_shape_hint","Med_Dist_Sph_to_Frag","Av_Dist_Sph_to_Frag","Var_Dist_Sph_to_Frag","Max_Dist_Sph_to_Frag","Med_Surf_of_Frag","Av_Surf_of_Frag","Var_Surf_of_Frag","Max_Surf_of_Frag","Med_Vol_of_Frag","Av_Vol_of_Frag","Var_Vol_of_Frag","Max_Vol_of_Frag","PixResol")
        #                  0              1                   2                 3                   4                  5                 6                    7                       8                    9                    10                      11                 12                       13                           14                     15                      16                17                  18                          19                  20                 21                        22                23               24                  25                26                27                  28            29              30      
        indheader = "no,size(surf),distance,\n"
        resultcoll = []
        cloud = io.read_point_cloud(self.plyfile)
        wolkenform = cloud.get_max_bound()
        #print ("o3dcalc 1")
        volasurf = volumeandsurface.surfandvol(cloud,self.reso)
        (surface,volume) = volasurf.surfvolcalc()
        
        #isolate compartments and find largest 30.05.2021
        #labels = np.array(cloud.cluster_dbscan(eps=10, min_points=10, print_progress=False))
        labels = np.array(cloud.cluster_dbscan(eps=2*self.reso, min_points=10, print_progress=False))
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
        box = bigcloud1.get_oriented_bounding_box()
        boxpunkte = np.asarray(box.get_box_points())
        ori = orientation.orient(boxpunkte)
        (correction,angles) = ori.get_orientation()
        
        #calc cloudcenter distances 30.05.2021
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
            outfile = self.resultsfold+self.ofilenames+"_ind_parts_results.csv"
            resfile = open( outfile , "w" )
            resfile.writelines(indheader)
            for gross in list(range(max_label + 1)):
                results2 = np.where(labels == gross)
                resultlist2 = list(results2[0])
                testcloud = cloud.select_by_index(resultlist2)
                distance =  bigcloud1.compute_point_cloud_distance(testcloud)
                distancearray = np.asarray(distance)
                indvolasurf = volumeandsurface.surfandvol(testcloud,self.reso)
                
                (indsurf,indvol) = indvolasurf.surfvolcalc()
                surfarray = np.asarray(indsurf)
                volarray = np.asarray(indvol)
                
                
                size = indsurf
                if (distancearray.mean()) > 1:
                    distvectors.append(distancearray.mean())
                    surfacevectors.append(surfarray.mean())
                    volumevectors.append(volarray.mean())

                line = str(gross)+","+str(size)+","+str(np.average(distancearray))+"\n"
                resfile.writelines(line)
            resfile.close()
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
        resultcoll.append(str(angles[0]))
        resultcoll.append(str(angles[1]))
        resultcoll.append(str(angles[2]))
        resultcoll.append(str(round((bigform[0]*self.reso),4)))
        resultcoll.append(str(round((bigform[1]*self.reso),4)))
        #resultcoll.append(str(round((bigform[2]*self.reso),4)))
        resultcoll.append(str(round((bigform[1]/bigform[0]),4)))
        resultcoll.append(str(round((bigform[1]/bigform[2]),4)))
        resultcoll.append(str(round((bigform[0]/bigform[2]),4)))
        resultcoll.append(str(round(surface,4)))
        resultcoll.append(str(round(volume,4)))
        
        if ((bigform[0]/bigform[1])< 0.9) or ((bigform[0]/bigform[1])> 1.1):
            interpret = "Spheroid elongated"
        else:
            interpret = "Spheroid round"

        resultcoll.append(interpret)
        resultcoll.append(str(round((vectmedavvar[0]*self.reso),4)))
        resultcoll.append(str(round((vectmedavvar[1]*self.reso),4)))
        resultcoll.append(str(round((vectmedavvar[2]*self.reso),4)))
        resultcoll.append(str(round((vectmedavvar[3]*self.reso),4)))
        
        resultcoll.append(str(round(vectsurfmedavvarmax[0],4)))
        resultcoll.append(str(round(vectsurfmedavvarmax[1],4)))
        resultcoll.append(str(round(vectsurfmedavvarmax[2],4)))
        resultcoll.append(str(round(vectsurfmedavvarmax[3],4)))
        
        resultcoll.append(str(round(vectvolmedavvarmax[0],4)))
        resultcoll.append(str(round(vectvolmedavvarmax[1],4)))
        resultcoll.append(str(round(vectvolmedavvarmax[2],4)))
        resultcoll.append(str(round(vectvolmedavvarmax[3],4)))

        
        resultcoll.append(str(round((self.reso),4)))

        return bigcloud1, resultcoll, resheader
