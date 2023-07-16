import os 
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from configWidget_ui import Ui_Form
from PyQt5.QtCore import pyqtSlot,QThread, pyqtSignal
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtWidgets


class ConfigWindow(QtWidgets.QWidget):
    _config_signal = pyqtSignal(dict)
    def __init__(self,thread_num=3,ocr_weight_path = '../config/template_number.npy',parent=None) -> None:
        super().__init__(parent)
        self.__ui = Ui_Form()
        self.__ui.setupUi(self)
        self._config_dict = {}
        self._config_dict['thread_num'] = thread_num 
        self._config_dict['ocr_weight_path'] = ocr_weight_path
        
        
        thread_min = 3
        thread_max = 15
        self.__ui.spinBox_thread_num.setValue(thread_num)
        self.__ui.spinBox_thread_num.setRange(thread_min,thread_max)
        self.__ui.lineEdit_ocr_weight_path.setText(ocr_weight_path)
        self._config_signal.emit(self._config_dict)
    
    def on_pushButton_open_ocr_weight_released(self):

        file_dialog = QFileDialog(self)
        
        files_path = file_dialog.getOpenFileName(self,filter ="Weight File (*.npy)" )
        self.__ui.lineEdit_ocr_weight_path.setText(files_path[0])
        self._config_dict['ocr_weight_path'] = files_path[0]
    
    @pyqtSlot(int)
    def on_spinBox_thread_num_valueChanged(self,value):
        self._config_dict['thread_num'] = value 
    
    def on_pushButton_cancel_released(self):
        self.close()

    def on_pushButton_ok_released(self):
        self._config_signal.emit(self._config_dict)
        self.close()
    
    @property
    def config_dict(self):
        return self._config_dict
    

        
        
        
