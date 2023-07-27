import os 
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from PyQt5 import QtWidgets
from EC_dicom2avi_ui import Ui_MainWindow
from PyQt5.QtCore import pyqtSlot,QThread, pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QErrorMessage, QButtonGroup, QMessageBox, QProgressDialog
from PyQt5.QtGui import QFont
from src.ec_ui import ECData
from src.ec_ui.show_ui import MplCanvas,ShowExtractOutcome, SimpleDictModel,FileTreeModel
from src.ec_ui.process_ui import StartExtractData, MultiThreadExtractData
from src.file_tree.file_tree import FileTree
from src.ec_ui.file_ui import *
import pydicom
import pandas as pd
import gc
import re



class EC_MainWindow(QtWidgets.QMainWindow):
    _extract_outcome_signal = pyqtSignal(dict,list)
    def __init__(self,parent=None):

        super().__init__(parent)
        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)
        self._process_data_dict = {}
        self._export_path = None

        self._mpl_canvas = MplCanvas()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self._mpl_canvas)
        self.button_group = QButtonGroup(self)
        self.button_group.addButton(self.__ui.radioButton_all,1)
        self.button_group.addButton(self.__ui.radioButton_avi,2)
        self.button_group.addButton(self.__ui.radioButton_npy,3)
        self.button_group.buttonClicked.connect(self.do_show)

        self._extract_outcome_signal.connect(self.do_showExtractOutcome)
        
        self._file_tree = FileTree()
        
        self._import_file_thread = ImportFileThread()
        self._import_file_thread.import_file_finish.connect(self.do_showImportFile)

        # self.__ui.widget_picture.setLayout(layout)

        #self.__ui.pushButton_file..connect(self.ec_func)
        #self.do_show()

    def do_show(self):
        print(self.button_group.checkedId())

    def addFile(self):
        self._error_file  = []

        dir_path = QFileDialog.getExistingDirectory()
        search_path = re.compile('\w+\/GEMS_IMG\/\d{4}_\w+\/\d+\/[_\w]+')
        search_with_sub_file = re.compile('\.\w+')
        search_with_dcm_sub_file = re.compile('^\w*.dcm')

        for (dir_path, dir_names, file_names) in os.walk(dir_path):
            # res.extend(file_names)
            search_dir = search_path.search(dir_path)
            if search_dir:
                # print(search_dir)
                for i in file_names:
                    try:
                        with_sub_file_name = search_with_sub_file.search(i)
                        if not with_sub_file_name:
                            dicom_file_path = dir_path+'/'+i
                            self._file_tree.insertFile(dicom_file_path)
                        
                        else:
                            with_dcm_sub_file = search_with_dcm_sub_file.search(i)
                            if with_dcm_sub_file:
                                dicom_file_path = dir_path+'/'+i
                                self._file_tree.insertFile(dicom_file_path)
                    except pydicom.errors.InvalidDicomError as e:
                        print(e)
                        file_head, file_tail = os.path.split(i)
                        self._error_file.append(file_tail)


        if len(self._error_file)>=1:
            print(self._error_file)
            error_file=str(self._error_file)+' is(are) NOT the DICOM file(s). Please select DICOM file.'
            message = QMessageBox.critical(self,"Error",error_file,buttons=QMessageBox.StandardButton.Ok)
        
        # FileTreeModel is used to show the Import Data on the UI
        file_tree_model = FileTreeModel(self._file_tree)
        self.__ui.treeView_file.setModel(file_tree_model)
        self.__ui.treeView_file.expandAll()

        # print(self._file_tree.file_nodes)

    @pyqtSlot(bool)
    def on_actionOpen_file_open_triggered(self,checked):
        dir_path = QFileDialog.getExistingDirectory()
        self._import_file_thread.getDirPath(dir_path)
        # Using multi-thread to import file
        self._import_file_thread.start()
        
        # Show the waiting Dialog
        self._progress_dialog = QProgressDialog(self)
        self._progress_dialog.setLabelText('Please Wait. Loading files... ')
        self._progress_dialog.setMinimumDuration(0)
        self._progress_dialog.setRange(0,0)
        self._progress_dialog.setCancelButton(None)
        self._progress_dialog.show()

        
        

    def on_pushButton_add_file_released(self):
        dir_path = QFileDialog.getExistingDirectory()
        self._import_file_thread.getDirPath(dir_path)
        # Using multi-thread to import file
        self._import_file_thread.start() 

        # Show the waiting Dialog
        self._progress_dialog = QProgressDialog(self)
        self._progress_dialog.setLabelText('Please Wait. Loading files... ')
        self._progress_dialog.setMinimumDuration(0)
        self._progress_dialog.setRange(0,0)
        self._progress_dialog.setCancelButton(None)
        self._progress_dialog.show()

    def on_pushButton_delete_file_released(self):
        #print(self.__ui.listWidget_file.currentItem())
        

        if self.__ui.treeView_file.model() !=None:
            current_index = self.__ui.treeView_file.currentIndex()
            current_node = self.__ui.treeView_file.model().getNodeFromIndex(current_index)
            
            if current_node:
            
                if current_node.is_leaf:
                    self._file_tree.delFile(current_node)
                    current_tree_view_model = self.__ui.treeView_file.model()
                    del current_tree_view_model
                    gc.collect()
                    file_tree_model = FileTreeModel(self._file_tree)
                    self.__ui.treeView_file.setModel(file_tree_model)
                    self.__ui.treeView_file.expandAll()
                    return
                else:
                    self._file_tree.delDir(current_node,current_node.parent)
                    current_tree_view_model = self.__ui.treeView_file.model()
                    del current_tree_view_model
                    gc.collect()
                    file_tree_model = FileTreeModel(self._file_tree)
                    self.__ui.treeView_file.setModel(file_tree_model)
                    self.__ui.treeView_file.expandAll()
                    return

        warning_str = 'Please select the file or directory that will be deleted.'
        
        message = QMessageBox.warning(self,"Error",warning_str,buttons=QMessageBox.StandardButton.Ok)
            # message.showMessage(error_file)

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
        """
        Using the MultiThreadExtractData to extract data. And the relative varaiable is self._data_extractor. Due to using multi thread, the function of showing TreeView must also be thread.
        
        """
        """
        TODO:  我這裡不是使用 self._files_dict 來儲存資料，而是使用 self._file_tree，所以需要進行修改
        我多了一個 FileProcessData 來取得 self._files_dict 這樣一來可以避免重新更改ExtractDataThread 的介面
        

        
        """
        
        process_data_extractor = FileTreeProcessData(self._file_tree)

        
        self._process_data_dict = process_data_extractor.getProcessData()
        print(self._process_data_dict)
        
        

        if len(self._process_data_dict)==0 and self._export_path==None:
            warning_str = 'Please open the file(s) that will be processed and select the path to store the exported file(s). '
            message = QMessageBox.warning(self,"Wanrning",warning_str,buttons=QMessageBox.StandardButton.Ok)
            return

        elif len(self._process_data_dict)==0:
            warning_str = 'Please open the file(s) that will be processed.'
            message = QMessageBox.warning(self,"Warning",warning_str,buttons=QMessageBox.StandardButton.Ok)
            return

        elif self._export_path == None:
            warning_str = 'Please select the path to store the exported file(s).'
            message = QMessageBox.warning(self,"Wanrning",warning_str,buttons=QMessageBox.StandardButton.Ok)
            return

        export_data_dict = {1:'all',2:'avi',3:'npy',4:'None'}
        # demc_info,three_dim_dicom_file = StartExtractData(self._files_dict,self._export_path,export_data_dict[self.button_group.checkedId()])
        
        self._data_extractor = MultiThreadExtractData(self._process_data_dict,self._export_path,export_data_dict[self.button_group.checkedId()],thread_num=3)
        
        # for test below funciton will not export extract data
        # self._data_extractor = MultiThreadExtractData(self._files_dict,self._export_path,export_data_dict[4],thread_num=3)

        self._data_extractor.startExtractData()
        
        self._outcome_thread = QThread()
        self._outcome_thread.run = self.getExtractOutcome
        self._outcome_thread.start()
        self.__ui.pushButton_start.setEnabled(False)
        
    
    def getExtractOutcome(self):
        """
        """
        self._data_extractor.threadWait()
        demc_info,three_dim_dicom_file = self._data_extractor.getOutcome()
        
        self._extract_outcome_signal.emit(demc_info,three_dim_dicom_file)

        # print('-----print outcome thread----')
        
        #ShowExtractOutcome(demc_info)
    
    @pyqtSlot(dict,list)
    def do_showExtractOutcome(self,demc_info,three_dim_dicom_file):
        if len(three_dim_dicom_file)!=0:
            warning_str = str(three_dim_dicom_file)+' is(are) not 3 dimesion file(s), so it(they) will not be processed.'
            message = QMessageBox.warning(self,"Wanrning",warning_str,buttons=QMessageBox.StandardButton.Ok)
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
        self.__ui.pushButton_start.setEnabled(True)
    
    @pyqtSlot(FileTree)
    def do_showImportFile(self,file_tree):
        self._file_tree = file_tree
        # print(self._file_tree.root.height)
        file_tree_model = FileTreeModel(self._file_tree)
        self.__ui.treeView_file.setModel(file_tree_model)
        self.__ui.treeView_file.expandAll()
        self._progress_dialog.close()
        if self._file_tree.root.height==0:
            warning_str = 'Please select the directory with the file structure similar to <font style="color: red;">\'Echo Strain\'</font> below.\
            <pre>\
Echo Strain/<br>\
├─ Strain 1/ <br>\
│  ├─ GEMS_IMG/<br>\
│  │  ├─ 2009_SEP/<br>\
│  │  │  ├─ 23/<br>\
│  │  │  │  ├─ 152534/<br>\
│  │  │  │  │  ├─ 99NFGTPC<br>\
├─ Strain 2/<br>\
│  ├─ GEMS_IMG/<br>\
│  │  ├─ 2019_DEC/<br>\
│  │  │  ├─ 19/<br>\
│  │  │  │  ├─ 162664/<br>\
│  │  │  │  │  ├─ 90ADGDV3<br>\
</pre>'
            message = QMessageBox.warning(self,"Wanrning",warning_str,buttons=QMessageBox.StandardButton.Ok)


