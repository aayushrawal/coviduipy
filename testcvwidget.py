#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from os import path
import cv2
import numpy as np
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from uvctypes import *
import time
try:
  from queue import Queue
except ImportError:
  from Queue import Queue
import platform

class RecordVideo(QtCore.QObject):
    image_data = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, camera_port=0, parent=None):
        super().__init__(parent)
        self.camera = cv2.VideoCapture(camera_port)
        self.timer = QtCore.QBasicTimer()
    ##
    BUF_SIZE = 2
    q = Queue(BUF_SIZE)

    def py_frame_callback(self,frame, userptr):

        array_pointer = cast(frame.contents.data, POINTER(c_uint16 * (frame.contents.width * frame.contents.height)))
        data = np.frombuffer(array_pointer.contents, dtype=np.dtype(np.uint16)).reshape(rame.contents.height, frame.contents.width)

        if frame.contents.data_bytes != (2 * frame.contents.width * frame.contents.height):
            return

        if not q.full():
            q.put(data)

    PTR_PY_FRAME_CALLBACK = CFUNCTYPE(None, POINTER(uvc_frame), c_void_p)(py_frame_callback)
    ##
    def start_recording(self):
        self.timer.start(0, self)

    def timerEvent(self, event):
        if (event.timerId() != self.timer.timerId()):
            return
        ##
        try:
        while True:
          data, read = q.get(True, 500)
          if data is None:
            break
        ##
        #read, data = self.camera.read()
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
        if read:
            self.image_data.emit(data)


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
        faces = self.detect_faces(image_data)

        for (x, y, w, h) in faces:
            #self.temp = x
            cv2.rectangle(image_data, # Face
                          (x, y),
                          (x+w, y+h),
                          self._red,
                          self._width)
            cv2.rectangle(image_data, #ForHead
                          (x, y),
                          (int((x + w)), int((y + h) / 2)),
                          self._green,
                          self._width)
            cv2.rectangle(image_data, #SinusLeft
                          (x, int((y + h)/1.7)),
                          (int((x + w/3.5)), int((y + h) / 1.2)),
                          self._orange,
                          self._width)
            cv2.rectangle(image_data, #SinusRight
                          (int((x + w - (w/3.5))), int((y + h)/1.7)),
                          (int((x+w)), int((y + h) / 1.2)),
                          self._orange,
                          self._width)

            try:
                forhead_roi = image_data[x: (int((x + w))), y:(int((y + h) / 2))]
                Lsinus_roi = image_data[x:int((x + w/3.5)), int((y + h)/1.7): int((y + h) / 1.2)]
                Rsinus_roi = image_data[int((x + w - (w/3.5))):int((x+w)), int((y + h)/1.7): int((y + h) / 1.2)]


                err = 20
                self.temp[1] = int(forhead_roi[:, :, 0].max()) - err
                self.temp[2] = int(Lsinus_roi[:, :, 0].max()) - err
                self.temp[3] = int(Rsinus_roi[:, :, 0].max()) - err
                self.temp[0] = max(self.temp[1], self.temp[2], self.temp[3])

            except(ValueError):
                pass

        image_data = cv2.resize(image_data,(int(320*self.vsc),int(240*self.vsc)),interpolation=cv2.INTER_AREA)
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
    ##
    ctx = POINTER(uvc_context)()
    dev = POINTER(uvc_device)()
    devh = POINTER(uvc_device_handle)()
    ctrl = uvc_stream_ctrl()

    res = libuvc.uvc_init(byref(ctx), 0)
    if res < 0:
        print("uvc_init error")
        exit(1)

    try:
        res = libuvc.uvc_find_device(ctx, byref(dev), PT_USB_VID, PT_USB_PID, 0)
        if res < 0:
            print("uvc_find_device error")
            exit(1)

        try:
            res = libuvc.uvc_open(dev, byref(devh))
            if res < 0:
                print("uvc_open error")
                exit(1)

            print("device opened!")

            print_device_info(devh)
            print_device_formats(devh)

            frame_formats = uvc_get_frame_formats_by_guid(devh, VS_FMT_GUID_Y16)
            if len(frame_formats) == 0:
                print("device does not support Y16")
                exit(1)

            libuvc.uvc_get_stream_ctrl_format_size(devh, byref(ctrl), UVC_FRAME_FORMAT_Y16,
                frame_formats[0].wWidth, frame_formats[0].wHeight, int(1e7 / frame_formats[0].dwDefaultFrameInterval)
            )

            res = libuvc.uvc_start_streaming(devh, byref(ctrl), PTR_PY_FRAME_CALLBACK, None, 0)
            if res < 0:
                print("uvc_start_streaming failed: {0}".format(res))
                exit(1)

            try:
                ##
                app = QtWidgets.QApplication(sys.argv)

                main_window = QtWidgets.QMainWindow()
                main_widget = MainWidget(haar_cascade_filepath)
                main_window.setCentralWidget(main_widget)
                main_window.show()
                sys.exit(app.exec_())
                ##
            finally:
                libuvc.uvc_stop_streaming(devh)

            print("done")
        finally:
            libuvc.uvc_unref_device(dev)
    finally:
        ibuvc.uvc_exit(ctx)


if __name__ == '__main__':
    script_dir = path.dirname(path.realpath(__file__))
    cascade_filepath = path.join(script_dir,'haarcascade_frontalface_default.xml')

    cascade_filepath = path.abspath(cascade_filepath)
    main(cascade_filepath)