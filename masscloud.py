#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 12:17:54 2020

@author: Dr. Arndt Rohwedder, University of Huddersfield
"""
import wx 
import os
import numpy as np
from skimage import io
from skimage import filters

import ratili
import skali
import positionen
import cloudgen
import combiniere
import o3dcalc
import saveply
import o3dext


class Masswin(wx.Frame): 
            
   def __init__(self, parent, title): 
      super(Masswin, self).__init__(parent, title = title,size = (300,200))  
      self.InitUI() 
         
   def InitUI(self):    
      self.count = 0 
      pnl = wx.Panel(self) 
      vbox = wx.BoxSizer(wx.VERTICAL)
		
      hbox1 = wx.BoxSizer(wx.HORIZONTAL) 
      hbox2 = wx.BoxSizer(wx.HORIZONTAL)
    
      self.gauge = wx.Gauge(pnl, range = 100, size = (250, 25), style =  wx.GA_HORIZONTAL) 
      self.btn1 = wx.Button(pnl, label = "Load script file") 
      
      self.Bind(wx.EVT_BUTTON, self.OnStart, self.btn1) 
		
      hbox1.Add(self.gauge, proportion = 1, flag = wx.ALIGN_CENTRE) 
      hbox2.Add(self.btn1, proportion = 1, flag = wx.RIGHT, border = 10) 
         
      vbox.Add((0, 30)) 
      vbox.Add(hbox1, flag = wx.ALIGN_CENTRE) 
      vbox.Add((0, 20)) 
      vbox.Add(hbox2, proportion = 1, flag = wx.ALIGN_CENTRE) 
      pnl.SetSizer(vbox) 
         
      self.SetSize((300, 200)) 
      self.Centre() 
      self.Show(True)   
		
   def OnStart(self, e): 
      mittel = os.path.sep
      self.btn1.SetLabel("Processing...")
      self.filename = wx.FileSelector("Choose a file to open")
      getrennt = self.filename.split(mittel)
      zwischen = getrennt[len(getrennt)-1]
      basefolder = self.filename.replace(zwischen,"")      
      scriptfile = open(self.filename,'r')
      scriptzeilen = scriptfile.readlines()
      amount = len(scriptzeilen)
      adding = 100/amount
      lineparts = []
      imnamemix = []
      
      for single in list(range(len(scriptzeilen)-1)):
          lineparts = scriptzeilen[single].split(',')
          self.imname = lineparts[0]
          imnamemix = self.imname.split('.')
          imfolderinter = imnamemix[0]
          imfolder = basefolder + imfolderinter + mittel
          addimfolder = imfolder + "results" + mittel
          extfolder = imfolder + "3D_files" + mittel
          if (os.path.exists(imfolder))==False:
              os.mkdir(imfolder)
          if (os.path.exists(addimfolder))==False:
              os.mkdir(addimfolder)
          if (os.path.exists(extfolder))==False:
              os.mkdir(extfolder)
          im = io.imread(basefolder+mittel+self.imname)
          xpixdim = float(lineparts[1])
          ypixdim = float(lineparts[2])
          zpixdim = float(lineparts[3])
          hinter = float(lineparts[4])
          imforrat = 750/im.shape[1]
          resolution = float(xpixdim)/float(imforrat)
          #------------------------------------------
          # ratio calculation
          ratiomix = ratili.ratios(im,xpixdim,ypixdim,zpixdim)
          transfer = ratiomix.imratio()
          #------------------------------------------
          # scaling of dimensions
          scales = skali.scale(im,transfer[2],transfer[1],transfer[0],hinter)
          finalscale = scales.sortscale()
          del im
          #------------------------------------------
          # thresholding
          thresh = filters.threshold_li(finalscale)
          binary = finalscale > thresh
          del finalscale
          #------------------------------------------
          # combine and rotate image
          a = np.empty(3, dtype=object)
          a[0] = binary
          a[1] = np.transpose(a[0], (1, 0, 2))
          a[2] = np.transpose(a[0], (1, 2, 0))
          #------------------------------------------
          # find edges in original
          bilder = positionen.positionen(a)
          kanten = bilder.combined()
          del a
          #------------------------------------------
          # extract 3D edges coordinates from original
          kantstack = cloudgen.wolken(kanten)
          wolkenstack = kantstack.combined()
          del kantstack
          #------------------------------------------
          # Combine clouds
          ordnung = [[0,2,1],[1,2,0]]
          result = combiniere.combiner(wolkenstack,ordnung)
          originalwolke = result.addingup()
          del wolkenstack
          #------------------------------------------
          # Clean cloud
          sauber = np.unique(originalwolke,axis=0)
          del originalwolke
          #------------------------------------------
          # Save cloud as PLY
          plyfile = imfolder+imfolderinter+".ply"
          saveit = saveply.saveply(plyfile, sauber)
          saveit.saveplynow()
          del sauber

          #------------------------------------------
          #o3d data
          calc3d = o3dcalc.o3dcalc(plyfile, imfolderinter, imfolder, addimfolder, extfolder, resolution)
          o3dresults = calc3d.o3dcalcul()
          partsresvalues = o3dresults[1]
          resheaders = o3dresults[2]

          #------------------------------------------
          # o3dext calclulation

          extdata = o3dext.o3dext(o3dresults[0],imfolderinter,imfolder,addimfolder, extfolder, resolution)
          extensions = extdata.o3dextcalc()
          extres = extensions[0]
          extheader = extensions[1]
          #------------------------------------------
          # save results
          
          bothheaders = np.append(resheaders,extheader, axis=0)
          bothentries = np.append(partsresvalues,extres, axis=0)
          
          header = ','.join(bothheaders)+"\n"
          
          tabentry = ','.join(bothentries)+"\n"
          

          savefile = addimfolder+imfolderinter+"_Final_Results.csv"
          pcfile = open( savefile , "w" )
          pcfile.writelines(header)
          pcfile.writelines(tabentry)
          pcfile.close()
        
          self.count = self.count + adding
          self.gauge.SetValue(int(self.count))
          wx.Yield()
      wx.MessageBox("Process finished","MassCloud" ,wx.OK | wx.ICON_INFORMATION)
      self.Close()
				
ex = wx.App() 
Masswin(None,'Cloudburst') 
ex.MainLoop()