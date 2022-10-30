#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 14:40:00 2021

#PCA: author= Erdogan Taskesen, year=2019, url=https://github.com/erdogant/pca

@author: Dr. Arndt Rohwedder
"""

import pcacalc
import corcalc
import hierclu
import kmeans
import figplot

from sklearn.preprocessing import StandardScaler
import wx
import os
import numpy as np
import pandas as pd
from pandas import set_option
import matplotlib.pyplot as plt
import re


class StatFrame(wx.Frame):
    def __init__(self, parent, title):
        super(StatFrame, self).__init__(parent, title = title,size = (500,200))
        self.InitUI()
        
    def InitUI(self):
        self.mittel = os.path.sep
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        
        self.sphbutton = wx.Button(panel, label = "Open Results Folder")
        self.startbutton = wx.Button(panel, label = "Start calculation")
        
        self.Bind(wx.EVT_BUTTON, self.OnSpheroid, self.sphbutton)
        self.Bind(wx.EVT_BUTTON, self.OnStart, self.startbutton)
        
        hbox1.Add(self.sphbutton, proportion = 1, flag = wx.RIGHT, border = 10)
        hbox2.Add(self.startbutton, proportion = 1, flag = wx.RIGHT, border = 10)
        
        vbox.Add((0, 10))
        vbox.Add(hbox1, flag = wx.ALIGN_CENTRE)
        
        vbox.Add((0, 40))
        vbox.Add(hbox2, flag = wx.ALIGN_CENTRE)
       
        panel.SetSizer(vbox)
        
        self.Show()
        
    def OnSpheroid(self, ev):

        self.dirname = wx.DirSelector("Choose a folder to open")
        Sppath = self.dirname+self.mittel+"acc_results.csv"
        self.basefolder = self.dirname+self.mittel
        csvfile = open(Sppath,'r')
        csvzeilen = csvfile.readline()
        csvarray = csvzeilen.split(',')
        self.sname = csvarray[0]
        csvfile.close()
        self.Sphdata = pd.read_csv(Sppath, names=csvarray)
        self.Sphdata = self.Sphdata.iloc[1:]
        namelist = list(self.Sphdata)
        dlg = wx.MultiChoiceDialog(self, 'Select parameters to REMOVE','Parameters',namelist)
        if (dlg.ShowModal() == wx.ID_OK):
            selections = dlg.GetSelections()
            self.strings = [namelist[x] for x in selections]
            #print ("You chose: ", strings)
        
    def OnStart(self, ev):
        
        emp_lis = []
        for z in range(1,self.Sphdata.shape[1]):
            wert = self.Sphdata.iat[1,z]
            new_result = re.findall('[0-9]+', wert)
            if wert.isdigit():
                emp_lis.append(int(z))
            if new_result != []:
                if len(new_result) < 2:
                    self.Sphdata.iloc[:,z] = self.Sphdata.iloc[:,z].astype(int)
                if len(new_result) >= 2:
                    self.Sphdata.iloc[:,z] = self.Sphdata.iloc[:,z].astype(float)
        
        floats = self.Sphdata.loc[:, self.Sphdata.dtypes == 'float64']
        ints = self.Sphdata.loc[:, self.Sphdata.dtypes == 'int64']
        seldata = pd.concat([floats, ints], axis=1, join='inner')
        samplenames = self.Sphdata[['File']]
        #del seldata['PixResol']
        for a in range(0,len(self.strings)-1):
            del seldata[self.strings[a]]
        
        
        #del seldata['AMaxZ']
        #del seldata['SPMaxZ']
        
       
        #PCA
        
        selarray = seldata.values
        data_scalar = StandardScaler().fit(selarray)
        data_rescaled = data_scalar.transform(selarray)
        selnames = np.asarray(seldata.columns)
        calcpca = pcacalc.pcacalc(seldata,data_rescaled,selnames)
        pcares = calcpca.calcul()
        pca_topten = pcares[0]
        
        pca_topten = list(dict.fromkeys(pca_topten))
        
        pca_topten = list( dict.fromkeys(pca_topten))
        pca_toptxt = []
        shortdata = seldata[pca_topten]
        

        for h in range(0,len(pca_topten)):
            pca_toptxt.append(pca_topten[h])
        
        pca_topten_txt = ", ".join(pca_toptxt)
        pcadf = pd.DataFrame(pca_topten)
        pcadataname = self.basefolder+"PCA_top.csv"
        pcadf.to_csv(pcadataname)
        pcadataname = self.basefolder+"PCA_top_raws.csv"
        shortdata.to_csv(pcadataname)
        
        testout = self.basefolder+"Scaled_toprated.csv"
        column_headers = list(shortdata.columns.values)
        pcadfarray = np.asarray(shortdata)
        pcadf_scalar = StandardScaler().fit(pcadfarray)
        pcadf_rescaled = pcadf_scalar.transform(pcadfarray)
        pcadf_scaled = pd.DataFrame(pcadf_rescaled)
        pcadf_scaled.columns =column_headers
        samplenamearray = samplenames[:].values
        pcadf_scaled.insert(0,'Samplenames',samplenamearray,True)
        pcadf_scaled.to_csv(testout)

        for i in range(0,len(pca_topten)):
            firsttxt = pca_topten[i]
            boxplot = self.Sphdata.boxplot(firsttxt, by=self.sname, rot=90, fontsize=8, figsize=(50,10))
            kfig = self.basefolder+firsttxt+".svg"
            plt.savefig(kfig)

        #Correlation
        toptenar = np.asarray(shortdata)
        correl = corcalc.corcalc(toptenar,pca_topten)
        pcacor = correl.correlcalc()
        cordataname = self.basefolder+"Correlation.csv"
        pcacor.to_csv(cordataname)
        pcacorred = pcacor.drop(pcacor.index[[0]])
        firstcol = pcacorred[pcacorred.columns[0:1]].to_numpy()
        pos_text = []
        neg_text = []
        for j in range(0,firstcol.shape[0]):
            if firstcol[j][0] >= 0:
                pos_text.append(pca_topten[j+1])
            if firstcol[j][0] < 0:
                neg_text.append(pca_topten[j+1])
        pos_df = pcadf_scaled[pos_text].mean(axis=1)
        neg_df = pcadf_scaled[neg_text].mean(axis=1)
        
        # For grouped data

        pre_data = pcadf_scaled.groupby(pcadf_scaled['Samplenames']).mean()
        grouparray = np.asarray(pre_data.index)
        data_rotated = pre_data.T
        rotated_array = data_rotated.values
        rotated_data_scalar = StandardScaler().fit(rotated_array)
        rotated_data_rescaled = rotated_data_scalar.transform(rotated_array)
        new_rotated = pd.DataFrame(rotated_data_rescaled)
    
        samplecorr = new_rotated.corr(method='pearson')
        
        #Hierarchical Clustering
        toptennames = pca_topten
        first = pos_df.to_numpy()
        second = neg_df.to_numpy()
        count=np.arange(0,first.size)
        dend = pd.DataFrame({'index': count,'First': first}, columns=['index','First'])
        hiera = hierclu.HierClu(dend)
        hierc = hiera.hiercalc()
        hierdf = pd.DataFrame(samplenames)
        hierdf.insert(1,'CluOrder',hierc,True)
        hiername = self.basefolder+"Hier_Clu.csv"
        hierdf.to_csv(hiername)
        
        #K-means clustering
        kmdf = pd.DataFrame({'First': first,'Second': second}, columns=['First','Second'])
        kmdfarray = np.asarray(kmdf)
        kmdf_scalar = StandardScaler().fit(kmdfarray)
        kmdf_rescaled = kmdf_scalar.transform(kmdfarray)
        kminit = kmeans.myKMeans(kmdf_rescaled)
        clusters = kminit.KMeanscalc()
        kmdf_complete = pd.DataFrame(kmdf_rescaled,columns=[toptennames[0],toptennames[1]])
        kmdf_complete.insert(2,'clusters',clusters[0],True)
        kmoutdf = self.Sphdata[['File']]
        kmoutdf.insert(1,'clusters',clusters[0],True)
        kmdf_name = self.basefolder+"K_Means_clu.csv"
        kmoutdf.to_csv(kmdf_name)
        kmdf_name = self.basefolder+"K_means_raw.csv"
        kmdf_complete.to_csv(kmdf_name)
        
        #plotting
        plotting = figplot.figplot(pcares[2],pcacor,pca_topten,samplecorr,grouparray,dend,kmdf_complete,self.basefolder,len(pca_topten))
        plotting.FigPlot()
        
        text = "PCA : Most relevant (95% of variances) parameters= \n"+pca_topten_txt+"\n\n"+"K-Means Clustering:\n"+str(clusters[1])+" Min. Clusters Identified, Used "+str(clusters[1]+1)+" \n\n"+"Detailed results stored as .csv files and graphs as .svg files in folder: \n"+self.basefolder
        wx.MessageBox(text,"Analysis" ,wx.OK | wx.ICON_INFORMATION)
def run():        
    ex = wx.App() 
    StatFrame(None,'Data Analysis') 
    ex.MainLoop()
