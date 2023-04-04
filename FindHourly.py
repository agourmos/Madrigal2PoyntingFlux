# -*- coding: utf-8 -*-
"""
Created on: 10/31/2022

@author: Adam Gourmos
"""
import numpy as np


# Seperates flight path data by hourly gaps into dictionary keys based on 
# Northern and Southern hemisphere values
def FindHourly(arr,hour_idx,MLAT_idx):
    # Define empty dictionaries
    dictionary = {}
    
    # Define empty lists
    N = []
    S = []
    
    # Define initial list of hour values
    ini_time = arr[:,hour_idx]
    
    
    # Parse through data to find switches in hour
    for idx, val in enumerate(ini_time):
        # Define MLAT
        MLAT = arr[idx,MLAT_idx]
        if MLAT < -39 or MLAT > 39:
            if idx == 0:
                if MLAT > 0:
                    # Insert the first row
                    N.append(arr[idx,:])
                else:
                    S.append(arr[idx,:])
                
            elif val == ini_time[idx-1] and idx != len(ini_time)-1: # N->S
                if MLAT > 0:
                    # add row to list 
                    N.append(arr[idx,:])
                else:
                    # add row to list 
                    S.append(arr[idx,:])
        
            elif val != ini_time[idx-1] or idx == len(ini_time)-1: # New hour
                # Define hour keyname
                KeyNameN = str(int(ini_time[idx-1])) +'N'
                KeyNameS = str(int(ini_time[idx-1])) +'S'
            
                # Insert dictionary values based on whether lists are empty
                if not N:
                    dictionary[KeyNameS] = np.array(S)
                elif not S:
                    dictionary[KeyNameN] = np.array(N)
                else:
                    dictionary[KeyNameN] = np.array(N)
                    dictionary[KeyNameS] = np.array(S)
            
                # redefine lists
                N = []
                S = []
            
        else:
            continue
    
    return dictionary