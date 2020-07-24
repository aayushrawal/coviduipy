import sys
from os import path

import cv2
import numpy as np

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import random


class RecordVideo(QtCore.QObject):
    image_data = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, camera_port=0, parent=None):
        super().__init__(parent)
        self.timer = QtCore.QBasicTimer()
        self.stop = False
        self.camera_port = camera_port
        self.counter = 0
        self.counter2 = 0
        self.camera = cv2.VideoCapture(self.camera_port)
        #self.camera.set(cv2.CAP_PROP_BUFFERSIZE, 0)

    def start_recording(self):
        self.timer.start(0, self)

    def stoprec(self):
        self.stop = True

    def startrec(self):
        self.stop = False

    def timerEvent(self, event):
        if (event.timerId() != self.timer.timerId()):
            return
        if self.stop:
            return
        read, data = self.camera.read()
        print(data)
        total_frames = self.camera.get(cv2.CAP_PROP_FRAME_COUNT)

        if read:
            if(data.shape[0]>640):
                if(data.shape[0]>4000):
                    scale_percent = 5
                elif(data.shape[0] > 2000):
                    scale_percent = 10
                elif (data.shape[0] > 1000):
                    scale_percent = 20
                elif (data.shape[0] > 640):
                    scale_percent = 35

                # calculate the 50 percent of original dimensions
                width = int(data.shape[1] * scale_percent / 100)
                height = int(data.shape[0] * scale_percent / 100)

                # dsize
                dsize = (width, height)

                # resize image
                data = cv2.resize(data, dsize)
                print(data)
                exit(1)
            self.image_data.emit(data)
            #if cv2.waitKey(210):
            #    return
        if(self.counter>1):
            self.camera.set(cv2.CAP_PROP_POS_FRAMES, total_frames-2)
            self.counter = 0
            self.counter2 = self.counter2 + 1
        if (self.counter2 >= 40):
            self.camera.release()
            self.counter = 0
            self.counter2 = 0
            self.camera = cv2.VideoCapture(self.camera_port)
        else:
            self.counter = self.counter + 1

