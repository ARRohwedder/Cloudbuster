#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 15:30:04 2020

@author: Dr. Arndt Rohwedder, University of Huddersfield
"""

import wx

class Menwin(wx.Frame): 
            
   def __init__(self, parent, title): 
      super(Menwin, self).__init__(parent, title = title,size = (300,600))  
      self.InitUI() 
         
   def InitUI(self):    
      pnl = wx.Panel(self) 
      vbox = wx.BoxSizer(wx.VERTICAL)
		
      hbox1 = wx.BoxSizer(wx.HORIZONTAL) 
      hbox2 = wx.BoxSizer(wx.HORIZONTAL)
      hbox3 = wx.BoxSizer(wx.HORIZONTAL)
      hbox4 = wx.BoxSizer(wx.HORIZONTAL)
      hbox5 = wx.BoxSizer(wx.HORIZONTAL)
      hbox6 = wx.BoxSizer(wx.HORIZONTAL)
		
      self.btn1 = wx.Button(pnl, pos=(10, 10), label = "Single cloud analysis") 
      self.btn1.Bind(wx.EVT_BUTTON, self.OnStart1)
      
      self.btn2 = wx.Button(pnl, pos=(10, 10), label = "Multiple cloud analysis") 
      self.btn2.Bind(wx.EVT_BUTTON, self.OnStart2) 
		
      self.btn3 = wx.Button(pnl, pos=(10, 10), label = "Results accumulation") 
      self.btn3.Bind(wx.EVT_BUTTON, self.OnStart3)
      
      self.btn4 = wx.Button(pnl, pos=(10, 10), label = "Data analysis") 
      self.btn4.Bind(wx.EVT_BUTTON, self.OnStart4) 
      
      self.btn5 = wx.Button(pnl, pos=(10, 10), label = "Script maker") 
      self.btn5.Bind(wx.EVT_BUTTON, self.OnStart5) 
      
      self.closebtn = wx.Button(pnl, pos=(10, 10), label = "Quit") 
      self.closebtn.Bind(wx.EVT_BUTTON, self.OnClose)

      hbox1.Add(self.btn1, proportion = 1)   
      vbox.Add((0, 30)) 
      vbox.Add(hbox1, proportion = 1,flag = wx.ALIGN_CENTRE)
      
      hbox2.Add(self.btn5, proportion = 1)
      vbox.Add((0, 20)) 
      vbox.Add(hbox2, proportion = 1, flag = wx.ALIGN_CENTRE)
      
      hbox3.Add(self.btn2, proportion = 1)
      vbox.Add((0, 30)) 
      vbox.Add(hbox3, proportion = 1, flag = wx.ALIGN_CENTRE)
      
      hbox4.Add(self.btn3, proportion = 1)
      vbox.Add((0, 40)) 
      vbox.Add(hbox4, proportion = 1, flag = wx.ALIGN_CENTRE) 
      pnl.SetSizer(vbox)
      
      hbox5.Add(self.btn4, proportion = 1)
      vbox.Add((0, 60)) 
      vbox.Add(hbox5, proportion = 1, flag = wx.ALIGN_CENTRE) 
      pnl.SetSizer(vbox) 

      hbox6.Add(self.closebtn, proportion = 1)
      vbox.Add((0, 80)) 
      vbox.Add(hbox6, proportion = 1, flag = wx.ALIGN_CENTRE) 
      pnl.SetSizer(vbox) 
         
      self.Centre() 
      self.Show()
		
   def OnQuit(self, e):
       self.Close()
       exit()
    
   def OnStart1(self, e):
       import cloudbuster
              
   def OnStart2(self, e):
       import masscloud
              
   def OnStart3(self, e):
       import accumulate
       
   def OnStart4(self, e):
       import statistics
       
   def OnStart5(self, e):
       import scriptmaker

   def OnClose(self, e):
       self.Close()
       exit()

       
ex = wx.App() 
Menwin(None,'What to do:') 
ex.MainLoop()