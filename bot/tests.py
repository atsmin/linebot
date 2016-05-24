# -*- coding:utf-8 -*-
import unittest
from datetime import datetime
import pytz

from api import make_message


class LastTrainMessageTest(unittest.TestCase):

    def test_normal(self):
        """正しい入力値の場合は正常に終電時刻を取得できること"""
        text = '上野から鶯谷'
        result = make_message(
            text, now=datetime(2016, 5, 24, 20, 0, tzinfo=pytz.timezone('Asia/Tokyo'))
        )
        assert '上野→鶯谷' in result
        assert '経路1' in result

    def test_invalid(self):
        """不正な入力値の場合はその旨のエラーメッセージを返すこと"""
        text = '不正な入力'
        result = make_message(text)
        expected = '''\
ごめんね、よく分からないや

◯◯から△△

みたいに終電を調べたい駅名を教えてね！'''
        assert result == expected

    def test_not_found(self):
        """入力された駅が見つからない場合はその旨のエラーメッセージを返すこと"""
        text = '未来から過去'
        result = make_message(text)
        expected = '''\
ごめんね、
調べたんだけど経路が見つからないや
駅名があってるか確認してね！'''
        assert result == expected

    def test_same_name(self):
        """同じ駅名が入力された場合もエラーにならないこと"""
        text = '鶯谷から鶯谷'
        result = make_message(text)
        expected = '''\
ごめんね、
調べたんだけど経路が見つからないや
駅名があってるか確認してね！'''
        assert result == expected

    def test_already_left1(self):
        """既に終電がないときは始発の時間を調べて返すこと(1)"""
        text = '横浜から大宮'
        result = make_message(
            text, now=datetime(2016, 5, 24, 23, 30, tzinfo=pytz.timezone('Asia/Tokyo'))
        )
        assert '横浜→大宮' in result
        assert '経路1' in result
        assert '始発の時間' in result

    def test_already_left2(self):
        """既に終電がないときは始発の時間を調べて返すこと(2)"""
        text = '渋谷から鶯谷'
        result = make_message(
            text, now=datetime(2016, 5, 25, 0, 30, tzinfo=pytz.timezone('Asia/Tokyo'))
        )
        assert '渋谷→鶯谷' in result
        assert '経路1' in result
        assert '始発の時間' in result


if __name__ == '__main__':
    unittest.main()
