import paho.mqtt.client as mqtt #import the client
import time
import random
import threading
from datetime import datetime
from si7021 import *

class MQTTThread(threading.Thread):
    def __init__(self, target, *args):
        super().__init__(target=target, args=args)
        self.client = mqtt.Client(self.getClientID())
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect("localhost", 1883, 60)
        self.client.subscribe("data/conf")
        self.client.loop_start()
    def getClientID(self):
        l = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        s=""
        for i in range(0,16):
            s=s+l[random.randint(0,25)]
        return s
    def getTimestamp(self):
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        return(str(now))
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
        payloadV=str((msg.payload).decode('utf-8'))
        topicV=str((msg.topic).decode('utf-8'))
        if(topicV=="data/conf"):
            if(payloadV!=""):
                doSomething=0

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
    a=0