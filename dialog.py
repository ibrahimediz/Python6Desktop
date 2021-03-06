import sys
import os
from AnaDB import Veritabani
from PyQt5.QtWidgets import QApplication,QDialog,QTableWidgetItem,QMessageBox
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic

class Dialog(QDialog):

    eklenen = pyqtSignal(list)

    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)
        ## veritabanı ve arayüz dosyaları çağırılıyor
        self.vt = Veritabani(os.getcwd()+r"\IEDB.db")
        self.pencere = uic.loadUi(os.getcwd()+r"\sozluk.ui")
        self.TabloDoldur()
        self.pencere.lstSozluk.itemDoubleClicked.connect(self.secim)
        self.pencere.btIptal.clicked.connect(self.pencere.close)
        self.pencere.btKaydet.clicked.connect(self.Kaydet)
    def TabloDoldur(self):
        self.pencere.lstSozluk.clear()
        self.liste = self.vt.TumSozlukListele()
        self.pencere.lstSozluk.setHorizontalHeaderLabels(("ID","TABLOID","SOZLUKID","SOZLUKADI"))
        self.pencere.lstSozluk.setRowCount(15)
        self.pencere.lstSozluk.setColumnCount(4)
        satir = 0
        for a,b,c,d in self.liste:
            self.pencere.lstSozluk.setItem(satir,0,QTableWidgetItem(str(a)))
            self.pencere.lstSozluk.setItem(satir,1,QTableWidgetItem(str(b)))
            self.pencere.lstSozluk.setItem(satir,2,QTableWidgetItem(str(c)))
            self.pencere.lstSozluk.setItem(satir,3,QTableWidgetItem(str(d)))
            satir += 1
    
    def secim(self):
        ADI = str(self.liste[self.pencere.lstSozluk.currentRow()][2])
        TABLO = str(self.liste[self.pencere.lstSozluk.currentRow()][3])
        ID = str(self.liste[self.pencere.lstSozluk.currentRow()][0])
        SOZID = str(self.liste[self.pencere.lstSozluk.currentRow()][1])
        self.pencere.lblKayit.setText(ID)
        self.pencere.txtTablo.setText(TABLO)
        self.pencere.txtAd.setText(ADI)
        self.pencere.txtID.setText(SOZID)

    def Kaydet(self):
        ID = self.pencere.lblKayit.text()
        tablo = self.pencere.txtTablo.text()
        sozlukAdi = self.pencere.txtAd.text()
        sozlukID = self.pencere.txtID.text()
       
        if ID == "":
            sonuc = self.vt.SozlukVeriEkle(tablo,sozlukID,sozlukAdi)
        else:
            sonuc = self.vt.SozlukVeriGuncelle(tablo,sozlukID,sozlukAdi,ID)

        gonderListe = [sozlukAdi,sozlukID]
        self.eklenen.emit(gonderListe)
        if sonuc == "1":
            self.Mesaj(1,"Bilgi","Başarıyla Kaydedildi")
            self.Temizle()
            self.TabloDoldur()
        else:
            self.Mesaj(2,"Kayıt Hatası",sonuc)
    
    def Mesaj(self,icon,baslik,metin):
        sonuc = True
        if icon == 1:
            QMessageBox.information(self,baslik,metin,QMessageBox.Ok)
        elif icon == 2:
            QMessageBox.critical(self,baslik,metin,QMessageBox.Ok)
        elif icon == 3:
            QMessageBox.warning(self,baslik,metin,QMessageBox.Ok)
        elif icon == 4:
            try:
                cevap =  QMessageBox.question(self,baslik,metin,QMessageBox.Ok|QMessageBox.Cancel,QMessageBox.Cancel)
                if cevap == QMessageBox.Ok:
                    sonuc = True
                else:
                    sonuc = False
            except:
                print("Hata")
        return sonuc
    
    def Temizle(self):
        self.pencere.txtAd.setText("")
        self.pencere.txtID.setText("")
        self.pencere.txtTablo.setText("")
        self.pencere.lblKayit.setText("")