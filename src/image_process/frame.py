import pydicom
import numpy as np
import cv2 as cv
from typing import Type

def getRgbArray(dicom_file: Type[pydicom.FileDataset]) -> np.ndarray:
    '''
    get RGB pixel array from dicom file 

    dicom_file:   data of "pydicom.dataset.FileDataset" 
    
    return:
    rgb_array: the rgb np.narray from dicom file

    '''
    current_color_space = dicom_file[0x0028,0x0004].value 
    if current_color_space == 'RGB':
        return dicom_file.pixel_array
    else:
        rgb_array = pydicom.pixel_data_handlers.convert_color_space(dicom_file.pixel_array,current_color_space,'RGB')
        return rgb_array
    

def getECGRoi_FixSize(image:np.ndarray,roi_location=None):
    '''
    get ECG FIXED SIZE ROI from the Echocardiography RGB array 
    
    image: 3 dimension image or 4 dimesion video data
    roi_loaction: please input 4 element data. roi_location[0] and roi_loaction[1] is range for y axis, and roi_location[0] and roi_loaction[1] is range for x axis.

    retrun:
    ecg_roi: get ecg ROI 
    
    '''
    
    if image.ndim!=4 and image.ndim!=3:
        raise ValueError('The dimesion of input image not correct. Please input 3 or 4 dimesion data!')
        
    img_size = image.shape
    
    if image.ndim == 4:
        if roi_location ==None:
            ecg_roi = image[:,350:,:int(img_size[2]/2),:]
        else:
            ecg_roi = image[:,roi_location[0]:roi_location[1],roi_location[2]:roi_location[3],:]
    
    else:
        if roi_location ==None:
            ecg_roi = image[350:,:int(img_size[2]/2),:]
        else:
            ecg_roi = image[roi_location[0]:roi_location[1],roi_location[2]:roi_location[3],:]
    
    return ecg_roi

def getHeartRateROI_FixSize(image:np.ndarray,roi_location=None):
    '''
    get heart rate FIXED SIZE ROI from the Echocardiography RGB array 
    
    image: 3 dimension image or 4 dimesion video data
    roi_loaction: please input 4 element data. roi_location[0] and roi_loaction[1] is range for y axis, and roi_location[0] and roi_loaction[1] is range for x axis.

    retrun:
    ecg_roi: get heart rate ROI 
    
    '''
    
    if image.ndim!=4 and image.ndim!=3:
        raise ValueError('The dimesion of input image not correct. Please input 3 or 4 dimesion data!')
        
    img_size = image.shape
    
    if image.ndim == 4:
        if roi_location ==None:
            ecg_roi = image[:,400:422,600:,:]
        else:
            ecg_roi = image[:,roi_location[0]:roi_location[1],roi_location[2]:roi_location[3],:]
    
    else:
        if roi_location ==None:
            ecg_roi = image[400:422,600:,:]
        else:
            ecg_roi = image[roi_location[0]:roi_location[1],roi_location[2]:roi_location[3],:]
    
    return ecg_roi
    
def denoiseEco(image,denoise_thres=3):
    '''
    denoise the Echocardiography data from image

    image: 3 dimesion image

    return:
    denoise_image: the image after denoise
    
    '''

    denoise_image = image.copy()
    denoise_image[denoise_image.std(axis=2)<denoise_thres]= np.array([0,0,0])
    
    return denoise_image

    
def getPixelMs(rr_interval_pixel,heart_rate):
    """
    Get millisecond for each pixel

    input:
    rr_interval_pixel: the pixel length between the two lines.
    heart_rate:    the heart rate between the two lines
    
    """
    rr_interval_ms = 60000/heart_rate
    pixel_ms = rr_interval_ms/rr_interval_pixel
    return pixel_ms