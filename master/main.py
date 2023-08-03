# This is a sample Python script.
from typing import Any

import cv2
import threading
import time
import numpy as np

from ImageDetectionUtil import ImageDetectionUtil
from State import State


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
    global active
    global cap
    global state
    global image
    cap = initCaptureDevice()
    state = State()
    _, image = cap.read()
    active = True

    while active:
        captureLoop()
        controllerLoop()
        viewLoop()



    """
    while True:
        # Read the frame
        _, img = cap.read()
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        sm.update(img)
        print(sm)
        drawPoint(img, sm.lastQRCodeLocation, (255, 0, 0))

        print(sm.lastQRCodeLocation)

        ret, enhanced = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
        # Detect the faces
        faces = face_cascade.detectMultiScale(img, 1.1, 4)

        # Checking for QR code
        
        qrX, qrY = (1, 1)
        if retval:
            qrX, qrY = getCenter2(points)
            cv2.polylines(img, points.astype(int), True, (0, 255, 0), 3)

        # Draw the rectangle around each face and add a center dot
        for (x, y, w, h) in faces:
            # Drawing the outer rectangle

            face = getCenter(x, y, w, h)
            # Drawing the green center square
            drawPoint(img, face, (0, 255, 0))
            a = np.array(face)
            # cv2.rectangle(img, getCenter(x, y, w, h), getCenter(x, y, w, h), (0, 255, 0), 3)
            if retval:

                b = np.array((qrX, qrY))
                drawPoint(img, b, (0, 0, 255))
                dist = np.linalg.norm(a-b)
                cv2.putText(img, str(dist), a, cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2, cv2.LINE_AA)
                print(dist)

        Helper.draw(img, sm.lastFace, (0, 255, 0))
        Helper.draw(img, sm.lastQRCodeLocation, (255, 0, 0))


        enhanced = state.update(img)
        state.draw(enhanced)

        # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # mask of green (36,25,25) ~ (86, 255,255)
        # mask = cv2.inRange(hsv, (36, 25, 25), (86, 255,255))
        # mask = cv2.inRange(hsv, (36, 25, 25), (70, 255, 255))

        # slice the green
        # imask = mask > 0
        # green = np.zeros_like(img, np.uint8)
        # green[imask] = img[imask]

        # Display
        # cv2.line(img, sm.lastFace, sm.lastQRCodeLocation, (0, 0, 0), 3)
        cv2.imshow('Web Capture', enhanced)

        # Stop if escape key is pressed
    """

    # Release the VideoCapture object
    cap.release()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
