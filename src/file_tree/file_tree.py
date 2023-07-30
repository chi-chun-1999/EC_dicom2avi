from src.ec_ui.ec_ui_data import *
from src.exception.value_exception import FileTreeError

class Node:
    def __init__(self,data,name=None,parent=None):

        self.data = data
        self.children = []
        self.parent = parent
        self.name = name
        if parent!=None:
            self.parent.add_children([self])
        if name ==None:
            self.name = str(self.data)
    def add_children(self,children):
        obj = tuple(children)
        Node._check_children(obj)
        
        for child in obj:
            if child not in self.children:
                child.parent = self
                self.children.append(child)

    def show(self):
        for i in self.children:
            print(i)
            i.show()

    def getParentHierarchy(self):
        parent_hierarchy = ''
        
        tmp_node = self
        
        while tmp_node.parent!=None:
            parent_hierarchy =tmp_node.parent.name+'/'+parent_hierarchy
            tmp_node = tmp_node.parent
            
        
        parent_hierarchy = '/' +parent_hierarchy
        return parent_hierarchy
    
    @property
    def is_root(self):
        return self.parent is None

    @property
    def is_leaf(self):
        return len(self.children)==0
    
    @property
    def parent(self):
        if hasattr(self,"_Node__parent"):
            return self.__parent
        else:
            return None

    @parent.setter
    def parent(self,value):
        if value is not None and not isinstance(value,Node):
            msg = "Parent node %r is not of type 'NodeMixin'." % (value,)
            raise ValueError(msg)

        self.__parent = value

    @property
    def ancestors(self):
        if self.parent is None:
            return tuple()
        return self.parent.path

    @property
    def height(self):
        children = self.children
        if children:
            return max(child.height for child in self.children)+1
        else:
            return 0

    @property
    def depth(self):
        # count without storing the entire path
        # pylint: disable=W0631
        for depth, _ in enumerate(self.iter_path_reverse()):
            continue
        return depth
    @property
    def path(self):
        return self._path

    def _check_children(children):
        seen = set()
        for child in children:
            if not isinstance(child,Node):
                msg = "Cannot add non-node object %r. It is not a subclass of 'Node'." % (child,)
                raise ValueError(msg)
            childid = id(child)
            if child not in seen:
                seen.add(child)
            
            else:
                msg = "Cannot add node %r multiple times as child." % (child,)
                raise ValueError(msg)
    def iter_path_reverse(self):
        node = self
        while node is not None:
            yield node
            node = node.parent            

    @property
    def _path(self):
        return tuple(reversed(list(self.iter_path_reverse())))

    def __str__(self) -> str:
        name = 'Node('+self.getParentHierarchy()+self.name+')'
        return name
    def __repr__(self) -> str:
        name = 'Node('+self.getParentHierarchy()+self.name+')'
        return name
    
class AbstractIter():
    # pylint: disable=R0205

    def __init__(self, node, filter_=None, stop=None, maxlevel=None):
        """
        Iterate over tree starting at `node`.

        Base class for all iterators.

        Keyword Args:
            filter_: function called with every `node` as argument, `node` is returned if `True`.
            stop: stop iteration at `node` if `stop` function returns `True` for `node`.
            maxlevel (int): maximum descending in the node hierarchy.
        """
        self.node = node
        self.filter_ = filter_
        self.stop = stop
        self.maxlevel = maxlevel
        self.__iter = None

    def __init(self):
        node = self.node
        maxlevel = self.maxlevel
        filter_ = self.filter_ or AbstractIter.__default_filter
        stop = self.stop or AbstractIter.__default_stop
        children = [] if AbstractIter._abort_at_level(1, maxlevel) else AbstractIter._get_children([node], stop)
        return self._iter(children, filter_, stop, maxlevel)

    @staticmethod
    def __default_filter(node):
        # pylint: disable=W0613
        return True

    @staticmethod
    def __default_stop(node):
        # pylint: disable=W0613
        return False

    def __iter__(self):
        return self

    def __next__(self):
        if self.__iter is None:
            self.__iter = self.__init()
        return next(self.__iter)

    @staticmethod
    def _iter(children, filter_, stop, maxlevel):
        raise NotImplementedError()  # pragma: no cover

    @staticmethod
    def _abort_at_level(level, maxlevel):
        return maxlevel is not None and level > maxlevel

    @staticmethod
    def _get_children(children, stop):
        return [child for child in children if not stop(child)]
            
