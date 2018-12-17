import paho.mqtt.client as mqtt
import urllib
import RPi.GPIO as GPIO
from time import sleep
MQTTBROKER = 'iot.eclipse.org'

PORT = 1883

def on_connect(client, userdata, flags, rc):
    print("Connected with result code" +str(rc))
    client.subscribe("lib/pingmaster")
    
def on_disconnect(client, userdata, rc):
    print("Disconnected with result code" +str(rc))
    
def on_message(client, userdata, msg):
    print(MQTTBROKER + ': <' +msg.topic + "> : " + str(msg.payload.decode()))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.connect(MQTTBROKER, PORT)
client.loop_forever()
