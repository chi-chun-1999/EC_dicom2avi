from __future__ import annotations
import sys
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import numpy as np
import contextlib

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
    
    def show_EC_roi(self,ecg_roi,current_frame):
        self.axes.cla()
        self.axes.imshow(ecg_roi[current_frame,:,:,:])
        self.draw()
    
    def show_whole_frame(self,whole_frame,current_frame):
        self.axes.cla()
        self.axes.imshow(whole_frame[current_frame,:,:,:])
        self.draw()

def ShowExtractOutcome(demc_info):
    a =1
    
    
from dataclasses import dataclass, field
from typing import List

@dataclass
class TreeItem:
    node: Any = None
    _parent: TreeItem = field(default=None, repr=False)
    _childs: List[TreeItem] = field(default_factory=list, repr=False)

    def child(self, row):
        return self._childs[row]

    def childCount(self):
        return len(self._childs)

    def parent(self):
        return self._parent

    def row(self):
        if self._parent:
            self_id = id(self)
            child_ids = [id(x) for x in self._parent._childs]
            if self_id in child_ids:
                return child_ids.index(self_id)
        return 0

    def addChild(self, node: Any):
        child = self.__class__(node, _parent=self)
        self._childs.append(child)
        return child  


class AbstractTreeModel(QtCore.QAbstractItemModel):
    def __init__(self, *args, parent=None, **kwargs):
        super().__init__(parent)
        self.rootItem = TreeItem()
        if post_init := getattr(self, "__post_init__", None):
            # pass all initialization arguments to __post_init__
            post_init(*args, **kwargs)

    def index(self, row, column, parent=QtCore.QModelIndex()) -> QtCore.QModelIndex:
        """為視圖中所有能歷遍到的項目，給定一個Unique Index"""
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex
        if not parent.isValid():
            parent_item = self.rootItem
        else:
            parent_item = self.itemFromIndex(parent)

        if row >= parent_item.childCount():
            return QtCore.QModelIndex()

        child_item = parent_item.child(row)
        assert type(child_item) == type(self.rootItem), "%r, %r" % (
            type(child_item),
            type(self.rootItem),
        )
        # 雖然這裡使用 createIndex，但 Qt 有一套機制，在可能的情況下將會返回快取值
        # 每當視圖結構有改變時，例如載入新節點或移除現有節點，才會重新產生一個新的 Index
        index = self.createIndex(row, column, child_item)
        return index

    def itemFromIndex(self, index) -> TreeItem:
        """從Index獲取原始項目"""
        return index.internalPointer()

    def indexFromItem(self, item, column=0):
        """從項目獲取其Index"""
        if item is None:
            return QtCore.QModelIndex()
        assert type(item) == type(self.rootItem), "%r, %r" % (
            type(item),
            type(self.rootItem),
        )
        return self.createIndex(item.row(), column, item)

    def columnCount(self, index) -> int:
        """總欄數 You can overwrite this method for multi-column data model"""
        return 1

    def parent(self, index) -> QtCore.QModelIndex:
        """從當前 Index 取得父層 Index"""
        if not index.isValid():
            return QtCore.QModelIndex()
        child_item = self.itemFromIndex(index)
        parent_item = child_item.parent()
        if parent_item == self.rootItem:
            return QtCore.QModelIndex()
        elif parent_item is None:
            return QtCore.QModelIndex()
        else:
            assert type(parent_item) == type(self.rootItem), "%r, %r" % (
                type(parent_item),
                type(self.rootItem),
            )
            # 無論Column為何，均返回 Column 為 0 的父項目
            # 這裡弄錯欄的話，子項目會顯示不出來
            return self.createIndex(parent_item.row(), 0, parent_item)

    def data(self, index, role=QtCore.Qt.ItemDataRole.DisplayRole) -> Any:
        """
        取得當前 Index 的 role 資料（文字顯示使用 DisplayRole，其他請參考 Document）
        you need to reimplement this method for correct data output
        """
        if not index.isValid():
            return None
        return None

    # You should implant/modify the following method for lazylod model

    def rowCount(self, index=QtCore.QModelIndex()) -> int:
        """
        取得當前 Index 的子項目數量
        LazyLoad 情況下也要計算出子項目數量，視圖中才會顯示展開圖示
        """
        if index.column() > 0:
            return 0
        if not index.isValid():
            item = self.rootItem
        else:
            item = self.itemFromIndex(index)
        return item.childCount()

    def canFetchMore(self, parent: QtCore.QModelIndex) -> bool:
        """視圖用來判斷當前 Index 是否可展開"""
        return False

    def fetchMore(self, parent: QtCore.QModelIndex) -> None:
        """展開節點時將會呼叫此 Method，請在此實作插入新資料/節點的程式碼"""
        ...


