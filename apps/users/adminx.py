# -*- coding: utf-8 -*-
"""
@Time   ： 2020/5/8 5:24 下午
@Author ： guos
@File   ：adminx.py
@IDE    ：PyCharm

"""
import xadmin
from .models import *


class VerifyCodeAdmin(object):
    """
        手机验证码表
    """
    list_display = ['code', 'mobile', 'add_time']


xadmin.site.register(VerifyCode, VerifyCodeAdmin)
