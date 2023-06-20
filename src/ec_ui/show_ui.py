import sys
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


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
