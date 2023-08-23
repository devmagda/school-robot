# This is a sample Python script.
import time
from typing import Any

import cv2

import Constants
from State import State

global active
global cap
global state
global image


blue = [255, 0, 0]

def initCaptureDevice() -> cv2.VideoCapture:
    # To capture video from webcam.
    global cap
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, Constants.SCREEN_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, Constants.SCREEN_HEIGHT)

    _, image = cap.read()
    cv2.imshow('Web Capture', image)
    return cap


def captureLoop():
    global image, cap, state
    _, image = cap.read()
    state.update(image)
    state.visualize(image)


def viewLoop():
    global image
    global active
    cv2.imshow('Web Capture', image)
    # print("--------------------------------")


def controllerLoop():
    global active
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        active = False


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    cap = initCaptureDevice()
    state = State()
    _, image = cap.read()
    active = True

    while active:
        captureLoop()
        controllerLoop()
        viewLoop()
        # time.sleep(5)

    # Release the VideoCapture object
    cap.release()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
