#!/usr/bin/env python

import logging as log
import os.path as osp
import os
import sys
import time
from argparse import ArgumentParser

import cv2
import numpy as np

from openvino.inference_engine import IENetwork
from ie_module import InferenceContext
from landmarks_detector import LandmarksDetector
from face_detector import FaceDetector
from faces_database import FacesDatabase
from face_identifier import FaceIdentifier

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

DEVICE_KINDS = ['CPU', 'GPU', 'FPGA', 'MYRIAD', 'HETERO', 'HDDL']
MATCH_ALGO = ['HUNGARIAN', 'MIN_DIST']

class FrameProcessor:
    QUEUE_SIZE = 16

    def __init__(self, varsd):
        used_devices = set([varsd["d_fd"], varsd["d_lm"], varsd["d_reid"]])
        self.context = InferenceContext(used_devices, varsd["cpu_lib"], varsd["gpu_lib"], varsd["perf_stats"])
        context = self.context

        log.info("Loading models")
        face_detector_net = self.load_model(varsd["m_fd"])
        
        assert (varsd["fd_input_height"] and varsd["fd_input_width"]) or \
               (varsd["fd_input_height"]==0 and varsd["fd_input_width"]==0), \
            "Both -fd_iw and -fd_ih parameters should be specified for reshape"
        
        if varsd["fd_input_height"] and varsd["fd_input_width"] :
            face_detector_net.reshape({"data": [1, 3, varsd["fd_input_height"],varsd["fd_input_width"]]})
        landmarks_net = self.load_model(varsd["m_lm"])
        face_reid_net = self.load_model(varsd["m_reid"])

        self.face_detector = FaceDetector(face_detector_net,
                                          confidence_threshold=varsd["t_fd"],
                                          roi_scale_factor=varsd["exp_r_fd"])

        self.landmarks_detector = LandmarksDetector(landmarks_net)
        self.face_identifier = FaceIdentifier(face_reid_net,
                                              match_threshold=varsd["t_id"],
                                              match_algo = varsd["match_algo"])

        self.face_detector.deploy(varsd["d_fd"], context)
        self.landmarks_detector.deploy(varsd["d_lm"], context,
                                       queue_size=self.QUEUE_SIZE)
        self.face_identifier.deploy(varsd["d_reid"], context,
                                    queue_size=self.QUEUE_SIZE)
        log.info("Models are loaded")

        log.info("Building faces database using images from '%s'" % (varsd["fg"]))
        self.faces_database = FacesDatabase(varsd["fg"], self.face_identifier,
                                            self.landmarks_detector,
                                            self.face_detector if varsd["run_detector"] else None, varsd["no_show"])
        self.face_identifier.set_faces_database(self.faces_database)
        log.info("Database is built, registered %s identities" % \
            (len(self.faces_database)))

        self.allow_grow = varsd["allow_grow"] and not varsd["no_show"]

    def load_model(self, model_path):
        model_path = osp.abspath(model_path)
        model_description_path = model_path
        model_weights_path = osp.splitext(model_path)[0] + ".bin"
        log.info("Loading the model from '%s'" % (model_description_path))
        assert osp.isfile(model_description_path), \
            "Model description is not found at '%s'" % (model_description_path)
        assert osp.isfile(model_weights_path), \
            "Model weights are not found at '%s'" % (model_weights_path)
        model = IENetwork(model_description_path, model_weights_path)
        log.info("Model is loaded")
        return model

    def process(self, frame):
        assert len(frame.shape) == 3, \
            "Expected input frame in (H, W, C) format"
        assert frame.shape[2] in [3, 4], \
            "Expected BGR or BGRA input"

        self.orig_image = frame.copy()
        frame = frame.transpose((2, 0, 1)) # HWC to CHW
        frame = np.expand_dims(frame, axis=0)

        self.face_detector.clear()
        self.landmarks_detector.clear()
        self.face_identifier.clear()

        self.face_detector.start_async(frame)
        self.rois = self.face_detector.get_roi_proposals(frame)
        if self.QUEUE_SIZE < len(self.rois):
            log.warning("Too many faces for processing." \
                    " Will be processed only %s of %s." % \
                    (self.QUEUE_SIZE, len(rois)))
            self.rois = self.rois[:self.QUEUE_SIZE]
        self.landmarks_detector.start_async(frame, self.rois)
        landmarks = self.landmarks_detector.get_landmarks()

        self.face_identifier.start_async(frame, self.rois, landmarks)
        face_identities, unknowns = self.face_identifier.get_matches()
        if self.allow_grow and len(unknowns) > 0:
            for i in unknowns:
                # This check is preventing asking to save half-images in the boundary of images
                if self.rois[i].position[0] == 0.0 or self.rois[i].position[1] == 0.0 or \
                    (self.rois[i].position[0] + self.rois[i].size[0] > self.orig_image.shape[1]) or \
                    (self.rois[i].position[1] + self.rois[i].size[1] > self.orig_image.shape[0]):
                    continue
                crop = self.orig_image[int(self.rois[i].position[1]):int(self.rois[i].position[1]+self.rois[i].size[1]), int(self.rois[i].position[0]):int(self.rois[i].position[0]+self.rois[i].size[0])]
                name = self.faces_database.ask_to_save(crop)
                if name:
                    id = self.faces_database.dump_faces(crop, face_identities[i].descriptor, name)
                    face_identities[i].id = id

        outputs = [self.rois, landmarks, face_identities]

        return outputs


    def get_performance_stats(self):
        stats = {
            'face_detector': self.face_detector.get_performance_stats(),
            'landmarks': self.landmarks_detector.get_performance_stats(),
            'face_identifier': self.face_identifier.get_performance_stats(),
        }
        return stats


