# main.py# import the necessary packages
import time

import cv2
import requests
from flask import Flask, render_template, Response

import Constants
from images import ImageUtils
from mcv import Model

app = Flask(__name__)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, Constants.SCREEN_HEIGHT)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, Constants.SCREEN_WIDTH)
model = Model()


@app.route('/')
def index():
    # rendering webpage
    return render_template('index.html')


def model_calculation_loop():
    while True:
        start_time = time.time()
        success, frame = cap.read()
        if not success:
            break
        else:
            found, _ = model.calculate(frame)
            frame = model.get_color_key_points_image()
            face = model.get_face_image()
            end_time = time.time()

            delta = end_time - start_time

            yield {'face': face, 'frame': frame, 'run_time': delta}


def gen_frames():
    while True:
        success, frame = cap.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def get_global_image():
    gen = model_calculation_loop()
    while True:
        result = next(gen)
        frame = result['frame']
        frame_mirrored = ImageUtils.mirror(frame, 1)
        ret, buffer = cv2.imencode('.jpg', frame_mirrored)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def get_face_image():
    gen = model_calculation_loop()
    while True:
        result = next(gen)
        frame = result['face']
        if frame is None:
            continue
        frame_mirrored = ImageUtils.mirror(frame, 1)
        ret, buffer = cv2.imencode('.jpg', frame_mirrored)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/play_sound')
def play_sound():
    from playsound import playsound
    from playsound import PlaysoundException
    try_harder = True
    while try_harder:
        try:
            playsound('blaster.wav')
            try_harder = False
        except PlaysoundException:
            pass
    return Response(status=200)


def get_response(function):
    return Response(function, mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/face_feed')
def face_feed():
    return Response(get_face_image(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/global_feed')
def global_feed():
    return Response(get_global_image(), mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == '__main__':
    # defining server ip address and port
    app.run(host='0.0.0.0', port='5000', debug=True)
