import RPi.GPIO as GPIO
from time import sleep
from urllib.request import urlopen
channel = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

while True:
        data = urlopen("https://api.thingspeak.com/update?api_key=Z0KWDBDNX3X04RON&field1=" + str(GPIO.input(17)));
        print(GPIO.input(channel))
        sleep(0.5)
    