#!/usr/bin/env python3

import io
import socket
import struct
import time
import picamera

client_socket = socket.socket()
client_socket.connect(("10.0.0.27", 8000))

connection = client_socket.makefile('wb')

try:
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)
    camera.start_preview()
    time.sleep(2)

    stream =io.BytesIO()
    for preview in camera.capture_continuous(stream, "jpeg"):
        connection.write(struct.pack("<L", stream.tell()))
        connection.flush()
        # Rewind and send the image
        stream.seek(0)
        connection.write(stream.read())
        # Reest for next capture
        stream.seek(0)
        stream.truncate()
    # Send the done signal
    connection.write(struct.pack("<L", 0))
finally:
    connection.close()
    client_socket.close()

