# -*- coding: utf-8 -*-
"""
Created on: 10/31/2022

@author: Adam Gourmos
"""
import numpy as np


# Takes an array of passes and sepreates by hemispehre into a dict
def FindPH(arr,MLAT_idx,MLT_idx,GLON_idx):
    # Define empty dictionary and list
    dictionary = {}
    #diff_list = []
    
    # Predefine pass number and index of start of pass
    N_passIdx = 1
    S_passIdx = 1
    #IdxHold = 0
    
    # Define initial list of MLAT and MLON values
    ini_list = arr[:,MLAT_idx]
    
    # Find the distance between adjacent points
    diff_list = abs(np.diff(arr[:,GLON_idx]))
    diff_list2 = abs(np.diff(ini_list))
    
    # Create an empty list to hold the values to append into a dictionary
    idx_hold = []

    # Create swithces turned off
    N_switch = 0
    S_switch = 0

    # Parse through data to find switches in pass and hemisphere
    for idx, val in enumerate(ini_list):   
        # Northern hemisphere
        if np.sign(val) == 1:
            # Empty list into dictionary
            if (idx_hold and S_switch == 1) or (diff_list[idx-1] > 20 and diff_list2[idx-1] < 0.66 and abs(val) < 45):
                # Create array and key for this pass/hemisphere
                KeyName = 'S' + str(S_passIdx)
            
                # Insert dictionary values
                dictionary[KeyName] = arr[idx_hold,:]
                
                # Define new pass number
                S_passIdx += 1
                
                # Turn switch back off
                S_switch = 0
                
                # Empty list
                idx_hold = []

            # Append new index value
            idx_hold.append(idx)
            
            # Turn on switch for this hemisphere
            N_switch = 1
        
        # Southern hemisphere 
        elif np.sign(val) == -1:
            # Empty list into dictionary
            if (idx_hold and N_switch == 1) or (diff_list[idx-1] > 20 and diff_list2[idx-1] < 0.66 and abs(val) < 45):
                # Create array and key for this pass/hemisphere
                KeyName = 'N' + str(N_passIdx)
            
                # Insert dictionary values
                dictionary[KeyName] = arr[idx_hold,:]
                
                # Define new pass number
                N_passIdx += 1
                
                # Turn switch back off
                N_switch = 0
                
                # Empty list
                idx_hold = []

            # Append new index value
            idx_hold.append(idx)
            
            # Turn on switch for this hemisphere
            S_switch = 1
        
    return dictionary