class Visualizer(QtWidgets.QWidget):
    BREAK_KEY_LABELS = "q(Q) or Escape"
    BREAK_KEYS = {ord('q'), ord('Q'), 27}
    image_data = QtCore.pyqtSignal(np.ndarray)


    def __init__(self, parent=None, scale = 1.3, feed = 'video.mp4'):
        super().__init__(parent)
        self.varsd = {'input': '/dev/video3', 'match_algo': 'HUNGARIAN', 'd_lm': 'CPU', 'd_fd': 'CPU', 'perf_stats': False, 't_id': 0.3, 'cpu_lib': '', 'run_detector': False, 'fd_input_height': 0, 'timelapse': False, 'm_fd': 'models/face-detection-retail-0004.xml', 't_fd': 0.6, 'crop_height': 0, 'no_show': False, 'exp_r_fd': 1.15, 'fd_input_width': 0, 'allow_grow': False, 'm_lm': 'models/landmarks-regression-retail-0009.xml', 'gpu_lib': '', 'crop_width': 0, 'fg': 'Face_Gallery', 'verbose': True, 'm_reid': 'models/face-reidentification-retail-0095.xml', 'd_reid': 'CPU'}
        
        self.varsd["input"] = feed
        self.frame_processor = FrameProcessor(self.varsd)
        self.display = not self.varsd["no_show"]
        self.print_perf_stats = self.varsd["perf_stats"]

        self.frame_time = 0
        self.frame_start_time = 0
        self.fps = 0
        self.frame_num = 0
        self.frame_count = -1

        self.timer = QtCore.QBasicTimer()

        self.input_crop = None
        if self.varsd["crop_width"] and self.varsd["crop_height"]:
            self.input_crop = np.array((self.varsd["crop_width"], self.varsd["crop_height"]))

        self.frame_timeout = 0 if self.varsd["timelapse"] else 1
        self.vsc = scale
        self.input_stream = cv2.VideoCapture(self.varsd["input"])

        self.modeFR = 0
        self.FRTrainflag = 0

    def update_fps(self):
        now = time.time()
        self.frame_time = now - self.frame_start_time
        self.fps = 1.0 / self.frame_time
        self.frame_start_time = now

    def draw_text_with_background(self, frame, text, origin,
                                  font=cv2.FONT_HERSHEY_SIMPLEX, scale=1.0,
                                  color=(0, 0, 0), thickness=1, bgcolor=(255, 255, 255)):
        text_size, baseline = cv2.getTextSize(text, font, scale, thickness)
        cv2.rectangle(frame,
                      tuple((origin + (0, baseline)).astype(int)),
                      tuple((origin + (text_size[0], -text_size[1])).astype(int)),
                      bgcolor, cv2.FILLED)
        cv2.putText(frame, text,
                    tuple(origin.astype(int)),
                    font, scale, color, thickness)
        return text_size, baseline

    def draw_detection_roi(self, frame, roi, identity):
        label = self.frame_processor \
            .face_identifier.get_identity_label(identity.id)

        # Draw face ROI border
        cv2.rectangle(frame,
                      tuple(roi.position), tuple(roi.position + roi.size),
                      (0, 220, 0), 2)

        # Draw identik, ty label
        text_scale = 0.5
        font = cv2.FONT_HERSHEY_SIMPLEX
        text_size = cv2.getTextSize("H1", font, text_scale, 1)
        line_height = np.array([0, text_size[0][1]])
        text = label
        #####print(text)
        if identity.id != FaceIdentifier.UNKNOWN_ID:
            text += ' %.2f%%' % (100.0 * (1 - identity.distance))
        self.draw_text_with_background(frame, text,
                                       roi.position - line_height * 0.5,
                                       font, scale=text_scale)

    def draw_detection_keypoints(self, frame, roi, landmarks):
        keypoints = [landmarks.left_eye,
                     landmarks.right_eye,
                     landmarks.nose_tip,
                     landmarks.left_lip_corner,
                     landmarks.right_lip_corner]

        for point in keypoints:
            center = roi.position + roi.size * point
            cv2.circle(frame, tuple(center.astype(int)), 2, (0, 255, 255), 2)

    def draw_detections(self, frame, detections):
        for roi, landmarks, identity in zip(*detections):
            self.draw_detection_roi(frame, roi, identity)
            self.draw_detection_keypoints(frame, roi, landmarks)

    def draw_status(self, frame, detections):
        origin = np.array([10, 10])
        color = (10, 160, 10)
        font = cv2.FONT_HERSHEY_SIMPLEX
        text_scale = 0.5
        text_size, _ = self.draw_text_with_background(frame,
                                                      "Frame time: %.3fs" % (self.frame_time),
                                                      origin, font, text_scale, color)
        self.draw_text_with_background(frame,
                                       "FPS: %.1f" % (self.fps),
                                       (origin + (0, text_size[1] * 1.5)), font, text_scale, color)

        log.debug('Frame: %s/%s, detections: %s, ' \
                  'frame time: %.3fs, fps: %.1f' % \
                     (self.frame_num, self.frame_count, len(detections[-1]), self.frame_time, self.fps))

        if self.print_perf_stats:
            log.info('Performance stats:')
            log.info(self.frame_processor.get_performance_stats())



    def should_stop_display(self):
        key = cv2.waitKey(self.frame_timeout) & 0xFF
        return key in self.BREAK_KEYS


    @staticmethod
    def center_crop(frame, crop_size):
        fh, fw, fc = frame.shape
        crop_size[0] = min(fw, crop_size[0])
        crop_size[1] = min(fh, crop_size[1])
        return frame[(fh - crop_size[1]) // 2 : (fh + crop_size[1]) // 2,
                     (fw - crop_size[0]) // 2 : (fw + crop_size[0]) // 2,
                     :]


    def imgdisplay(self,image_data):

        #cv2.cvtColor(image_data, cv2.COLOR_BGR2RGB, image_data)



        if self.input_crop is not None:
            image_data = Visualizer.center_crop(image_data, image_data)

        self.image_data_print = cv2.resize(image_data, (int(320*self.vsc), int(240*self.vsc)), interpolation=cv2.INTER_AREA)

        detections = self.frame_processor.process(self.image_data_print)


        self.draw_detections(self.image_data_print, detections)
        self.draw_status(self.image_data_print, detections)

        self.update_fps()
        self.frame_num += 1

        
        

        self.image = self.get_qimage(self.image_data_print)

        if self.image.size() != self.size():
            self.setFixedSize(self.image.size())

        self.update()



    def start_recording(self):

        self.timer.start(0, self)
    
    def timerEvent(self, event):
        
        if (event.timerId() != self.timer.timerId()):
            return
            
        """ fps = input_stream.get(cv2.CAP_PROP_FPS)
        frame_size = (int(input_stream.get(cv2.CAP_PROP_FRAME_WIDTH)),
                      int(input_stream.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        self.frame_count = int(input_stream.get(cv2.CAP_PROP_FRAME_COUNT))
        if self.varsd["crop_width"] and self.varsd["crop_height"]:
            crop_size = (self.varsd["crop_width"], self.varsd["crop_height"])
            frame_size = tuple(np.minimum(frame_size, crop_size))
        #log.info("Input stream info: %d x %d @ %.2f FPS" % \
        #    (frame_size[0], frame_size[1], fps))
        
        #self.process(input_stream)


        #while input_stream.isOpened(): """
        has_frame, frame = self.input_stream.read()
        
        if has_frame:
            self.image_data.emit(frame)

        

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
    
    def paintEvent(self, QPaintEvent):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.drawImage(0, 0, self.image)
        self.image = QtGui.QImage()  

    def CheckTrainTrigger(self):
        face_identities, unknowns = self.frame_processor.face_identifier.get_matches()
        rois = self.frame_processor.rois
        if len(unknowns) > 0:
            for i in unknowns:
                # This check is preventing asking to save half-images in the boundary of images
                if rois[i].position[0] == 0.0 or rois[i].position[1] == 0.0 or \
                    (rois[i].position[0] + rois[i].size[0] > self.frame_processor.orig_image.shape[1]) or \
                    (rois[i].position[1] + rois[i].size[1] > self.frame_processor.orig_image.shape[0]):
                    continue
                crop = self.frame_processor.orig_image[int(rois[i].position[1]):int(rois[i].position[1]+rois[i].size[1]), int(rois[i].position[0]):int(rois[i].position[0]+rois[i].size[0])]
                #name = self.frame_processor.faces_database.ask_to_save(crop)
                dirs = os.listdir("Face_Gallery")
                max_label = 0
                for dir_names in dirs:
                    max_label=max(int(dir_names.split("-")[0]), max_label)
                name = str(max_label+1)
                if name:
                    id = self.frame_processor.faces_database.dump_faces(crop, face_identities[i].descriptor, name)
                    face_identities[i].id = id    

class MainWidget(QtWidgets.QWidget):
    def __init__(self,scale = 1.3, parent=None):
        super().__init__(parent)
        self.face_detection_widget =  Visualizer()
        self.face_detection_widget.vsc = scale
        self.image_data_slot=self.face_detection_widget.imgdisplay
        self.startrec=self.face_detection_widget.start_recording()
        self.face_detection_widget.image_data.connect(self.image_data_slot)
        self.layout=QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.face_detection_widget)
        self.setLayout(self.layout)
        


    

def main():

    app = QtWidgets.QApplication(sys.argv)

    main_window = QtWidgets.QMainWindow()
    main_widget = MainWidget()
    main_window.setCentralWidget(main_widget)
    main_window.resize(320,240)
    main_window.show()
    sys.exit(app.exec_())
    sys.exit()


if __name__=="__main__":
    main()