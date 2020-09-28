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

from openvino_inference.detection import ModelDetection

from copy import deepcopy

class RecordVideo(QtCore.QObject):
    image_data = QtCore.pyqtSignal(np.ndarray)
    BUF_SIZE = 2

    def __init__(self, parent=None):
        super().__init__(parent)
        self.stop = False
        self.timer = QtCore.QBasicTimer()
        self.q = Queue(self.BUF_SIZE)
        self.PTR_PY_FRAME_CALLBACK = CFUNCTYPE(None, POINTER(uvc_frame), c_void_p)(self.py_frame_callback)


    def py_frame_callback(self,frame, userptr):

        array_pointer = cast(frame.contents.data, POINTER(c_uint16 * (frame.contents.width * frame.contents.height)))
        data = np.frombuffer(array_pointer.contents, dtype=np.dtype(np.uint16)).reshape(frame.contents.height, frame.contents.width)

        if frame.contents.data_bytes != (2 * frame.contents.width * frame.contents.height):
            return

        if not self.q.full():
            self.q.put(data)

    def start_recording(self):
        self.timer.start(0, self)

    def timerEvent(self, event):
        if (event.timerId() != self.timer.timerId()):
            return
        
        ctx = POINTER(uvc_context)()
        dev = POINTER(uvc_device)()
        devh = POINTER(uvc_device_handle)()
        ctrl = uvc_stream_ctrl()

        res = libuvc.uvc_init(byref(ctx), 0)
        if res < 0:
            print("uvc_init error")
            exit(1)
        else:print("uvc_init worked")
        try:
            res = libuvc.uvc_find_device(ctx, byref(dev), PT_USB_VID, PT_USB_PID, 0)
            if res < 0:
                print("uvc_find_device error")
                exit(1)
            else:print("uvc_find_device worked")
            try:
                res = libuvc.uvc_open(dev, byref(devh))
                if res < 0:
                    print("uvc_open error")
                    exit(1)
                else:print("uvc_open worked")
                print("device opened!")

                print_device_info(devh)
                print_device_formats(devh)

                frame_formats = uvc_get_frame_formats_by_guid(devh, VS_FMT_GUID_Y16)
                if len(frame_formats) == 0:
                    print("device does not support Y16")
                    exit(1)
                else:print("uvc_get_frame_formats worked")

                libuvc.uvc_get_stream_ctrl_format_size(devh, byref(ctrl), UVC_FRAME_FORMAT_Y16,
                    frame_formats[0].wWidth, frame_formats[0].wHeight, int(1e7 / frame_formats[0].dwDefaultFrameInterval)
                )

                res = libuvc.uvc_start_streaming(devh, byref(ctrl), self.PTR_PY_FRAME_CALLBACK, None, 0)
                if res < 0:
                    print("uvc_start_streaming failed: {0}".format(res))
                    exit(1) 
                else:print("uvc_start_streaming worked")

                try:
                    while True:
                        data = self.q.get(True, 500)
                        read = data
                        if data is None:
                            break


                        data = cv2.resize(data[:,:], (640, 480))                       
                        #minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(data)
                       

                        if data.any():
                            self.image_data.emit(data)
   

                finally:
                    libuvc.uvc_stop_streaming(devh)

                print("done")

            finally:
                libuvc.uvc_unref_device(dev)
        finally:
            libuvc.uvc_exit(ctx)


class FaceDetectionWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, scale=1.3):
        super().__init__(parent)
        #self.classifier = cv2.CascadeClassifier(haar_cascade_filepath)
        self.image = QtGui.QImage()
        self._red = (0, 0, 255)
        self._green = (0, 255, 0)
        self._orange = (0, 20, 155)
        self._width = 2
        self._min_size = (30, 30)
        self.vsc = scale
        self.temp = 0


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
        
        #minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(image_data)

        image_data_copy = deepcopy(image_data)
        
        image_data = self.raw_to_8bit(image_data)

        """ faces = self.detect_faces(image_data)

        

        for (x, y, w, h) in faces:
            #self.temp = 
            
            cv2.rectangle(image_data, # Face
                (x, y),
                (x+w, y+h),
                self._red,
                self._width)  
            

            try:
                
                face_roi = image_data[x: int(x+w), y: int(y+h)]

                face_roi_clean = image_data_clean[x: int(x+w), y: int(y+h)]

                minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(image_data_clean)

                self.display_temperature(image_data, maxVal, maxLoc, (0, 0, 255))
                cv2.imshow("thermal", image_data)
                cv2.waitKey(1)

                self.temp[0]=round(self.ktof(maxVal),2)
                
                #print("{0:.1f} degF".format(self.ktof(maxVal)))

            except(ValueError):
                pass """

       
        ######

        #video_src = '/dev/video0'
        color_fd = (0, 150, 250)
        pd_path = 'models/face-detection-retail-0005'
        device = "CPU"
        cpu_extension = None

        th_detection = 0.65
        self.detection = ModelDetection(model_name=pd_path, device=device, extensions=cpu_extension, threshold = th_detection)
        self.detection.load_model()    
        #cap = cv2.VideoCapture(video_src)
        #while cap.isOpened():
            #ret, frame = cap.read()        
        self.boxes = []
        self.boxes, scores = self.detection.predict(image_data)

            

        for i in range(len(self.boxes)):
            box = self.boxes[i]
            cv2.rectangle(image_data, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])),(255,255,0), 2)
            try:
                face_roi = image_data_copy[int(box[0]+4):int(box[0]+box[2]-4),int(box[1]+4):int(box[1]+box[3]-4)]
                
                minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(face_roi)

                #minVal1, maxVal1, minLoc1, maxLoc1 = cv2.minMaxLoc(image_data_copy)

                maxLoc_frame = (int(box[0]+maxLoc[0]),int(box[1]+maxLoc[1]))
                
                if(maxVal>80):
                    #print(int(maxLoc[0]+box[0]),int(maxLoc[1]+box[1]))
                    #print(int(maxLoc1[0]),int(maxLoc1[1]))
                    if(maxLoc_frame[0] > box[0] and maxLoc_frame[0]<box[2] and maxLoc_frame[1] > box[1] and maxLoc_frame[1]<box[3]):
                        self.display_temperature(image_data, maxVal, maxLoc_frame, (0, 0, 255))
                        self.temp = round(self.ktof(maxVal),2)
                    #print(self.temp)
                else:pass
            except(ValueError):
                pass

        
        ######

        #self.display_temperature(image_data, maxVal, maxLoc, (0, 0, 255))


        cv2.imshow("thermal", image_data)

        cv2.waitKey(1)
        
        #self.temp = round(self.ktof(maxVal),2)

        

        image_data = cv2.resize(image_data,(int(320*self.vsc),int(240*self.vsc)),interpolation=cv2.INTER_AREA)

        
        self.image = self.get_qimage(image_data)
        

        if self.image.size() != self.size():
            self.setFixedSize(self.image.size())
        
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
        painter.drawImage(0, 0, self.image)
        self.image = QtGui.QImage()


class MainWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, scale=1.3):
        super().__init__(parent)
        #fp = haarcascade_filepath
        self.face_detection_widget = FaceDetectionWidget(scale=scale)
        self.face_detection_widget.vsc = scale        
        self.record_video = RecordVideo()
        self.image_data_slot = self.face_detection_widget.image_data_slot
        self.record_video.image_data.connect(self.image_data_slot)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.face_detection_widget)
        self.record_video.start_recording()
        self.setLayout(layout)

def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    main_widget = MainWidget()
    main_window.setCentralWidget(main_widget)
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    #script_dir = path.dirname(path.realpath(__file__))
    #cascade_filepath = path.join(script_dir,'haarcascade_frontalface_default.xml')

    #cascade_filepath = path.abspath(cascade_filepath)
    main()