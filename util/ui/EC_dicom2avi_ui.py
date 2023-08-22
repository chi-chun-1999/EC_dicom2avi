# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/chi-chun/institute/project/strain/EC_dicom2avi/util/ui/EC_dicom2avi.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(838, 850)
        MainWindow.setStyleSheet("QLineEdit\n"
"{\n"
"    color: black;\n"
"    background-color: white;\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.treeView_file = QtWidgets.QTreeView(self.tab)
        self.treeView_file.setObjectName("treeView_file")
        self.verticalLayout.addWidget(self.treeView_file)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.pushButton_add_file = QtWidgets.QPushButton(self.tab)
        self.pushButton_add_file.setObjectName("pushButton_add_file")
        self.horizontalLayout_2.addWidget(self.pushButton_add_file)
        self.pushButton_delete_file = QtWidgets.QPushButton(self.tab)
        self.pushButton_delete_file.setObjectName("pushButton_delete_file")
        self.horizontalLayout_2.addWidget(self.pushButton_delete_file)
        self.horizontalLayout_2.setStretch(0, 2)
        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout_2.setStretch(2, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout.setStretch(1, 2)
        self.verticalLayout.setStretch(2, 22)
        self.horizontalLayout_9.addLayout(self.verticalLayout)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_export_path = QtWidgets.QLabel(self.tab)
        self.label_export_path.setAlignment(QtCore.Qt.AlignCenter)
        self.label_export_path.setObjectName("label_export_path")
        self.horizontalLayout.addWidget(self.label_export_path)
        self.lineEdit_export_path = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_export_path.setEnabled(False)
        self.lineEdit_export_path.setObjectName("lineEdit_export_path")
        self.horizontalLayout.addWidget(self.lineEdit_export_path)
        self.pushButton_export = QtWidgets.QPushButton(self.tab)
        self.pushButton_export.setObjectName("pushButton_export")
        self.horizontalLayout.addWidget(self.pushButton_export)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_export_file_type = QtWidgets.QLabel(self.tab)
        self.label_export_file_type.setObjectName("label_export_file_type")
        self.horizontalLayout_3.addWidget(self.label_export_file_type)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.radioButton_all = QtWidgets.QRadioButton(self.tab)
        self.radioButton_all.setAcceptDrops(False)
        self.radioButton_all.setChecked(True)
        self.radioButton_all.setObjectName("radioButton_all")
        self.horizontalLayout_3.addWidget(self.radioButton_all)
        self.radioButton_avi = QtWidgets.QRadioButton(self.tab)
        self.radioButton_avi.setObjectName("radioButton_avi")
        self.horizontalLayout_3.addWidget(self.radioButton_avi)
        self.radioButton_npy = QtWidgets.QRadioButton(self.tab)
        self.radioButton_npy.setObjectName("radioButton_npy")
        self.horizontalLayout_3.addWidget(self.radioButton_npy)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.pushButton_start = QtWidgets.QPushButton(self.tab)
        self.pushButton_start.setObjectName("pushButton_start")
        self.horizontalLayout_3.addWidget(self.pushButton_start)
        self.horizontalLayout_3.setStretch(0, 2)
        self.horizontalLayout_3.setStretch(1, 1)
        self.horizontalLayout_3.setStretch(2, 1)
        self.horizontalLayout_3.setStretch(3, 1)
        self.horizontalLayout_3.setStretch(4, 1)
        self.horizontalLayout_3.setStretch(5, 1)
        self.horizontalLayout_3.setStretch(6, 2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_5 = QtWidgets.QLabel(self.tab)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_7.addWidget(self.label_5)
        self.progressBar = QtWidgets.QProgressBar(self.tab)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout_7.addWidget(self.progressBar)
        self.label_progress = QtWidgets.QLabel(self.tab)
        self.label_progress.setObjectName("label_progress")
        self.horizontalLayout_7.addWidget(self.label_progress)
        self.verticalLayout_4.addLayout(self.horizontalLayout_7)
        self.line = QtWidgets.QFrame(self.tab)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_4.addWidget(self.line)
        self.groupBox = QtWidgets.QGroupBox(self.tab)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.lineEdit_process_time = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_process_time.setEnabled(False)
        self.lineEdit_process_time.setText("")
        self.lineEdit_process_time.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_process_time.setObjectName("lineEdit_process_time")
        self.horizontalLayout_4.addWidget(self.lineEdit_process_time)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)
        self.horizontalLayout_4.setStretch(0, 3)
        self.horizontalLayout_4.setStretch(1, 5)
        self.horizontalLayout_4.setStretch(2, 1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_5.addWidget(self.label_3)
        self.lineEdit_process_file_num = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_process_file_num.setEnabled(False)
        self.lineEdit_process_file_num.setText("")
        self.lineEdit_process_file_num.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_process_file_num.setObjectName("lineEdit_process_file_num")
        self.horizontalLayout_5.addWidget(self.lineEdit_process_file_num)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem6)
        self.horizontalLayout_5.setStretch(0, 3)
        self.horizontalLayout_5.setStretch(1, 5)
        self.horizontalLayout_5.setStretch(2, 1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self.treeView_outcome = QtWidgets.QTreeView(self.groupBox)
        self.treeView_outcome.setObjectName("treeView_outcome")
        self.verticalLayout_3.addWidget(self.treeView_outcome)
        self.horizontalLayout_6.addLayout(self.verticalLayout_3)
        self.verticalLayout_4.addWidget(self.groupBox)
        self.verticalLayout_4.setStretch(1, 2)
        self.verticalLayout_4.setStretch(2, 2)
        self.verticalLayout_4.setStretch(4, 2)
        self.verticalLayout_4.setStretch(5, 20)
        self.horizontalLayout_9.addLayout(self.verticalLayout_4)
        self.horizontalLayout_9.setStretch(0, 2)
        self.horizontalLayout_9.setStretch(1, 5)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout(self.tab_2)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setSpacing(6)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem7)
        self.label_6 = QtWidgets.QLabel(self.tab_2)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_5.addWidget(self.label_6)
        self.treeView_file_npy = QtWidgets.QTreeView(self.tab_2)
        self.treeView_file_npy.setObjectName("treeView_file_npy")
        self.verticalLayout_5.addWidget(self.treeView_file_npy)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem8)
        self.pushButton_add_file_npy = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_add_file_npy.setObjectName("pushButton_add_file_npy")
        self.horizontalLayout_10.addWidget(self.pushButton_add_file_npy)
        self.pushButton_delete_file_npy = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_delete_file_npy.setObjectName("pushButton_delete_file_npy")
        self.horizontalLayout_10.addWidget(self.pushButton_delete_file_npy)
        self.horizontalLayout_10.setStretch(0, 2)
        self.horizontalLayout_10.setStretch(1, 1)
        self.horizontalLayout_10.setStretch(2, 1)
        self.verticalLayout_5.addLayout(self.horizontalLayout_10)
        self.verticalLayout_5.setStretch(1, 2)
        self.verticalLayout_5.setStretch(2, 22)
        self.horizontalLayout_13.addLayout(self.verticalLayout_5)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_11.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_11.setSpacing(6)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_npy_file_path_npy = QtWidgets.QLabel(self.tab_2)
        self.label_npy_file_path_npy.setAlignment(QtCore.Qt.AlignCenter)
        self.label_npy_file_path_npy.setObjectName("label_npy_file_path_npy")
        self.horizontalLayout_11.addWidget(self.label_npy_file_path_npy)
        self.lineEdit_npy_file_path_npy = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_npy_file_path_npy.setEnabled(False)
        self.lineEdit_npy_file_path_npy.setObjectName("lineEdit_npy_file_path_npy")
        self.horizontalLayout_11.addWidget(self.lineEdit_npy_file_path_npy)
        self.verticalLayout_6.addLayout(self.horizontalLayout_11)
        self.widget_npy = QtWidgets.QWidget(self.tab_2)
        self.widget_npy.setObjectName("widget_npy")
        self.verticalLayout_6.addWidget(self.widget_npy)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem9)
        self.pushButton_previous_npy = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_previous_npy.setObjectName("pushButton_previous_npy")
        self.horizontalLayout_12.addWidget(self.pushButton_previous_npy)
        self.lineEdit_current_npy = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_current_npy.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_current_npy.setObjectName("lineEdit_current_npy")
        self.horizontalLayout_12.addWidget(self.lineEdit_current_npy)
        self.label_all_npy = QtWidgets.QLabel(self.tab_2)
        self.label_all_npy.setAlignment(QtCore.Qt.AlignCenter)
        self.label_all_npy.setObjectName("label_all_npy")
        self.horizontalLayout_12.addWidget(self.label_all_npy)
        self.pushButton_next_npy = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_next_npy.setObjectName("pushButton_next_npy")
        self.horizontalLayout_12.addWidget(self.pushButton_next_npy)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem10)
        self.horizontalLayout_12.setStretch(0, 3)
        self.horizontalLayout_12.setStretch(1, 1)
        self.horizontalLayout_12.setStretch(2, 1)
        self.horizontalLayout_12.setStretch(3, 1)
        self.horizontalLayout_12.setStretch(4, 1)
        self.horizontalLayout_12.setStretch(5, 3)
        self.verticalLayout_6.addLayout(self.horizontalLayout_12)
        self.verticalLayout_6.setStretch(0, 2)
        self.verticalLayout_6.setStretch(1, 4)
        self.verticalLayout_6.setStretch(2, 2)
        self.horizontalLayout_13.addLayout(self.verticalLayout_6)
        self.horizontalLayout_13.setStretch(0, 2)
        self.horizontalLayout_13.setStretch(1, 5)
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_2.addWidget(self.label_7)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 838, 37))
        self.menubar.setObjectName("menubar")
        self.menufile_file = QtWidgets.QMenu(self.menubar)
        self.menufile_file.setObjectName("menufile_file")
        self.menusettings = QtWidgets.QMenu(self.menubar)
        self.menusettings.setObjectName("menusettings")
        MainWindow.setMenuBar(self.menubar)
        self.actionOpen_file_open = QtWidgets.QAction(MainWindow)
        self.actionOpen_file_open.setObjectName("actionOpen_file_open")
        self.action_config = QtWidgets.QAction(MainWindow)
        self.action_config.setObjectName("action_config")
        self.menufile_file.addAction(self.actionOpen_file_open)
        self.menusettings.addAction(self.action_config)
        self.menubar.addAction(self.menufile_file.menuAction())
        self.menubar.addAction(self.menusettings.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Import File"))
        self.pushButton_add_file.setText(_translate("MainWindow", "+"))
        self.pushButton_delete_file.setText(_translate("MainWindow", "-"))
        self.label_export_path.setText(_translate("MainWindow", "Export Path:"))
        self.pushButton_export.setText(_translate("MainWindow", "select"))
        self.label_export_file_type.setText(_translate("MainWindow", "Export file type:"))
        self.radioButton_all.setText(_translate("MainWindow", "avi + npy"))
        self.radioButton_avi.setText(_translate("MainWindow", "avi"))
        self.radioButton_npy.setText(_translate("MainWindow", "npy"))
        self.pushButton_start.setText(_translate("MainWindow", "Start"))
        self.label_5.setText(_translate("MainWindow", "Progress:"))
        self.label_progress.setText(_translate("MainWindow", "0%"))
        self.groupBox.setTitle(_translate("MainWindow", "Outcome"))
        self.label_2.setText(_translate("MainWindow", "Extract Time:"))
        self.label_3.setText(_translate("MainWindow", "Extract File Num:"))
        self.label_4.setText(_translate("MainWindow", "Extract File Info:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "DEMC"))
        self.label_6.setText(_translate("MainWindow", "Npy Viewer Import File"))
        self.pushButton_add_file_npy.setText(_translate("MainWindow", "+"))
        self.pushButton_delete_file_npy.setText(_translate("MainWindow", "-"))
        self.label_npy_file_path_npy.setText(_translate("MainWindow", "npy file path"))
        self.pushButton_previous_npy.setText(_translate("MainWindow", "<"))
        self.label_all_npy.setText(_translate("MainWindow", "/ --"))
        self.pushButton_next_npy.setText(_translate("MainWindow", ">"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "npy Viewer"))
        self.label_7.setText(_translate("MainWindow", "v2.0.2"))
        self.menufile_file.setTitle(_translate("MainWindow", "File"))
        self.menusettings.setTitle(_translate("MainWindow", "Settings"))
        self.actionOpen_file_open.setText(_translate("MainWindow", "Open..."))
        self.action_config.setText(_translate("MainWindow", "set config"))
