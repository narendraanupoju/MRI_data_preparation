# -*- coding: utf-8 -*-
"""
Created on Wed Jan  2 14:10:31 2019

@author: narendra

This is an example code that operates directly for 256*256*X (X is no of slices) 

An other alternative for main() and getListoFFiles() can be replaced by using glob functions.
"""

import os
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

dirName = r"file_path" # directory for mri data

#function to read data from dirName
def FileRead(file_path):
    nii = nib.load(file_path)
    data = nii.get_data()
    #if (np.shape(np.shape(data))[0] == 3): #If channel data not present
     #   data = np.expand_dims(data, 3)
    return data

#function returns a 2 dimensional numpy array from a 3 dimensional data
def Nifti3Dto2D(Nifti3D):
    Nifti3DWOChannel = Nifti3D#[:,:,:,0] #Considering there is only one channel info
    Nifti2D = Nifti3DWOChannel.reshape(np.shape(Nifti3DWOChannel)[0], np.shape(Nifti3DWOChannel)[1] * np.shape(Nifti3DWOChannel)[2])
    return Nifti2D

#function returns a 1 dimensional numpy array from a 2 dimensional array
def Nifti2Dto1D(Nifti2D):
    Nifti1D = Nifti2D.reshape(np.shape(Nifti2D)[0] * np.shape(Nifti2D)[1])
    return Nifti1D

#reshapes a 1 dimensional array to 2 dimensional data
def Nifti1Dto2D(Nifti1D, height):     # height represents the height of image to be reconstructed from 1d array
    Nifti2D = Nifti1D.reshape(height,int(np.shape(Nifti1D)[0]/height))
    return Nifti2D

#reshapes 2 dimensional array to 3 dimensional data
def Nifti2Dto3D(Nifti2D):
    Nifti3DWOChannel = Nifti2D.reshape(np.shape(Nifti2D)[0],np.shape(Nifti2D)[0],np.shape(Nifti2D)[1]//np.shape(Nifti2D)[0])
    #Nifti3D = np.expand_dims(Nifti3DWOChannel, 3)
    return Nifti3DWOChannel

#normalize data between o-1
def normalize(x):
    min_val = np.min(x)
    max_val = np.max(x)
    x = (x-min_val) / (max_val-min_val)
    return x

# to copy data to local storage
def FileSave(data, file_path):
    nii = nib.Nifti1Image(data, np.eye(4))
    nib.save(nii, file_path)

# returns list of files from the given dirName
def getListOfFiles(dirName):
    # creating a list of file and sub directories 
    listOfFile = os.listdir(dirName)
    allFiles = []
    # Iterate over entries
    for entry in listOfFile:
        # Creating full path
        fullPath = os.path.join(dirName, entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
    return allFiles

# takes list of files and creates 1 dimension and 2 dimension data from MR data
def main():
    listOfFiles = getListOfFiles(dirName)
    twod_data = []# to save two dimensional data
    oned_data = []
    listOfFiles = []
    for (dirpath, dirnames, filenames) in os.walk(dirName):
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]
       # listOfFiles_under.append(listOfFiles_under)
        #print(listOfFiles_under)
    for element in listOfFiles:
        print(element)
        red_files = FileRead(element)
        twod_array = Nifti3Dto2D(red_files)
        twod_data.append(twod_array)
        #print(twod_unsam)
        oned_array= Nifti2Dto1D(twod_array)
        oned_data.append(oned_array)
    oned_data = np.asarray(oned_data, dtype=np.float64, order='C')
    twod_data = np.asarray(twod_data, dtype=np.float64, order='C')
    return oned_data, twod_data

oned_data, twod_data = main()
#for visualization
data_vis = Nifti2Dto3D(Nifti1Dto2D(oned_data[0,:], 256))
#plt.imshow(data_vis[20,:,:], cmap='gray')
plt.imshow(data_vis[:,:,20], cmap='gray')
