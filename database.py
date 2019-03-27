import sqlite3
import requests
import datetime
from bs4 import BeautifulSoup
import config


def db_connect(db_name):
    connection = sqlite3.connect(db_name)
    return connection


def db_execute_query(query):
    '''
    Функиця принимает один параметр - sql запрос
    образабывает его и возвращает ответ, если он есть
    '''
    con = db_connect(config.db_name)
    cur = con.cursor()
    cur.execute(query)
    con.commit()
    return cur.fetchall()


def generate_url_list(start_date, finish_date):
    '''
    Функция генерирующая ссфлки на сайт cbr.ru, для получения курса валют за определенную дату
    необходима при обновлении базы или некоторых других случаев.
    Принимает 2 аргумента:
    дату начала генерации
    и дату конца
    Возвращает список ссылок
    '''
    month_list = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    url_list = []
    from_year = int(start_date[0:4])
    from_month = int(start_date[5:7])
    from_day = int(start_date[8:])
    to_year = int(finish_date[0:4])
    to_month = int(finish_date[5:7])
    to_day = int(finish_date[8:])
    from_day += 1
    for year in range(2018, 2020):
        if year < int(from_year):
            continue
        for i in range(12):
            if year != int(from_year) or i + 1 >= int(from_month):
                for day in range(1, month_list[i] + 1):
                    if i + 1 == int(from_month) and day < int(from_day):
                        continue
                    if year >= to_year and i + 1 >= to_month and day > to_day:
                        return url_list
                    if day < 10:
                        date = "0" + str(day)
                    else:
                        date = str(day)
                    if i+1 < 10:
                        month = "0" + str(i+1)
                    else:
                        month = str(i+1)
                    text = "https://www.cbr.ru/currency_base/daily/?date_req=" + date + "." + month + "." + str(year)
                    url_list.append(text)
    return url_list


def get_last_date():
    '''
    Функция получения даты последней записи в таблице.
    Необходима для проверки актуальности информации в таблице и ее обновления
    Возвращает дату последней записи в таблице
    '''
    con = db_connect(config.db_name)
    cur = con.cursor()
    query = "SELECT date FROM prices ORDER BY date DESC LIMIT 1"
    text = db_execute_query(query)
    return text[0][0]


def reverse_date(date):
    '''функция преобразует дату из формата dd.mm.yyyy в yyyy.mm.dd'''
    new_date = date[6:] + date[2:6] + date[:2]
    return new_date


def insert_new_information(today_date):
    '''
    Функция для заполнения и обновления базы данных
    принимает сегодняшнюю дату, запрашивает дату последней записи в таблице
    и обновляет базу
    '''
    date = get_last_date()
    con = db_connect(config.db_name)
    cur = con.cursor()

    query = 'CREATE TABLE IF NOT EXISTS prices(date TEXT, currency_code TEXT, price REAL)'
    db_execute_query(query)
    con.commit()
    url_list = generate_url_list(date, today_date)
    for url in url_list:
        print(url)
        html_doc = requests.get(url)
        soup = BeautifulSoup(html_doc.text, features="html.parser")

        i = 0
        for currency in soup.find_all('tr'):
            l = list(currency.find_all('td'))
            if i > 0:
                d = {"id": str(l[0])[4:-5], "code": str(l[1])[4:-5], "count": str(l[2])[4:-5],
                     "fullname": str(l[3])[4:-5], "price": str(l[4])[4:-5]}
                price = d.get("price").replace(',', '.')
                date = reverse_date(url[49:])
                query = 'INSERT INTO prices VALUES("' + date + '", "' + d.get("code") \
                        + '", ' + price + ' )'
                db_execute_query(query)
                con.commit()
            i += 1


def check_for_actual_information():
    '''
    проверка актуальности информации в бд. Если сегодняшнего курса валют нет,
    то обновляет базу начиная с последнего присутствующего курса
    '''
    now = datetime.datetime.now()
    today_date = now.strftime("%Y.%m.%d")
    last_record_in_table = get_last_date()
    if last_record_in_table != today_date:
        return True
