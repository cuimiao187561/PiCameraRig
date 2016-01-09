#!/usr/bin/env python

import threading
import os
import paho.mqtt.client as mqtt

class mqttThread(threading.Thread):
    # setup the thread object
    # def __init__(self, id, brokerURL, brokerPort, settings):
    def __init__(self, clientID, brokerURL, brokerPort, captureTopic, shutdownTopic, cameraThread):
        threading.Thread.__init__(self)

        # setup thread variables
        self.brokerURL = brokerURL
        self.brokerPort = brokerPort
        self.captureTopic = str(captureTopic)
        self.shutdownTopic = str(shutdownTopic)
        self.cameraThread = cameraThread

        self.client = mqtt.Client(client_id=clientID, clean_session=True)

    def shutdown(self):
        # TODO: report back over MQTT
        print('shuting down...')
        os.system("sudo shutdown -h now")

    def capture(self):
        print "capturing image"
        self.cameraThread.capture()

    def on_message(self, client, userdata, message):
        print("Received message '" + str(message.payload) + "' on topic '"
        + message.topic + "' with QoS " + str(message.qos))

        if message.topic == self.captureTopic:
            self.capture()
        elif message.topic == self.shutdownTopic:
            self.shutdown()

    def run(self):
        self.client.connect(self.brokerURL, self.brokerPort, 60)

        self.client.subscribe(self.captureTopic, qos=0)
        self.client.subscribe(self.shutdownTopic, qos=0)

        self.client.on_message = self.on_message

        print "connected!"
        self.client.loop_forever()
