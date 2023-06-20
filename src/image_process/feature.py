import cv2 as cv
import numpy as np
import abc
import matplotlib.pyplot as plt
from .frame import denoiseEco
import math
from scipy.stats import norm 
from sklearn.cluster import DBSCAN


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
        else:
            self._lower_bgr = lower_bgr
        if upper_bgr==None:
            self._upper_bgr = np.array([110,110,225])
        else:
            self._upper_bgr = upper_bgr
    
    
    def process(self,extract_data):
        """
        Given the 4-dimensional video data, this function utilizes the COLOR feature to filter the region of interest (ROI) based on the color red.

        input:
        extract_data: the 4-dim roi of ecg video data.
        
        return:
        self.__return_data: the 4-dim mask of ROI based on the color red.


        """
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

class GreenECGExtractor(FeatureExtractor):
    def __init__(self,denoise_thres=3,lower_bgr=None,upper_bgr=None):
        self.__denoise_thres = denoise_thres
        if lower_bgr==None:
            self._lower_bgr =np.array([120,130,0])
        else:
            self._lower_bgr = lower_bgr
        if upper_bgr==None:
            self._upper_bgr = np.array([190,190,100])
        else:
            self._upper_bgr = upper_bgr
        
        
    def process(self, extract_data):
        first_frame = extract_data[0].copy()
        final_frame = extract_data[-1].copy()
        denoise_first_frame = denoiseEco(first_frame,self.__denoise_thres)
        denoise_final_frame = denoiseEco(final_frame,self.__denoise_thres)

        first_mask = cv.inRange(denoise_first_frame,self._lower_bgr,self._upper_bgr)
        final_mask = cv.inRange(denoise_final_frame,self._lower_bgr,self._upper_bgr)
        ecg_mask = cv.bitwise_or(first_mask,final_mask)
        
        #plt.figure()
        #plt.imshow(denoise_first_frame)
        #plt.figure()
        #plt.imshow(first_mask)
        #plt.figure()
        #plt.imshow(final_mask)
        #plt.figure()
        #plt.imshow(ecg_mask)
        #plt.show()
        return ecg_mask
        
        


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
            


class YellowLineSlideMatchExtractor(FeatureExtractor):
    def __init__(self,denoise_thres=3,lower_bgr=None ,upper_bgr=None):
        self._denoise_thres = denoise_thres
        
        if lower_bgr == None:
            self._lower_bgr = np.array([80,150,150])
        if lower_bgr == None:
            self._upper_bgr = np.array([150,200,180])
            
    def process(self,extractor_data):
        """
        Find only the location of two yellow lines in the image.
        
        """

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

        # Because the the size of kernel is 84x3, the actual location of line must add 1 

        self._first_line = list(np.unravel_index(score.argsort()[0,-1],score.shape))
        self._first_line[1]+=1         # Because the the size of kernel is 84x3, the actual location of line must add 1

        self._second_line =list(np.unravel_index(score.argsort()[0,-2],score.shape))
        self._second_line[1]+=1         # Because the the size of kernel is 84x3, the actual location of line must add 1

        yellow_line_mask = np.zeros(mask.shape,np.uint8)
        #print(first_line[1])
        #print(second_line[1])
        #print(yellow_line_mask.shape)
        yellow_line_mask[-52:-1,self._first_line[1]]=255
        yellow_line_mask[-52:-1,self._second_line[1]]=255


        return yellow_line_mask

    def getTwoLineLocation(self):
        
        if self._first_line[1]<self._second_line[1]:
            return self._first_line[1],self._second_line[1]
        else:
            return self._second_line[1],self._first_line[1]

class RRIntervalExtractor(FeatureExtractor):
    def __init__(self,red_feature_extractor=None,yellow_feature_extractor=None):
        
        if red_feature_extractor == None:
            self._red_feature_extractor = RedExtractor()
        else:
            self._red_feature_extractor = red_feature_extractor

        if yellow_feature_extractor == None:
            self._yellow_feature_extractor = YellowLineSlideMatchExtractor()

        else:
            self._yellow_feature_extractor =  yellow_feature_extractor
        
    def process(self, extract_data):
        '''
        Given a 4-dimensional video array, this function extracts a cycle of heart Echocardiography data from the extract_data.
        
        input:
        extract_data: The 4-dim numpy array echo data.
        
        return:
        extract_data[cycle_start:cycle_end]: a cycle of heart Echocardiography data.
        
        '''

        self.__extract_data = extract_data
        
        red_mask = self._red_feature_extractor.process(self.__extract_data)

        yellow_line_mask = self._yellow_feature_extractor.process(self.__extract_data[0])
        yellow_line_argwhere = np.argwhere(yellow_line_mask[-2])

        red_argwhere = np.argwhere(red_mask)

        match_first_line = red_argwhere[red_argwhere[:,2]==yellow_line_argwhere[0,0]]
        match_second_line = red_argwhere[red_argwhere[:,2]==yellow_line_argwhere[1,0]]

        bias = 0
        while(match_first_line.size==0):

            bias+=1

            match_first_line = red_argwhere[red_argwhere[:,2]==yellow_line_argwhere[0,0]-bias]
            if match_first_line.size!=0:
                break
            match_first_line = red_argwhere[red_argwhere[:,2]==yellow_line_argwhere[0,0]+bias]
            
        bias = 0
        while(match_second_line.size==0):

            bias+=1

            match_second_line = red_argwhere[red_argwhere[:,2]==yellow_line_argwhere[1,0]-bias]
            if match_second_line.size!=0:
                break
            match_second_line = red_argwhere[red_argwhere[:,2]==yellow_line_argwhere[1,0]+bias]

        #print(match_first_line)
        #print(match_second_line)

        #print(yellow_line_argwhere[0,0])
        #print(yellow_line_argwhere[1,0])
            

        cycle_start = match_first_line[0,0]
        cycle_end = match_second_line[0,0]
        #print(cycle_start)
        #print(cycle_end)
        return (cycle_start,cycle_end)


