import sys
import psutil
import time
import threading

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import pyqtgraph as pg
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

import numpy as np
import random
import psutil

class MainWin(QtWidgets.QWidget):
    
    def __init__(self):
        super().__init__()
        self.timeCounter=0
        self.arrCounter=[]
        self.listDataRecv=[]
        self.listDataSent=[]
        self.maxTimer=0
        self.aturWin()

    def aturWin(self):
        #self.setFixedSize(self.size())
        self.setWindowTitle("Informasi Sistem Operasi")
        # atur layout utama
        self.winLayout = QtWidgets.QHBoxLayout(self)
        
        # atur layout-layout pendukung dan frame

        self.topLeftFrame = QtWidgets.QFrame()
        self.topLeftFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.topRightFrame = QtWidgets.QFrame()
        self.topRightFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.bottomLeftFrame = QtWidgets.QFrame()
        self.bottomLeftFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.bottomRightFrame = QtWidgets.QFrame()
        self.bottomRightFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        
        self.spliterAtas = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.spliterTengah = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        self.spliterBawah = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

        # posisi tampilan
        self.spliterAtas.addWidget(self.topLeftFrame)
        self.spliterAtas.addWidget(self.topRightFrame)

        self.spliterBawah.addWidget(self.bottomLeftFrame)
        self.spliterBawah.addWidget(self.bottomRightFrame)
        
        self.spliterTengah.addWidget(self.spliterAtas)
        self.spliterTengah.addWidget(self.spliterBawah)
        
        
        # atur grafik jaringan
        self.layOutNetwork = QtWidgets.QGridLayout(self.topLeftFrame)
        self.figNetwork = pg.GraphicsLayoutWidget()
        self.layOutNetwork.addWidget(self.figNetwork)
        
        self.p1=self.figNetwork.addPlot(title="Data In")
        self.c1 = self.p1.plot(pen="r",clear=True)
        self.p1.setLabel("left","Kbytes")
        self.p1.setLabel("bottom","Waktu (s)")
        
        self.figNetwork.nextRow()
        self.p2=self.figNetwork.addPlot(title="Data Out")
        self.c2 = self.p2.plot(pen="y",clear=True)
        self.p2.setLabel("left","Kbytes")
        self.p2.setLabel("bottom","Waktu (s)")
        
        # atur grafik memory
        self.layOutMemory = QtWidgets.QGridLayout(self.bottomLeftFrame)
        self.figMemory = plt.figure()
        self.canvas = FigureCanvas(self.figMemory)
        self.layOutMemory.addWidget(self.canvas)

        self.ax1 = self.figMemory.add_subplot(131)
        self.ax1.set_title("Memory Fisik")
        
        self.ax2 = self.figMemory.add_subplot(132)
        self.ax2.set_title("Memory Swapping")

        self.ax3 = self.figMemory.add_subplot(133)
        self.ax3.set_title("CPU")

        plt.tight_layout()

        self.spliterBawah.addWidget(self.bottomLeftFrame)
        
        # atur tabel proses
        self.tblProses = QtWidgets.QTableWidget(0,4)
        self.tblProses.setSelectionMode( QtWidgets.QAbstractItemView.MultiSelection )
        self.tblProses.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.tblProses.setHorizontalHeaderLabels( ["#ProcessID","Nama Proses","Username","Mem Percent"] )
        
        self.layOutProses = QtWidgets.QGridLayout(self.bottomRightFrame)
        self.layOutProses.addWidget(self.tblProses)

        self.spliterBawah.addWidget(self.bottomRightFrame)

        # atur info Disk
        fnt = QtGui.QFont()
        fnt.setPointSize(16)
        fnt.setBold(True)
        fnt.setWeight(75)
        

        lblPartisi = QtWidgets.QLabel("Jumlah Disk:")
        lblPartisi.setFont(fnt)
        self.lblPartisiJumlah = QtWidgets.QLabel("0")
        self.lblPartisiJumlah.setFont(fnt)
        self.lblPartisiJumlah.setStyleSheet("background-color:yellow;")
        lblTotal = QtWidgets.QLabel("Ukuran:")
        lblTotal.setFont(fnt)
        self.lblTotalJumlah = QtWidgets.QLabel("0")
        self.lblTotalJumlah.setFont(fnt)
        self.lblTotalJumlah.setStyleSheet("background-color:yellow;")
        lblTerisi = QtWidgets.QLabel("Terisi:")
        lblTerisi.setFont(fnt)
        self.lblTerisiJumlah = QtWidgets.QLabel("0")
        self.lblTerisiJumlah.setFont(fnt)
        self.lblTerisiJumlah.setStyleSheet("background-color:yellow;")
        lblKosong = QtWidgets.QLabel("Kosong:")
        lblKosong.setFont(fnt)
        self.lblKosongJumlah = QtWidgets.QLabel("0")
        self.lblKosongJumlah.setFont(fnt)
        self.lblKosongJumlah.setStyleSheet("background-color:yellow;")
        lblPersentase = QtWidgets.QLabel("Persentase:")
        lblPersentase.setFont(fnt)
        self.lblPersentaseJumlah = QtWidgets.QLabel("0")
        self.lblPersentaseJumlah.setFont(fnt)
        self.lblPersentaseJumlah.setStyleSheet("background-color:yellow;")
        
        self.layOutDisk = QtWidgets.QGridLayout(self.topRightFrame)
        self.layOutDisk.addWidget(lblPartisi,0,0)
        self.layOutDisk.addWidget(self.lblPartisiJumlah,0,1)
        self.layOutDisk.addWidget(lblTotal,1,0)
        self.layOutDisk.addWidget(self.lblTotalJumlah,1,1)
        self.layOutDisk.addWidget(lblTerisi,2,0)
        self.layOutDisk.addWidget(self.lblTerisiJumlah,2,1)
        self.layOutDisk.addWidget(lblKosong,3,0)
        self.layOutDisk.addWidget(self.lblKosongJumlah,3,1)
        self.layOutDisk.addWidget(lblPersentase,4,0)
        self.layOutDisk.addWidget(self.lblPersentaseJumlah,4,1)
        
        self.spliterAtas.addWidget(self.topRightFrame)
        
        self.winLayout.addWidget(self.spliterTengah)
        
        
        self.showMaximized()

        self.bytesSentOld=0
        self.deltaBytesSent=0
    
        self.bytesRecvOld=0
        self.deltaBytesRecv=0

        self.plot()
        
    def plot(self):
       
        # isi timer
        self.maxTimer = 3*60
        self.arrCounter.extend( 0 for x in range(self.maxTimer) )
        
        self.old_value_sent=0
        self.old_value_recv=0
        
        # fungsikan timer
        self.tmr = pg.QtCore.QTimer(self)
        self.tmr.timeout.connect(self.updateData)
        self.tmr.start(50)

        self.tmr1 = pg.QtCore.QTimer(self)
        self.tmr1.timeout.connect(self.updateMemgraph)
        self.tmr1.start(50)

        self.tmr2 = pg.QtCore.QTimer(self)
        self.tmr2.timeout.connect(self.updateProses)
        self.tmr2.start(50)

        self.tmr3 = pg.QtCore.QTimer(self)
        self.tmr3.timeout.connect(self.updateNetwork)
        self.tmr3.start(50)

    def updateMemgraph(self):
        memv = psutil.virtual_memory() 
        labelsv = 'Bebas', 'Digunakan'
        sizesv = [memv.free, memv.used]
        colorsv = ['red', 'yellowgreen']
        self.ax1.pie(sizesv,  labels=labelsv, colors=colorsv, autopct='%1.1f%%', shadow=True, startangle=140, frame=True)
        self.ax1.axis('equal')
            
        mems = psutil.swap_memory() 
        labelss = 'Bebas', 'Digunakan'
        sizess = [mems.free, mems.used]
        colorss = ['blue', 'gray']
        self.ax2.pie(sizess,  labels=labelss, colors=colorss, autopct='%1.1f%%', shadow=True, startangle=140, frame=True)
        self.ax2.axis('equal')
        
        cpu = psutil.cpu_stats()
        labelsc = 'ctx_switches', 'interupts','soft_interupts','syscalls'
        sizesc = [cpu.ctx_switches, cpu.interrupts, cpu.soft_interrupts, cpu.syscalls]
        colorsc = ['blue', 'gray','red','yellow']
        self.ax3.pie(sizesc,  labels=labelsc, colors=colorsc, autopct='%1.1f%%', shadow=True, startangle=140, frame=True)
        self.ax3.axis('equal')
        
        
    def updateProses(self):
        self.tblProses.setRowCount(0)
        self.tblProses.setRowCount(100)
        
        no=0
        for proc in psutil.process_iter( attrs=['pid', 'name', 'username','memory_percent']) :
            self.tblProses.setItem(no,0,QtWidgets.QTableWidgetItem( str(proc.pid) ))
            self.tblProses.setItem(no,1,QtWidgets.QTableWidgetItem( str(proc.info['name']) ) )
            self.tblProses.setItem(no,2,QtWidgets.QTableWidgetItem( str(proc.info['username']) ) )
            self.tblProses.setItem(no,3,QtWidgets.QTableWidgetItem( str(proc.info['memory_percent']) ) )
            no=no+1
    
    def updateNetwork(self):
        # ambil data dari psutil.net_io_counters()
        dataCard = psutil.net_io_counters()
        # menerima Bytes In
        if self.bytesSentOld == 0:
            self.deltaBytesSent =0
        else:
            self.deltaBytesSent = (dataCard.bytes_sent/1024) - self.bytesSentOld
        self.bytesSentOld = dataCard.bytes_sent/1024    
        # mengirim Bytes Out
        if self.bytesRecvOld == 0:
            self.deltaBytesRecv =0
        else:
            self.deltaBytesRecv = (dataCard.bytes_recv/1024) - self.bytesRecvOld
        self.bytesRecvOld = dataCard.bytes_sent/1024    
             
        self.listDataSent.append(self.deltaBytesSent)
        self.c1.setData(self.listDataSent)
             
        self.listDataRecv.append(self.deltaBytesRecv)
        self.c2.setData(self.listDataRecv)
         
        
    def updateData(self):
        jlhDisk = psutil.disk_partitions()
        self.lblPartisiJumlah.setText(str(len(jlhDisk)))
        jlh = psutil.disk_usage( '/' )
        self.lblTotalJumlah.setText(str(jlh.total/1000)+" mb")
        self.lblTerisiJumlah.setText(str(jlh.used/1000)+" mb")
        self.lblKosongJumlah.setText(str(jlh.free/1000)+" mb")
        self.lblPersentaseJumlah.setText(str(jlh.percent))
        
        print(str(self.arrCounter)+"-"+str(self.listDataRecv)+"\n\n")

        self.timeCounter=self.timeCounter+1
        QtCore.QCoreApplication.processEvents()
                    
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = MainWin()
    sys.exit(app.exec_())
