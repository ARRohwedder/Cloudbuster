#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 15:41:23 2020

@author: Dr. Arndt Rohwedder, University of Huddersfield
"""
import wx
import os
import sammler

class AccFrame(wx.Frame):
    
    def __init__(self, parent, title):
        super(AccFrame, self).__init__(parent, title = title,size = (500,200))
        self.InitUI()
        
    def InitUI(self):
        panel = wx.Panel(self)
        self.cbDir = os.getcwd()
        self.info1 = wx.StaticText(panel, label="Open Folder with the image and results subfolder.")        
        self.info2 = wx.StaticText(panel, label="The script combines all result tables to a single table.")        
        self.my_btn = wx.Button(panel, label='File Folder')
        self.info1.SetPosition((20, 20))
        self.info2.SetPosition((20, 60))
        self.my_btn.SetPosition((20, 100))
        self.my_btn.Bind(wx.EVT_BUTTON, self.on_press)
        self.Show()

    def OnQuit(self, e):
        self.Close()

    def on_press(self, event):

        self.dirname = wx.DirSelector("Choose a folder to open")

        mainfileheader = 'Sample,AMaxX,AMaxY,AMaxZ,ACDEVYX,ABDEVYZ,ABDEVXZ,A_Hint,Sep_Comp,SpMaxX,SPMaxY,SPMaxZ,SPCDEVYX,SPBDEVYZ,SPBDEVXZ,Sp_Hint,MedCl_Dist,AvCl_Dist,VarCl_Dist,MaxCl_Dist,PixResol\n'
        mainoutfile = "acc_results.csv"
        maintofind = 'Final_Results.csv'
        
        maincol = sammler.sammler(mainfileheader,mainoutfile,maintofind,self.dirname)
        maincol.collect()

        text = "Results saved in:\n"+mainoutfile+"\n"

        wx.MessageBox(text,"Result Accumulation" ,wx.OK | wx.ICON_INFORMATION)
        self.Close()
def run():    
    ex = wx.App() 
    AccFrame(None,'Accumulate') 
    ex.MainLoop()
