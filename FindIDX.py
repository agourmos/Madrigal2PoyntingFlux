# -*- coding: utf-8 -*-
"""
Title: FindIDX.py

Created on Mon Oct 24 13:16:06 2022

@author: Adam Gourmos

The purpose of this script is to find the index of specific variables in order
to plot the poynting flux. This is becasue it may be different each time based
on what the user decides.

** Notes before use:
    -

"""
import numpy as np
import sys

def FindIDX(settings):
    # Define user option
    #user_opt = 0
    
    # Define corrected parameter vector positions
    param_idxs =np.asarray(np.where(np.array(settings['parameters_vec']) == 1))[0].astype(int)
    
    # Define chosen parameter names
    chosen_parameter_names = []
    [chosen_parameter_names.append(settings['parameter_names'][i]) for i in param_idxs]
    
    # Define values for plotting
    plot_vals = ['YEAR','MONTH','DAY','HOUR','MIN','SEC','MLAT','MLT','GDLAT',
                 'GLON','POYNTING_FLUX','DIFF_B_FOR','DIFF_B_PERP_L',
                 'ION_V_SAT_FOR','ION_V_SAT_LEFT']
    
    # Vector representing values that were found in the search process
    vals_switch = np.ones(15)
    
    # Define empty vector for value positions
    vals_pos = np.nan*np.ones(15)
    
    # Search parameters for position of important variables
    for idx,param in enumerate(plot_vals):
        try:
            # Value was found, save index
            vals_pos[idx] = chosen_parameter_names.index(param)
        except ValueError:
            # Value not found, set vector value to not found
            vals_switch[idx] = 0
            
    # Make sure that the values that are chosen will allow for plotting
    if sum(vals_switch[0:6]) == 6: # Check date and time
        # All good, check for LAT/LON or MLAT/MLT
        
        if sum(vals_switch[6:8]) == 2 or sum(vals_switch[8:10]) == 2:
            # All good, check to see if both options were given and ask user
            
            if sum(vals_switch[6:8]) == 2 and sum(vals_switch[8:10]) == 2:
                # Define MLAT and MLT as default parameters
                # Set LAT/LON swithces to 0
                vals_switch[8:10] = 0
                
                # Ask user for parameter setup
                #while user_opt == 0:
                    # Ask user
                    #user_choice = input('Would you like to plot using LAT/LON '+
                    #                '(type 1) or MLAT/MLT (type 2)?:\n')
                    
                    #if user_choice == 1:
                        # Set MLAT/MLT swithces to 0
                        #vals_switch[6:8] = 0
                        
                        # Turn off while loop
                        #user_opt = 1
                        
                    #elif int(user_choice) == 2:
                        # Set LAT/LON swithces to 0
                        #vals_switch[8:10] = 0
                        
                        # Turn off while loop
                        #user_opt = 1
                        
                    #else:
                        #print('Invalid option chocen. Please type either 1 or 2.\n')    
                        
            # Check to see if magnetic values were given for plotting
            if settings['plotMF'] == 1 and not sum(vals_switch[11:13]) == 2:
                print('PlotError: Magnetic flux component(s) not given for plotting.')
                sys.exit()
            # If values are turned on, turn them off. Helps with indexing
            elif settings['plotMF'] == 0 and sum(vals_switch[11:13]) == 2:
                vals_switch[11:13] = 0
                
                
            # Check to see if magnetic values were given for plotting
            if settings['plotEF'] == 1 and not sum(vals_switch[13:15]) == 2:
                print('PlotError: Magnetic flux component(s) not given for plotting.')
                sys.exit()
            # If values are turned on, turn them off. Helps with indexing
            elif settings['plotEF'] == 0 and sum(vals_switch[13:15]) == 2:
                vals_switch[11:13] = 0
                        
            # Check to see if poynting flux is given
            if vals_switch[10] == 1:
                # All good, reduce and ouput positional values
                final_idxs = np.asarray(np.where(vals_switch == 1))[0].astype(int)
                
                final_pos = []
                [final_pos.append(int(vals_pos[i])) for i in final_idxs]
                return final_pos
            
            else:
                # No poynting flux given
                print('PlotError: Poynting flux was not found in the data set.')
                sys.exit()
            
            
        else:
            # Missing date or time values
            print('PlotError: No MLT/MLAT or LAT/LON values were found in the ' + 
                  'reduced data.')
            sys.exit() 
    else:
        # Missing date or time values
        print('PlotError: Date or time values are missing. This is needed ' + 
              'for parsing.')
        sys.exit()
        
            