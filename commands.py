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
    try:
        query = 'SELECT price FROM prices WHERE currency_code = "{}" AND date = "{}"'.format(currency, today_date)
        response_currency = database.db_execute_query(query)[0][0]
        query_count = 'SELECT currency_count FROM general_info WHERE currency_code = "{}"'.format(currency)
        response_count = database.db_execute_query(query_count)[0][0][0]
    except:
        print('Ошибка в get_current_rate')
    message = 'Цена {} {} на сегодняшний день составляет {} руб.'.format(response_count, currency, response_currency)
    bot.send_message(config.my_chat_id, message)


""" Команда get---------------------------------------------------------------------------------------------GET-----
    имеет две сигнатуры get и get <валюта>
    В первом случае выводит список доступных валют,
    во втором текущий курс для заданной валюты"""


def parse_get_command(message, bot):
    pos = message.text.find('/get')
    split_message = message.text[pos + 4:].split()
    if len(split_message) == 0:
        get_list_of_currency(bot)
        return
    currency_ = split_message[0].upper()
    query = 'SELECT currency_code FROM general_info'
    response = database.db_execute_query(query)
    for tup in response:
        if currency_ == tup[0]:
            print('запрос курса {}'.format(currency_))
            get_current_rate(currency_, bot)
            return
    bot.send_message(config.my_chat_id, 'Некорректная валюта')
