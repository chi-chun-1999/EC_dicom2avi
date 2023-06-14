#%%
import os 
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import pydicom
import cv2 as cv
import numpy as np
#import SimpleITK as sitk
import matplotlib.pyplot as plt
from typing import Type
from image_process import *

from show.matplot_show import matplot_show_video
from scipy.stats import norm
from sklearn.cluster import DBSCAN
import glob
#%%
data_dir = '../../dataset/test/H/GEMS_IMG/2020_NOV/18/__174122/*'

print(glob.glob(data_dir))
dicom_files = glob.glob(data_dir)

files_4d = []
for f in dicom_files:
    dcm = pydicom.dcmread(f)
    array_data = dcm.pixel_array
    if array_data.ndim == 4:
        #head,file_name = os.path.split(f)
        files_4d.append(f)

#%%
dcm = pydicom.dcmread(files_4d[6])
#video_array = avi2array(video_name)
#npy_array = np.load('./test.npz.npy')

#video_array_rgb = cv.cvtColor(video_array[0],cv.COLOR_BGR2RGB)


dcm_rgb_array =  getRgbArray(dcm)

dcm_bgr_array = dcm_rgb_array[:,:,:,::-1]



#plt.imshow(video_array[1,350:,0:318,:])


ecg_roi =getECGRoi_FixSize(dcm_bgr_array,[350,434,0,400]) 

plt.figure()
plt.imshow(ecg_roi[0,:,:,::-1])



gree_ecg_extractor = GreenECGExtractor(denoise_thres=5)

green_ecg_mask = gree_ecg_extractor.process(ecg_roi)

plt.figure()
plt.imshow(green_ecg_mask)

ecg_location = np.argwhere(green_ecg_mask)
ecg_mean = np.argwhere(green_ecg_mask).mean(axis=0)
ecg_y_range_upper_bound = np.ceil(np.abs(ecg_location-ecg_mean).max(axis=0)[0])
ecg_y_range_upper_bound = ecg_y_range_upper_bound.astype(int)
#print(ecg_y_range_upper_bound)
ecg_y_axis_center = ecg_mean.astype(int)[0]




yellow_line_extractor = YellowLineSlideMatchExtractor()
yellow_line_extractor.process(ecg_roi)
first_line,second_line  = yellow_line_extractor.getTwoLineLocation()
#print(first_line,second_line)

template_mask = green_ecg_mask[ecg_y_axis_center-ecg_y_range_upper_bound:ecg_y_axis_center+ecg_y_range_upper_bound,first_line+1:first_line+40]

plt.figure()
plt.imshow(template_mask)


# Using the OpenCV template match to find the match place.

w,h = template_mask.shape[::-1]
threshold = 0.7
match = cv.matchTemplate(green_ecg_mask,template_mask,cv.TM_CCORR_NORMED)
loc = np.where( match >= threshold)
#print(loc,h,w)

# the GMM of R location accroding to RR interval


ecg_location_x_max = np.max(ecg_location[:,1])
ecg_location_x_min = np.min(ecg_location[:,1])

image_rr_interval_dist = second_line-first_line

R_dist_probability = np.zeros((green_ecg_mask.shape[1],2))
R_dist_probability[:,0] = np.arange(0,green_ecg_mask.shape[1])


probability_center_list = []
current_location = first_line
probability_center_list.append(current_location)

while current_location>=ecg_location_x_min:
    current_location-=image_rr_interval_dist
    probability_center_list.append(current_location)


current_location = second_line
probability_center_list.append(current_location)

while current_location<=ecg_location_x_max:
    current_location+=image_rr_interval_dist
    probability_center_list.append(current_location)
    
#print(probability_center_list)


for i in probability_center_list:
    #print(i-int(image_rr_interval_dist/2))
    #R_dist_probability[i-int(image_rr_interval_dist/2):i+int(image_rr_interval_dist/2),1] = y
    R_dist_probability[:,1]+=norm.pdf(R_dist_probability[:,0],loc=i,scale=35)

R_dist_probability[0:ecg_location_x_min,1]=0
R_dist_probability[ecg_location_x_max:,1]=0


#plt.plot(R_dist_probability[:,0],R_dist_probability[:,1])
#plt.show()

# Combine R_dist_probability and match matrix


template_match_mask = np.zeros(green_ecg_mask.shape)
template_match_mask[0:match.shape[0],0:match.shape[1]] = match

combine_mask = template_match_mask*R_dist_probability.T[1:2,:]

plt.figure()
plt.imshow(combine_mask)


## getorder and R wave location in x axis

ind = np.unravel_index(np.argsort(combine_mask, axis=None), combine_mask.shape)
#print(ind[0][-15::],ind[1][-15::])
#print(combine_mask[ind])
##

r_wave_x_location = []



X = ind[1][np.arange(-1,-16,-1)].reshape((-1,1))
clustering = DBSCAN(eps=3, min_samples=2).fit(X)
labels = clustering.labels_
unique_label = np.unique(labels).tolist()

for i in unique_label:
    index = np.where(labels==i)[0][0]
    r_wave_x_location.append((ind[1][-1-index],ind[0][-1-index]))

print(r_wave_x_location)
#rr_interval_extractor = RRIntervalExtractor()
#rr_start, rr_end = rr_interval_extractor.process(ecg_roi)
#
#cycle_start = rr_start
#cycle_end = rr_end

#matplot_show_video(video_array[cycle_start:cycle_end])

#rr_interval_frame_num = cycle_end-cycle_start
#plt.imshow(ecg_roi[0])
#print(rr_interval_frame_num)


#cycyle_file_name = '../data_video/KBIHSS90_cycle.avi'
#array2avi(video_array[cycle_start:cycle_end],cycyle_file_name,30)
#%%
ecg_roi_copy = ecg_roi[0].copy()
for pt in r_wave_x_location:
    print(pt[0],pt[1])
    cv.rectangle(ecg_roi_copy, pt, (pt[0] + w, pt[1] + h), (0,0,255), 1)

plt.figure()
plt.imshow(ecg_roi_copy[:,:,::-1])



# %%