class PreOrderIter(AbstractIter):
    @staticmethod
    def _iter(children, filter_, stop, maxlevel):
        for child_ in children:
            if stop(child_):
                continue
            if filter_(child_):
                yield child_
            if not AbstractIter._abort_at_level(2, maxlevel):
                descendantmaxlevel = maxlevel - 1 if maxlevel else None
                for descendant_ in PreOrderIter._iter(child_.children, filter_, stop, descendantmaxlevel):
                    yield descendant_

class FileTree(object):
    def __init__(self,root=None):
        if root == None:
            self.root = Node('root')
        else:
            self.root = root
    
    def insertFile(self,file_path,show=False):
        # if not os.path.isfile(file_path):
        #     msg = 'Please inuput the file not dir.'
        #     raise ValueError(msg)
        path_list = file_path.split(os.sep)

        search_node = self.root
        
        current_path = ""
        
        for i in range(len(path_list)):
            search_name = path_list[i]
            search_child = self._searchChild(search_node,search_name)
            if search_child==None:
                
                if i ==len(path_list)-1:
                    current_path += path_list[i]
                    dcm = pydicom.dcmread(file_path)
                    node_data = ECData(file_path,path_list[i])
                    # node_data = ECData(file_path,path_list[i],'test')
                
                else:
                    current_path += path_list[i]+'/'
                    node_data = DirData(current_path,path_list[i])
                    
                tmp_node = Node(node_data,path_list[i],search_node)
                search_node = tmp_node
            
            else:
                current_path += path_list[i]+'/'
                search_node = search_child
            
        # if show:
        #     print(self.root.show())

        # test = [node.name for node in PreOrderIter(self.root,filter_=lambda n:n.is_leaf())]
        # print(test)
    @property
    def file_nodes(self):
        return tuple(PreOrderIter(self.root, filter_=lambda node: node.is_leaf and isinstance(node.data,ECData)))

    def _searchChild(self,search_node,search_name):
        search_node_children = search_node.children 
        for i in range(len(search_node_children)):
            if search_node_children[i].name == search_name:
                # print(search_name)
                return search_node_children[i]
        
        return None
    
    
    def delFile(self,file_node):
        if file_node.is_leaf:
            file_node_parent = file_node.parent
            parent_children = file_node_parent.children
            file_node_parent.children = [child for child in parent_children if child is not file_node]
            del file_node
            
            dir_parent = file_node_parent
            
            while dir_parent.children==[] and dir_parent!=self.root:
                parent = dir_parent.parent
                parent_children = parent.children
                parent.children = [child for child in parent_children if child is not dir_parent]

                del dir_parent
                dir_parent = parent
        
        else:
            msg = 'The input node is not file node.'
            raise FileTreeError(msg)

    def delDir(self,dir_node,del_dir_parent):

        if not dir_node.is_leaf:
            # current_children = dir_node.children
            # current_parent = dir_node
            k = 0
            for i in range(len(dir_node.children)):
                self.delDir(dir_node.children[i-k],del_dir_parent)
                # print('--->',dir_node.children[i-k])
                del dir_node.children[i-k] 
                k+=1
            
            # del dir_node
            if dir_node in del_dir_parent.children:
            
                del_dir_parent_children = del_dir_parent.children
                del_dir_parent.children = [child for child in del_dir_parent_children if child is not dir_node]
                
                del dir_node

                while del_dir_parent.children==[] and del_dir_parent!=self.root:
                    parent =del_dir_parent.parent
                    parent_children = parent.children
                    parent.children = [child for child in parent_children if child is not del_dir_parent]
                    del del_dir_parent
                    del_dir_parent = parent
        
        else:
            # print(dir_node)
            # del dir_node
            return
            


    def showRootNode(self):
        """
        當這個FileTree中由一個節點下的子節點有兩個以上，則使這個節點為現示的根節點(ShowRoot)
        
        """
        if len(self.root.children) == 0:
            return None

        else:
            show_root = self.root
            
            while len(show_root.children)==1:
                if show_root.children[0].is_leaf:
                    break
                show_root = show_root.children[0]
            
            return show_root
        
