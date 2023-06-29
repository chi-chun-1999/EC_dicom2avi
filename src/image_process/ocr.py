
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import cv2 as cv

import numpy as np
import abc
from src.image_process.frame import getHeartRateROI_FixSize
import matplotlib.pyplot as plt



class OCR(abc.ABC):
    def __init__(self) -> None:
        pass

    @abc.abstractclassmethod
    def fit(self,image):
        pass
    
    def getWeight(self,weight):
        self._weight = weight

class NumberOCR_Template(OCR):
    def __init__(self,weight) -> None:
        self.getWeight(weight)
        
    def fit(self,image):
        """
        
        This method utilizes template weighting to classify the input ROI image and returns the number of the ROI image.
        
        input:
        image:  ROI image
        
        return:
        num:    the number of the ROI image
        """
        if np.sum(image)==0:
            return -1
        tmp = image*self._weight
        tmp_sum = np.sum(tmp,axis=1)
        score = np.sum(tmp_sum,axis=1)
        num = np.argmax(score)
        return num
        
class HearRateOCR(OCR):
    def __init__(self,NumberOCR:NumberOCR_Template) -> None:
        self._number_ocr = NumberOCR
        self._number_roi = (10,8)
    
    def fit(self,image):
        """
        Given one frame of the echocardiography data, and this method returns the heart rate of this frame.
        
        input:
        image: one frame of the echocardiography data

        return:
        heart_rate: the heart rate
        
        """
        roi = []
        heart_rate = 0
        
        
        heart_rate_roi = getHeartRateROI_FixSize(image)
        #plt.imshow(heart_rate_roi)
        img_gray = cv.cvtColor(heart_rate_roi,cv.COLOR_RGB2GRAY)
        re,img_bin = cv.threshold(img_gray,127,255,cv.THRESH_BINARY)

        roi.append(img_bin[8:18,8:16])
        roi.append(img_bin[8:18,16:24])
        roi.append(img_bin[8:18,24:32])
        
        for i in range(len(roi)):

            tmp = self._number_ocr.fit(roi[i])
            if tmp != -1:
                heart_rate += tmp*10**(2-i)
        
        return heart_rate

                


        
