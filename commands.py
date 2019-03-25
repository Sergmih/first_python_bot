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
        response_count = database.db_execute_query(query_count)[0][0]
        message = 'Цена {} {} на сегодняшний день составляет {} руб.'.format(response_count, currency, response_currency)
        bot.send_message(config.my_chat_id, message)
    except:
        print('Ошибка в get_current_rate')
        bot.send_message(config.my_chat_id, 'Ошибка\n возможно команда была некорректная')


""" Команда get---------------------------------------------------------------------------------------------GET-----
    имеет две сигнатуры get и get <валюта>
    В первом случае выводит список доступных валют,
    во втором текущий курс для заданной валюты
    """


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


""" Команда statistic-----------------------------------------------------------------------------STATISTIC---------
    /statistic показывает помощь по этой команде
    /statistic <currency> from <from_date> to <to_date> строит график курса указанной валюты в заданных датах.
    Если не указана дата начала, то по умолчанию считается 2018.01.01, если не указана дата окончания, то берется
    текущая дата
    """


def parse_statistic_command(message, bot):
    pos = message.text.find('/statistic')
    work_message = message.text[pos + 11:]
    print("work_message = " + work_message)
    pos = work_message.find(' ')
    currency = work_message[:pos]
    work_message = work_message[pos:]
    print("currency = " + currency + " work_message = " + work_message)
    pos = work_message.find('from')
    if pos != -1:
        from_date = work_message[pos+5:pos+15]
    else:
        from_date = '2018.01.01'
    print("from_date = " + from_date)
    pos = work_message.find('to')
    if pos != -1:
        to_date = work_message[pos+5:pos+15]
    else:
        now = datetime.datetime.now()
        today_date = now.strftime("%Y.%m.%d")
        to_date = today_date
    print('to_date = ' + to_date)