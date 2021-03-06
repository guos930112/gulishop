# -*- coding: utf-8 -*-
"""
@Time   ： 2020/5/13 8:33 下午
@Author ： guos
@File   ：serializers.py
@IDE    ：PyCharm

"""
from rest_framework import serializers
from .models import UserFav, UserLeavingMessage, UserAddress
from goods.serializers import GoodsSerializer


class UserFavSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = UserFav
        fields = '__all__'


class UserFavListSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    # 这里goods 是我们userfav 表里外键字段， 它对应了一个商品，所以序列化我们many=False
    # django 本身的 serializer 序列化器没有办法直接序列化外键
    goods = GoodsSerializer(many=False)

    class Meta:
        model = UserFav
        fields = '__all__'


class UserLeavingMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = UserLeavingMessage
        fields = '__all__'


class UserAddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = UserAddress
        fields = '__all__'
