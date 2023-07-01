import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *



class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        treeV = QTreeView(self)
        treeV.resize(450, 250)
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["name", "value"])
        item0 = QStandardItem('item0')
        item1 = QStandardItem('item1')
        item2 = QStandardItem('item2')
        item1.setData('111')
        item2.setData('222')

        item1_value = QStandardItem('123')
        item2_value = QStandardItem('223')
        
        
        model.appendRow(item0)
        item0.appendRow([item1,item1_value])
        model.appendRow([item2,item2_value])
        treeV.setModel(model)
        print(item2.data())

if __name__ == "__main__":
    app = QApplication([])

    widget = MyWidget()
    widget.resize(500, 300)
    widget.show()

    sys.exit(app.exec())