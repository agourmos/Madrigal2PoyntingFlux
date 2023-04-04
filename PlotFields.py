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
import sys
import numpy as np
import matplotlib.pyplot as plt
import functions.satplottools2 as spt
from functions.FindHourly import FindHourly
from functions.FindPH import FindPH
from functions.FindIDX import FindIDX


def PlotFields(settings):
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
    GLON_idx = 8
    
    # If plotting total plots over multiple days, define plots
    if settings['plotTotalPF'] == 1:
        # Define figure 4 outside of the loop (important)
        figN, axN = plt.subplots(44)
        figS, axS = plt.subplots(55)
        
        # Define switch to turn off after defining the first plot for ax4
        ax4switchN = 1
        ax4switchS = 1    
                       
    # For each file in reduced files
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
        try:
            # Find the maximum and minimum bounds values to deteremine colorbar bounds
            bounds = [np.nanmin(DataArr[:,poy_idx]),np.nanmax(DataArr[:,poy_idx])]
        except ValueError:
            sys.exit()
            
        # Redefine the bounds if the user specifically defines them
        if boundsType == 2:
            bounds = settings['bounds']
        
        # Insert bounds into dictionary to pass through function
        boundsDict = {'boundsType':boundsType,'bounds':bounds}
        
        if parseType == 0:
            # Use function to seperate data into hourly and hemisphere dictionary values
            Dict = FindHourly(DataArr[1:-3,:],hour_idx,MLAT_idx)
        elif parseType == 1:
            # Use function to seperate data into pass-by-pass dictionary values
            Dict = FindPH(DataArr[1:-3,:],MLAT_idx,MLT_idx,GLON_idx)
            
        # Define the date
        date_hold_ns = str(int(DataArr[0,0]))+ str(int(DataArr[0,1])) + str(int(DataArr[0,2]))
        
        # For debugging purposes
        #print(date_hold_ns)
            
        # If plotting total plots over a single day
        if settings['plotTotalPF'] == 2:
            # Define figure number based on date
            numN = int(date_hold_ns + '0')
            numS = int(date_hold_ns + '1')
            
            # Define figure outside of the loop (important)
            figN = plt.figure(numN)
            figS = plt.figure(numS)
            
            # Define axises
            axN = figN.add_subplot(111)
            axS = figS.add_subplot(111)
                
            # Define switch to turn off after defining the first plot for ax4
            ax4switchN = 1
            ax4switchS = 1 
            
        #%% PART F: Data conversion and definition
        # For each hour and hemisphere, plot data
        for i in Dict:
            # For debugging purposes
            #print(i)
            
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
            if  settings['plotPF'] == 1:
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
                        
                    savePath = os.getcwd() + r"\plots" + s + date_hold_ns + '_Hourly_'+ DMSPType2 + '_PF' + s +  'Hour' + str(int(DataArr_hold[0,hour_idx])) + hemi + '.jpg'
                        
                elif parseType == 1:
                    if MLAT[0] < 0:
                        titlename = DMSPType + ' Poynting Flux Along Path, Southern Hemisphere: \n' + date_hold + ' Pass #' + i[1:3] + ' ' +time_str
                    else:
                        titlename = DMSPType + ' Poynting Flux Along Path, Northern Hemisphere: \n' + date_hold + ' Pass #' + i[1:3] + ' '+ time_str
                        
                    # Make save directory for PF
                    if not os.path.isdir('plots/'+date_hold_ns + '_PBP_'+ DMSPType2 + '_PF'):
                        os.makedirs('plots/'+date_hold_ns + '_PBP_' + DMSPType2 + '_PF')
                        
                    savePath = os.getcwd() + r"\plots" + s + date_hold_ns +'_PBP_'+ DMSPType2 + '_PF' + s +  'Pass' + i[1:3] + hemi + '.jpg'
                    
                plt.title(titlename,pad = 10)
                
                    
                # Increase figure size
                fig0.set_size_inches(10, 7)
                
                # Save figure
                plt.savefig(savePath, dpi = 100)
                
                # Close figure
                plt.close()
            
        #%% Part X-II: Plotting Magnetic field vecotrs ========================
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
                        
                    savePath = os.getcwd() + r"\plots" + s + date_hold_ns + '_Hourly_'+ DMSPType2 + '_MF' + s +  'Hour' + str(int(DataArr_hold[0,hour_idx])) + hemi + '.jpg'
                        
                elif parseType == 1:
                    if MLAT[0] < 0:
                        titlename = DMSPType + ' Magnetic Field Vector, Southern Hemisphere: \n' + date_hold + ' Pass #' + i[1:3] + ' ' +time_str
                    else:
                        titlename = DMSPType + ' Magnetic Field Vector, Northern Hemisphere: \n' + date_hold + ' Pass #' + i[1:3] + ' '+ time_str
                        
                    # Make save directory for PF
                    if not os.path.isdir('plots/'+date_hold_ns + '_PBP_'+ DMSPType2 + '_MF'):
                        os.makedirs('plots/'+date_hold_ns + '_PBP_' + DMSPType2 + '_MF')
                        
                    savePath = os.getcwd() + r"\plots" + s + date_hold_ns +'_PBP_'+ DMSPType2 + '_MF' + s +  'Pass' + i[1:3] + hemi + '.jpg'
                    
                plt.title(titlename,pad = 10)             
                    
                # Increase figure size
                fig1.set_size_inches(10, 7)
                
                # Save figure
                plt.savefig(savePath, dpi = 100)
                
                # Close figure
                plt.close()
                
        #%% Part X-III: Plotting velocity field vecotrs =======================
            if settings['plotVF'] == 1:
                
                if settings['plotMF'] == 1:
                    # Define indicies for the velocity field
                    VFHori_idx = val_pos[11]
                    VFVert_idx = val_pos[12]
                else:
                    # Define indicies for the velocity field
                    VFHori_idx = val_pos[9]
                    VFVert_idx = val_pos[10]
                
                # Define componenets of magnetic field
                VFVert = DataArr_hold[:,VFVert_idx]
                VFHori = DataArr_hold[:,VFHori_idx]
                
                # Define figures for North and South pole
                fig2, ax2 = plt.subplots(1) # North Pole
                
                # Use geospacepy plotting tools to add in the poynting vector
                spt.hairplot3(fig2,ax2,MLAT,MLT,VFVert,VFHori,hemi,settings)
                
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
                        
                    savePath = os.getcwd() + r"\plots" + s + date_hold_ns + '_Hourly_'+ DMSPType2 + '_VF' + s +  'Hour' + str(int(DataArr_hold[0,hour_idx])) + hemi + '.jpg'
                        
                elif parseType == 1:
                    if MLAT[0] < 0:
                        titlename = DMSPType + ' Velocity Vector, Southern Hemisphere: \n' + date_hold + ' Pass #' + i[1:3] + ' ' +time_str
                    else:
                        titlename = DMSPType + ' Velocity Vector, Northern Hemisphere: \n' + date_hold + ' Pass #' + i[1:3] + ' '+ time_str
                        
                    # Make save directory for PF
                    if not os.path.isdir('plots/'+date_hold_ns + '_PBP_'+ DMSPType2 + '_VF'):
                        os.makedirs('plots/'+date_hold_ns + '_PBP_' + DMSPType2 + '_VF')
                        
                    savePath = os.getcwd() + r"\plots" + s + date_hold_ns +'_PBP_'+ DMSPType2 + '_VF' + s +  'Pass' + i[1:3] + hemi + '.jpg'
                    
                plt.title(titlename,pad = 10)
                
                    
                # Increase figure size
                fig2.set_size_inches(10, 7)
                
                # Save figure
                plt.savefig(savePath, dpi = 100)
                
                # Close figure
                plt.close()
                
        #%% Part X-IV: Plotting electric field vecotrs =======================
            if settings['plotEF'] == 1:
                
                if settings['plotMF'] == 1 and settings['plotVF'] == 1:
                    # Define indicies for the electric field
                    EFHori_idx = val_pos[13]
                    EFVert_idx = val_pos[14]
                    
                elif settings['plotMF'] == 1 or settings['plotVF'] == 1:
                    # Define indicies for the electric field
                    EFHori_idx = val_pos[11]
                    EFVert_idx = val_pos[12]
                    
                else:
                    # Define indicies for the electric field
                    EFHori_idx = val_pos[9]
                    EFVert_idx = val_pos[10]
                
                # Define componenets of magnetic field
                EFVert = DataArr_hold[:,EFHori_idx]
                EFHori = DataArr_hold[:,EFVert_idx]
                
                # Define figures for North and South pole
                fig3, ax3 = plt.subplots(1) # North Pole
                
                # Use geospacepy plotting tools to add in the poynting vector
                spt.hairplot4(fig3,ax3,MLAT,MLT,EFVert,EFHori,hemi,settings)
                
                # Determine if this is a pass-by-pass case or hourly
                if parseType == 0:
                    # Title plot
                    if MLAT[0] < 0:
                        titlename = DMSPType + ' Electric Field Vector, Southern Hemisphere: \n' + date_hold + ' ' + time_str
                    else:
                        titlename = DMSPType + ' Electric Field Vector, Northern Hemisphere: \n' + date_hold + ' ' + time_str
                        
                    # Make save directory for PF
                    if not os.path.isdir('plots/'+date_hold_ns + '_Hourly_' + DMSPType2 + '_EF'):
                        os.makedirs('plots/'+date_hold_ns + '_Hourly_' + DMSPType2 + '_EF')
                        
                    savePath = os.getcwd() + r"\plots" + s + date_hold_ns + '_Hourly_'+ DMSPType2 + '_EF' + s +  'Hour' + str(int(DataArr_hold[0,hour_idx])) + hemi + '.jpg'
                        
                elif parseType == 1:
                    if MLAT[0] < 0:
                        titlename = DMSPType + ' Electric Field Vector, Southern Hemisphere: \n' + date_hold + ' Pass #' + i[1:3] + ' ' +time_str
                    else:
                        titlename = DMSPType + ' Electric Field Vector, Northern Hemisphere: \n' + date_hold + ' Pass #' + i[1:3] + ' '+ time_str
                        
                    # Make save directory for PF
                    if not os.path.isdir('plots/'+date_hold_ns + '_PBP_'+ DMSPType2 + '_EF'):
                        os.makedirs('plots/'+date_hold_ns + '_PBP_' + DMSPType2 + '_EF')
                        
                    savePath = os.getcwd() + r"\plots" + s + date_hold_ns +'_PBP_'+ DMSPType2 + '_EF' + s +  'Pass' + i[1:3] + hemi + '.jpg'
                    
                plt.title(titlename,pad = 10)
                
                    
                # Increase figure size
                fig3.set_size_inches(10, 7)
                
                # Save figure
                plt.savefig(savePath, dpi = 100)
                
                # Close figure
                plt.close()
                
        #%% Part X-IV: Plotting all paths for PF onto one plot ================
            if settings['plotTotalPF'] == 1 or settings['plotTotalPF'] == 2:
                # Make save directory for PF
                if not os.path.isdir(r"plots\TotalPlots"):
                    os.makedirs(r"plots\TotalPlots")
                
                # Check to see if it is a requested pass
                if sum([i == j for j in settings['passes']]) == 1 or not settings['passes']:
                    if MLAT[0] > 0:
                        # Use geospacepy plotting tools to add in the poynting vector
                        axN, ax4switchN = spt.hairplotT(figN,axN,MLAT,MLT,poy,hemi,boundsDict,settings,ax4switchN)
                        
                        # Define title name based on hemisphere and type of total plot
                        if settings['plotTotalPF'] == 1:
                            titlenameN = 'All Dates Plotted'
                        else:
                            titlenameN = 'Northern Hemisphere, All Passes: \n' + date_hold
                            
                    else:
                        axS, ax4switchS = spt.hairplotT(figS,axS,MLAT,MLT,poy,hemi,boundsDict,settings,ax4switchS)
                        
                        # Define title name based on hemisphere and type of total plot
                        if settings['plotTotalPF'] == 1:
                            titlenameS = 'All Dates Plotted'
                        else:
                            titlenameS = 'Southern Hemisphere, All Passes: \n' + date_hold 
        
        if settings['plotTotalPF'] == 2:
            # Set Northern figure
            plt.figure(figN)                    
                            
            # Save file for this day and hemisphere                 
            savePath = os.getcwd() + r"\plots" + r"\TotalPlots" + r"\TP_" + date_hold_ns + 'N.jpg'
            
            # Insert title name
            plt.title(titlenameN,pad = 10)               
                                            
            # Increase figure size
            figN.set_size_inches(7, 5)
                                        
            # Save figure
            plt.savefig(savePath, dpi = 1200)
                                        
            # Close figure
            #plt.close()
        
            # Set Southern figure
            plt.figure(figS)  
                
            # Save file for this day and hemisphere                 
            savePath = os.getcwd() + r"\plots" + r"\TotalPlots" + r"\TP_" + date_hold_ns + 'S.jpg'
                                     
            # Insert title name
            plt.title(titlenameS,pad = 10)               
                                                
            # Increase figure size
            figS.set_size_inches(7, 5)
                                            
            # Save figure
            plt.savefig(savePath, dpi = 1200)
                                            
            # Close figure
            #plt.close()
                
    # Save total plots for all days 
    if settings['plotTotalPF'] == 1:
        # Create save path name                    
        savePathN = os.getcwd() + r"\plots" + r"\TotalPlots" + r"\TP_AllDates_N.jpg"
             
        # Insert title name
        plt.title(titlename,pad = 10)               
                            
        # Increase figure size
        figN.set_size_inches(7, 5)
                    
        # Save figure
        plt.savefig(savePathN, dpi = 1200)
                    
        # Close figure
        plt.close()
            
        # Create save path name                    
        savePathS = os.getcwd() + r"\plots" + r"\TotalPlots" + r"\TP_AllDates_S.jpg"
             
        # Insert title name
        plt.title(titlename,pad = 10)               
                            
        # Increase figure size
        figS.set_size_inches(7, 5)
                    
        # Save figure
        plt.savefig(savePathS, dpi = 1200)
                    
        # Close figure
        plt.close()