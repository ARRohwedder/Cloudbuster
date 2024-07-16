#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 18:10:53 2022

@author: Dr. Arndt Rohwedder, Johannes Keppler University, Linz
"""

import wx
import os
import gc
import locale
import multiprocessing as mp

import lib.stackprep
import lib.cloudprep
import lib.o3dproc
import lib.ioply
import lib.names


locale.setlocale(locale.LC_ALL,'C')

class MassFrame(wx.Frame):
    
    def __init__(self, title, parent=None):
        wx.Frame.__init__(self, parent=parent, title=title,size = (300,200))
        self.initUI()
        
    #def InitLocale(self):
        #self.ResetLocale()

        
    def initUI(self):
        panel = wx.Panel(self)
        self.count = 0 
        self.gauge = wx.Gauge(panel, range = 100,pos=(10,50), size = (250, 25), style =  wx.GA_HORIZONTAL) 
        self.btn1 = wx.Button(panel, pos=(10, 10), label = "Load script file") 
        self.Bind(wx.EVT_BUTTON, self.OnStart, self.btn1) 
        self.Show()
        
    def OnStart(self, event):
        mittel = os.path.sep
        self.btn1.SetLabel("Processing...")
        self.filename = wx.FileSelector("Choose a file to open")
        getrennt = self.filename.split(mittel)
        zwischen = getrennt[len(getrennt)-1]
        basefolder1 = self.filename.replace(zwischen,"")
        logfile = basefolder1+"cloudbust.log"
        #------------------------------------------
        scriptfile = open(self.filename,'r')
        scriptzeilen = scriptfile.readlines()
        amount = len(scriptzeilen)
        adding = 100/amount
        lineparts = []
        imnamemix = []
        for single in list(range(len(scriptzeilen)-1)):
            try:
                lineparts = scriptzeilen[single].split(',')
            
                arg = lineparts[0].split(mittel)
                argf = arg[len(arg)-1]
                self.imname = argf
                imnamemix = self.imname.split('.')
                imfolderinter = imnamemix[0]
                basefolder = basefolder1 + imfolderinter + mittel
                results_folder = basefolder + "results" + mittel
                folder_3D = basefolder + "3D_files" + mittel
                imagename = basefolder1+self.imname
                if (os.path.exists(basefolder))==False:
                    os.mkdir(basefolder)
                if (os.path.exists(results_folder))==False:
                    os.mkdir(results_folder)
                if (os.path.exists(folder_3D))==False:
                    os.mkdir(folder_3D)
                    #------------------------------------------
                    #stacks preparation
                stackobj = lib.stackprep.imprep()
                print (self.imname)
                #------------------------------------------
                # get data obljects from script file
                im,fehler,xvalue,yvalue,zvalue = stackobj.openfile(lineparts[0])
                print (self.imname)
                xpixdim = float(lineparts[1])
                ypixdim = float(lineparts[2])
                zpixdim = float(lineparts[3])
                hinter = float(lineparts[4])
                selindex = int(lineparts[5])
            
                imforrat = 750/im.shape[1]
            
                resolution = float(xpixdim)/float(imforrat)
                #------------------------------------------
                # ratio calculation
                transfer = stackobj.imratio(im,xpixdim,ypixdim,zpixdim)
                #------------------------------------------
                # scaling of dimensions
                finalscale = stackobj.sortscale(im,transfer[2],transfer[1],transfer[0],hinter)
                #------------------------------------------
                # thresholding
                pool = mp.Pool(mp.cpu_count())
                binary = [pool.apply(stackobj.threshold, args=(finalscale,))][0]
                pool.close()            
                #------------------------------------------
                # combine and rotate image
                pool = mp.Pool(mp.cpu_count())
                rotated = [pool.apply(stackobj.rotate, args=(binary,))][0]
                pool.close()            
                #rotated = stackobj.rotate(binary)
                #------------------------------------------
                # find edges in original
                pool = mp.Pool(mp.cpu_count())
                kanten = [pool.apply(stackobj.positions, args=(rotated,))][0]
                pool.close()            
                #------------------------------------------
                #cloud preparation
                cloudobj = lib.cloudprep.wolke()
                #------------------------------------------
                # extract 3D edges coordinates from original
                wolkenstack = cloudobj.combined(kanten)
                del stackobj
                #------------------------------------------
                # Combine clouds
                sauber = cloudobj.addingup(wolkenstack)
                #------------------------------------------
                #o3d preparation
                o3dwork = lib.o3dproc.o3dmeth(imfolderinter,folder_3D)
                #------------------------------------------
                # Save cloud as PLY
                plyfile = folder_3D+imfolderinter+".ply"
                lib.ioply.ioplynow(plyfile).saveplynow(sauber)
                del cloudobj
                #------------------------------------------
                #o3d point cloud characterisation
                (resultcoll, bestfit) = o3dwork.o3dcalcul(plyfile,results_folder,resolution)
                (results,resheader) = o3dwork.o3dextcalc(selindex, results_folder,folder_3D,resolution,resultcoll)
                #------------------------------------------
                #save results
                resultsfile = results_folder+imfolderinter+"_final_results.csv"
                with open(resultsfile,'a+') as f:
                    outline = (','.join(resheader))+'\n'
                
                    f.write(outline)
                    outline2 = (','.join([str(x) for x in results]))+'\n'
                    f.write(outline2)
                f.close()

                del o3dwork
                gc.collect()
                #------------------------------------------
                #update gauge
            except:
                with open(logfile,'a+') as faulty:
                    faultline = self.imname+" could not be analysed"
                    faulty.write(faultline)
                print ("Error occured")
                pass
                    
                    
            self.count = self.count + adding
            self.gauge.SetValue(int(self.count))
            wx.Yield()
        wx.MessageBox("Process finished","MassCloud" ,wx.OK | wx.ICON_INFORMATION)
        self.Close()
            
            
            
#----------------------------------------------------------------------------
class CbFrame(wx.Frame):
    def __init__(self, title, parent=None):
        wx.Frame.__init__(self, parent=parent, title=title, size = (1000,900))
        self.InitUI()
        
    #def InitLocale(self):
        #self.ResetLocale()

    def InitUI(self):
        panel = wx.Panel(self)
        self.cbDir = os.getcwd()

        #attention =
        wx.StaticText(panel, pos=(10, 10),label="Attention: Does not work with multichannel stacks!")
        #FileSelector
        loadbtn = wx.Button(panel, pos=(10,50),label='Load a stack')
        loadbtn.Bind(wx.EVT_BUTTON, self.on_press1)
        #text1a =
        wx.StaticText(panel, pos=(10,90),label="X pixel dimensions")
        self.x_dim = wx.TextCtrl(panel, pos=(200,90))
        #text2a =
        wx.StaticText(panel, pos=(10,130),label="Y pixel dimensions")
        self.y_dim = wx.TextCtrl(panel, pos=(200,130))
        #text3a =
        wx.StaticText(panel, pos=(10,170),label="Z pixel dimensions")
        self.z_dim = wx.TextCtrl(panel, pos=(200,170))
        #text4a =
        wx.StaticText(panel, pos=(10,210),label="Image Background =")
        hinter = ['White', 'Black']
        #Start proc.
        choise = wx.ComboBox(panel, pos=(10, 230), size = (150,30), choices=hinter, style=wx.CB_READONLY)
        choise.Bind(wx.EVT_COMBOBOX, self.OnSelect)
        
        startbtn = wx.Button(panel, pos=(10,300),label='Start analysis')
        startbtn.Bind(wx.EVT_BUTTON, self.on_press)

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

        self.Show()
        
    def OnSelect(self, event):
        bg = event.GetString()
        if bg == 'Black':
            self.hinter = 0.0
        else:
            self.hinter = 1.0
            
    def on_press1(self, event):

        self.filename = wx.FileSelector("Choose a file to open")
        stackobj = lib.stackprep.imprep()
        self.im,fehler,xvalue,yvalue,zvalue = stackobj.openfile(self.filename)
        if fehler == "-1":
            wx.MessageBox("file type could not be identified or entries missing","Cloudbuster" ,wx.OK | wx.ICON_INFORMATION)
            self.bild1b.SetBitmap(wx.Bitmap(icondir+'error.png'))
            self.Close()
        self.x_dim.SetValue(str(xvalue))
        self.y_dim.SetValue(str(yvalue))
        self.z_dim.SetValue(str(zvalue))
        import numpy as np
        import matplotlib.pyplot as plt
        makemax = np.max(self.im,axis=0)
        transfer = plt.imshow(makemax)
        plt.show()
        

    def OnQuit(self, event):
        self.Close()

    def on_press(self, event):

        mittel = os.path.sep
        
        icondir = self.cbDir+mittel+"icons"+mittel
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
        
        #------------------------------------------
        #names preparation
        namepreps = lib.names.nameprep(mittel, self.filename)
        (fullname,filesinglename) = namepreps.splitter()
        (results_folder,folder_3D, basefolder) = namepreps.foldprep(fullname)
        #------------------------------------------
        #stacks preparation
        stackobj = lib.stackprep.imprep()
        #------------------------------------------
        
        xpixdim = float(self.x_dim.GetValue())
        ypixdim = float(self.y_dim.GetValue())
        zpixdim = float(self.z_dim.GetValue())

        wx.GetApp().Yield()
          
        imforrat = 750/self.im.shape[1]
            
        resolution = float(xpixdim)/float(imforrat)
           
        if (os.path.exists(results_folder))==False:
            os.mkdir(results_folder)
                
        if (os.path.exists(folder_3D))==False:
            os.mkdir(folder_3D)
            
        self.bild1b.SetBitmap(wx.Bitmap(icondir+'load.png'))
        loadinfo = "Loaded: \n"+str(filesinglename)
        self.text1b.SetLabel(loadinfo)
        self.Update()
        print ("loaded")
        
        #------------------------------------------
        # ratio calculation
        transfer = stackobj.imratio(self.im,xpixdim,ypixdim,zpixdim)
        self.bild2b.SetBitmap(wx.Bitmap(icondir+'ratio.png'))
        self.text2b.SetLabel("Ratio between dimensions calculated")
        self.Update()
        print ("ratio")
        #------------------------------------------
        # scaling of dimensions
        finalscale = stackobj.sortscale(self.im,transfer[2],transfer[1],transfer[0],self.hinter)
        self.bild3b.SetBitmap(wx.Bitmap(icondir+'scale.png'))
        self.text3b.SetLabel("Stack scaled to 1x1x1 ratio.")
        self.Update()
        print ("scaled")
        del self.im,transfer
        #------------------------------------------
        # thresholding
        #import multiprocessing as mp
        
        pool = mp.Pool(mp.cpu_count())
        binary = [pool.apply(stackobj.threshold, args=(finalscale,))][0]
        pool.close()
        
        self.bild4b.SetBitmap(wx.Bitmap(icondir+'thresh.png'))
        self.text4b.SetLabel("Stack made binary.")
        self.Update()
        print ("thresholded")
        del finalscale
        #------------------------------------------
        # combine and rotate image
        
        pool = mp.Pool(mp.cpu_count())
        rotated = [pool.apply(stackobj.rotate, args=(binary,))][0]
        pool.close()
        #rotated = stackobj.rotate(binary)
        
        self.bild5b.SetBitmap(wx.Bitmap(icondir+'rotate.png'))
        self.text5b.SetLabel("Stack rotated to XZY and ZXY to improve outline.")
        self.Update()
        print ("rotated")
        del binary
        #------------------------------------------
        # find edges in original

        pool = mp.Pool(mp.cpu_count())
        kanten = [pool.apply(stackobj.positions, args=(rotated,))][0]
        pool.close()
        #kanten = stackobj.positions(rotated)
        
        self.bild6b.SetBitmap(wx.Bitmap(icondir+'edges.png'))
        self.text6b.SetLabel("Edges identified in all orientations.")
        self.Update()
        print ("edges found")
        del rotated
        #------------------------------------------
        #cloud preparation
        #import lib.cloudprep
        cloudobj = lib.cloudprep.wolke()
        #------------------------------------------
        # extract 3D edges coordinates from original
        wolkenstack = cloudobj.combined(kanten)
        self.bild7b.SetBitmap(wx.Bitmap(icondir+'edgepoint.png'))
        self.text7b.SetLabel("Point clouds extracted from all edges in all orientations.")
        self.Update()
        print ("edges to points")
        del kanten, stackobj
        #------------------------------------------
        # Combine clouds
        sauber = cloudobj.addingup(wolkenstack)
        self.bild8b.SetBitmap(wx.Bitmap(icondir+'cloud.png'))
        self.text8b.SetLabel("All point clouds combined.")
        self.Update()
        print ("combined")
        del wolkenstack
        #------------------------------------------
        #o3d preparation
        #import lib.o3dproc
        o3dwork = lib.o3dproc.o3dmeth(filesinglename,folder_3D)
        #------------------------------------------
        # Save cloud as PLY
        plyfile = folder_3D+filesinglename+".ply"
        lib.ioply.ioplynow(plyfile).saveplynow(sauber)
        self.bild9b.SetBitmap(wx.Bitmap(icondir+'reducecloud.png'))
        rawcloud = "Combined point cloud cleaned and saved as ply file: \n"+plyfile
        self.text9b.SetLabel(rawcloud)
        self.Update()
        print ("cleaned and saved")
        #------------------------------------------
        #o3d point cloud characterisation
        (resultcoll, bestfit) = o3dwork.o3dcalcul(plyfile,results_folder,resolution)
        print ("parts calculated")
        namelist = ['Torus','Ellipsoid','Parabolid','Hor. Cylinder','Vert. Cylinder']#,'Spindle'
        text = 'Best was: '+bestfit+'\n'+' Available shapes'
        selections=bestfit

        dlg = wx.SingleChoiceDialog(self, text,'Select shape to fit spheroid',namelist)
        if (dlg.ShowModal() == wx.ID_OK):
        
            selections = dlg.GetStringSelection()
        selindex = namelist.index(selections)
        (results,resheader) = o3dwork.o3dextcalc(selindex, results_folder,folder_3D,resolution,resultcoll)
        #------------------------------------------
        #save results
        resultsfile = results_folder+filesinglename+"_final_results.csv"
        f = open(resultsfile,"w")
        outline = (','.join(resheader))+'\n'
        f.writelines(outline)
        outline = (','.join([str(x) for x in results]))+'\n'
        f.writelines(outline)
        f.close
        #------------------------------------------
        # present results
        res1 = "Extension of entire cloud:  X = "+results[0]+" Y = "+results[1]
        res2 = "Extension of central spheroid:  X = "+results[10]+" Y = "+results[11]
        res3 = "Hint: "+results[17]
        res4 = "Number of separated parts = "+results[6]
        res5 = "Dist. from spheroid: Average = "+results[24]+" Average size of separated parts = "+results[28]
        res6 = "Number of extensions = "+results[35]+" Av. length of extensions = "+results[41]
            
        collres = res1 + "\n" + res2 + "\n" + res3 + "\n" + res4 + "\n" + res5 + "\n" + res6
            
        finaltext = "Key feature calculated and saved in file: \n"+resultsfile
        self.bild10b.SetBitmap(wx.Bitmap(icondir+'measure.png'))            
        self.Update()
        self.text10b.SetLabel(finaltext)
        wx.MessageBox(collres,"Selected Results" ,wx.OK | wx.ICON_INFORMATION)
        message = "Display resulting 3D model?"
        caption = "3D Results"
        mbdlg = wx.MessageDialog(self, message, caption,wx.YES_NO)
        if (mbdlg.ShowModal() == wx.ID_YES):
            mbdlg.SetMessage("Display resulting 3D model?")
            bigcloud = plyfile.replace(".ply","_color.ply")
            try:
                wolke =lib.ioply.ioplynow(bigcloud).openplyfile()
            except:
                self.text1b.SetLabel("Cloud not be displayed.")
                self.bild1b.SetBitmap(wx.Bitmap(self.icondirs+'error.png'))
            else:
                lib.ioply.ioplynow(wolke).showpcd()

        self.icondirs = icondir
        
        

#----------------------------------------------------------------------------
class ScriptFrame(wx.Frame):
    def __init__(self, title, parent=None):
        wx.Frame.__init__(self, parent=parent, title=title, size = (400,200))
        self.initUI()

    def initUI(self):
        panel = wx.Panel(self)
        wx.StaticText(panel, pos=(10,10), label="Open Folder with the image files.")
        wx.StaticText(panel, pos=(10,50), label="The script extracts image meta data and produces a script file.")
        fbtn = wx.Button(panel,pos = (50,90), label = "Open Image Folder")
        fbtn.Bind(wx.EVT_BUTTON, self.Onbasefolder)
        self.Show()

    def Onbasefolder(self, event):
        namelist = ['Torus','Ellipsoid','Parabolid','Hor. Cylinder','Vert. Cylinder']#,'Spindle'
        text = "Basic Shapes"
        dlg = wx.SingleChoiceDialog(self, text,'Select shape to fit spheroid',namelist)
        if (dlg.ShowModal() == wx.ID_OK):
            selections = dlg.GetStringSelection()
        which = namelist.index(selections)
        
        backgroundlist = ['Black','White']
        
        dlg = wx.SingleChoiceDialog(self, text,'Color of Background',backgroundlist)
        if (dlg.ShowModal() == wx.ID_OK):
            bgsel = dlg.GetStringSelection()
        whichbg = backgroundlist.index(bgsel)
        
        import lib.scriptmaker
        dirname = wx.DirSelector("Choose a folder to open")
        print (dirname)
        
        try:
            script = lib.scriptmaker.scriptmaker(dirname,whichbg,which)
            text = script.makescript()
            print (text)
            wx.MessageBox(text,"Scriptmaker" ,wx.OK | wx.ICON_INFORMATION)
        except:
            wx.MessageBox("No folder selected","Scriptmaker" ,wx.OK | wx.ICON_INFORMATION)
        self.Close()
#----------------------------------------------------------------------------
class AccuFrame(wx.Frame):
    def __init__(self, title, parent=None):
        wx.Frame.__init__(self, parent=parent, title=title, size = (400,200))
        self.initUI()

    def initUI(self):
        panel = wx.Panel(self)
        wx.StaticText(panel, pos=(10,10), label="Open Folder with the image and results subfolder.")
        wx.StaticText(panel, pos=(10,50), label="The script combines all result tables to a single table.")
        fbtn = wx.Button(panel,pos = (50,90), label = "Open Results Folder")
        fbtn.Bind(wx.EVT_BUTTON, self.OnResfolder)
        self.Show()

    def OnResfolder(self, event):
        import lib.sammler
        dirname = wx.DirSelector("Choose a folder to open")
        try:
            collection = lib.sammler.sammler(dirname)
            text = collection.collect()
            wx.MessageBox(text,"Accumulator" ,wx.OK | wx.ICON_INFORMATION)
        except:
            wx.MessageBox("No folder selected","Accumulator" ,wx.OK | wx.ICON_INFORMATION)
        self.Close()
#----------------------------------------------------------------------------
class StatFrame(wx.Frame):
    def __init__(self, title, parent=None):
        wx.Frame.__init__(self, parent=parent, title=title, size = (400,200))
        self.initUI()

    def initUI(self):
        panel = wx.Panel(self)
        wx.StaticText(panel, pos=(10,10), label="Open CSV table with accumulated data.")
        wx.StaticText(panel, pos=(10,50), label="The script performs data analysis and produces result graphs.")
        fbtn = wx.Button(panel,pos = (50,90), label = "Open data file")
        startbtn = wx.Button(panel,pos = (50,130), label = "Start analysis")
        fbtn.Bind(wx.EVT_BUTTON, self.OnDatfile)
        startbtn.Bind(wx.EVT_BUTTON, self.OnStart)
        self.Show()

    def OnDatfile(self,event):
        import pandas as pd
        Sppath = wx.FileSelector("Choose a file to open")
        mittel = os.path.sep
        try:
            getrennt = Sppath.split(mittel)
            zwischen = getrennt[len(getrennt)-1]
            self.basefolder = Sppath.replace(zwischen,"")
            csvfile = open(Sppath,'r')
            csvzeilen = csvfile.readline()
            csvarray = csvzeilen.split(',')
            self.sname = csvarray[0]
            csvfile.close()
            self.Sphdata = pd.read_csv(Sppath, names=csvarray)
            self.Sphdata = self.Sphdata.iloc[1:]
            namelist = list(self.Sphdata)
            self.nameparam = ""
            
            self.strings1 = []
            
            dlg1 = wx.MultiChoiceDialog(self, 'Select parameter for sample names','Parameters',namelist)
            while len(self.strings1) < 1:
                if (dlg1.ShowModal() == wx.ID_OK):
                    selections = dlg1.GetSelections()
                    self.strings1 = [namelist[x] for x in selections]
            self.nameparam = namelist[selections[0]]
            namelist.remove(self.strings1[0])

            dlg = wx.MultiChoiceDialog(self, 'Select parameters to REMOVE','Parameters',namelist)
            if (dlg.ShowModal() == wx.ID_OK):
                selections = dlg.GetSelections()
                self.strings = [namelist[x] for x in selections]
        except:
            wx.MessageBox("Problems opening file or importing data","Data analyser" ,wx.OK | wx.ICON_INFORMATION)
            self.Close()

    def OnStart(self,event):
        import lib.statistics
        
        try:
            calculation = lib.statistics.statistics(self.basefolder,self.Sphdata,self.strings,self.strings1,self.sname,self.nameparam)#lib.
            text = calculation.compute()
            wx.MessageBox(text,"Analysis" ,wx.OK | wx.ICON_INFORMATION)
            self.Close()
        except:
            wx.MessageBox("Analysis failed","Data analyser" ,wx.OK | wx.ICON_INFORMATION)
            self.Close()

#------------------------------------im.shape----------------------------------------
class ChoicePanel(wx.Panel):
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        self.frame_number = 1

        btn1 = wx.Button(self, pos=(10, 10), label = "Single stack analysis")
        btn1.Bind(wx.EVT_BUTTON, self.on_CBuster)

        btn2 = wx.Button(self, pos=(10, 50), label = "Script Maker")
        btn2.Bind(wx.EVT_BUTTON, self.on_scripter)

        btn3 = wx.Button(self, pos=(10, 90), label = "Multiple cloud analysis")
        btn3.Bind(wx.EVT_BUTTON, self.on_mass_clouds)

        btn4 = wx.Button(self, pos=(10, 130), label = "Results accumulation")
        btn4.Bind(wx.EVT_BUTTON, self.on_accumulate)

        btn5 = wx.Button(self, pos=(10, 170), label = "Data analysis")
        btn5.Bind(wx.EVT_BUTTON, self.on_data_analysis)

        btn6 = wx.Button(self,pos=(210, 210), label="Quit")
        btn6.Bind(wx.EVT_BUTTON, self.OnQuit)
        
        wx.StaticText(self, pos=(210,15),label="Analyse one stack")
        wx.StaticText(self, pos=(210,55),label="Make script for multiple analysis")
        wx.StaticText(self, pos=(210,95),label="Analyse multiple stacks")
        wx.StaticText(self, pos=(210,135),label="Combine results in folders to table")
        wx.StaticText(self, pos=(210,175),label="Statistical analyis from results table")

    def OnQuit(self, event):
        self.Close()
        exit()

    def on_CBuster(self, event):
        title = 'Cloudbuster: single stack analysis'
        frame = CbFrame(title = title)
            
    def on_scripter(self, event):
        title = 'Script from image fim.shapeolder'
        frame = ScriptFrame(title = title)

    def on_accumulate(self, event):
        title = 'Table from results folders'
        frame = AccuFrame(title = title)

    def on_data_analysis(self, event):
        title = 'Data analysis from CSV file'
        frame = StatFrame(title = title)
        
    def on_mass_clouds(self, event):
        title = 'Cloudbuster: many stacks analysis'
        frame = MassFrame(title=title)
        
#----------------------------------------------------------------------------
        
class CBChoice(wx.Frame):
    
    def __init__(self):
        wx.Frame.__init__(self, None, title='What to do?', size=(500, 300))
        panel = ChoicePanel(self)
        self.Show()
        

if __name__ == '__main__':
    app = wx.App(False)
    frame = CBChoice()
    app.MainLoop()
