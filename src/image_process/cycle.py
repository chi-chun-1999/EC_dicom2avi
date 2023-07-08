import cv2 as cv
import os

import numpy as np
import abc
import matplotlib.pyplot as plt
from .frame import denoiseEco
import math
from .feature import FeatureExtractor, RedExtractor, RWaveExtractor_IntervalMax
from .video import array2avi
from .frame import getRgbArray, getECGRoi_FixSize
import pydicom
import pandas as pd
from src.image_process.ocr import HeartRateOCR, NumberOCR_Template
from src.image_process.feature import RRIntervalExtractor
from src.image_process.frame import getPixelMs
from src.exception.value_exception import MultiCycleExtractError


class CycleAbstract(abc.ABC):
    def __init__(self,dicom_file_path) -> None:
        self.setDicomFilePath(dicom_file_path)
        self._cycle_data = []
    
    def setDicomFilePath(self,dicom_file_path):
        self._dicom_file_path = dicom_file_path
        head, tail = os.path.split(dicom_file_path)
        self._file_name, file_name_extension = os.path.splitext(tail)
        
    @abc.abstractmethod
    def extractCycle(self):
        raise NotImplementedError

    def getCycle(self):
        return self._cycle_data
    
    def _exportFilePath(self,file_name_extension,idx,export_dir = './'):
        #export_file_path = export_dir+self._file_name+'_'+__class__.__name__+'_'+str(idx)+'.'+file_name_extension
        if idx!=-1:
            export_file_path = "%s%s_%s_%d.%s"%(export_dir,self._file_name,type(self).__name__,idx,file_name_extension)
        else:
            whole_str = 'whole'
            export_file_path = "%s%s_%s.%s"%(export_dir,self._file_name,whole_str,file_name_extension)
            
        return export_file_path
    
    def createOutputDir(self, export_dir):

        if os.path.isdir(export_dir)==False:
            os.makedirs(export_dir)
    
    def exportWholeNpy(self,export_dir=None):
        if export_dir == None:
            export_dir = './'+self._file_name+'/'
            
        else:
            if export_dir[-1]!='/':
                export_dir+='/'
            export_dir+=self._file_name+'/'

        self.createOutputDir(export_dir)
        export_file_path = self._exportFilePath('npy',-1,export_dir)
        np.save(export_file_path,self._dcm_rgb_array)

    def exportWholeAvi(self,export_dir=None,fps=30):
        if export_dir == None:
            export_dir = './'+self._file_name+'/'
            
        else:
            if export_dir[-1]!='/':
                export_dir+='/'
            export_dir+=self._file_name+'/'

        self.createOutputDir(export_dir)
        export_file_path = self._exportFilePath('avi',-1,export_dir)
        array2avi(self._dcm_rgb_array,export_file_path,fps=fps,numpy_channel=True)

        

    def exportNpy(self,export_dir = None):
        if export_dir == None:
            export_dir = './'+self._file_name+'/npy/'
            
        else:
            if export_dir[-1]!='/':
                export_dir+='/'
            export_dir+=self._file_name+'/npy/'

        self.createOutputDir(export_dir)
                
        for i in range(len(self._cycle_data)):
            export_file_path = self._exportFilePath('npy',i,export_dir)
            np.save(export_file_path,self._cycle_data[i])

    def exportAvi(self,export_dir = None,fps = 30):

        if export_dir == None:
            export_dir = './'+self._file_name+'/avi/'
            
        else:
            if export_dir[-1]!='/':
                export_dir+='/'
            export_dir+=self._file_name+'/avi/'

        self.createOutputDir(export_dir)
            
        for i in range(len(self._cycle_data)):
            export_file_path = self._exportFilePath('avi',i,export_dir)
            #print(export_file_path)
            
            array2avi(self._cycle_data[i],export_file_path,fps=fps,numpy_channel=True)
        
    @abc.abstractmethod
    def exportExtractInfo(self):
        raise NotImplementedError
        
            
