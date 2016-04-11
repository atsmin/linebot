# -*- coding:utf-8 -*-

import os
import json

import requests
import flask


CID = os.environ.get('CID')
CS = os.environ.get('CS')
MID = os.environ.get('MID')
PROXY = os.environ.get('PROXY')


def receive():
    data = json.loads(flask.request.data.decode('utf-8'))
    content = data['result'][0]['content']
    return content['from'], content['text'].split('から')


def send(user, text):
    url = 'https://trialbot-api.line.me/v1/events'
    headers = {
        'Content-Type': 'application/json; charser=UTF-8',
        'X-Line-ChannelID': CID,
        'X-Line-ChannelSecret': CS,
        'X-Line-Trusted-User-With-ACL': MID
    }
    values = {
        'to': [user],
        'toChannel': 1383378250,  # Fixed value
        'eventType': "138311608800106203",  # Fixed value
        'content': {
            "contentType": 1,
            "toType": 1,
            "text": text
        }
    }
    proxies = {'http': PROXY, 'https': PROXY}
    data = json.dumps(values).encode('utf-8')
    print(data)
    response = requests.post(url, data=data, headers=headers, proxies=proxies)
    print(response.status_code)
    print(response.text)
