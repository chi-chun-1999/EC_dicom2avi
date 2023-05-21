import os 
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pydicom

from image_process import *

class ECData():
    def __init__(self,file_path,file_name,dcm) -> None:
        self._file_path = file_path
        self._file_name = file_name
        self._dcm = dcm
        
    def __str__(self) -> str:
        return self._file_name