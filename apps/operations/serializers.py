# -*- coding: utf-8 -*-
"""
@Time   ： 2020/5/13 8:33 下午
@Author ： guos
@File   ：serializers.py
@IDE    ：PyCharm

"""
from rest_framework import serializers
from .models import UserFav


class UserFavSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = UserFav
        fields = '__all__'
