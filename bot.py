# -*- coding: utf-8 -*-

import config
import telebot
import requests

bot = telebot.TeleBot(config.token)

bot.send_message(350378109, 'Hi!')

url = "https://api.telegram.org/bot733240319:AAHZRY9w7JThKrkSZ_4cKKBQI_PH_QfHZ8A/"
param = {'chat_id': 350378109, 'text': 'Hello!'}
requests.post(url + 'sendMessage', data=param)


@bot.message_handler(content_types=["text"])
def repeater(message):
    bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    bot.polling(none_stop=True)
