
from flask import Flask,Response, render_template

import cv2, time

app = Flask(__name__, static_url_path='', static_folder='static')

def gen_frames():  
    tick = time.time()
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
            preds = tf.math.argmax(tf.nn.softmax(output,axis=1),1)
            #conf = np.max(tf.nn.softmax(output,axis=1),1)
            for (x,y,w,h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h),(0,255,0), 2)
         
                cv2.putText(frame,  f'{emotion_dict[preds.item()]}',(x, y), 
                  cv2.FONT_HERSHEY_SIMPLEX , 
                  fontScale=1, 
                  color = (255, 255, 0) , 
                  thickness= 3)


            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            if time.time()-tick > 100:
              camera.release()
              break

            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/FER')
def FER():
    return render_template('fer.html')

@app.route('/video')
def video():
  return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(host = '0.0.0.0')