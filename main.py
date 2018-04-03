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
    LINE_ACCESS_TOKEN = f.read().rstrip("\n")
with open('conf/line/user_id.txt') as f:
    LINE_USER_ID = f.read().rstrip("\n")

line_bot_api = LineBotApi(LINE_ACCESS_TOKEN)

# initialize others
lastThirsty = datetime.datetime(1970, 1, 1)
lastWatering = datetime.datetime(1970, 1, 1)
lastSleepDay = 0
lastMorningDay = datetime.datetime.now().day

# read data using pin 11
dht11 = dht11.DHT11(pin=11)
yl69 = yl69.YL69(pinCLK=2, pinDIO=4, pinCS=3, pinYl69Vcc=5)

# const
THIRSTY_THRESH = 170
WATERING_THRESH = 70
SLEEP_HOUR = 22
MORNING_HOUR = 9

def push_message_with_time_check(line_user_id, text_send_message):
    if MORNING_HOUR <= now.hour and now.hour <= SLEEP_HOUR:
        line_bot_api.push_message(line_user_id, text_send_message)

while True:
    now = datetime.datetime.now()

    if now.hour >= SLEEP_HOUR and lastSleepDay < now.day:
        line_bot_api.push_message(LINE_USER_ID, TextSendMessage(text="今日はもう寝るね！おやすみZzz"))

    if now.hour >= MORNING_HOUR and lastMorningDay < now.day:
        line_bot_api.push_message(LINE_USER_ID, TextSendMessage(text="おはよう！今日もよろしくね！"))

    if now.minute == 0 and now.second == 0:
        while True:
            dht11Result = dht11.read():
            if dht11Result.is_valid():
                print("Temperature: %d C" % dht11Result.temperature)
                print("Humidity: %d %%" % dht11Result.humidity)

                yl69Result = yl69.getResult(0)
                report = "{0}時時点の状況をお知らせするよ！\n温度: {1} ℃\n湿度 {2} %%\n土壌水分: {3}({4}以下は水やり直後、{5}以上はカラカラ状態)".format(now.hour, dht11Result.temperature, dht11Result.humidity, yl69Result, WATERING_THRESH, THIRSTY_THRESH)
                push_message_with_time_check(LINE_USER_ID, TextSendMessage(text=report))
                break

    if now.minute % 2 == 0 and now.second == 30:
        yl69Result = yl69.getResult(0)
        print("Soil moisture: %d" % yl69Result)

        if yl69Result > THIRSTY_THRESH:
            delta = now - lastThirsty
            if delta.seconds > 1800:
                push_message_with_time_check(LINE_USER_ID, TextSendMessage(text='もう喉からから・・・。誰か水ちょうだいm(__)m'))
                lastThirsty = datetime.datetime.now()
        elif yl69Result < WATERING_THRESH:
            if lastWatering < lastThirsty:  # 最後に水やりに喜んだ時間が、最後に喉乾いたメッセージを送信するよりも前の場合
                push_message_with_time_check(LINE_USER_ID, TextSendMessage(text='誰かが水をくれたよ！ありがとう！'))
                lastWatering = datetime.datetime.now()