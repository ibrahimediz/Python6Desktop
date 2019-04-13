import sys
from AnaDB import Veritabani
from PyQt5.QtWidgets import QApplication,QMainWindow,QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

class Ana(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__()
        ## veritabanı ve arayüz dosyaları çağırılıyor
        self.vt = Veritabani(r"D:\İbrahim EDİZ\DesktopProje\IEDB.db")
        self.win = uic.loadUi(r"D:\İbrahim EDİZ\DesktopProje\ana.ui")
        
        ## Arayüzdeki nesneler veritabanından dolduruluyor
        self.InitUI()
        self.TabloDoldur()
        ## Arayüzdeki Nesnelere Fonksiyonlar Atanıyor
        self.win.btYeni.clicked.connect(self.InitUI)

        self.win.btKaydet.clicked.connect(self.Kaydet)
        ## Ekranda Gösterim için
        self.win.show()

    def Kaydet(self):
        kalem = self.win.cmbKalem.currentIndex()
        ay = self.win.cmbAy.currentIndex()
        tutar =  self.win.txtTutar.text()
        self.vt.VeriEkle(kalem,ay,tutar)

    def TabloDoldur(self):
        liste = self.vt.Listele()
        self.win.lstHarcama.setHorizontalHeaderLabels(("ID","KALEM","TUTAR","AY"))
        self.win.lstHarcama.setRowCount(15)
        self.win.lstHarcama.setColumnCount(4)
        satir = 0
        for a,b,c,d in liste:
            self.win.lstHarcama.setItem(satir,0,QTableWidgetItem(str(a)))
            self.win.lstHarcama.setItem(satir,1,QTableWidgetItem(str(b)))
            self.win.lstHarcama.setItem(satir,2,QTableWidgetItem(str(c)))
            self.win.lstHarcama.setItem(satir,3,QTableWidgetItem(str(d)))
            satir += 1

        

    def InitUI(self):
        # Ay 
        self.cmbAyDoldur()
        # Kalem
        self.cmbKalemDoldur()
        #Tutar
        self.win.txtTutar.setText("")
        self.win.lblKayit.setText("")

    def cmbAyDoldur(self):
        # Ay Combosu Dolduruluyor 
        self.win.cmbAy.clear()
        self.win.cmbAy.addItem("Seçiniz",-1)
        for a,b in self.vt.SozlukListele(2):
            self.win.cmbAy.addItem(a,b)
    
    def cmbKalemDoldur(self):
        # Kalem Combosu Dolduruluyor 
        self.win.cmbKalem.clear()
        self.win.cmbKalem.addItem("Seçiniz",-1)
        for a,b in self.vt.SozlukListele(1):
            self.win.cmbKalem.addItem(a,b)

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Ana()
    sys.exit(app.exec_())




