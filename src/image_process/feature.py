import cv2 as cv
import numpy as np
import abc
import matplotlib.pyplot as plt
from .frame import denoiseEco
import math

class FeatureExtractor(abc.ABC):
    def __init__(self):
        self.__extract_data = None
    
    @abc.abstractmethod
    def process(self,extract_data):
        return NotImplemented
    

class RedExtractor(FeatureExtractor):
    def __init__(self,lower_bgr=None ,upper_bgr=None):
        if lower_bgr==None:
            self._lower_bgr =np.array([50,50,120])
        if upper_bgr==None:
            self._upper_bgr = np.array([110,110,225])
    
    
    def process(self,extract_data):
        self.__extract_data = extract_data
        
        extract_data_shape = self.__extract_data.shape
        
        self.__return_data = np.zeros(self.__extract_data.shape[0:3],dtype=np.uint8)

        for i in range(self.__extract_data.shape[0]):
            tmp = self.__extract_data[i]
            tmp_rgb=cv.cvtColor(tmp,cv.COLOR_BGR2RGB)
            mask = cv.inRange(tmp,self._lower_bgr,self._upper_bgr)
            #mix_mask = cv.inRange(tmp,self._mix_lower_bgr,self._mix_upper_bgr)
            kernel = cv.getStructuringElement(cv.MORPH_RECT, (2, 2))
            #or_mask = cv.bitwise_or(mask,mix_mask)
            or_mask = cv.bitwise_or(mask,mask)
            or_mask = cv.erode(or_mask,kernel)
            or_mask = cv.dilate(or_mask,kernel)
            self.__return_data[i] = or_mask
            #self.__return_data[i] = cv.bitwise_and(tmp_rgb,tmp_rgb,mask=or_mask)
        
        return self.__return_data


class YellowLineExtractor(FeatureExtractor):

    def __init__(self,denoise_thres=3,hough_line_thres = 25,lower_bgr=None ,upper_bgr=None):
        self._denoise_thres = denoise_thres
        self._hough_line_thres = hough_line_thres
        
        if lower_bgr == None:
            self._lower_bgr = np.array([80,150,150])
        if lower_bgr == None:
            self._upper_bgr = np.array([150,200,180])
            
    def process(self,extractor_data):
        

        self.__extractor_data = extractor_data

        if self.__extractor_data.ndim>=4:
            tmp = self.__extractor_data[0].copy()
        else:
            tmp = self.__extractor_data.copy()


        tmp = denoiseEco(tmp,self._denoise_thres)

#tmp = tmp.mean(axis=2)
        mask = cv.inRange(tmp,self._lower_bgr,self._upper_bgr)
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (2, 2))
        mask = cv.dilate(mask,kernel)
        plt.figure()
        plt.imshow(mask)
        print(mask.shape)
        lines = cv.HoughLines(mask,1,np.pi/180,self._hough_line_thres)

        yellow_line_mask = np.zeros(tmp.shape,dtype=np.uint8)

        points = np.zeros((len(lines),2,2))

        for i in range(0, len(lines)):
                    rho_l = lines[i][0][0]
                    theta_l = lines[i][0][1]
                    a_l = math.cos(theta_l)
                    b_l = math.sin(theta_l)
                    x0_l = a_l * rho_l
                    y0_l = b_l * rho_l
                    pt1_l = (int(x0_l + 1000*(-b_l)), int(y0_l + 1000*(a_l)))
                    pt2_l = (int(x0_l - 1000*(-b_l)), int(y0_l - 1000*(a_l)))
                    points[i][0]=pt1_l
                    points[i][1]=pt2_l
                    cv.line(yellow_line_mask, pt1_l, pt2_l, (255,255,255), 1, cv.LINE_AA)
        
        print(points.std(axis=0))
        
        return yellow_line_mask
            


class SlideMatchExtractor(FeatureExtractor):
    def __init__(self,denoise_thres=3,lower_bgr=None ,upper_bgr=None):
        self._denoise_thres = denoise_thres
        
        if lower_bgr == None:
            self._lower_bgr = np.array([80,150,150])
        if lower_bgr == None:
            self._upper_bgr = np.array([150,200,180])
            
    def process(self,extractor_data):
        

        self.__extractor_data = extractor_data

        if self.__extractor_data.ndim>=4:
            tmp = self.__extractor_data[0].copy()
        else:
            tmp = self.__extractor_data.copy()


        tmp = denoiseEco(tmp,self._denoise_thres)

#tmp = tmp.mean(axis=2)
        mask = cv.inRange(tmp,self._lower_bgr,self._upper_bgr)
        #kernel = cv.getStructuringElement(cv.MORPH_RECT, (2, 2))
        #mask = cv.dilate(mask,kernel)
        #plt.figure()
        #plt.imshow(mask)
        #print(mask.shape)

        slide_view = np.lib.stride_tricks.sliding_window_view(mask,(84,3))

        #print(slide_view.shape)
        extract_slide_window = np.ones((84,3))
        extract_slide_window[:,1]=10

        outcome = slide_view*extract_slide_window
        score = (outcome.sum(axis=2)).sum(axis=2)
        yello_location = np.unravel_index(score.argmax(), score.shape)

        first_line = np.unravel_index(score.argsort()[0,-1],score.shape)
        second_line = np.unravel_index(score.argsort()[0,-2],score.shape)

        yellow_line_mask = np.zeros(mask.shape,np.uint8)
        #print(first_line[1])
        #print(second_line[1])
        #print(yellow_line_mask.shape)
        yellow_line_mask[-52:-1,first_line[1]]=255
        yellow_line_mask[-52:-1,second_line[1]]=255


        return yellow_line_mask
