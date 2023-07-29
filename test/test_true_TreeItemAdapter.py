from __future__ import annotations
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.ec_ui.show_ui import TreeItem
from src.file_tree.file_tree import Node
from src.ec_ui.show_ui import AbstractTreeModel,FileTreeModel
from src.file_tree.file_tree import FileTree
from PyQt5 import QtCore,QtWidgets
import contextlib
import gc
import re
from PyQt5.QtWidgets import QFileDialog, QErrorMessage, QButtonGroup, QMessageBox



#%%

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # self._file_tree = file_tree
        # self.setup_model()
        self._pushbutton = QtWidgets.QPushButton(self)
        self._pushbutton.setText('Button')
        self._pushbutton.clicked.connect(self.press)

        self._add_file_button = QtWidgets.QPushButton(self)
        self._add_file_button.setText('+')
        self._add_file_button.clicked.connect(self.addFile)
        self._add_file_button.move(150,0)
        self.setup_ui()
        
        
        
    def setup_ui(self):
        self.tree_view = QtWidgets.QTreeView()
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self._pushbutton)
        self.layout.addWidget(self._add_file_button)
        self.layout.addWidget(self.tree_view)

    def setup_model(self):
        tree_model = FileTreeModel(self._file_tree)
        self.tree_view.setModel(tree_model)
        self.tree_view.expandAll()
    
    def press(self):
        # print('hello')
        current_index = self.tree_view.currentIndex() 
        data = self.tree_view.model().getNodeFromIndex(current_index)
        # print(data.is_leaf)
        
        if data.is_leaf:
            self._file_tree.delFile(data)
            current_tree_view_model =self.tree_view.model() 
            del current_tree_view_model
            gc.collect()
            self.setup_model()
    
    def addFile(self):
        
        dir_path = QFileDialog.getExistingDirectory()
        search_path = re.compile('\w+\/GEMS_IMG\/\d{4}_\w+\/\d+\/[_\w]+')
        search_with_sub_file = re.compile('\.\w+')
        search_with_dcm_sub_file = re.compile('^\w*.dcm')

        self._file_tree = FileTree()
        for (dir_path, dir_names, file_names) in os.walk(dir_path):
            # res.extend(file_names)
            search_dir = search_path.search(dir_path)
            if search_dir:
                # print(search_dir)
                for i in file_names:
                    with_sub_file_name = search_with_sub_file.search(i)
                    if not with_sub_file_name:
                        dicom_file_path = dir_path+'/'+i
                        self._file_tree.insertFile(dicom_file_path)
                    
                    else:
                        with_dcm_sub_file = search_with_dcm_sub_file.search(i)
                        if with_dcm_sub_file:
                            dicom_file_path = dir_path+'/'+i
                            self._file_tree.insertFile(dicom_file_path)
                
        self.setup_model()
        print(len(self._file_tree.file_nodes))
        
        
        

#%%
if __name__ == "__main__":
    app = QtWidgets.QApplication([])

# print(file_tree.root.show())
            
# test = [node.name for node in PreOrderIter(file_tree.root,filter_=lambda n:n.is_leaf())]
# test = [node.data for node in PreOrderIter(file_tree.root)]
# print(test)
    # file_nodes = file_tree.file_nodes
    # print(file_nodes)

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())

