# -*- coding: utf-8 -*-
"""
Created on: 10/31/2022

@author: Adam Gourmos
"""
import numpy as np


# Takes an array of passes and sepreates by hemispehre into a dict
def FindPH(arr,MLAT_idx):
    # Define empty dictionary and list
    dictionary = {}
    #diff_list = []
    
    # Predefine pass number and index of start of pass
    PassIdx = 1
    IdxHold = 0
    
    # Define initial list of MLAT values
    ini_list = arr[:,MLAT_idx]
    
    # Add adjacent values to find switch in hemisphere and pass
    #for x, y in zip(ini_list[0::], ini_list[1::]):
    #    diff_list.append(x+y)
    diff_list = np.diff(np.sign(ini_list))
    
    # Parse through data to find switches in pass and hemisphere
    for idx, val in enumerate(diff_list):
        if val != 0: # Change in pass
            # Determine which hemisphere the previous pass was in
            if ini_list[idx] < 0:
                # Create array and key for this pass/hemisphere
                idx_array = np.arange(IdxHold,idx,1)
                KeyName = 'S' + str(PassIdx)
            
                # Insert dictionary values
                dictionary[KeyName] = arr[idx_array,:]
            
                # Redfine start of new pass
                IdxHold = idx + 1
                
                # Define new pass number
                #PassIdx =+ 1
        
            else: # New Pass
                # Create array and key for this pass/hemisphere
                idx_array = np.arange(IdxHold,idx,1)
                KeyName = 'N' + str(PassIdx)
            
                # Insert dictionary values
                dictionary[KeyName] = arr[idx_array,:]
            
                # Redfine start of new pass
                IdxHold = idx + 1
            
                # Increase pass number
                PassIdx += 1
            
        else:
            continue
    
    return dictionary