# -*- coding:utf-8 -*-

import urllib.parse
from html.parser import HTMLParser
from datetime import datetime

import requests


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

    message = '''調べてきたよ！

{}

だって！
乗り遅れないようにね～
    '''

    encode = urllib.parse.quote
    now = datetime.now()
    minute = str(now.minute).zfill(2)
    url = 'http://www.jorudan.co.jp/norikae/cgi/nori.cgi?rf=top&eok1=&eok2=R-&pg=0&eki1={}&Cmap1=&eki2={}&Dym={}&Ddd={}&Dhh={}&Dmn1={}&Dmn2={}&Cway=3&Cfp=1&Czu=2&S.x=101&S.y=19&S=%E6%A4%9C%E7%B4%A2&Csg=1'.format(
        encode(_from), encode(_to), "{0:%Y%m}".format(now), now.day, now.hour, minute[0], minute[1]
    )
    print(url)

    response = requests.get(url)
    parser = LastTrainParser()
    parser.feed(response.text)
    parser.result.insert(0, '→'.join([_from, _to]) + ' 最終電車')
    return message.format('\n'.join(parser.result))
