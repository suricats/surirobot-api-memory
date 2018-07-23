import os
import requests
import json

services_url = os.environ.get('SERVICES_URL')
if services_url is None:
    raise Exception('services_url_not_provided')

headers = {'Content-Type': 'application/json'}


def get_weather(latitude, longitude, time, language):
    data = {'latitude': latitude, 'longitude': longitude, 'time': time, 'language': language}
    data = json.dumps(data)
    res = requests.post(url=services_url+'/api/weather/', data=data, headers=headers)
    if res.status_code == 200:
        return res.json()


def get_crypto(crypto):
    res = requests.get(url=services_url+'/api/crypto/'+crypto, headers=headers)
    if res.status_code == 200:
        return res.json()


def get_news():
    res = requests.get(url=services_url+'/api/news', headers=headers)
    if res.status_code == 200:
        return res.json()
