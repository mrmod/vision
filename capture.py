#!/usr/bin/env python3

import io
import os
import subprocess as sp
import sys

import gphoto2 as gp
import numpy as np
import cv2
def zoom(key, camera):
    # Focus on a point further away
    if key == ord('k'):
        print("Zooming in")
        w = gp.check_result(gp.gp_widget_new(gp.GP_WIDGET_TEXT, "focus"))
        gp.gp_widget_set_name(w, "manualfocusdrive")
        gp.gp_widget_set_value(w, "Far 3")
        gp.gp_camera_set_single_config(camera, "manualfocusdrive", w)
    # Focus on a nearer point
    if key == ord('j'):
        print("Zooming out")
        w = gp.check_result(gp.gp_widget_new(gp.GP_WIDGET_TEXT, "focus"))
        gp.gp_widget_set_name(w, "manualfocusdrive")
        gp.gp_widget_set_value(w, "Near 3")
        gp.gp_camera_set_single_config(camera, "manualfocusdrive", w)

camera = gp.check_result(gp.gp_camera_new())
gp.check_result(gp.gp_camera_init(camera))
orb = cv2.ORB_create()
#config = camera.list_config()
config = gp.check_result(gp.gp_camera_list_config(camera))
# set_single_config, set_config, get_config
#for e in config:
#    print("Config element", e)
def feature_index(config, feature):
    i = -1
    for f in config:
        if f[0] == feature:
          return i
        i+=1
focus = feature_index(config, "manualfocusdrive")
while (True):
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
    key = cv2.waitKey(25) # 25 ms wait for a keypress
    if key == ord('q'):
        break
    zoom(key, camera)
