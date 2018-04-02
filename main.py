# coding: utf-8
import RPi.GPIO as GPIO
import dht11
import yl69
import time
import datetime
from linebot import LineBotApi
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# initialize line messaging api
with open('conf/line/access_token.txt') as f:
    LINE_ACCESS_TOKEN = f.read()
with open('conf/line/user_id.txt') as f:
    LINE_USER_ID = f.read()

line_bot_api = LineBotApi(LINE_ACCESS_TOKEN)

# initialize others
lastThirsty = datetime.datetime(1970, 1, 1)
lastWatering = datetime.datetime(1970, 1, 1)

# read data using pin 11
dht11 = dht11.DHT11(pin=11)
yl69 = yl69.YL69(pinCLK=2, pinDIO=4, pinCS=3, pinYl69Vcc=5)

while True:
    now = datetime.datetime.now()

    if now.minute == 0 and now.second == 0:
        dht11Result = dht11.read()
        if dht11Result.is_valid():
            print("Last valid input: " + str(datetime.datetime.now()))
            print("Temperature: %d C" % dht11Result.temperature)
            print("Humidity: %d %%" % dht11Result.humidity)

    if now.minute % 2 == 0 and now.second == 0:
        yl69Result = yl69.getResult(0)
        print("Soil moisture: %d" % yl69Result)

        if yl69Result > 180:
            delta = now - lastThirsty
            if delta.seconds > 1800:
                line_bot_api.push_message(LINE_USER_ID, TextSendMessage(text='もう喉からから・・・。誰か水ちょうだいm(__)m'))
                lastThirsty = datetime.datetime.now()
        if yl69Result < 70:
            if lastWatering < lastThirsty:  # 最後に水やりに喜んだ時間が、最後に喉乾いたメッセージを送信するよりも前の場合
                line_bot_api.push_message(LINE_USER_ID, TextSendMessage(text='誰かが水をくれたよ！ありがとう！'))
                lastWatering = datetime.datetime.now()