class ImportFileThread(QThread):
    import_file_finish = pyqtSignal(FileTree)
    def __init__(self,parent=None):
        QThread.__init__(self,parent)
    def getDirPath(self,dir_path):
        self._dir_path = dir_path

    def run(self):
        self._error_file  = []
        file_tree = FileTree()

        # dir_path = QFileDialog.getExistingDirectory()
        search_path = re.compile('\w+\/GEMS_IMG\/\d{4}_\w+\/\d+\/[_\w]+')
        search_with_sub_file = re.compile('\.\w+')
        search_with_dcm_sub_file = re.compile('^\w*.dcm')

        for (dir_path, dir_names, file_names) in os.walk(self._dir_path):
            # res.extend(file_names)
            search_dir = search_path.search(dir_path)
            if search_dir:
                # print(search_dir)
                for i in file_names:
                    try:
                        with_sub_file_name = search_with_sub_file.search(i)
                        if not with_sub_file_name:
                            dicom_file_path = dir_path+'/'+i
                            file_tree.insertFile(dicom_file_path)
                        
                        else:
                            with_dcm_sub_file = search_with_dcm_sub_file.search(i)
                            if with_dcm_sub_file:
                                dicom_file_path = dir_path+'/'+i
                                file_tree.insertFile(dicom_file_path)
                    except pydicom.errors.InvalidDicomError as e:
                        print(e)
                        file_head, file_tail = os.path.split(i)
                        self._error_file.append(file_tail)

        if len(self._error_file)>=1:
            print(self._error_file)
            error_file=str(self._error_file)+' is(are) NOT the DICOM file(s). Please select DICOM file.'
            message = QMessageBox.critical(self,"Error",error_file,buttons=QMessageBox.StandardButton.Ok)
        
        
        self.import_file_finish.emit(file_tree)
        
        

if __name__=="__main__":
    app=QtWidgets.QApplication(sys.argv)
    main_widget = EC_MainWindow()
    main_widget.show()
    sys.exit(app.exec_())
