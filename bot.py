# -*- coding: utf-8 -*-
import config
import requests
from time import sleep


URL = "https://api.telegram.org/bot{}/".format(config.token)



param = {'chat_id': 350378109, 'text': 'Hello!'}
requests.post(URL + 'sendMessage', data=param)


def get_updates_json():
    response = requests.get(URL + 'getUpdates')
    return response.json()


def get_last_update(response):
    result = response['result']
    len = len(result)
    return result[len-1]


def send_echo_answer(lastupdate):
    param = {'chat_id': lastupdate['message']['chat']['id'],
             'text': lastupdate['message']['text']}
    response = requests.post(URL + 'sendMessage', data=param)
    return response


def echo_bot_function():
    last_update_id = 0
    while 1:
        response = get_updates_json()
        lastupdate = get_last_update(response)
        if lastupdate['update_id'] == last_update_id:
            pass
        else:
            send_echo_answer(lastupdate)
        sleep(2)


def main():
    echo_bot_function()


if __name__ == '__main__':
    main()
