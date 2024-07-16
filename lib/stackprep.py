# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 11:23:29 2022

@author: Dr. Arndt Rohwedder, Johannes Keppler University, Linz
"""

import numpy as np

from skimage import io
from skimage import transform
from skimage.draw import rectangle_perimeter
from skimage import filters
from skimage import feature


class imprep:

    def openfile (self,fname):
        self.file = fname
        print (fname)
        xvalue = 0
        yvalue = 0
        zvalue = 0
        zhelp = ""
        xstrarray = []
        ystrarray = []
        zstrarray = []
        try:
            print ("startet hier")
            im = io.imread(self.file)
            
            import tifffile
            with tifffile.TiffFile(self.file) as tif:
                tif_tags = {}
                for tag in tif.pages[0].tags.values():
                    name, value = tag.name, tag.value

                    if "spacing" in str(value):
                        zhelp = str(value)
                        zstrarray = zhelp.split("\n")
                        for i in range(len(zstrarray)):
                            if "spacing" in zstrarray[i]:
                                zvalue = zstrarray[i].split("=")[1]

                    if "XResolution" in name:
                        xstrarray = list(value)
                        xvalue = xstrarray[1]/xstrarray[0]

                    if "YResolution" in name:
                        ystrarray = list(value)
                        yvalue = ystrarray[1]/ystrarray[0]

        except:
            fehler = "-1"
            return fehler
        else:
            fehler = "0"
            return im,fehler,xvalue,yvalue,zvalue
        
    def imratio (self,im,x,y,z):
        self.image = im
        self.xdim = x
        self.ydim = y
        self.zdim = z

        largest = 0
        ratio = 0
        zxratio = 0
        dimensions = []
        largest = np.max(self.image.shape)
        ratio = 750/largest
        zxratio = self.zdim/self.xdim
        dimensions.append(zxratio*ratio)
        dimensions.append(ratio)
        dimensions.append(ratio)
        
        return dimensions
    
    def sortscale (self,im,x,y,z,hinter):
        
        self.image = im
        self.xdim = x
        self.ydim = y
        self.zdim = z
        self.backg = hinter

        imscale = []
        bild = []
        bild2 = []
        bild2 = transform.rescale(self.image, (self.zdim,self.ydim,self.xdim),mode="edge",preserve_range=False)
        start = (1, 1)

        for slide in range(bild2.shape[0]-1):
            einzelbild = bild2[slide]
            endx = (einzelbild.shape[0])-2
            endy = (einzelbild.shape[1])-2
            end = (endx, endy)
            rr, cc = rectangle_perimeter(start, end, shape=einzelbild.shape)
            einzelbild[rr, cc] = self.backg
            bild2[slide] = einzelbild
        bild = np.full((1,bild2.shape[1], bild2.shape[2]), self.backg)
        imscale = np.concatenate([bild,bild2,bild])
        return imscale
    
    def threshold (self,im):
        self.finalscale = im
        thresh = filters.threshold_li(self.finalscale)
        binary = self.finalscale > thresh
        return binary
    
    def rotate (self,im):
        self.binary = im
        a = np.empty(3, dtype=object)
        a[0] = self.binary
        a[1] = np.transpose(a[0], (1, 0, 2))
        a[2] = np.transpose(a[0], (1, 2, 0))
        return a
    
    def positions (self,im):
        self.imstack = im
        edgestack = np.empty(3, dtype=object)
        bild = 0
        for bild in list(range(self.imstack.shape[0])):
            edges = []
            result = []
            positions = []
            poscollect = []
            zwert = 0
            image = self.imstack[bild]
            for zwert in list(range(image.shape[0])):
                edges = feature.canny(image[zwert])
                result = np.where(edges == True)
                positions = np.asarray(list(zip(result[0], result[1])))
                poscollect.append(positions)
            edgestack[bild] = poscollect
        return edgestack
    
    
        
    