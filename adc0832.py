# coding: utf-8
import time
import RPi.GPIO as GPIO


class ADC0832(object):
    def __init__(self, pinCLK, pinDIO, pinCS):
        self.__pinCLK = pinCLK
        self.__pinDIO = pinDIO
        self.__pinCS = pinCS
        GPIO.setup(self.__pinCLK, GPIO.OUT)
        GPIO.setup(self.__pinCS,  GPIO.OUT)

    def getResult(self, channel=0):
		GPIO.setup(self.__pinDIO, GPIO.OUT)
		GPIO.output(self.__pinCS, 0)
		
		GPIO.output(self.__pinCLK, 0)
		GPIO.output(self.__pinDIO, 1);  time.sleep(0.000002)
		GPIO.output(self.__pinCLK, 1);  time.sleep(0.000002)
		GPIO.output(self.__pinCLK, 0)
	
		GPIO.output(self.__pinDIO, 1);  time.sleep(0.000002)
		GPIO.output(self.__pinCLK, 1);  time.sleep(0.000002)
		GPIO.output(self.__pinCLK, 0)
	
		GPIO.output(self.__pinDIO, channel);  time.sleep(0.000002)
	
		GPIO.output(self.__pinCLK, 1)
		GPIO.output(self.__pinDIO, 1);  time.sleep(0.000002)
		GPIO.output(self.__pinCLK, 0)
		GPIO.output(self.__pinDIO, 1);  time.sleep(0.000002)
	
		dat1 = 0
		for i in range(0, 8):
			GPIO.output(self.__pinCLK, 1);  time.sleep(0.000002)
			GPIO.output(self.__pinCLK, 0);  time.sleep(0.000002)
			GPIO.setup(self.__pinDIO, GPIO.IN)
			dat1 = dat1 << 1 | GPIO.input(self.__pinDIO)  
		
		dat2 = 0
		for i in range(0, 8):
			dat2 = dat2 | GPIO.input(self.__pinDIO) << i
			GPIO.output(self.__pinCLK, 1);  time.sleep(0.000002)
			GPIO.output(self.__pinCLK, 0);  time.sleep(0.000002)
		
		GPIO.output(self.__pinCS, 1)
		GPIO.setup(self.__pinDIO, GPIO.OUT)

		if dat1 == dat2:
			return dat1
		else:
			return 0
