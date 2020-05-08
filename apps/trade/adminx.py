# -*- coding: utf-8 -*-
"""
@Time   ： 2020/5/6 5:33 下午
@Author ： guos
@File   ：adminx.py
@IDE    ：PyCharm

"""
import xadmin
from .models import *


class ShopCartAdmin(object):
    '''
        购物车： 谁买谁 买了几件
    '''
    list_display = ['user', 'goods', 'nums', 'add_time']


class OrderInfoAdmin(object):
    """
        订单表
    """
    list_display = ['user', 'order_sn', 'order_amount', 'trade_no', 'trade_status', 'pay_time', 'signing_name',
                    'signing_mobile', 'address', 'add_time']


class OrderGoodsAdmin(object):
    """
        订单商品表
    """
    list_display = ['order', 'goods', 'nums', 'add_time']


xadmin.site.register(ShopCart, ShopCartAdmin)
xadmin.site.register(OrderInfo, OrderInfoAdmin)
xadmin.site.register(OrderGoods, OrderGoodsAdmin)
