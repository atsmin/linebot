# -*- coding:utf-8 -*-
import os
import json

import requests
import flask


TOKEN = os.environ.get('TOKEN')
PROXY = os.environ.get('PROXY')


def receive():
    event = json.loads(flask.request.data.decode('utf-8'))['events'][0]
    reply_token = event.get('replyToken')
    event_type = event['type']
    if event_type == 'message':
        text = event['message']['text']
    else:
        text = None
    return reply_token, event_type, text


def send(reply_token, text):
    url = 'https://api.line.me/v2/bot/message/reply'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(TOKEN),
    }
    values = {
        'replyToken': reply_token,
        'messages': [{
            "type": 'text',
            "text": text
        }]
    }
    proxies = {'http': PROXY, 'https': PROXY}
    data = json.dumps(values).encode('utf-8')
    response = requests.post(url, data=data, headers=headers, proxies=proxies)
    return response
