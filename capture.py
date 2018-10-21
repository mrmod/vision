#!/usr/bin/env python3

import io
import os
import subprocess as sp
import sys

import gphoto2 as gp
import numpy as np
import cv2
import time
from PIL import Image

camera = gp.check_result(gp.gp_camera_new())
gp.check_result(gp.gp_camera_init(camera))
orb = cv2.ORB_create()
while (True):
    print("Capturing preview")
    # print(dir(gp))
    # camera.set_config
    preview = gp.check_result(gp.gp_camera_capture_preview(camera))
    image = gp.check_result(gp.gp_file_get_data_and_size(preview))
    jpg = memoryview(image)
    dec = cv2.imdecode(np.array(jpg), 1)
    kp = orb.detect(dec, None)
    kp, des = orb.compute(dec, kp)
    frame = cv2.drawKeypoints(dec, kp, None, color=(0,0,255), flags=0)
    cv2.imshow('frame', frame)
    #cv2.imshow('image', dec)
    # Works to show image
    #i = Image.open(io.BytesIO(jpg))
    #i.show()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
	
	
