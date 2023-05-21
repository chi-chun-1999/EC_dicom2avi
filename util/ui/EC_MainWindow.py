import os 
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from PyQt5 import QtWidgets
from EC_dicom2avi_ui import Ui_MainWindow
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QErrorMessage
from ec_ui import ECData
import pydicom



class EC_MainWindow(QtWidgets.QMainWindow):
    def __init__(self,parent=None):

        super().__init__(parent)
        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)
        self._error_file  = []
        #self.__ui.pushButton_file..connect(self.ec_func)

    def on_pushButton_file_released(self):
        files_path = QFileDialog.getOpenFileNames(self)
        self._files_dict = {}
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
        

        

if __name__=="__main__":
    app=QtWidgets.QApplication(sys.argv)
    main_widget = EC_MainWindow()
    main_widget.show()
    sys.exit(app.exec_())
