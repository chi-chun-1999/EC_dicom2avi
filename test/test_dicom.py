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

data_path = '../../dataset/test/__174122/KBIHSR0C'
video_name = './testmp4.mp4'
fps = 30

dcm = pydicom.dcmread(data_path)
#video_array = avi2array(video_name)
#npy_array = np.load('./test.npz.npy')

#video_array_rgb = cv.cvtColor(video_array[0],cv.COLOR_BGR2RGB)


dcm_rgb_array =  getRgbArray(dcm)


print(dcm_rgb_array.shape)
plt.figure()
plt.imshow(dcm_rgb_array[0])
#plt.figure()
#plt.imshow(video_array_rgb)
#plt.figure()
#plt.imshow(npy_array[0])
plt.show()

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

#mp4_video_name = 'testmp4.mp4'
#array2avi(dcm_rgb_array[:,:,:,::-1],mp4_video_name,fps,fourcc='mp4v')
#array2avi(dcm_rgb_array[1,:,:,::-1],video_name,fps)
