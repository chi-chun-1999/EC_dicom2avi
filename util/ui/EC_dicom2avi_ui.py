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
        MainWindow.resize(830, 780)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(30, 0, 241, 691))
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.widget)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_file = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_file.setObjectName("pushButton_file")
        self.horizontalLayout_2.addWidget(self.pushButton_file)
        self.pushButton_export = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_export.setObjectName("pushButton_export")
        self.horizontalLayout_2.addWidget(self.pushButton_export)
        self.verticalLayout.addWidget(self.groupBox)
        self.listWidget_file = QtWidgets.QListWidget(self.widget)
        self.listWidget_file.setObjectName("listWidget_file")
        self.verticalLayout.addWidget(self.listWidget_file)
        self.verticalLayout.setStretch(1, 8)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 830, 37))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_file.setText(_translate("MainWindow", "File"))
        self.pushButton_export.setText(_translate("MainWindow", "Export"))
