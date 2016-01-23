#!/usr/bin/env python

import threading
import time
import picamera
import json
import os


class cameraThread(threading.Thread):
    # setup the thread object
    # def __init__(self, id, brokerURL, brokerPort, settings):
    def __init__(self, filePath, settingsFilePath, settings):
        threading.Thread.__init__(self)

        self.filePath = filePath
        self.settingsFilePath = settingsFilePath

        # set up camera
        self.camera = picamera.PiCamera()
        self.camera.start_preview()

        self.camera.resolution = (2592, 1944)

        self.camera.annotate_text = ""

        # load settings
        for key in settings:
            print key, ':', settings[key]

            setattr(self.camera, key, settings[key])

    def update_annotation(self, text, color_string):
        self.camera.annotate_text = text
        self.camera.annotate_background = picamera.Color.from_string(color_string)

    def capture(self):
        # hide text
        text = self.camera.annotate_text
        self.camera.annotate_text = ""

        now = time.time()
        self.camera.capture(self.filePath + str(now) + '.jpg')

        self.camera.annotate_text = text

    def update_setting(self, setting, value):
        # live update
        print "updating " + setting
        setattr(self.camera, setting, value)

        # save setting to file
        data = None
        with open(self.settingsFilePath, 'r+') as data_file:
            data = json.load(data_file)
            data["camera_settings"][setting] = value

            data_file.seek(0)
            json.dump(data, data_file, indent=2)
            data_file.truncate() # clear out the file before saving
