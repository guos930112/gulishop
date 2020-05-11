# -*- coding: utf-8 -*-
"""
@Time   ： 2020/5/8 9:10 下午
@Author ： guos
@File   ：filters.py
@IDE    ：PyCharm

"""
from django_filters import rest_framework as filters
from .models import Goods
from django.db.models import Q


class GoodsFilter(filters.FilterSet):
    pricemin = filters.NumberFilter(field_name='shop_price', lookup_expr='gte', label='最低价格')
    pricemax = filters.NumberFilter(field_name='shop_price', lookup_expr='lte', label='最高价格')
    # name = filters.CharFilter(field_name='name', lookup_expr='contains', label='商品名称')
    top_category = filters.NumberFilter(method='get_top_category')  # 当传过来的是一个类别，而商品里没有这个字段，有也是最低级别的类，但是传过来的不一定是最低级别的类

    def get_top_category(self, queryset, name, value):
        # Q 或 的意思
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(
            category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        # fields = ['minprice', 'maxprice', 'name']
        fields = ['pricemin', 'pricemax']  # 参数需要和前端传参对应上
