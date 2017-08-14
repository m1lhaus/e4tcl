# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uic\mainform.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(505, 168)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/e4tcl.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.fileList = QtWidgets.QListWidget(self.centralwidget)
        self.fileList.setMinimumSize(QtCore.QSize(250, 0))
        self.fileList.setObjectName("fileList")
        self.horizontalLayout.addWidget(self.fileList)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.addBtn = QtWidgets.QPushButton(self.centralwidget)
        self.addBtn.setObjectName("addBtn")
        self.verticalLayout.addWidget(self.addBtn)
        self.removeBtn = QtWidgets.QPushButton(self.centralwidget)
        self.removeBtn.setObjectName("removeBtn")
        self.verticalLayout.addWidget(self.removeBtn)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.nokiaCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.nokiaCheckBox.setObjectName("nokiaCheckBox")
        self.verticalLayout.addWidget(self.nokiaCheckBox)
        self.generateBtn = QtWidgets.QPushButton(self.centralwidget)
        self.generateBtn.setObjectName("generateBtn")
        self.verticalLayout.addWidget(self.generateBtn)
        self.horizontalLayout.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "e4tcl"))
        self.addBtn.setText(_translate("MainWindow", "Add"))
        self.removeBtn.setText(_translate("MainWindow", "Remove"))
        self.nokiaCheckBox.setText(_translate("MainWindow", "Nokia phone"))
        self.generateBtn.setText(_translate("MainWindow", "Generate"))

import icons_rc
