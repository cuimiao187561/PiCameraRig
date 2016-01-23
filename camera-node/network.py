#!/usr/bin/env python

import threading
import os
import paho.mqtt.client as mqtt
import json

import socket
import fcntl
import struct

import time

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


class mqttThread(threading.Thread):
    # setup the thread object
    # def __init__(self, id, brokerURL, brokerPort, settings):
    def __init__(self, clientID, brokerURL, brokerPort, captureTopic, shutdownTopic, settingsTopic, fallbackLoopTime, cameraThread):
        threading.Thread.__init__(self)

        # setup thread variables
        self.clientID = clientID
        self.brokerURL = brokerURL
        self.brokerPort = brokerPort
        self.captureTopic = str(captureTopic)
        self.shutdownTopic = str(shutdownTopic)
        self.settingsTopic = str(settingsTopic)
        self.fallbackLoopTime = fallbackLoopTime
        self.cameraThread = cameraThread

        self.cameraThread.update_annotation("Camera " + self.clientID + " Connecting...", "blue")

        self.client = mqtt.Client(client_id=clientID, clean_session=True)

    def shutdown(self):
        # TODO: report back over MQTT
        self.client.publish("debug", self.clientID + " shutting down...")
        print('shuting down...')
        os.system("sudo shutdown -h now")

    def capture(self):
        print "capturing image"
        self.cameraThread.capture()

    def update_setting(self, payload):
        settings = json.loads(payload)
        self.client.publish("debug", self.clientID + " updating " + str(settings["setting"])+ " "+str(settings["value"]))
        self.cameraThread.update_setting(settings["setting"],settings["value"])

    def on_message(self, client, userdata, message):
        print("Received message '" + str(message.payload) + "' on topic '" + message.topic + "' with QoS " + str(message.qos))

        if message.topic == self.captureTopic:
            self.capture()
        elif message.topic == self.shutdownTopic:
            self.shutdown()
        elif message.topic == self.settingsTopic:
            self.update_setting(message.payload)

    def on_connect(self, client, userdata, flags, rc):
        print("Connection returned " + str(rc))

    def fallback(self):
        while True:
            self.cameraThread.update_annotation("Camera " + self.clientID + " Fallback Mode: " + str(self.fallbackLoopTime) + "secs", "red")
            self.capture()
            time.sleep(self.fallbackLoopTime)
            print "taking image"

    def run(self):
        #self.client.on_connect = self.on_connect

        print self.brokerURL
        try:
            self.client.connect(self.brokerURL, self.brokerPort, 60)

            self.client.subscribe(self.captureTopic, qos=0)
            self.client.subscribe(self.shutdownTopic, qos=0)
            self.client.subscribe(self.settingsTopic, qos=0)

            self.client.on_message = self.on_message

            print "connected!"
            self.client.publish("debug", self.clientID + " connected IP:" + get_ip_address('eth0'))
            self.cameraThread.update_annotation("Camera " + self.clientID, "green")
            self.client.loop_forever()
        except socket.gaierror:
            print "No Connection"
            self.fallback()
