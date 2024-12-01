import os
from time import sleep
from requests import get
import datetime


while True:
    sleep(60)
    if not get('https://fonts.ladybrill.ru').ok:
        os.system('systemctl stop flask.socket')
        os.system('systemctl restart flask.service')
        print(f'{datetime.datetime.now()} -> Сервер перезапущен')
