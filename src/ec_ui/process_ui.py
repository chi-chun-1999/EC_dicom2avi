import os 
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.image_process.cycle import ExtractMulitCycle
import pydicom
import re
import time 
import json
import numpy as np
import abc
from PyQt5.QtCore import QThread,pyqtSignal,pyqtSlot
from PyQt5 import QtCore


class NumpyEncoder(json.JSONEncoder):
    """ Custom encoder for numpy data types """
    def default(self, obj):
        if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
                            np.int16, np.int32, np.int64, np.uint8,
                            np.uint16, np.uint32, np.uint64)):

            return int(obj)

        elif isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
            return float(obj)

        elif isinstance(obj, (np.complex_, np.complex64, np.complex128)):
            return {'real': obj.real, 'imag': obj.imag}

        elif isinstance(obj, (np.ndarray,)):
            return obj.tolist()

        elif isinstance(obj, (np.bool_)):
            return bool(obj)

        elif isinstance(obj, (np.void)): 
            return None

        return json.JSONEncoder.default(self, obj)

class ExtractDataThread(QThread):
    # Using signal to get data is too slow. Finally, I use the class method to get self variable.
    # signal_three_dim_file = pyqtSignal(list)
    # signal_extract_file = pyqtSignal(list)
    # signal_outcome = pyqtSignal(int,list,list)
    
    def __init__(self,thread_num,split_file_dict:dict,export_root_path:str,export_data:str,export_whole=True,fps=30,parent=None,ocr_weight_path = '../config/template_number.npy'):
        QtCore.QThread.__init__(self, parent)
        self._split_file_dict =split_file_dict
        self._export_root_path = export_root_path
        self._export_data = export_data
        self._export_whole = export_whole
        self._fps = fps
        self._thread_num = thread_num
        self._ocr_weight_path = ocr_weight_path
    
        self._three_dim_dicom_file = []
        self._extract_info = []

    def run(self):
        for key, f in self._split_file_dict.items():
            extract_multi_cycle = ExtractMulitCycle(f.getPath(),ocr_weight_path=self._ocr_weight_path)
            print('=======Process %s======'%(extract_multi_cycle._file_name))

            try:
                extract_multi_cycle.extractCycle()
            except ValueError as err:
                print("Warning:",err)
                self._three_dim_dicom_file.append(key)
            except pydicom.errors.InvalidDicomError as err:

                print("Error:",'\'%s\' is not dicom file. Please input DICOM file.'%(f))
                return
        
            else:

                if self._export_data=='all':
                    if self._export_whole:
                        extract_multi_cycle.exportWholeNpy(self._export_root_path)
                        extract_multi_cycle.exportWholeAvi(self._export_root_path,fps=self._fps)
                    extract_multi_cycle.exportNpy(self._export_root_path)
                    extract_multi_cycle.exportAvi(self._export_root_path,fps=self._fps)
                elif self._export_data=='npy':
                    if self._export_whole:
                        extract_multi_cycle.exportWholeNpy(self._export_root_path)
                    extract_multi_cycle.exportNpy(self._export_root_path)
                elif self._export_data=='avi':
                    if self._export_whole:
                        extract_multi_cycle.exportWholeAvi(self._export_root_path,fps=self._fps)
                    extract_multi_cycle.exportAvi(self._export_root_path,fps=self._fps)

                self._extract_info.append(extract_multi_cycle.exportExtractInfo())
        
        # self._extract_info = [1,2,3,4,6]
        # self._three_dim_dicom_file = [1,2,3,14,6]
        
        # print(type(self._extract_info))
        # print(type(self._three_dim_dicom_file))
                
        
        # self.signal_extract_file.emit(self._extract_info)
        # self.signal_three_dim_file.emit(self._three_dim_dicom_file)
        # self.signal_outcome.emit(self._thread_num,self._extract_info,self._three_dim_dicom_file)
    
    def getOutcome(self):
        return self._thread_num,self._extract_info,self._three_dim_dicom_file


