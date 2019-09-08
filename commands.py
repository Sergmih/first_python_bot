import database
import config
import datetime
import telebot
import re
import matplotlib.pyplot as plt


def send_me_log(bot, message):
    if config.log_flag:
        bot.send_message(config.my_chat_id, 'Сообщение : {}\n от {} {}'.format(message.text,
                                                                               message.from_user.first_name,
                                                                               message.from_user.last_name))


def get_list_of_currency(bot, chat_id):
    '''
    При получения команды "./get" без аругментов.
    Отправляет сообщение пользователю со списком всех поддерживаемых валют
    '''
    query = 'SELECT * FROM general_info'
    text = database.db_execute_query(query)
    message = ''
    for line in text:
        a = '{} {}({})"\n'.format(line[2], line[3], line[1])
        message += a
    bot.send_message(chat_id, message)


def get_current_rate(currency, bot, chat_id):
    '''
    Функция выдает курс запрошенной валюты
    Перед выполнением запроса проверяется актуальность данных
    '''
    now = datetime.datetime.now()
    today_date = now.strftime("%Y.%m.%d")
    if database.check_for_actual_information():
        print("обновление базы")
        get_today_rate(currency, bot, chat_id)
        bot.send_message(chat_id, 'Пожалуйста подождите\nНужно обновить базу')
        database.insert_new_information(today_date)
    try:
        query = 'SELECT price FROM prices WHERE currency_code = "{}" AND date = "{}"'.format(currency, today_date)
        response_currency = database.db_execute_query(query)[0][0]
        query_count = 'SELECT currency_count FROM general_info WHERE currency_code = "{}"'.format(currency)
        response_count = database.db_execute_query(query_count)[0][0]
        message = 'Цена {} {} на сегодняшний день составляет {} руб.'.format(response_count, currency, response_currency)
        bot.send_message(chat_id, message)
    except:
        print('Ошибка в get_current_rate')
        bot.send_message(chat_id, 'Ошибка\n возможно команда была некорректная')


def get_today_rate(currency, bot, chat_id):
    try:
        date = database.get_last_date()
        year = int(date[0:4])
        month = int(date[5:7])
        day = int(date[8:])
        url = "https://www.cbr.ru/currency_base/daily/?date_req=" + day + "." + month + "." + str(year)
        print(url)
        list = database.get_query_from_link(url, True)
        for item in list:
            if item[0] == currency:
                price = item[1]
        print('нашли ценуhe')
        query_count = 'SELECT currency_count FROM general_info WHERE currency_code = "{}"'.format(currency)
        response_count = database.db_execute_query(query_count)[0][0]
        message = 'Цена {} {} на сегодняшний день составляет {} руб.'.format(response_count, currency, price)
        bot.send_message(chat_id, 'тут будет курс на сегодня')
    except:
        print('Ошибка быстрой валюты')


def check_correct_currency_name(currency):
    '''
    Функция проверяет правильность написания запрощенной валюты. Сверяет со списком валют в базе
    '''
    print('проверка правильности написания валюты')
    query = 'SELECT currency_code FROM general_info'
    currency = currency.upper()
    response = database.db_execute_query(query)
    for tup in response:
        if currency == tup[0]:
            return True
    return False


def parse_get_command(message, bot):
    '''
    Функция парсит команду "/get .."
    Если аргументы отсутствуют то выдается список доступных валют.
    При наличии валюты, проверяется корректность запроса и выдается текущий курс
    '''
    pattern = r'/get\s\b\w\w\w\b'
    match = re.search(pattern, message.text.lower())
    if not match:
        get_list_of_currency(bot, message.chat.id)
        return
    currency_ = match[0][5:8].upper()
    query = 'SELECT currency_code FROM general_info'
    response = database.db_execute_query(query)
    for tup in response:
        if currency_ == tup[0]:
            print('запрос курса {}'.format(currency_))
            get_current_rate(currency_, bot, message.chat.id)
            return
    bot.send_message(message.chat.id, 'Некорректная валюта')


def simple_statistic_command(bot, chat_id):
    '''
    Отправляет сообщение помощи работы с командой "/statistic"
    Вызывается при поступлении этой команды без аргументов
    '''
    bot.send_message(chat_id, config.statistic_message)


def parse_statistic_command(message, bot):
    '''
    Обработка команды "/statistic <currency> ..."
    проверяет корректность, строит график за указанные даты и отправяет пользователю.
    Если не указаны доты начала периода и окончания, то в качестве канача берется 2018.01.01,
    а в качестве окончания сегодняшняя дата
    '''
    pattern = r'/statistic\s*\b\w\w\w\b(\s*from\s\d\d\d\d\.\d\d\.\d\d)?(\s*to\s\d\d\d\d\.\d\d\.\d\d)?'
    match = re.search(pattern, message.text.lower())
    print(match[0] if match else 'invalid statistic command')
    now = datetime.datetime.now()
    today_date = now.strftime("%Y.%m.%d")
    if not match:
        print('неправильная команда')
        simple_statistic_command(bot, message.chat.id)
        return
    else:
        currency = re.search(r'\b\w\w\w\b', match[0])
        print('currency = ' + currency[0])
        currency = currency[0]
        if not check_correct_currency_name(currency):
            bot.send_message(message.chat.id, 'Неправильная валюта')
            return
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
    create_plot_for_statistic(currency, from_date, to_date, bot, message.chat.id)


def create_plot_for_statistic(currency, from_date, to_date, bot, chat_id):
    '''
    создает график для валюты currency, начиная с даты from_date, заканчивая
    датой to_date. охраянет картинку и отправляет запросившему
    '''
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
    labels.append(n - 1)
    plt.xticks(labels, rotation=50)
    path = 'img/' + str(config.my_chat_id) + 'statistic_plot.png'
    plt.tight_layout()
    plt.savefig(path, format='png', dpi=100)
    plt.close()
    with open(path, 'rb') as plot:
        bot.send_photo(chat_id, plot)

