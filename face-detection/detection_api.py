# main.py# import the necessary packages
import time
from threading import Thread

import cv2
import requests
from flask import Flask, render_template, Response

import Constants
from detections import FaceUtils
from images import ImageUtils
from mcv import Model

app = Flask(__name__)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, Constants.SCREEN_HEIGHT)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, Constants.SCREEN_WIDTH)
model = Model()


@app.route('/')
def index_page():
    # rendering webpage
    return render_template('index.html')

@app.route('/history')
def history_page():
    result_set = FaceUtils.load_from_db()
    html = FaceUtils.to_html_view(result_set)
    return render_template('history.html', data=f'{html}')


def model_calculation_loop():
    while True:
        start_time = time.time()
        success, frame = cap.read()
        if not success:
            break
        else:
            frame_mirrored = ImageUtils.mirror(frame, 1)
            face = model.last_valid_face
            found, _ = model.calculate(frame_mirrored)
            frame = model.draw_current_view()

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
        ret, buffer = cv2.imencode('.jpg', frame)
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
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/play_sound')
def play_sound():
    Thread(target=_play_sound).start()
    return Response(status=200)

def _play_sound():
    from playsound import playsound
    from playsound import PlaysoundException
    try_harder = True
    while try_harder:
        try:
            playsound('blaster.wav')
            try_harder = False
        except PlaysoundException:
            pass


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
