from camera import cameraThread
from network import mqttThread
import time
import json
import os

# Mount usb drive

os.system("sudo mount /dev/sda1 /media/usb -o uid=pi,gid=pi")

# load settings from file

settings = None

with open('/media/usb/settings.json') as data_file:
    settings = json.load(data_file)

m = mqttThread(
    settings["clientID"],
    settings["brokerURL"],
    settings["brokerPort"],
    settings["captureTopic"],
    settings["shutdownTopic"],
    cameraThread(settings["localImageFolder"], settings["camera_settings"]),
)

m.run()
