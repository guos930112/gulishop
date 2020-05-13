# -*- coding: utf-8 -*-
"""
@Time   ： 2020/5/11 9:13 下午
@Author ： guos
@File   ：serializers.py
@IDE    ：PyCharm

"""
import re
from datetime import datetime
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import VerifyCode, UserProfile
from gulishop.settings import MOBILE_RE, SEND_INTERVAL_TIMES


class VerifyCodeSerializer(serializers.ModelSerializer):

    def validate_mobile(self, mobile):
        # 手机是否合法：
        ret = re.compile(MOBILE_RE)  # 形成匹配对象
        if not ret.match(mobile):
            raise serializers.ValidationError('mobile is not valid')
        # 手机是否注册过
        if UserProfile.objects.filter(mobile=mobile):
            raise serializers.ValidationError('mobile is registered')
        # 发送短信频率
        ver_list = VerifyCode.objects.filter(mobile=mobile).order_by('-add_time')
        if ver_list:
            ver_code = ver_list[0]
            if (datetime.now() - ver_code.add_time).seconds <= SEND_INTERVAL_TIMES:
                raise serializers.ValidationError('send times is frequently')
            else:
                ver_code.delete()
        return mobile

    class Meta:
        model = VerifyCode
        fields = ['mobile']


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, max_length=30, min_length=11,
                                     validators=[UniqueValidator(queryset=UserProfile.objects.all())])
    password = serializers.CharField(required=True, max_length=20, min_length=6,
                                     write_only=True, style={'input_type': 'password'})
    # write_only只能写不能读，即只能写进来，不能返回前端
    code = serializers.CharField(required=True, max_length=6, min_length=6, write_only=True)

    def validate_code(self, code):
        mobile = self.initial_data['username']
        ver_list = VerifyCode.objects.filter(mobile=mobile, code=code).order_by('-add_time')
        if ver_list:
            last_ver = ver_list[0]
            if (datetime.now() - last_ver.add_time).seconds > 1800:
                raise serializers.ValidationError('verify code is expired')
        else:
            raise serializers.ValidationError('mobile or code is error')

    class Meta:
        model = UserProfile
        fields = ['username', 'password', 'code']
