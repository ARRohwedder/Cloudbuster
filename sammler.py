#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 20:13:40 2021

@author: Dr. Arndt Rohwedder, University of Huddersfield
"""
import os

class sammler:
    
    def __init__(self,kopf,resnam,finds,dire):
        self.fileheader = kopf
        self.outnam = resnam
        self.findelem = finds
        self.dirname = dire
        
    def collect (self):
        
        mittel = os.path.sep
        outfile = self.dirname+mittel+self.outnam
        resfile = open(outfile , "w" )
        listOfFiles = list()
        counter = 0
        for (dirpath, dirnames, filenames) in os.walk(self.dirname):
            listOfFiles += [os.path.join(dirpath, file) for file in filenames]
        for elem in listOfFiles:
            if elem.find(self.findelem) > 0:
                csvfile = open(elem,'r')
                if counter < 1:
                    headerzeile = 'File,'+csvfile.readline()
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
