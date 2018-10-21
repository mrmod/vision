#!/usr/bin/env python3

import os
import subprocess as sp
import sys

import gphoto2 as gp
import numpy as np
import cv2

camera = gp.check_result(gp.gp_camera_new())
gp.check_result(gp.gp_camera_init(camera))
print("Capturing preview")
# print(dir(gp))
# camera.set_config
preview = gp.check_result(gp.gp_camera_capture_preview(camera))
mat = gp.check_result(gp.gp_file_get_data_and_size(preview))
print(mat)
print("Can preview")
cv2.imshow('frame', np.asarray(mat))


