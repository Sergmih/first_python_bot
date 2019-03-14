import requests

url = 'https://api.telegram.org/bot733240319:AAHZRY9w7JThKrkSZ_4cKKBQI_PH_QfHZ8A/'


def get_updates_json(request):
    response = requests.get(request + 'getUpdates')
    return response.json()


def last_update(data):
    results = data['result']
    total_updates = len(results) - 1
    return results[total_updates]


def get_chat_id(update):
    chat_id = update['message']['chat']['id']
    return chat_id


def send_mess(chat, text):
    params = {'chat_id': chat, 'text': text}
    response = requests.post(url + 'sendMessage', data=params)
    return response


get_updates_json(url)

#chat_id = get_chat_id(last_update(get_updates_json(url)))
#ssend_mess(chat_id, 'First message from python')
