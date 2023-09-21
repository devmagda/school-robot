# This is a sample Python script.
import time
from typing import Any

import cv2
import numpy as np

import Constants
import ImageUtils
from Shapes import Rectangle
from State import State

global active
global cap
global state
global image
global last
global fps_tracker

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


def aid(img):
    p = (1, 1)
    Rectangle.drawLine(img, p, p, Constants.COLOR_RED, 10)


def captureLoop():
    global image, cap, state, last
    _, image = cap.read()
    state.update(image)
    state.visualize(image)


def printFps():
    global last
    diff_sec = (time.time_ns() - last) / 1000000000
    diff_mil = int(diff_sec * 1000)
    last = time.time_ns()
    fps = int(1 / diff_sec)
    print(f'{fps} Fps | {diff_mil} ms -> ')


def viewLoop():
    global image
    global active

    image = ImageUtils.ImageUtils.scaleImage(image, 1.25)
    # aid(image)
    if Constants.MIRROR_VIEW:
        image = ImageUtils.ImageUtils.mirror(image, Constants.MIRROR_HORIZONTAL)
    cv2.imshow('Web Capture', image)
    # print("--------------------------------")


def controllerLoop():
    global active
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        active = False


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    last = 0
    fps_tracker = list()
    cap = initCaptureDevice()
    state = State()
    _, image = cap.read()
    active = True

    while active:
        if Constants.INFO_FPS:
            printFps()
        captureLoop()
        controllerLoop()
        viewLoop()
        # time.sleep(5)

    # Release the VideoCapture object
    cap.release()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
