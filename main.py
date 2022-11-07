import paho.mqtt.client as mqtt #import the client
import time
import random
import threading
from datetime import datetime
from si7021 import *

# === Threads for the app ===

class MQTTThread(threading.Thread):
    """
    The MQTT Thread class do multiple things.
    Generate a client ID for unique client node.
    Handles on_connect and on_message MQTT Events and keep publishing the sensors data to the respective topics.

    1.  **__init__** - Init function handles mqtt connection
    2.  **getClientID** - generates a unique client ID
    3.  **getTimestamp** - Get current timestamp
    4.  **on_connect** - Handles the connection of the MQTT
    5.  **on_message** - Handles when a message is received
    6.  **run** - Main MQTT Thread to keep publishing the sensor data
    """

    # === __init__ ===
    def __init__(self, target, *args):
        super().__init__(target=target, args=args)
        self.client = mqtt.Client(self.getClientID())
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect("localhost", 1883, 60)
        self.client.subscribe("data/conf")
        self.client.loop_start()
    # === getClientID ===
    def getClientID(self):
        l = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        s=""
        for i in range(0,16):
            s=s+l[random.randint(0,25)]
        return s
    # === getTimestamp ===
    def getTimestamp(self):
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        return(str(now))
    # === on_connect ===
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
    # === on_message ===
    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
        payloadV=str((msg.payload).decode('utf-8'))
        topicV=str((msg.topic).decode('utf-8'))
        if(topicV=="data/conf"):
            if(payloadV!=""):
                doSomething=0
    # === run ===
    def run(self, *args):
        print( self._args )
        while 1:
            dataArr=getData() 
            self.client.publish('data/humid',dataArr[0])
            self.client.publish('data/tempC',dataArr[1])
            self.client.publish('data/tempF',dataArr[2])
                
            time.sleep(self._args[1])
        self._target(*self._args)


def funcThreading(say=''):
  print("ThreadName: %s" % say)

mqttThread = MQTTThread(funcThreading, 'MQTTThread',0.5)

mqttThread.start()

while 1:
    # ... to keep the main thread alive ...
    a=0