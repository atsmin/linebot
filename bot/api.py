# -*- coding:utf-8 -*-
import os
import json
import pytz
import random
import functools
import urllib.parse
from datetime import datetime
from tzlocal import get_localzone

import requests
from bs4 import BeautifulSoup


KEY = os.environ['KEY']


# UTC to JST
def to_jst(func):
    @functools.wraps(func)
    def wrapper(*args, **kwds):
        now = kwds.get('now', datetime.now())
        if get_localzone().zone == 'Asia/Tokyo':
            kwds['now'] = now.replace(tzinfo=pytz.timezone('Asia/Tokyo'))
        else:
            kwds['now'] = now.replace(
                tzinfo=pytz.utc
            ).astimezone(pytz.timezone('Asia/Tokyo'))
        return func(*args, **kwds)
    return wrapper


def shorten_url(long_url):
    url = 'https://www.googleapis.com/urlshortener/v1/url?key={}'.format(KEY)
    headers = {'Content-Type': 'application/json'}
    values = {'longUrl': long_url}
    data = json.dumps(values).encode('utf-8')
    response = requests.post(url, data=data, headers=headers)
    return json.loads(response.text)['id']


@to_jst
def make_message(text, now=datetime.now()):
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
調べたんだけど経路が見つからないや
駅名があってるか確認してね！'''

    try:
        _from, _to = text.split(sep)
    except ValueError:
        return invalid
    else:
        result, url = check_last_train(_from, _to, now=now)
        if not result:
            return not_found
        else:
            try:
                time = datetime.strptime(
                    result[2].split(' → ')[0][:-1], '%m/%d %H:%M'
                ).replace(year=now.year, tzinfo=pytz.timezone('Asia/Tokyo'))
            except ValueError:
                pass
            else:
                # If the last train has already left, check the next first train instead.
                # Jorudan returns the day's last train.
                if time <= now or (0 <= now.hour < 6 and (time - now).total_seconds() // 3600 > 12):
                    result, url = check_last_train(_from, _to, now=now, firstTrain=True)
                    result.insert(0, 'ごめんね、もう終電なかったから始発の時間だよ！')

            return template.format('\n'.join(result), shorten_url(url))


@to_jst
def check_last_train(_from, _to, now=datetime.now(), firstTrain=False):
    mode = 2 if firstTrain else 3
    encode = urllib.parse.quote
    url = 'http://www.jorudan.co.jp/norikae/cgi/nori.cgi?Sok=%E6%B1%BA+%E5%AE%9A&eki1={}&eok1=R-&eki2={}&eok2=R-&eki3=&eok3=&eki4=&eok4=&eki5=&eok5=&eki6=&eok6=&rf=nr&pg=0&Dym={}&Ddd={}&Dhh={}&Dmn={}&Cway={}&C1=0&C2=0&C3=0&C4=0&C6=2&Cmap1=&Cfp=1&Czu=2'.format(
        encode(_from), encode(_to), "{0:%Y%m}".format(now), now.day, now.hour, now.minute, mode
    )
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; .NET4.0E; .NET4.0C; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729; Tablet PC 2.0; rv:11.0) like Gecko'}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        result = [soup.h2.string.replace('\n', '') + ' 最終電車']
        data = [
            td.string for td in soup.find(id='Bk_list_tbody').find('tr').find_all('td')
            if td.string
        ]
        result.extend(data)
    except AttributeError:
        result = None
    return result, url
