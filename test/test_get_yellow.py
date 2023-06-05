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

file_name = '../data_video/KBIHSQO2.avi'

video_array = avi2array(file_name)
print(video_array.shape)


ecg_roi =getECGRoi_FixSize(video_array) 


tmp = ecg_roi[40].copy()

yellow_line_extractor = YellowLineExtractor(denoise_thres=2,hough_line_thres=25)
yellow_line_mask = yellow_line_extractor.process(ecg_roi)
plt.figure()
plt.imshow(yellow_line_mask)

#plt.figure()

#plt.imshow(tmp[:,:,::-1])
#tmp[tmp.std(axis=2)<3]= np.array([0,0,0])
##tmp = tmp.mean(axis=2)
#plt.figure()
#plt.imshow(tmp[:,:,::-1])
#
## %%
#
#lower_bgr = np.array([80,150,150])
#upper_bgr = np.array([150,200,180])
#
##lower_bgr = np.array([100,100,100])
##upper_bgr = np.array([255,255,255])
#
#mix_lower_bgr = np.array([50,70,115])
#mix_upper_bgr = np.array([110,110,140])
#
#
#mask = cv.inRange(tmp,lower_bgr,upper_bgr)
#
#red_frames = np.ones(ecg_roi.shape,dtype=np.uint8)
#tmp_rgb=cv.cvtColor(tmp,cv.COLOR_BGR2RGB)
#
#kernel = cv.getStructuringElement(cv.MORPH_RECT, (2, 2))
#or_mask = cv.bitwise_or(mask,mask)
##or_mask = cv.erode(or_mask,kernel)
#lines = cv.HoughLines(or_mask,1,np.pi/180,25)
#
#
#plt.figure()
#plt.imshow(mask)
#plt.figure()
#plt.imshow(or_mask)
#plt.figure()
#plt.imshow(tmp_rgb)
#
#yellow_line_mask = np.zeros(ecg_roi[0].shape,dtype=np.uint8)
#
#for i in range(0, len(lines)):
#            rho_l = lines[i][0][0]
#            theta_l = lines[i][0][1]
#            a_l = math.cos(theta_l)
#            b_l = math.sin(theta_l)
#            x0_l = a_l * rho_l
#            y0_l = b_l * rho_l
#            pt1_l = (int(x0_l + 1000*(-b_l)), int(y0_l + 1000*(a_l)))
#            pt2_l = (int(x0_l - 1000*(-b_l)), int(y0_l - 1000*(a_l)))
#            cv.line(yellow_line_mask, pt1_l, pt2_l, (255,255,255), 1, cv.LINE_AA)
#            
#plt.figure()
#plt.imshow(yellow_line_mask)
#print(lines.shape)
## %%
#