#!/usr/bin/env python3
import io
import cv2
import numpy as np
import socket
import struct
from PIL import Image
server_socket = socket.socket()
server_socket.bind(("10.0.0.27", 8000))
server_socket.listen(0)
connection = server_socket.accept()[0].makefile('rb')
try:
    while True:
        # Read the image length
        l = struct.unpack("<L", connection.read(struct.calcsize("<L")))[0]
        image_stream = io.BytesIO()
        print("Reading ", l, "bytes of image")
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
        cv2.waitKey(10) #Wait 10ms for a keypress
finally:
    connection.close()
    server_socket.close()
