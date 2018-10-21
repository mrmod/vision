#!/usr/bin/env python3

import cv2
import numpy as np
import subprocess as sp

cap = cv2.VideoCapture('demo.mjpg')
orb = cv2.ORB_create()
while(cap.isOpened()):
    ret, frame = cap.read()
    # Find keypoints
    kp = orb.detect(frame, None)
    # Get descriptors
    kp, des = orb.compute(frame, kp)
    # draw keypoints
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img = cv2.drawKeypoints(frame, kp, None, color=(0,255,0), flags=0)

    cv2.imshow('frame', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print("Closing capture")
cap.release()
cv2.destroyAllWindows()
