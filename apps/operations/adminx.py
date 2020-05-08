# -*- coding: utf-8 -*-
"""
@Time   ： 2020/5/6 5:33 下午
@Author ： guos
@File   ：adminx.py
@IDE    ：PyCharm

"""
import xadmin
from .models import *


class UserFavAdmin(object):
    """
        用户收藏表
    """
    list_display = ['user', 'goods', 'add_time']


class UserLeavingMessageAdmin(object):
    """
        用户留言表
    """
    list_display = ['user', 'msg_type', 'subject', 'message', 'file', 'add_time']


class UserAddressAdmin(object):
    """
        用户收货地址信息表
    """
    list_display = ['user', 'province', 'city', 'district', 'signing_name', 'signing_mobile', 'address', 'add_time']


xadmin.site.register(UserFav, UserFavAdmin)
xadmin.site.register(UserLeavingMessage, UserLeavingMessageAdmin)
xadmin.site.register(UserAddress, UserAddressAdmin)