class RWaveExtractor_Cluster(FeatureExtractor):
    def __init__(self,template_width = 40,denoise_thres = 5,gmm_scale = 35,match_candidate=15):

        self._template_width = template_width
        self._denoise_thres = denoise_thres
        self._gmm_scale = gmm_scale
        self._match_candidate = match_candidate

    def _get_ecg_info(self):
        gree_ecg_extractor = GreenECGExtractor(denoise_thres=self._denoise_thres)

        self._green_ecg_mask = gree_ecg_extractor.process(self._extract_data)

        self._ecg_location = np.argwhere(self._green_ecg_mask)
        self._ecg_mean = np.argwhere(self._green_ecg_mask).mean(axis=0)
        self._ecg_y_range_upper_bound = np.ceil(np.abs(self._ecg_location-self._ecg_mean).max(axis=0)[0])
        self._ecg_y_range_upper_bound = self._ecg_y_range_upper_bound.astype(int)
#print(ecg_y_range_upper_bound)
        self._ecg_y_axis_center = self._ecg_mean.astype(int)[0]
    
    def _get_two_yello_line_location(self):


        yellow_line_extractor = YellowLineSlideMatchExtractor()
        yellow_line_extractor.process(self._extract_data)
        #yellow_line_mask = yellow_line_extractor.process(extract_data)
        #plt.figure()
        #plt.imshow(yellow_line_mask)
        self._first_line,self._second_line  = yellow_line_extractor.getTwoLineLocation()
        
         
    def _generate_template_mask(self):

        self._template_mask = self._green_ecg_mask[self._ecg_y_axis_center-self._ecg_y_range_upper_bound:self._ecg_y_axis_center+self._ecg_y_range_upper_bound,self._first_line+1:self._first_line+self._template_width]
        
        return self._template_mask

    def _generate_gmm(self):

# the GMM of R location accroding to RR interval
        ecg_location_x_max = np.max(self._ecg_location[:,1])
        ecg_location_x_min = np.min(self._ecg_location[:,1])

        image_rr_interval_dist = self._second_line-self._first_line

        self._R_dist_probability = np.zeros((self._green_ecg_mask.shape[1],2))
        self._R_dist_probability[:,0] = np.arange(0,self._green_ecg_mask.shape[1])


        self._probability_center_list = []
        current_location = self._first_line
        self._probability_center_list.append(current_location)

        #plt.figure()
        while current_location>=ecg_location_x_min:
            current_location-=image_rr_interval_dist
            self._probability_center_list.append(current_location)


        current_location = self._second_line
        self._probability_center_list.append(current_location)
        
        while current_location<=ecg_location_x_max:
            current_location+=image_rr_interval_dist
            self._probability_center_list.append(current_location)
            

        for i in self._probability_center_list:
            self._R_dist_probability[:,1]+=norm.pdf(self._R_dist_probability[:,0],loc=i,scale=self._gmm_scale)
            #tmp=norm.pdf(self._R_dist_probability[:,0],loc=i,scale=self._gmm_scale)
            #plt.plot(self._R_dist_probability[:,0],tmp)


        #self._R_dist_probability[0:ecg_location_x_min,1]=0
        #self._R_dist_probability[ecg_location_x_max:,1]=0
        ##plt.figure()
        #plt.plot(self._R_dist_probability[:,0],self._R_dist_probability[:,1],'b')
        #plt.show()
        
        return self._R_dist_probability
        
    def _template_match(self,template_mask=None):
# Using the OpenCV template match to find the match place.

        if type(template_mask)==np.ndarray:
            self._template_mask = template_mask
            

        w,h = self._template_mask.shape[::-1]
        #threshold = 0.7
        self._match = cv.matchTemplate(self._green_ecg_mask,self._template_mask,cv.TM_CCORR_NORMED)
        #loc = np.where( match >= threshold)
        return self._match
        
    def _combine_match_mat_and_R_dist_prob(self,match=None,R_dist_prob = None):
