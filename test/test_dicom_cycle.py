import os 
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import pydicom
import cv2 as cv
import numpy as np
#import SimpleITK as sitk
import matplotlib.pyplot as plt
from typing import Type
from image_process import *

from show.matplot_show import matplot_show_video


data_path = '../../dataset/test/H/GEMS_IMG/2020_NOV/18/__174122/KBIHSR0C'

dcm = pydicom.dcmread(data_path)
#video_array = avi2array(video_name)
#npy_array = np.load('./test.npz.npy')

#video_array_rgb = cv.cvtColor(video_array[0],cv.COLOR_BGR2RGB)


dcm_rgb_array =  getRgbArray(dcm)

dcm_bgr_array = dcm_rgb_array[:,:,:,::-1]


ecg_roi =getECGRoi_FixSize(dcm_bgr_array) 

#
rr_interval_extractor = RRIntervalExtractor()
rr_start, rr_end = rr_interval_extractor.process(ecg_roi)

cycle_start = rr_start - int((rr_end-rr_start)/3)
cycle_end = rr_end - int((rr_end-rr_start)/3)

red_extractor = RedExtractor()
red_mask = red_extractor.process(ecg_roi)


matplot_show_video(red_mask)
#matplot_show_video(dcm_bgr_array[cycle_start:cycle_end])




#print(dcm_rgb_array.shape)
#plt.figure()
#plt.imshow(dcm_rgb_array[0])
##plt.figure()
##plt.imshow(video_array_rgb)
##plt.figure()
##plt.imshow(npy_array[0])
#plt.show()