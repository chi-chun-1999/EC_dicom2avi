
#%%
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ec_ui.ec_ui_data import *
from src.exception.value_exception import FileTreeError

from src.file_tree.file_tree import Node,FileTree

#%%
root = Node('root')
a = Node(1,name='a',parent=root)
b = Node(2,name='b',parent=root)
c = Node(3,name='c',parent=a)
d = Node(4,name='d',parent=c)
a1 = Node(2,name='a1')
root.add_children([a1])
# for c in root.children:
#     print( c.data)
root.show()
print(a.is_root)
print(a.is_leaf)
print(d.is_leaf)
print(root.children)
print(d.depth)
print(d.path)
            
#%%
import os
dir1_file_a = '/A1/B/C/D/E/F/file_a'
dir1_file_b = '/A1/B/C/D/E/F/file_b'
dir1_dirb_file_b = '/A1/B1/C/D/E/F/file_b'

dir2_file_a = '/A/B/C/D/E/F1/file_a'
dir2_file_b = '/A/B/C/D/E/F1/file_b'

file_tree = FileTree()
file_tree.insertFile(dir1_file_a)
file_tree.insertFile(dir1_file_b)
file_tree.insertFile(dir1_dirb_file_b)
file_tree.insertFile(dir2_file_a)
file_tree.insertFile(dir2_file_b)

# print(file_tree.root.show())
        
# test = [node.name for node in PreOrderIter(file_tree.root,filter_=lambda n:n.is_leaf())]
# test = [node.data for node in PreOrderIter(file_tree.root)]
# print(test)
file_nodes = file_tree.file_nodes
print(file_nodes)



# %%
# file_tree.delFile(file_nodes[-1])
# file_tree.delFile(file_nodes[-2])
# file_tree.delFile(file_nodes[1])
# file_tree.delFile(file_nodes[0])
# print(file_tree.root.show())

a1 = file_tree.root.children[0].children[0]
file_tree.delDir(a1,a1.parent)

# space_node = file_tree.root.children[0]
# file_tree.delDir(space_node,space_node.parent)

print(file_tree.root.show())
print(file_tree.showRootNode())


# %%
