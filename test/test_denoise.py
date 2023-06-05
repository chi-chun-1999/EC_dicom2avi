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

file_name = '../data_video/KBIHSR8G.avi'

video_array = avi2array(file_name)
print(video_array.shape)


ecg_roi =getECGRoi_FixSize(video_array) 


tmp = ecg_roi[40].copy()
plt.figure()
plt.imshow(tmp[:,:,::-1])
tmp[tmp.std(axis=2)<5]= np.array([0,0,0])
#tmp = tmp.mean(axis=2)
plt.figure()
plt.imshow(tmp[:,:,::-1])


#%%
#rect = [10,20,300,60]
#b_Model = np.zeros((1,65),np.float64)
#f_Model = np.zeros((1,65),np.float64)
#mask_new,b_model,f_model=cv.grabCut(ecg_roi[40],None,rect,b_Model,f_Model,10,cv.GC_INIT_WITH_RECT)
#
#print(np.unique(mask_new))
#plt.imshow(mask_new)
## %%
#
#dst = cv.pyrMeanShiftFiltering(ecg_roi[40],20,30,2)
#plt.imshow(dst)
#
## %%
#y_template = np.ones((52,1,3))*np.array([164,110,181])
#y_template = y_template.astype(ecg_roi.dtype)
#
#ori_gray = cv.cvtColor(ecg_roi[40].copy(),cv.COLOR_BGR2GRAY)
#y_template_gray = cv.cvtColor(y_template.copy(),cv.COLOR_BGR2GRAY)
#plt.imshow(y_template)
#w = y_template.shape[1]
#h = y_template.shape[0]
#
#methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
#            'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
#
#for meth in methods:
#    img = ecg_roi[40].copy()
#    method = eval(meth)
# 
#    # Apply template Matching
#    res = cv.matchTemplate(ori_gray,y_template_gray,method)
#    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
# 
#    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
#    if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
#        top_left = min_loc
#    else:
#        top_left = max_loc
#    bottom_right = (top_left[0] + w, top_left[1] + h)
# 
#    cv.rectangle(img,top_left, bottom_right, 255, 2)
# 
#    plt.subplot(121),plt.imshow(res,cmap = 'gray')
#    plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
#    plt.subplot(122),plt.imshow(img)
#    plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
#    plt.suptitle(meth)
# 
#    plt.show()
## %%
