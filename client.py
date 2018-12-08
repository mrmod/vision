#!/usr/bin/env python3

import io
import socket
import struct
import time
import picamera
import sys
import argparse
import datetime
import json

class PhotoStreamer(object):
    def __init__(self, camera, connection, args):
        self._stream = io.BytesIO()
        self.camera = camera
        self.connection = connection
        self.args = args
        self.config = args.__dict__

        self.camera.start_preview()

    def stream(self): 
        counter = 0
        for preview in self.camera.capture_continuous(self._stream, "jpeg"):
            if counter % 10 == 0:
                conter = 0
                self.log(self.camera)
                self.read_settings_file()
                self.update_settings(self.camera)
            counter += 1
            # Write the size of the bytearray
            image_size = self._stream.tell()
            #connection.write(struct.pack("<L", image_size))
            self.connection.write(struct.pack("<L", image_size))
            self.connection.flush()
            # Rewind and send the image
            now_at = self._stream.seek(0)
            self.connection.write(self._stream.read())
            # Reset for next capture
            self._stream.seek(0)
            self._stream.truncate()
        # Send the done signal
        self.connection.close()
    def log(self, camera):
            with open("awbGains", "a+") as f:
                f.write("{} : {}\n".format(datetime.datetime.now(), camera.awb_gains))
            print("{},{},{}".format(datetime.datetime.now(), camera.awb_gains, camera.brightness))
    
    def update_settings(self, camera):
        camera.brightness = args.brightness
        camera.awb_mode = args.awbmode
        camera.contrast = args.contrast
        camera.brightness = args.brightness
    
    def read_settings_file(self ):
        new_config = {}
        try:
            with open("nightview.json") as f:
                new_config = json.load(f)
        except json.JSONDecodeError:
            print("{}: error parsing nightview.json".format(datetime.datetime.now()))

        for key in new_config:
            self.config[key] = new_config[key]
        for key in self.config:
            method = setattr(self.args, key, self.config[key])

    
def run(args):
    camera = picamera.PiCamera(framerate=args.framerate)
    camera.resolution = (640, 480)
    client_socket = socket.socket()
    client_socket.connect((args.server, 8000))
    connection = client_socket.makefile('wb')
    try:
        PhotoStreamer(camera, connection, args).stream()
    except BrokenPipeError as e:
        print("Server shutdown. Exiting...")
    finally:
        connection.close()
        client_socket.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--brightness", type=int, default=50)
    parser.add_argument("--framerate", type=int, default=40)
    parser.add_argument("--server", type=str, default="10.0.0.100")
    parser.add_argument("--awbmode", type=str, default="auto")
    parser.add_argument("--contrast", type=int, default=0, help="-100 0 100")
    args = parser.parse_args()
    try:
        run(args)
    except ConnectionRefusedError as e:
        print("Server is down")
