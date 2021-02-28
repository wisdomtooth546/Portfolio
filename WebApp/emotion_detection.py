import tensorflow as tf
import cv2, json
import numpy as np

model = tf.keras.models.load_model("G:\Portfolio\Website-Portfolio\Classic-Theme\WebApp\essentials\ResNet-50.h5")
camera = cv2.VideoCapture(0)
cascade_file = 'G:\Portfolio\Website-Portfolio\Classic-Theme\WebApp\essentials\haarcascade_frontalface_alt2.xml'
face_Detection = cv2.CascadeClassifier(cascade_file)
emotion_dict = {0:'Angry', 1:'Disgust', 2:'Fear', 3:'Happy', 4:'Sad', 5:'Surprise', 6:'Neutral'}

def default(obj):
    if type(obj).__module__ == np.__name__:
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return obj.item()
    raise TypeError('Unknown type:', type(obj))

def get_objects(frame):
    
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
            preds = np.argmax(logit ,1)
            
            item = dict()
            item['name'] = 'Output'
            item['class_name'] = emotion_dict[preds.item()]
            item['score'] = np.max(logit ,1)
            for x,y,w,h in faces:
             item['x'] = x
             item['y'] = y
             item['w'] = w
             item['h'] = h
            
            outputJSON = json.dumps(item, default=default)
            return outputJSON
            """
                cv2.rectangle(frame, (x, y), (x + w, y + h),(0,255,0), 2)
         
                cv2.putText(frame,  f'{emotion_dict[preds.item()]}',(x, y), 
                  cv2.FONT_HERSHEY_SIMPLEX , 
                  fontScale=1, 
                  color = (255, 255, 0) , 
                  thickness= 3)
            """


