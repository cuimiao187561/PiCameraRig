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
        self.camera.annotate_text_size = 128

        self.camera.resolution = (2592, 1944)
        self.camera.led = False

        self.camera.annotate_text = ""

        # load settings
        self.camera.hflip = settings["hflip"]
        self.camera.vflip = settings["vflip"]

    def update_annotation(self, text, color_string):
        self.camera.annotate_text = text
        self.camera.annotate_background = picamera.Color.from_string(color_string)

    def capture(self):
        #hide text
        text = self.camera.annotate_text
        self.camera.annotate_text = ""

        now = time.time()
        self.camera.capture(self.filePath + str(now) + '.jpg')

        self.camera.annotate_text = text

    def update_setting(self, setting, value):
        setattr(self.camera, setting, int(value))
        print getattr(self.camera, setting)
