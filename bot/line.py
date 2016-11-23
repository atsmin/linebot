# -*- coding:utf-8 -*-
import os
import json

import requests
import flask


TOKEN = os.environ.get('TOKEN')
PROXY = os.environ.get('PROXY')


def receive():
    event = json.loads(flask.request.data.decode('utf-8'))['events'][0]
    return event['replyToken'], event['message']['text']


def send(replyToken, text):
    url = 'https://api.line.me/v2/bot/message/reply'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(TOKEN),
    }
    values = {
        'replyToken': replyToken,
        'messages': [{
            "type": 'text',
            "text": text
        }]
    }
    proxies = {'http': PROXY, 'https': PROXY}
    data = json.dumps(values).encode('utf-8')
    response = requests.post(url, data=data, headers=headers, proxies=proxies)
    return response
