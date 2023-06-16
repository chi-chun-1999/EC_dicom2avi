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
dcm = pydicom.dcmread(files_4d[11])
#video_array = avi2array(video_name)
#npy_array = np.load('./test.npz.npy')

#video_array_rgb = cv.cvtColor(video_array[0],cv.COLOR_BGR2RGB)


dcm_rgb_array =  getRgbArray(dcm)

dcm_bgr_array = dcm_rgb_array[:,:,:,::-1]



#plt.imshow(video_array[1,350:,0:318,:])


ecg_roi =getECGRoi_FixSize(dcm_bgr_array,[350,434,0,400]) 

plt.figure()
plt.imshow(ecg_roi[0,:,:,::-1])

r_wave_extractor = RWaveExtractor_IntervalMax(gmm_scale=25)
r_wave_location = r_wave_extractor.process(ecg_roi)
#
#r_wave_extractor._extract_data = ecg_roi
#
#r_wave_extractor._get_ecg_info()
#
#r_wave_extractor._get_two_yello_line_location()
#
#template_mask = r_wave_extractor._generate_template_mask()
#
#match = r_wave_extractor._template_match(template_mask)
#
#R_dist_prob = r_wave_extractor._generate_gmm()
#
#combine_mask = r_wave_extractor._combine_match_mat_and_R_dist_prob(match=match,R_dist_prob=R_dist_prob)
#
#plt.figure()
#plt.imshow(combine_mask)
#plt.show()
#
#rr_interval_dist = r_wave_extractor._second_line-r_wave_extractor._first_line
#
#r_wave_extractor._probability_center_list.sort()
#
#r_wave_location_dict = {}
#
#
#for i in r_wave_extractor._probability_center_list:
#    
#    if i <0:
#        i = 0
#    if i>r_wave_extractor._first_line:
#        break
#    dectect_roi_y_start = r_wave_extractor._ecg_y_axis_center-r_wave_extractor._ecg_y_range_upper_bound
#    dectect_roi_y_end = r_wave_extractor._ecg_y_axis_center+r_wave_extractor._ecg_y_range_upper_bound
#
#    dectect_roi_x_start = i-int(rr_interval_dist/2)
#    dectect_roi_x_end = i+int(rr_interval_dist/2)
#
#    if dectect_roi_x_start<0:
#        dectect_roi_x_start = 0
#
#    if dectect_roi_x_end>combine_mask.shape[1]:
#        dectect_roi_x_end = combine_mask.shape[1]
#
#
#    detect_interval = combine_mask[dectect_roi_y_start:dectect_roi_y_end,dectect_roi_x_start:dectect_roi_x_end]
#    
#    argmax_detect_interval = np.unravel_index(np.argmax(detect_interval),detect_interval.shape)
#
#    if detect_interval[argmax_detect_interval]>=0.01:
#        
#        tmp_r_wave_x_loaction = dectect_roi_x_start + argmax_detect_interval[1]
#        tmp_r_wave_y_loaction = dectect_roi_y_start + argmax_detect_interval[0]
#
#        #print('-->',tmp_r_wave_x_loaction)
#        #print('-->',tmp_r_wave_y_loaction)
#        r_wave_location_dict[tmp_r_wave_x_loaction]=tmp_r_wave_y_loaction
#
#    #plt.figure()
#    #plt.imshow(detect_interval)
#    #plt.show()
#
#r_wave_location_dict[r_wave_extractor._second_line] = list(r_wave_location_dict.values())[-1]
#
##print(r_wave_x_loactions)
#print(r_wave_location_dict)
#
#r_wave_location = [(k,v) for k,v in r_wave_location_dict.items()]
#
#
#show_R_wave_place(ecg_roi,r_wave_location)

#print(r_wave_location)


show_R_wave_place(ecg_roi,r_wave_location)
# %%
