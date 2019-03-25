import database
import config
import datetime
import telebot


def get_list_of_currency(bot):
    query = 'SELECT * FROM general_info'
    text = database.db_execute_query(query)
    message = ''
    for line in text:
        a = 'Чтобы узнать цену за {} {} \nнапишите команду "/get {}"\n\n'.format(line[2], line[3], line[1])
        message += a
    bot.send_message(config.my_chat_id, message)


def get_current_rate(currency, bot):
    now = datetime.datetime.now()
    today_date = now.strftime("%Y.%m.%d")
    if database.check_for_actual_information():
        print("Нужно обновить базу")
        database.insert_new_information(today_date)
    query = 'SELECT price FROM prices WHERE currency_code = "{}" AND date = "{}"'.format(currency, today_date)
    text = database.db_execute_query(query)[0][0]
    message = 'Курс {} на сегодняшний день составляет {} руб.'.format(currency, text)
    bot.send_message(config.my_chat_id, message)


""" Команда get---------------------------------------------------------------------------------------------GET-----
    имеет две сигнатуры get и get <валюта>
    В первом случае выводит список доступных валют,
    во втором текущий курс для заданной валюты"""


def parse_get_command(message, bot):
    pos = message.text.find('/get')
    currency = message.text[pos + 4:].split()
    print(currency[0])
    query = 'SELECT currency_code FROM general_info'
    response = database.db_execute_query(query)
    if currency[0] in response:
        print('запрос курса {}'.format(currency))
        get_current_rate(currency, bot)
