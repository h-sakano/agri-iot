# coding: utf-8
import RPi.GPIO as GPIO
from adc0832 import ADC0832
import time


class YL69(ADC0832):
    def __init__(self, pinCLK, pinDIO, pinCS, pinYl69Vcc):
        super(YL69, self).__init__(pinCLK, pinDIO, pinCS)
        self.__pinYl69Vcc = pinYl69Vcc
        GPIO.setup(self.__pinYl69Vcc, GPIO.OUT)

    def getResult(self, channel=0):
        # データ取得前にYL-69に電圧を印可
        GPIO.output(self.__pinYl69Vcc, True)

        time.sleep(1)

        ret = super(YL69, self).getResult(channel)

        # YL-69の印加電圧を止める
        GPIO.output(self.__pinYl69Vcc, False)

        return ret