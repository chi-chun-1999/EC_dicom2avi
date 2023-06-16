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
        export_file_path = "%s%s_%s_%d.%s"%(export_dir,self._file_name,type(self).__name__,idx,file_name_extension)
        
        return export_file_path
    
    def createOutputDir(self, export_dir):

        if os.path.isdir(export_dir)==False:
            os.makedirs(export_dir)
    

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

            
class ExtractMulitCycle(CycleAbstract):
    def __init__(self, dicom_file_path,red_extractor = None,r_wave_extractor=None) -> None:
        super().__init__(dicom_file_path)
        
        if red_extractor ==None:
            self._red_extractor = RedExtractor()
        else:
            self._red_extractor = red_extractor
        if r_wave_extractor ==None:
            self._r_wave_extractor = RWaveExtractor_IntervalMax()
        else:
            self._r_wave_extractor = r_wave_extractor
    
    def extractCycle(self):


        dcm = pydicom.read_file(self._dicom_file_path)

        if dcm.pixel_array.ndim!=4:
            input_dicom_dim = dcm.pixel_array.ndim
            error_str = "The dicom file of "+self._file_name+' msut be 4 dimesion array, but getting '+str(input_dicom_dim)+'.'
            raise ValueError(error_str)

        dcm_rgb_array =  getRgbArray(dcm)
        dcm_bgr_array = dcm_rgb_array[:,:,:,::-1]
        

#plt.imshow(video_array[1,350:,0:318,:])

        ecg_roi =getECGRoi_FixSize(dcm_bgr_array,[350,434,0,400]) 

        red_mask = self._red_extractor.process(ecg_roi)
        red_argwhere = np.argwhere(red_mask)

        r_wave_location = self._r_wave_extractor.process(ecg_roi)

        #show_R_wave_place(ecg_roi,r_wave_location)
        match_frame =[]

        for i in r_wave_location:
            red_match_r_wave = red_argwhere[red_argwhere[:,2]==i[0]]
            bias = 0 
            while(red_match_r_wave.size==0):
                bias+=1
                red_match_r_wave = red_argwhere[red_argwhere[:,2]==i[0]-bias]
                if red_match_r_wave.size!=0:
                    break
                
                red_match_r_wave = red_argwhere[red_argwhere[:,2]==i[0]+bias]
            
            match_frame.append(red_match_r_wave[0,0])
            
        for i in range(len(match_frame)-1):
            tmp_cycle_data = dcm_rgb_array[match_frame[i]:match_frame[i+1],:,:,:]
            self._cycle_data.append(tmp_cycle_data)
                    
        #print(match_frame)
        
        