class ExtractMulitCycle(CycleAbstract):
    def __init__(self, dicom_file_path,red_extractor = None,r_wave_extractor=None,ocr_weight_path='../config/template_number.npy') -> None:
        super().__init__(dicom_file_path)
        
        if red_extractor ==None:
            self._red_extractor = RedExtractor()
        else:
            self._red_extractor = red_extractor
        if r_wave_extractor ==None:
            self._r_wave_extractor = RWaveExtractor_IntervalMax()
        else:
            self._r_wave_extractor = r_wave_extractor
            
        # Unregular Interval detect init
        
        self._ocr_weight_path = ocr_weight_path
        
        template = np.load(self._ocr_weight_path)

        self._number_ocr = NumberOCR_Template(template)
        self._heart_rate_ocr = HeartRateOCR(self._number_ocr)
    
    def extractCycle(self):

        self._unregualr_rr_interval = False

        dcm = pydicom.read_file(self._dicom_file_path)

        if dcm.pixel_array.ndim!=4:
            input_dicom_dim = dcm.pixel_array.ndim
            error_str = "The dicom file of "+self._file_name+' msut be 4 dimesion array, but getting '+str(input_dicom_dim)+'.'
            raise ValueError(error_str)

        self._dcm_rgb_array =  getRgbArray(dcm)
        dcm_bgr_array = self._dcm_rgb_array[:,:,:,::-1]
        

#plt.imshow(video_array[1,350:,0:318,:])

        ecg_roi =getECGRoi_FixSize(dcm_bgr_array,[350,434,0,400]) 

        red_mask = self._red_extractor.process(ecg_roi)
        red_argwhere = np.argwhere(red_mask)

        self._r_wave_location = self._r_wave_extractor.process(ecg_roi)
        
        

        #show_R_wave_place(ecg_roi,r_wave_location)
        self._match_frame =[]

        for i in self._r_wave_location:
            red_match_r_wave = red_argwhere[red_argwhere[:,2]==i[0]]
            bias = 0 
            while(red_match_r_wave.size==0):
                bias+=1
                red_match_r_wave = red_argwhere[red_argwhere[:,2]==i[0]-bias]
                if red_match_r_wave.size!=0:
                    break
                
                red_match_r_wave = red_argwhere[red_argwhere[:,2]==i[0]+bias]

                if bias >=500:
                    raise MultiCycleExtractError(self._dicom_file_path)
            
            self._match_frame.append(int(red_match_r_wave[0,0]))
            
        for i in range(len(self._match_frame)-1):
            tmp_cycle_data = self._dcm_rgb_array[self._match_frame[i]:self._match_frame[i+1],:,:,:]
            self._cycle_data.append(tmp_cycle_data)
                    
        self._unregualr_rr_interval = self.detectUnregular_RRInterval()
        #print(match_frame)
        
    def detectUnregular_RRInterval(self):
       
        
        first_line = self._r_wave_location[-2][0] 
        second_line = self._r_wave_location[-1][0] 
        rr_interval_pixel = second_line-first_line

        cycle_start = self._match_frame[-2]
        cycle_end = self._match_frame[-1]
        detect_frame = self._dcm_rgb_array[int((cycle_start+cycle_end)/2)]
        
        heart_rate = self._heart_rate_ocr.fit(detect_frame)
        pixel_ms = getPixelMs(rr_interval_pixel,heart_rate)
        
        
         
        for i in range(len(self._r_wave_location)-1):
            
            
            tmp_rr_interval_pixel = self._r_wave_location[i+1][0]-self._r_wave_location[i][0]
            
            tmp_rr_interval_ms = tmp_rr_interval_pixel*pixel_ms
            # print(tmp_rr_interval_ms)
            
            #if self._r_wave_location[i+1][0] -self._r_wave_location[i][0]>=90:
            #   
            #    print("Warnning: Detect unregular RR interval length.")
            #    return True

            #elif self._r_wave_location[i+1][0] -self._r_wave_location[i][0]<=40:
            #    print("Warnning: Detect unregular RR interval length.")
            #    return True
            if tmp_rr_interval_ms > 1200:
                print("Warnning: Detect unregular RR interval length.")
                return True
            elif tmp_rr_interval_ms < 600:
                print("Warnning: Detect unregular RR interval length.")
                return True
                

        return False
    
    def exportExtractInfo(self):
        
        r_wave_location_dict = []

        for i in self._r_wave_location:
            r_wave_location_dict.append({'x':i[0],'y':i[1]})
            

        self._extract_info = {}
        self._extract_info['Name'] = self._file_name
        self._extract_info['R_wave_location'] = r_wave_location_dict
        self._extract_info['extract_frame'] = self._match_frame
        self._extract_info['unregular_rr_interval'] = self._unregualr_rr_interval
        
        #print(self._extract_info)
        
        return self._extract_info
        
        
        