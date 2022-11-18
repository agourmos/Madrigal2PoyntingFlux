# -*- coding: utf-8 -*-
"""
Title: PlotPF.py

Created on Mon Oct 24 13:16:06 2022

@author: Adam Gourmos

The purpose of this script is to plot poynting flux along the flight path. The
plots are provided in hourly gaps or pass-by-pass. These plots are then saved 
to a file in the current code directory. 

** Notes before use:
    -

"""
#%% Packages and modules
import os
import numpy as np
import matplotlib.pyplot as plt
import functions.satplottools2 as spt
from functions.FindHourly import FindHourly
from functions.FindPH import FindPH
from functions.FindIDX import FindIDX


def PlotPF(settings):
    #%% Part A: Variable definitions ==========================================
    # Define parseing type (i.e pass-by-pass or hourly)
    parseType = settings['parseType'] 
    
    # Determine whether or not colorbar will have fixed values or not
    boundsType = settings['boundsType']
    
    # Find index of values used for plotting
    val_pos = FindIDX(settings)
    
    # Define directory of reduced data
    DataFileDir = os.path.join(os.getcwd(),'data','ReducedData')
    
    # Define vector of filenames given from reduction                          
    DataFiles = os.listdir(DataFileDir)    
    
    # Define indicies of values used for parsing and plotting 
    hour_idx = val_pos[3]
    min_idx = val_pos[4]
    sec_idx = val_pos[5]
    MLAT_idx = val_pos[6]
    MLT_idx = val_pos[7]
    poy_idx = val_pos[8]
                       
    for DataFilename in DataFiles:
        # Define empty array
        DataArr = np.empty([0,sum(settings['parameters_vec'])])  
                
        #Define variables
        DataFile = os.path.join(DataFileDir,DataFilename)
        DMSPType = 'DMSP F' + str(DataFilename[19:21])
        DMSPType2 = 'DMSPF' + str(DataFilename[19:21])
        
