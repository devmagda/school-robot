# This is a sample Python script.
from typing import Any

import cv2
import threading
import time
import numpy as np

from ImageDetectionUtil import ImageDetectionUtil
from State import State

global active
global cap
global state
global image


def initCaptureDevice() -> cv2.VideoCapture:
    # To capture video from webcam.
    global cap
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    return cap


def captureLoop():
    global image, cap, state
    print("captureLoop")
    _, image = cap.read()
    state.update(image)
    state.draw(image)


def viewLoop():
    global image
    global active
    print("viewLoop")
    cv2.imshow('Web Capture', image)


def controllerLoop():
    global active
    print("controllerLoop")
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

    # Release the VideoCapture object
    cap.release()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
