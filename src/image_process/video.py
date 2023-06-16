import pydicom
import cv2 as cv
import numpy as np

def array2avi(array_data: np.ndarray, video_name:str,fps:int, fourcc='MJPG',numpy_channel=False):
    """transfer array to avi
    array_data: 4D np.ndarray data, and the default channel order is for opencv
    file_name:  output file name
    fps:        the fps of avi file
    """

    if numpy_channel==True:
        array_data = array_data[:,:,:,::-1]

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

def avi2array(file_name:str)->np.ndarray:

    cap = cv.VideoCapture(file_name)

    frameCount = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    #frameWidth = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    #frameHeight = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

    #print(frameCount,frameWidth,frameHeight)

    video_array =  None

    for i in range(frameCount):
        ind, frame = cap.read()
        tmp_frame = np.expand_dims(frame,axis=0)
        if i == 0:
            video_array = tmp_frame
        else:
            video_array = np.vstack([video_array,tmp_frame])


    #print(video_array.shape)
    return video_array
