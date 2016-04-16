# -*- coding:utf-8 -*-
import os

import flask

from line import receive, send
from api import make_message

app = flask.Flask(__name__)


@app.route('/', methods=['POST'])
def main():
    user, text = receive()
    message = make_message(text)
    send(user, message)
    return message

if __name__ == '__main__':
    app.run(port=int(os.environ.get('PORT', 5000)))
