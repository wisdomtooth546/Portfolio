import tensorflow as tf
import cv2, json
import numpy as np

#'./WebApp/essentials/haarcascade_frontalface_alt2.xml'
model = tf.keras.models.load_model("./essentials/ResNet-50.h5")
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
            output = model.predict(input, steps=1)
            print(output)
            logit = tf.nn.softmax(output,axis=1)
            preds = np.argmax(logit ,1)
            
            item = dict()
            item['name'] = 'Output'
            item['class_name'] = emotion_dict[preds.item()]
            item['score'] = np.max(logit ,1)
            for x,y,w,h in faces:
             item['x'] = x/scale_factor
             item['y'] = y/scale_factor
             item['w'] = w/frame.shape[1]
             item['h'] = h/frame.shape[1] 
            outputJSON = json.dumps(item, default=default)
            return outputJSON
            


