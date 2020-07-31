import sys
from os import path
import os
import cv2
import numpy as np

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from statistics import mode


class TrainFR(QtCore.QThread):
    Status = QtCore.pyqtSignal(int)

    def detect_face(self,img):
        # convert the test image to gray image as opencv face detector expects gray images
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # load OpenCV face detector, I am using LBP which is fast
        # there is also a more accurate but slow Haar classifier
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        # let's detect multiscale (some images may be closer to camera than others) images
        # result is a list of faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5);

        # if no faces are detected then return original img
        if (len(faces) == 0):
            return None, None

        # under the assumption that there will be only one face,
        # extract the face area
        (x, y, w, h) = faces[0]

        # return only the face part of the image
        return gray[y:y + w, x:x + h], faces[0]

    # I am using OpenCV's **LBP face detector**. On _line 4_, I convert the image to grayscale because most operations in OpenCV are performed in gray scale, then on _line 8_ I load LBP face detector using `cv2.CascadeClassifier` class. After that on _line 12_ I use `cv2.CascadeClassifier` class' `detectMultiScale` method to detect all the faces in the image. on _line 20_, from detected faces I only pick the first face because in one image there will be only one face (under the assumption that there will be only one prominent face). As faces returned by `detectMultiScale` method are actually rectangles (x, y, width, height) and not actual faces images so we have to extract face image area from the main image. So on _line 23_ I extract face area from gray image and return both the face image area and face rectangle.
    #
    # Now you have got a face detector and you know the 4 steps to prepare the data, so are you ready to code the prepare data step? Yes? So let's do it.

    # In[4]:

    # this function will read all persons' training images, detect face from each image
    # and will return two lists of exactly same size, one list
    # of faces and another list of labels for each face
    def prepare_training_data(self, data_folder_path):

        # ------STEP-1--------
        # get the directories (one directory for each subject) in data folder
        dirs = os.listdir(data_folder_path)

        # list to hold all subject faces
        faces = []
        # list to hold labels for all subjects
        labels = []

        # let's go through each directory and read images within it
        for dir_name in dirs:

            # our subject directories start with letter 's' so
            # ignore any non-relevant directories if any
            if not dir_name.startswith("s"):
                continue;

            # ------STEP-2--------
            # extract label number of subject from dir_name
            # format of dir name = slabel
            # , so removing letter 's' from dir_name will give us label
            label = int(dir_name.replace("s", ""))

            # build path of directory containin images for current subject subject
            # sample subject_dir_path = "training-data/s1"
            subject_dir_path = data_folder_path + "/" + dir_name

            # get the images names that are inside the given subject directory
            subject_images_names = os.listdir(subject_dir_path)

            # ------STEP-3--------
            # go through each image name, read image,
            # detect face and add face to list of faces
            for image_name in subject_images_names:

                # ignore system files like .DS_Store
                if image_name.startswith("."):
                    continue;

                # build image path
                # sample image path = training-data/s1/1.pgm
                image_path = subject_dir_path + "/" + image_name

                # read image
                image = cv2.imread(image_path)

                # display an image window to show the image
                #cv2.imshow("Training on image...", cv2.resize(image, (400, 500)))
                #cv2.waitKey(100)

                # detect face
                face, rect = self.detect_face(image)

                # ------STEP-4--------
                # for the purpose of this tutorial
                # we will ignore faces that are not detected
                if face is not None:
                    # add face to list of faces
                    faces.append(face)
                    # add label for this face
                    labels.append(label)
                else:
                    print("ignoring Image ", image_path)

        #cv2.destroyAllWindows()
        cv2.waitKey(1)
        cv2.destroyAllWindows()

        return faces, labels

    # I have defined a function that takes the path, where training subjects' folders are stored, as parameter. This function follows the same 4 prepare data substeps mentioned above.
    #
    # **(step-1)** On _line 8_ I am using `os.listdir` method to read names of all folders stored on path passed to function as parameter. On _line 10-13_ I am defining labels and faces vectors.
    #
    # **(step-2)** After that I traverse through all subjects' folder names and from each subject's folder name on _line 27_ I am extracting the label information. As folder names follow the `sLabel` naming convention so removing the  letter `s` from folder name will give us the label assigned to that subject.
    #
    # **(step-3)** On _line 34_, I read all the images names of of the current subject being traversed and on _line 39-66_ I traverse those images one by one. On _line 53-54_ I am using OpenCV's `imshow(window_title, image)` along with OpenCV's `waitKey(interval)` method to display the current image being traveresed. The `waitKey(interval)` method pauses the code flow for the given interval (milliseconds), I am using it with 100ms interval so that we can view the image window for 100ms. On _line 57_, I detect face from the current image being traversed.
    #
    # **(step-4)** On _line 62-66_, I add the detected face and label to their respective vectors.

    # But a function can't do anything unless we call it on some data that it has to prepare, right? Don't worry, I have got data of two beautiful and famous celebrities. I am sure you will recognize them!
    #
    # ![training-data](visualization/tom-shahrukh.png)
    #
    # Let's call this function on images of these beautiful celebrities to prepare data for training of our Face Recognizer. Below is a simple code to do that.

    # In[5]:

    # let's first prepare our training data
    # data will be in two lists of same size
    # one list will contain all the faces
    # and other list will contain respective labels for each face
    def run(self):
        self.Status.emit(0)
        print("Preparing data...")
        faces, labels = self.prepare_training_data("ModelTrainer\\training-data")
        print("Data prepared")

        # print total faces and labels
        print("Total faces: ", len(faces))
        print("Total labels: ", len(labels))

        # This was probably the boring part, right? Don't worry, the fun stuff is coming up next. It's time to train our own face recognizer so that once trained it can recognize new faces of the persons it was trained on. Read? Ok then let's train our face recognizer.

        # ### Train Face Recognizer

        # As we know, OpenCV comes equipped with three face recognizers.
        #
        # 1. EigenFace Recognizer: This can be created with `cv2.face.createEigenFaceRecognizer()`
        # 2. FisherFace Recognizer: This can be created with `cv2.face.createFisherFaceRecognizer()`
        # 3. Local Binary Patterns Histogram (LBPH): This can be created with `cv2.face.LBPHFisherFaceRecognizer()`
        #
        # I am going to use LBPH face recognizer but you can use any face recognizer of your choice. No matter which of the OpenCV's face recognizer you use the code will remain the same. You just have to change one line, the face recognizer initialization line given below.

        # In[6]:

        # create our LBPH face recognizer
        face_recognizer = cv2.face.LBPHFaceRecognizer_create()

        # or use EigenFaceRecognizer by replacing above line with
        # face_recognizer = cv2.face.EigenFaceRecognizer_create()

        # or use FisherFaceRecognizer by replacing above line with
        # face_recognizer = cv2.face.FisherFaceRecognizer_create()

        # Now that we have initialized our face recognizer and we also have prepared our training data, it's time to train the face recognizer. We will do that by calling the `train(faces-vector, labels-vector)` method of face recognizer.

        # In[7]:

        # train our face recognizer of our training faces
        face_recognizer.train(faces, np.array(labels))
        face_recognizer.write("trained_model.yml")
        self.Status.emit(1)
        #self.quit()


