import database
import config
import datetime
import telebot
import re
import matplotlib.pyplot as plt


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


def check_correct_currency_name(currency):
    print('проверка правильности написания валюты')
    query = 'SELECT currency_code FROM general_info'
    currency = currency.upper()
    response = database.db_execute_query(query)
    for tup in response:
        if currency == tup[0]:
            return True
    return False


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


def simple_statistic_command(bot):
    bot.send_message(config.my_chat_id, config.statistic_message)


def parse_statistic_command(message, bot):
    pattern = r'/statistic\s*\b\w\w\w\b(\s*from\s\d\d\d\d\.\d\d\.\d\d)?(\s*to\s\d\d\d\d\.\d\d\.\d\d)?'
    match = re.search(pattern, message.text.lower())
    print(match[0] if match else 'invalid statistic command')
    now = datetime.datetime.now()
    today_date = now.strftime("%Y.%m.%d")
    if not match:
        print('неправильная команда')
        bot.send_message(config.my_chat_id, 'Упс, ошибочка. Некорректная команда')
        simple_statistic_command(bot)
        return
    else:
        currency = re.search(r'\b\w\w\w\b', match[0])
        print('currency = ' + currency[0])
        currency = currency[0]
        from_date = re.search(r'from\s\d\d\d\d\.\d\d\.\d\d', match[0])
        if not from_date:
            from_date = '2018.01.01'
        else:
            from_date = from_date[0][5:]
        print('from date = ' + from_date)
        to_date = re.search(r'to\s\d\d\d\d\.\d\d\.\d\d', match[0])
        if not to_date:
            to_date = today_date
        else:
            to_date = to_date[0][3:]
        print('to date = ' + to_date)
    create_plot_for_statistic(currency, from_date, to_date, bot)


def create_plot_for_statistic(currency, from_date, to_date, bot):
    con = database.db_connect(config.db_name)
    cur = con.cursor()
    query = 'SELECT date, price FROM prices WHERE currency_code = "{}" AND date >= "{}" ' \
            'AND date <= "{}"'.format(currency.upper(), from_date, to_date)
    cur.execute(query)
    text = cur.fetchall()
    date_list = []
    price_list = []
    for a in text:
        date_list.append(a[0])
        price_list.append(a[1])
    plt.plot(date_list, price_list)
    plt.title('Курс {} с {} по {}'.format(currency, from_date, to_date))
    plt.xlabel('дата', fontsize=15)
    plt.ylabel('цена в рублях', fontsize=15)
    n = len(date_list)
    labels = []
    for i in range(10):
        labels.append(i * n / 10)
    plt.xticks(labels, rotation=50)
    path = 'img/' + str(config.my_chat_id) + 'statistic_plot.png'
    plt.tight_layout()
    plt.savefig(path, format='png', dpi=100)
    plt.close()
    with open(path, 'rb') as plot:
        bot.send_photo(config.my_chat_id, plot)