# Combine R_dist_probability and match matrix

        if type(match)==np.ndarray:
            self._match = match
        if type(R_dist_prob)==np.ndarray:
            self._R_dist_probability = R_dist_prob


        template_match_mask = np.zeros(self._green_ecg_mask.shape)
        template_match_mask[0:self._match.shape[0],0:self._match.shape[1]] = self._match

        self._combine_mask = template_match_mask*self._R_dist_probability.T[1:2,:]
        
        return self._combine_mask
        
    
    def process(self, extract_data):
        """
        input the 4 dimesion of ecg roi array, this function will output the location of R wave
        
        input:
        extract_data: the 4 dimesion of ecg roi array
        
        output:
        the location of R wave
        """
        
        
        self._extract_data = extract_data

        self._get_ecg_info()

        self._get_two_yello_line_location()
        
        template_mask = self._generate_template_mask()
        
        match = self._template_match(template_mask)
        
        R_dist_prob = self._generate_gmm()
        
        combine_mask = self._combine_match_mat_and_R_dist_prob(match=match,R_dist_prob=R_dist_prob)

       
## getorder and R wave location in x axis

        ind = np.unravel_index(np.argsort(combine_mask, axis=None), combine_mask.shape)
#print(ind[0][-15::],ind[1][-15::])
#print(combine_mask[ind])
##

        r_wave_x_location = []


        new_ind_x = np.append(ind[1],[self._second_line+1])
        new_ind_y = np.append(ind[0],ind[0][-1])
        X = new_ind_x[np.arange(-1,-16,-1)].reshape((-1,1))
        clustering = DBSCAN(eps=3, min_samples=2).fit(X)
        labels = clustering.labels_
        unique_label = np.unique(labels).tolist()

        for i in unique_label:
            index = np.where(labels==i)[0][0]
            r_wave_x_location.append((new_ind_x[-1-index]-1,new_ind_y[-1-index]))
            
        return r_wave_x_location

class RWaveExtractor_IntervalMax(RWaveExtractor_Cluster):
    def __init__(self, template_width=40, denoise_thres=5, gmm_scale=25):
        
        self._template_width = template_width
        self._denoise_thres = denoise_thres
        self._gmm_scale = gmm_scale
    
    def process(self, extract_data):
        """
        input the 4 dimesion of ecg roi array, this function will output the location of R wave
        
        input:
        extract_data: the 4 dimesion of ecg roi array
        
        output:
        the location of R wave
        """
        
        
        self._extract_data = extract_data

        self._get_ecg_info()

        self._get_two_yello_line_location()
        
        template_mask = self._generate_template_mask()
        
        match = self._template_match(template_mask)
        
        R_dist_prob = self._generate_gmm()
        
        combine_mask = self._combine_match_mat_and_R_dist_prob(match=match,R_dist_prob=R_dist_prob)
 
        tolerance_pixel = 2

        rr_interval_dist = self._second_line-self._first_line+tolerance_pixel

        self._probability_center_list.sort()

        r_wave_location_dict = {}


        for i in self._probability_center_list:
            
            if i <0:
                i = 0
            if i>self._first_line:
                break
            dectect_roi_y_start = self._ecg_y_axis_center-self._ecg_y_range_upper_bound
            dectect_roi_y_end = self._ecg_y_axis_center+self._ecg_y_range_upper_bound

            dectect_roi_x_start = i-int(rr_interval_dist/2)
            dectect_roi_x_end = i+int(rr_interval_dist/2)

            if dectect_roi_x_start<0:
                dectect_roi_x_start = 0

            if dectect_roi_x_end>combine_mask.shape[1]:
                dectect_roi_x_end = combine_mask.shape[1]


            detect_interval = combine_mask[dectect_roi_y_start:dectect_roi_y_end,dectect_roi_x_start:dectect_roi_x_end]
            
            argmax_detect_interval = np.unravel_index(np.argmax(detect_interval),detect_interval.shape)

            if detect_interval[argmax_detect_interval]>=0.01:
                
                tmp_r_wave_x_loaction = dectect_roi_x_start + argmax_detect_interval[1]
                tmp_r_wave_y_loaction = dectect_roi_y_start + argmax_detect_interval[0]

                #print('-->',tmp_r_wave_x_loaction)
                #print('-->',tmp_r_wave_y_loaction)
                r_wave_location_dict[tmp_r_wave_x_loaction]=tmp_r_wave_y_loaction

            #plt.figure()
            #plt.imshow(detect_interval)
            #plt.show()

        r_wave_location_dict[self._second_line] = list(r_wave_location_dict.values())[-1]

#print(r_wave_x_loactions)
        #print(r_wave_location_dict)

        r_wave_location = [(k,v) for k,v in r_wave_location_dict.items()]
        
        
        return r_wave_location