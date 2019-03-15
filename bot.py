# -*- coding: utf-8 -*-
import config
import requests


url = "https://api.telegram.org/bot733240319:AAHZRY9w7JThKrkSZ_4cKKBQI_PH_QfHZ8A/"
param = {'chat_id': 350378109, 'text': 'Hello!'}
requests.post(url + 'sendMessage', data=param)

