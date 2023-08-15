import os 
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from PyQt5 import QtWidgets
from EC_dicom2avi_ui import Ui_MainWindow
from PyQt5.QtCore import pyqtSlot,QThread, pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QErrorMessage, QButtonGroup, QMessageBox, QProgressDialog
from PyQt5.QtGui import QFont
from src.ec_ui import ECData
from src.ec_ui.show_ui import MplCanvas, SimpleDictModel,FileTreeModel
from src.ec_ui.process_ui import StartExtractData, MultiThreadExtractData
from config_Window import ConfigWindow
from src.file_tree.file_tree import FileTree
from src.ec_ui.file_ui import *
import pydicom
import pandas as pd
import gc
import re
from src.ec_ui.export_ui import OutcomeTreeExportData,DoctorAndResearchOutcomeTreeExportData
import numpy as np



class EC_MainWindow(QtWidgets.QMainWindow):
    _extract_outcome_signal = pyqtSignal(dict,list)
    def __init__(self,parent=None):

        super().__init__(parent)
        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)
        self._process_data_dict = {}
        self._export_path = None

        self._thread_num = 3
        self._ocr_weight_path = './config/template_number.npy'
        self._config_window = ConfigWindow(self._thread_num,self._ocr_weight_path)
        self._config_window._config_signal.connect(self.do_getConfig)
        
        self._mpl_canvas = MplCanvas()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self._mpl_canvas)
        self.button_group = QButtonGroup(self)
        self.button_group.addButton(self.__ui.radioButton_all,1)
        self.button_group.addButton(self.__ui.radioButton_avi,2)
        self.button_group.addButton(self.__ui.radioButton_npy,3)

        self._extract_outcome_signal.connect(self.do_showExtractOutcome)
        
        self._file_tree = FileTree()
        
        self._import_file_thread = ImportFileThread()
        self._import_file_thread.import_file_finish.connect(self.do_showImportFile)


        # self.__ui.widget_picture.setLayout(layout)

        #self.__ui.pushButton_file..connect(self.ec_func)
        #self.do_show()
        self._config_dict = self._config_window.config_dict
        # print(self._config_dict)
        
        self.__ui.progressBar.setValue(0)
        self.__ui.label_progress.setText('0%')

        self._mpl_canvas = MplCanvas()
        [canvas_width,canvas_height] = self._mpl_canvas.get_width_height()
        # self._mpl_canvas.axes.text(canvas_width/2,canvas_height/2,'npy Viewer',fontsize=100)
        self._mpl_canvas.axes.text(0,0.5,'npy Viewer',fontsize=50)
        self._mpl_canvas.axes.axis('off')
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self._mpl_canvas)
        self.__ui.widget_npy.setLayout(layout)
        
        self._import_npy_file_thread = ImportNpyFileThread()
        self._import_npy_file_thread.import_file_finish.connect(self.do_showNpyImportFile)
        
        self._current_whole_frame = None
        self.__ui.lineEdit_current_npy.setEnabled(False)
        self._setFrameButtonEnable()

    
    @pyqtSlot(dict)
    def do_getConfig(self,config_dict):
        # print(config_dict)
        self._config_dict = config_dict
    
    @pyqtSlot(float)
    def do_getProgress(self,progress):
        # print('------------------>',progress,'%')
        progress_text = str(int(progress))+'%'
        self.__ui.progressBar.setValue(progress)
        self.__ui.label_progress.setText(progress_text)

    def addFile(self):
        self._error_file  = []

        dir_path = QFileDialog.getExistingDirectory()
        print(dir_path)
        search_path = re.compile('\w+\\GEMS_IMG\\\d{4}_\w+\\\d+\\[_\w]+')
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
        self._import_path = dir_path
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

        
        

    @pyqtSlot(bool)
    def on_action_config_triggered(self,checked):
        self._config_window.show()

    def on_pushButton_add_file_released(self):
        dir_path = QFileDialog.getExistingDirectory()
        self._import_path = dir_path
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
        
        if self._export_path=="":
            self._export_path=None
        
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
        
        process_data_extractor = FileTreeProcessData(self._file_tree)

        
        self._process_data_dict = process_data_extractor.getProcessData()
        # print(self._process_data_dict)
        
        

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
        
        
        # self._export_data_method = OutcomeTreeExportData(self._export_path) 
        self._export_data_method = DoctorAndResearchOutcomeTreeExportData(self._export_path,self._import_path) 
        self._data_extractor = MultiThreadExtractData(self._process_data_dict,self._export_data_method,export_data_dict[self.button_group.checkedId()],thread_num=self._config_dict['thread_num'],ocr_weight_path=self._config_dict['ocr_weight_path'])
        
        # for test below funciton will not export extract data
        # self._epxort_data_method = OutcomeTreeExportData(self._export_path) 
        # self._data_extractor = MultiThreadExtractData(self._process_data_dict,self._epxort_data_method,export_data_dict[4],thread_num=3)
        self._data_extractor.signal_progress.connect(self.do_getProgress)

        self._data_extractor.startExtractData()
        
        self._outcome_thread = QThread()
        self._outcome_thread.run = self.getExtractOutcome
        self._outcome_thread.start()
        self.__ui.pushButton_start.setEnabled(False)
        
    
    def getExtractOutcome(self):
        """
        """
        self._data_extractor.threadWait()
        demc_info_dict,three_dim_dicom_file = self._data_extractor.getOutcome()
        # self._data_extractor.exportDecmInfo()
        self._export_data_method.exportDecmInfo()
        
        self._extract_outcome_signal.emit(demc_info_dict,three_dim_dicom_file)

        # print('-----print outcome thread----')
        
        #ShowExtractOutcome(demc_info)
    
    @pyqtSlot(dict,list)
    def do_showExtractOutcome(self,demc_info,three_dim_dicom_file):
        if len(three_dim_dicom_file)!=0:
            warning_str = str(three_dim_dicom_file)+' is(are) not 4 dimesion file(s), so it(they) will not be processed.'
            # message = QMessageBox.warning(self,"Wanrning",warning_str,buttons=QMessageBox.StandardButton.Ok)
            message = QErrorMessage(self)
            message.showMessage(warning_str)
        # demc_info = {'process_time': 'Fri Jun 30 17:56:41 2023', 'process_file_num': 2, 'process_file_info': [{'Name': 'KBIHSQ00', 'R_wave_location': [(98, 52), (175, 52), (259, 52)], 'extract_frame': [22, 47, 75], 'unregular_rr_interval': False}, {'Name': 'KBIHSQO2', 'R_wave_location': [(32, 52), (109, 52), (186, 52), (263, 52)], 'extract_frame': [0, 25, 51, 76], 'unregular_rr_interval': False}]}
        # print(demc_info)
        self.__ui.lineEdit_process_time.setText( demc_info['process_time'])
        self.__ui.lineEdit_process_file_num.setText(str(demc_info['process_file_num']))
        
        # data = pd.DataFrame(demc_info['process_patient_info'])
        
        # tmp = data.copy().set_index('Name')
        # data_dict = tmp.to_dict()
        
        data_dict = demc_info['process_patient_info']
        # self._model = TableModel(data)
        self._model = SimpleDictModel(data_dict)
        
        # Set Progress to zero
        self.__ui.progressBar.setValue(0)
        self.__ui.label_progress.setText('0%')


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
            
    
# npy viewer code
    def add_npy_file(self):
        
        dir_path = QFileDialog.getExistingDirectory()
    
    def on_pushButton_add_file_npy_released(self):
        dir_path = QFileDialog.getExistingDirectory()
        self._import_npy_file_thread.getDirPath(dir_path)
        
        self._import_npy_file_thread.start()

        # Show the waiting Dialog
        self._progress_dialog = QProgressDialog(self)
        self._progress_dialog.setLabelText('Please Wait. Loading files... ')
        self._progress_dialog.setMinimumDuration(0)
        self._progress_dialog.setRange(0,0)
        self._progress_dialog.setCancelButton(None)
        self._progress_dialog.show()
        self.__ui.lineEdit_current_npy.setEnabled(False)

    def on_pushButton_delete_file_npy_released(self):
        #print(self.__ui.listWidget_file.currentItem())
        

        if self.__ui.treeView_file_npy.model() !=None:
            current_index = self.__ui.treeView_file_npy.currentIndex()
            current_node = self.__ui.treeView_file_npy.model().getNodeFromIndex(current_index)
            
            if current_node:
            
                if current_node.is_leaf:
                    self._file_npy_tree.delFile(current_node)
                    current_tree_view_model = self.__ui.treeView_file_npy.model()
                    del current_tree_view_model
                    gc.collect()
                    file_tree_model = FileTreeModel(self._file_npy_tree)
                    self.__ui.treeView_file_npy.setModel(file_tree_model)
                    self.__ui.treeView_file_npy.expandAll()
                    return
                else:
                    self._file_npy_tree.delDir(current_node,current_node.parent)
                    current_tree_view_model = self.__ui.treeView_file_npy.model()
                    del current_tree_view_model
                    gc.collect()
                    file_tree_model = FileTreeModel(self._file_npy_tree)
                    self.__ui.treeView_file_npy.setModel(file_tree_model)
                    self.__ui.treeView_file_npy.expandAll()
                    return

        warning_str = 'Please select the file or directory that will be deleted.'
        
        message = QMessageBox.warning(self,"Error",warning_str,buttons=QMessageBox.StandardButton.Ok)
            # message.showMessage(error_file)
    
    def on_treeView_file_npy_doubleClicked(self):
        
        current_index = self.__ui.treeView_file_npy.currentIndex()
        current_node = self.__ui.treeView_file_npy.model().getNodeFromIndex(current_index)
        self.__ui.lineEdit_current_npy.setEnabled(True)

        
        if current_node:
            if current_node.is_leaf:
                # print(current_node.data)
                self.__ui.lineEdit_npy_file_path_npy.setText(current_node.data)
                
                self._current_whole_frame = np.load(current_node.data)
                self._current_frame = 0
                self._mpl_canvas.show_whole_frame(self._current_whole_frame,self._current_frame)
                self.__ui.lineEdit_current_npy.setText(str(self._current_frame+1))
                self._setFrameButtonEnable()
                all_frame_size_str = '/ '+str(self._current_whole_frame.shape[0])
                
                self.__ui.label_all_npy.setText(all_frame_size_str)

    
    def on_lineEdit_current_npy_returnPressed(self):
        # print('------------>',self.__ui.lineEdit_current_npy.text())
        flag = True
        
        try:
            tmp_current_frame = int(self.__ui.lineEdit_current_npy.text())
        
        except ValueError:
            flag =  False
        
        if flag:
            self._current_frame = tmp_current_frame-1
            if type(self._current_whole_frame) == np.ndarray:
                if tmp_current_frame<=0:
                    self._current_frame = 0
                
                elif tmp_current_frame>self._current_whole_frame.shape[0]:
                    self._current_frame =self._current_whole_frame.shape[0]-1 
                
                self.__ui.lineEdit_current_npy.setText(str(self._current_frame+1))
                self._mpl_canvas.show_whole_frame(self._current_whole_frame,self._current_frame)

                self._setFrameButtonEnable()
        
        else:
            warning_str = 'Please Input Integer!'
            # print(warning_str)
            message = QMessageBox.warning(self,"Wanrning",warning_str,buttons=QMessageBox.StandardButton.Ok)
            


    
        # self.__ui.lineEdit_current_npy
                
            
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
        
        if type(self._current_whole_frame) == np.ndarray:
            if self._current_frame == 0:
                self.__ui.pushButton_previous_npy.setEnabled(False)
            
            else:
                self.__ui.pushButton_previous_npy.setEnabled(True)
                

            if self._current_frame == self._current_whole_frame.shape[0]-1:
                self.__ui.pushButton_next_npy.setEnabled(False)

            else:
                self.__ui.pushButton_next_npy.setEnabled(True)
        
        else:
            self.__ui.pushButton_previous_npy.setEnabled(False)
            self.__ui.pushButton_next_npy.setEnabled(False)
            
                
                
        

    @pyqtSlot(FileTree)
    def do_showNpyImportFile(self,file_tree):
        self._file_npy_tree = file_tree
        # print(self._file_tree.root.height)
        file_tree_model = FileTreeModel(self._file_npy_tree)
        self.__ui.treeView_file_npy.setModel(file_tree_model)
        self.__ui.treeView_file_npy.expandAll()
        self._progress_dialog.close()
        if self._file_npy_tree.root.height==0:
            warning_str = 'Please select the directory with the file structure similar to <font style="color: red;">\'ExportData\'</font> below.\
<pre>\
ExportData/<br>\
└── ac7b1825f4/<br>\
    └── 20220203/<br>\
        ├── npy/<br>\
        │   ├── KBIHSR0C_0.npy<br>\
        │   ├── KBIHSR0C_1.npy<br>\
        │   ├── KBIHSR0C_2.npy<br>\
        │   ├── KBIHSQ00_0.npy<br>\
        │   ├── KBIHSQ00_1.npy<br>\
        │   └── KBIHSQ00_2.npy<br>\
        └── whole_npy/<br>\
            ├── KBIHSR0C_whole.npy<br>\
            └── KBIHSQ00_whole.npy<br>\
</pre><br>\
'
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
        if sys.platform == 'win32':
            search_path = re.compile(r'\w+\\GEMS_IMG\\\d{4}_\w+\\\d+\\[_\w]+')
        else:
            search_path = re.compile(r'\w+\/GEMS_IMG\/\d{4}_\w+\/\d+\/[_\w]+')
            
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
                            if sys.platform == 'win32':
                                dicom_file_path = dir_path+'\\'+i
                            else:
                                dicom_file_path = dir_path+'/'+i
                                
                            file_tree.insertFile(dicom_file_path)
                        
                        else:
                            with_dcm_sub_file = search_with_dcm_sub_file.search(i)
                            if with_dcm_sub_file:
                                
                                if sys.platform == 'win32':
                                    dicom_file_path = dir_path+'\\'+i
                                
                                else:
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
        
