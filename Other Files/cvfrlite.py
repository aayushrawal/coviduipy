import sys
from os import path
import os
import cv2
import numpy as np

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from statistics import mode


class RecordVideo(QtCore.QObject):
    image_data = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, camera_port="/dev/video3", parent=None):
        super().__init__(parent)
        self.camera_port = camera_port
        self.camera = cv2.VideoCapture(camera_port)
        self.timer = QtCore.QBasicTimer()

    def start_recording(self):

        self.timer.start(0, self)

    def timerEvent(self, event):
        
        if (event.timerId() != self.timer.timerId()):
            return
        read, data = self.camera.read()
        total_frames = self.camera.get(cv2.CAP_PROP_FRAME_COUNT)
  
        if read:
            self.image_data.emit(data)
        

class FaceDetectionWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, scale=1.3):
        super().__init__(parent)

        image_data = RecordVideo()
        
        self.image = QtGui.QImage()
        self.vsc = scale


    def image_data_slot(self, image_data):
        image_data = cv2.resize(image_data, (int(320*self.vsc), int(240*self.vsc)), interpolation=cv2.INTER_AREA)
        self.image = self.get_qimage(image_data)
        if self.image.size() != self.size():
            self.setFixedSize(self.image.size())
        
        self.update()
        


    def get_qimage(self, image: np.ndarray):
        height, width, colors = image.shape
        bytesPerLine = 3 * width
        QImage = QtGui.QImage

        image = QImage(image.data,
                       width,
                       height,
                       bytesPerLine,
                       QImage.Format_RGB888)

        image = image.rgbSwapped()
        return image

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QtGui.QImage()
        


class MainWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, scale=1, feed="video.mp4"):
        super().__init__(parent)
        self.face_detection_widget = FaceDetectionWidget(scale=scale)
        self.face_detection_widget.vsc = scale
        self.record_video = RecordVideo(feed)
        self.record_video.start_recording()
        image_data_slot = self.face_detection_widget.image_data_slot
        self.record_video.image_data.connect(image_data_slot)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.face_detection_widget)
        self.setLayout(layout)

def main():
    app = QtWidgets.QApplication(sys.argv)

    main_window = QtWidgets.QMainWindow()
    main_widget = MainWidget()
    main_window.setCentralWidget(main_widget)
    main_window.show()
    sys.exit(app.exec_())
    sys.exit()


if __name__ == '__main__':
    main()