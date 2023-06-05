import os 
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from image_process import *

import matplotlib.pyplot as plt
from show.matplot_show import matplot_show_video


import cv2 as cv
import numpy as np
import math

file_name = '../data_video/KBIHSR8G.avi'

video_array = avi2array(file_name)
print(video_array.shape)

#plt.imshow(video_array[1,350:,0:318,:])

ecg_roi =getECGRoi_FixSize(video_array) 
red_extractor = RedExtractor()

red_mask = red_extractor.process(ecg_roi)

#red_frames = np.ones(ecg_roi.shape,dtype=np.uint8)
#for i in range(ecg_roi.shape[0]):
#    tmp_rgb=cv.cvtColor(ecg_roi[i],cv.COLOR_BGR2RGB)
#    red_frames[i] = cv.bitwise_and(tmp_rgb,tmp_rgb,mask=red_mask[i])
#    
#matplot_show_video(red_frames)







    



