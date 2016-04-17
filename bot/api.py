# -*- coding:utf-8 -*-
import os
import json
import pytz
import random
import urllib.parse
from datetime import datetime

import requests
from bs4 import BeautifulSoup


KEY = os.environ['KEY']


def shorten_url(long_url):
    url = 'https://www.googleapis.com/urlshortener/v1/url?key={}'.format(KEY)
    headers = {'Content-Type': 'application/json'}
    values = {'longUrl': long_url}
    data = json.dumps(values).encode('utf-8')
    response = requests.post(url, data=data, headers=headers)
    return json.loads(response.text)['id']


def make_message(text):
    sep = 'から'

    template = '''\
調べてきたよ！

{}
{}

だって！
''' + random.choice([
        '乗り遅れないようにね～',
        '帰り気をつけてね～',
        '飲み過ぎないでね～',
        '歩きスマホはやめてね～',
        'またね～',
        '今日もお疲れ様～',
    ])

    invalid = '''\
ごめんね、よく分からないや

◯◯から△△

みたいに終電を調べたい駅名を教えてね！'''

    not_found = '''\
ごめんね、
調べたんだけど駅が見つからないや
駅名があってるか確認してね！'''

    try:
        _from, _to = text.split(sep)
        result, url = check_last_train(_from, _to)
        if result:
            return template.format('\n'.join(result), shorten_url(url))
        else:
            return not_found
    except ValueError:
        return invalid


def check_last_train(_from, _to):
    # UTC to JST
    now = datetime.now().replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Tokyo'))

    encode = urllib.parse.quote
    url = 'http://www.jorudan.co.jp/norikae/cgi/nori.cgi?Sok=%E6%B1%BA+%E5%AE%9A&eki1={}&eok1=R-&eki2={}&eok2=R-&eki3=&eok3=&eki4=&eok4=&eki5=&eok5=&eki6=&eok6=&rf=nr&pg=0&Dym={}&Ddd={}&Dhh={}&Dmn={}&Cway=3&C1=0&C2=0&C3=0&C4=0&C6=2&Cmap1=&Cfp=1&Czu=2'.format(
        encode(_from), encode(_to), "{0:%Y%m}".format(now), now.day, now.hour, now.minute
    )
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; .NET4.0E; .NET4.0C; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729; Tablet PC 2.0; rv:11.0) like Gecko'}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        result = [soup.h2.string.replace('\n', '') + ' 最終電車'] if soup.h2 else None
        if result:
            data = [
                td.string for td in soup.find(id='Bk_list_tbody').find('tr').find_all('td')
                if td.string
            ]
            result.extend(data)
    except AttributeError:
        result = None
    return result, url