class FaceDetectionWidget(QtWidgets.QWidget):
    def __init__(self, haar_cascade_filepath, parent=None, scale=1.3):
        super().__init__(parent)
        self.classifier = cv2.CascadeClassifier(haar_cascade_filepath)
        self.image = QtGui.QImage()
        self._red = (0, 0, 255)
        self._green = (0, 255, 0)
        self._orange = (0, 20, 155)
        self._width = 2
        self._min_size = (30, 30)
        self.vsc = scale
        self.temp = [0, 0, 0, 0]
        self.stop = False

    def detect_faces(self, image: np.ndarray):
        # haarclassifiers work better in black and white
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_image = cv2.equalizeHist(gray_image)

        faces = self.classifier.detectMultiScale(gray_image,
                                                 scaleFactor=1.3,
                                                 minNeighbors=4,
                                                 flags=cv2.CASCADE_SCALE_IMAGE,
                                                 minSize=self._min_size)
        return faces

    def ktof(self, val):
        return (1.8 * self.ktoc(val) + 32.0)

    def ktoc(self, val):
        return (val - 27315) / 100.0

    def raw_to_8bit(self, data):
        cv2.normalize(data, data, 0, 65535, cv2.NORM_MINMAX)
        np.right_shift(data, 8, data)
        return cv2.cvtColor(np.uint8(data), cv2.COLOR_GRAY2RGB)

    def display_temperature(self, img, val_k, loc, color):
        val = self.ktof(val_k)
        cv2.putText(img, "{0:.1f} degF".format(val), loc, cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)
        x, y = loc
        cv2.line(img, (x - 2, y), (x + 2, y), color, 1)
        cv2.line(img, (x, y - 2), (x, y + 2), color, 1)

    def image_data_slot(self, image_data):

        self.temp[1] = 0
        self.temp[2] = 0
        self.temp[3] = 0
        self.temp[0] = self.temp[0] = max(self.temp[0],int(image_data[:,:,0].max()))

        if(not self.stop):
            faces = self.detect_faces(image_data)
            for (x, y, w, h) in faces:
                try:
                    forhead_roi = image_data[x: (int((x + w))), y:(int((y + h) / 2))]
                    Lsinus_roi = image_data[x:int((x + w/3.5)), int((y + h)/1.7): int((y + h) / 1.2)]
                    Rsinus_roi = image_data[int((x + w - (w/3.5))):int((x+w)), int((y + h)/1.7): int((y + h) / 1.2)]


                    err = 50
                    self.temp[1] = int(forhead_roi[:, :, 0].max()) - err
                    self.temp[2] = int(Lsinus_roi[:, :, 0].max()) - err
                    self.temp[3] = int(Rsinus_roi[:, :, 0].max()) - err
                    self.temp[0] = max(self.temp[1], self.temp[2], self.temp[3])

                    for aa in range(len(self.temp)):
                        temptemp = self.temp[aa]
                        if (temptemp > 145):
                            temptemp = temptemp - 48
                        if (temptemp < 55):
                            temptemp = temptemp + 48
                        #if (temptemp < 95) or (temptemp > 100):
                        #    temptemp = int(random.randrange(96, 99))
                        self.temp[aa] = temptemp


                    cv2.rectangle(image_data,  # Face
                                  (x, y),
                                  (x + w, y + h),
                                  self._red,
                                  self._width)
                    cv2.rectangle(image_data,  # ForHead
                                  (x, y),
                                  (int((x + w)), int((y + h) / 2)),
                                  self._green,
                                  self._width)
                    cv2.rectangle(image_data,  # SinusLeft
                                  (x, int((y + h) / 1.7)),
                                  (int((x + w / 3.5)), int((y + h) / 1.2)),
                                  self._orange,
                                  self._width)
                    cv2.rectangle(image_data,  # SinusRight
                                  (int((x + w - (w / 3.5))), int((y + h) / 1.7)),
                                  (int((x + w)), int((y + h) / 1.2)),
                                  self._orange,
                                  self._width)

                    
                    image_data = cv2.putText(image_data,str(self.temp[1]),(x,y),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,0,0),1)
                    image_data = cv2.putText(image_data,str(self.temp[2]),(x-20, int((y + h)/1.7)),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,0,0),1)
                    image_data = cv2.putText(image_data,str(self.temp[3]),(int((x + w - (w/3.5))), int((y + h)/1.7)),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,0,0),1)

                except(ValueError):
                    pass


        image_data = cv2.resize(image_data,(int(320*self.vsc),int(240*self.vsc)),interpolation=cv2.INTER_AREA)
        nx = image_data.shape[1]
        ny = image_data.shape[0]
        if(self.temp[0]==0):
            pass
        if (len(faces) == 0):
            point_roi = image_data[int(nx / 2) - 2:int(nx / 2) + 2, int(ny / 4) - 2:int(ny / 4) + 2]
            try:
                self.temp[0] = int(point_roi[:, :, 0].max())
            except:
                print("Max temp error")
            image_data = cv2.putText(image_data, str("+"), (int(nx / 2) - 5, int(ny / 4) - 5), cv2.FONT_HERSHEY_SIMPLEX,
                                     0.7,
                                     (255, 0, 0), 2)
        self.image = self.get_qimage(image_data)
        if self.image.size() != self.size():
            self.setFixedSize(self.image.size())
        #self.image = cv2.resize(self.image, (320, 240), interpolation=cv2.INTER_AREA)
        self.update()


    def gettemp(self):
        return(self.temp)

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

    def stoprec(self):
        self.stop = True

    def startrec(self):
        self.stop = False

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        #self.image = cv2.resize(self.image, (640, 480), interpolation=cv2.INTER_AREA)
        painter.drawImage(0, 0, self.image)
        self.image = QtGui.QImage()


class MainWidget(QtWidgets.QWidget):
    def __init__(self, haarcascade_filepath, parent=None, scale=1.3, feed=0):
        super().__init__(parent)
        fp = haarcascade_filepath
        self.face_detection_widget = FaceDetectionWidget(fp,scale=scale)

        self.face_detection_widget.vsc = scale

        # TODO: set video port
        self.record_video = RecordVideo(feed)#"I:\\The.Big.Bang.Theory.S11.720p.WEB-DL.x264.AAC\\s11e1.mp4")

        image_data_slot = self.face_detection_widget.image_data_slot
        self.record_video.image_data.connect(image_data_slot)

        layout = QtWidgets.QVBoxLayout()

        layout.addWidget(self.face_detection_widget)

        self.record_video.start_recording()
        self.setLayout(layout)

def main(haar_cascade_filepath):
    app = QtWidgets.QApplication(sys.argv)

    main_window = QtWidgets.QMainWindow()
    main_widget = MainWidget(haar_cascade_filepath)
    main_window.setCentralWidget(main_widget)
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    script_dir = path.dirname(path.realpath(__file__))
    cascade_filepath = path.join(script_dir,'haarcascade_frontalface_default.xml')

    cascade_filepath = path.abspath(cascade_filepath)
    main(cascade_filepath)