import RPi.GPIO as GPIO
import time

pirsensor = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(pirsensor, GPIO.IN)


previous_state = False

current_state = False


while True:
    time.sleep(1)
    previous_state = current_state
    current_state = GPIO.input(pirsensor)
    if current_state != previous_state:
            print("Light Detected!")
    elif current_state == previous_state:
        if current_state:
            print("No Light Detected!")
            
            
    
    
    