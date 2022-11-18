# -*- coding: utf-8 -*-

"""
Title: init.py

Created on Mon Oct 24 13:16:06 2022

@author: Adam Gourmos

The purpose of this program is to take dwonloaded data from Madrigal using FTP 
and reduce the data down. From that data, the program will then plot the 
poynting flux (PF) as a function of geographic coordinates or magnetic 
coordiantes.

How to use:
    1) Initialize all user settings in initSettings.py
    2) Run this script

This is a flow down of the programs scripts and functions
    - init.py
        -> initSettings.py
        -> MadReducPF.py
        -> PlotPF.py
            -> FindHourly.py
            -> FindPH.py
            -> satplottools2.py
            

** Notes before use:
    -

"""
from initSettings import initSettings
from functions.MadReducPF import MadReducPF
from functions.PlotPF import PlotPF

#%% Section A -----------------------------------------------------------------
# Establish settings variables to input into other functions
#------------------------------------------------------------------------------

# Define program parameters
settings = initSettings()

#%% Section B -----------------------------------------------------------------
# Reduce file based on user defined parameters
#------------------------------------------------------------------------------

# Reduce file 
MadReducPF(settings)

#%% Section C -----------------------------------------------------------------
# Plot and save data based on user provided parameters
#------------------------------------------------------------------------------

# Plot and save plots
PlotPF(settings)