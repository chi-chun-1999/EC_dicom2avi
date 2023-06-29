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
import pytesseract
from PIL import Image
from src.image_process.ocr import NumberOCR_Template, HearRateOCR


#%%
data_dir = '../../dataset/test/__174122/*'

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

heart_rate_roi = getHeartRateROI_FixSize(dcm_rgb_array)

#plt.imshow(heart_rate_roi[0,:,15:24])



img_re = cv.cvtColor(heart_rate_roi[0,:,:],cv.COLOR_RGB2GRAY)
re,img_bin = cv.threshold(img_re,127,255,cv.THRESH_BINARY)
#img_re = cv.resize(img_re,(44,72),interpolation=cv.INTER_CUBIC)

roi_1 = img_bin[8:18,8:16]
roi_2 = img_bin[8:18,16:24]
roi_3 = img_bin[8:18,24:32]
plt.figure()
plt.imshow(roi_1)
plt.figure()
plt.imshow(roi_2)
plt.show()
plt.figure()
plt.imshow(roi_3)
plt.show()

#img = Image.fromarray(heart_rate_roi[0,:,15:24])
#img = Image.fromarray(img_bin)
#pytesseract.image_to_string(img,lang='eng')


# %%

template = np.load('./template_number.npy')
template = template/255

nubmer_ocr = NumberOCR_Template(template)
#print(nubmer_ocr.fit(roi_1))
#print(nubmer_ocr.fit(roi_2))
#print(nubmer_ocr.fit(roi_3))

heart_ocr = HearRateOCR(nubmer_ocr)
plt.imshow(dcm_rgb_array[0])
print(heart_ocr.fit(dcm_rgb_array[0]))



#def fit(image,template):
#    if np.sum(image)==0:
#        return -1
#    tmp = image*template
#    tmp_sum = np.sum(tmp,axis=1)
#    score = np.sum(tmp_sum,axis=1)
#    num = np.argmax(score)
#    return num
#
#
#print(fit(roi_1,template))
#print(fit(roi_2,template))
#print(fit(roi_3,template))

# %%

    