class SimpleDictModel(AbstractTreeModel):

    def __post_init__(self, data):
        self.rootItem = TreeItem(("", {}))  # key value pair

        self._insert_items(data)

    def _insert_items(self, data: dict, parent=None):
        """
        custom private method to insert all children item in dict
        """
        parent_item = parent or self.rootItem

        for key, value in iter_children(data):
            item = parent_item.addChild((key, value))
            if len(list(iter_children(value))):
                self._insert_items(value, item)

    def columnCount(self, index) -> int:
        return 2

    def rowCount(self, index=QtCore.QModelIndex()) -> int:
        if not index.isValid():
            return self.rootItem.childCount()

        item = self.itemFromIndex(index)
        return item.childCount()

    def data(self, index, role=QtCore.Qt.ItemDataRole.DisplayRole):
        item = self.itemFromIndex(index)
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            key, val = item.node
            if index.column() == 0:
                return key
            elif index.column() == 1:
                if len(list(iter_children(val))) == 0:
                    return val
                else:
                    return ""
            else:
                return str(type(val))

def iter_children(data: Any):
    """function to iterate data children"""
    if isinstance(data, list):
        iter_func = lambda x: enumerate(x)
    elif isinstance(data, dict):
        iter_func = lambda x: x.items()
    # elif isinstance(data,tuple):
    #     #data = [data]
    #     # print('data 0: ',data[0])
    #     # print('data 1: ',data[1])
    #     # data = {'x':data[0],'y':data[1]}
    #     iter_func = lambda x:enumerate(x)
    # # elif isinstance(data,np.ndarray):
    # #     data = {'x':data[0],'y':data[1]}
    # #     iter_func = lambda x:x.items()
    elif isinstance(data,np.int64):
        data = int(data)
        iter_func = lambda x: []
    else:
        iter_func = lambda x: [] 

    for x in iter_func(data):
        yield x


@contextlib.contextmanager
def layoutChange(model: AbstractTreeModel):
    try:
        model.layoutAboutToBeChanged.emit()
        yield
    finally:
        model.layoutChanged.emit() 

class FileTreeModel(AbstractTreeModel):
    def __post_init__(self,file_tree:FileTree):
        self.rootItem =TreeItem(file_tree.showRootNode())
        # print(self.rootItem.node.name)
        self.fetchMore(self.indexFromItem(self.rootItem))

    def data(self, index, role=QtCore.Qt.ItemDataRole.DisplayRole):
        item = self.itemFromIndex(index)
        # print(item.node)
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return item.node.name
    def getNodeFromIndex(self,index, role=QtCore.Qt.ItemDataRole.DisplayRole):
        item = self.itemFromIndex(index)
        if role ==QtCore.Qt.ItemDataRole.DisplayRole:
            if item!=None:
                return item.node
            else:
                return None

    def headerData(
        self,
        section: int,
        orientation: QtCore.Qt.Orientation,
        role=QtCore.Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        assert orientation == QtCore.Qt.Orientation.Horizontal
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            if section == 0:
                return "Name"
        return super().headerData(section, orientation, role)
    def rowCount(self, index=QtCore.QModelIndex()):
        if not self.canFetchMore(index):
            # print('***************')
            return super().rowCount(index)
        item = self.itemFromIndex(index)
        # print('-------------',item.node.children)
        if not(item.node.is_leaf):
            try:
                return len(item.node.children)
            except PermissionError:
                return 0
        else:
            return 0

    def canFetchMore(self, parent: QtCore.QModelIndex) -> bool:
        if not parent.isValid():
            return False
        item = self.itemFromIndex(parent)
        # print('-------------',item)
        if item is None:
            return False
        return item.childCount() == 0 and not(item.node.is_leaf)

    def fetchMore(self, parent: QtCore.QModelIndex) -> None:
        parent_item = self.itemFromIndex(parent)
        
        if parent_item.node!=None:
            children_node = parent_item.node.children
            with layoutChange(self):
                self.beginInsertRows(parent, 0, len(children_node))
                for c in children_node:
                    parent_item.addChild(c)
                self.endInsertRows()