def StartExtractData(file_dict:dict,export_path:str,export_data:str,export_whole=True, fps=30):
    """

    The function in the user interface (UI) for extracting data using ExtractMultiCycle.
    
    input: 
    file_dict: the python dictionary the key is file name and the content is ECData
    export_path: the path to store extract data
    export_data: 'all', 'avi', 'npy'
    export_whole: export all dicom array data
    fps: the fps for avi file

    return:
    demc_info: the information for extraction
    
    """

    process_time = time.ctime()
    three_dim_dicom_file = []
    demc_info = {"process_time":process_time,"process_file_num":0,"process_file_info":[]}
    fps = 30
    
    for key, f in file_dict.items():
        extract_multi_cycle = ExtractMulitCycle(f.getPath())
        
        print('=======Process %s======'%(extract_multi_cycle._file_name))

        try:
            extract_multi_cycle.extractCycle()
        except ValueError as err:
            print("Warning:",err)
            three_dim_dicom_file.append(key)
        except pydicom.errors.InvalidDicomError as err:

            print("Error:",'\'%s\' is not dicom file. Please input DICOM file.'%(f))
            return
        
        else:

            if export_data=='all':
                if export_whole:
                    extract_multi_cycle.exportWholeNpy(export_path)
                    extract_multi_cycle.exportWholeAvi(export_path,fps=fps)
                extract_multi_cycle.exportNpy(export_path)
                extract_multi_cycle.exportAvi(export_path,fps=fps)
            elif export_data=='npy':
                if export_whole:
                    extract_multi_cycle.exportWholeNpy(export_path)
                extract_multi_cycle.exportNpy(export_path)
            elif export_data=='avi':
                if export_whole:
                    extract_multi_cycle.exportWholeAvi(export_path,fps=fps)
                extract_multi_cycle.exportAvi(export_path,fps=fps)
            demc_info['process_file_num']+=1
            demc_info['process_file_info'].append(extract_multi_cycle.exportExtractInfo())
        

    if export_path[-1]!='/':
        export_path+='/'
    
    demc_info_file_path =  export_path+'demc_info.json'
    with open(demc_info_file_path, 'w') as f:
      f.write(json.dumps(demc_info, indent = 4,cls=NumpyEncoder))
    
    return demc_info,three_dim_dicom_file
    


class UiExtractDataAbs(QtCore.QObject):
    def __init__(self,file_dict:dict,export_root_path:str,export_data:str,export_whole=True,fps=30):
        """
        Using the origin method without multi thread to extract data
        input: 
        file_dict: the python dictionary the key is file name and the content is ECData
        export_path: the path to store extract data
        export_data: 'all', 'avi', 'npy'
        export_whole: export all dicom array data
        fps: the fps for avi file
        """
        super().__init__()
        
        self._file_dict = file_dict
        self._export_root_path = export_root_path
        self._export_data = export_data
        self._export_whole = export_whole
        self._fps = fps
        self._demc_info = {}
    
    def startExtractData(self):
        pass
    
    def exportDecmInfo(self):
        if self._export_root_path[-1]!='/':
            self._export_root_path+='/'
        
        demc_info_file_path =  self._export_root_path+'demc_info.json'
        # print('----------->',demc_info_file_path)
        with open(demc_info_file_path, 'w') as f:
          f.write(json.dumps(self._demc_info, indent = 4,cls=NumpyEncoder))
        
    
