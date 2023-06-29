import os 
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from image_process import *

import matplotlib.pyplot as plt
from show.matplot_show import matplot_show_video


import cv2 as cv
import numpy as np
import math

file_name = '../data_video/KBIHSS90.avi'

video_array = avi2array(file_name)
print(video_array.shape)



#plt.imshow(video_array[1,350:,0:318,:])


#ecg_roi =getECGRoi_FixSize(video_array) 

red_extractor = RedExtractor()
#
rr_interval_extractor = RRIntervalExtractor()
rr_start, rr_end = rr_interval_extractor.process(video_array)

cycle_start = rr_start
cycle_end = rr_end

matplot_show_video(video_array[cycle_start:cycle_end])

#cycyle_file_name = '../data_video/KBIHSS90_cycle.avi'
#array2avi(video_array[cycle_start:cycle_end],cycyle_file_name,30)




#red_mask = red_extractor.process(ecg_roi)
#
#red_frames = np.ones(ecg_roi.shape,dtype=np.uint8)
#for i in range(ecg_roi.shape[0]):
#    tmp_rgb=cv.cvtColor(ecg_roi[i],cv.COLOR_BGR2RGB)
#    red_frames[i] = cv.bitwise_and(tmp_rgb,tmp_rgb,mask=red_mask[i])
#    
#matplot_show_video(red_frames)


#slide_match_extractor = YellowLineSlideMatchExtractor()
#
#yellow_line_mask = slide_match_extractor.process(ecg_roi[0])
#yellow_line_argwhere = np.argwhere(yellow_line_mask[-2])
#
#red_argwhere = np.argwhere(red_mask)
#
#match_first_line = red_argwhere[red_argwhere[:,2]==yellow_line_argwhere[0,0]]
#match_second_line = red_argwhere[red_argwhere[:,2]==yellow_line_argwhere[1,0]]
#
#
#
#bias = 0
#while(match_first_line.size==0):
#
#    bias+=1
#
#    match_first_line = red_argwhere[red_argwhere[:,2]==yellow_line_argwhere[0,0]-bias]
#    if match_first_line.size!=0:
#        break
#    match_first_line = red_argwhere[red_argwhere[:,2]==yellow_line_argwhere[0,0]+bias]
#    
#bias = 0
#while(match_second_line.size==0):
#
#    bias+=1
#
#    match_second_line = red_argwhere[red_argwhere[:,2]==yellow_line_argwhere[1,0]-bias]
#    if match_second_line.size!=0:
#        break
#    match_second_line = red_argwhere[red_argwhere[:,2]==yellow_line_argwhere[1,0]+bias]
#
#    
#print(match_first_line)
#print(match_second_line)
#
#print(yellow_line_argwhere[0,0])
#print(yellow_line_argwhere[1,0])
#
#cycle_start = match_first_line[0,0]
#cycle_end = match_second_line[0,0]
#print(cycle_start)
#print(cycle_end)
#    
#
#matplot_show_video(video_array[cycle_start:cycle_end+1,:,:,::-1])

