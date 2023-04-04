                    # -*- coding: utf-8 -*-
"""
Title: MadReducPF.py

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
#%% Packages and modules
import os
import sys
import tarfile
import gzip
import shutil
import numpy as np

def MadReducPF(settings):
    #%% Define variables
    parameters_vec  = settings['parameters_vec']
    parameter_names = settings['parameter_names']
    parameter_params= settings['parameter_params']
    zipOpt          = settings['zipOpt']
    filesDir        = settings['filesDir']
    
    #%% Begin data extracction
    
    # Convert parameters_vec to a boolean for postional comparison
    parameters_vec_bool = [str(item) for item in  [bool(item) for item in parameters_vec]]
    
    # Extract the parameter_title and parameters_format
    parameter_title = ' '.join([x for x, y in zip(parameter_names, parameters_vec_bool) if y == 'True'])+'\n'
    parameter_format = ' '.join([x for x, y in zip(parameter_params, parameters_vec_bool) if y == 'True']) +'\n'
    
    # Determine if files need to be extracted from zip.
    if zipOpt == 1: 
        # Define files in the specified directory
        dir_list = [file for file in os.listdir(filesDir) if os.path.isfile(os.path.join(filesDir, file))]
        
        # Create a directory to unzip directories to. This allows for easier clean up
        if not os.path.exists(os.path.join(filesDir,'DataHold')):
            os.mkdir(os.path.join(filesDir,'DataHold'))
        
        # Create a directory to unzip files to
        if not os.path.exists(os.path.join(filesDir,'DataTransfer')):
            os.mkdir(os.path.join(filesDir,'DataTransfer'))
        
        # Extract all files from each zip file. NOTE: This requires two extractions
        for zfile in dir_list:
            # Define full zip file path
            zfile_dir = os.path.join(filesDir,zfile)
            
            # Extract folder path to current directory
            with tarfile.open(zfile_dir) as tarfiledir:        
                try:
                    # Extract data to DataHold directory
                    tarfiledir.extractall(os.path.join(filesDir,'DataHold'))
                    
                except tarfile.ReadError or EOFError: 
                    # This is because of a bad ending in tarfiles after extraction
                    pass
                
            # Extract data that are also zipped
            files_list = os.listdir(os.path.join(filesDir,'DataHold','opt','cedar3','experiments','stage'))
            
            # For each file, extract to DataTransfer
            for file in files_list:
                # Define full directory name
                dirnamehold = os.path.join(filesDir,'DataHold','opt','cedar3','experiments','stage',file)
                
                # Define new file directory name
                direnewhold = os.path.join(filesDir,'DataTransfer',file[:-7]+'.txt')
                
                # Open given file
                with gzip.open(dirnamehold,'rt') as zipref:
                    # Save .txt file to DataTransfer
                    with open(direnewhold,'w') as f:
                        try:
                            # Save file
                            f.write(zipref.read())
                        except EOFError: # This is becasue of an exexpected end
                            print('Unable to extract ' + file + '\n')
                            continue
                        
                        # Close file
                        f.close()
                        
                    # Close gzip file
                    zipref.close()
                    
            # Delete the opt directory created from origional extraction
            shutil.rmtree(os.path.join(filesDir,'DataHold','opt'))
        
        # Delete empty directory
        os.rmdir(os.path.join(filesDir,'DataHold'))
                    
    # Determine the data location for extraction
    if zipOpt == 1: 
        files_in = os.listdir(os.path.join(filesDir,'DataTransfer'))
        files_in_dir = [os.path.join(filesDir,'DataTransfer',val) for val in os.listdir(os.path.join(filesDir,'DataTransfer'))]
    elif zipOpt == 0:
        files_in = os.listdir(filesDir)
        files_in_dir = [os.path.join(filesDir,val) for val in os.listdir(filesDir)]
    else:
        print('zipOpt value chosen is an invalid option.\n')
        sys.exit()
        
    #%% Begin saving data to a new file
     
    # Determine if data is already reduced
    if settings['reduced'] == 0:
        # Create new directory to save files to if it doesn't exists already
        if not os.path.exists(os.path.join(filesDir,'ReducedData')):
            os.mkdir(os.path.join(filesDir,'ReducedData'))
            
        # Given this directory and user chosen params, reduce file and save to ReducedData
        for idx,file in enumerate(files_in):
            # Define empty dataArr
            dataArr = np.empty([0,np.sum(parameters_vec)])
            
            # Define new data filename
            NewDataFilename = file[:-4] + '_Reduced.txt'
            
            # Define new data filename directory name
            NewDataFile = os.path.join(filesDir,'ReducedData',NewDataFilename)
            
            # Begin data extraction
            with open(files_in_dir[idx]) as data:
                DataList = data.readlines()
                
                # Convert the list into an array
                for line in DataList:
                    # Find the first line
                    try:
                       # line = line.replace(" ", ",")
                        lineHold = np.asarray([float(i) for i in line.strip().split()])
                        if line == '\n':
                            continue
                    except ValueError:
                        continue
                    else:
                        # Find the values to use
                        lineHold = [x for x, y in zip(lineHold, parameters_vec_bool) if y == 'True']
                        # Extract relevant data
                        dataArr = np.vstack([dataArr,lineHold])
                        
            # Begin saving data to a new .txt files
            # Define tempfile name
            fileHolder = open(NewDataFile, "w")
            
            # Save header
            fileHolder.write(parameter_title)
            
            # Save each row
            for row in dataArr:
                # Convert this rows values into reduced forms
                stringHold = parameter_format % tuple(row)
                
                # Save line to file
                fileHolder.write(stringHold)
                
            # Close file
            fileHolder.close()
            
        # Delete dataTransfer directory if it exists
        if os.path.exists(os.path.join(filesDir,'DataTransfer')):
            shutil.rmtree(os.path.join(filesDir,'DataTransfer'))
            
                
            