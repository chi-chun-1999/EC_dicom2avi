#%%
import os 
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from src.image_process.feature import *
from src.image_process.frame import *
import pydicom
import cv2 as cv
import numpy as np
#import SimpleITK as sitk
import matplotlib.pyplot as plt
from typing import Type
#from image_process import *

from src.show.matplot_show import matplot_show_video,show_R_wave_place

import glob
#%%
data_dir = '../../dataset/test/H/GEMS_IMG/2020_NOV/18/__174122/*'

print(glob.glob(data_dir))
dicom_files = glob.glob(data_dir)

files_4d = []
for f in dicom_files:
    dcm = pydicom.dcmread(f)
    array_data = dcm.pixel_array
    if array_data.ndim == 4:
        #head,file_name = os.path.split(f)
        files_4d.append(f)

#%%
dcm = pydicom.dcmread(files_4d[1])
#video_array = avi2array(video_name)
#npy_array = np.load('./test.npz.npy')

#video_array_rgb = cv.cvtColor(video_array[0],cv.COLOR_BGR2RGB)


dcm_rgb_array =  getRgbArray(dcm)

dcm_bgr_array = dcm_rgb_array[:,:,:,::-1]



#plt.imshow(video_array[1,350:,0:318,:])


ecg_roi =getECGRoi_FixSize(dcm_bgr_array,[350,434,0,400]) 


plt.figure()
plt.imshow(ecg_roi[0,:,:,::-1])


red_extractor =  RedExtractor()
red_mask = red_extractor.process(ecg_roi)
red_argwhere = np.argwhere(red_mask)

r_wave_extractor = RWaveExtractor_IntervalMax(gmm_scale=25)
r_wave_location = r_wave_extractor.process(ecg_roi)
show_R_wave_place(ecg_roi,r_wave_location)


match_frame =[]
for i in r_wave_location:
    red_match_r_wave = red_argwhere[red_argwhere[:,2]==i[0]]
    bias = 0 
    while(red_match_r_wave.size==0):
        bias+=1
        red_match_r_wave = red_argwhere[red_argwhere[:,2]==i[0]-bias]
        if red_match_r_wave.size!=0:
            break
        
        red_match_r_wave = red_argwhere[red_argwhere[:,2]==i[0]+bias]
    
    match_frame.append(red_match_r_wave[0,0])

print(match_frame) 
    
        




# %%
