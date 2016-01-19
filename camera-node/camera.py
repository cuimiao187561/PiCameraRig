#!/usr/bin/env python

import threading
import time
import picamera


class cameraThread(threading.Thread):
    # setup the thread object
    # def __init__(self, id, brokerURL, brokerPort, settings):
    def __init__(self, filePath, settings):
        threading.Thread.__init__(self)

        # settings
        self.filePath = filePath

        # set up camera
        self.camera = picamera.PiCamera()
        self.camera.start_preview()
        self.camera.resolution = (2592, 1944)
        self.camera.led = False

        # load settings
        self.camera.hflip = settings["hflip"]
        self.camera.vflip = settings["vflip"]

    def capture(self):
        now = time.time()
        self.camera.capture(self.filePath + str(now) + '.jpg')
