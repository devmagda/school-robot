from asyncio import sleep

import cv2
from fastapi import FastAPI

import requests
from pydantic import BaseModel

import Constants
from Human import FacesUtil
from ImageUtils import ImageUtils

mode = 1

app = FastAPI()

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

class FaceComparisonData(BaseModel):
    last_seen: str
    whole: str


@app.post('/faces/')
async def a(data: FaceComparisonData):
    print('Added faces')
    image = ImageUtils.fromByteString(data.whole)
    last_seen = ImageUtils.fromByteString(data.last_seen)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces, found = \
        FacesUtil.get_valid_faces(gray, eye_cascade, face_cascade, scale=Constants.FACE_DETECTION_SCALE)

    for i, face in enumerate(faces):
        x, y, w, h = face.to_x_y_width_height()
        img2 = ImageUtils.getSubImage(image, x, y, w, h, margin=Constants.FACE_COMPARISON_MARGIN)
        img2 = ImageUtils.scaleImage(img2, scale=Constants.FACE_COMPARISON_SCALE)
        verified, distance, threshold = await FacesUtil.compare(last_seen, img2)
        try:
            d = await FacesUtil.analyze(img2)
            print(d)
        except:
            pass
        print(verified, distance, threshold, end='')
    pass


@app.get('/b')
def b():
    print('b')


@app.get("/o/api/gpio/{pin}")
def root(pin: str):
    print("Getting pin " + pin)

    return {"message": "Hello World"}


@app.get("/hello/{name}")
def say_hello(name: str):
    print("Hello " + name)
    return {"message": f"Hello {name}"}


class Client:

    @staticmethod
    def post_faces(last_seen, whole):
        data = {
            'last_seen': last_seen,
            'whole': whole
        }
        Client.post('faces', data)


    @staticmethod
    def post(endpoint, json):
        endpoint = Constants.API_URL + endpoint
        requests.post(endpoint, json)
