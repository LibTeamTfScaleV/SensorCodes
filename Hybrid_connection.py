import paho.mqtt.client as mqtt
import urllib
import RPi.GPIO as GPIO
from time import sleep
import random 
## Set up connection / define server
MQTTBROKER = 'iot.eclipse.org'
PORT = 1883
client = mqtt.Client()
client.connect(MQTTBROKER,PORT)
client.on_connect = on_connect
#GPIO ports(Replace as needed)
Port_list = [1,2,3,4]
 
#Functions
def on_connect(client, userdata, flags, rc):
    print("Connected with result code" +str(rc))
    client.subscribe("sensor/light")
    
def on_disconnect(client, userdata, rc):
    print("Disconnected with result code" +str(rc))
    
def on_message(client, userdata, msg):
    print(MQTTBROKER + ': <' +msg.topic + "> : " + str(msg.payload.decode()))
    if(msg.payload.decode().equals("Done1")):
        i = 0
        while i <= len(Port_list):
            client.publish("sensor/light","Sensor %s output %s"%(Port_list[i]),str(random.randint(0,1)))
            i += 1
        client.publish("pi/notify","Done")
#Initial boot loop
i = 0
while i <= len(Port_list):
    client.publish("sensor/light","Sensor %s output %s"%(Port_list[i]),str(random.randint(0,1))));
    i += 1;
    sleep(1)
client.publish("pi/notify","Done")
client.on_message = on_message
client.on_disconnect = on_disconnect
client.loop_forever()
    
