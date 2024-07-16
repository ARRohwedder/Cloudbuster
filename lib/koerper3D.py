#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 21:40:36 2022

@author: linatix2
"""

# takes 3,1 array for size in x,y,z direction and point number for resolution.
# returns numpy array of surface points for 3D body.

import numpy as np

class koerper:
    def __init__(self,pointnumber):
        #self.coefs = coeficents
        self.points = pointnumber
        
        # provide array for angular calculation
        self.u = np.linspace(0, 2*np.pi, pointnumber)
        self.v = np.linspace(0, 2*np.pi, pointnumber)
        
        # prepare a meshgrid based on angular arrays
        self.u,self.v = np.meshgrid(self.u, self.v)
        
    def ellipsoid(self,coefs,center):
        
        rx, ry, rz = coefs
       
        # calculate x,y,z point positions from parameters
        x = (rx * np.sin(self.u)*np.cos(self.v))+center[0]
        y = (ry * np.sin(self.u)*np.sin(self.v))+center[1]
        z = (rz * np.cos(self.u))+center[2]
        
        x1,y1,z1 = [],[],[]
        
        # store x,y,z point postions in individual arrays
        for i in range(x.shape[0]):
            for j in range (x.shape[1]):
                x1.append(x[i,j])
                y1.append(y[i,j])
                z1.append(z[i,j])
        
        # combine x,y,z arrays
        koerper = np.column_stack((np.asarray(x1),np.asarray(y1),np.asarray(z1)))
        koerper = np.unique(koerper,axis=0)
        
        return koerper
    
    def torus(self,coefs,center):
        
        rx, ry, rz = coefs
        rx = rx/2
        ry = ry/2
        rz = rz
        
        # calculate x,y,z point positions from parameters (rx,ry,rz)
        #x = rx * np.cos(self.u)+rz*np.cos(self.v)*np.cos(self.u) <- adaptation for circular torus
        x = (rx * np.cos(self.u)+(rx/2)*np.cos(self.v)*np.cos(self.u))+center[0]
        #y = ry*np.sin(self.u)+rz*np.cos(self.v)*np.sin(self.u) <- adaptation for circular torus
        y = (ry*np.sin(self.u)+(ry/2)*np.cos(self.v)*np.sin(self.u) )+center[1]
        z = rz*np.sin(self.v)+(rz)#+center[2]
        
        x1,y1,z1 = [],[],[]
        
        # store x,y,z point postions in individual arrays
        for i in range(x.shape[0]):
            for j in range (x.shape[1]):
                x1.append(x[i,j])
                y1.append(y[i,j])
                z1.append(z[i,j])
        
        # combine x,y,z arrays
        koerper = np.column_stack((np.asarray(x1),np.asarray(y1),np.asarray(z1)))
        koerper = np.unique(koerper,axis=0)
        
        return koerper
    
    def parabolid(self,coefs,center):
        
        rx, ry, rz = coefs
        
        # calculate x,y,z point positions from parameters (rx,ry,rz)
        x = (-(rx)*(self.u/(2*np.pi))*np.cos(self.v))+center[0]
        y = (-(ry)*(self.u/(2*np.pi))*np.sin(self.v))+center[1]
        z = (-(rz*2)*np.square(self.u/(2*np.pi))+(rz))+center[2]
        #zbase = (np.min(z))+center[2] #base plate for parabolid
        zbase = (np.min(z))
        x1,y1,z1 = [],[],[]
        
        # store x,y,z point postions in individual arrays
        for i in range(x.shape[0]):
            for j in range (x.shape[1]):
                x1.append(x[i,j])
                y1.append(y[i,j])
                z1.append(z[i,j])
                
                x1.append(x[i,j])
                y1.append(y[i,j])
                z1.append(zbase)
        
        # combine x,y,z arrays
        koerper = np.column_stack((np.asarray(x1),np.asarray(y1),np.asarray(z1)))
        koerper = np.unique(koerper,axis=0)
        
        return koerper
    
    def horcylinder(self,coefs,center):
        
        rx, ry, rz = coefs
        
        # calculate x,y,z point positions from parameters (rx,ry,rz)
        x = (rx*(self.u/(2*np.pi))-(rx/2))+center[0]
        y = (ry*np.sin(self.v))+center[1]
        z = (rz*np.cos(self.v))+center[2]
        
        minx = np.min(x)
        maxx = np.max(x)
                
        x1,y1,z1 = [],[],[]
        
        # Addition to close cylinder at top and bottom
        zirk = (np.linspace(0, rz, self.points))+center[2]
        zmin = (zirk*np.cos(self.v))+center[2]
        
        # store x,y,z point postions in individual arrays
        for i in range(x.shape[0]):
            for j in range (x.shape[1]):
                x1.append(x[i,j])
                y1.append(y[i,j])
                z1.append(z[i,j])
                
                x1.append(minx)
                y1.append(y[i,j])
                z1.append(zmin[i,j])
                
                x1.append(maxx)
                y1.append(y[i,j])
                z1.append(zmin[i,j])
        
        # combine x,y,z arrays
        koerper = np.column_stack((np.asarray(x1),np.asarray(y1),np.asarray(z1)))
        koerper = np.unique(koerper,axis=0)
        
        return koerper
    
    def vertcylinder(self,coefs,center):
        
        rx, ry, rz = coefs
        
        # calculate x,y,z point positions from parameters (rx,ry,rz)
        x = (rx*np.cos(self.v))+center[0]
        y = (ry*np.sin(self.v))+center[1]
        z = (rz*(self.u/(2*np.pi))-(rz))+(center[2])#/2
        
        minz= np.min(z)
        maxz = np.max(z)
                
        x1,y1,z1 = [],[],[]
        
        # Addition to close cylinder at top and bottom
        zirkx = np.linspace(0, rx, self.points)
        zirky = np.linspace(0, ry, self.points)
        xmin = (zirkx*np.cos(self.v))+center[0]
        ymin = (zirky*np.sin(self.v))+center[1]
        
        # store x,y,z point postions in individual arrays
        for i in range(x.shape[0]):
            for j in range (x.shape[1]):
                x1.append(x[i,j])
                y1.append(y[i,j])
                z1.append(z[i,j])
                
                x1.append(xmin[i,j])
                y1.append(ymin[i,j])
                z1.append(minz)
                
                x1.append(xmin[i,j])
                y1.append(ymin[i,j])
                z1.append(maxz)
        
        # combine x,y,z arrays
        koerper = np.column_stack((np.asarray(x1),np.asarray(y1),np.asarray(z1)))
        koerper = np.unique(koerper,axis=0)
        
        return koerper
    
    def spindle(self,coefs,center):
        
        # actually 2 halfs of a parabolid
        rx, ry, rz = coefs
        
        # calculate x,y,z point positions from parameters (rx,ry,rz)
        # negative part:
        x = (-(rx)*np.square(self.u/(2*np.pi))+(rx))+center[0]
        y = (-(ry)*(self.u/(2*np.pi))*np.sin(self.v))+center[1]
        z = (-(rz)*(self.u/(2*np.pi))*np.cos(self.v))+center[2]
        
        # positive part:
        xpos = ((rx)*np.square(self.u/(2*np.pi))-(rx))+center[0]
        ypos = ((ry)*(self.u/(2*np.pi))*np.sin(self.v))+center[1]
        zpos = ((rz)*(self.u/(2*np.pi))*np.cos(self.v))+center[2]
             
        x1,y1,z1 = [],[],[]

        # store x,y,z point postions in individual arrays
        for i in range(x.shape[0]):
            for j in range (x.shape[1]):
                x1.append(x[i,j])
                y1.append(y[i,j])
                z1.append(z[i,j])
                
                x1.append(xpos[i,j])
                y1.append(ypos[i,j])
                z1.append(zpos[i,j])
        
        # combine x,y,z arrays
        koerper = np.column_stack((np.asarray(x1),np.asarray(y1),np.asarray(z1)))
        koerper = np.unique(koerper,axis=0)
        
        return koerper