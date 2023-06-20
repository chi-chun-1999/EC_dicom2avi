import os 
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from PyQt5 import QtWidgets
from EC_dicom2avi_ui import Ui_MainWindow
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QErrorMessage
from src.ec_ui import ECData
from src.ec_ui.show_ui import MplCanvas
import pydicom



class EC_MainWindow(QtWidgets.QMainWindow):
    def __init__(self,parent=None):

        super().__init__(parent)
        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)
        self._error_file  = []
        self._files_dict = {}

        self._mpl_canvas = MplCanvas()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self._mpl_canvas)
        self.__ui.widget_picture.setLayout(layout)

        #self.__ui.pushButton_file..connect(self.ec_func)

    def on_pushButton_file_released(self):
        files_path = QFileDialog.getOpenFileNames(self)
        for f in files_path[0]:
            file_head, file_tail = os.path.split(f)

            try:
                dcm = pydicom.dcmread(f)
                tmp_ec_data = ECData(f,file_tail,dcm)
                self._files_dict[file_tail] = tmp_ec_data
                self.__ui.listWidget_file.addItem(file_tail)
            except pydicom.errors.InvalidDicomError as e:
                print(e)
                self._error_file.append(file_tail)


        if len(self._error_file)>=1:
            print(self._error_file)
            error_file=str(self._error_file)+' is(are) NOT the DICOM file(s). Please select DICOM file.'
            
            message = QErrorMessage(self)
            message.showMessage(error_file)
        

    def on_pushButton_export_released(self):
        self._export_path = QFileDialog.getExistingDirectory(self)
        
    def on_listWidget_file_itemDoubleClicked(self):
        select_file = self.__ui.listWidget_file.currentItem().text()
        select_num = self.__ui.listWidget_file.currentIndex().row()
        print(select_num,select_file)
        print(self._files_dict[select_file]._file_path)
        self._current_show_file = self._files_dict[select_file]
        self._current_show_file.loadData()
        rgb_array_data = self._current_show_file.getRgbArray()
        print(rgb_array_data.shape)
        self._current_frame_num = 0
        self.__ui.lineEdit_current_pic.setText(str(self._current_frame_num))
        self.__ui.lineEdit_all_pic.setText(str(rgb_array_data.shape[0]))
        
        self._mpl_canvas.show_whole_frame(rgb_array_data,self._current_frame_num)

    def on_pushButton_next_pic_released(self):
        self._current_frame_num += 1
        self.__ui.lineEdit_current_pic.setText(str(self._current_frame_num))
        rgb_array_data = self._current_show_file.getRgbArray()

        self._mpl_canvas.show_whole_frame(rgb_array_data,self._current_frame_num)
        
    def on_pushButton_last_pic_released(self):
        self._current_frame_num -= 1
        self.__ui.lineEdit_current_pic.setText(str(self._current_frame_num))
        rgb_array_data = self._current_show_file.getRgbArray()

        self._mpl_canvas.show_whole_frame(rgb_array_data,self._current_frame_num)
    
    #def setCurrenctPic(self,frame):
    #    if frame<self.__ui.
        
        
        

        

        

if __name__=="__main__":
    app=QtWidgets.QApplication(sys.argv)
    main_widget = EC_MainWindow()
    main_widget.show()
    sys.exit(app.exec_())
