#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 10:25:10 2020

@author: Dr. Arndt Rohwedder, University of Huddersfield
"""

import os
import shutil
import subprocess

class cccalc:
    
    def __init__(self,ocloud,filenames,basefolder,folder,isoparam):
        self.cloud = ocloud
        self.foldertarget = folder
        self.imagefolder = basefolder
        self.ofilenames = filenames
        self.param = isoparam
        
    def ccalcul (self):
        partcount = 0
        resfile = self.foldertarget+self.ofilenames+"_CC_Results.txt"
        
        try:
            cccomand = "CloudCompare -SILENT -o " + self.cloud+" -LOG_FILE "+resfile+" -C_EXPORT_FMT PLY -EXTRACT_CC "+self.param #-AUTO_SAVE OFF 
            subprocess.run(cccomand, shell=True, check=True)
        except:
            cccomand = "cloudcompare.CloudCompare -SILENT -o " + self.cloud+" -LOG_FILE "+resfile+" -C_EXPORT_FMT PLY -EXTRACT_CC "+self.param #-AUTO_SAVE OFF 
            subprocess.run(cccomand, shell=True, check=True)
        
        try:
            logfile = open(resfile,'r')
        except:
            partcount = 0
            return partcount

        logzeilen = logfile.readlines()
        
        einzelzeile = ""
        teile = []
        for wowert in list(range(len(logzeilen))):
            einzelzeile = logzeilen[wowert]
            if einzelzeile.find('component(s) were created') > 0:
                teile = einzelzeile.split(' ')
                print ("parts------------------------------->"+str(teile[1]))
                partcount=str(teile[1])

        if int(partcount) < 1:
            partcount = 1
            
        print ("partcount ------------------------->"+str(partcount))
        for wowert in list(range(len(logzeilen))):
            einzelzeile = logzeilen[wowert]
            if einzelzeile.find('No component was created!') > 0:
                fromfile= self.imagefolder+self.ofilenames+".ply"
                tofile = self.imagefolder+self.ofilenames+"_COMPONENT_1.ply"
                shutil.copyfile(fromfile, tofile)
        

        anzahl = int(partcount)
        biggest = 0
        bigfind = 0
        for bigfile in range(1,anzahl+1):
            filename= self.imagefolder+self.ofilenames+"_COMPONENT_"+str(bigfile)+".ply"
            file_size = os.stat(filename)
            if file_size.st_size > biggest:
                biggest = file_size.st_size
                bigfind = bigfile

        if bigfind < 1:
            bigfind = 1
        
        
        fromfile= self.imagefolder+self.ofilenames+"_COMPONENT_"+str(bigfind)+".ply"
        tofile = self.foldertarget+self.ofilenames+"_COMPONENT_1.ply"
        shutil.copyfile(fromfile, tofile)
        
        for shiftfile in range(1,anzahl+1):
            filename= self.imagefolder+self.ofilenames+"_COMPONENT_"+str(shiftfile)+".ply"
            if shiftfile< bigfind:
                targetfile = self.foldertarget+self.ofilenames+"_COMPONENT_"+str(shiftfile+1)+".ply"
                shutil.copyfile(filename, targetfile)
            if shiftfile> bigfind:
                targetfile = self.foldertarget+self.ofilenames+"_COMPONENT_"+str(shiftfile)+".ply"
                shutil.copyfile(filename, targetfile)
                
        for delfile in range(1,anzahl+1):
            filename= self.imagefolder+self.ofilenames+"_COMPONENT_"+str(delfile)+".ply"
            os.remove(filename)

        return partcount
