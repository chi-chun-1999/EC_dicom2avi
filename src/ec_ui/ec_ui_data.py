import os 
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pydicom

from image_process import *
from src.image_process.frame import getRgbArray

class ECData():
    def __init__(self,file_path,file_name,dcm) -> None:
        self._file_path = file_path
        self._file_name = file_name
        self._dcm = dcm
        
    def __str__(self) -> str:
        return self._file_name

    def loadData(self):
        dcm = pydicom.read_file(self._file_path)
        self._dcm_rgb_array =  getRgbArray(dcm)
    
    def getRgbArray(self):
        return self._dcm_rgb_array

    def getPath(self):
        return self._file_path
    
    @property
    def file_name(self):
        return self._file_name

    @property
    def file_path(self):
        return self._file_path

    def __str__(self) -> str:
        name = 'ECData('+self.file_name+')'
        return name
    
    def __repr__(self) -> str:
        name = 'ECData('+self.file_name+')'
        return name

class DirData():
    def __init__(self,dir_path,dir_name) -> None:
        self.__dir_path = dir_path
        self.__dir_name = dir_name
    
    @property
    def dir_path(self):
        return self.__dir_path

    @property
    def dir_name(self):
        return self.__dir_name
    
    def __str__(self) -> str:
        name = 'DirData('+self.dir_name+')'
        return name
    
    def __repr__(self) -> str:
        name = 'DirData('+self.dir_name+')'
        return name
    

    