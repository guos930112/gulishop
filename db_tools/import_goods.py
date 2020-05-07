# -*- coding: utf-8 -*-
"""
@Time   ： 2020/5/7 12:00 下午
@Author ： guos
@File   ：import_goods.py
@IDE    ：PyCharm

"""
import os, sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gulishop.settings")
import django

django.setup()

from goods.models import Goods, GoodsCategory, GoodsImage
from db_tools.data.product_data import row_data

for item in row_data:
    goods = Goods()
    goods.name = item['name']
    goods.goods_brief = item['desc'] if item['desc'] else ''
    goods.desc = item['goods_desc'] if item['goods_desc'] else ''
    goods.market_price = float(item['market_price'].replace('￥', '').replace('元', ''))
    goods.shop_price = float(item['sale_price'].replace('￥', '').replace('元', ''))
    goods.goods_front_image = item["images"][0] if item["images"] else ''

    # 我们导入的数据当中存储的是类别的名字，而不是类别的对象，如果我们要去给外键赋值，得找到这个类别的对象/或者对象id（对象/id映射）
    category_name = item['categorys'][-1]
    category_list = GoodsCategory.objects.filter(name=category_name)  # filter/all 拿到的是对象的列表
    if category_list:
        goods.category = category_list[0]

    goods.save()

    for image in item['images']:
        goods_image = GoodsImage()
        goods_image.goods = goods
        goods_image.image = image
        goods_image.save()
