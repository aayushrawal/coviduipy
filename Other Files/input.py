import numpy
import cv2

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

import sys

import numpy as np


class MyDialog(QtWidgets.QWidget):

    image_data = QtCore.pyqtSignal(np.ndarray)
    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)
        self.input_stream = cv2.VideoCapture("video.mp4")
        self.timer = QtCore.QBasicTimer()

    def start_recording(self):

        self.timer.start(0, self)

    def timerEvent(self, event):
        
        if (event.timerId() != self.timer.timerId()):
            return
        flag, self.cvImage = self.input_stream.read()
        if flag:
            self.image_data.emit(self.cvImage)
            #self.image_data.connect(self.cvImage)

    def testfunc(self,image_data):
        height, width, byteValue =image_data.shape
        byteValue = byteValue * 640

        cv2.cvtColor(image_data, cv2.COLOR_BGR2RGB, image_data)

        self.mQImage = QtGui.QImage(image_data, 320*1.3,240*1.3, byteValue, QtGui.QImage.Format_RGB888)

        """ if self.mQImage.size() != self.size():
            self.setFixedSize(self.mQImage.size()) """

        self.update()


    def paintEvent(self, QPaintEvent):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.drawImage(0, 0, self.mQImage)
        self.mQImage = QtGui.QImage()
        #self.update()
        #painter.end()

class MainWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.test = MyDialog()
        self.t=self.test.testfunc
        self.u=self.test.start_recording()
        self.test.image_data.connect(self.t)
        layout=QtWidgets.QVBoxLayout()
        layout.addWidget(self.test)
        self.setLayout(layout)
    

def main():

    app = QtWidgets.QApplication(sys.argv)

    main_window = QtWidgets.QMainWindow()
    main_widget = MainWidget()
    main_window.setCentralWidget(main_widget)
    main_window.show()
    sys.exit(app.exec_())
    sys.exit()


if __name__=="__main__":
    main()
    