# =============================================================================
        #%% Part B: Data extraction **Takes awhile**
        # Begin data extraction
        with open(DataFile) as data:
            DataList = data.readlines()
            
        # Convert the list into an array
        for line in DataList:
            # Find the first line
            try:
                # line = line.replace(" ", ",")
                lineHold = np.asarray([float(i) for i in line.strip().split()])

            except ValueError:
                continue
            
            # Insert values into data array
            DataArr = np.vstack([DataArr,lineHold])
                
        #%% Part E: Data seperation
        # Find the maximum and minimum bounds values to deteremine colorbar bounds
        bounds = [np.nanmin(DataArr[:,poy_idx]),np.nanmax(DataArr[:,poy_idx])]
        
        # Insert bounds into dictionary to pass through function
        boundsDict = {'boundsType':boundsType,'bounds':bounds}
        
        if parseType == 0:
            # Use function to seperate data into hourly and hemisphere dictionary values
            Dict = FindHourly(DataArr[1:-3,:],hour_idx,MLAT_idx)
        elif parseType == 1:
            # Use function to seperate data into pass-by-pass dictionary values
            Dict = FindPH(DataArr[1:-3,:],MLAT_idx)
            
        #%% PART F: Data conversion and definition
        # For each hour and hemisphere, plot data
        for i in Dict:
            # Find index from chosen pass and hemisphere
            DataArr_hold = Dict[i]
        
            # Find magnetic latitude
            MLAT = DataArr_hold[:,MLAT_idx]
            
            # Check to see if array is empty
            try:
                # Define North or South
                if MLAT[0] > 0:
                    hemi = 'N'
                else:
                    hemi = 'S'
            except IndexError:
                continue
            
            # Extract MLT and convert to polar plot equivlent
            MLT = DataArr_hold[:,MLT_idx] 
        
            # Extract poynting values
            poy = DataArr_hold[:,poy_idx]
        
            # Define date name
            date_hold = str(int(DataArr_hold[0,1]))+ '/' + str(int(DataArr_hold[0,2])) + '/' + str(int(DataArr_hold[0,0]))
            date_hold_ns = str(int(DataArr_hold[0,0]))+ str(int(DataArr_hold[0,1])) + str(int(DataArr_hold[0,2]))
            
            # Extract time string
            time_str = str(int(DataArr_hold[0,hour_idx])) + ':' + str(int(DataArr_hold[0,min_idx])) + \
                ':' + str(int(DataArr_hold[0,sec_idx])) + '-' + str(int(DataArr_hold[-1,hour_idx])) + \
                ':' + str(int(DataArr_hold[-1,min_idx])) + ':' + str(int(DataArr_hold[-1,sec_idx]))
        
        #%% Part X-I: Plotting PF =============================================
            # Define figures for North and South pole
            fig0, ax0 = plt.subplots(1) # North Pole
            
            # Use geospacepy plotting tools to add in the poynting vector
            spt.hairplot(fig0,ax0,MLAT,MLT,poy,hemi,boundsDict,settings)
            
            # Define string gap
            s = "\\"
            
            # Determine if this is a pass-by-pass case or hourly
            if parseType == 0:
                # Title plot
                if MLAT[0] < 0:
                    titlename = DMSPType + ' Poynting Flux Along Path, Southern Hemisphere: \n' + date_hold + ' ' + time_str
                else:
                    titlename = DMSPType + ' Poynting Flux Along Path, Northern Hemisphere: \n' + date_hold + ' ' + time_str
                    
                # Make save directory for PF
                if not os.path.isdir('plots/'+date_hold_ns + '_Hourly_' + DMSPType2 + '_PF'):
                    os.makedirs('plots/'+date_hold_ns + '_Hourly_' + DMSPType2 + '_PF')
                    
                savePath = os.getcwd() + r"\plots" + s + date_hold_ns + '_Hourly_'+ DMSPType2 + '_PF' + s +  'Hour' + str(int(DataArr_hold[0,hour_idx])) + hemi + '.png'
                    
            elif parseType == 1:
                if MLAT[0] < 0:
                    titlename = DMSPType + ' Poynting Flux Along Path, Southern Hemisphere: \n' + date_hold + ' Pass #' + i[1:3] + ' ' +time_str
                else:
                    titlename = DMSPType + ' Poynting Flux Along Path, Northern Hemisphere: \n' + date_hold + ' Pass #' + i[1:3] + ' '+ time_str
                    
                # Make save directory for PF
                if not os.path.isdir('plots/'+date_hold_ns + '_PBP_'+ DMSPType2 + '_PF'):
                    os.makedirs('plots/'+date_hold_ns + '_PBP_' + DMSPType2 + '_PF')
                    
                savePath = os.getcwd() + r"\plots" + s + date_hold_ns +'_PBP_'+ DMSPType2 + '_PF' + s +  'Pass' + i[1:3] + hemi + '.png'
                
            plt.title(titlename,pad = 10)
            
                
            # Increase figure size
            fig0.set_size_inches(10, 7)
            
            # Save figure
            plt.savefig(savePath, dpi = 100)
            
            # Close figure
            plt.close()
            
        #%% Part X_II: Plotting Magnetic field vecotrs ========================
            if settings['plotMF'] == 1:
                # Define indicies for the magnetic field
                MFEW_idx = val_pos[9]
                MFNS_idx = val_pos[10]
                
                # Define componenets of magnetic field
                MFNS = DataArr_hold[:,MFNS_idx]
                MFEW = DataArr_hold[:,MFEW_idx]
                
                # Define figures for North and South pole
                fig1, ax1 = plt.subplots(1) # North Pole
                
                # Use geospacepy plotting tools to add in the poynting vector
                spt.hairplot2(fig1,ax1,MLAT,MLT,MFNS,MFEW,hemi,settings)
                
                # Define string gap
                s = "\\"
                
                # Determine if this is a pass-by-pass case or hourly
                if parseType == 0:
                    # Title plot
                    if MLAT[0] < 0:
                        titlename = DMSPType + ' Magnetic Field Vector, Southern Hemisphere: \n' + date_hold + ' ' + time_str
                    else:
                        titlename = DMSPType + ' Magnetic Field Vector, Northern Hemisphere: \n' + date_hold + ' ' + time_str
                        
                    # Make save directory for PF
                    if not os.path.isdir('plots/'+date_hold_ns + '_Hourly_' + DMSPType2 + '_MF'):
                        os.makedirs('plots/'+date_hold_ns + '_Hourly_' + DMSPType2 + '_MF')
                        
                    savePath = os.getcwd() + r"\plots" + s + date_hold_ns + '_Hourly_'+ DMSPType2 + '_MF' + s +  'Hour' + str(int(DataArr_hold[0,hour_idx])) + hemi + '.png'
                        
                elif parseType == 1:
                    if MLAT[0] < 0:
                        titlename = DMSPType + ' Magnetic Field Vector, Southern Hemisphere: \n' + date_hold + ' Pass #' + i[1:3] + ' ' +time_str
                    else:
                        titlename = DMSPType + ' Magnetic Field Vector, Northern Hemisphere: \n' + date_hold + ' Pass #' + i[1:3] + ' '+ time_str
                        
                    # Make save directory for PF
                    if not os.path.isdir('plots/'+date_hold_ns + '_PBP_'+ DMSPType2 + '_MF'):
                        os.makedirs('plots/'+date_hold_ns + '_PBP_' + DMSPType2 + '_MF')
                        
                    savePath = os.getcwd() + r"\plots" + s + date_hold_ns +'_PBP_'+ DMSPType2 + '_MF' + s +  'Pass' + i[1:3] + hemi + '.png'
                    
                plt.title(titlename,pad = 10)
                
                    
                # Increase figure size
                fig1.set_size_inches(10, 7)
                
                # Save figure
                plt.savefig(savePath, dpi = 100)
                
                # Close figure
                plt.close()
                
        #%% Part X_III: Plotting Electric field vecotrs =======================
            if settings['plotEF'] == 1:
                
                if settings['plotMF'] == 1:
                    # Define indicies for the magnetic field
                    EFHori_idx = val_pos[11]
                    EFVert_idx = val_pos[12]
                else:
                    # Define indicies for the magnetic field
                    EFHori_idx = val_pos[9]
                    EFVert_idx = val_pos[10]
                
                # Define componenets of magnetic field
                EFVert = DataArr_hold[:,EFVert_idx]
                EFHori = DataArr_hold[:,EFHori_idx]
                
                # Define figures for North and South pole
                fig2, ax2 = plt.subplots(1) # North Pole
                
                # Use geospacepy plotting tools to add in the poynting vector
                spt.hairplot3(fig2,ax2,MLAT,MLT,EFVert,EFHori,hemi,settings)
                
                # Define string gap
                s = "\\"
                
                # Determine if this is a pass-by-pass case or hourly
                if parseType == 0:
                    # Title plot
                    if MLAT[0] < 0:
                        titlename = DMSPType + ' Velocity Vector, Southern Hemisphere: \n' + date_hold + ' ' + time_str
                    else:
                        titlename = DMSPType + ' Velocity Vector, Northern Hemisphere: \n' + date_hold + ' ' + time_str
                        
                    # Make save directory for PF
                    if not os.path.isdir('plots/'+date_hold_ns + '_Hourly_' + DMSPType2 + '_VF'):
                        os.makedirs('plots/'+date_hold_ns + '_Hourly_' + DMSPType2 + '_VF')
                        
                    savePath = os.getcwd() + r"\plots" + s + date_hold_ns + '_Hourly_'+ DMSPType2 + '_VF' + s +  'Hour' + str(int(DataArr_hold[0,hour_idx])) + hemi + '.png'
                        
                elif parseType == 1:
                    if MLAT[0] < 0:
                        titlename = DMSPType + ' Velocity Vector, Southern Hemisphere: \n' + date_hold + ' Pass #' + i[1:3] + ' ' +time_str
                    else:
                        titlename = DMSPType + ' Velocity Vector, Northern Hemisphere: \n' + date_hold + ' Pass #' + i[1:3] + ' '+ time_str
                        
                    # Make save directory for PF
                    if not os.path.isdir('plots/'+date_hold_ns + '_PBP_'+ DMSPType2 + '_VF'):
                        os.makedirs('plots/'+date_hold_ns + '_PBP_' + DMSPType2 + '_VF')
                        
                    savePath = os.getcwd() + r"\plots" + s + date_hold_ns +'_PBP_'+ DMSPType2 + '_VF' + s +  'Pass' + i[1:3] + hemi + '.png'
                    
                plt.title(titlename,pad = 10)
                
                    
                # Increase figure size
                fig2.set_size_inches(10, 7)
                
                # Save figure
                plt.savefig(savePath, dpi = 100)
                
                # Close figure
                plt.close()