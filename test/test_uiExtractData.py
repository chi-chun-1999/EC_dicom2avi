#%%
import os 
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from unittest import TestCase
from unittest.mock import patch

from src.ec_ui.process_ui import *
from src.ec_ui.ec_ui_data import ECData
import glob
from PyQt5 import QtCore

class TestExtract(TestCase):
    @patch.multiple(OriExtractData,__abstractmethods__=set())
    def testOriExtractData(self):
        
        file_path = '../../dataset/test/__174122/KBIHSQO2'
        export_root_path = '../../test_gui_demc/'
        export_data = 'all'
        file_head, file_tail = os.path.split(file_path)
        dcm = pydicom.dcmread(file_path)
        
        ec_data = ECData(file_path, file_tail,dcm)
        
        file_dict = {}
        file_dict[file_tail] = ec_data
        
        ori_extract_data = OriExtractData(file_dict,export_root_path,export_data)
        demc_info, three_dim_data = ori_extract_data.startExtractData()
        
        print(demc_info)
        print(three_dim_data)
    def testMultiExtractData_splitFiles(self):
        data_dir = '../../dataset/test/__174122/*'
        export_root_path = '../../test_gui_demc/'
        export_data = 'all'
        dicom_files = glob.glob(data_dir)
        print(len(dicom_files))
        file_dict={}
        for f in dicom_files:
            file_head, file_tail = os.path.split(f)
            dcm = pydicom.dcmread(f)
            
            ec_data = ECData(f, file_tail,dcm)
            file_dict[file_tail] = ec_data
            
        # file_dict.popitem()
        # file_dict.popitem()
        # file_dict.popitem()
        
        ori_extract_data = MultiThreadExtractData(file_dict,export_root_path,export_data,thread_num=3)
        split_list = ori_extract_data.splitFiles()
        return split_list
    def testMultiExtractData_startExtractData(self):
        app = QtCore.QCoreApplication(sys.argv)
        data_dir = '../../dataset/test/__174122/*'
        export_root_path = '../../test_gui_demc/'
        export_data = 'None'
        dicom_files = glob.glob(data_dir)
        print(len(dicom_files))
        file_dict={}
        for f in dicom_files:
            file_head, file_tail = os.path.split(f)
            dcm = pydicom.dcmread(f)
            
            ec_data = ECData(f, file_tail,dcm)
            file_dict[file_tail] = ec_data
            
        # file_dict.popitem()
        # file_dict.popitem()
        # file_dict.popitem()
        

        ori_extract_data = MultiThreadExtractData(file_dict,export_root_path,export_data,thread_num=5)
        
        # ori_extract_data._setConnection()
        demc_info, three_dim_data = ori_extract_data.startExtractData()
        print(demc_info)
        print(three_dim_data)
        app.exit()
        # sys.exit(app.exit())

    def testMultiExtractData_getOutcome(self):
        app = QtCore.QCoreApplication(sys.argv)
        data_dir = '../../dataset/test/__174122/*'
        export_root_path = '../../test_gui_demc/'
        export_data = 'None'
        dicom_files = glob.glob(data_dir)
        print(len(dicom_files))
        file_dict={}
        for f in dicom_files:
            file_head, file_tail = os.path.split(f)
            dcm = pydicom.dcmread(f)
            
            ec_data = ECData(f, file_tail,dcm)
            file_dict[file_tail] = ec_data
            
        # file_dict.popitem()
        # file_dict.popitem()
        # file_dict.popitem()
        

        self._ori_extract_data = MultiThreadExtractData(file_dict,export_root_path,export_data,thread_num=5)
        
        # ori_extract_data._setConnection()
        self._ori_extract_data.startExtractData()
        
        print_outcome_thread = QThread()
        print_outcome_thread.run=self.printOutcome
        print_outcome_thread.start()
        
        print('-----main thread----')
        
        print_outcome_thread.wait()

        app.exit()
    
    def printOutcome(self):
        self._ori_extract_data.threadWait()
        demc_info,three_dim_file = self._ori_extract_data.getOutcome()
        print('-----print outcome thread----')
        print(demc_info)
        print(three_dim_file)
        
    
    


test_extract = TestExtract()
# test_extract.testOriExtractData()
# demc_info,three_dim_dicom_file = test_extract.testMultiExtractData_startExtractData()
test_extract.testMultiExtractData_getOutcome()

# print(demc_info)
# print(three_dim_dicom_file)

# for i in split_list:
#     print(len(i))
# print(len(split_list[1]))
# print(len(split_list[2]))
    



# %%
