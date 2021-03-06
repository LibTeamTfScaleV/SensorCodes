import time
import smbus
import RPi.GPIO as GPIO
import subprocess
from time import sleep
from urllib2 import urlopen

#api key (input here)

api_key= #Replace with api key

#GPIO/List initiation
channel = 5
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)
light_list = [4,17,27,22]
x = 0
for x in range(len(light_list)):
    GPIO.setup(light_list[x], GPIO.IN)
chair_list = [5,6,7,8]

i2c_ch = 1

# TMP102 address on the I2C bus
i2c_address = 0x48

# Register addresses
reg_temp = 0x00
reg_config = 0x01

# Calculate the 2's complement of a number
def twos_comp(val, bits):
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    return val

# Read temperature registers and calculate Celsius
def read_temp():

    # Read temperature registers
    val = bus.read_i2c_block_data(i2c_address, reg_temp, 2)
    temp_c = (val[0] << 4) | (val[1] >> 5)

    # Convert to 2s complement (temperatures can be negative)
    temp_c = twos_comp(temp_c, 12)

    # Convert registers value to temperature (C)
    temp_c = temp_c * 0.0625

    return temp_c

# Initialize I2C (SMBus)
bus = smbus.SMBus(i2c_ch)

# Read the CONFIG register (2 bytes)
val = bus.read_i2c_block_data(i2c_address, reg_config, 2)
print("Old CONFIG:", val)

# Set to 4 Hz sampling (CR1, CR0 = 0b10)
val[1] = val[1] & 0b00111111
val[1] = val[1] | (0b10 << 6)

# Write 4 Hz sampling back to CONFIG
bus.write_i2c_block_data(i2c_address, reg_config, val)

# Read CONFIG to verify that we changed it
val = bus.read_i2c_block_data(i2c_address, reg_config, 2)
print("New CONFIG:", val)

#For loop / the main show
def Main_program():
    while True:
        temperature = read_temp()
        package = urlopen("https://api.thingspeak.com/update?api_key=%s&field1=%s&field2=%s&field3=%s&field4=%s&field5=%s&field6=%s"%(str(api_key),str(GPIO.input(light_list[0])),str(GPIO.input(light_list[1])),str(GPIO.input(light_list[2])),str(GPIO.input(light_list[3])),str(temperature),str(GPIO.input(channel))))
#Output / response code
        print("\n| Chair %s : %s | Chair %s : %s | Chair %s : %s | Chair %s : %s |\n| Temperature : %s C | Noise level : %s |\n" % (
            str(chair_list[0]),
            "Available" if GPIO.input(light_list[0]) == 0 else "Occupied",
            str(chair_list[1]),
            "Available" if GPIO.input(light_list[1]) == 0 else "Occupied",
            str(chair_list[2]),
            "Available" if GPIO.input(light_list[2]) == 0 else "Occupied",
            str(chair_list[3]),
            "Available" if GPIO.input(light_list[3]) == 0 else "Occupied",
            str(temperature),
            "Too Noisy" if GPIO.input(channel) == 1 else "Acceptable"))
        print("[Response code] : "+ str(package))
        sleep(1)

while True:
    try:
        Main_program()
    except:
        Main_program()
