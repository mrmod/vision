#!/usr/bin/env python3

import cv2
import numpy as np
import subprocess as sp

cap = cv2.VideoCapture('movie.mjpg')
while(cap.isOpened()):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print("Closing capture")
cap.release()
cv2.destroyAllWindows()
