#%%
import os 
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from src.image_process.feature import *
from src.image_process.frame import *
import pydicom
import cv2 as cv
import numpy as np
#import SimpleITK as sitk
import matplotlib.pyplot as plt
from typing import Type
#from image_process import *

from src.show.matplot_show import matplot_show_video,show_R_wave_place
from src.image_process.cycle import *


import glob

from unittest import TestCase
from unittest.mock import patch
from src.ec_ui.export_ui import OutcomeTreeExportData
import json

# %%
#data_dir = '../../dataset/test/H/GEMS_IMG/2020_NOV/18/__174122/*'
#
#print(glob.glob(data_dir))
#dicom_files = glob.glob(data_dir)
#
#files_4d = []
#for f in dicom_files:
#    dcm = pydicom.dcmread(f)
#    array_data = dcm.pixel_array
#    if array_data.ndim == 4:
#        #head,file_name = os.path.split(f)
#        files_4d.append(f)

files_4d = ['../../dataset/test/__174122/KBIHSSH2',
#  '../../dataset/test/__174122/KBIHST1G',
#  '../../dataset/test/__174122/KBIHSSH4',
#  '../../dataset/test/__174122/KBIHSQ00',
#  '../../dataset/test/__174122/KBIHSS8S',
#  '../../dataset/test/__174122/KBIHST9M',
#  '../../dataset/test/__174122/KBIHST9K',
 '../../dataset/test/__174122/KBIHSR0E']

ec_datas = []
for f in files_4d:
    head,tail = os.path.split(f)
    dcm = pydicom.read_file(f)
    ec_datas.append(ECData(f,tail,dcm))

#%%
class TestMultiCycleAndOutcomeTree(TestCase):
    def __init__(self):
        # self.extract_multi_cycle = ExtractMulitCycle(ec_datas[3])
        
        self.export_data = OutcomeTreeExportData('../../test_gui_demc/')
        #file_path = '../../dataset/test/H/GEMS_IMG/2020_NOV/18/__174122/KBIHSR06'
        #self.extract_multi_cycle = ExtractMulitCycle(file_path)
        # self.extract_multi_cycle.extractCycle()
        # multi_cycle_lists = self.extract_multi_cycle.getCycle()
        #print(len(multi_cycle_lists))
        #print(multi_cycle_lists[0].shape)
        #matplot_show_video(multi_cycle_lists[0])
        # plt.imshow(multi_cycle_lists[0][0])

    def test_export_data(self):
        self.extract_multi_cycle.exportAvi()
        self.extract_multi_cycle.exportNpy()

    def test_detect_unregular_r_wave(self):
        print(self.extract_multi_cycle.detectUnregular_RRInterval())
    
    def test_extract_info(self):
        return self.extract_multi_cycle.exportExtractInfo()
    
    def addProcessFile(self):
        for e in ec_datas:
            self.extract_multi_cycle = ExtractMulitCycle(e,self.export_data)
            self.extract_multi_cycle.extractCycle()
            export_extract_info = self.extract_multi_cycle.exportExtractInfo()
            self.export_data.addProcessFile(e,export_extract_info)
            self.extract_multi_cycle.exportAvi()
            self.extract_multi_cycle.exportNpy()
            self.extract_multi_cycle.exportWholeAvi()
            self.extract_multi_cycle.exportWholeNpy()
            # self.export_data.exportDecmInfo()
        print(self.export_data.to_data_frame())
            
            # export_path = self.export_data.ECDataGetExportPath(e,'npy',-1)
            
            # print(export_path)


        # print(self.export_data.to_dict())
        # print(json.dumps(self.export_data.to_dict(),indent=4))
            
        # export_extract_file = self.extract_multi_cycle.exportExtractInfo()

        

        

test_cycle = TestMultiCycleAndOutcomeTree()
test_cycle.addProcessFile()
#test_cycle.test_export_data()
# test_cycle.test_detect_unregular_r_wave()

# extract_info = test_cycle.test_extract_info()

# %%
