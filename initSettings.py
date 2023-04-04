# -*- coding: utf-8 -*-
"""
Title: initSettings.py

Created on Mon Oct 24 13:16:06 2022

@author: Adam Gourmos

The purpose of this script is to allow user to initialize variables in 
extracting data and plotting it

- Sections:
    -> Data extraction and reduction
    -> Plot type

** Notes before use:
    -

"""
import os

def initSettings():
    #%% Section B -------------------------------------------------------------
    # Determine what file type is being extracted and what variables will be 
    # saved
    #--------------------------------------------------------------------------
    # Define folder location of all zip file --or-- all files
    filesDir = os.path.join(os.getcwd(),'data')

    # Are the files in the given directory zip-files?
    zipOpt = 1;         # 0 - no, they are .txt (good for dubugging)
                        # 1 - yes (default)
                        
    # Are the files in the given directory already reduced?
    reduced = 0;        # 0 - no (default)
                        # 1 - yes (if already reduced and would just like plots)                  
                    
    # Determine which parameters to extract into a new .txt file

    #                         1 = [on]    ---or---    0 = [off]
    # Always keep on ----------------------------------------------------------
    year            = 1     # Year
    month           = 1     # Month
    day             = 1     # Day
    hour            = 1     # Hour
    minute          = 1     # Minute
    sec             = 1     # Seconds
    # -------------------------------------------------------------------------

    recNO           = 0     #
    kinDAT          = 0     #
    kinST           = 0     #
    UT1_unix        = 0     #
    UT2_unix        = 0     #
    
    # Always keep on ----------------------------------------------------------
    GDALT           = 1     #
    GDLAT           = 1     #
    GLON            = 1     #
    MLAT            = 1     #
    MLT             = 1     #
    # -------------------------------------------------------------------------

    ION_V_SAT_for   = 1     #
    ION_V_SAT_left  = 1     #
    VERT_ION_V_up   = 0     #
    B_for           = 0     #
    B_PERP_left     = 0     #
    B_up            = 0     #
    DIFF_B_for      = 1     #
    DIFF_B_perp_L   = 1     #
    DIFF_B_up       = 0     #
    E_FIELD_ram     = 1     #
    E_FIELD_horiz   = 1     #
    E_up            = 0     #
    Poynting_Flux   = 1     #
    RPA_flag        = 0     #
    IDM_flag        = 0     #
    
    #%% Section C -------------------------------------------------------------
    # Determine how data will be parsed and plotted
    #--------------------------------------------------------------------------
    # Define parseing type (i.e pass-by-pass or hourly)
    parseType = 1; # 0 = Hourly --or-- 1 = pass-by-pass
    
    # Determine whether or not colorbar will have fixed values or not
    boundsType = 2; # 0 = variable, 1 = fixed, 2 = user decided
    
    # IF the above choice is 2, define the bounds you would like to use
    #bounds = [-0.015,0.0]
    bounds = [-0.025,-0.015]
    
    # Determine whether or not to plot poynting flux
    plotPF = 1; # 0 = no/off --or-- 1 = yes/on
    
    # Determine whether or not to plot magnetic field
    plotMF = 0; # 0 = no/off --or-- 1 = yes/on
    
    # Determine whether or not to plot velocity field
    plotVF = 0; # 0 = no/off --or-- 1 = yes/on
    
    # Determine whether or not to plot electric
    plotEF = 0; # 0 = no/off --or-- 1 = yes/on
    
    # Determine whether or not to plot all poynting flux together
    plotTotalPF = 2; # 0 = off 1 = yes all/on --or-- 2 = yes daily/on
    
    # Determine the passes to be used in the plotting (only north for now)
    passes = [];

    
    #%% END OF USER DEFINE PARAMETERS -----------------------------------------
    
    # Define vector continaing user defined parameters
    parameters_vec = [year, month, day, hour, minute, sec, recNO, kinDAT, kinST,
                      UT1_unix, UT2_unix, GDALT, GDLAT, GLON, MLAT, MLT,
                      ION_V_SAT_for, ION_V_SAT_left, VERT_ION_V_up, B_for, 
                      B_PERP_left, B_up, DIFF_B_for, DIFF_B_perp_L, DIFF_B_up,
                      E_FIELD_ram, E_FIELD_horiz, E_up, Poynting_Flux, RPA_flag, 
                      IDM_flag]

    # Define all variable names for printing onto the reduced .txt file
    parameter_names = ['YEAR','MONTH','DAY','HOUR','MIN','SEC','RECNO','KINDAT',
                        'KINST','UT1_UNIX','UT2_UNIX','GDALT','GDLAT','GLON',
                        'MLAT','MLT','ION_V_SAT_FOR','ION_V_SAT_LEFT',
                        'VERT_ION_V_UP','B_FORWARD','B_PERP_LEFT','B_UP',
                        'DIFF_B_FOR','DIFF_B_PERP_L','DIFF_B_UP','E_FIELD_RAM',  
                        'E_FIELD_HORIZ','EU','POYNTING_FLUX','RPA_FLAG_UT',
                        'IDM_FLAG_UT']

    # Define string input value for each value
    parameter_params = ["%.0f" , "%.0f", "%.0f", "%.0f", "%.0f", "%.0f", "%.0f",
                        "%.0f", "%.0f", "%.0f","%.0f", "%.2f", "%.2f", "%.2f", "%.2f",
                        "%.5f", "%.1f", "%.1f","%.1f","%6.5e","%6.5e","%6.5e",
                        "%6.5e","%6.5e","%6.5e","%6.5e","%6.5e","%6.5e","%6.5e",
                        "%.0f","%.0f"]
    
    settings = {"filesDir":filesDir,"zipOpt":zipOpt, "reduced":reduced,
                "parameters_vec":parameters_vec,
                "parameter_names":parameter_names,
                "parameter_params":parameter_params,
                "parseType":parseType,"boundsType":boundsType,
                "plotMF":plotMF,"plotVF":plotVF,"plotEF":plotEF,"plotPF":plotPF,
                "bounds":bounds,"plotTotalPF":plotTotalPF,"passes":passes}
    
    return settings