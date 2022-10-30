#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 15:35:54 2021

@author: linatix2
"""
import wx
import os
import tifffile as tf

class StatFrame(wx.Frame):
    def __init__(self, parent, title):
        super(StatFrame, self).__init__(parent, title = title,size = (300,200))
        self.InitUI()
        
    def InitUI(self):
        self.mittel = os.path.sep
        panel = wx.Panel(self)
        self.imbutton = wx.Button(panel, label = "Open Image Folder")      
        self.Bind(wx.EVT_BUTTON, self.OnImfolder, self.imbutton)
        self.imbutton.SetPosition((50, 50))
        self.Show()
        
    def OnImfolder(self, ev):
        dirname = wx.DirSelector("Choose a folder to open")
        folder = dirname+self.mittel
        outfile = dirname+self.mittel+"script.txt"
        listOfFiles = list()
        tiflist = []
        endscript = open(outfile, "w" )
        for (dirpath, dirnames, filenames) in os.walk(dirname):
            listOfFiles += [os.path.join(dirpath, file) for file in filenames]
        for line in list(range(len(listOfFiles))):
            singlefile = listOfFiles[line]
            getrennt = singlefile.split(self.mittel)
            zwischen = getrennt[len(getrennt)-1]
            test = ('.tif' in zwischen)
            if test == True :
                tiflist.append(zwischen)
        for single in list(range(len(tiflist))):
            tif = tf.TiffFile(folder+tiflist[single])
            for page in tif.pages:
                for tag in page.tags:
                    tag_name, tag_value = tag.name, tag.value
                    if 'unit=' in str(tag_value):
                        alles = str(tag_value)
                        zeilen = alles.split("\n")
                        zauflösung = zeilen[4]
                        zaufteil = zauflösung.split("=")
                    if tag_name == 'XResolution':
                        tagwertstring = str(tag.value)
                zauflösung = (float(zaufteil[1]))
                tagwertstring = tagwertstring.replace('(','')
                tagwertstring = tagwertstring.replace(')','')
                tagwertstring = tagwertstring.replace(' ','')
                xzeilen = tagwertstring.split(",")
                xauflösung = float(int(xzeilen[1])/int(xzeilen[0]))
            ausgabezeile = tiflist[single]+","+str(xauflösung)+","+str(xauflösung)+","+str(zauflösung)+","+"0.0"+"\n"
            endscript.writelines(ausgabezeile)
        ausgabezeile = "\n"
        endscript.writelines(ausgabezeile)
        endscript.close()
        text = "Script file generated: \n"+outfile
        wx.MessageBox(text,"Scriptmaker" ,wx.OK | wx.ICON_INFORMATION)
        self.Close()

def run():
    ex = wx.App() 
    StatFrame(None,'Script Maker') 
    ex.MainLoop()
