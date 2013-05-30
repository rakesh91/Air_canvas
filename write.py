#!/usr/bin/python
import time
import cv2
import cwiid 
import thread
import numpy as np
from PyQt4 import QtGui, QtCore


class Gui(QtGui.QWidget):
    
    def __init__(self):
        super(Gui, self).__init__()
        self.ptsArry=[]
        self.ARRAY=[]
        self.initUI()
        
    def initUI(self):      
        self.button = QtGui.QPushButton('Clear', self)
        self.button.clicked.connect(self.clear)
        self.setGeometry(300, 300, 1024, 788)
        self.setWindowTitle('Colors')
        self.show()

    def paintEvent(self, e):
	qp = QtGui.QPainter()
        qp.begin(self)
        self.drawRectangles(qp)

    def clear(self):
        a=[]
        t=[]
        RED=[0,0,255]
        for i in range(768):
            t=[]
            for j in range(1024):
                t.append(255)

            a.append(t)

        a = np.array(a,dtype="int16")

        for j in range(len(self.ARRAY)):
            p=self.ARRAY[j]
            for i in range(len(p)-1):
                f=tuple(p[i])
                f1=tuple(p[i+1])
                cv2.line(a,f,f1,RED,2)
        cv2.imwrite('myimage.png', a)
        self.ptsArry=[]
        self.ARRAY=[]
        thread.start_new_thread( self.update,() )        
        
    def drawRectangles(self, qp):
         pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.setBrush(QtGui.QColor(0, 0, 0))
        for j in range(len(self.ARRAY)):
            p=self.ARRAY[j]
            for i in range(len(p)-1):
                qp.drawLine(p[i][0], p[i][1],p[i+1][0],p[i+1][1])
        for i in range(len(self.ptsArry)-1):
            qp.drawLine(self.ptsArry[i][0], self.ptsArry[i][1],self.ptsArry[i+1][0], self.ptsArry[i+1][1])



def detect(m):
    flag=1
    count=0
    #Connect to the wii remote
    print 'Put Wiimote in discoverable mode now (press 1+2)...'
    w = cwiid.Wiimote()
    # Request nunchuk to be active.
    w.rpt_mode = cwiid.RPT_IR
   # Turn on LED1 so we know we're connected.
    w.led = 1
    while 1:
        try:
            x= w.state['ir_src'][0]['pos'][0]
            y= w.state['ir_src'][0]['pos'][1]
            flag=1
            m.ptsArry.append([(1024-x),(768-y)])
            draw(m) 
            time.sleep(0.01)
        except Exception, e:
            x=0
            y=0
            if flag==1:
                flag=-1
                m.ARRAY.append(m.ptsArry)
                m.ptsArry=[]

def draw(m):
    m.update()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = Gui()
    thread.start_new_thread( detect,(ex,) )
    sys.exit(app.exec_())
