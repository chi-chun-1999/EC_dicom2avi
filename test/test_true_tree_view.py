import re
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ec_ui.ec_ui_data import *
from src.exception.value_exception import FileTreeError

from src.file_tree.file_tree import Node,FileTree

search_path = re.compile('\w+\/GEMS_IMG\/\d{4}_\w+\/\d+\/[_\w]+')
search_file = re.compile('\.\w+')
dir_path = r'/Volumes/MY DISK/project/strain/dataset/test_2_Echo Strain/'

# res = []
file_tree = FileTree()

for (dir_path, dir_names, file_names) in os.walk(dir_path):
    # res.extend(file_names)
    search_dir = search_path.search(dir_path)
    if search_dir:
        print(search_dir)
        for i in file_names:
            dicom_file_name = search_file.search(i)
            if not dicom_file_name:
                dicom_file_path = dir_path+'/'+i
                file_tree.insertFile(dicom_file_path)
                # res.append(dir_path+"/"+i)

    #print(dir_path,dir_names,file_names)


# for i in res:
#     print(i)

# print(len(res))

file_nodes = file_tree.file_nodes
print(file_nodes)