class OriExtractData(UiExtractDataAbs):
    def __init__(self,file_dict:dict,export_root_path:str,export_data:str,export_whole=True,fps=30):
        """
        Using the origin method without multi thread to extract data
        input: 
        file_dict: the python dictionary the key is file name and the content is ECData
        export_path: the path to store extract data
        export_data: 'all', 'avi', 'npy'
        export_whole: export all dicom array data
        fps: the fps for avi file
        """
        super().__init__(file_dict,export_root_path,export_data,export_whole,fps)
        
        # print(self._file_dict)
        # print(self._export_data)
        
    
    def startExtractData(self):
        process_time = time.ctime()
        self._three_dim_dicom_file = []
        self._demc_info = {"process_time":process_time,"process_file_num":0,"process_file_info":[]}

        for key, f in self._file_dict.items():
            extract_multi_cycle = ExtractMulitCycle(f.getPath())
            
            print('=======Process %s======'%(extract_multi_cycle._file_name))

            try:
                extract_multi_cycle.extractCycle()
            except ValueError as err:
                print("Warning:",err)
                self._three_dim_dicom_file.append(key)
            except pydicom.errors.InvalidDicomError as err:

                print("Error:",'\'%s\' is not dicom file. Please input DICOM file.'%(f))
                return
            
            else:

                if self._export_data=='all':
                    if self._export_whole:
                        extract_multi_cycle.exportWholeNpy(self._export_root_path)
                        extract_multi_cycle.exportWholeAvi(self._export_root_path,fps=self._fps)
                    extract_multi_cycle.exportNpy(self._export_root_path)
                    extract_multi_cycle.exportAvi(self._export_root_path,fps=self._fps)
                elif self._export_data=='npy':
                    if self._export_whole:
                        extract_multi_cycle.exportWholeNpy(self._export_root_path)
                    extract_multi_cycle.exportNpy(self._export_root_path)
                elif self._export_data=='avi':
                    if self._export_whole:
                        extract_multi_cycle.exportWholeAvi(self._export_root_path,fps=self._fps)
                    extract_multi_cycle.exportAvi(self._export_root_path,fps=self._fps)
                self._demc_info['process_file_num']+=1
                self._demc_info['process_file_info'].append(extract_multi_cycle.exportExtractInfo())
        
        self.exportDecmInfo()
        

        return self._demc_info,self._three_dim_dicom_file

# class MultiThreadExtractData(QtCore.QObject,metaclass=UiExtractDataAbs):
class MultiThreadExtractData(UiExtractDataAbs):
    def __init__(self, file_dict: dict, export_root_path: str, export_data: str, export_whole=True, fps=30,thread_num=3,ocr_weight_path = '../config/template_number.npy'):
        
        # QtCore.QObject.__init__(self)
        super().__init__(file_dict, export_root_path, export_data, export_whole, fps)
        self._thread_num  = thread_num
        self._extract_data_threads=[]
        self._three_dim_dicom_file = []
        self._demc_info={}
        self._ocr_weight_path = ocr_weight_path
        
        split_thread_files = self.splitFiles()

        for i in range(self._thread_num):
            self._extract_data_threads.append(ExtractDataThread(i,split_thread_files[i],self._export_root_path,self._export_data,self._export_whole,self._fps,ocr_weight_path=self._ocr_weight_path))
        
    def splitFiles(self):
        file_num = len(self._file_dict)
        

        split_num = [file_num//self._thread_num for i in range(self._thread_num)]

        for i in range(file_num%self._thread_num):
            split_num[i] = split_num[i]+1


        slice_start = 0
        slice_end = 0
        split_thread_files = []
        for i in split_num:
            slice_end=slice_start+i
            split_thread_files.append(dict(list(self._file_dict.items())[slice_start:slice_end]))
            slice_start = slice_end
        
        # print(split_thread_files)
        return split_thread_files

    
    def getOutcome(self):
        for thread in self._extract_data_threads:
            thread_num, demc_info, three_dim = thread.getOutcome()
            self._demc_info['process_file_info'].extend(demc_info)
            self._three_dim_dicom_file.extend(three_dim)
            # self._test.extend(demc_info)
        
        return self._demc_info,self._three_dim_dicom_file

    def threadWait(self):
        for thread in self._extract_data_threads:
            thread.wait()
    
    def startExtractData(self):

        process_time = time.ctime()
        self._three_dim_dicom_file = []
        self._demc_info = {"process_time":process_time,"process_file_num":0,"process_file_info":[]}

        for i in range(len(self._extract_data_threads)):
            self._extract_data_threads[i].start()


        # for thread in self._extract_data_threads:
        #     thread.wait()

        # self.exportDecmInfo()
        # self.getOutcome()
        # print(self._demc_info)
        # print(self._three_dim_dicom_file)

        # return self._demc_info,self._three_dim_dicom_file
        return
