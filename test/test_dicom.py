import os 
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import pydicom
import cv2 as cv
import numpy as np
import SimpleITK as sitk
import matplotlib.pyplot as plt
from typing import Type
from image_process import getRgbArray
from image_process import array2avi


data_path = '../../dataset/H/GEMS_IMG/2020_NOV/18/__174122/KBIHSQ00'
video_name = 'test3.avi'
fps = 30

dcm = pydicom.dcmread(data_path)


dcm_rgb_array =  getRgbArray(dcm)
print(dcm_rgb_array.shape)
plt.imshow(dcm_rgb_array[0])


#(framenum, height, width, channel) = dcm_rgb_array.shape
#
#fourcc = cv.VideoWriter_fourcc(*'MJPG')
#out = cv.VideoWriter(video_name,fourcc,fps,(width,height),True)
#
##
### 將每一幀像素數據寫入AVI影片
#for frame_pixels in dcm_rgb_array:
##    # 將像素數據轉換為8位灰度影像
##    #frame = cv.convertScaleAbs(frame_pixels, alpha=(255.0/np.amax(ec_pixels)))
##
##    # 寫入影片
#    out.write(frame_pixels[:,:,::-1])
##
### 釋放影片寫入器
#out.release()

array2avi(dcm_rgb_array[:,:,:,::-1],video_name,fps)
