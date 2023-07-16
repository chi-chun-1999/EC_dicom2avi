import sys
import matplotlib
from src.file_tree.file_tree import FileTree
import abc

class FileProcessDataAbs(abc.ABC):
    def __init__(self) -> None:
        super().__init__()
        self._process_data = {}
    
    @abc.abstractmethod
    def getProcessData(self):
        pass 
        

class FileTreeProcessData(FileProcessDataAbs):
    def __init__(self,file_tree:FileTree):
        super().__init__()
        self._file_tree = file_tree

    def getProcessData(self):
        file_nodes = self._file_tree.file_nodes
        print(self._file_tree.showRootNode())
        
        for i in file_nodes:
            # print(i.data)
            self._process_data[i.data.file_path] = i.data

        return self._process_data

