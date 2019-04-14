import sys
import os
from AnaDB import Veritabani
from PyQt5.QtWidgets import QApplication,QDialog,QTableWidgetItem,QMessageBox
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

class Dialog(QDialog):
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)
        ## veritabanı ve arayüz dosyaları çağırılıyor
        self.vt = Veritabani(os.getcwd()+r"\IEDB.db")
        self.pencere = uic.loadUi(os.getcwd()+r"\sozluk.ui")
        self.pencere.btIptal.clicked.connect(self.pencere.close)