class ImportNpyFileThread(QThread):
    import_file_finish = pyqtSignal(FileTree)
    def __init__(self,parent=None):
        QThread.__init__(self,parent)
    def getDirPath(self,dir_path):
        self._dir_path = dir_path

    def run(self):
        self._error_file  = []
        file_tree = FileTree(file_type='npy')

        # dir_path = QFileDialog.getExistingDirectory()
        if sys.platform == 'win32':
            search_path = re.compile(r'\w{10}\\\d+\\\w*npy')
        else:
            search_path = re.compile(r'\w{10}\/\d+\/\w*npy')
            
        search_with_sub_file = re.compile('\.\w+')
        search_with_dcm_sub_file = re.compile('^\w*.npy')

        for (dir_path, dir_names, file_names) in os.walk(self._dir_path):
            # res.extend(file_names)
            search_dir = search_path.search(dir_path)
            if search_dir:
                # print(search_dir)
                for i in file_names:
                    try:
                        with_sub_file_name = search_with_sub_file.search(i)
                        if not with_sub_file_name:
                            if sys.platform == 'win32':
                                dicom_file_path = dir_path+'\\'+i
                            else:
                                dicom_file_path = dir_path+'/'+i
                                
                            file_tree.insertFile(dicom_file_path)
                        
                        else:
                            with_dcm_sub_file = search_with_dcm_sub_file.search(i)
                            if with_dcm_sub_file:
                                
                                if sys.platform == 'win32':
                                    dicom_file_path = dir_path+'\\'+i
                                
                                else:
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
