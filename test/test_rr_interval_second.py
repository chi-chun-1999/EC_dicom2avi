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
from src.image_process.ocr import HeartRateOCR, NumberOCR_Template
from src.image_process.feature import RRIntervalExtractor
import glob


#%%

files_4d = ['../../dataset/test/__174122/KBIHSSH2',
 '../../dataset/test/__174122/KBIHST1G',
 '../../dataset/test/__174122/KBIHSSH4',
 '../../dataset/test/__174122/KBIHSQ00',
 '../../dataset/test/__174122/KBIHSS8S',
 '../../dataset/test/__174122/KBIHST9M',
 '../../dataset/test/__174122/KBIHST9K',
 '../../dataset/test/__174122/KBIHSR8G',
 '../../dataset/test/__174122/KBIHSR8I',
 '../../dataset/test/__174122/KBIHST1C',
 '../../dataset/test/__174122/KBIHST1E',
 '../../dataset/test/__174122/KBIHSSPA',
 '../../dataset/test/__174122/KBIHSS90',
 '../../dataset/test/__174122/KBIHSSP8',
 '../../dataset/test/__174122/KBIHSSP6',
 '../../dataset/test/__174122/KBIHSTHO',
 '../../dataset/test/__174122/KBIHSQO2',
 '../../dataset/test/__174122/KBIHSR0C',
 '../../dataset/test/__174122/KBIHST9I',
 '../../dataset/test/__174122/KBIHSR0E']


#%%

dcm = pydicom.dcmread(files_4d[5])

dcm_rgb_array =  getRgbArray(dcm)
dcm_bgr_array = dcm_rgb_array[:,:,:,::-1]


rr_interval_extractor = RRIntervalExtractor()

cycle_start, cycle_end = rr_interval_extractor.process(dcm_bgr_array)
first_yellow_line, second_yellow_line = rr_interval_extractor.getTwoLineLocation()

print(cycle_start,cycle_end,first_yellow_line,second_yellow_line)
plt.imshow(dcm_rgb_array[int((cycle_start+cycle_end)/2)])

detect_frame = dcm_rgb_array[int((cycle_start+cycle_end)/2)]


template = np.load('./template_number.npy')
template = template/255

nubmer_ocr = NumberOCR_Template(template)
heart_ocr = HeartRateOCR(nubmer_ocr)
heart_rate = heart_ocr.fit(detect_frame)
rr_interval_pixel = second_yellow_line-first_yellow_line

pixel_ms = getPixelMs(rr_interval_pixel,heart_rate)
print('pixel ms:',pixel_ms)


# %%
