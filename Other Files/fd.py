import cv2
import numpy as np
from openvino_inference.detection import ModelDetection


if __name__ == '__main__':

    #video_src = "/home/sensor/Desktop/coviduipy/video.mp4"
    video_src = '/dev/video0'
    color_fd = (0, 150, 250)
    pd_path = 'models/face-detection-retail-0004'
    device = "CPU"
    cpu_extension = None
    view_detection = True

    th_detection = 0.7
    detection = ModelDetection(model_name=pd_path, device=device, extensions=cpu_extension, threshold = th_detection)
    detection.load_model()    
    cap = cv2.VideoCapture(video_src)
    while cap.isOpened():
        ret, frame = cap.read()        
        boxes = []
        boxes, scores = detection.predict(frame)
        if view_detection:
            for i in range(len(boxes)):
                box = boxes[i]
                cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])),(255,255,0), 2)
        
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
