import database
import config
import datetime


def get_list_of_currency():
    query = 'SELECT * FROM general_info'
    text = database.db_execute_query(query)
    for line in text:
        message = 'Чтобы узнать цену за {} {} \nнапишите команду /get {}\n'.format(line[2], line[3], line[1])
        print(message)


def get_current_rate(currency):
    now = datetime.datetime.now()
    today_date = now.strftime("%Y.%m.%d")
    if database.check_for_actual_information():
        print("Нужно обновить базу")
        database.insert_new_information(today_date)
    query = 'SELECT price FROM prices WHERE currency_code = "{}" AND date = "{}"'.format(currency, today_date)
    text = database.db_execute_query(query)[0][0]
    message = 'Курс {} на сегодняшний день составляет {} руб.'.format(currency, text)
    print(message)
