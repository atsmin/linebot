# -*- coding:utf-8 -*-

import os

import flask

from line import receive, send
from api import check_last_train

app = flask.Flask(__name__)


@app.route('/', methods=['POST'])
def main():
    user, text = receive()
    result = check_last_train(*text.split('から'))
    print(result)
    send(user, result)
    return 'Done'

if __name__ == '__main__':
    app.run(port=int(os.environ.get('PORT', 5000)))
