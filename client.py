#!/usr/bin/env python3

import io
import socket
import struct
import time
import picamera
import sys

def stream_photos(camera, connection):
    stream = io.BytesIO()
    for preview in camera.capture_continuous(stream, "jpeg"):
        connection.write(struct.pack("<L", stream.tell()))
        connection.flush()
        # Rewind and send the image
        stream.seek(0)
        connection.write(stream.read())
        # Reest for next capture
        stream.seek(0)
        stream.truncate()
    connection.write(struct.pack("<L", 0))
    # Send the done signal
def run(srv_addr):
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)
    camera.start_preview()
    client_socket = socket.socket()
    client_socket.connect((srv_addr, 8000))
    connection = client_socket.makefile('wb')
    try:
        stream_photos(camera, connection)
    except BrokenPipeError as e:
        print("Server shutdown. Exiting...")
    finally:
        connection.close()
        client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Need a server address")
        sys.exit(1)
    try:
        run(sys.argv[1])
    except ConnectionRefusedError as e:
        print("Server is down")
