# -*- coding:utf-8 -*-
import unittest
from unittest import mock
from datetime import datetime

from api import make_message


class LastTrainMessageTest(unittest.TestCase):
    localzone_mock = mock.MagicMock(
        return_value=mock.MagicMock(zone='Asia/Tokyo')
    )

    @mock.patch('api.get_localzone', localzone_mock)
    def test_normal(self):
        """正しい入力値の場合は正常に終電時刻を取得できること"""
        text = '上野から鶯谷'
        result = make_message('message', text, now=datetime(2016, 5, 24, 20, 0))
        self.assertTrue('上野→鶯谷' in result)
        self.assertTrue('経路1' in result)

    def test_invalid(self):
        """不正な入力値の場合はその旨のエラーメッセージを返すこと"""
        text = '不正な入力'
        result = make_message('message', text)
        expected = '''\
ごめんね、よく分からないや

◯◯から△△

みたいに終電を調べたい駅名を教えてね！'''
        self.assertEqual(result, expected)

    def test_not_found(self):
        """入力された駅が見つからない場合はその旨のエラーメッセージを返すこと"""
        text = '未来から過去'
        result = make_message('message', text)
        expected = '''\
ごめんね、
調べたんだけど経路が見つからないや
駅名があってるか確認してね！'''
        self.assertEqual(result, expected)

    def test_same_name(self):
        """同じ駅名が入力された場合もエラーにならないこと"""
        text = '鶯谷から鶯谷'
        result = make_message('message', text)
        expected = '''\
ごめんね、
調べたんだけど経路が見つからないや
駅名があってるか確認してね！'''
        self.assertEqual(result, expected)

    @mock.patch('api.get_localzone', localzone_mock)
    def test_already_left1(self):
        """既に終電がないときは始発の時間を調べて返すこと(1)"""
        text = '横浜から大宮'
        result = make_message('message', text, now=datetime(2016, 5, 24, 23, 30))
        self.assertTrue('横浜→大宮' in result)
        self.assertTrue('経路1' in result)
        self.assertTrue('始発の時間' in result)

    @mock.patch('api.get_localzone', localzone_mock)
    def test_already_left2(self):
        """既に終電がないときは始発の時間を調べて返すこと(2)"""
        text = '渋谷から鶯谷'
        result = make_message('message', text, now=datetime(2016, 5, 25, 0, 30))
        self.assertTrue('渋谷→鶯谷' in result)
        self.assertTrue('経路1' in result)
        self.assertTrue('始発の時間' in result)

    def test_when_followed(self):
        """新規に追加された場合には使い方のメッセージを送ること"""
        result = make_message('follow', None)
        expected = '''\
登録ありがとうございます！

◯◯から△△

みたいに終電を調べたい駅名を教えて下さい、時間を調べてきます！'''
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
