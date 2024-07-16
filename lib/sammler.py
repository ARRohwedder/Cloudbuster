#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 20:13:40 2021

@author: Dr. Arndt Rohwedder, University of Huddersfield
"""
import os

class sammler:

    def __init__(self,dire):
        self.dirname = dire

    def collect (self):
        #fileheader = 'Sample,PCL_max_x_size,PCL_max_y_size,PCL_ratio_YX_size,PCL_ratio_YZ_size,PCL_ratio_XZ_size,PCL_shape_hint,Sep_Comp_Count,Spheroid_rotation_X,Spheroid_rotation_Y,Spheroid_rotation_Z,Spheroid_max_x_size,Spheroid_max_y_size,Spheroid_ratio_YX_size,Spheroid_ratio_YZ_size,Spheroid_ratio_XZ_size,Spheroid_surface_area,Spheroid_Volume,Spheroid_shape_hint,Med_Dist_Sph_to_Frag,Av_Dist_Sph_to_Frag,Var_Dist_Sph_to_Frag,Max_Dist_Sph_to_Frag,Med_Surf_of_Frag,Av_Surf_of_Frag,Var_Surf_of_Frag,Max_Surf_of_Frag,Med_Vol_of_Frag,Av_Vol_of_Frag,Var_Vol_of_Frag,Max_Vol_of_Frag,PixResol,Ext_Count,Brim,Broad,Narrow,Small,Ext_Max_length,Ext_Av_Max_length,Ext_Av_length,Ext_Surface_sum,Ext_Max_Surface,Ext_Av_Surface,Ext_Av_Med_length,Ext_Av_Var_length\n'
        outfile = "acc_results.csv"
        #findelem = 'Final_Results.csv'
        findelem = 'final_results.csv'
        mittel = os.path.sep
        outfile = self.dirname+mittel+outfile
        resfile = open(outfile , "w" )
        listOfFiles = list()
        counter = 0
        for (dirpath, dirnames, filenames) in os.walk(self.dirname):
            listOfFiles += [os.path.join(dirpath, file) for file in filenames]
        for elem in listOfFiles:
            if elem.find(findelem) > 0:
                #print (elem)
                csvfile = open(elem,'r')
                if counter < 1:
                    headerzeile = 'File,'+csvfile.readline()
                    #print (headerzeile)
                    resfile.writelines(headerzeile)
                    csvzeilen = csvfile.readline()
                if counter >= 1:

                    csvzeilen = csvfile.readline()
                    csvzeilen = csvfile.readline()

                getrennt = elem.split(mittel)
                zwischen = getrennt[len(getrennt)-1]
                zwischen2 = zwischen.split(".")
                isofile = zwischen2[0]

                entry = isofile+','+csvzeilen
                resfile.writelines(entry)
                csvfile.close()
                counter +=1
        resfile.close()

        return ('Finished ')
