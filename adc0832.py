import time
import RPi.GPIO as GPIO


class ADC0832:
    def __init__(self, pinCLK, pinDI, pinDO, pinCS):
        self.__pinCLK = pinCLK
        self.__pinDI = pinDI
        self.__pinDO = pinDO
        self.__pinCS = pinCS
        GPIO.setup(self.__pinCLK, GPIO.OUT)
        GPIO.setup(self.__pinDI,  GPIO.OUT)
        GPIO.setup(self.__pinDO,  GPIO.IN)
        GPIO.setup(self.__pinCS,  GPIO.OUT)

    # read SPI data from ADC8032
    def getADC(channel):
    	# 1. CS LOW.
        GPIO.output(PIN_CS, True)      # clear last transmission
        GPIO.output(PIN_CS, False)     # bring CS low

    	# 2. Start clock
        GPIO.output(PIN_CLK, False)  # start clock low

    	# 3. Input MUX address
        for i in [1,1,channel]: # start bit + mux assignment
            if (i == 1):
                GPIO.output(PIN_DI, True)
            else:
                GPIO.output(PIN_DI, False)

            GPIO.output(PIN_CLK, True)
            GPIO.output(PIN_CLK, False)

            # 4. read 8 ADC bits
            ad = 0
            for i in range(8):
                GPIO.output(PIN_CLK, True)
                GPIO.output(PIN_CLK, False)
                ad <<= 1 # shift bit
                if (GPIO.input(PIN_DO)):
                    ad |= 0x1 # set first bit

            # 5. reset
            GPIO.output(PIN_CS, True)

            return ad
