# -*- coding: utf-8 -*-
"""
@Time   ： 2020/5/7 9:04 下午
@Author ： guos
@File   ：serializers.py
@IDE    ：PyCharm

"""
from rest_framework import serializers


class GoodsSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=30, min_length=3, help_text='名字验证')
    goods_front_image = serializers.IntegerField(required=True)
    shop_price = serializers.FloatField(required=True)
    add_time = serializers.DateTimeField(required=True)

