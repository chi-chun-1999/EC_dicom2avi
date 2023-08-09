import os 
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from PyQt5 import QtWidgets
from EC_dicom2avi_ui import Ui_MainWindow

from PyQt5.QtCore import pyqtSlot,QThread, pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QErrorMessage, QButtonGroup, QMessageBox, QProgressDialog

from src.ec_ui.show_ui import MplCanvas, FileTreeModel
from src.file_tree.file_tree import FileTree
import re
import pydicom



class TestECToolMatplot(QtWidgets.QMainWindow):
    def __init__(self,parent=None):

        super().__init__(parent)
        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)
        self._mpl_canvas = MplCanvas()
        self._mpl_canvas.axes.plot([0,1,2,3,4], [10,1,20,3,40])
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self._mpl_canvas)
        self.__ui.widget_npy.setLayout(layout)
        
        self._import_npy_file_thread = ImportNpyFileThread()
        self._import_npy_file_thread.import_file_finish.connect(self.do_showNpyImportFile)
    
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
    
    def on_treeView_file_npy_doubleClicked(self):
        
        current_index = self.__ui.treeView_file_npy.currentIndex()
        current_node = self.__ui.treeView_file_npy.model().getNodeFromIndex(current_index)
        
        if current_node:
            if current_node.is_leaf:
                # print(current_node.data)
                self.__ui.lineEdit_npy_file_path_npy.setText(current_node.data)
                
                
        

    @pyqtSlot(FileTree)
    def do_showNpyImportFile(self,file_tree):
        self._file_tree = file_tree
        # print(self._file_tree.root.height)
        file_tree_model = FileTreeModel(self._file_tree)
        self.__ui.treeView_file_npy.setModel(file_tree_model)
        self.__ui.treeView_file_npy.expandAll()
        self._progress_dialog.close()
        if self._file_tree.root.height==0:
            warning_str = 'Please select the directory with the file structure similar to <font style="color: red;">\'Echo Strain\'</font> below.\
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
    main_widget = TestECToolMatplot()
    main_widget.show()
    sys.exit(app.exec_())
