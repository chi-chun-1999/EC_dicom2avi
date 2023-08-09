import os 
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from PyQt5 import QtWidgets
from EC_dicom2avi_ui import Ui_MainWindow

from PyQt5.QtCore import pyqtSlot,QThread, pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QErrorMessage, QButtonGroup, QMessageBox, QProgressDialog

from src.ec_ui.show_ui import MplCanvas



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

if __name__=="__main__":
    app=QtWidgets.QApplication(sys.argv)
    main_widget = TestECToolMatplot()
    main_widget.show()
    sys.exit(app.exec_())