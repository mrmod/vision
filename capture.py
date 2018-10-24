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
    def camera_image(self):
        preview = gp.check_result(
            gp.gp_camera_capture_preview(self.camera))
        preview_data = gp.check_result(
            gp.gp_file_get_data_and_size(preview))
        # Convert the preview data to an image
        # 1 CV_LOAD_IMAGE_COLOR: 3 Channel color image
        return cv2.imdecode(
            np.array(memoryview(preview_data)), 1)
    def stream(self):
        while (True):
            image = self.camera_image()
            kp = self.orb.detect(image, None)
            kp, des = self.orb.compute(image, kp)
            frame = cv2.drawKeypoints(image, kp, None, color=(0,0,255), flags=0)
            # Find keypoints
            if not self.blurry(image) and self.stable(kp):
                print("Good image")
            # Display
            cv2.imshow('frame', frame)
            key = cv2.waitKey(25) # 25 ms wait for a keypress
            if key == ord('q'):
                break
            else:
                self.zoom(key)
    def blurry(self, image):
        # Laplacian variance
        v = cv2.Laplacian(image, cv2.CV_64F).var()
        # n > 80 : Pretty good human
        # n > 40 : With a struggle; hand-writing @ 1ft
        # n < 10 : Utter rubbish
        # Always, always, always, you terrible photographer
        if v > 45:
            return False
        return True
    def stable(self, keypoints):
        # > 400 : Very good human
        # > 250 : Camera is fairly stable
        # > 150 : Well, at least it's in someone's hands
        if len(keypoints) > 280:
            return True
        return False

    def zoom(self, key):
        # Focus on a point further away
        if key == ord('i'):
            self.zoom_in()
        # Focus on a nearer point
        if key == ord('o'):
            self.zoom_out()
    def zoom_out(self):
        w = gp.check_result(gp.gp_widget_new(gp.GP_WIDGET_TEXT, "focus"))
        gp.gp_widget_set_name(w, "manualfocusdrive")
        gp.gp_widget_set_value(w, "Near 3")
        gp.gp_camera_set_single_config(self.camera, "manualfocusdrive", w)

    def zoom_in(self):
        w = gp.check_result(gp.gp_widget_new(gp.GP_WIDGET_TEXT, "focus"))
        gp.gp_widget_set_name(w, "manualfocusdrive")
        gp.gp_widget_set_value(w, "Far 3")
        gp.gp_camera_set_single_config(self.camera, "manualfocusdrive", w)

    def configuration(self):
        for option in self.camera.list_config():
            print(option[0])

if __name__ == "__main__":
    canon = CanonCapture()
    #canon.configuration()
    canon.stream()
