#!/usr/bin/env python3
import sys
from os import path
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication,)
from cvwidget2 import MainWidget as FDWidget

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.GraphicsWindow = QVBoxLayout()
        self.fd = FDWidget(path.abspath(path.join(path.dirname(path.realpath(__file__)), 'haarcascade_frontalface_default.xml')), scale=(self.geometry().height()/350), feed="/dev/video0")
        self.messagepanellayout = QVBoxLayout()
        self.CVPanel = QHBoxLayout()
        self.CVPanel.addWidget(self.fd.face_detection_widget)

        self.CVPanel.addLayout(self.messagepanellayout)
        self.CVPanelHeading = QHBoxLayout()
        self.InfoPanelLabels = QHBoxLayout()
        self.InfoPanel = QHBoxLayout()
        self.GraphicsWindow.addLayout(self.CVPanelHeading)
        self.GraphicsWindow.addLayout(self.CVPanel)
        self.hbox = QHBoxLayout()
        self.hbox.setContentsMargins(10, 10, 10, 10)
        self.hbox.addLayout(self.GraphicsWindow)
        self.setLayout(self.hbox)
        self.setMinimumSize(500,500)
        self.setWindowTitle('Test')
        self.show()

    def paintEvent(self, e):
        #self.fd.face_detection_widget.update()
        self.fd.update()
        painter = QtGui.QPainter(self)
        self.brush = QtGui.QBrush()
        self.brush.setColor(QtGui.QColor('#222223'))
        self.brush.setStyle(QtCore.Qt.SolidPattern)
        self.rect = QtCore.QRect(0, 0, painter.device().width(), painter.device().height())
        painter.fillRect(self.rect, self.brush)
        self.vrecti = QtCore.QRect(0, 0, (painter.device().height() * 0.29), painter.device().height())
        self.fd.face_detection_widget.setGeometry(QtCore.QRect(painter.device().width()*0.25, painter.device().height()*0.06, painter.device().width()*0.35, painter.device().height()*0.35))  

def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()