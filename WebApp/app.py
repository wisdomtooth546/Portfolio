
from flask import Flask,Response, render_template
import emotion_detection
import cv2, time
from PIL import Image

app = Flask(__name__, static_url_path='', static_folder='static')




@app.route('/')
def home():
    return render_template('index.html')

@app.route('/FER')
def FER():
    return render_template('fer.html')

@app.route('/image', methods=['POST'])
def image():
    try:
        image_file = request.files['image']  # get the image
  
        # finally run the image through tensor flow object detection`
        image_object = Image.open(image_file)
        objects = object_detection_api.get_objects(image_object)
        return objects
 
    except Exception as e:
        print('POST /image error: %e' % e)
        return e
  

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST') # Put any other methods you need here
    return response

if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug=True)