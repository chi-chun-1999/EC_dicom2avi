import os 
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import skvideo.io
import cv2 as cv
import numpy as np
from image_process import avi2array

#video = skvideo.io.vread('KBIHSQ00.avi')
#print(video.shape)

file_name = '../util/test/KBIHSQO2.avi'

video_array = avi2array(file_name)
print(video_array.shape)

