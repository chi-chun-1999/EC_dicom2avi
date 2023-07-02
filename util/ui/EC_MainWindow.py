import os 
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from PyQt5 import QtWidgets
from EC_dicom2avi_ui import Ui_MainWindow
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QErrorMessage, QButtonGroup, QMessageBox
from src.ec_ui import ECData
from src.ec_ui.show_ui import MplCanvas,ShowExtractOutcome,TableModel, SimpleDictModel
from src.ec_ui.process_ui import StartExtractData
import pydicom
import pandas as pd



class EC_MainWindow(QtWidgets.QMainWindow):
    def __init__(self,parent=None):

        super().__init__(parent)
        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)
        self._files_dict = {}

        self._mpl_canvas = MplCanvas()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self._mpl_canvas)
        self.button_group = QButtonGroup(self)
        self.button_group.addButton(self.__ui.radioButton_all,1)
        self.button_group.addButton(self.__ui.radioButton_avi,2)
        self.button_group.addButton(self.__ui.radioButton_npy,3)
        self.button_group.buttonClicked.connect(self.do_show)

        # self.__ui.widget_picture.setLayout(layout)

        #self.__ui.pushButton_file..connect(self.ec_func)
        #self.do_show()

    def do_show(self):
        print(self.button_group.checkedId())

    def addFile(self):
        self._error_file  = []
        files_path = QFileDialog.getOpenFileNames(self)
        for f in files_path[0]:
            file_head, file_tail = os.path.split(f)

            try:
                if not(file_tail in self._files_dict):
                    dcm = pydicom.dcmread(f)
                    tmp_ec_data = ECData(f,file_tail,dcm)
            except pydicom.errors.InvalidDicomError as e:
                print(e)
                self._error_file.append(file_tail)
                if len(self._error_file)>=1:
                    print(self._error_file)
                    error_file=str(self._error_file)+' is(are) NOT the DICOM file(s). Please select DICOM file.'
                    
                    message = QMessageBox.critical(self,"Error",error_file,buttons=QMessageBox.StandardButton.Ok)
                    # message.showMessage(error_file)
            
            else:
                if not(file_tail in self._files_dict):
                    self._files_dict[file_tail] = tmp_ec_data
                    self.__ui.listWidget_file.addItem(file_tail)
        # for idx, j in self._files_dict.items():
        #     print(idx,j.getPath())

    @pyqtSlot(bool)
    def on_actionOpen_file_open_triggered(self,checked):
        self.addFile()

    def on_pushButton_add_file_released(self):
        self.addFile()
    
    def on_pushButton_delete_file_released(self):
        #print(self.__ui.listWidget_file.currentItem())
        
        if self.__ui.listWidget_file.currentItem()!=None:
            del self._files_dict[self.__ui.listWidget_file.currentItem().text()]
            delete_item = self.__ui.listWidget_file.takeItem(self.__ui.listWidget_file.currentRow())
            del delete_item

    def on_pushButton_export_released(self):
        
        self._export_path = QFileDialog.getExistingDirectory(self)
        self.__ui.lineEdit_export_path.setText(self._export_path)
        
    # def on_listWidget_file_itemDoubleClicked(self):
    #     select_file = self.__ui.listWidget_file.currentItem().text()
    #     select_num = self.__ui.listWidget_file.currentIndex().row()
    #     print(select_num,select_file)
    #     print(self._files_dict[select_file]._file_path)
    #     self._current_show_file = self._files_dict[select_file]
    #     self._current_show_file.loadData()
    #     rgb_array_data = self._current_show_file.getRgbArray()
    #     print(rgb_array_data.shape)
    #     self._current_frame_num = 0
    #     self.__ui.lineEdit_current_pic.setText(str(self._current_frame_num))
    #     self.__ui.lineEdit_all_pic.setText(str(rgb_array_data.shape[0]))
        
    #     self._mpl_canvas.show_whole_frame(rgb_array_data,self._current_frame_num)

    def on_pushButton_start_released(self):
        export_data_dict = {1:'all',2:'avi',3:'npy'}
        demc_info = StartExtractData(self._files_dict,self._export_path,export_data_dict[self.button_group.checkedId()])
        
        # demc_info = {'process_time': 'Fri Jun 30 17:56:41 2023', 'process_file_num': 2, 'process_file_info': [{'Name': 'KBIHSQ00', 'R_wave_location': [(98, 52), (175, 52), (259, 52)], 'extract_frame': [22, 47, 75], 'unregular_rr_interval': False}, {'Name': 'KBIHSQO2', 'R_wave_location': [(32, 52), (109, 52), (186, 52), (263, 52)], 'extract_frame': [0, 25, 51, 76], 'unregular_rr_interval': False}]}
        # print(demc_info)
        self.__ui.lineEdit_process_time.setText( demc_info['process_time'])
        self.__ui.lineEdit_process_file_num.setText(str(demc_info['process_file_num']))
        
        data = pd.DataFrame(demc_info['process_file_info'])
        
        tmp = data.copy().set_index('Name')
        data_dict = tmp.to_dict()
        
        # self._model = TableModel(data)
        self._model = SimpleDictModel(data_dict)


        self.__ui.treeView_outcome.setModel(self._model)
        
        #ShowExtractOutcome(demc_info)
        
        

if __name__=="__main__":
    app=QtWidgets.QApplication(sys.argv)
    main_widget = EC_MainWindow()
    main_widget.show()
    sys.exit(app.exec_())
