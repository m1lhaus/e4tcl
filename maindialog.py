# -*- coding: utf-8 -*-

import os
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import mainform


class MainDialog(QMainWindow, mainform.Ui_MainWindow):

    def __init__(self, args):
        super(MainDialog, self).__init__()
        self.setupUi(self)

    @pyqtSlot()
    def addFolder(self):
        pass
        # open file dialog
        # get selected files
        # add them to folderList

    @pyqtSlot()
    def removeFolder(self):
        pass
        # get selected folder from folderList
        # remove this folder from folderList

    @pyqtSlot()
    def generate(self):
        pass
        # get all paths from folder list
        # call parser methods
        # display pop-up when its done
