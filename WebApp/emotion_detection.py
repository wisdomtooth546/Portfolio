import tensorflow as tf
import cv2, os, json

model = tf.keras.models.load_model("./WebApp/essentials/ResNet-50.h5")
camera = cv2.VideoCapture(0)
cascade_file = './WebApp/essentials/haarcascade_frontalface_alt2.xml'
face_Detection = cv2.CascadeClassifier(cascade_file)
emotion_dict = {0:'Angry', 1:'Disgust', 2:'Fear', 3:'Happy', 4:'Sad', 5:'Surprise', 6:'Neutral'}
class Object(object):
    def __init__(self):
        self.name = "Tensorflow Object API"
    
    def toJSON(self):
        return json.dumps(self.__dict__)

def get_objects():
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            faces = face_Detection.detectMultiScale(frame,
                                         scaleFactor=1.1,
                                         minNeighbors=5,
                                         minSize=(60, 60),
                                         flags=cv2.CASCADE_SCALE_IMAGE)
            img = tf.image.resize(frame,(197, 197)) 
            input = tf.expand_dims(img,0)
            input-= 128.8006
            input /= 64.6497
            output = model.predict(input)
            logit = tf.nn.softmax(output,axis=1)
            preds = tf.math.argmax(logit ,1)
            item = object()
            item.name = 'Output'
            item.class_name = emotion_dict[preds.item()]
            item.score = tf.math.max(logit ,1)
            item.x = faces[0]
            item.y = faces[1]
            item.w = faces[2]
            item.h = faces[3]
            outputJSON = json.dumps(item.__dict__)
            return outputJSON
               """
                cv2.rectangle(frame, (x, y), (x + w, y + h),(0,255,0), 2)
         
                cv2.putText(frame,  f'{emotion_dict[preds.item()]}',(x, y), 
                  cv2.FONT_HERSHEY_SIMPLEX , 
                  fontScale=1, 
                  color = (255, 255, 0) , 
                  thickness= 3)
               """


