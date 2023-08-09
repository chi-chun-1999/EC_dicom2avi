import os 
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from PyQt5 import QtWidgets
from EC_dicom2avi_ui import Ui_MainWindow

from PyQt5.QtCore import pyqtSlot,QThread, pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QErrorMessage, QButtonGroup, QMessageBox, QProgressDialog

from src.ec_ui.show_ui import MplCanvas

import numpy as np



class TestECToolMatplot(QtWidgets.QMainWindow):
    def __init__(self,parent=None):

        super().__init__(parent)
        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)
        self._mpl_canvas = MplCanvas()
        
        self._current_whole_frame = np.load('/Users/chi-chun/institute/project/strain/test_gui_demc/ac7a6865f3/20201118/npy/KBIHSQ00_0.npy')
        
        all_frame_size_str = '/ '+str(self._current_whole_frame.shape[0])
        
        self.__ui.label_all_npy.setText(all_frame_size_str)

        # self._mpl_canvas.axes.plot([0,1,2,3,4], [10,1,20,3,40])
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self._mpl_canvas)
        self.__ui.widget_npy.setLayout(layout)
        self._current_frame = 0
        self._mpl_canvas.show_whole_frame(self._current_whole_frame,self._current_frame)
        self.__ui.lineEdit_current_npy.setText(str(self._current_frame+1))
        self._setFrameButtonEnable()
    
        
    
    def on_pushButton_next_npy_released(self):
        self._current_frame+=1
        self._mpl_canvas.show_whole_frame(self._current_whole_frame,self._current_frame)
        self.__ui.lineEdit_current_npy.setText(str(self._current_frame+1))
        self._setFrameButtonEnable()

    def on_pushButton_previous_npy_released(self):
        self._current_frame-=1
        self._mpl_canvas.show_whole_frame(self._current_whole_frame,self._current_frame)
        self.__ui.lineEdit_current_npy.setText(str(self._current_frame+1))
        self._setFrameButtonEnable()
    
    def _setFrameButtonEnable(self):
        if self._current_frame == 0:
            self.__ui.pushButton_previous_npy.setEnabled(False)
        
        else:
            self.__ui.pushButton_previous_npy.setEnabled(True)
            

        if self._current_frame == self._current_whole_frame.shape[0]-1:
            self.__ui.pushButton_next_npy.setEnabled(False)

        else:
            self.__ui.pushButton_next_npy.setEnabled(True)
        
        

    

if __name__=="__main__":
    app=QtWidgets.QApplication(sys.argv)
    main_widget = TestECToolMatplot()
    main_widget.show()
    sys.exit(app.exec_())

