#!/usr/bin/env python3

import io
import os
import subprocess as sp
import sys

import gphoto2 as gp
import numpy as np
import cv2
class CanonCapture(object):
    def __init__(self):
        self.camera = gp.check_result(gp.gp_camera_new())
        gp.check_result(gp.gp_camera_init(self.camera))
        self.orb = cv2.ORB_create()
    def preview(self):
        while (True):
            # print(dir(gp))
            # camera.set_config
            img_preview = gp.check_result(
                    gp.gp_camera_capture_preview(self.camera))
            image = gp.check_result(
                    gp.gp_file_get_data_and_size(img_preview))
            jpg = memoryview(image)
            dec = cv2.imdecode(np.array(jpg), 1)
            kp = self.orb.detect(dec, None)
            kp, des = self.orb.compute(dec, kp)
            frame = cv2.drawKeypoints(dec, kp, None, color=(0,0,255), flags=0)
            cv2.imshow('frame', frame)
            #cv2.imshow('image', dec)
            key = cv2.waitKey(25) # 25 ms wait for a keypress
            if key == ord('q'):
                break
            self.zoom(key)
    def zoom(self, key):
        # Focus on a point further away
        if key == ord('k'):
            print("Zooming in")
            w = gp.check_result(gp.gp_widget_new(gp.GP_WIDGET_TEXT, "focus"))
            gp.gp_widget_set_name(w, "manualfocusdrive")
            gp.gp_widget_set_value(w, "Far 3")
            gp.gp_camera_set_single_config(self.camera, "manualfocusdrive", w)
        # Focus on a nearer point
        if key == ord('j'):
            print("Zooming out")
            w = gp.check_result(gp.gp_widget_new(gp.GP_WIDGET_TEXT, "focus"))
            gp.gp_widget_set_name(w, "manualfocusdrive")
            gp.gp_widget_set_value(w, "Near 3")
            gp.gp_camera_set_single_config(self.camera, "manualfocusdrive", w)
#config = camera.list_config()
# List of config Tuples [key, value]
#config = gp.check_result(gp.gp_camera_list_config(camera))

if __name__ == "__main__":
    CanonCapture().preview()
