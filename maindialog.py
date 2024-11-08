# -*- coding: utf-8 -*-

import os
import sys
import logging

import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import mainform

import cltools

logger = logging.getLogger("")


class MainDialog(QMainWindow, mainform.Ui_MainWindow):
    def __init__(self, args):
        super(MainDialog, self).__init__()
        self.setupUi(self)

        self.fileList.setSelectionMode(QAbstractItemView.SingleSelection)

        self.addBtn.clicked.connect(self.addFiles)
        self.removeBtn.clicked.connect(self.removeFile)
        self.generateBtn.clicked.connect(self.generate)

    @pyqtSlot()
    def addFiles(self):
        logger.debug("Add button clicked, adding new files...")

        fileDialog = QFileDialog(self)
        fileDialog.setFileMode(QFileDialog.ExistingFiles)
        fileDialog.setNameFilter("Contact list (*.xlsx)")
        fileDialog.setDirectory(os.path.dirname(sys.argv[0]))

        logger.debug("Opening file dialog")
        if not fileDialog.exec_():
            logger.debug("File dialog closed, no files were chosen")
            return

        cl_files = fileDialog.selectedFiles()
        logger.debug("Selected contact list files:\n%s", "\n".join(cl_files))

        # check if file pth is already in the list
        for ffile in cl_files:
            ffile = os.path.abspath(ffile)
            found_items = self.fileList.findItems(ffile, Qt.MatchExactly)
            if not found_items:
                self.fileList.addItem(ffile)
                logger.debug("Filepath '%s' added to the fileList", ffile)
            else:
                logger.debug("Given file path '%s' already in the fileList", ffile)

    @pyqtSlot()
    def removeFile(self):
        logger.debug("Remove button clicked, removing selected file...")

        current_row = self.fileList.currentRow()
        if current_row == -1:
            logger.debug("No row deleted, because no row selected or fileList is empty")
        else:
            logger.debug("Row number '%d' will be removed from the fileList", current_row)
            self.fileList.takeItem(current_row)

    @pyqtSlot()
    def generate(self):
        logger.debug("Generate button clicked, generating contacts...")

        cl_merged = []
        for i in range(self.fileList.count()):
            cl_path = self.fileList.item(i).text()
            cl_path = os.path.abspath(cl_path)  # not necessary

            # check if given path exists
            if not os.path.isfile(cl_path):
                logger.error("Given file path '%s' does not exist!", cl_path)
                QMessageBox(QMessageBox.Critical,
                            "File not found",
                            "Given file path from the list '%s' does not exist!" % cl_path,
                            QMessageBox.Ok).exec_()
                continue

            try:
                logger.debug("Parsing cl file '%s'...", cl_path)
                cl_merged.append(cltools.load_cl(cl_path))  # parse contacts from given file
            except Exception:
                logger.exception("Error when parsing cl files")
                QMessageBox(QMessageBox.Critical,
                            "Error",
                            "Error when parsing contacts from XLSX file '%s'!" % cl_path,
                            QMessageBox.Ok).exec_()

        if not cl_merged:
            logger.debug("No contacts parsed")
            return
        else:
            if len(cl_merged) > 1:
                cl_merged = pd.concat(cl_merged)
                cl_merged = cl_merged.drop_duplicates()
            else:
                cl_merged = cl_merged[0]

        logger.debug("Dumping contacts into vCard format...")
        vcard_data = cltools.cl2vcard(cl_merged, self.nokiaCheckBox.isChecked())  # dump contacts to vcard format

        if not vcard_data:
            logger.debug("No contacts in vCard format")
            return

        if self.nokiaCheckBox.isChecked():
            dialog_path = os.path.join(os.path.dirname(sys.argv[0]), "backup.dat")
            dialog_filter = "Data file(*.dat)"
        else:
            dialog_path = os.path.dirname(sys.argv[0])
            dialog_filter = "vCard file(*.vcf)"
        selected_file, _ = QFileDialog.getSaveFileName(self, "Save file location", dialog_path, dialog_filter)
        logger.debug("Selected save location '%s'", selected_file)

        if not selected_file:
            logger.debug("No save file chosen")
            return

        try:
            cltools.write_vcf(selected_file, vcard_data)
        except Exception:
            logger.exception("Error when writing down generated contacts")
            QMessageBox(QMessageBox.Critical,
                        "Error",
                        "Error occurred when creating output file '%s'! "
                        "Check if you have write permissions to this location.",
                        QMessageBox.Ok).exec_()

        else:
            logger.debug("Generated contacts successfully written to '%s'", selected_file)
            QMessageBox(QMessageBox.Information,
                        "Finished",
                        "Generated contacts successfully written to '%s'" % selected_file,
                        QMessageBox.Ok).exec_()
