import pydicom
import cv2 as cv
import numpy as np

def array2avi(array_data: np.ndarray, video_name:str,fps:int, fourcc='MJPG'):
    """transfer array to avi
    array_data: 4D np.ndarray data, and the channel order is for opencv
    file_name:  output file name
    fps:        the fps of avi file
    """
    if len(array_data.shape)!=4:
        raise ValueError('The shape of array data not match')
    elif np.max(array_data)>255:
        raise ValueError('The max value in arry data larger than 255.')
        return
    else:
        (framenum, height, width, channel) = array_data.shape
        fourcc = cv.VideoWriter_fourcc(*fourcc)
        out = cv.VideoWriter(video_name,fourcc,fps,(width,height),True)

        for frame_pixels in array_data:
            out.write(frame_pixels)

        out.release()