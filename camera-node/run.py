from camera import cameraThread
from network import mqttThread
from pins import pinsThread
import time
import json
import os

# Mount usb drive

os.system("sudo mount /dev/sda1 /media/usb -o uid=pi,gid=pi")

# load settings from file

settings = None
settingsFilePath = '/media/usb/settings.json'

with open(settingsFilePath) as data_file:
    settings = json.load(data_file)

m = mqttThread(
    settings["clientID"],
    settings["brokerURL"],
    settings["brokerPort"],
    settings["captureTopic"],
    settings["shutdownTopic"],
    settings["settingsTopic"],
    settings["pinsTopic"],
    settings["fallbackLoopTime"],
    cameraThread(settings["localImageFolder"], settingsFilePath, settings["camera_settings"]),
    pinsThread(settingsFilePath, settings["pin_settings"]),
)

m.run()