class RecordVideo(QtCore.QObject):
    image_data = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, camera_port=0, parent=None):
        super().__init__(parent)
        self.camera_port = camera_port
        self.camera = cv2.VideoCapture(camera_port)
        self.timer = QtCore.QBasicTimer()
        self.counter = 0
        self.lastframe = None

    def start_recording(self):

        self.timer.start(0, self)

    def timerEvent(self, event):
        try:
            if (event.timerId() != self.timer.timerId()):
                return
            read, data = self.camera.read()
            total_frames = self.camera.get(cv2.CAP_PROP_FRAME_COUNT)
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
                self.lastframe = data
            self.camera.release()
        finally:self.camera.release()
        #if cv2.waitKey(2):
        #    self.image_data.emit(self.lastframe)
        #    return
        #if(self.counter>1):
        #    self.camera.set(cv2.CAP_PROP_POS_FRAMES, total_frames)
        #    self.counter = 0
        #else:
        #    self.counter = self.counter + 1


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
        self.meanFR = [0]
        self.modeFR = 0
        self.FRTrainflag = 0
        self.last10frames = []
        self.face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        print("Loading Dataset")
        self.face_recognizer.read("trained_model.yml")
        print("Loaded Dataset")
        pass


    def refreshFRdataset(self,Stt):
        if Stt:
            self.face_recognizer = cv2.face.LBPHFaceRecognizer_create()
            print("Loading Dataset")
            self.face_recognizer.read("trained_model.yml")
            print("Loaded Dataset")
            self.FRTrainflag = 0


    def StartTraining(self):
        self.FRTrainflag = 1
        self.training = TrainFR()
        self.training.Status.connect(self.refreshFRdataset)
        self.training.start()

    def CheckTrainTrigger(self):
        if self.modeFR == 0 and self.FRTrainflag == 0:
            self.saveFRData()
            self.StartTraining()

    def detect_faces(self, image: np.ndarray):
        # haarclassifiers work better in black and white
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # load OpenCV face detector, I am using LBP which is fast
        # there is also a more accurate but slow Haar classifier
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        # let's detect multiscale (some images may be closer to camera than others) images
        # result is a list of faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5);

        # if no faces are detected then return original img
        if (len(faces) == 0):
            return None, None

        # under the assumption that there will be only one face,
        # extract the face area
        (x, y, w, h) = faces[0]

        # return only the face part of the image
        return gray[y:y + w, x:x + h], faces[0]

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

    def draw_text(self, img, text, x, y):
        cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

    def draw_rectangle(self, img, rect):
        (x, y, w, h) = rect
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)


    def resMeanFRSession(self):
        self.meanFR = [0]
        self.modeFR = 0
        self.last10frames = []

    def returnmeanFRSession(self):
        self.modeFR = mode(self.meanFR)
        return self.modeFR

    def recmodeFRsession(self,val):
        if val != 0:
            self.meanFR.append(val)

    def saveFRData(self):
        dirs = os.listdir("ModelTrainer\\training-data")
        max_label = 0
        for dir_name in dirs:
            if not dir_name.startswith("s"):
                continue;
            label = int(dir_name.replace("s", ""))
            max_label = max(label, max_label)
        os.mkdir("ModelTrainer\\training-data\\s" + str(max_label + 1))
        for x in range(len(self.last10frames)):
            cv2.imwrite("ModelTrainer\\training-data\\s"+str(max_label+1)+"\\"+str(x)+".jpg", self.last10frames[x])
        print("Data Saved")

    def image_data_slot(self, image_data):
        face, rect = self.detect_faces(image_data)

        if face is not None:
            if(len(self.last10frames)>=10):
                self.last10frames = []
            self.last10frames.append(face)
            (x, y, w, h) = rect
            cv2.rectangle(image_data, # Face
                          (x, y),
                          (x+w, y+h),
                          self._red,
                          self._width)
            try:
                label, confidence = self.face_recognizer.predict(face)
                # get name of respective label returned by face recognizer
                self.recmodeFRsession(label)
                self.returnmeanFRSession()
                if self.modeFR != 0:
                    label_text = str(self.modeFR)
                elif label == 0:
                    label_text = "None"
                else:
                    label_text = str(label)
                # draw a rectangle around face detected
                self.draw_rectangle(image_data, rect)
                # draw name of predicted person
                self.draw_text(image_data, label_text, rect[0], rect[1] - 5)

                #print(confidence)

            except:
                pass

        image_data = cv2.resize(image_data, (int(320*self.vsc), int(240*self.vsc)), interpolation=cv2.INTER_AREA)
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
    def __init__(self, haarcascade_filepath, parent=None, scale=1, feed=0):
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
    sys.exit()


if __name__ == '__main__':
    script_dir = path.dirname(path.realpath(__file__))
    cascade_filepath = path.join(script_dir,'haarcascade_frontalface_default.xml')

    cascade_filepath = path.abspath(cascade_filepath)
    main(cascade_filepath)