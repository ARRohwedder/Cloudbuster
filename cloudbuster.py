#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 00:00:28 2020

@author: Dr. Arndt Rohwedder, University of Huddersfield
"""

import wx
import os
import open3d as o3d
import numpy as np

from skimage import io
from skimage import filters

import ratili
import skali
import positionen
import combiniere
import cloudgen
import o3dcalc
import saveply
import o3dext



class CbFrame(wx.Frame):    
    def __init__(self, parent, title):
        super(CbFrame, self).__init__(parent, title = title,size = (1000,900))
        self.InitUI()
        
    def InitUI(self):
        
        panel = wx.Panel(self)
        self.cbDir = os.getcwd()
        
        #linke Seite        
        vert_sizer1 = wx.BoxSizer(wx.VERTICAL)

        hor_sizer1a = wx.BoxSizer(wx.HORIZONTAL)
        hor_sizer2a = wx.BoxSizer(wx.HORIZONTAL)
        hor_sizer3a = wx.BoxSizer(wx.HORIZONTAL)
        hor_sizer4a = wx.BoxSizer(wx.HORIZONTAL)
        hor_sizer5a = wx.BoxSizer(wx.HORIZONTAL)
        hor_sizer6a = wx.BoxSizer(wx.HORIZONTAL)
        hor_sizer7a =  wx.BoxSizer(wx.HORIZONTAL)

        self.x_dim = wx.TextCtrl(panel, pos=(200,30))
        self.y_dim = wx.TextCtrl(panel, pos=(200,70))
        self.z_dim = wx.TextCtrl(panel, pos=(200,110))

        hinter = ['White', 'Black']
        choise = wx.ComboBox(panel, pos=(10, 210), size = (150,30), choices=hinter, style=wx.CB_READONLY)
    
        attention = wx.StaticText(panel, pos=(10, 10),label="Attention: Does not work with multichannel stacks!")        
        text1a = wx.StaticText(panel, pos=(10,30),label="X pixel dimensions")
        text2a = wx.StaticText(panel, pos=(10,70),label="Y pixel dimensions")
        text3a = wx.StaticText(panel, pos=(10,110),label="Z pixel dimensions")
        text4a = wx.StaticText(panel, pos=(10,180),label="Image Background")

        self.text1b = wx.StaticText(panel, pos=(500,10), label="")
        self.text2b = wx.StaticText(panel, pos=(500,82), label="")
        self.text3b = wx.StaticText(panel, pos=(500,154), label="")
        self.text4b = wx.StaticText(panel, pos=(500,226), label="")
        self.text5b = wx.StaticText(panel, pos=(500,298), label="")
        self.text6b = wx.StaticText(panel, pos=(500,370), label="")
        self.text7b = wx.StaticText(panel, pos=(500,442), label="")
        self.text8b = wx.StaticText(panel, pos=(500,514), label="")
        self.text9b = wx.StaticText(panel, pos=(500,586), label="")
        self.text10b = wx.StaticText(panel, pos=(500,658), label="")
        self.text11b = wx.StaticText(panel, pos=(500,678), label="")
        self.text12b = wx.StaticText(panel, pos=(500,698),label="")
        self.text13b = wx.StaticText(panel, pos=(500,718),label="")
        self.text14b = wx.StaticText(panel, pos=(500,738), label="")
        self.text15b = wx.StaticText(panel, pos=(500,758),label="")
        self.text16b = wx.StaticText(panel, pos=(500,778),label="")

        cdisp = wx.Button(panel, pos=(10,300), label = 'Display final cloud')

        my_btn = wx.Button(panel, pos=(10,250),label='Find a stack and start')

        self.bild1b = wx.StaticBitmap(panel, pos=(400,10), bitmap=wx.Bitmap(width=72,height=72))
        self.bild2b = wx.StaticBitmap(panel, pos=(400,82),bitmap=wx.Bitmap(width=72,height=72))
        self.bild3b = wx.StaticBitmap(panel, pos=(400,154),bitmap=wx.Bitmap(width=72,height=72))
        self.bild4b = wx.StaticBitmap(panel, pos=(400,226),bitmap=wx.Bitmap(width=72,height=72))
        self.bild5b = wx.StaticBitmap(panel, pos=(400,298),bitmap=wx.Bitmap(width=72,height=72))
        self.bild6b = wx.StaticBitmap(panel, pos=(400,370),bitmap=wx.Bitmap(width=72,height=72))
        self.bild7b = wx.StaticBitmap(panel, pos=(400,442),bitmap=wx.Bitmap(width=72,height=72))
        self.bild8b = wx.StaticBitmap(panel, pos=(400,514),bitmap=wx.Bitmap(width=72,height=72))
        self.bild9b = wx.StaticBitmap(panel, pos=(400,586),bitmap=wx.Bitmap(width=72,height=72))
        self.bild10b = wx.StaticBitmap(panel, pos=(400,658),bitmap=wx.Bitmap(width=72,height=72))

        #linke Seite
        hor_sizer1a.Add(attention, flag=wx.CENTER, border=10)
        vert_sizer1.Add((0, 10))
        vert_sizer1.Add(hor_sizer1a, proportion = 1,flag = wx.ALIGN_CENTRE)


        hor_sizer2a.Add(text1a, flag=wx.RIGHT, border=10)
        hor_sizer2a.Add(self.x_dim, proportion = 1) 
        vert_sizer1.Add((0, 20))
        vert_sizer1.Add(hor_sizer2a, proportion = 1,flag = wx.ALIGN_CENTRE)

        hor_sizer3a.Add(text2a, flag=wx.LEFT, border=10)
        hor_sizer3a.Add(self.y_dim, proportion = 1) 
        vert_sizer1.Add((0, 30))
        vert_sizer1.Add(hor_sizer3a, proportion = 1,flag = wx.ALIGN_CENTRE)

        hor_sizer4a.Add(text3a, flag=wx.RIGHT, border=10)
        hor_sizer4a.Add(self.z_dim, proportion = 1)        
        vert_sizer1.Add((0, 40))
        vert_sizer1.Add(hor_sizer4a, proportion = 1,flag = wx.ALIGN_CENTRE)

        choise.Bind(wx.EVT_COMBOBOX, self.OnSelect)
        hor_sizer7a.Add(text4a, flag=wx.RIGHT, border=10)
        hor_sizer7a.Add(choise, 0, wx.ALL | wx.LEFT, 5)
        vert_sizer1.Add((0, 50))
        vert_sizer1.Add(hor_sizer7a, proportion = 1,flag = wx.ALIGN_CENTRE)

        my_btn.Bind(wx.EVT_BUTTON, self.on_press)
        hor_sizer5a.Add(my_btn, 0, wx.ALL | wx.LEFT, 5)
        vert_sizer1.Add((0, 60))
        vert_sizer1.Add(hor_sizer5a, proportion = 1,flag = wx.ALIGN_CENTRE)

        cdisp.Bind(wx.EVT_BUTTON,self.on_Checked)
        hor_sizer6a.Add(cdisp, 0, wx.ALL | wx.LEFT, 5)
        vert_sizer1.Add((0, 70))
        vert_sizer1.Add(hor_sizer6a, proportion = 1,flag = wx.ALIGN_CENTRE)

        self.Show()


    def OnSelect(self, ev):
        bg = ev.GetString()
        if bg == 'Black':
            self.hinter = 0.0
        else:
            self.hinter = 1.0

    def OnQuit(self, e):
        self.Close()


    def on_press(self, event):
        mittel = os.path.sep
        icondir = self.cbDir+mittel+"icons"+mittel
        self.filename = wx.FileSelector("Choose a file to open")
        
        getrennt = self.filename.split(mittel)
        zwischen = getrennt[len(getrennt)-1]
        zwischen2 = zwischen.split(".")
        isofile = zwischen2[0]
        
        addimfolder1 = self.filename.replace(zwischen,"results")
        addimfolder = addimfolder1+mittel
        
        extfolder1 = self.filename.replace(zwischen,"3D_files")
        extfolder = extfolder1+mittel
        
        imfolder1 = self.filename.replace(zwischen,"")
        imfolder = imfolder1+mittel
        
        
        self.bild1b.SetBitmap(wx.Bitmap(icondir+'schwarz.png'))
        self.bild2b.SetBitmap(wx.Bitmap(icondir+'schwarz.png'))
        self.bild3b.SetBitmap(wx.Bitmap(icondir+'schwarz.png'))
        self.bild4b.SetBitmap(wx.Bitmap(icondir+'schwarz.png'))
        self.bild5b.SetBitmap(wx.Bitmap(icondir+'schwarz.png'))
        self.bild6b.SetBitmap(wx.Bitmap(icondir+'schwarz.png'))
        self.bild7b.SetBitmap(wx.Bitmap(icondir+'schwarz.png'))
        self.bild8b.SetBitmap(wx.Bitmap(icondir+'schwarz.png'))
        self.bild9b.SetBitmap(wx.Bitmap(icondir+'schwarz.png'))
        self.bild10b.SetBitmap(wx.Bitmap(icondir+'schwarz.png'))
        self.Update()
        try:
            im = io.imread(self.filename)

        except:
            self.text1b.SetLabel("file type could not be identified")
            self.bild1b.SetBitmap(wx.Bitmap(icondir+'error.png'))

        else:

            xpixdim = float(self.x_dim.GetValue())
            ypixdim = float(self.y_dim.GetValue())
            zpixdim = float(self.z_dim.GetValue())
            
            imforrat = 750/im.shape[1]
            
            resolution = float(xpixdim)/float(imforrat)
           
            if (os.path.exists(addimfolder))==False:
                os.mkdir(addimfolder)
                
            if (os.path.exists(extfolder))==False:
                os.mkdir(extfolder)
            
            self.bild1b.SetBitmap(wx.Bitmap(icondir+'load.png'))
            loadinfo = "Loaded: \n"+str(isofile)
            self.text1b.SetLabel(loadinfo)
            self.Update()
            print ("loaded")
            #------------------------------------------
            # ratio calculation
            ratiomix = ratili.ratios(im,xpixdim,ypixdim,zpixdim)
            transfer = ratiomix.imratio()
            self.bild2b.SetBitmap(wx.Bitmap(icondir+'ratio.png'))
            self.text2b.SetLabel("Ratio between dimensions calculated")
            self.Update()
            print ("ratio")
            #------------------------------------------
            # scaling of dimensions
            scales = skali.scale(im,transfer[2],transfer[1],transfer[0],self.hinter)
            finalscale = scales.sortscale()
            self.bild3b.SetBitmap(wx.Bitmap(icondir+'scale.png'))
            self.text3b.SetLabel("Stack scaled to 1x1x1 ratio.")
            self.Update()
            print ("scaled")
            del im
            #------------------------------------------
            # thresholding
            thresh = filters.threshold_li(finalscale)
            binary = finalscale > thresh
            self.bild4b.SetBitmap(wx.Bitmap(icondir+'thresh.png'))
            self.text4b.SetLabel("Stack made binary.")
            self.Update()
            print ("thresholded")
            del finalscale
            #------------------------------------------
            # combine and rotate image
            a = np.empty(3, dtype=object)
            a[0] = binary
            a[1] = np.transpose(a[0], (1, 0, 2))
            a[2] = np.transpose(a[0], (1, 2, 0))
            self.bild5b.SetBitmap(wx.Bitmap(icondir+'rotate.png'))
            self.text5b.SetLabel("Stack rotated to XZY and ZXY to improve outline.")
            self.Update()
            print ("rotated")
            #------------------------------------------
            # find edges in original
            bilder = positionen.positionen(a)
            kanten = bilder.combined()
            del a
            self.bild6b.SetBitmap(wx.Bitmap(icondir+'edges.png'))
            self.text6b.SetLabel("Edges identified in all orientations.")
            self.Update()
            print ("edges found")
            #------------------------------------------
            # extract 3D edges coordinates from original
            kantstack = cloudgen.wolken(kanten)
            wolkenstack = kantstack.combined()
            del kantstack
            self.bild7b.SetBitmap(wx.Bitmap(icondir+'edgepoint.png'))
            self.text7b.SetLabel("Point clouds extracted from all edges in all orientations.")
            self.Update()
            print ("edges to points")
            #------------------------------------------
            # Combine clouds
            ordnung = [[0,2,1],[1,2,0]]
            result = combiniere.combiner(wolkenstack,ordnung)
            originalwolke = result.addingup()
            del wolkenstack
            self.bild8b.SetBitmap(wx.Bitmap(icondir+'cloud.png'))
            self.text8b.SetLabel("All point clouds combined.")
            self.Update()
            print ("combined")
            #------------------------------------------
            # Clean cloud
            sauber = np.unique(originalwolke,axis=0)
            del originalwolke            
            #------------------------------------------
            # Save cloud as PLY
            plyfile = imfolder+isofile+".ply"
            saveit = saveply.saveply(plyfile, sauber)
            saveit.saveplynow()
            del sauber
            self.bild9b.SetBitmap(wx.Bitmap(icondir+'reducecloud.png'))
            rawcloud = "Combined point cloud cleaned and saved as ply file: \n"+plyfile
            self.text9b.SetLabel(rawcloud)
            self.Update()
            print ("cleaned")
            #------------------------------------------
            #o3d data
            calc3d = o3dcalc.o3dcalc(plyfile, isofile, imfolder, addimfolder, extfolder, resolution)
            o3dresults = calc3d.o3dcalcul()
            partsresvalues = o3dresults[1]
            resheaders = o3dresults[2]
            print ("parts calculated")
            #------------------------------------------                      
            # o3dext calclulation
            extdata = o3dext.o3dext(o3dresults[0],isofile,imfolder,addimfolder, extfolder, resolution)
            extensions = extdata.o3dextcalc()
            extres = extensions[0]
            extheader = extensions[1]
            print ("extensions calculated")
            #------------------------------------------                      
            # save results
            
            bothheaders = np.append(resheaders,extheader, axis=0)
            bothentries = np.append(partsresvalues,extres, axis=0)
            
            header = ','.join(bothheaders)+"\n"
            tabentry = ','.join(bothentries)+"\n"
            savefile = addimfolder+isofile+"_Final_Results.csv"
            pcfile = open( savefile , "w" )
            pcfile.writelines(header)
            pcfile.writelines(tabentry)
            pcfile.close()
            #------------------------------------------                      
            # present results
            res1 = "Extension of entire cloud:  X = "+partsresvalues[0]+" Y = "+partsresvalues[1]+" Z = "+partsresvalues[2]
            res2 = "Extension of central spheroid:  X = "+partsresvalues[8]+" Y = "+partsresvalues[9]+" Z = "+partsresvalues[10]
            res3 = "Hint: "+partsresvalues[14]
            res4 = "Number of separated parts = "+partsresvalues[7]
            res5 = "Dist. from spheroid: Average = "+partsresvalues[16]+", Median = "+partsresvalues[15]+", Variance = "+partsresvalues[17]
            res6 = "Dist. from spheroid: Maximum = "+partsresvalues[18]
            
            collres = res1 + "\n" + res2 + "\n" + res3 + "\n" + res4 + "\n" + res5 + "\n" + res6
            
            finaltext = "Key feature calculated and saved in file: \n"+isofile+"_Final_Results.csv"
            self.bild10b.SetBitmap(wx.Bitmap(icondir+'measure.png'))            
            self.Update()
            self.text10b.SetLabel(finaltext)
            wx.MessageBox(collres,"Selected Results" ,wx.OK | wx.ICON_INFORMATION)
            self.endcloud = extfolder+isofile+"_color.ply"
            self.endball = extfolder+isofile+"_ellipsoid.ply"
            self.icondirs = icondir

    def on_Checked(self, cbev):

        try:
            wolke =o3d.io.read_point_cloud(self.endcloud)
            ballm = o3d.io.read_point_cloud(self.endball)
        except:
            self.text1b.SetLabel("Cloud not yet generated.")
            self.bild1b.SetBitmap(wx.Bitmap(self.icondirs+'error.png'))
        else:            
            wolke.paint_uniform_color([0.0, 0.0, 0.5])
            ballm.paint_uniform_color([0.0,0.5,0.0])
            o3d.visualization.draw_geometries([wolke, ballm],window_name='Spheroid',width=750,height=750)

ex = wx.App() 
CbFrame(None,'Cloudbuster') 
ex.MainLoop()
