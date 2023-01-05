#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 01:05:12 2023

@author: alankar
"""

import numpy as np
import os
import subprocess

class observedColDens:
    
    def __init__(self, galaxyDataFile='apjs456058t3_mrt.txt', galaxySizeFile='VirialRad.txt'):
        _tmp = subprocess.check_output('pwd').decode("utf-8").split('/')[1:]
        _pos = None
        for i, val in enumerate(_tmp):
            if val == 'MultiphaseGalacticHaloModel':
                _pos = i
        _tmp = os.path.join('/',*_tmp[:_pos+1], 'misc')
        self.loc = _tmp
        
        self.galaxyDataFile = '%s/%s'%(self.loc,galaxyDataFile)
        self.galaxySizeFile = '%s/%s'%(self.loc,galaxySizeFile)
        
    def readData(self, filename):
        lines = None
        start = 41
        with open(filename, 'r') as file:
            lines = file.readlines()
        
        galaxies = []
        names = []
        impact = []
        limit = []
        coldens = []
        e_coldens = []
        for line in lines[start:]:
            # print(line)
            galaxies.append(line[:17].strip())
            names.append(line[29:35])
            impact.append(float(line[25:28]))
            if line[78]==' ':
                limit.append('e')
            elif line[78]=='<':
                limit.append('l')
            elif line[78]=='>':
                limit.append('g')
            if (line[80:85] != '     '):
                coldens.append(float(line[80:85]))
                if limit[-1]=='e':
                    e_coldens.append(float(line[86:90]))
                else:
                    e_coldens.append(0.)
            else:
                if line[62]==' ':
                    limit[-1] = 'e'
                elif line[62]=='<':
                    limit[-1] = 'l'
                elif line[62]=='>':
                    limit[-1] = 'g'
                coldens.append(float(line[64:69]))
                if limit[-1]=='e':
                    e_coldens.append(float(line[70:74]))
                else:
                    e_coldens.append(0.)
        
        self.galaxies  = galaxies
        self.names     = names
        self.impact    = impact
        self.limit     = limit
        self.coldens   = coldens
        self.e_coldens = e_coldens
    
    def RreadRvir(self, filename):
        lines = None
        start = 6
        stop = 50
        with open(filename, 'r') as file:
            lines = file.readlines()
       
        qsoGal_names = []
        rvir = []
        for line in lines[start:stop]:
             # print(line) 
             values = line.split()
             qsoGal_names.append((values[0]+'_'+values[1]).strip())
             rvir.append(float(values[-1]))
        
        self.qsoGal_names =  qsoGal_names
        self.rvir         = rvir
    
    def col_densGen(self, element = 'O VI'):
        self.readData(self.galaxyDataFile)
        self.RreadRvir(self.galaxySizeFile)
        
        indices = [index for index in range(len(self.names)) if self.names[index].strip()==element ]
        coldens_min = []
        coldens_max = []
        coldens_detect = []
        e_coldens_detect = []
        gal_id_min = []
        gal_id_max = []
        gal_id_detect = []
        impact_select_min = []
        rvir_select_min = []
        impact_select_max = []
        rvir_select_max = []
        impact_select_detect = []
        rvir_select_detect = []
        
        for indx in indices:
            if   (self.limit[indx]=='l'): 
                gal_id_max.append(self.galaxies[indx])
                coldens_max.append(self.coldens[indx])
                impact_select_max.append(self.impact[indx])
                rvir_select_max.append(self.rvir[self.qsoGal_names.index(self.galaxies[indx])])
            elif (self.limit[indx]=='g'): 
                gal_id_min.append(self.galaxies[indx])
                coldens_min.append(self.coldens[indx])
                impact_select_min.append(self.impact[indx])
                rvir_select_min.append(self.rvir[self.qsoGal_names.index(self.galaxies[indx])])
            elif (self.limit[indx]=='e'): 
                gal_id_detect.append(self.galaxies[indx])
                coldens_detect.append(self.coldens[indx])
                e_coldens_detect.append(self.e_coldens[indx])
                impact_select_detect.append(self.impact[indx])
                rvir_select_detect.append(self.rvir[self.qsoGal_names.index(self.galaxies[indx])])
                
        impact_select_min = np.array(impact_select_min)
        rvir_select_min = np.array(rvir_select_min)
        impact_select_max = np.array(impact_select_max)
        rvir_select_max = np.array(rvir_select_max)
        impact_select_detect = np.array(impact_select_detect)
        rvir_select_detect = np.array(rvir_select_detect)
        coldens_min = np.array(coldens_min)
        coldens_max = np.array(coldens_max)
        coldens_detect = np.array(coldens_detect)
        e_coldens_detect = np.array(e_coldens_detect)
        
        return (gal_id_min, gal_id_max, gal_id_detect, 
                rvir_select_min, rvir_select_max, rvir_select_detect,
                impact_select_min, impact_select_max, impact_select_detect,
                coldens_min, coldens_max, coldens_detect, e_coldens_detect)