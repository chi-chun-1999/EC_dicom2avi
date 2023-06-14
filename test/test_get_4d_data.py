#%%
import os 
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import pydicom
import cv2 as cv
import numpy as np
#import SimpleITK as sitk
import matplotlib.pyplot as plt
from typing import Type
from image_process import getRgbArray
from image_process import array2avi,avi2array
import glob
#%%
data_dir = '../../dataset/test/H/GEMS_IMG/2020_NOV/18/__174122/*'

print(glob.glob(data_dir))
dicom_files = glob.glob(data_dir)

#%%

files_4d = []
for f in dicom_files:
    dcm = pydicom.dcmread(f)
    array_data = dcm.pixel_array
    if array_data.ndim == 4:
        #head,file_name = os.path.split(f)
        files_4d.append(f)


print(files_4d)

# %%
