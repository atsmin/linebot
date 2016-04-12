# -*- coding:utf-8 -*-
import os
import json
import pytz
import random
import urllib.parse
from html.parser import HTMLParser
from datetime import datetime

import requests


KEY = os.environ['KEY']


def shorten_url(long_url):
    url = 'https://www.googleapis.com/urlshortener/v1/url?key={}'.format(KEY)
    headers = {'Content-Type': 'application/json'}
    values = {'longUrl': long_url}
    data = json.dumps(values).encode('utf-8')
    response = requests.post(url, data=data, headers=headers)
    return json.loads(response.text)['id']


def check_last_train(_from, _to):
    class LastTrainParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.found = False
            self.result = []

        def handle_starttag(self, tag, attrs):
            if dict(attrs).get('id') == 'Bk_list_tbody':
                self.found = True

        def handle_endtag(self, tag):
            if self.found and tag == 'tr':
                self.found = False

        def handle_data(self, data):
            if self.found and data != '\n':
                self.result.append(data)

    template = '''調べてきたよ！

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

    encode = urllib.parse.quote
    # UTC to JST
    now = datetime.now().replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Tokyo'))
    url = 'http://www.jorudan.co.jp/norikae/cgi/nori.cgi?Sok=%E6%B1%BA+%E5%AE%9A&eki1={}&eok1=R-&eki2={}&eok2=R-&eki3=&eok3=&eki4=&eok4=&eki5=&eok5=&eki6=&eok6=&rf=nr&pg=0&Dym={}&Ddd={}&Dhh={}&Dmn={}&Cway=3&C1=0&C2=0&C3=0&C4=0&C6=2&Cmap1=&Cfp=1&Czu=2'.format(
        encode(_from), encode(_to), "{0:%Y%m}".format(now), now.day, now.hour, now.minute
    )
    print(url)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; .NET4.0E; .NET4.0C; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729; Tablet PC 2.0; rv:11.0) like Gecko'}

    response = requests.get(url, headers=headers)
    parser = LastTrainParser()
    parser.feed(response.text)
    parser.result.insert(0, '→'.join([_from, _to]) + ' 最終電車')
    return template.format('\n'.join(parser.result), shorten_url(url))
