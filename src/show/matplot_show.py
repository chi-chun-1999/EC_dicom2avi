import matplotlib.pyplot as plt
import cv2 as cv


def matplot_show_video(video_array):

    fig = plt.figure()
    viewer = fig.add_subplot(111)
    plt.ion() # Turns interactive mode on (probably unnecessary)
    fig.show() # Initially shows the figure

    for i in range(video_array.shape[0]):
        viewer.clear()
        viewer.imshow(video_array[i])
        plt.pause(.1)
        fig.canvas.draw()


def show_R_wave_place(ecg_roi,R_wave_location):
    
    ecg_roi_copy = ecg_roi[0].copy()
    for pt in R_wave_location:
        cv.line(ecg_roi_copy, (pt[0],pt[1]-10), (pt[0], pt[1] + 10), (0,0,255), 1)

    plt.figure()
    plt.imshow(ecg_roi_copy[:,:,::-1])
    
    