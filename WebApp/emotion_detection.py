import tensorflow as tf
import cv2, json, requests
import numpy as np

#'./WebApp/essentials/haarcascade_frontalface_alt2.xml'
model = 'http://localhost:9000/v1/models/EmotionClassifier:predict'
cascade_file = './essentials/haarcascade_frontalface_alt2.xml'
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
            frame = cv2.cvtColor(np.asarray(frame), cv2.COLOR_RGB2BGR)
            scale_factor = frame.shape[0]
            faces = face_Detection.detectMultiScale(frame,
                                         minNeighbors=5,
                                         minSize=(60, 60)
                                         )
            img = tf.image.resize(frame,(197, 197)) 
            input = tf.expand_dims(img,0)
            input-= 128.8006
            input /= 64.6497
            payload = {
                "instances": [{'input_1': input}]
            }
            output = requests.post(model, json=payload)
            preds = np.argmax(json.loads(output.content.decode('utf-8')))
            
            item = dict()
            item['name'] = 'Output'
            item['class_name'] = emotion_dict[preds.item()]
            for x,y,w,h in faces:
             item['x'] = x/scale_factor
             item['y'] = y/scale_factor
             item['w'] = w/frame.shape[1]
             item['h'] = h/frame.shape[1] 
            outputJSON = json.dumps(item, default=default)
            return outputJSON
            


