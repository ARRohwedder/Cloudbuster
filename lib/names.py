# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 16:29:44 2023

@author: AK126086
"""

class nameprep:

    def __init__(self,sep,file):
        self.mittel = sep
        self.fullpath = file

    def splitter (self):
        getrenntarr = self.fullpath.split(self.mittel)
        fullname = getrenntarr[len(getrenntarr)-1]
        filename = fullname.split(".")[0]

        return fullname,filename

    def foldprep (self,fname):
        self.fullname = fname
        results_folder = self.fullpath.replace(self.fullname,"results")+self.mittel
        folder_3D = self.fullpath.replace(self.fullname,"3D_files")+self.mittel
        basefolder = self.fullpath.replace(self.fullname,"")

        return results_folder, folder_3D, basefolder


