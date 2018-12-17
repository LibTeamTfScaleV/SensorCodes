import RPi.GPIO as GPIO
import urllib.request as urlopen
import time
GPIO.setmode(GPIO.BCM)
chan_list = [5,6,7,13]
GPIO.setup(chan_list, GPIO.IN)

while True:
    i = 0
    count = 1
    while i <= len(chan_list):
        chan_list = str(chan_list)
        url = "https://api.thingspeak.com/update?api_key = 7ZCH92AZ732EPYSY&field1=%s&field2=%s"%(chan_list[i],count)
        data = urlopen.Request(url)
        print(data)
        i+=1
        count+=1
        time.sleep(1)
