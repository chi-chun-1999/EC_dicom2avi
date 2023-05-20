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