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



#%%

class MyWidget(QtWidgets.QWidget):
    def __init__(self,file_tree:FileTree):
        super().__init__()
        self._file_tree = file_tree
        self.setup_ui()
        self.setup_model()
        pushbutton = QtWidgets.QPushButton(self)
        pushbutton.setText('Button')
        pushbutton.clicked.connect(self.press)
        
    def setup_ui(self):
        self.tree_view = QtWidgets.QTreeView()
        self.layout = QtWidgets.QVBoxLayout(self)
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

#%%
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    dir1_file_a = '/A/B/C/D/E/F/file_a'
    dir1_file_b = '/A/B/C/D/E/F/file_b'

    dir2_file_a = '/A/B/C/D/E/F1/file_a'
    dir2_file_b = '/A/B/C/D/E/F1/file_b'

    dir3_file_a = '/A/B/C/D/E1/F1/file_a'
    dir3_file_b = '/A/B/C/D/E1/F1/file_b'

    file_tree = FileTree()
    file_tree.insertFile(dir1_file_a)
    file_tree.insertFile(dir1_file_b)
    file_tree.insertFile(dir2_file_a)
    file_tree.insertFile(dir2_file_b)
    file_tree.insertFile(dir3_file_a)
    file_tree.insertFile(dir3_file_b)
    print(file_tree.showRootNode())

# print(file_tree.root.show())
            
# test = [node.name for node in PreOrderIter(file_tree.root,filter_=lambda n:n.is_leaf())]
# test = [node.data for node in PreOrderIter(file_tree.root)]
# print(test)
    # file_nodes = file_tree.file_nodes
    # print(file_nodes)

    widget = MyWidget(file_tree)
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())

