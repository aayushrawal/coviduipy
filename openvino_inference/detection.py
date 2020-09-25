import os
import sys
import logging as log
import numpy as np
import cv2
from openvino.inference_engine import IENetwork, IECore

class ModelDetection:
    '''
    Class for the Face Detection Model.
    '''
    def __init__(self, model_name, device='CPU', extensions=None, threshold=0.5):
        self.threshold = threshold
        self.model_name = model_name
        self.device = device
        self.extensions = extensions

    def load_model(self):
        ## Get model_bin and model_xml
        model_bin = self.model_name + ".bin"
        model_xml = self.model_name + ".xml"
        plugin = IECore()
        network = IENetwork(model=model_xml, weights=model_bin)
        ## Add extension if any
        if self.extensions and "CPU" in self.device:                # Add a CPU extension, if applicable
            plugin.add_extension(self.extensions, self.device)
        ## (Additional) Check unsupported layer 
        supported_layers = plugin.query_network(network=network, device_name=self.device)
        unsupported_layers = [l for l in network.layers.keys() if l not in supported_layers]
        if len(unsupported_layers) > 2:
            print("Unsupported layers found: {}".format(unsupported_layers))
            print("Check whether extensions are available to add to IECore.")
            exit(1)
        ## Load network
        self.exec_network = plugin.load_network(network, self.device)                                        
        self.input_blob = next(iter(network.inputs))
        self.output_blob = next(iter(network.outputs))
        self.n, self.c, self.h, self.w = network.inputs[self.input_blob].shape
        self.plugin = plugin
        self.network = network
        
        
    def predict(self, image):
        frame_shape = image.shape
        image = self.preprocess_input(image)
        self.exec_network.requests[0].infer({self.input_blob: image})
        outputs = self.exec_network.requests[0].outputs[self.output_blob]
        self.outputs = outputs
        boxes, scores = self.preprocess_output(outputs, frame_shape)
        return boxes, scores

    def check_model(self):
        raise NotImplementedError

    def preprocess_input(self, image):
        img = cv2.dnn.blobFromImage(image, size=(self.w, self.h))
        return img

    def preprocess_output(self, outputs, frame_shape):
        img_h, img_w, _ = frame_shape
        boxes = []
        scores = []
        res = outputs
        people = res[0][:, np.where((res[0][0][:, 2] > self.threshold))]
        for person in people[0][0]:
            box = person[3:7] * np.array([img_w, img_h, img_w, img_h])
            box = int(box[0]), int(box[1]), int(box[2]), int(box[3])
            boxes.append(box)
            scores.append(person[2])
        return boxes, scores

