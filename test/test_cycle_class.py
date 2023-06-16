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

files_4d = ['../../dataset/test/H/GEMS_IMG/2020_NOV/18/__174122/KBIHSSH2',
 '../../dataset/test/H/GEMS_IMG/2020_NOV/18/__174122/KBIHST1G',
 '../../dataset/test/H/GEMS_IMG/2020_NOV/18/__174122/KBIHSSH4',
 '../../dataset/test/H/GEMS_IMG/2020_NOV/18/__174122/KBIHSQ00',
 '../../dataset/test/H/GEMS_IMG/2020_NOV/18/__174122/KBIHSS8S',
 '../../dataset/test/H/GEMS_IMG/2020_NOV/18/__174122/KBIHST9M',
 '../../dataset/test/H/GEMS_IMG/2020_NOV/18/__174122/KBIHST9K',
 '../../dataset/test/H/GEMS_IMG/2020_NOV/18/__174122/KBIHSR8G',
 '../../dataset/test/H/GEMS_IMG/2020_NOV/18/__174122/KBIHSR8I',
 '../../dataset/test/H/GEMS_IMG/2020_NOV/18/__174122/KBIHST1C',
 '../../dataset/test/H/GEMS_IMG/2020_NOV/18/__174122/KBIHST1E',
 '../../dataset/test/H/GEMS_IMG/2020_NOV/18/__174122/KBIHSSPA',
 '../../dataset/test/H/GEMS_IMG/2020_NOV/18/__174122/KBIHSS90',
 '../../dataset/test/H/GEMS_IMG/2020_NOV/18/__174122/KBIHSSP8',
 '../../dataset/test/H/GEMS_IMG/2020_NOV/18/__174122/KBIHSSP6',
 '../../dataset/test/H/GEMS_IMG/2020_NOV/18/__174122/KBIHSTHO',
 '../../dataset/test/H/GEMS_IMG/2020_NOV/18/__174122/KBIHSQO2',
 '../../dataset/test/H/GEMS_IMG/2020_NOV/18/__174122/KBIHSR0C',
 '../../dataset/test/H/GEMS_IMG/2020_NOV/18/__174122/KBIHST9I',
 '../../dataset/test/H/GEMS_IMG/2020_NOV/18/__174122/KBIHSR0E']

#%%

class TestCycle(TestCase):
    @patch.multiple(CycleAbstract,__abstractmethods__=set())
    def test_file_path(self):
        cycle_abstract = CycleAbstract('../data_video/KBIHSQ00.avi')
        cycle_abstract._cycle_data = np.zeros((2,3,3,3))
        cycle_abstract.exportAvi()
        cycle_abstract.exportNpy()
    


test_cycle = TestCycle()
test_cycle.test_file_path()
#%%
class TestMultiCycle(TestCase):
    def test_extract_cycle(self):
        self.extract_multi_cycle = ExtractMulitCycle(files_4d[1])
        self.extract_multi_cycle.extractCycle()
        multi_cycle_lists = self.extract_multi_cycle.getCycle()
        print(len(multi_cycle_lists))
        print(multi_cycle_lists[0].shape)
        #matplot_show_video(multi_cycle_lists[0])
    def test_export_data(self):
        self.extract_multi_cycle.exportAvi()
        self.extract_multi_cycle.exportNpy()
        

test_cycle = TestMultiCycle()
test_cycle.test_extract_cycle()
test_cycle.test_export_data()

# %%
