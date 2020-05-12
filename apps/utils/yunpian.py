# -*- coding: utf-8 -*-
"""
@Time   ： 2020/5/12 6:28 下午
@Author ： guos
@File   ：yunpian.py
@IDE    ：PyCharm

"""
import requests, json


class YunPian(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = 'https://sms.yunpian.com/v2/sms/single_send.json'

    def send_msg(self, mobile, code):
        data = {
            'apikey': self.api_key,
            'mobile': mobile,
            'text': '【刘渊先生】您的验证码是{code}。如非本人操作，请忽略本短信'.format(code=code)
        }
        result = requests.post(url=self.single_send_url, data=data).text
        result = json.loads(result)
        return result
