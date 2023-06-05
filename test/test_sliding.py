#%%
import os 
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from image_process import *

import matplotlib.pyplot as plt
from show.matplot_show import matplot_show_video


import cv2 as cv
import numpy as np
import math

file_name = '../data_video/KBIHSSPA.avi'

video_array = avi2array(file_name)
print(video_array.shape)


ecg_roi =getECGRoi_FixSize(video_array) 


tmp = ecg_roi[40].copy()

slide_match_extractor = YellowLineSlideMatchExtractor()

yellow_line_mask = slide_match_extractor.process(tmp)


plt.figure()
plt.imshow(yellow_line_mask)

# %%
