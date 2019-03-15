# -*- coding: utf-8 -*-
import config
import requests
import telebot
from time import sleep


URL = "https://api.telegram.org/bot{}/".format(config.token)


def get_updates_json():
    response = requests.get(URL + 'getUpdates')
    return response.json()


def get_last_update(response):
    result = response['result']
    lens = len(result)
    return result[lens-1]


def send_echo_answer(lastupdate):
    param = {'chat_id': lastupdate['message']['chat']['id'],
             'text': lastupdate['message']['text']}
    response = requests.post(URL + 'sendMessage', data=param)
    return response


def echo_bot_function():
    lastupdateid = 0
    while 1:
        response = get_updates_json()
        lastupdate = get_last_update(response)
        if lastupdate['update_id'] == lastupdateid or \
                lastupdate['message']['from']['is_bot'] == 'true':
            pass
        else:
            lastupdateid = lastupdate['update_id']
            send_echo_answer(lastupdate)
        sleep(2)


def main():
    echo_bot_function()



if __name__ == '__main__':
    main()
