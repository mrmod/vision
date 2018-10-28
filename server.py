#!/usr/bin/env python3
import io
import cv2
import numpy as np
import socket
import struct
import subprocess
import sys
import time
from PIL import Image
orb = cv2.ORB_create()
n = 0
lock = time.time() -1
def isstable(orb, image):
    kp = orb.detect(image, None)
    kp, des = orb.compute(image, kp)
    # > 45: not blurry
    # > 80: sharp
    blurriness = cv2.Laplacian(image, cv2.CV_64F).var()
    # > 400: Sharp, > 250 : Acceptable
    # blurriness > 110 in highlight
    print("Blurriness", blurriness, "Focus ", len(kp),"/500")
    if blurriness > 100 and len(kp) > 450:
        print("    Sharp", blurriness, "Focus ", len(kp),"/500")
        return True
    return False
def run_scary(audio):
    print("run_scary")
    # Call music player
    #subprocess.run(["afplay", audio])

server_socket = socket.socket()
server_socket.bind(("10.0.0.16", 8000))
server_socket.listen(0)
connection = server_socket.accept()[0].makefile('rb')
audio = sys.argv[1]
try:
    while True:
        # Read the image length
        l = struct.unpack("<L", connection.read(struct.calcsize("<L")))[0]
        image_stream = io.BytesIO()
        image_stream.write(connection.read(l))
        # Rewind the stream
        image_stream.seek(0)
        preview = Image.open(image_stream)
        # Don't do this. Each image gets a window
        #preview.show()
        #image = cv2.imdecode(memoryview(preview), 1)
        # PIL is RGB, CV2 is BGR Color
        image = cv2.cvtColor(np.array(preview), cv2.COLOR_RGB2BGR)
        cv2.imshow("pi image", image)
        if isstable(orb, image) and lock < time.time():
            lock = time.time()+10
            run_scary(audio)
            n += 1
        cv2.waitKey(10) #Wait 10ms for a keypress
finally:
    connection.close()
    server_socket.close()
