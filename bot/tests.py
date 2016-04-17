# -*- coding:utf-8 -*-
import unittest

from api import make_message


class LastTrainMessageTest(unittest.TestCase):

    def test_normal(self):
        """正しい入力値の場合は正常に終電時刻を取得できること"""
        text = '上野から鶯谷'
        result = make_message(text)
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

if __name__ == '__main__':
    unittest.main()
