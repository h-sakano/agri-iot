# coding: utf-8
import RPi.GPIO as GPIO
import dht11
import yl69
import time
import datetime

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# read data using pin 11
dht11 = dht11.DHT11(pin=11)
yl69 = yl69.YL69(pinCLK=2, pinDIO=4, pinCS=3, pinYl69Vcc=5)

while True:
    dht11Result = dht11.read()
    if dht11Result.is_valid():
        print("Last valid input: " + str(datetime.datetime.now()))
        print("Temperature: %d C" % dht11Result.temperature)
        print("Humidity: %d %%" % dht11Result.humidity)

    yl69Result = yl69.getResult(0)
    print("Soil moisture: %d" % yl69Result)

    time.sleep(1)